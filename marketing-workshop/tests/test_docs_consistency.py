"""Cross-file consistency checks for the skill's prose.

The skill is mostly markdown that other markdown points at, so the failures
that matter aren't syntax errors — they're a reference to a file that moved, a
step number that shifted when a flow was rewritten, or an enum value the
document meant to define and didn't. Each of those has happened at least once
in this repo's short history, so they're checked here rather than found in a
session.
"""

import json
import re
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
GENERATED = ("portable/paste", "dist")


def docs():
    """Every hand-written markdown file in the skill, plus the repo README."""
    out = [p for p in sorted(SKILL.rglob("*.md"))
           if not any(part in str(p.relative_to(SKILL)) for part in GENERATED)]
    readme = SKILL.parent / "README.md"
    if readme.exists():
        out.append(readme)
    return out


def schema():
    return json.loads((SKILL / "schemas" / "pipeline-state.schema.json").read_text())


def enum_named(node, key):
    """First `enum` under a property called `key`, anywhere in the schema."""
    if isinstance(node, dict):
        prop = node.get(key)
        if isinstance(prop, dict) and "enum" in prop:
            return prop["enum"]
        for value in node.values():
            found = enum_named(value, key)
            if found:
                return found
    elif isinstance(node, list):
        for value in node:
            found = enum_named(value, key)
            if found:
                return found
    return None


class TestReferencesResolve(unittest.TestCase):
    def test_cited_skill_files_exist(self):
        cited = re.compile(
            r"`((?:flows|references|templates|schemas|scripts|portable)/[A-Za-z0-9_./-]+)`"
        )
        for doc in docs():
            for path in sorted(set(cited.findall(doc.read_text()))):
                with self.subTest(doc=doc.name, path=path):
                    self.assertTrue(
                        (SKILL / path).exists(),
                        f"{doc.name} cites {path}, which doesn't exist",
                    )


class TestStepReferences(unittest.TestCase):
    """A flow rewrite renumbers its steps; the files pointing at them don't."""

    def test_positioning_step_references_resolve(self):
        headings = dict(
            re.findall(
                r"^## Step (\d+) — (.+)$",
                (SKILL / "flows" / "positioning.md").read_text(),
                re.M,
            )
        )
        self.assertTrue(headings, "positioning.md has no numbered steps to check")
        for doc in docs():
            for number in sorted(set(re.findall(r"positioning step (\d+)", doc.read_text()))):
                with self.subTest(doc=doc.name, step=number):
                    self.assertIn(
                        number,
                        headings,
                        f"{doc.name} cites positioning step {number}, which doesn't exist",
                    )


class TestSchemaMatchesDocs(unittest.TestCase):
    def test_every_business_model_is_documented_by_identifier(self):
        models = enum_named(schema(), "business_model")
        self.assertTrue(models, "no business_model enum found in the schema")
        doc = (SKILL / "references" / "business-models.md").read_text()
        for value in models:
            with self.subTest(business_model=value):
                self.assertIn(
                    f"`{value}`",
                    doc,
                    f"business-models.md never names the identifier `{value}`",
                )

    def test_every_pipeline_state_is_documented(self):
        states = enum_named(schema(), "state")
        self.assertTrue(states, "no state enum found in the schema")
        skill = (SKILL / "SKILL.md").read_text()
        for value in states:
            with self.subTest(state=value):
                self.assertIn(f"`{value}`", skill, f"SKILL.md never names `{value}`")


class TestPortableParity(unittest.TestCase):
    def test_every_flow_has_a_paste_file(self):
        flows = {p.stem for p in (SKILL / "flows").glob("*.md")}
        pastes = {p.stem for p in (SKILL / "portable" / "paste").glob("*.md")}
        self.assertEqual(
            flows,
            pastes,
            "portable/paste is out of step with flows/ — rerun portable/build.py",
        )


if __name__ == "__main__":
    unittest.main()
