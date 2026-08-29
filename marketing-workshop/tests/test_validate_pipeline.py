import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import init_pipeline  # noqa: E402
import validate_pipeline  # noqa: E402


def make_pipeline(tmp):
    """A working directory with brand-brief.md (as if positioning already ran)
    plus the automation-layer files from init_pipeline."""
    target = Path(tmp) / "pipeline"
    init_pipeline.main([str(target)])
    (target / "brand-brief.md").write_text("# Brand Brief — Acme\n")
    return target


def load_state(target):
    return json.loads((target / "pipeline-state.json").read_text())


def save_state(target, state):
    (target / "pipeline-state.json").write_text(json.dumps(state, indent=2) + "\n")


class TestValidState(unittest.TestCase):
    def test_fresh_pipeline_has_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            exit_code = validate_pipeline.main([str(target)])
            self.assertEqual(exit_code, 0)

    def test_fresh_pipeline_gate_not_met(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            state = load_state(target)
            met, reasons = validate_pipeline.evaluate_launch_gate(state)
            self.assertFalse(met)
            self.assertTrue(reasons)


class TestMissingRequiredFields(unittest.TestCase):
    def test_missing_top_level_field_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            state = load_state(target)
            del state["objective"]
            errors = validate_pipeline.validate_schema(state)
            self.assertTrue(any("objective" in e for e in errors))

    def test_missing_required_file_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            (target / "research.md").unlink()
            errors = validate_pipeline.validate_required_files(target)
            self.assertTrue(any("research.md" in e for e in errors))

    def test_missing_brand_brief_means_positioning_never_ran(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "pipeline"
            init_pipeline.main([str(target)])  # no brand-brief.md written
            errors = validate_pipeline.validate_required_files(target)
            self.assertTrue(any("brand-brief.md" in e for e in errors))


class TestInvalidStatus(unittest.TestCase):
    def test_unknown_state_value_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            state = load_state(target)
            state["components"]["conversion_asset"]["state"] = "PUBLISHED"
            errors = validate_pipeline.validate_states(state)
            self.assertTrue(any("PUBLISHED" in e for e in errors))


class TestInvalidTransition(unittest.TestCase):
    def test_live_component_without_approval_is_invalid_transition(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            state = load_state(target)
            state["components"]["conversion_asset"]["state"] = "LIVE"
            errors = validate_pipeline.validate_transitions(state)
            self.assertTrue(any("invalid transition" in e for e in errors))

    def test_approved_component_with_approval_on_file_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            state = load_state(target)
            state["components"]["conversion_asset"]["state"] = "APPROVED"
            state["approvals"].append({"item": "conversion_asset", "approved_at": "2026-08-29T00:00:00Z"})
            errors = validate_pipeline.validate_transitions(state)
            self.assertEqual(errors, [])

    def test_live_claim_without_capability_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            state = load_state(target)
            state["components"]["monitoring_task"]["state"] = "LIVE"
            state["approvals"].append({"item": "monitoring_task", "approved_at": "2026-08-29T00:00:00Z"})
            errors = validate_pipeline.validate_live_claims(state)
            self.assertTrue(any("READY_TO_IMPLEMENT" in e for e in errors))

    def test_live_claim_with_capability_present_is_not_flagged_for_that_reason(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            state = load_state(target)
            state["capabilities"]["scheduled_tasks"] = True
            state["components"]["monitoring_task"]["state"] = "LIVE"
            errors = validate_pipeline.validate_live_claims(state)
            self.assertEqual(errors, [])


class TestCsvHeaderValidation(unittest.TestCase):
    def test_correct_headers_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            errors = validate_pipeline.validate_csv_headers(target)
            self.assertEqual(errors, [])

    def test_mismatched_header_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            (target / "campaign-plan.csv").write_text("date,owner,channel\n")
            errors = validate_pipeline.validate_csv_headers(target)
            self.assertTrue(any("campaign-plan.csv" in e for e in errors))


class TestPipelineCompletionGate(unittest.TestCase):
    def test_gate_met_when_all_six_conditions_hold(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            state = load_state(target)
            state["positioning_input"]["status"] = "ACCEPTED"
            state["assets"].append({"type": "homepage", "state": "LIVE", "path": "messaging-guide.md", "verified_at": "2026-08-29T00:00:00Z"})
            state["campaigns"].append({"channel": "newsletter", "state": "LIVE"})
            state["measurements"] = {"north_star": "qualified demo requests", "funnel": "b2b", "plan_path": "measurement-plan.md", "state": "LIVE"}
            state["approvals"].append({"item": "conversion_asset", "approved_at": "2026-08-29T00:00:00Z"})

            met, reasons = validate_pipeline.evaluate_launch_gate(state)
            self.assertTrue(met, reasons)
            self.assertEqual(reasons, [])

    def test_gate_not_met_when_no_conversion_asset_is_live(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = make_pipeline(tmp)
            state = load_state(target)
            state["positioning_input"]["status"] = "ACCEPTED"
            met, reasons = validate_pipeline.evaluate_launch_gate(state)
            self.assertFalse(met)
            self.assertTrue(any("conversion asset" in r for r in reasons))


if __name__ == "__main__":
    unittest.main()
