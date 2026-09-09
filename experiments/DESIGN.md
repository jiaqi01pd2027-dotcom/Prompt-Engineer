# Experiment design (v1, Claude-only)

Goal: measure how prompt *phrasing patterns* change output quality on the same task,
across the Claude family, so the skill can recommend patterns with evidence.

## Factors

**Tasks (12):** 6 domains x 2 tasks. Each task has a fixed hidden "ground truth" or
rubric that the prompt variants never see.

| Domain | Task id | Description |
|---|---|---|
| coding | code-1 | Write a function to parse and validate ISO-8601 durations (edge cases hidden). |
| coding | code-2 | Debug a short Python snippet with two subtle bugs (off-by-one, mutable default). |
| writing | write-1 | Customer support reply to a failed-export complaint (paying user). |
| writing | write-2 | 250-word LinkedIn post: lessons from a 4-day work week switch. |
| analysis | analysis-1 | Summarize a 900-word meeting transcript into decisions and action items. |
| analysis | analysis-2 | Compare three project tools for a 5-10 person team (features, limits, pricing). |
| extraction | extract-1 | Turn 6 user-feedback lines into support ticket titles "[Area] description". |
| extraction | extract-2 | Extract structured JSON (name, date, amount, category) from 5 messy receipts. |
| reasoning | reason-1 | Multi-step word problem with a discount and tax (single numeric answer). |
| reasoning | reason-2 | Scheduling puzzle with constraints (find a valid assignment). |
| agentic | agent-1 | Plan the steps to add a feature to a described small codebase (no code execution). |
| agentic | agent-2 | Given a vague product brief, produce a scoped implementation plan with risks. |

**Prompt patterns (10):** each variant is written for each task; the underlying task
is identical, only the phrasing changes.

| id | pattern | what changes |
|---|---|---|
| P0 | bare | one vague sentence, no specifics ("write something about X") |
| P1 | specific | precise task statement only (what, for whom, how long) |
| P2 | role | P1 + "You are a <expert role>" |
| P3 | context | P1 + relevant background facts (audience, situation, numbers) |
| P4 | constraints | P1 + explicit constraints and negative instructions (do not...) |
| P5 | format | P1 + exact output format (JSON schema, headings, bullet count) |
| P6 | fewshot | P1 + 2-3 input/output examples |
| P7 | cot | P1 + "think step by step before answering; show reasoning then final answer" |
| P8 | fullstack | role + goal + context + constraints + format combined (the "hierarchy") |
| P9 | interview | model is told to ask clarifying questions first; answers are pre-supplied in a second turn (simulated by giving the Q&A in the prompt) |

**Models (3):** fable (claude-fable-5-1), opus (claude-opus-5), sonnet (claude-sonnet-5).
Each variant is run as a fresh subagent with *only* the variant prompt as its input.
No system context about the experiment is given to the subagent.

Total runs: 12 x 10 x 3 = 360.

## Scoring

1. **Objective checks** (scripted where possible): correct answer (reasoning, code
   tests), JSON validity, length limits, banned phrases absent, required fields present.
2. **Blind LLM judge**: a separate agent receives the task, the rubric, and the 30
   outputs for a task with pattern and model labels stripped and order shuffled.
   Scores 1-10 on: correctness, completeness, instruction adherence, usefulness,
   concision. Also picks a top 3.
3. **Human ratings**: website rating page (side-by-side, blind) collects scores later.

## Output layout

experiments/tasks/<task-id>.md         task, hidden rubric, and the 10 variant prompts
experiments/results/<task-id>/<model>/<Pn>.md   raw output of each run
experiments/results/<task-id>/judge.json        blind judge scores
experiments/results/summary.json                aggregated
