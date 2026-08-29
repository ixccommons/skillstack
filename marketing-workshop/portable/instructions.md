# Platform adapter — running this skill on ChatGPT

The complete skill follows below: `SKILL.md`, then any reference files this
flow cites, then the flow itself. **All of it is authoritative and none of it
is summarised.** This section says only how the platform differs from the one
`SKILL.md` was written for — a Claude session with a filesystem and tools.

Where the two conflict, this section wins. Everywhere else, follow `SKILL.md`
exactly as written.

## Assume a free ChatGPT account

`SKILL.md`'s Stage 1 asks you to detect what this session can do. Here the
answer is already known, so don't re-derive it:

- `web_research` — **yes.** Use it wherever a step calls for current facts.
- `file_write`, `spreadsheet_write`, `crm_read`, `crm_write`, `cms_read`,
  `cms_write`, `analytics_read`, `analytics_write`, `publishing_write`,
  `scheduled_tasks` — **no.**

Say that once, plainly, when a flow first depends on it. If the person tells
you they have something more, believe them and use it.

The consequence, which `SKILL.md` already covers and you must not soften:
nothing can reach `LIVE` from inside this chat, because you can't publish
anything or read it back. Components stop at `READY_TO_IMPLEMENT`, the
completion gate stays unmet, and the deliverable is an exact specification a
person can execute by hand. That is a real result. It is not a live pipeline,
and it is never described as one.

## There is no filesystem — the brief lives in the chat

`SKILL.md` and the flows write to `brand-brief.md`, `copy/homepage.md`,
`channel-map.md` and similar. Those are names, not paths, here:

- **The brief.** Keep it yourself. Print **just the header table** as one
  copyable block after every second step, the **whole brief** at the end of
  the flow and whenever asked. Use the header exactly as `SKILL.md` defines
  it — every field, same order — leaving blank whatever isn't filled yet.
- **Drafts** (page copy, ad sets, the research table, the campaign plan).
  Print each once, as its own copyable block, under the name the flow gives
  it. Don't reprint one you've already given unless asked; on a small context
  window, repetition is what pushes the early steps out of the conversation.
- **`pipeline-state.json`** is optional even on Claude. Skip it unless the
  person asks, and if they do, print it as one JSON block at the end of a
  stage rather than maintaining it turn by turn.
- **Tell them to paste the brief somewhere they own** at the end of every
  flow. A closed tab is a lost session.

## What isn't loaded here

- **`scripts/`** (`init_pipeline.py`, `validate_pipeline.py`,
  `generate_utm.py`) can't run. Where a flow calls for one, do the equivalent
  by hand following the convention in the reference file included below, and
  say the generator wasn't used so the person can re-run it properly later.
- **`templates/`, `schemas/`** aren't attached. Produce the artifact from the
  flow's own description of it.
- **`references/`** — only the files this flow cites are included below. Where
  `SKILL.md` points at one that isn't here, work from `SKILL.md`'s own summary
  of the rule and say the detail file isn't loaded. **Never invent the
  contents of a file you weren't given.**

## One flow per chat

Each paste file carries one flow. Don't run a second one in the same chat —
the context is too small and the flows blur into each other.

`SKILL.md`'s whole-pipeline mode still works, as a sequence of chats: finish a
flow, take the printed brief, open the next flow's paste in a new chat, and
paste the brief in before answering the first question. If someone opens with
a pasted brief, read it, say which flows it already covers and which
components are `APPROVED` or `READY_TO_IMPLEMENT`, and continue from there
rather than re-asking. That's also how a session that degraded or hit a limit
gets resumed — a new chat plus the brief loses nothing but the transcript.

## Pacing, mechanically

`SKILL.md`'s pacing rules apply in full. These are guards on top of them,
because this platform pushes harder than Claude towards answering everything
at once:

- End your message with the step's question and **nothing after it**. No
  preview of the next step, no "once you've answered, we'll…", no numbered
  plan of what's coming.
- Never answer a step on the person's behalf, even when the answer seems
  obvious from what they've said. The exception is drafting *options* when a
  step explicitly asks for them.
- If a step's output is running past ~200 words, you're writing instead of
  asking. Cut it.
- If they answer two steps at once, take both — and still stop at the next.

---

The skill itself follows. If nothing follows, it's in your uploaded files:
read `SKILL.md` first, then only the flow being run.
