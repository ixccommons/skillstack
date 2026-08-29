# Execution Policy

This pipeline executes real actions when the capabilities exist to execute
them, and produces exact, import-ready specifications when they don't. This
file governs which is which, and the approval rules around the ones that
touch the outside world.

## Out of scope

This pipeline never does lead scraping, unsolicited outreach, or sales
closing. If a step could drift into building a contact list or drafting cold
outreach, stop and say plainly that it's out of scope — same as
`marketing-workshop/flows/distribution.md` scopes out lead generation.
Distribution here means channels and content, not people to contact
individually.

## Capability detection

Before doing anything, determine what's actually available in this session.
Use these generic names — never require a named vendor, and never assume a
capability exists because a similar one does:

| Capability | What it means |
|---|---|
| `web_research` | Can browse or search current public information |
| `file_write` | Can create durable files the person keeps |
| `spreadsheet_write` | Can create/edit spreadsheets |
| `crm_read` / `crm_write` | Can read from / write to a CRM |
| `cms_read` / `cms_write` | Can read from / write to a CMS or website |
| `publishing_write` | Can publish content (blog, listing, social, email send) |
| `analytics_read` / `analytics_write` | Can read analytics data / create tracking or event specs |
| `scheduled_tasks` | Can create tasks that run on a recurring schedule |

Record the result in `pipeline-state.json.capabilities`. Re-check rather than
assume it's unchanged if a session resumes much later.

**When a capability is absent:** produce the exact artifact a human would
need to do it by hand — the full page copy ready to paste, the CSV ready to
import, the task prompt ready to schedule. Mark the relevant component
`READY_TO_IMPLEMENT`. State the one missing capability plainly. Never imply
or claim that execution happened when it didn't.

## Action classification

Every action this pipeline might take falls into exactly one class:

1. **READ_ONLY** — reading a page, searching, reading current state back.
   May run within the scope of the user's request, no extra approval needed.
2. **REVERSIBLE_DRAFT** — creating a file, a draft page, a draft campaign
   that isn't live yet. May be created within scope; still needs approval
   before it moves to the next class.
3. **PUBLIC_OR_PERSON_DIRECTED** — anything a customer, prospect, or the
   public would see: publishing a page, posting to a community, sending an
   email, going live on a channel.
4. **FINANCIAL** — anything that spends money: ad budget, a paid listing,
   a paid tool.
5. **DESTRUCTIVE** — anything that removes or overwrites existing live
   content or data with no easy way back.

## Approval rules

- Classes 1–2 may proceed within the scope of what was asked.
- Classes 3 and 4 require an **exact preview and explicit approval
  immediately before execution** — not a general go-ahead given earlier in
  the session. Show: exact destination, exact content, audience, timing,
  budget if any, expected result, and the rollback or stop condition. Then
  wait for a yes.
- Class 5 requires explicit confirmation **and** a stated recovery plan
  before proceeding.
- **Don't group unrelated approvals.** Approving the homepage copy is not
  approval to also post to three communities. Each consequential action gets
  its own preview and its own yes — this mirrors the "one consequential
  decision per turn" rule the whole pipeline follows.
- **Apply maximum budget ceilings.** Never spend past a ceiling the person
  set, and ask for one before proposing anything in class 4 if none exists.
- **Do not send, publish, or launch if the target cannot be verified.** If
  the destination can't be confirmed reachable and correct, that's a blocker,
  not a reason to proceed anyway.

## After an action executes

- **Read the object back.** Don't trust the write call's return value alone
  — fetch or view what was actually created.
- **Record it** in `action_log`: action, classification, destination,
  identifier, timestamp, result.
- **Mark LIVE only after verification** succeeds. Before that it stays
  `READY_TO_IMPLEMENT` or `DRAFT`, even if the write call reported success.
- **On failure,** store the error in `action_log` and set the component to
  `BLOCKED` (if it needs a decision to unblock) or back to
  `READY_TO_IMPLEMENT` (if it just needs a retry later).
- **Never retry indefinitely.** One retry for a transient-looking failure,
  then stop and report it as blocked. A loop of silent retries is worse than
  a clear stop.

## Scheduled tasks

When `scheduled_tasks` is available, the three reusable tasks in
`flows/distribution.md` and `references/artifact-contracts.md` are created
after approval, then verified to exist before being marked `LIVE`. When it
isn't, write the full specifications (prompt, cadence, data sources,
destination, owner, success condition, failure behavior) and mark them
`READY_TO_IMPLEMENT` — never implying they're running.

## Never call READY_TO_IMPLEMENT "live"

This is the single most important state distinction in the whole pipeline.
`READY_TO_IMPLEMENT` means: everything needed exists and is correct, and a
human or a tool with the right capability can make it live with no further
judgment calls. It is not live. Don't round it up in conversation, in
`pipeline-state.json`, or in any generated summary. `scripts/validate_pipeline.py`
checks for this being misrepresented programmatically — see its
`validate_live_claims` — but the rule applies to everything said out loud
too, not just what's written to the state file.
