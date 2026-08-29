# Measurement Flow

Runs after `flows/distribution.md`, or in parallel with it once the channel
choice is approved. Produces `measurement-plan.md`, drives the
`measurement_plan` component, and sets up tracking for everything
`campaign-plan.csv` will point traffic at.

Full metric definitions and the funnel table live in `references/metrics.md`
— this file is the sequence for applying them.

## Sequence

1. **Select the funnel** from `references/metrics.md` matching
   `pipeline-state.json.business_model`. If the business genuinely spans two
   models (see `references/business-models.md`), use the funnel for the one
   `objective` is built around.
2. **Name the north star** — the single outcome this pipeline run is built
   to move. Exactly one. If more than one metric seems equally important,
   that's a sign the objective itself needs to be sharpened first, not a
   reason to name two north stars.
3. **Define leading indicators, guardrails, and diagnostics.** For each:
   owner, source, formula, cadence, baseline, target type, decision
   threshold. A metric with no decision threshold isn't ready for
   `flows/review.md` yet — it's still a diagnostic.
4. **Capture or schedule the baseline.** Use `analytics_read` where it
   exists; otherwise use business-provided numbers (`PROVIDED` per
   `references/evidence-policy.md`). If neither is available yet, schedule
   the capture with an owner and a date rather than leaving it blank —
   `flows/launch.md` checks for one or the other.
5. **Generate tracking links** for every destination in `campaign-plan.csv`
   using `scripts/generate_utm.py`, following the convention in
   `references/metrics.md`. Never hand-build a tracking URL — the generator
   is what keeps parameters deterministic and stops duplicate UTM values
   from piling up when a link gets re-shared.
6. **Specify events**, when `analytics_write` exists: event name, fires-when,
   properties, owner. Without that capability, this section is the
   specification an owner implements later — mark it `READY_TO_IMPLEMENT`
   and say so.

## Closing

State the north star, its baseline (captured or scheduled), and whether the
measurement plan is `READY_TO_IMPLEMENT` or fully wired up (`LIVE`). Then
move to launch preflight in `flows/launch.md` — a plan that can't measure its
own result shouldn't go live yet, and that's one of the gate conditions
there, not just a suggestion here.
