# Launch Checklist — [company or product name]

Run through `flows/launch.md` preflight before marking anything LIVE overall.
Check items only when verified, not when merely planned.

- [ ] Positioning input accepted (`positioning_input.status == ACCEPTED`)
- [ ] Research provenance valid — no UNKNOWN or ASSUMPTION items feeding a
      claim that will appear on a live asset
- [ ] Conversion asset approved
- [ ] Conversion destination works (opened and checked, not assumed)
- [ ] Links work
- [ ] CTA and conversion event agree
- [ ] Claims match evidence — nothing on a live asset lacks the proof cited
      for it
- [ ] Owners assigned
- [ ] Dates assigned
- [ ] Tracking identifiers consistent across every generated link
- [ ] Required approvals recorded in `pipeline-state.json.approvals`
- [ ] Budget ceilings defined for anything with a spend
- [ ] Baseline captured, or explicitly scheduled with an owner and date
- [ ] Distribution path active or scheduled
- [ ] Monitoring configured

## Gate

The pipeline overall may be marked LIVE only if all of the following hold —
`scripts/validate_pipeline.py` checks these programmatically as the launch
gate:

1. Positioning input is accepted.
2. At least one conversion asset is live and reachable (read back and
   verified).
3. At least one distribution action is active or scheduled.
4. The desired conversion is measurable (measurement plan is at least
   READY_TO_IMPLEMENT, north star is named).
5. Owners, cadence and decision rules exist (at least one approval on
   record).
6. External changes were verified, not assumed.

Otherwise the pipeline stays READY_TO_IMPLEMENT, and this checklist should
list only the blockers separating it from LIVE — not a restatement of
everything still to do.

## Blockers separating this pipeline from LIVE

| Blocker | Missing capability, if any | Owner | Next step |
|---|---|---|---|
| | | | |
