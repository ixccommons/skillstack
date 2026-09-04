---
title: Building the base
covers: The problem, the premise behind it, the alternatives, and the one you're committing to
triggers: help me think through an idea; is this worth building; what should I build; pressure-test my idea; I have an idea
minutes: 40
pacing: one step per turn
order: 10
adds-header: Problem, Who it's for, Chosen approach
---

# Building the base

Six steps, roughly 40 minutes. Output is a problem stated in one sentence, the
assumptions it rests on written down and agreed, two or three real alternatives
with one chosen, and a handoff concrete enough to act on tomorrow.

The goal is **a better decision, not an implementation.** Nothing gets built in
this module. If the session drifts into writing code or copy, that's the failure
mode — say so and come back.

Run one step per turn. See the pacing section in `SKILL.md`.

Open by telling them the shape: you'll spend the first half on the problem and
almost none of it on solutions, and that's deliberate — most of what makes a
build wrong is decided before anyone opens an editor.

---

## Step 1 — The problem

**Ask:** What are you trying to accomplish, and who is it for?

Then, one at a time, and only as far as their answers leave gaps:

- What problem does it solve, and why does that problem matter to them?
- What have they already tried — theirs or someone else's?
- What constraints exist? Time, money, skills, a platform they're stuck on.

Don't propose anything yet. The instinct to say "you could build X" arrives
about ninety seconds in, and acting on it ends the useful part of the module.

**Push back on:** a solution described as a problem. Most founders arrive with
the answer already chosen and describe the problem backwards from it.

*They say:* "The problem is there's no AI tool for managing freelance invoices."
*Weak:* "What would the AI tool do?" — a reasonable question that accepts the
solution as the premise and never reaches the problem.
*Better:* "That's a missing product, not a problem. What does a freelancer do
today at the end of the month, and which part of it costs them something?"

**Write to brief:** Problem (header), Who it's for (header) — rough is fine, the
positioning work sharpens it later — plus the constraints in the module's
section.

---

## Step 2 — Challenge the premise

Before anything is proposed, take the assumptions apart. Work these in order,
one at a time:

1. Is this actually the right problem, or a symptom of a different one?
2. Who *specifically* has it? A named person or role, not a category.
3. What happens if nothing gets built? If the honest answer is "not much", say
   so out loud.
4. Is the problem observed or hypothetical? What did they see, and when?
5. What already addresses it — products, workarounds, doing nothing?
6. What existing work can be reused — their own code, a library, a service,
   a spreadsheet?
7. Is there a simpler way to the same outcome?

**Then state the premises back as a numbered list and stop.**

```
PREMISES
1. [statement] — agree / disagree?
2. [statement] — agree / disagree?
3. [statement] — agree / disagree?
```

Wait for a real answer on each. If they disagree with one, update the
understanding and re-state it before moving on. This is the gate the rest of the
module rests on — a premise nobody ratified is an assumption that resurfaces as
a rebuild in six weeks.

**Push back on:** evidence that is really enthusiasm.

*They say:* "Everyone I've spoken to says they'd use it."
*Weak:* "Who have you spoken to?" — gets you a list of names and no test.
*Better:* "Saying they'd use it is free. Has anyone asked when it ships, offered
to pay, or been annoyed when something broke? Those are the three that count."

**Write to brief:** the agreed premises, numbered, with any that were rejected
and what replaced them.

---

## Step 3 — The landscape

**Ask:** nothing first — go and look, then bring it back.

Search the problem space rather than working from memory: what exists, what the
common approaches are, what open-source or off-the-shelf option gets partway
there, and — the useful part — why existing approaches succeed or fail. Naming a
product that shut down last year in front of a room costs credibility, so check.

Bring back five or six things, and for each say what a person genuinely gets
from it. Not why it's worse. What it's actually good at.

Then the question this step exists for: **is the proposed direction
differentiated, or is something that already exists sufficient?** Be willing to
answer "sufficient". A founder who leaves having decided not to build something
has had a good session, and it's cheaper here than in month four.

**Write to brief:** the alternatives that already exist, what each does well,
and the one-line verdict on whether this is differentiated.

---

## Step 4 — Alternatives

**Produce at least two, ideally three.** Not optional, and not three variations
of the same idea.

- **A — Minimal.** The smallest thing that could work. Fewest moving parts,
  ships soonest.
- **B — Ideal.** The best long-term shape, if the constraints from step 1
  weren't binding.
- **C — Alternative.** A meaningfully different framing, where one exists. The
  "sufficient existing option" from step 3 is often the honest C.

For each: what it does, effort, risks, advantages, disadvantages, and what
existing work it reuses.

**Then recommend one, in a line, tied to what they said they wanted — and
stop.** Present the options and wait. A clearly winning option is still their
decision, and a recommendation accepted by silence gets abandoned the first
week it becomes inconvenient.

**Push back on:** picking B because it's the most interesting. The gap between
what's fun to build and what's worth building is where most first products die.

**Write to brief:** Chosen approach (header), the alternatives considered in
one line each, and the reason for the choice — which is what makes it possible
to revisit later without re-running the whole module.

---

## Step 5 — The design

Skip this step entirely if there's no interface — say so and move on rather than
inventing one.

If there is, think through:

- The core user flow, start to finish, in the fewest steps
- Information hierarchy: what the first screen has to make obvious
- The states that aren't the happy path — loading, empty, error, success
- Edge cases that would embarrass it
- **What can be removed.** Usually more than feels comfortable.
- Where trust comes from — what a first-time user needs to see to believe it

Rough sketches or wireframes where they'd communicate faster than prose.
Iterate on their feedback rather than presenting a finished thing.

**Write to brief:** the core flow, and anything cut.

---

## Step 6 — The handoff

Produce one concise plan. Not a document nobody reads — a page:

- Problem
- Goals
- Key assumptions (the agreed premises from step 2)
- Recommended approach, and the alternatives considered
- Core user flow
- Technical approach
- Important edge cases
- Open questions
- **Next step** — one, concrete, doable this week, with a name against it

Everything above it is context for that last line. If the next step is "start
building", it's too vague to be a next step.

**Write to brief:** the plan as its own draft, with the brief carrying the
recommended approach, the open questions, and the next step with its owner and
date.

---

## Closing the module

Read back the problem in one sentence and the chosen approach. Nothing else —
the plan holds the rest.

Then the checkpoint: tell them to post their problem sentence and their next
step where the room can see it. The pair is the interesting thing — a sharp
problem with a vague next step is the most common shape in the room, and seeing
it next to someone else's is what makes it obvious.

**Then what's next.** This module decides *what* to build and roughly who for.
Sharpening who, and what to say to them, is the positioning work in the
`marketing-workshop` skill — run its positioning flow next, and it will read
Problem and Who it's for straight out of this brief. The landing page comes
after that, from the same skill's copy flow. Say that out loud so the arc is
visible: idea → pressure-test → position → page.

---

## If they already built it

Some people arrive with the thing already made, looking for a landing page
rather than a decision. The module still runs and it's usually the most useful
forty minutes of their day, but three steps change tense:

- **Step 1** asks what it does and who's using it now, not what they intend.
- **Step 2** is the same seven questions asked of a product that exists —
  "what happens if nothing gets built" becomes "what happens if you stop working
  on this", which is a harder and better question.
- **Step 4** compares carrying on, narrowing to a smaller product, and stopping.
  Those are real alternatives at any stage, and a founder who has never priced
  the third one hasn't chosen the first.

Don't let them skip to the landing page. A page built on an unexamined premise
is a faster way to find out the premise was wrong, but it's not a cheaper one.
