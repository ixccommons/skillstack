# Running this on ChatGPT

The skill in `../SKILL.md` only loads on Claude. Most workshop attendees won't
have it, so the same flows run three other ways. The flow files are shared source
in all cases — `flows/positioning.md` and friends are read by Claude directly and
concatenated into the paste files here, so a change to a step lands on both
platforms from one edit.

| | Setup cost | Works on a free account | Best for |
|---|---|---|---|
| **A. Paste-in prompt** | none | yes | the room |
| **B. Project** | 2 minutes, per person | needs Projects | someone continuing after the workshop |
| **C. Custom GPT** | 10 minutes, instructor only | see below | handing out one link |

## A. Paste-in prompt — the one to use in a room

`paste/positioning.md`, `paste/copy.md`, `paste/distribution.md` are each
self-contained: the operating instructions plus one flow. The person opens a new
chat, pastes the whole file as their first message, and answers the question it
asks back.

No account tier, no setup, no feature that might be missing on the day. If
ChatGPT converts the paste into an attachment because of its length, that's fine
— it reads it either way.

Host the three files somewhere copyable before the session (a gist, a page, a
pinned message). Asking a room to clone a repo costs more minutes than the flow
you're trying to run.

## B. Project

One Project per person, instructions once, then a chat per flow.

1. New Project → **Instructions** → paste `instructions.md`.
2. Attach `../flows/positioning.md`, `copy.md` and `distribution.md` as files.
3. Start a chat per flow: *"Run the positioning flow."*

Project instructions apply to every chat inside the Project, and the brief and
drafts stay in one place across all three flows. This is the closest match to how
the skill behaves on Claude, and the right shape for someone carrying on the work
after the room empties.

## C. Custom GPT

Instructions field, then the flows as knowledge files. Same as B, but the
instructor builds it once and hands out a link.

The Instructions box caps at **8,000 characters**. `instructions.md` is about
6,200, which leaves room to edit — `build.py` fails the build if it goes over.

Check before you rely on this one: building a GPT needs a paid plan, and whether
your attendees can open a shared GPT link on whatever tier they're on is worth
testing with an actual free account a day early, not at the start of the session.

## What is genuinely different on ChatGPT

**The brief is a canvas document, not a file.** `instructions.md` says to open a
canvas titled `Brand Brief — [company]` and update it after every step, falling
back to printing a copyable block every second step where canvas isn't there. It
also says to tell people to copy the brief out at the end of each flow, because a
lost tab is a lost session and the next flow may be a new chat. On Claude the
filesystem does this quietly; here it has to be an instruction.

**Pacing needs more force.** The one-step-per-turn rule is the whole design, and
GPT models push harder than Claude towards answering everything at once. So
`instructions.md` carries mechanical guards the Claude `SKILL.md` doesn't need —
end the message with the question and nothing after it, never preview the next
step, cut any step output running past ~200 words. If you're calibrating pacing,
calibrate it here; this is where it slips.

**Distribution step 6 degrades.** Scheduled tasks are a paid-tier feature (three
active tasks on the entry plan, more further up) and aren't in the desktop app.
On a free account the step can't create anything, so the flow writes the three
task prompts out in full instead and says that's what happened. Worth knowing
before you promise the room automation at minute 95.

**No progressive disclosure.** Claude reads one flow file per session. Routes A
and B put a whole flow in context at once, and the Custom GPT retrieves from
knowledge files, which is fuzzier still. Practical effect: keep one flow per
chat. A single chat running all three drifts, and the copy instructions start
leaking into positioning questions.

## Maintaining both

```sh
python3 marketing-workshop/portable/build.py          # regenerate paste/
python3 marketing-workshop/portable/build.py --check  # verify, change nothing
```

Edit `../flows/*.md` or `instructions.md`, never `paste/` — it's generated, and
the banner at the top of each file says so. `--check` also fails if a flow file
starts naming file paths again, since that's what breaks it on a platform with no
filesystem.

The paste files work in any chat assistant, not just ChatGPT — there's nothing
OpenAI-specific in them beyond the canvas wording.
