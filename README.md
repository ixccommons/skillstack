# skillstack

Agent skills, one directory each.

## marketing-workshop

Runs a founder through three marketing flows, one step at a time: positioning,
copy, distribution. Built for a live workshop — the pacing rules exist so that
attendees do the thinking rather than watch generated text scroll past.

```
marketing-workshop/
  SKILL.md              router, shared rules, brief format
  flows/positioning.md  8 steps · ~40 min · + a 10-minute express pass
  flows/copy.md         8 steps · ~35 min
  flows/distribution.md 6 steps · ~25 min
```

The three flows share one state file, `brand-brief.md`, written into the working
directory of whoever is running it. Positioning writes it, copy and distribution
read it and append. Longer output — page copy, ad sets, scheduled-task prompts —
goes to `copy/` and `tasks/` alongside it.

### Install

Copy the directory into wherever the agent looks for skills:

```sh
cp -r marketing-workshop ~/.claude/skills/        # available everywhere
cp -r marketing-workshop .claude/skills/          # this project only
```
