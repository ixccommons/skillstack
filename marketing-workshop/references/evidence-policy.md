# Evidence Policy

Research that can't be trusted is worse than no research — it gets built into
copy and channel decisions that then have to be walked back in front of a
customer or a room. Every consequential research item follows this policy.
"Consequential" means: anything that ends up as a claim on a live asset, a
reason to prioritize one channel over another, or an input to a measurement
target.

## Provenance types

Every item records exactly one:

| Type | Meaning |
|---|---|
| `PROVIDED` | Given directly by the business (a number from their own system, a fact they stated) |
| `OBSERVED` | Directly observed by this pipeline right now — a page read, a search result seen, a listing checked |
| `SOURCED` | From a specific external source with a URL and a retrieval date |
| `INFERENCE` | Reasoned from other evidence in this file, not observed directly — state the reasoning |
| `ASSUMPTION` | Working assumption with no evidence yet — must be flagged as such everywhere it's used downstream |
| `UNKNOWN` | Actively looked for and not found — recorded so nobody re-derives the same dead end |

An item with no provenance type is not a valid research entry. `UNKNOWN` and
`ASSUMPTION` are legitimate answers — better than silently omitting the row.

## What every item needs

Per the schema (`schemas/pipeline-state.schema.json`, `research[]`): claim,
value, provenance, retrieved_at, confidence, and — when the type is `SOURCED`
— a direct source URL. Also record geography and applicability where they
affect whether the number transfers to this business.

## Hard rules

- **Never invent** search volume, traffic, reach, CTR, CAC, CPL, conversion
  rate, or market size. If it isn't observed or sourced, it's `UNKNOWN` or
  `ASSUMPTION`, stated as such, not a plausible-sounding number.
- **Distinguish a competitor's claims about itself from verified customer
  perception.** "Competitor X says they serve 10,000 teams" is `SOURCED` to
  the competitor's own page — it is not evidence about how customers actually
  feel, and must never be presented as if it were.
- **Do not infer market share from search prominence.** Ranking first for a
  term says something about SEO, not about revenue or customer count.
- **Business-owned observed data outranks external benchmarks.** If the
  business has their own conversion rate, use it before reaching for an
  industry number.
- **A benchmark is only usable when the model, market, price point, channel,
  and date are all stated and applicable.** A 2019 enterprise SaaS benchmark
  does not apply to a 2026 local-business budget decision. If any of those
  five don't match, the benchmark doesn't go in — note it as `UNKNOWN`
  instead, or find one that actually applies.
- **Geography and freshness travel with the claim.** A pricing figure or
  channel size from a different country, or from more than roughly a
  business cycle ago, gets flagged in `applicability`, not presented as
  current.

## Confidence

`low` / `medium` / `high`, judged on: how direct the observation was, how
recent, and how well it matches this business's specifics. A single
`SOURCED` data point from a relevant, recent, on-geography source can be
`high`. An `INFERENCE` chained from two other inferences is `low` almost by
definition — say so.

## Where this shows up downstream

- `flows/copy.md` step on evidence: every claim on a live asset traces back
  to a research item here, or is marked `[EVIDENCE NEEDED]` rather than
  stated as fact.
- `flows/research.md`: the collection step this policy governs directly.
- `flows/launch.md` preflight: "claims match evidence" is checked against
  this file before anything is marked LIVE.
