# Review Flow

Runs on the cadence set in `measurement-plan.md`, starting the week after
launch (or the week after the plan's Week 1, if the gate in `flows/launch.md`
isn't met yet but the plan is running anyway under `READY_TO_IMPLEMENT`
distribution). This is how the pipeline optimizes itself against observed
performance rather than running the original 30-day plan unchanged forever.

## Separate the failure types before recommending anything

A metric missing its threshold has more than one possible cause, and the fix
is different for each. Work through these in order and don't skip to a
recommendation before naming which one applies:

- **Insufficient data** — too little volume or too little time elapsed to
  read the number yet. The honest answer is often "we don't know yet," not a
  strategy change.
- **Execution failure** — the plan wasn't actually run. A `campaign-plan.csv`
  row marked done that wasn't, or a scheduled task that didn't fire. Check
  `action_log` before assuming the channel or message was the problem.
- **Channel failure** — the plan ran as specified, and this channel doesn't
  reach the segment the way `channel-map.md` assumed.
- **Message failure** — the channel is reaching the right audience, but the
  adapted message from `channel-map.md` isn't landing (low engagement despite
  reach).
- **Offer failure** — the message is landing but the conversion asset's
  offer or CTA isn't converting once someone arrives.
- **Measurement failure** — the plan may be working, but the tracking is
  wrong (a UTM mismatch, an event not firing), so the numbers can't be
  trusted either way. Check this one whenever a result looks implausibly
  good or bad before trusting it.

## Recommend exactly one

After naming the failure type (or confirming there isn't one — the metric
is on track), recommend exactly one of:

- **CONTINUE** — on track, no change.
- **STOP** — channel or message failure with no credible repair; redirect
  the effort to the next-ranked candidate in `channel-map.md`'s long list.
- **REPAIR** — execution or measurement failure with a specific, named fix.
- **RUN_CONTROLLED_EXPERIMENT** — offer or message failure where the cause
  isn't yet clear enough to just fix; add a row to `experiment-backlog.csv`
  with the hypothesis, the variable being tested, the audience, the success
  metric, and a guardrail metric that must not get worse.

## Record

For the period: evidence (cite the specific `weekly-scorecard.csv` row and
`action_log` entries), uncertainty (what would change the recommendation if
it turned out wrong), owner, next action, next review date. Append the
period's row to `weekly-scorecard.csv`.

**Do not replace the entire strategy because one week was noisy.** A single
off week is usually insufficient data, not a verdict — apply the failure-type
separation above before treating a bad week as proof of anything. Two or
three consecutive periods pointing the same direction is a different
conversation than one.

## Resuming after an interruption

If this pipeline picks back up after a gap — a new session, a different
person continuing the work — read `pipeline-state.json` and
`brand-brief.md` first, state which stage and which components are
already `LIVE` or `APPROVED`, and resume from there rather than re-asking
questions already answered. Re-verify anything claiming `LIVE` (per
`references/execution-policy.md`) before trusting it, since external state
can drift between sessions even when the pipeline's own file didn't change.
