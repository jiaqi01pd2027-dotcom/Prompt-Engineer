---
name: prompt-engineer
description: Grade, interview, and rewrite a prompt so it gets the best output from Claude, adapted to the project, document folder, or assignment it will run in. Use whenever the user asks to improve, refine, fix, rate, grade, review, or rewrite a prompt; asks "how should I ask for X" or "what is the best way to prompt for X"; pastes a prompt and wants feedback; wants a system prompt, subagent prompt, skill description, or CLAUDE.md instruction phrased well; is about to ask Claude to write an essay, article, cover letter, email, report, or any document and wants the ask phrased well ("help me write my college essay", "I need a prompt for my history paper"); works in a Cowork folder with a brief, rubric, or past drafts; or invokes /prompt-engineer. Also use when the user says their prompts keep getting mediocre results, even if they do not say the word "prompt".
---

# Prompt engineer

Turn a draft prompt into the version that gets the best output, using facts from the
project, folder, or assignment it will run in: code and agent prompts, and writing
prompts (essays, articles, letters, reports) alike. The model is the same either way;
the wording changes the result. Four steps: collect context, grade the draft out of
100, ask the few questions that would change the rewrite, then give three rewrites
and name the patterns each one uses.

Read `references/rubric.md` when grading and `references/context-adaptation.md` when
collecting context. The pattern table below is enough to name patterns and their
evidence; open `references/patterns.md` only when the user asks why a pattern works.
`references/examples.md` has eight worked cases; skim one to calibrate reply length.

## Pattern table (from 360 blind-judged runs on Fable 5.1, Opus 5, Sonnet 5; 0 to 10)

| id | pattern | evidence | mean score | one-line use |
|---|---|---|---|---|
| P1 | specific deliverable | strong | 7.09 (bare: 5.46) | say what, for whom, what done means |
| P3 | context and the why | strong where facts are missing | 7.13 | facts the model cannot infer, with the reason |
| P4 | constraints naming the failure | strong | 7.88 | limits and do-nots that say why |
| P5 | output format with a shape | strong | 8.40 | exact structure, where the output goes |
| P6 | few-shot by example or pointer | moderate | 8.12 | 2 to 3 examples or "match file X" |
| P8 | full stack, ordered | strong | 9.12 | role (if real), goal, context, constraints, format |
| P9 | interview first | strong when facts are missing | 8.75 | ask up to N questions, then act |
| P10 | verification and done-criteria | strong (agentic) | see P8 | run the check, report evidence, stop rule |
| P11 | decompose and chain | moderate | | one ask, or ordered steps with a stop |
| P12 | positive framing | moderate | | say what to do, then rule out the misreading |
| P13 | project substitution | strong (agentic) | | real files, commands, examples, audience |
| P2 | role | weak (tone only) | 6.94 | only when a real expert persona exists |
| P7 | chain-of-thought cue | weak on current Claude | 6.99 | only for bare-answer multi-step logic |

## Workflow

### 1. Capture the draft and the target

Take the prompt from the arguments, the last message, or a file the user points at. If
there is no draft yet, ask for the one-line goal and treat that as the draft (it will
grade low; that is fine).

Establish where it will run, because the rewrite shape depends on it:
Claude Code in this repo, claude.ai chat, an API system prompt or template, a
subagent, or a writing task (essay, article, letter, report; in chat or in a Cowork
document folder). Infer it when obvious (a prompt that names files and tests is
agentic; one that pastes an email or names an assignment is writing); otherwise it is
the first interview question.

### 2. Collect project context before judging

Follow `references/context-adaptation.md`. Read only; never modify. In a repo: CLAUDE.md,
README, the manifest, `git log --oneline -15`, and any file the prompt names; if it names
a concept ("the parser"), find the file that implements it. Pull exact identifiers and
commands, and note whether the project's check can actually run here; if it cannot, the
rewrite says to report that rather than install things.

In a Cowork or document folder: the brief, any rubric, prior drafts and their feedback,
a style guide, one sample of the user's own writing. With no folder, collect the same
facts in the interview. Everything found here is rewrite material and removes an
interview question. With no project, skip to grading.

### 3. Grade the draft

Score it with `references/rubric.md` and show a scorecard:

| Dimension | Score | Evidence |
|---|---|---|
| Goal and deliverable | 8/20 | "help with the docs" names no output |
| ... | | |
| **Total** | **41/100** | band: the model will guess most of what matters |

One line of evidence per row, quoting the draft or noting the absence. Show any rubric
adjustment as its own row before the total. No praise padding. Then name the two
dimensions whose fix would move the grade most.

### 4. Interview, batched

Use AskUserQuestion with three to six questions in one call, never one at a time. Without
that tool, one numbered list with the recommended default marked; proceed on the defaults
if unanswered. Ask only about gaps that would change the rewrites. Each question offers
concrete options, recommended default first, plus room for free text. Skip any the project
answers and say what you inferred ("assuming `pytest -q`, from the Makefile").

Pick from the seven standing questions in `references/context-adaptation.md` rather
than inventing new ones: reader, done, must-not, format, hard constraints, plan or go,
and for writing the thesis, grader, sources, and voice sample.

If the user says "just rewrite it", skip the interview and mark unknowns as
`[placeholders]` with a list of what to fill in. Facts only the user holds (a thesis,
true experiences, a voice sample) have no default: placeholder them, never invent.

### 5. Rewrite three ways

Give three options, each in its own fenced block so it can be copied whole. Keep the
user's voice and any exact wording they clearly chose. Never invent facts; unknowns
become `[bracketed placeholders]`. When a placeholder holds the keystone fact, the one
the whole prompt turns on, do not bury it: open the rewrite with "Fill in before
sending: X" and keep it out of the acceptance criterion, which has to stay checkable.
A done condition resting on an unfilled blank cannot be met. The exception is a file
the project loads as-is (a system prompt, a template): a literal bracket reaching
production is worse than a stated default, so write your best default in the block and
list it under "Before deploying, confirm:" after it.

- **A. Minimal.** The draft with only the two highest-value fixes, as short as those
  fixes allow; for a draft under fifteen words, up to three sentences. For people who
  want their prompt, not a new one.
- **B. Structured.** Role (only if a real expert persona exists), goal, the reader and
  what they do with the output, context from the project, constraints with the failure
  modes they prevent, output format, and how to verify. Important thing first.
- **C. Interview or agentic.** Chat: ask up to N questions first. Claude Code: plan,
  name files and commands, define done, verify. Each target shapes A, B and C
  differently; the table is "Rewrite shapes by target" in
  `references/context-adaptation.md`. Read it once per target, not per draft.

Every writing rewrite ends with a self-check the model reports after the piece, under
a separator so the piece copies clean. Name the constraints most likely to break, not
the safe ones: quote the banned words and openers back, give the word and paragraph
counts, list each rubric line. Every item must produce an artifact the reader can look
at, never an attestation: "list every sentence over 35 words", not "confirm you read it
aloud". A check the model can satisfy by claiming it did is worth nothing, and a check
confirming what it was never going to get wrong is decoration.

Every agentic rewrite (B and C for Claude Code or a subagent) ends with three named
parts: the check to run; what to deliver when it cannot run or a needed fact is
missing (a named file, a question to the user, or a report); and a stop rule saying
whether to halt the task or skip that step and continue. When the project's own check
provably cannot run here, do not stop at reporting that: name one that can, such as
tracing every claim back to the source line it came from. Give whatever the model
reports back a shape, named sections in order: that report is the part the user
actually reads, and "run this check" with no antecedent leaves them guessing.

Before delivering, read each rewrite once as the model would receive it. Confirm it
names its reader; that clause is the one most often dropped. Where it points at an
exemplar to copy, say which parts do not apply, or "match X" will fight the additions
you just asked for. Then fix any pair that fights: a stop rule naming a file the plan
step may edit, a length target the allowed sources cannot fill, a format the
constraints forbid, "proceed without
waiting" beside "ask me first". When a pair cannot both hold, say which wins inside
the rewrite ("if the notes run out before 1,800 words, stop and list what is missing
rather than padding"). The rubric costs 5 points per contradictory pair.

Pick which of the three to recommend and say why in one sentence.

### 6. Explain the patterns applied

Under "Patterns applied", list each pattern used with a short reason and its evidence
and mean score from the table above ("constraints naming the failure, strong, 7.88").
Also name one or two you deliberately did not apply and why ("no chain-of-thought cue:
Claude already reasons here; it adds length, not accuracy").

### 7. Show how to push it higher

Under "To push it higher", give the projected score of the recommended rewrite, the
remaining gaps in rubric terms, and the exact facts the user could add to close them.
If the target is Claude Code, offer to run the recommended prompt now.

## Output shape

Keep the whole reply scannable: scorecard, the rewrites, "Patterns applied" and "To
push it higher" as short lists. Print the recommended rewrite in full; give the other
two as a fenced block only if they are under ten lines, otherwise one line each
naming what they change ("A: the two fixes only, four lines"). Offer the full text on
request. No preamble about what prompt engineering is. No restating the draft. Aim for
60 lines; a short draft gets a shorter reply.

## Rules that keep rewrites honest

- Shorter beats longer at equal clarity. Every added sentence must remove a guess the
  model would otherwise make.
- Do not add a role when there is no meaningful expert for the task. In writing, a
  role earns its place only when it fixes voice (a specific reader or writer), never
  as a source of facts; the user's own voice sample beats any persona.
- Do not add "think step by step" for current Claude models unless the task is
  multi-step logic and the draft asks for a bare answer.
- Do not stack "always" and "never" on style rules; say what to do and why.
- Name the project's real files, commands, audiences, and examples instead of generic
  nouns. That substitution is where most of the gain comes from. It includes commit
  hashes instead of "the last commit", function names instead of "the stubs", package
  names instead of "the deps", and an absolute repo path in any subagent brief.
- When you add no role, name the reader and what they do with the output in one
  clause ("for the on-call engineer who triages the board").
- Constraints name the failure mode ("do not ask them to retry; they already did
  twice"), not just the rule.
- Carry the user's own bans word for word. "Do not say passionate" bans the word, not
  one phrase containing it; narrowing a ban restores what the user cut.
- When a length target and the available material disagree, say which wins. Thin
  sources plus a word count produce padding or a skeleton unless the rewrite names
  the tie-break and caps the `[add example]` markers.
- For agentic prompts, always include how to verify and what not to touch.
- Keep the user's decisions. If they wrote "under 100 words", do not change the number.

## Quick examples

"Write tests for the parser" grades 18/100 and "write my college essay" 9/100; both
recommended rewrites are `references/examples.md`, cases 6 and 7.
