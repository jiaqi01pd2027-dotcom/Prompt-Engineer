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


---

## 6. Claude Code, tests (the quick example)

**Draft:** "write tests for the parser"

**Scorecard:** 18/100. Task named, success undefined; no file, no check; the agentic
penalty applies. Context found: Python repo, `pytest -q`, tests live in `tests/`,
`parse_iso_duration` in `src/durations.py`, CLAUDE.md says "no mocks".

**Rewrite B (recommended):**

```
Add pytest tests for parse_iso_duration in src/durations.py. Put them in
tests/test_durations.py, matching the style of tests/test_dates.py. Cover: each
component alone, all components together, fractional seconds, weeks, and three
invalid strings that must raise ValueError. No mocks (CLAUDE.md). Check: run
`pytest -q` and paste the output; if pytest is not installed, say so and show the
tests instead of installing anything. Stop rule: if a new test fails, say whether
the test or the parser is wrong; do not change the parser.
```

**Patterns applied:** specific deliverable and location (P1), project substitution
(P13), few-shot by pointing at an existing test (P6), constraints with the reason
(P4), verification with a stop rule (P10). Not applied: role, chain-of-thought.

---

## 7. Writing, college application essay (chat)

**Draft:** "write my college essay"

**Context collected:** none (chat). Interview asked five questions: the exact prompt,
the reader, the true material, the limit and format, and a voice sample. Answers: the
Common App prompt "Describe a topic, idea, or concept you find so engaging that it
makes you lose all track of time"; admissions readers who skim hundreds; two true
stories (rebuilding a bike derailleur at 2 a.m., teaching a cousin to ride); 650 words;
a pasted paragraph from a scholarship essay as the voice sample.

**Scorecard (draft):** 9/100. Goal 3 (which essay, which prompt), context 0,
constraints 0, format 2 (an essay is implied), audience 0, verification 0, scope 4.

**Rewrite B (recommended):**

```
Write a first draft of my Common App essay for the prompt: "Describe a topic, idea,
or concept you find so engaging that it makes you lose all track of time." Readers
are admissions officers skimming hundreds of essays, so the first two sentences must
be concrete and mine, not a definition or a rhetorical question.

Use only these two true things, and nothing invented: (1) rebuilding a bike
derailleur at 2 a.m. after breaking it, and figuring out the indexing from the click
pattern; (2) teaching my cousin to ride last summer and noticing I explain by feel,
not by steps. The idea the essay is about: I lose time when a mechanism has a
pattern I can almost hear. Do not add achievements, quotes, or a moral at the end.

Match the voice in the sample below: short sentences, plain words, a little dry.
Under 650 words, five to seven paragraphs, no title, no headings.

<voice_sample>
[pasted paragraph]
</voice_sample>

Before returning it: state the word count, confirm nothing outside the two stories
was invented, and read it once aloud for any sentence I would not say.
```

**Rewrite C (interview form):**

```
I need a first draft of my Common App essay (650 words). Before writing, ask me
up to five questions in one batch: which prompt, who reads it, two or three true
things I could use, what to avoid, and a sample of my writing to match. Then
propose a one-line arc and wait for my yes before drafting.
```

**Patterns applied:** specific deliverable with the assignment quoted (P1), closed fact
list (P3, which also blocks invented material), constraints with the reason (P4),
format and length (P5), voice by sample (P6), self-check (P10), interview gate (P9 in
C). Not applied: a persona ("award-winning essayist" pushes toward polish the readers
distrust), chain-of-thought.

---

## 8. Cowork folder, history paper

**Draft:** "help with my paper"

**Context collected (folder):** assignment.pdf (question: "To what extent was the
Marshall Plan a strategic rather than humanitarian program?", 1,500 words, Chicago
notes), rubric.md (thesis 30%, use of assigned sources 30%, structure 20%, prose 20%),
sources/ (four assigned readings as PDFs), drafts/v1.md (900 words, no thesis yet),
feedback-v1.txt ("your intro summarises; take a position").

**Interview:** two questions, the rest answered by the folder. Stance? "Strategic
first, humanitarian as means." Which sources must appear? "All four, Kennan and
Hogan most."

**Rewrite B (recommended):**

```
Revise drafts/v1.md into drafts/v2.md, a 1,500-word paper answering
assignment.pdf's question: "To what extent was the Marshall Plan a strategic rather
than humanitarian program?" Thesis, stated in the first paragraph and in my words:
strategic first, with humanitarian aid as the means. feedback-v1.txt says the intro
summarises instead of taking a position; fix that first.

Use only the four readings in sources/, citing each at least once in Chicago
footnotes, with Kennan and Hogan carrying the argument. Do not add facts, dates, or
quotations that are not in those files. Keep my sentences from v1 where they already
support the thesis; rewrite, do not pad.

Structure per rubric.md: thesis, three body sections (one per line of evidence), a
counter-argument paragraph, a conclusion that answers "to what extent". Prose:
plain, no rhetorical questions, no "throughout history".

Before returning: word count, a checklist against the four rubric lines, a list of
every footnote's source file, and confirmation that nothing outside sources/ was
used. Write v2.md; leave v1.md unchanged.
```

**Patterns applied:** project substitution from the folder (P13: the question, rubric
lines, source files, feedback), specific deliverable as a file (P1, P5), closed source
list (P3), constraints with reasons (P4), self-check against the rubric (P10). Not
applied: role (the writer is the student), interview beyond two questions (the folder
answered the rest).
