# skillstack

Agent skills, one directory each.

## cofounder-workshop

The standalone twin of `cofounder`. Same modules and the same brief, but
positioning runs as a ten-minute express pass carried inside the skill instead
of handing off — so it needs nothing else installed, and the whole arc fits a
short room. Use `cofounder` when there's time to position properly and both
skills are available; use this one otherwise.

The express pass is generated from `marketing-workshop`'s positioning flow by
`cofounder-workshop/scripts/build_express.py` and committed, so an installed
copy is self-contained while the text can't drift from the original. A parity
test pins every file the two twins share and lists the four that legitimately
differ.

## cofounder

The business decisions a founder would normally take to a cofounder — what to
build next, pricing, hiring, runway, and the weekly operating rhythm. Parallel
to `marketing-workshop`: same live-room shape, same one-step-per-turn pacing,
its own `company-brief.md`, and the same portable route for people without
Claude. Marketing questions hand off rather than being answered twice.

Modules are added under `cofounder/flows/` — one file each, with frontmatter
that drives the router, the trigger phrases, the brief's header table, the room
timetable and the ChatGPT paste file. Adding a module updates all five:

```sh
cp cofounder/flows/_TEMPLATE.md cofounder/flows/pricing.md   # write it
make -C cofounder                                            # rebuild
make -C cofounder check                                      # what CI runs
```

See [`cofounder/AUTHORING.md`](cofounder/AUTHORING.md) for the frontmatter
contract and what a module owes the rest of the skill.

## marketing-workshop

Takes a product from an undefined position to a running, measured marketing
pipeline — one skill, one running brief. Positioning, copy, and distribution
are built for a live workshop, one step at a time, so attendees do the
thinking rather than watch generated text scroll past. Positioning follows
Al Ries and Jack Trout's *Positioning: The Battle for Your Mind* — the
category ladder, the word the leader owns, the hole nobody stands in, and a
message short enough to survive in a crowded head. Research, measurement,
launch, and review pick up from there — deep competitor and customer
research, UTM tracking and measurement, automated execution where the host
agent's tools allow it, launch verification, and weekly review. No lead
scraping, no unsolicited outreach, no sales closing.

Run it flow by flow ("run the positioning flow", "set up my tracking",
"review this week"), or ask for the whole thing ("build my marketing
pipeline") and it runs positioning through launch as one session — asking
what it genuinely needs, researching rather than guessing, and handing back
an honest state (`READY_TO_IMPLEMENT` or `LIVE`, never one claimed as the
other) at the end.

```
marketing-workshop/
  SKILL.md               router, pacing, capability detection, state model,
                          completion gate — the whole process in one file
  flows/
    positioning.md       8 steps · ~40 min · + a 10-minute express pass
                          method: Ries & Trout, Positioning
    copy.md               8 steps · ~35 min · + a 9th if the session can publish
    distribution.md       6 steps · ~25 min
    research.md           deep competitor / customer / channel-seed research
    measurement.md        funnel, north star, UTM tracking, baselines
    launch.md              preflight and the live/not-live gate
    review.md               weekly scorecard, stop/continue/repair/experiment
  references/            positioning contract, business-model differences,
                          evidence policy, execution policy, metrics, artifact map
  schemas/                pipeline-state.schema.json — the optional state contract
  templates/               starting files for the deeper, automation-capable stages
  scripts/                 init_pipeline.py, validate_pipeline.py, generate_utm.py
  tests/                   unittest coverage for all three scripts
  portable/                all seven flows again, built from the same source,
                          for anyone who can't install a skill
```

Every flow shares one state file, `brand-brief.md`, written into the working
directory of whoever is running it — positioning writes it, every later flow
reads and appends. Longer output — page copy, ad sets, the research table,
the campaign plan — goes to `copy/`, `tasks/`, and a handful of named files
alongside it. Once research or later stages are in play, an optional
structured layer (`pipeline-state.json`, scaffolded by
`scripts/init_pipeline.py`) tracks the same decisions in a machine-checkable
form — every deliverable carries exactly one state (`MISSING`, `DRAFT`,
`APPROVED`, `READY_TO_IMPLEMENT`, `LIVE`, `MEASURING`, or `BLOCKED`), and
`READY_TO_IMPLEMENT` is never reported as `LIVE`.

Positioning is actively maintained separately from the rest of this skill —
every later flow reads it and treats it as a fixed contract; none of them
revise it.

### Install

Copy the directory into wherever the agent looks for skills:

```sh
cp -r marketing-workshop ~/.claude/skills/        # available everywhere
cp -r marketing-workshop .claude/skills/          # this project only
```

Works the same way in Claude Code and Claude Desktop — once installed,
invoke it as `/marketing-workshop`, or just describe what you want.

### On ChatGPT

Two ways in. Which one you get is decided by the account's plan, not by
preference:

- **Paste-in / Project / Custom GPT — works on a free account.**
  `marketing-workshop/portable/` carries all seven flows with no upload
  feature needed. Each paste file is built from the real source — `SKILL.md`
  verbatim, the references that flow cites, then the flow — so it's the same
  skill rather than a reduced copy of it. This is the workshop route: a room
  is mostly free accounts, and it's the only one all of them can open. See
  [`marketing-workshop/portable/README.md`](marketing-workshop/portable/README.md).

- **Native Skills upload — Business, Enterprise, Healthcare and Edu only.**
  Skills aren't in the Free, Plus or Pro rollout, and on managed workspaces an
  admin may have to enable them first (sidebar → Plugins → Skills). Where it
  is available it takes the whole skill, all seven flows, prebuilt at
  [`marketing-workshop/dist/marketing-workshop.zip`](marketing-workshop/dist/marketing-workshop.zip).
  It's a generated file — never edit it by hand. After changing anything
  under `marketing-workshop/` (other than `dist/`), rebuild and commit it:

  ```sh
  python3 marketing-workshop/scripts/build_skill_zip.py          # rebuild
  python3 marketing-workshop/scripts/build_skill_zip.py --check  # verify, change nothing
  ```

  Plan boundaries move — check
  [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)
  before building a session around this route.

Either way, research, measurement, launch, and review depend on real tool
access (browsing, files, a connected account) that a given ChatGPT session
may or may not actually have — the skill detects and states that rather than
assuming it. See "Installing and running this skill" at the bottom of
`marketing-workshop/SKILL.md`.

### Quick start for the deeper stages

```sh
python3 marketing-workshop/scripts/init_pipeline.py .
python3 marketing-workshop/scripts/validate_pipeline.py .
```

Run against the same directory `brand-brief.md` already lives in — it's
additive and safe to run more than once.
