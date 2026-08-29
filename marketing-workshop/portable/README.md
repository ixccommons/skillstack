# Running this on ChatGPT

The skill in `../SKILL.md` only loads on Claude. Most attendees won't have it, so
the same flows run three other ways here.

**These assume a free ChatGPT account** — that's what a room actually has, and
designing for Plus produces a session where a third of the people can't follow
along. Everything below degrades on purpose rather than by accident.

The flow files are shared source in all three routes: `../flows/positioning.md`
and friends are read by Claude directly and concatenated into `paste/` by
`build.py`, so calibrating a step updates both platforms from one edit.

| | Setup | Free account | Best for |
|---|---|---|---|
| **A. Paste-in prompt** | none | yes | the room |
| **B. Project** | 2 min, per person | yes, within a small upload allowance | continuing afterwards |
| **C. Custom GPT** | instructor builds once, needs a paid plan | attendees can use one | handing out a link |

## A. Paste-in prompt — the one to use in a room

`paste/positioning.md`, `paste/copy.md` and `paste/distribution.md` are each
self-contained: the operating instructions plus one flow. Open a new chat, paste
the whole file as the first message, answer the question it asks back.

No tier, no setup, no feature that might be missing on the day. If ChatGPT turns
the paste into an attachment because of its length, it reads it either way.

Host the three files somewhere copyable before the session — a gist, a page, a
pinned message. Asking a room to clone a repo costs more minutes than the flow
you're trying to run.

## B. Project

Projects are on the free plan. One per person, instructions once, a chat per
flow, and the brief stays reachable across all three.

1. New Project → **Instructions** → paste `instructions.md`.
2. Attach the flow files from `../flows/`.
3. Start a chat per flow: *"Run the positioning flow."*

Free accounts have a small daily upload allowance, so attach only the flow being
run that day rather than all three up front — or use route A and spend nothing.

## C. Custom GPT

Instructions field, flows as knowledge files. The instructor builds it once and
hands out one link; free accounts can use a shared GPT even though they can't
build one.

The Instructions box caps at **8,000 characters**. `instructions.md` is about
7,050, and `build.py` fails the build if an edit pushes it over.

## What is genuinely different on free ChatGPT

**No canvas — the brief lives in the chat.** Canvas is Plus and above, so there's
nothing persistent to write to. `instructions.md` has the assistant keep the
brief itself, print the header table as a copyable block every second step, print
it in full at the end of the flow, and tell the person to paste it somewhere they
own. Handing off between flows is that paste: someone who opens the copy flow
with their positioning brief pasted in gets picked up where they left off. On
Claude the filesystem does this quietly; here it's an instruction and a habit you
should mention out loud at the start.

**No scheduled tasks — distribution's last step writes them out.** Task
scheduling is a paid feature. The step produces the three task prompts in full,
with the schedule each should run on, and says plainly they need setting up by
hand or on a paid plan. Don't promise the room working automation at minute 95.

**A small context window, and a model that can get lighter mid-session.** The
default free model runs a materially smaller window than the paid ones, and long
sessions can drop to a lighter model partway through. The paste files are 15–20KB
— call it 4–5k tokens — before anyone says a word, so a 40-minute flow is a real
share of the budget. Three consequences, all already in `instructions.md`: one
flow per chat, never reprint a draft already given, and keep the header table
current so a fresh chat can resume from a paste. If someone's session degrades,
starting a new chat with their brief pasted in is the fix, not a lost morning.

**No progressive disclosure.** Claude reads one flow file per session. Routes A
and B put a whole flow in context at once; a Custom GPT retrieves from knowledge
files, which is fuzzier still. Practical rule: one flow per chat. A single chat
running all three drifts, and copy instructions start leaking into positioning
questions — the thing the three-file split exists to prevent.

**Search works**, so the steps that need current facts — competitor sets, who
ranks for a phrase, which communities exist — behave the same as on Claude.

Tier boundaries move often. The ones above were checked in August 2026; test the
route you're depending on with an actual free account a day before, not at the
start of the session.

## Maintaining both

```sh
python3 marketing-workshop/portable/build.py          # regenerate paste/
python3 marketing-workshop/portable/build.py --check  # verify, change nothing
```

Edit `../flows/*.md` or `instructions.md`, never `paste/` — it's generated, and
each file says so at the top. `--check` also fails if a flow file starts naming
file paths again, since that's what breaks it on a platform with no filesystem.

The paste files work in any chat assistant, not just ChatGPT.
