# Metrics

Reference for `flows/measurement.md`. Defines the funnel per business model,
the metric roles, and the UTM convention. See `references/business-models.md`
for the full per-model breakdown this file's funnels summarize, and
`references/evidence-policy.md` for what's allowed to count as a number.

## Funnels by business model

| Business model | Funnel |
|---|---|
| B2B SaaS | awareness → qualified conversation → demo/consultation → opportunity → customer |
| B2B service or agency | awareness → qualified conversation → proposal → engagement → repeat engagement |
| Ecommerce / D2C | discovery → product view → cart → purchase → repeat purchase |
| Consumer application | discovery → install → activation → retention → paid conversion |
| Local business | discovery → call/booking/directions → visit → review → repeat visit |
| Creator or personal brand | discovery → subscription/registration → return → purchase/support |
| Event or community | discovery → registration → attendance/participation → return |
| Marketplace | qualified supply + qualified demand → match → transaction → repeat liquidity |
| Nonprofit | awareness → engagement → contribution → repeat contribution/advocacy |

## Metric roles

Every metric in `measurement-plan.md` and `pipeline-state.json.measurements`
gets exactly one role:

- **North star** — the one outcome this pipeline run is built to move.
  Exactly one per pipeline. Chosen to match `objective`.
- **Leading indicators** — move before the north star does and predict it.
  Useful for a 30-day plan, where the north star itself may not have moved
  yet by day 30.
- **Guardrail metrics** — must not get worse while the north star improves.
  A CAC guardrail on a growth push; a support-ticket-volume guardrail on an
  activation push.
- **Diagnostic metrics** — explain *why* the north star or a leading
  indicator moved. Not targets themselves.

For each metric, record: owner, source, formula, cadence, baseline, target
type (absolute / relative / directional), and the decision threshold — the
number that triggers a stop/continue/repair/experiment call in
`flows/review.md`. A metric with no decision threshold is not yet usable for
a weekly review; it's still a diagnostic.

## Baseline

Every north-star and guardrail metric needs a baseline before launch — either
captured now from `analytics_read` / business-provided numbers (`PROVIDED` or
`OBSERVED` per the evidence policy), or explicitly scheduled with an owner
and date if the data doesn't exist yet. `flows/launch.md` preflight checks
this; a plan can go live without a captured baseline only if a capture date
is on the calendar.

## UTM convention

Five parameters, always in this order: `utm_source`, `utm_medium`,
`utm_campaign`, `utm_content`, `utm_term`. Generate every tracking link with
`scripts/generate_utm.py` rather than by hand — it preserves any existing
non-UTM query parameters, replaces rather than duplicates an existing UTM
value, encodes values safely, and produces the same output for the same
input every time, which matters when `campaign-plan.csv` gets diffed week to
week.

Suggested values, adapt per channel:

- `utm_source` — the specific site or list (`reddit`, `the-name-newsletter`),
  not the channel type
- `utm_medium` — the channel type (`community`, `newsletter`, `paid-social`,
  `directory`)
- `utm_campaign` — the 30-day plan's name or the specific push
  (`launch-2026-08`)
- `utm_content` — which asset or variant, when running more than one
- `utm_term` — the specific angle or keyword being tested, when relevant

## Weekly scorecard and experiment backlog

`weekly-scorecard.csv` and `experiment-backlog.csv` headers are fixed — see
`schemas/pipeline-state.schema.json` context and
`scripts/validate_pipeline.py` for the exact columns checked. Populate one
scorecard row per metric per period, and one backlog row per hypothesis
tested via `flows/review.md`'s `RUN_CONTROLLED_EXPERIMENT` recommendation.
