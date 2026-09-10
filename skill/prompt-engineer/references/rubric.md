# Prompt grading rubric (score out of 100)

Grade the prompt as written, before any interview. Each dimension has a max and three
anchors. Pick the anchor that fits, interpolate if needed, and write one line of
evidence per dimension quoting the prompt (or noting the absence).

| # | Dimension | Max | 0 | Half | Full |
|---|-----------|-----|---|------|------|
| 1 | Goal and deliverable | 20 | Vague verb, no object ("help with my essay") | Task named but success undefined | States what is produced, for whom, and what "done" looks like |
| 2 | Context | 20 | None; the model must guess the situation | Some background, key facts missing | Situation, audience, relevant numbers/files/constraints from the project are present |
| 3 | Constraints and negatives | 15 | None | Length or tone only | Length, tone, scope, and explicit "do not" items that name the failure mode |
| 4 | Output format | 15 | Unspecified | Loosely stated ("a list") | Exact shape: sections, count, schema, file path, or example |
| 5 | Role and audience | 10 | Neither | One of the two | Both, and the role is specific to the domain. If no meaningful expert persona exists for the task, score audience alone out of 10 |
| 6 | Reasoning and verification | 10 | None | "Think carefully" only | Asks for a plan, checks, tests, or self-review appropriate to the task |
| 7 | Scope and decomposition | 10 | Many unrelated asks in one prompt | One ask but with hidden sub-steps | One ask, or ordered steps with a stop condition |

## Bands

- 85-100: ship it. Interview only if a fact is missing.
- 65-84: good bones. Two or three targeted additions will move it a band.
- 40-64: the model will guess most of the important things. Interview needed.
- 0-39: a command, not a prompt. Rewrite from the goal up.

## Adjustments (apply after summing; show each as its own row before the total)

- Agentic target (Claude Code, tools, files): if the prompt does not say how to verify
  (tests, screenshots, lint) subtract 5; if it asks for a plan before editing on a
  non-trivial change add 0 (already counted in #6) but mention it as a strength.
- Over-specification: if the prompt is more than ~400 words and half of it is
  restating obvious things, subtract up to 5 for "noise the model must wade through".
- Contradictions: subtract 5 per contradictory instruction pair (e.g. "be brief" and
  "cover everything in depth").
- Absolutes: "always"/"never" applied to style rather than safety can over-trigger in
  current Claude models; note it as an improvement rather than a penalty.

## What NOT to penalise

- Short prompts for trivial tasks. A one-line prompt for "rename this variable" can
  score 90 if goal, scope, and format are obvious from the project.
- Missing role when the task has no meaningful expert persona.
- Missing chain-of-thought instructions for current reasoning models; only reward it
  when the task is multi-step logic and the model is not already reasoning.
