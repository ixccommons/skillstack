# Measurement Plan — [company or product name]

## Funnel

Business model: `[from positioning_input.fields.business_model]`. Funnel
stages adapted per `references/business-models.md`:

`[stage] → [stage] → [stage] → [stage] → [stage]`

## North star

**Outcome:** [the one measurable outcome this pipeline run is built to move]

## Metrics

| Metric | Role (leading / guardrail / diagnostic) | Owner | Source | Formula | Baseline | Cadence | Target type | Decision threshold |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

Baseline is captured or explicitly scheduled before launch — see
`flows/launch.md` preflight. Business-owned observed data is used before
external benchmarks; a benchmark only appears here when its model, market,
price point, channel and date are stated and applicable — see
`references/evidence-policy.md`.

## Tracking

UTM convention: `utm_source / utm_medium / utm_campaign / utm_content /
utm_term`, generated with `scripts/generate_utm.py` so links stay
deterministic and existing parameters aren't duplicated.

| Link destination | Source | Medium | Campaign | Content | Term | Generated URL |
|---|---|---|---|---|---|---|
| | | | | | | |

## Events

Only for capabilities that actually exist (`analytics_write`); otherwise this
is the specification an owner implements later, marked READY_TO_IMPLEMENT.

| Event name | Fires when | Properties | Owner | State |
|---|---|---|---|---|
| | | | | |
