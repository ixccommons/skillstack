---
name: marketing-workshop
description: Runs a founder or marketer through a real product's marketing, end to end — positioning (segment, competitors, value proposition, brand voice), copy (homepage, landing pages, ads, email, SEO), distribution (channel discovery, ranking, 30-day plan), and everything after that: deep research, measurement and tracking, automated execution where tools exist, scheduled monitoring, launch verification, and weekly review. Use this skill whenever someone wants to work on their positioning, write or rewrite marketing copy, find where their customers are, set up tracking, launch a campaign, review this week's numbers, or asks to "run the positioning flow", "do the copy flow", "go through the channel map", "build my marketing pipeline", "run the whole thing", or names any part of the Coffee with Claude workshop. Also use it for value proposition, homepage copy, ad headlines, competitor analysis, brand voice, channel strategy, UTM tracking, or launch readiness, even if the request doesn't name a flow or a workshop.
---

# Marketing Workshop

One process that takes a real product from an undefined position to a
running, measured marketing pipeline: positioning, copy, distribution,
research, measurement, launch, and review. Everything downstream of
positioning stays consistent with it, because everything reads the same
brief.

The first three flows are designed to be run live, by a person working on
their own business, usually in a room with other people doing the same
thing. The later ones do real research and, where the session has the tools
for it, real execution — they still ask before anything consequential, but
they don't wait for a person to think out loud the way positioning does. See
Pacing below for the difference, and Stage 1 for what "the tools for it"
means concretely.

## Two ways to run this

**Flow by flow.** Ask for one part by name — "run the positioning flow",
"rewrite my homepage", "set up my tracking", "review this week" — and only
that flow runs, the same as always.

**The whole pipeline.** Ask to "build my marketing pipeline," "run the whole
thing," or similar, and this skill runs positioning through launch as one
session: it asks the questions each stage genuinely needs (starting with
whatever's missing from positioning), does real research rather than
guessing, drafts and adapts copy, ranks and sequences channels, sets up
measurement, executes what the session's tools allow, and ends by handing
back an honest state — a working `READY_TO_IMPLEMENT` or `LIVE` pipeline,
never a claim past what actually happened. It still stops at every
consequential decision (an angle, a channel ranking, a launch go/no-go) and
waits for a real answer — "the whole pipeline" means one continuous session
and one running brief, not fewer decisions in the person's hands.

Either way, `brand-brief.md` is the same file, so switching between the two
mid-project costs nothing — a person who ran positioning alone last week can
come back and ask for the whole pipeline from here, or vice versa.

## The flows

| Flow | Covers | File | Pacing |
|---|---|---|---|
| Positioning | Segment, competitors, gap, value proposition, messaging, objections, voice | `flows/positioning.md` | one step per turn |
| Copy | Homepage, landing pages, ads, email, one-pagers, SEO, AI-answer visibility | `flows/copy.md` | one step per turn |
| Distribution | Channel discovery, ranking, message fit, 30-day plan, scheduled tasks | `flows/distribution.md` | one step per turn |
| Research | Deep competitor, pricing, customer-language, and channel-seed research | `flows/research.md` | one decision per turn |
| Measurement | Funnel, north star, metrics, UTM tracking, baselines | `flows/measurement.md` | one decision per turn |
| Launch | Preflight verification, the live/not-live gate | `flows/launch.md` | one decision per turn |
| Review | Weekly scorecard, stop/continue/repair/experiment | `flows/review.md` | one decision per turn |

Read only the flow file actually being run — loading all seven at once blurs
every one of them, the same reason positioning, copy, and distribution have
always been read one at a time.

## Routing

Most people won't name a flow. Map what they ask for:

- "who is this for" / "my competitors all sound the same" / "I can't
  describe what we do" → **positioning**
- "rewrite my homepage" / "I need ad headlines" / "my landing page doesn't
  convert" → **copy**
- "channel map" / "where do I find customers" / "what should I post where" →
  **distribution**
- "dig into my competitors" / "what's my customers' actual language" / "is
  this a real gap" → **research**
- "set up tracking" / "what's my north star" / "how do I measure this" →
  **measurement**
- "is this ready to launch" / "can I go live" / "what's blocking launch" →
  **launch**
- "how did this week go" / "should I keep doing this" / "review the
  campaign" → **review**
- "build my marketing pipeline" / "run the whole thing" / "take this from
  positioning to launch" → **the whole pipeline**, per the section above

If it's ambiguous ("help me with my marketing"), don't guess — name the
options in one line each and ask which. If someone mid-flow asks something
from another flow, answer briefly and offer to switch rather than silently
changing track.

## Order and dependencies

Positioning → research → copy → distribution → measurement → launch →
review, then review repeats on a cadence. Research is the one optional
depth step: copy and distribution can run without it (they each do their own
lighter research inline), but skip it only when the person already has
strong competitive and customer-language evidence — guessing instead of
researching is exactly the failure this skill exists to prevent.

Before copy or distribution, check `brand-brief.md`. If there's no
positioning section, say so and offer the express pass at the end of
`flows/positioning.md` rather than writing against nothing. Before
measurement or launch, check that copy and distribution have at least a
draft — measuring nothing, or launching nothing, isn't a real gate.

## Positioning stays someone else's work

Positioning is actively being worked on elsewhere in this project.
**Never edit `flows/positioning.md`, or the positioning section of a
generated `brand-brief.md` / portable paste file** — not to fix a weak value
proposition, not to add a field that looks missing, not for any reason.
Every later flow *reads* positioning and treats it as a fixed contract; none
of them revise it. If positioning looks wrong once you're deep into
research or copy, say so once, plainly, and ask whether to proceed with it
as-is or pause for the person to revisit it — then follow their answer. Full
contract for what "accepted positioning" means and what to do when a field
is missing: `references/positioning-input.md`.

## Stage 1 — Capability detection

Before research, measurement, launch, or the whole-pipeline mode do
anything, work out what this session can actually do. Don't assume, and
never require a named vendor:

`web_research`, `file_write`, `spreadsheet_write`, `crm_read`, `crm_write`,
`cms_read`, `cms_write`, `analytics_read`, `analytics_write`,
`publishing_write`, `scheduled_tasks`.

**When a capability is absent:** produce the exact artifact a human needs to
do it by hand, mark the component `READY_TO_IMPLEMENT`, state the one
missing capability, and never claim execution happened when it didn't. Full
detail, including action classification and approval rules for anything
public, person-directed, financial, or destructive: `references/execution-policy.md`.

Positioning, copy, and distribution's live-workshop core doesn't need this —
they run the same way regardless of tools available, the way they always
have. Capability detection matters once research starts doing live lookups
and once distribution, measurement, or launch might actually publish
something.

## Pipeline states

Once a stage produces something with a real state — a conversion asset, a
channel, a scheduled task, the measurement plan — it carries exactly one of:

| State | Means |
|---|---|
| `MISSING` | not started |
| `DRAFT` | in progress, not yet approved |
| `APPROVED` | approved, not yet implementable |
| `READY_TO_IMPLEMENT` | complete and correct; a human or a capable tool could make it live with no further judgment calls |
| `LIVE` | actually live, read back and verified |
| `MEASURING` | live and past its baseline period, generating measurable results |
| `BLOCKED` | can't proceed without a decision or a missing capability |

**`READY_TO_IMPLEMENT` is never called "live."** In conversation, in
`brand-brief.md`, or in the optional `pipeline-state.json`. This is the
single rule everything in Stage 1 through the launch gate exists to protect.

## The brief is the state

Everything lands in one document, `brand-brief.md`, written into the working
directory. It's the state (a closed tab isn't a lost session), the handoff
between every flow above, and the thing the person takes home.

Create it on the first write with this header, and keep it updated as later
steps change it:

```markdown
# Brand Brief — [company name]

| Field | Value |
|---|---|
| Product | |
| Category | |
| Primary segment | |
| Value proposition | |
| Business model | |
| Objective | |
| Channels chosen | |
| North-star metric | |
| Capabilities noted | |
| Flows completed | |
| Current stage | |
| Last updated | |

```

`Business model`, `Objective`, `North-star metric`, and `Capabilities noted`
are filled in once research, distribution, or measurement runs — leave them
blank until then rather than guessing. `Current stage` tracks where the
pipeline is in the order above (`positioning`, `research`, `copy`,
`distribution`, `measurement`, `launch`, `review`), so resuming after a gap
starts from a read, not a re-ask.

Keep the header short and factual. Everything below it is free text, one
section per flow, appended in order. Never rewrite an earlier flow's
section; if positioning changes during a later flow, note the revision in
that flow's section and update the header.

Long output doesn't go in the brief — the homepage draft, the ad set, the
task prompts, the research table, the campaign plan. Those are **drafts**,
each a file of its own: `copy/homepage.md`, `copy/ads.md`,
`tasks/weekly-report.md`, `research.md`, `channel-map.md`,
`campaign-plan.csv`, `measurement-plan.md`. The brief records the decision
and a pointer. Full map of what each file is and who reads it:
`references/artifact-contracts.md`.

**Optional structured layer.** Once research or later flows are in play,
`scripts/init_pipeline.py <dir>` scaffolds the companion files above plus
`pipeline-state.json`, the machine-checkable mirror of the same decisions
against `schemas/pipeline-state.schema.json`. It's additive — it never
creates or touches `brand-brief.md`, and it's safe to run more than once.
Use `scripts/validate_pipeline.py <dir>` to check consistency, and
`scripts/generate_utm.py` for every tracking link measurement produces.
None of this is required for positioning, copy, or distribution on their
own; it exists for people going further.

The flows never name a path themselves beyond what's shown above, so the
same flow text can run on a platform with no filesystem — see `portable/`
for the ChatGPT version, which covers positioning, copy, and distribution.

## Pacing

**Positioning, copy, and distribution: one step per turn. Ask, stop, wait
for a real answer.** The failure mode is running several steps in one
response and handing back thousands of words the person didn't write and
won't defend. Concretely, for each step: ask the question (one short example
if abstract) → stop → when they answer, reflect it back sharpened, push back
if vague → write it to the brief → next step. Vague answers are the norm and
are the actual work — "small businesses" is not a segment, "high quality" is
not a differentiator.

**Research, measurement, launch, and review: one consequential decision per
turn**, not one micro-step. These flows do real work between decision
points — searching, drafting a ranked list, checking a gate — that a person
doesn't need to narrate their way through the way they do their own
segment or value proposition. What still gets a stop-and-wait: an angle
choice, a channel ranking, a launch go/no-go, a stop/continue/repair call.
Full detail on what counts as consequential and the approval rules around
anything that touches the outside world: `references/execution-policy.md`.

**In the whole-pipeline mode**, each flow keeps its own pacing rule as it
runs — the session doesn't get faster just because it's continuous. What
changes is that the assistant moves to the next flow on its own once a stage
closes, rather than waiting to be asked.

Let people skip. Someone who already knows their segment shouldn't be walked
through segmentation — take the answer, record it, move on, and offer the
skip explicitly when they answer fast and confidently. If someone's short on
time, name which steps are load-bearing for their goal and drop the rest.

## Completion gate

The pipeline overall may be marked `LIVE` only when all six hold:

1. Positioning is accepted.
2. At least one conversion asset is live and reachable, verified.
3. At least one distribution action is active or scheduled.
4. The desired conversion is measurable (north star named, measurement plan
   at least `READY_TO_IMPLEMENT`).
5. Owners, cadence, and decision rules exist.
6. External changes were verified, not assumed.

Otherwise it stays `READY_TO_IMPLEMENT`, and the response lists only the
specific blockers separating it from `LIVE` — not a restatement of
everything still to do. `scripts/validate_pipeline.py`'s
`evaluate_launch_gate` is the programmatic source of truth over eyeballing
it by hand. Full preflight: `flows/launch.md`.

## Resuming after an interruption

If a session picks back up after a gap, read `brand-brief.md` (and
`pipeline-state.json` if it exists) before doing anything else. State which
flows are already done and which components are `APPROVED` or `LIVE`, and
continue from there — don't re-ask questions already answered. Re-verify
anything claiming `LIVE` before trusting it; external state (a page, a
listing, a scheduled task) can drift between sessions even when the brief
didn't change.

## Checkpoints

At the end of positioning, copy, and distribution, tell the person to post
their headline result where the room can see it — the value proposition, the
new hero section, the top three channels. At the end of measurement,
launch, and review, the equivalent is stating the result plainly in the
brief: the north star and its baseline, the live/not-live verdict with its
blockers, the week's stop/continue/repair/experiment call. Keep it to one
line; don't turn it into a ceremony.

## Quality rules that apply everywhere

- Never invent search volume, traffic, CAC, CPL, conversion rates, or market
  size — see `references/evidence-policy.md`.
- Distinguish a competitor's claims about itself from verified customer
  perception.
- No hardcoded vendors — capabilities are generic, tools are whatever the
  session actually has.
- No fake execution — "I've set this up" only after read-back verification.
- No infinite retries, no destructive default behavior, no giant
  questionnaire — one consequential decision at a time.
- Keep every generated artifact human-readable without needing
  `pipeline-state.json` open.
- Timestamps are UTC ISO 8601 internally; identifiers are stable and
  deterministic where practical.
- No lead scraping, no unsolicited outreach, no sales closing — distribution
  means channels and content, not a contact list.

## Tone

The person is doing hard thinking about their own business, often in
public, often discovering their positioning is weak. Be direct about weak
answers and warm about the person. In the later, more autonomous flows,
that directness extends to capability gaps and launch blockers — state them
plainly, don't round `READY_TO_IMPLEMENT` up to `LIVE` to sound further
along than the pipeline actually is. Don't pad, don't cheerlead, and don't
produce more than the person can read in the time they have.

## Installing and running this skill

```sh
cp -r marketing-workshop ~/.claude/skills/        # available everywhere
cp -r marketing-workshop .claude/skills/          # this project only
```

**Claude Code / Claude Desktop:** reads `SKILL.md` first, then loads
`flows/`, `references/`, `templates/`, and `scripts/` progressively as each
stage needs them. Invoke it as `/marketing-workshop`, or just describe what
you want — see Routing above.

**ChatGPT / Custom GPT:** `portable/` runs positioning, copy, and
distribution — the live-room three — without a skills directory, assuming a
free account. See `portable/README.md`. Research, measurement, launch, and
review depend on real tool access (browsing, files, a connected CMS or
analytics account) that the free-room paste-in mode doesn't have; run those
in a ChatGPT Project or Custom GPT with `flows/`, `references/`, and
`templates/` attached as knowledge files, or in an agent that actually has
the tools.

**Codex, or another `SKILL.md`-compatible agent:** the folder is plain
markdown, JSON, and Python with no platform-specific syntax in the core
behavior. Point the agent at `marketing-workshop/SKILL.md` and it has
everything it needs to start; deeper stages progressively pull in the
matching `flows/` and `references/` file.

**No feature parity is claimed across platforms.** What actually goes live
depends entirely on the host agent's tools and connected accounts in that
session — this skill's job is to detect what's there (Stage 1), do
everything possible with it, and produce exact, import-ready specifications
for everything it can't do itself.
