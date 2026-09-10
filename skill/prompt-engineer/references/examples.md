# Worked examples

Match this length and tone. Each example shows the draft, the scorecard summary, the
context that was collected, the recommended rewrite, and the patterns note.

---

## 1. Claude Code, coding task

**Draft:** "fix the login bug"

**Context collected:** Next.js repo, `npm test` and `npm run lint` in package.json,
CLAUDE.md says "never edit files under `generated/`", last three commits touch
`lib/auth/session.ts`, an open issue titled "Session cookie not cleared on logout".

**Scorecard:** 22/100. Goal 8/20 (a bug is named, which one is not), context 4/20
(the repo is implied), constraints 3/15 (CLAUDE.md rules are implied), format 4/15
(a fix is the obvious artifact), role and audience 2/10, verification 2/10, scope 4/10;
agentic verification penalty -5. Fixes with most leverage: goal and verification.

**Interview:** skipped two questions the repo answered (test command, forbidden dirs);
asked one: "Is the bug the logout cookie issue in the open issue, or something else?"
Answer: yes, that one.

**Rewrite B (recommended):**

```
Fix the logout bug from the open issue "Session cookie not cleared on logout". Start
in lib/auth/session.ts (the last three commits touched it). Reproduce it first with a
failing test in lib/auth/__tests__/, matching the style of session.test.ts. Then fix
the code, not the test. Do not edit anything under generated/ (CLAUDE.md). Run
`npm test` and `npm run lint` and paste the results. If the fix needs a change
outside lib/auth, stop and tell me what and why before making it.
```

**Patterns applied:** specific deliverable and location (P1), project substitution
(P13: real files, commands, CLAUDE.md rule), few-shot by pointing at an existing
test (P6), verification with a stop rule (P10), scope boundary (P11). Not applied:
role (no meaningful persona), chain-of-thought (Claude plans on its own here).

**To push it higher:** projected 88/100. Add the expected behaviour in one sentence
("after logout, GET /api/me returns 401") and it reaches the 90s.

---

## 2. claude.ai chat, writing task

**Draft:** "write a linkedin post about our 4 day work week"

**Context collected:** none (chat). Interview asked four questions: audience, the
facts that are true, tone, and length. Answers: founders and CEOs; productivity up,
revenue flat, satisfaction up, no surprises; candid, no hype; about 250 words.

**Scorecard (draft):** 31/100.

**Rewrite A (minimal):**

```
Write a 250-word LinkedIn post for founders and CEOs on what we learned switching a
10-person remote team to a 4-day week. Facts to use, and only these: productivity
went up, revenue stayed flat, satisfaction went up, nothing unexpected broke. Candid
tone, no hype, no emojis or hashtags. End with one question to readers.
```

**Rewrite C (interview form, for next time):**

```
I need a ~250-word LinkedIn post about lessons from moving to a 4-day work week.
Before writing, ask me up to five questions about audience, facts, tone, and what to
avoid, one batch. Then write it, and tell me which facts you used.
```

**Patterns applied:** specific deliverable (P1), context with a closed fact list (P3,
which also stops invented metrics), constraints with the failure they prevent (P4),
interview gate (P9). Not applied: role (the writer is the user; a "marketing expert"
persona pushes toward hype).

---

## 3. API system prompt

**Draft:** "You are a helpful assistant that turns feedback into tickets."

**Context collected:** the user's app ingests support feedback and posts to Linear;
titles must be under 60 characters; areas are a fixed list of six.

**Rewrite C (system slot, variables, one example):**

```
System:
You turn one line of user feedback into one support ticket title. Titles are read
in a Linear board by engineers triaging quickly, so they must name the area first
and the symptom second.

Format: "[Area] symptom", under 60 characters, one line, no trailing period. Area
is exactly one of: Login, Export, Billing, Editor, Mobile, Notifications. If the
feedback fits none, use "[Triage]".

<example>
Feedback: Google sign-in on Safari just spins forever
Title: [Login] Google sign-in hangs on Safari
</example>

Return only the title.

User:
Feedback: {{feedback}}
```

**Patterns applied:** identity in the system slot with the why (P3), exact format and
closed label set (P5), one example (P6), escape hatch for the unlisted case (P12),
variable for the per-request part (P13 for templates). Not applied: chain-of-thought,
role beyond the task itself.

---

## 4. Subagent prompt

**Draft (what the user typed to the parent):** "have a subagent check the docs"

**Rewrite C:**

```
You are checking the documentation in docs/ of a Python CLI for commands that no
longer exist. Facts: the current commands are listed by `python -m tool --help`;
docs are Markdown under docs/; you have no other context and cannot ask questions.
Read-only: do not edit any file. Return a Markdown table with columns file, line,
documented command, status (missing or renamed, with the new name if you can find
it in src/). Stop after docs/; do not scan README.md.
```

**Patterns applied:** self-contained context (P3), read-only boundary and stop
condition (P4, P11), return shape for the parent (P5). This shape is what our own
experiment runners used.

---

## 5. Data analysis in chat

**Draft:** "analyze this csv"

**Rewrite B:**

```
This CSV is 28 days of daily YouTube views for one channel (columns: date, views).
I am deciding whether to post twice a week or three times. Give me: (1) the weekly
mean and the day-of-week pattern in one short table, (2) whether the last week is
different from the first three in a way that matters (say how you judged that), (3)
one recommendation with the main risk. Under 200 words plus the table. Do not
invent data I did not give you; if the CSV is missing a column you need, say so.
```

**Patterns applied:** goal with the decision it feeds (P1, P3), numbered deliverables
(P5), constraints with the failure prevented (P4), explicit unknown handling (P12).
