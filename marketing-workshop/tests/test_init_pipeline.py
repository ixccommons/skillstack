import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import init_pipeline  # noqa: E402

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
TEMPLATE_FILENAMES = sorted(p.name for p in TEMPLATES.iterdir() if p.is_file())


class TestFreshInitialization(unittest.TestCase):
    def test_creates_every_template_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "pipeline"
            init_pipeline.main([str(target)])
            for name in TEMPLATE_FILENAMES:
                self.assertTrue((target / name).exists(), f"{name} was not created")

    def test_state_file_is_valid_json_with_identifiers(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "pipeline"
            init_pipeline.main([str(target), "--pipeline-id", "acme-2026-08-29", "--cohort-id", "yc-w26", "--participant-id", "p042"])
            state = json.loads((target / "pipeline-state.json").read_text())
            self.assertEqual(state["pipeline_id"], "acme-2026-08-29")
            self.assertEqual(state["cohort_id"], "yc-w26")
            self.assertEqual(state["participant_id"], "p042")
            self.assertTrue(state["created_at"])
            self.assertTrue(state["updated_at"])
            self.assertEqual(state["current_stage"], "positioning_intake")

    def test_default_pipeline_id_is_derived_deterministically(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "acme-co"
            init_pipeline.main([str(target)])
            state = json.loads((target / "pipeline-state.json").read_text())
            self.assertTrue(state["pipeline_id"].startswith("acme-co-"))


class TestRepeatedInitialization(unittest.TestCase):
    def test_running_twice_does_not_change_existing_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "pipeline"
            init_pipeline.main([str(target)])
            first = (target / "pipeline-state.json").read_text()

            init_pipeline.main([str(target), "--pipeline-id", "different-id"])
            second = (target / "pipeline-state.json").read_text()

            self.assertEqual(first, second)

    def test_running_twice_is_idempotent_for_all_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "pipeline"
            init_pipeline.main([str(target)])
            before = {p.name: p.read_text() for p in target.iterdir() if p.is_file()}

            init_pipeline.main([str(target)])
            after = {p.name: p.read_text() for p in target.iterdir() if p.is_file()}

            self.assertEqual(before, after)


class TestExistingFilePreservation(unittest.TestCase):
    def test_user_edits_to_a_template_file_survive_rerun(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "pipeline"
            init_pipeline.main([str(target)])

            (target / "research.md").write_text("# Approved research — do not touch\n")
            init_pipeline.main([str(target)])

            self.assertEqual(
                (target / "research.md").read_text(),
                "# Approved research — do not touch\n",
            )

    def test_does_not_create_or_touch_brand_brief(self):
        """brand-brief.md belongs to flows/positioning.md, never to this
        script — init_pipeline must not create a placeholder for it."""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "pipeline"
            init_pipeline.main([str(target)])
            self.assertFalse((target / "brand-brief.md").exists())

            (target / "brand-brief.md").write_text("# Brand Brief — Acme\n")
            init_pipeline.main([str(target)])
            self.assertEqual((target / "brand-brief.md").read_text(), "# Brand Brief — Acme\n")

    def test_approved_state_survives_rerun(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "pipeline"
            init_pipeline.main([str(target)])

            state_path = target / "pipeline-state.json"
            state = json.loads(state_path.read_text())
            state["components"]["conversion_asset"]["state"] = "APPROVED"
            state_path.write_text(json.dumps(state, indent=2) + "\n")

            init_pipeline.main([str(target)])

            reloaded = json.loads(state_path.read_text())
            self.assertEqual(reloaded["components"]["conversion_asset"]["state"], "APPROVED")


if __name__ == "__main__":
    unittest.main()
