#!/usr/bin/env python3
"""Validate a working directory's optional automation layer against the
state contract.

    python3 marketing-workshop/scripts/validate_pipeline.py .

Checks, in one run, reporting every problem found rather than stopping at the
first:

  1. required files are present
  2. pipeline-state.json is valid JSON with every required top-level field
  3. every state value (component, asset, campaign, scheduled task) is one of
     the six allowed states
  4. no item has skipped straight to an implemented state without an approval
     recorded for it (an "invalid transition")
  5. no item claims LIVE that the pipeline could not actually have made live —
     missing capability, or no verification recorded. This is the check for
     READY_TO_IMPLEMENT being misrepresented as LIVE.
  6. campaign-plan.csv, weekly-scorecard.csv and experiment-backlog.csv have
     the exact required headers

It also reports whether the launch completion gate (SKILL.md / flows/launch.md)
is currently met, as information rather than a failure — most runs are not at
launch yet, and that is not itself an error.

Exits 0 if no errors were found, 1 otherwise. Standard library only.
"""

import csv
import json
import sys
from pathlib import Path

STATE_FILENAME = "pipeline-state.json"

REQUIRED_FILES = [
    STATE_FILENAME,
    "brand-brief.md",
    "research.md",
    "messaging-guide.md",
    "channel-map.md",
    "campaign-plan.csv",
    "measurement-plan.md",
    "weekly-scorecard.csv",
    "experiment-backlog.csv",
    "launch-checklist.md",
]

ALLOWED_STATES = {
    "MISSING",
    "DRAFT",
    "APPROVED",
    "READY_TO_IMPLEMENT",
    "LIVE",
    "MEASURING",
    "BLOCKED",
}

# States at or past this rank require an approval recorded before the item
# could legitimately have reached them.
STATE_RANK = {
    "MISSING": 0,
    "DRAFT": 1,
    "APPROVED": 2,
    "READY_TO_IMPLEMENT": 3,
    "LIVE": 4,
    "MEASURING": 5,
}
APPROVAL_REQUIRED_RANK = STATE_RANK["APPROVED"]

REQUIRED_TOP_LEVEL_FIELDS = [
    "schema_version",
    "pipeline_id",
    "business",
    "objective",
    "positioning_input",
    "business_model",
    "geography",
    "constraints",
    "capabilities",
    "components",
    "research",
    "assets",
    "campaigns",
    "measurements",
    "scheduled_tasks",
    "approvals",
    "action_log",
    "blockers",
    "current_stage",
    "created_at",
    "updated_at",
]

CSV_HEADERS = {
    "campaign-plan.csv": [
        "date", "owner", "channel", "destination", "action", "asset", "cta",
        "dependency", "effort", "expected_signal", "metric", "decision_rule",
        "status",
    ],
    "weekly-scorecard.csv": [
        "period", "owner", "objective", "metric", "definition", "source",
        "baseline", "current", "target_type", "threshold", "status",
        "decision", "next_action",
    ],
    "experiment-backlog.csv": [
        "id", "hypothesis", "evidence", "variable", "audience", "channel",
        "success_metric", "guardrail", "start_date", "end_date", "owner",
        "status", "result", "decision",
    ],
}

CAPABILITY_FOR_COMPONENT = {
    "conversion_asset": ("cms_write", "publishing_write"),
    "monitoring_task": ("scheduled_tasks",),
    "weekly_report_task": ("scheduled_tasks",),
    "content_brief_task": ("scheduled_tasks",),
}


def validate_required_files(target_dir):
    errors = []
    for name in REQUIRED_FILES:
        if not (target_dir / name).exists():
            errors.append(f"missing required file: {name}")
    return errors


def load_state(target_dir):
    path = target_dir / STATE_FILENAME
    if not path.exists():
        return None, [f"missing required file: {STATE_FILENAME}"]
    try:
        return json.loads(path.read_text()), []
    except json.JSONDecodeError as exc:
        return None, [f"{STATE_FILENAME} is not valid JSON: {exc}"]


def validate_schema(state):
    errors = []
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in state:
            errors.append(f"pipeline-state.json missing required field: {field}")
    if "positioning_input" in state:
        pos = state["positioning_input"]
        if not isinstance(pos, dict) or "status" not in pos or "fields" not in pos:
            errors.append("positioning_input must have 'status' and 'fields'")
        elif pos["status"] not in {"MISSING", "PARTIAL", "ACCEPTED"}:
            errors.append(f"positioning_input.status invalid: {pos['status']!r}")
    return errors


def _iter_stateful_items(state):
    """Yield (label, item_dict) for every object in the state file that
    carries a 'state' field."""
    for name, comp in state.get("components", {}).items():
        if isinstance(comp, dict) and "state" in comp:
            yield f"components.{name}", comp
    for i, asset in enumerate(state.get("assets", [])):
        yield f"assets[{i}] ({asset.get('type', '?')})", asset
    for i, campaign in enumerate(state.get("campaigns", [])):
        yield f"campaigns[{i}] ({campaign.get('channel', '?')})", campaign
    for i, task in enumerate(state.get("scheduled_tasks", [])):
        yield f"scheduled_tasks[{i}] ({task.get('name', '?')})", task
    measurements = state.get("measurements")
    if isinstance(measurements, dict) and "state" in measurements:
        yield "measurements", measurements


def validate_states(state):
    errors = []
    for label, item in _iter_stateful_items(state):
        value = item.get("state")
        if value not in ALLOWED_STATES:
            errors.append(f"{label}: invalid status {value!r}")
    return errors


def validate_transitions(state):
    """An item at APPROVED or beyond must have an approval recorded for it.
    Skipping straight to an implemented state with no approval on file is an
    invalid transition."""
    errors = []
    approved_items = {a.get("item") for a in state.get("approvals", []) if isinstance(a, dict)}
    for label, item in _iter_stateful_items(state):
        value = item.get("state")
        if value in ("BLOCKED", "MISSING", "DRAFT"):
            continue
        if value not in STATE_RANK:
            continue
        if STATE_RANK[value] < APPROVAL_REQUIRED_RANK:
            continue
        name = _item_name(label, item)
        if name not in approved_items:
            errors.append(
                f"{label}: state is {value} but no approvals entry has item={name!r} — invalid transition"
            )
    return errors


def _item_name(label, item):
    for key in ("name", "channel", "type"):
        if key in item:
            return item[key]
    return label.split(".")[-1].split(" ")[0]


def validate_live_claims(state):
    """Detect READY_TO_IMPLEMENT misrepresented as LIVE: a LIVE claim the
    pipeline had no way to actually make live."""
    errors = []
    capabilities = state.get("capabilities", {})
    component_name_by_label = {}
    for name, comp in state.get("components", {}).items():
        component_name_by_label[f"components.{name}"] = name

    for label, item in _iter_stateful_items(state):
        if item.get("state") != "LIVE":
            continue

        comp_name = component_name_by_label.get(label)
        if comp_name in CAPABILITY_FOR_COMPONENT:
            needed = CAPABILITY_FOR_COMPONENT[comp_name]
            if not any(capabilities.get(cap) for cap in needed):
                errors.append(
                    f"{label}: marked LIVE but none of the required capabilities "
                    f"({', '.join(needed)}) are present — this looks like "
                    f"READY_TO_IMPLEMENT represented as LIVE"
                )

        if label.startswith("assets["):
            if not item.get("verified_at"):
                errors.append(
                    f"{label}: marked LIVE with no verified_at — an asset can only "
                    f"be marked LIVE after being read back and verified"
                )
            if not capabilities.get("publishing_write") and not capabilities.get("cms_write"):
                errors.append(
                    f"{label}: marked LIVE but no publishing_write or cms_write "
                    f"capability is present"
                )

        if label.startswith("scheduled_tasks[") and not capabilities.get("scheduled_tasks"):
            errors.append(
                f"{label}: marked LIVE but capabilities.scheduled_tasks is false"
            )

    return errors


def validate_csv_headers(target_dir):
    errors = []
    for filename, expected in CSV_HEADERS.items():
        path = target_dir / filename
        if not path.exists():
            continue  # already reported by validate_required_files
        with path.open(newline="") as f:
            reader = csv.reader(f)
            try:
                actual = next(reader)
            except StopIteration:
                errors.append(f"{filename}: file is empty, expected a header row")
                continue
        if actual != expected:
            errors.append(
                f"{filename}: header mismatch\n"
                f"    expected: {','.join(expected)}\n"
                f"    actual:   {','.join(actual)}"
            )
    return errors


def evaluate_launch_gate(state):
    """The six conditions from flows/launch.md that must all hold before the
    pipeline overall may be called LIVE. Returns (met, reasons_if_not)."""
    reasons = []

    if state.get("positioning_input", {}).get("status") != "ACCEPTED":
        reasons.append("positioning_input is not ACCEPTED")

    live_assets = [a for a in state.get("assets", []) if a.get("state") == "LIVE" and a.get("verified_at")]
    if not live_assets:
        reasons.append("no conversion asset is LIVE and verified")

    active_distribution = [c for c in state.get("campaigns", []) if c.get("state") in ("LIVE", "MEASURING")] or \
        [t for t in state.get("scheduled_tasks", []) if t.get("state") in ("LIVE", "MEASURING")]
    if not active_distribution:
        reasons.append("no distribution action is LIVE or scheduled")

    measurements = state.get("measurements", {})
    if measurements.get("state") not in ("READY_TO_IMPLEMENT", "LIVE", "MEASURING") or not measurements.get("north_star"):
        reasons.append("the desired conversion is not measurable yet (no north_star / measurement plan not ready)")

    if not state.get("approvals"):
        reasons.append("no owners, cadence or decision rules have been approved")

    unresolved_blockers = [b for b in state.get("blockers", []) if isinstance(b, dict)]
    if unresolved_blockers:
        reasons.append(f"{len(unresolved_blockers)} unresolved blocker(s)")

    return (len(reasons) == 0, reasons)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: validate_pipeline.py <target_dir>", file=sys.stderr)
        return 2
    target_dir = Path(argv[0])

    errors = []
    errors += validate_required_files(target_dir)

    state, load_errors = load_state(target_dir)
    errors += load_errors

    if state is not None:
        errors += validate_schema(state)
        errors += validate_states(state)
        errors += validate_transitions(state)
        errors += validate_live_claims(state)

    errors += validate_csv_headers(target_dir)

    if errors:
        print(f"{len(errors)} problem(s) found in {target_dir}:")
        for e in errors:
            print(f"  ! {e}")
    else:
        print(f"{target_dir}: valid")

    if state is not None:
        met, reasons = evaluate_launch_gate(state)
        if met:
            print("launch gate: MET")
        else:
            print("launch gate: NOT MET")
            for r in reasons:
                print(f"    - {r}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
