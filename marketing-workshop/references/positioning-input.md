# Positioning Input Contract

Everything from research onward consumes positioning. It does not produce it,
revise it, or run a second version of `flows/positioning.md`. Positioning is
actively maintained by someone else on this project — treat it as a
dependency with a stable contract, not a step later flows can improve on.

**Never edit `flows/positioning.md`, or the positioning section of a
generated `brand-brief.md` / portable paste file.** That file is someone
else's active work even though it lives in this same skill. If positioning
looks wrong, that's a finding to hand back to whoever owns it, not something
to silently fix here — see "If positioning looks wrong" below.

## Accepted sources

**A. `brand-brief.md`**, written by this skill's own `flows/positioning.md`
earlier in the same session, or in an earlier session in the same working
directory. Read it; don't parse it defensively — it's markdown with a header
table and free-text sections, not a machine format. Pull the fifteen fields
below from the header and the positioning section.

**B. Pasted content.** When there's no filesystem, no `brand-brief.md`
exists yet, or the person is bringing in positioning done somewhere else
entirely, ask them to paste their positioning output (or answer the fifteen
fields directly). Same contract, no file.

## Required fields

| # | Field | Typically found at |
|---|---|---|
| 1 | Company or product name | Brief header / product baseline |
| 2 | Offer | Product baseline (positioning step 1) |
| 3 | Business model | Not always explicit in the brief — see below |
| 4 | Primary customer segment | Brief header, positioning step 2 |
| 5 | Problem or desired progress | Positioning step 2 |
| 6 | Buying trigger | Not always explicit — ask if missing |
| 7 | Current alternatives | Positioning step 3 |
| 8 | Category or frame of reference | Brief header, positioning step 3 |
| 9 | Approved value proposition | Brief header, positioning step 5 |
| 10 | Reasons to believe | Positioning step 6 (the ranked points + evidence) |
| 11 | Primary objections | Positioning step 7 |
| 12 | Messaging hierarchy | Positioning step 6 |
| 13 | Voice rules | Positioning step 8 |
| 14 | Geography | Not always explicit — ask if missing |
| 15 | Constraints | Not always explicit — ask if missing (budget, timeline, regulatory, brand) |

Fields 3, 6, 14 and 15 are the ones a `brand-brief.md` written for a workshop
often doesn't state outright, because the workshop didn't need them. Expect to
ask for these even when everything else is present.

## When fields are missing

1. Read whatever positioning input exists first. Identify only the fields
   that are actually missing — don't ask about fields you can already fill
   in from the brief.
2. Ask for the missing ones **one at a time**, in the order above. This
   mirrors the pacing rule this skill follows everywhere for consequential
   decisions — see `references/execution-policy.md`.
3. Never invent a value for a missing field. A blank `null` in
   `positioning_input.fields` is the correct state until the person answers;
   guessing at a segment or a value proposition produces exactly the
   fluent-and-empty copy positioning exists to prevent.
4. Never send the person back through the full positioning flow to answer
   one or two fields. That flow is ten times the length of what's needed
   here. Ask directly, plainly, and move on.
5. Once every field has a value, set `positioning_input.status` to
   `ACCEPTED`, record `accepted_at`, and record which `source` supplied it.
   Before that, `status` is `MISSING` (nothing usable yet) or `PARTIAL` (some
   fields present, gaps identified).

## If positioning looks wrong

Sometimes the positioning input is complete but looks weak — a value
proposition a competitor could say verbatim, a segment that's really a
demographic. That's a real finding, and it matters, but it's not later
flows' job to re-litigate it: positioning is owned by whoever ran that step,
and unilaterally rewriting it here creates two sources of truth for the same
brief.

State the concern plainly, once, and ask whether to proceed with it as-is or
pause for the person to revisit positioning. Then follow their answer. If
they proceed, note the concern in `brand-brief.md`'s research or copy section
so it isn't lost.

## Business model mapping

`positioning_input.fields.business_model` is free text as given. Map it to
one of the nine `business_model` enum values in `pipeline-state.json` for
everything downstream to key off — see `references/business-models.md`. If
the mapping is ambiguous, ask rather than guess; funnel stages, channels and
measurement all branch on this one value.
