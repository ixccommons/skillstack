# skillstack

Agent skills, one directory each.

## marketing-workshop

Takes a product from an undefined position to a running, measured marketing
pipeline — one skill, one running brief. Positioning, copy, and distribution
are built for a live workshop, one step at a time, so attendees do the
thinking rather than watch generated text scroll past. Research, measurement,
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
  portable/                positioning + copy + distribution, for people without Claude
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

Two ways in, depending on what's available on the account:

- **Native skill upload** (`chatgpt.com/skills` → drag in a `.zip`): the whole
  skill, prebuilt at
  [`marketing-workshop/dist/marketing-workshop.zip`](marketing-workshop/dist/marketing-workshop.zip).
  It's a generated file — never edit it by hand. After changing anything
  under `marketing-workshop/` (other than `dist/`), rebuild and commit it:

  ```sh
  python3 marketing-workshop/scripts/build_skill_zip.py          # rebuild
  python3 marketing-workshop/scripts/build_skill_zip.py --check  # verify, change nothing
  ```

- **Paste-in / Project / Custom GPT, no upload feature needed:**
  `marketing-workshop/portable/` runs positioning, copy, and distribution —
  the live-room three — as a paste-in prompt, a Project, or a Custom GPT,
  assuming a free account. See
  [`marketing-workshop/portable/README.md`](marketing-workshop/portable/README.md).

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
