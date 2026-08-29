#!/usr/bin/env python3
"""Scaffold the optional automation layer (pipeline-state.json and its
companion files) once a brand-brief.md is ready to move past positioning.

    python3 marketing-workshop/scripts/init_pipeline.py .
    python3 marketing-workshop/scripts/init_pipeline.py . \
        --pipeline-id acme-2026-08-29 --cohort-id yc-w26 --participant-id p042

Run this against the same working directory brand-brief.md already lives in
— it never touches brand-brief.md itself, only adds the files research.md
onward need. Copies every file in templates/ into the target directory, then
fills in pipeline-state.json's identifiers and timestamps. Never overwrites a
file that already exists in the target directory — rerunning this against a
pipeline that has DRAFT, APPROVED, or LIVE work in it must not touch that
work. This is what makes the command idempotent and safe to run again after
an interruption.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
TEMPLATES = SKILL / "templates"
STATE_FILENAME = "pipeline-state.json"


def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "pipeline"


def default_pipeline_id(target_dir):
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"{slugify(target_dir.name)}-{date}"


def copy_templates(target_dir):
    """Copy every template file, skipping any that already exist. Returns
    (created, skipped) filename lists, both excluding pipeline-state.json,
    which is handled separately because it needs identifiers filled in."""
    created, skipped = [], []
    for template in sorted(TEMPLATES.iterdir()):
        if not template.is_file() or template.name == STATE_FILENAME:
            continue
        dest = target_dir / template.name
        if dest.exists():
            skipped.append(template.name)
            continue
        dest.write_text(template.read_text())
        created.append(template.name)
    return created, skipped


def init_state(target_dir, pipeline_id, cohort_id, participant_id):
    dest = target_dir / STATE_FILENAME
    if dest.exists():
        return dest, False

    state = json.loads((TEMPLATES / STATE_FILENAME).read_text())
    now = utc_now_iso()
    state["pipeline_id"] = pipeline_id or default_pipeline_id(target_dir)
    if cohort_id:
        state["cohort_id"] = cohort_id
    if participant_id:
        state["participant_id"] = participant_id
    state["created_at"] = now
    state["updated_at"] = now

    dest.write_text(json.dumps(state, indent=2) + "\n")
    return dest, True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("target_dir", help="Directory to create or update the pipeline in")
    parser.add_argument("--pipeline-id", default=None, help="Stable identifier for this pipeline (default: derived from the directory name and today's date)")
    parser.add_argument("--cohort-id", default=None, help="Optional cohort identifier")
    parser.add_argument("--participant-id", default=None, help="Optional participant identifier")
    args = parser.parse_args(argv)

    target_dir = Path(args.target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    created, skipped = copy_templates(target_dir)
    state_path, state_created = init_state(target_dir, args.pipeline_id, args.cohort_id, args.participant_id)

    for name in created:
        print(f"created  {name}")
    for name in skipped:
        print(f"exists   {name}  (left unchanged)")
    if state_created:
        print(f"created  {state_path.name}")
    else:
        print(f"exists   {state_path.name}  (left unchanged — rerun validate_pipeline.py to check it)")

    print(f"\npipeline workspace ready: {target_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
