# Research Flow

Runs after positioning is accepted (`references/positioning-input.md`) and
before copy. Produces `research.md` and the matching `research[]` entries in
`pipeline-state.json`. Every rule about what counts as evidence lives in
`references/evidence-policy.md` — read it before starting; this file is the
sequence, that one is the standard.

## What to research

Work through these, using `web_research` where available:

- **Direct competitors** — named alternatives from the positioning input's
  `current_alternatives` field, checked and refreshed, not assumed current.
- **Indirect alternatives and manual workarounds** — the spreadsheet, the
  intern, doing nothing. Positioning step 3 in `marketing-workshop` already
  surfaced these; verify they're still accurate rather than re-deriving them.
- **Customer language** — how the segment actually describes the problem,
  from reviews, forum threads, community discussion. Keep this separate from
  what competitors say about themselves.
- **Current public pricing** — observed directly from competitor pricing
  pages, dated.
- **Category messages already in use** — what everyone claims, to confirm
  the gap from positioning still holds.
- **Search intent and current result types** — for the keyword work
  `flows/copy.md` will do next.
- **Communities, directories, newsletters, publications, events** — enough
  to seed `flows/distribution.md`'s long list; the full ranking happens
  there.
- **Applicable benchmarks** — only ones that pass the applicability test in
  `references/evidence-policy.md`.

## Sequencing

Research doesn't need one-question-at-a-time pacing the way positioning
does — there's no person being walked through their own thinking here, it's
gathering. But it does need one consequential judgment call surfaced at a
time: if the research turns up something that contradicts the accepted
positioning (a competitor claiming the same gap, a segment that looks smaller
than assumed), stop and flag it rather than quietly building around it. That
follows `references/positioning-input.md`'s "if positioning looks wrong"
guidance.

## Recording

For every consequential item: write the row to `research.md` in the matching
table, and append the structured entry to `pipeline-state.json.research[]`
with claim, value, provenance, source (if `SOURCED`), retrieved_at,
geography, applicability, confidence. Do both — the markdown table is what a
person reads, the array is what `validate_pipeline.py` and later flows key
off.

## Closing

Summarize in five lines or fewer: the sharpest competitive finding, the
clearest gap confirmation or contradiction, and the one thing marked
`UNKNOWN` that would most change the plan if it were known. Then move to
`flows/copy.md`.
