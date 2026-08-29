# Running this skill on ChatGPT

ChatGPT's own Skills feature would carry the whole skill, `dist/` zip and all —
but it's a Business / Enterprise / Healthcare / Edu feature, not in the Free,
Plus or Pro rollout. This directory is the backup that works anyway, and it
carries **the same skill, not a reduced one**.

## What "the same" means here

Each file in `paste/` is built by `build.py` from the real source, verbatim:

```
instructions.md      the platform adapter — free-tier deltas only
../SKILL.md          the whole router, unabridged (frontmatter stripped)
../references/*.md   the ones this flow cites, in full
../flows/<flow>.md   the flow itself
```

Nothing is summarised, re-derived, or trimmed to fit. There is one paste file
per flow — all seven, `positioning` through `review` — so a flow that exists on
Claude exists here. The brief header, the seven pipeline states, the six-part
completion gate and the quality rules are the same text on both platforms
because they *are* the same text.

That's the point: a hand-maintained second copy drifts, and this one had
already drifted five fields on the brief header before it was replaced by this
build.

`instructions.md` is the only file written for this platform. It says what's
different — no filesystem, no publishing, no scripts — and defers to `SKILL.md`
for everything else.

## The three routes

| | Setup | Free account | Best for |
|---|---|---|---|
| **A. Paste-in prompt** | none | yes | the room |
| **B. Project** | 2 min, per person | yes, within a small upload allowance | continuing afterwards |
| **C. Custom GPT** | instructor builds once, needs a paid plan | attendees can use one | handing out a link |

**A. Paste-in.** Open a new chat, paste the whole of `paste/<flow>.md` as the
first message, answer the question it asks back. Nothing to install, no tier.
Host the files somewhere copyable before the session — asking a room to clone a
repo costs more minutes than the flow you're running.

**B. Project.** `instructions.md` in the Instructions box; `../SKILL.md`, the
flow, and any references it cites attached as files. Projects are on the free
plan, but the daily upload allowance is small — attach one flow at a time
rather than all seven up front.

**C. Custom GPT.** Same shape as B, built once and shared as a link. The
Instructions box caps at 8,000 characters; `instructions.md` is 4,762, and
`build.py` fails the build if an edit pushes it over.

## Context is the real constraint

The paste files run 30–40 KB — roughly 7,500 to 10,000 tokens — before anyone
says a word, against a free-tier window materially smaller than the paid ones.
`build.py` prints the per-file budget on every run so it can't creep up
unnoticed.

Three rules follow, all of them in `instructions.md`: **one flow per chat**,
never reprint a draft already given, and keep the header table current so a
fresh chat can resume from a pasted brief. If a session degrades or hits a
limit mid-flow, a new chat plus the brief loses nothing but the transcript.

`SKILL.md`'s whole-pipeline mode therefore runs as a *sequence of chats* rather
than one long one — finish a flow, take the brief, open the next flow's paste,
paste the brief in first.

## What a free account still can't do

Not omissions from the skill — capabilities the platform doesn't have. The
adapter pre-answers `SKILL.md`'s Stage 1 with them, so the flows behave exactly
like a Claude session that happens to have no tools:

- **`web_research` is available.** Everything else is not: no file writing, no
  CMS or analytics or CRM access, no publishing, no scheduled tasks.
- **Nothing reaches `LIVE` from inside the chat**, because nothing can be
  published and read back. Components stop at `READY_TO_IMPLEMENT` and the
  completion gate stays unmet. The adapter is explicit that this is a real
  result and is never described as a live pipeline.
- **`scripts/` can't run**, so `generate_utm.py`'s job is done by hand against
  the convention in `references/metrics.md`, which is inlined into the
  measurement paste for exactly that reason.
- **`templates/` and `schemas/` aren't attached**, and `pipeline-state.json` is
  skipped unless asked for — it's optional on Claude too.
- **`references/artifact-contracts.md` is never inlined**: it maps deliverables
  onto filenames, and there are no files here.

Tier boundaries move. These were checked in August 2026 — test the route you're
depending on with an actual free account a day before, not at the start of the
session.

## Maintaining it

```sh
python3 marketing-workshop/portable/build.py          # regenerate paste/
python3 marketing-workshop/portable/build.py --check  # verify, change nothing
```

Edit `../SKILL.md`, `../flows/*.md`, `../references/*.md` or
`instructions.md` — never `paste/`, which is generated and says so at the top
of every file. `--check` runs in CI and fails on a stale build, a flow citing a
reference that doesn't exist, or a leftover paste file whose flow was renamed
or removed. Adding a flow to `flows/` is enough to get a paste file for it; the
build discovers them.

The paste files work in any chat assistant, not just ChatGPT.
