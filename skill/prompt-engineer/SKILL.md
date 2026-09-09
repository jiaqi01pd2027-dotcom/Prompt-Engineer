---
name: prompt-engineer
description: Grade, interview, and rewrite a prompt so it gets the best output from Claude, adapted to the project it will run in. Use whenever the user asks to improve, refine, fix, rate, grade, review, or rewrite a prompt; asks "how should I ask for X" or "what is the best way to prompt for X"; pastes a prompt and wants feedback; wants a system prompt, subagent prompt, skill description, or CLAUDE.md instruction phrased well; or invokes /prompt-engineer. Also use when the user says their prompts keep getting mediocre results, even if they do not say the word "prompt".
---

# Prompt engineer

Turn a draft prompt into the version that gets the best output, using facts from the
project the prompt will run in. The model is the same either way; the wording is what
changes the result. This skill does four things in order: collects context, grades the
draft out of 100, asks the few questions that would change the rewrite, then gives three
rewrites and explains which patterns each one uses and why.

Read `references/patterns.md` once per session for the pattern catalogue and the
evidence behind it. Read `references/rubric.md` when grading and
`references/context-adaptation.md` when collecting context. `references/examples.md`
has worked before/after cases to match in tone and length.

## Workflow

### 1. Capture the draft and the target

Take the prompt from the arguments, the last message, or a file the user points at. If
there is no draft yet, ask for the one-line goal and treat that as the draft (it will
grade low; that is fine).

Establish where it will run, because the rewrite shape depends on it:
Claude Code in this repo, claude.ai chat, an API system prompt or template, or a
subagent. Infer it when obvious (a prompt that names files and tests is agentic; one
that pastes an email is chat); otherwise it is the first interview question.

### 2. Collect project context before judging

Follow `references/context-adaptation.md`. In a repo, read CLAUDE.md, README, the
manifest, `git log --oneline -15`, and any file the prompt names. Pull exact
identifiers, commands, and conventions. Everything you learn here is material for the
rewrite and removes interview questions. Read only; never modify.

If there is no project, skip to grading and collect the same facts in the interview.

### 3. Grade the draft

Score it with `references/rubric.md` and show a scorecard:

| Dimension | Score | Evidence |
|---|---|---|
| Goal and deliverable | 8/20 | "help with the docs" names no output |
| ... | | |
| **Total** | **41/100** | band: the model will guess most of what matters |

One line of evidence per row, quoting the draft or noting the absence. Do not pad the
table with praise. Then state the two dimensions whose fix would move the grade most.

### 4. Interview, batched

Use AskUserQuestion with three to six questions in one call, never one at a time. Ask
only about gaps that would make the rewrites materially different. Each question offers
concrete options with a recommended default first, plus room for free text. Skip any
question the project context already answers and say what you inferred instead
("I am assuming the tests are `pytest -q`, from the Makefile").

Typical questions, pick from these rather than inventing new ones:
- Who reads or runs the output, and what will they do with it?
- What does done look like (tests pass, a file exists, a number, a decision)?
- What must it not do (touch, mention, assume, exceed)?
- What format or example should it match?
- Which constraints are hard (length, deadline, budget, tone)?
- Should the model plan first, ask before acting, or just go?

If the user says "just rewrite it", skip the interview and mark unknowns as
`[placeholders]` in the rewrite with a list of what to fill in.

### 5. Rewrite three ways

Give three options, each in its own fenced block so it can be copied whole. Keep the
user's voice and any exact wording they clearly chose. Never invent facts; unknowns
become `[bracketed placeholders]`.

- **A. Minimal.** The draft with only the two highest-value fixes. Same length or
  shorter. For people who want their prompt, not a new one.
- **B. Structured.** Role (only if a real expert persona exists), goal, context from
  the project, constraints with the failure modes they prevent, output format, and how
  to verify. Ordered so the important thing comes first.
- **C. Interview or agentic.** For chat: the model is told to ask up to N questions
  before answering. For Claude Code: plan first, name the files and commands, define
  done, say how to verify, say whether to proceed without confirming. For system
  prompts: identity and rules in the system slot, per-request material with
  `{{variables}}`, one worked example.

Pick which of the three to recommend and say why in one sentence.

### 6. Explain the patterns applied

Under "Patterns applied", list each pattern used with a short reason and the evidence
tag from `references/patterns.md` (for example "constraints and negatives: largest
single gain in our adherence scores; see patterns.md P4"). Also list one or two
patterns you deliberately did not apply and why (for example "no chain-of-thought
cue: Claude already reasons on this task; the cue added length without accuracy").

### 7. Show how to push it higher

Under "To push it higher", give the projected score of the recommended rewrite, the
remaining gaps in rubric terms, and the exact facts the user could add to close them.
If the target is Claude Code, offer to run the recommended prompt now.

## Output shape

Keep the whole reply scannable: scorecard, three fenced rewrites with one-line labels,
"Patterns applied" as a short list, "To push it higher" as a short list. No preamble
about what prompt engineering is. No restating the draft. Match the length of the
examples in `references/examples.md`; a short draft gets a short reply.

## Rules that keep rewrites honest

- Shorter beats longer at equal clarity. Every added sentence must remove a guess the
  model would otherwise make.
- Do not add a role when there is no meaningful expert for the task.
- Do not add "think step by step" for current Claude models unless the task is
  multi-step logic and the draft asks for a bare answer.
- Do not stack "always" and "never" on style rules; say what to do and why.
- Name the project's real files, commands, audiences, and examples instead of generic
  nouns. That substitution is where most of the gain comes from.
- Constraints name the failure mode ("do not ask them to retry; they already did
  twice"), not just the rule.
- For agentic prompts, always include how to verify and what not to touch.
- Keep the user's decisions. If they wrote "under 100 words", do not change the number.

## Quick example

Draft: "write tests for the parser"

Scorecard total 34/100. Context found: Python repo, `pytest -q`, tests live in
`tests/`, `parse_iso_duration` in `src/durations.py`, CLAUDE.md says "no mocks".

Recommended rewrite (B):

```
Add pytest tests for parse_iso_duration in src/durations.py. Put them in
tests/test_durations.py, matching the style of tests/test_dates.py. Cover: each
component alone, all components together, fractional seconds, weeks, and three
invalid strings that must raise ValueError. No mocks (CLAUDE.md). Run `pytest -q`
and report the results; if any new test fails, say whether the test or the parser is
wrong rather than changing the parser.
```

Patterns applied: specific deliverable and location; project context substituted
for generic nouns; few-shot by pointing at an existing test; constraints with the
reason; verification and a stop rule. Not applied: role, chain-of-thought.
