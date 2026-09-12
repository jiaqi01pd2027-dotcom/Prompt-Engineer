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

Follow `references/context-adaptation.md`. In a repo, read CLAUDE.md, README, the
manifest, `git log --oneline -15`, and any file the prompt names. If the prompt names
a concept rather than a file ("the parser", "the login flow"), find the file that
implements it. Pull exact identifiers, commands, and conventions. Note whether the
project's check (tests, build, lint) can actually run in this environment; if it
cannot, the rewrite should tell the model to report that rather than install things. Everything you learn here is material for the
rewrite and removes interview questions. Read only; never modify.

In a Cowork or document folder, read the brief or assignment, any rubric, prior
drafts and feedback on them, a style guide, and one sample of the user's own writing
(for voice). For a writing task with no folder, collect the same facts in the
interview: the exact assignment wording, who grades or reads it, length, sources
allowed, a stance or thesis if the user has one, and what to avoid. If there is no
project at all, skip to grading and collect the facts in the interview.

### 3. Grade the draft

Score it with `references/rubric.md` and show a scorecard:

| Dimension | Score | Evidence |
|---|---|---|
| Goal and deliverable | 8/20 | "help with the docs" names no output |
| ... | | |
| **Total** | **41/100** | band: the model will guess most of what matters |

One line of evidence per row, quoting the draft or noting the absence. Show any
adjustment from the rubric (the agentic verification penalty, contradictions) as its
own row before the total. Do not pad the table with praise. Then state the two
dimensions whose fix would move the grade most.

### 4. Interview, batched

Use AskUserQuestion with three to six questions in one call, never one at a time. If
that tool is not available, put the same questions in one numbered list with the
recommended default marked, and continue with the defaults if the user does not
answer. Ask only about gaps that would make the rewrites materially different. Each question offers
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
- For writing: what is the thesis or stance, who grades it and against what, what
  facts and sources may be used, and is there a sample of your own voice to match?

If the user says "just rewrite it", skip the interview and mark unknowns as
`[placeholders]` with a list of what to fill in. Facts only the user holds (a thesis,
true experiences, a voice sample) have no default: placeholder them, never invent.

### 5. Rewrite three ways

Give three options, each in its own fenced block so it can be copied whole. Keep the
user's voice and any exact wording they clearly chose. Never invent facts; unknowns
become `[bracketed placeholders]`.

- **A. Minimal.** The draft with only the two highest-value fixes, as short as those
  fixes allow; for a draft under fifteen words, up to three sentences. For people who
  want their prompt, not a new one.
- **B. Structured.** Role (only if a real expert persona exists), goal, context from
  the project, constraints with the failure modes they prevent, output format, and how
  to verify. Ordered so the important thing comes first.
- **C. Interview or agentic.** For chat: the model is told to ask up to N questions
  before answering. For Claude Code: plan first, name the files and commands, define
  done, say how to verify, say whether to proceed without confirming. For system
  prompts: B is one self-contained block; C splits identity and rules into the system
  slot and per-request material into `{{variables}}`, with one worked example. For a
  subagent brief: A is the one-line ask the user gives the parent, B is the
  self-contained brief (every fact, read-only rules, return shape), C is B plus a
  stop rule and an exact return schema. For writing: B carries the assignment
  wording, audience and grader, thesis, the facts and sources allowed (and only
  those), length, format, voice sample or pointer, and what to avoid with the reason;
  C tells the model to ask up to N questions or to outline first and wait, then draft,
  then check itself against the brief. In our writing tasks the interview form (8.67)
  and full stack (8.63) led; a role alone scored 5.43, so use a role only for voice.

Placeholders: for chat and Claude Code targets, unknowns become `[bracketed
placeholders]`. For a system prompt or any file the project loads as-is, put no
placeholders inside the block; list unknowns under "Before deploying, fill in:" after
the block, or turn them into interview questions.

Every writing rewrite ends with a self-check the model reports after the piece, under
a separator so the piece copies clean: word count against the limit, each required
section or rubric line present, no invented facts, quotes, or citations, one
read-aloud pass for voice. Every agentic rewrite (B and C for Claude Code or a
subagent) ends with three named parts: the check to run; what to deliver when the check cannot run or a needed fact is
missing (a named file, a question to the user, or a report); and a stop rule that says
whether to halt the whole task or skip that step and continue with the rest.

Pick which of the three to recommend and say why in one sentence.

### 6. Explain the patterns applied

Under "Patterns applied", list each pattern used with a short reason and the evidence
column and mean score from the pattern table above (for example "constraints naming
the failure, strong, 7.88"); open `references/patterns.md` only if the user asks why. Also list one or two
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
- For agentic prompts, always include how to verify and what not to touch.
- Keep the user's decisions. If they wrote "under 100 words", do not change the number.

## Quick examples

Coding draft "write tests for the parser" grades 18/100; with the repo's facts the
recommended rewrite names the function, file, style file to match, cases, the no-mocks
rule, `pytest -q`, and a stop rule (full text: `references/examples.md`, case 6).
Writing draft "write my college essay" grades 9/100; with the brief, the grader, the
prompt question, two true stories the user supplied, a 650-word limit, and a voice
sample, the recommended rewrite is case 7 in `references/examples.md`.
