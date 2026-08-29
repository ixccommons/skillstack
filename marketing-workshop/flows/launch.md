# Launch Flow

Runs once copy, distribution, and measurement each have at least one
component at `APPROVED` or beyond. Verifies the pipeline as a whole, and
decides whether it can be marked `LIVE` or stays `READY_TO_IMPLEMENT`.

This flow only checks and gates. It doesn't build anything new — if a
preflight item fails, the fix happens back in the flow that owns it
(`flows/copy.md`, `flows/distribution.md`, `flows/measurement.md`), not here.

## Preflight

Verify each of these against the actual current state, not against what was
planned:

- Positioning input accepted (`positioning_input.status == ACCEPTED`)
- Research provenance valid — no claim on a live asset traces to `UNKNOWN`
  or an unflagged `ASSUMPTION`
- Conversion asset approved
- Conversion destination works — open it, don't assume it
- Links work — every link in `channel-map.md` and `campaign-plan.csv`,
  checked
- CTA and conversion event agree — the button says what the tracked event
  actually measures
- Claims match evidence — every claim on a live asset traces to
  `research.md` or `reasons_to_believe`
- Owners assigned to every open item in `campaign-plan.csv`
- Dates assigned to every open item
- Tracking identifiers consistent — every link uses the same
  `utm_campaign` for this push
- Required approvals recorded in `pipeline-state.json.approvals`
- Budget ceilings defined for anything with spend
- Baseline captured, or explicitly scheduled with an owner and date
- Distribution path active or scheduled
- Monitoring configured (or specified `READY_TO_IMPLEMENT`, if
  `scheduled_tasks` is absent)

Record results in `launch-checklist.md`. Check an item only when verified —
a plan to do something is not the same as having done it.

## The gate

The pipeline overall may be marked `LIVE` only if all six hold:

1. Positioning input is accepted.
2. At least one conversion asset is live and reachable (read back and
   verified — see `references/execution-policy.md`).
3. At least one distribution action is active or scheduled.
4. The desired conversion is measurable — the measurement plan is at least
   `READY_TO_IMPLEMENT` and a north star is named.
5. Owners, cadence, and decision rules exist — at least one approval is on
   record.
6. External changes were verified, not assumed.

`scripts/validate_pipeline.py`'s `evaluate_launch_gate` checks these
programmatically and is the source of truth for whether the gate is met —
run it rather than eyeballing the checklist.

**If the gate isn't met**, the pipeline stays `READY_TO_IMPLEMENT`. List
only the specific blockers separating it from `LIVE` in
`launch-checklist.md`'s blocker table — not a restatement of the whole
checklist. Each blocker gets the missing capability if that's the cause, an
owner, and a next step.

**If the gate is met**, mark the overall pipeline `LIVE`, record the
verification in `action_log`, and move to `flows/review.md`'s weekly cadence.

Never mark the pipeline `LIVE` to match enthusiasm or a deadline. A
`READY_TO_IMPLEMENT` pipeline with an honest blocker list is more useful than
a `LIVE` one that overstates what actually happened — the whole point of the
state model in `schemas/pipeline-state.schema.json` is that these are
different, checkable claims.
