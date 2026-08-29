# Artifact Contracts

What each file in a working directory is for, who writes it, who reads it,
and when it changes state. Use this as the map when a flow says "write to
the brief" or "update the state file" without spelling out the mechanics.

## Files

| File | Written by | Read by | Contains |
|---|---|---|---|
| `brand-brief.md` | every flow, human-readable mirror of key decisions | the person, any flow resuming | positioning, plus one section per later stage — see `SKILL.md`'s extended header |
| `pipeline-state.json` (optional) | `scripts/init_pipeline.py`, then every automation-stage flow after each consequential step | `scripts/validate_pipeline.py`, any flow resuming an automation stage | the structured, machine-checkable mirror of the same decisions — only needed once research/measurement/launch/review are in play |
| `copy/<asset>.md`, `tasks/<name>.md` | `flows/copy.md`, `flows/distribution.md` | the person, `flows/launch.md` | full-length drafts, kept out of the brief so it stays short |
| `research.md` | `flows/research.md` | `flows/copy.md`, `flows/distribution.md` | the evidence table — see `references/evidence-policy.md` |
| `messaging-guide.md` | `flows/copy.md`, once an asset moves toward automation | `flows/distribution.md` (message adaptation), `flows/launch.md` (claims-match-evidence check) | the conversion asset's angle, audit, and implementation checklist — points at the actual draft in `copy/` rather than duplicating it |
| `channel-map.md` | `flows/distribution.md` | `flows/launch.md`, `flows/review.md` | long list, ranking, adapted messages per channel |
| `campaign-plan.csv` | `flows/distribution.md` | `flows/launch.md`, `flows/review.md` | the 30-day sequence, one row per action |
| `measurement-plan.md` | `flows/measurement.md` | `flows/launch.md`, `flows/review.md` | funnel, north star, metrics, tracking |
| `weekly-scorecard.csv` | `flows/review.md`, one row appended per period per metric | the person, next review | actuals against target and threshold |
| `experiment-backlog.csv` | `flows/review.md` when recommending `RUN_CONTROLLED_EXPERIMENT` | next review | hypotheses, one row per experiment |
| `launch-checklist.md` | `flows/launch.md` | the person before go-live | preflight checklist and current blockers |

Every file above is human-readable on its own — none of them require
`pipeline-state.json` to be meaningful to a person, and `brand-brief.md`
alone is enough to run positioning, copy, and distribution the way this
skill always has. The optional `pipeline-state.json` exists so
`validate_pipeline.py` can check consistency mechanically once someone wants
the deeper, automation-capable stages; treat it as generated-from-decisions,
not the primary place decisions get made.

**Do not hand-edit files this skill generates as if they were source.**
`pipeline-state.json` is written by the flows and read by the scripts; if you
need to fix a mistake in it, fix it the way the flow that owns that section
would — update the relevant `.md` or `.csv` first, then reflect the change
into the state file, the same direction data always flows.

## Scheduled task specifications

Three reusable tasks. Each needs the fields below whether it's actually
created (capability present) or just specified (`READY_TO_IMPLEMENT`).

### 1. Channel and competitor monitor

- **Purpose:** surface threads, posts and mentions worth responding to,
  before they go stale.
- **Prompt:** "Search [chosen channels from `channel-map.md`] and the
  competitor names in `research.md` for mentions of [the problem, in the
  segment's own words], [the category], and [the business name]. List each
  hit with a link, one line on why it's relevant, and whether it looks worth
  a response. Do not draft a response — that's a judgment call for the
  owner."
- **Cadence:** daily or weekly, matched to channel activity level.
- **Data sources:** the channels named in `channel-map.md`, `web_research`.
- **Destination:** wherever the owner actually checks daily — the pipeline
  doesn't assume a specific tool.
- **Owner:** named in `pipeline-state.json.scheduled_tasks`.
- **Success condition:** the list is produced and delivered on schedule,
  even when it's empty — an empty result is still a completed run.
- **Failure behavior:** if a channel becomes unreachable or search fails,
  report which source failed rather than silently omitting it; don't retry
  more than once per run.

### 2. Weekly pipeline report

- **Purpose:** one message the owner can read on a phone: what went out,
  what came back, what's due this week.
- **Prompt:** "Summarize this week from `campaign-plan.csv` (rows due this
  week and their status) and `weekly-scorecard.csv` (this period's row per
  metric). State what shipped, what's behind, and the single most important
  number versus its threshold. Under 150 words."
- **Cadence:** weekly, on the day the 30-day plan's repeating slot falls.
- **Data sources:** `campaign-plan.csv`, `weekly-scorecard.csv`.
- **Destination:** wherever the owner receives it (chat, email, doc —
  capability-dependent, not vendor-specific).
- **Owner:** named in `pipeline-state.json.scheduled_tasks`.
- **Success condition:** delivered on schedule, references real current
  data (not a stale cache).
- **Failure behavior:** if either source file is unreadable, report that
  directly rather than sending a partial report that looks complete.

### 3. Content brief generator

- **Purpose:** turn a keyword or question from `messaging-guide.md`'s
  keyword/topic work into a ready-to-write outline, so the week 3
  substantial item in `campaign-plan.csv` starts from a brief, not a blank
  page.
- **Prompt:** "Given [a keyword or question], produce: the angle, the
  section outline, the evidence needed for each section (flagging anything
  not yet in `research.md` as `[EVIDENCE NEEDED]`), and the internal links
  to existing pages. Follow the voice rules in the accepted positioning
  input."
- **Cadence:** on demand, or weekly ahead of the next substantial content
  item due.
- **Data sources:** `messaging-guide.md`, `research.md`, positioning input.
- **Destination:** a new file the writer opens directly.
- **Owner:** named in `pipeline-state.json.scheduled_tasks`.
- **Success condition:** the brief is complete enough that the writer's
  next action is writing, not researching.
- **Failure behavior:** if the keyword has no supporting research yet, say
  so and stop rather than fabricating evidence to fill the outline.

If `scheduled_tasks` capability is absent, write all three specifications in
full into `pipeline-state.json.scheduled_tasks` and the brief, mark them
`READY_TO_IMPLEMENT`, and say plainly they need setting up by hand or with a
scheduling tool.
