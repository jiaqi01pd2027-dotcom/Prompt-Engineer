# Pattern catalogue with evidence

Each pattern: what it is, the phrasing that works, when it helps, when it hurts, and
the evidence. "Lit" cites published studies (full citations in the project paper).
"Anthropic" cites Claude's current prompting docs. "Exp" cites this project's own
blind-judged runs (12 tasks x 10 patterns x 3 Claude models); see
`experiments/results/summary.md` in the repo for the numbers.

Evidence strength: strong = replicated across studies and our runs; moderate = one
solid source or consistent in our runs; weak = contested or model-specific.

Headline from our runs: full stack 9.12, interview 8.75, format 8.40, few-shot 8.12,
constraints 7.88, context 7.13, specific 7.09, chain-of-thought 6.99, role 6.94,
bare 5.46 (mean judge score, 0 to 10). Same ordering on Fable 5.1, Opus 5, Sonnet 5.
Sonnet 5 with the full stack (9.12) beat Fable 5.1 with a bare prompt (6.07).

---

## P1. Specific deliverable (strong)

State what is produced, for whom, and what done looks like. The single biggest jump is
from a command ("summarize this") to a deliverable ("four bullets on decisions and
owners, for the VP who missed the meeting").

Phrasing: `Write a <thing> for <audience> that <does what>. Done means <check>.`

Helps: every task type. Hurts: nothing, unless the specifics are wrong.

- Lit: Yang et al. 2025, models infer unstated requirements only 41% of the time;
  under-specified prompts regress twice as often across model changes.
- Anthropic: "the more precisely you explain what you want, the better the result";
  the colleague test: if a colleague with no context would be confused, so is Claude.
- Exp: 7.09 vs 5.46 for the bare command (0 to 10, 36 runs each); the largest single step in extraction (1.80 to 9.13) and agentic planning.

## P2. Role (weak for accuracy, moderate for tone)

"You are a senior B2B copywriter." A role sets voice and what counts as good; it does
not make the model know more.

Helps: writing, replies, anything where the audience's taste matters. Hurts: factual
and reasoning tasks (no gain, occasional loss); tasks with no real expert.

- Lit: Zheng et al. 2023 (162 personas, no accuracy gain); Wharton 2025 replication
  (9 significant degradations, none significant improvements); Kong et al. 2023 gains
  look like an accidental reasoning trigger.
- Anthropic: "even a single sentence makes a difference" for focus and tone.
- Exp: 6.94, below the specific statement it was added to (7.09); moved tone on the writing tasks and nothing else.

## P3. Context and the why (strong)

Give the situation, the numbers, the files, the audience, and the reason behind each
rule. "Never use ellipses" loses to "this is read aloud by text-to-speech, so no
ellipses."

Phrasing: `Background: <facts>. This matters because <reason>.`

Helps: any task where the model would otherwise guess facts. Hurts: when the context is
long and buried in the middle (lost-in-the-middle), or is generic overview the model
can infer itself.

- Lit: Liu et al. 2023 U-shaped attention; Gloaguen et al. 2026 generic repo overviews
  in AGENTS.md add cost without lifting success, while non-standard rules help.
- Anthropic: "Claude is smart enough to generalize from the explanation."
- Exp: 7.13 overall, but decisive where the task needed facts the model could not infer (support reply: 1.93 to 7.40 on its own) and neutral elsewhere; it lowered concision (6.61) because models wrote more.

## P4. Constraints that name the failure mode (strong)

Length, tone, scope, and "do not" items that say why. "Do not ask them to retry; they
already tried twice" beats "do not ask them to retry."

Phrasing: `Under N words. Do not <X>, because <failure it causes>. Prefer <Y> instead.`

Helps: adherence, concision, anything with a reader who will notice filler. Hurts:
stacking many constraints (IFEval: even GPT-4 misses one prompt in four); naming a
forbidden word primes it (Rana 2026: 87% of violations are priming failures), so state
the wanted behaviour when the banned term is likely anyway.

- Lit: Zhou et al. 2023 IFEval; Rana 2026; Truong et al. 2023 negation insensitivity.
- Anthropic: "tell Claude what to do instead of what not to do"; recent models
  over-trigger on "CRITICAL" and "ALWAYS", so use plain "Use X when Y."
- Exp: 7.88; adherence 7.50 and concision 7.75 against 6.33 and 6.75 for the specific statement; won the transcript summary task. Weak on writing (5.70) when the prompt banned things without supplying the facts to say instead.

## P5. Output format with an example shape (strong)

Exact structure: sections, counts, a JSON schema, a file path, or a filled example.

Phrasing: `Return only <shape>. Example: <one filled instance>.`

Helps: extraction, classification, anything parsed downstream, anything the reader
scans. Hurts: creative writing when the format is imposed for no reason.

- Lit: He et al. 2024 (format alone moves smaller models up to 40%); Sclar et al. 2023
  (formatting spread up to 76 points); Min et al. 2022 (examples teach format more
  than content).
- Anthropic: examples are "one of the most reliable ways to steer format"; XML tags
  for delimiting; Structured Outputs replaces prefill.
- Exp: 8.40, the best single addition; won three tasks; 94% objective pass; a perfect 10 on receipt extraction. On coding tasks it also decided whether the code landed in the reply or in a file the reader never sees.

## P6. Few-shot examples (moderate; strong for format and voice)

Two or three input/output pairs in the wanted style, wrapped in tags, diverse enough
not to be copied verbatim.

Helps: style matching, classification labels, ticket titles, anything with a house
voice. Hurts: reasoning models (DeepSeek-R1 report: few-shot degrades), large code
models (Cheng and Mastropaolo 2026), and any case where the examples get parroted.

- Lit: Min et al. 2022; Lu et al. 2022 (order sensitivity); Agarwal et al. 2024
  (many-shot with long context).
- Anthropic: 3 to 5 examples, relevant, diverse, in `<example>` tags.
- Exp: 8.12; won the feature-plan task and helped wherever voice or shape mattered; two extraction outputs copied an example's wording instead of the input's.

## P7. Chain-of-thought cue (weak on current Claude)

"Think step by step, then answer." Historically large gains on arithmetic; on models
that reason internally it mostly adds length.

Helps: multi-step logic when the model is asked for a bare answer and thinking is off.
Hurts: pattern-recognition tasks (Liu et al. 2024, up to 36 points lost); latency;
Opus 5 over-verifies when told to check.

- Lit: Wei 2022, Kojima 2022 (historic); Sprague 2024 (gains concentrate on math);
  Wharton 2025 Report 2 (reasoning models gain 3% for 20 to 80% more latency).
- Anthropic: prefer "think thoroughly" over a hand-written step plan; adaptive thinking
  beats manual CoT; the `effort` parameter replaces "think hard" tiers.
- Exp: 6.99; highest correctness of the single additions (8.53) and the lowest concision of any pattern (5.06); every run of every pattern already solved both reasoning tasks, so the cue bought nothing there.

## P8. The full stack, ordered (strong)

Role (if real) + goal + context + constraints + format, important thing first, task at
the end after any long material.

Helps: any non-trivial one-shot request. Hurts: trivial tasks (over-specification is
noise); contradictions inside the stack (GPT-5 and Claude docs both flag conflicting
rules as the top failure).

- Lit: Bsharat et al. 2023 structural principles replicate; incentive principles (tips,
  threats) do not (Wharton 2025).
- Anthropic: long data at top, query at end, "up to 30%" better on long inputs.
- Exp: 9.12, first on every model; 99% objective pass; won five of twelve tasks outright and was within 0.1 of the winner on four more.

## P9. Interview first (strong when facts are missing)

Tell the model to ask its questions before acting, or ask the user yourself and fold
the answers in. Gate on ambiguity: ask only when different answers would change the
work.

Phrasing (chat): `Before writing, ask me up to 5 questions about anything that would
change the result. Then write it.` (Claude Code): batched question tool, 3 to 6
questions, recommended default first.

Helps: any task where the user does not know what context matters; coding with
under-specified issues (Ambig-SWE: up to 74% better with interaction; ClarifyGPT:
+10 pass@1). Hurts: autonomous runs where nobody can answer; trivial tasks.

- Lit: Zhang and Choi 2023; Mu et al. 2023; Vijayvargiya et al. 2025; Bsharat
  principle 14 improved every question it was applied to.
- Anthropic: "check in only when different readings would lead to materially different
  work"; autonomous prompts suppress "Shall I...?".
- Exp: 8.75 with the answers supplied, matching the full stack on correctness and completeness and trailing on concision (echoed Q&A); best pattern on the vague product brief.

## P10. Verification and done-criteria (strong for agentic)

Say how the model can check its own work: run the tests, render the page, diff against
the example. Demand evidence, not a claim.

Phrasing: `Run <command>. Report the output. If it fails, say whether the test or the
code is wrong; do not change the test to pass.`

- Lit: Reflexion (Shinn 2023) 91% vs 80% HumanEval with feedback; OpenAI GPT-4.1 guide
  +20 points SWE-bench from persistence, tool-use, and planning reminders.
- Anthropic: "give Claude a check it can run"; "show evidence rather than asserting
  success"; do not tell Opus 5 to double-check (over-verifies).

## P11. Decompose and chain (moderate)

One ask per prompt, or ordered steps with a stop condition. Inspect intermediate
outputs on pipelines.

- Anthropic: chaining "still useful when you need to inspect intermediate outputs";
  draft, review, refine is the common self-correction chain.
- Lit: Prompt Report decomposition family; Tree of Thoughts for search-shaped tasks.

## P12. Positive framing (moderate)

Say what to do, then rule out the nearest misreading with a contrast pair: "Brief is
good; silent is not."

- Lit: Truong 2023; Rana 2026. Anthropic: matching prompt style to output style.

## P13. Project substitution (strong; the hard part)

Replace every generic noun with the project's own: the real test command, the real
file, an existing example in the repo, the real audience from the README, the branch
name. This is where most of the gain in Claude Code comes from and it costs nothing.

- Lit: Gloaguen 2026 (context files help only when they carry non-standard facts);
  Cheng and Mastropaolo 2026 (defaults copied from elsewhere lower correctness).
- Anthropic: "only add context Claude doesn't already have"; CLAUDE.md test: "would
  removing this cause a mistake?"

## Patterns to avoid or ration

- Tips, threats, emotional appeals: no reliable gain on 2025 models, high per-question
  variance (Wharton Aug 2025).
- ALL CAPS, "CRITICAL", "MUST", stacked "always/never": current Claude over-triggers;
  emphasis is a scarce signal, spend it on one line.
- Contradictory rules: the top failure mode named by both Anthropic and OpenAI.
- Long generic preambles about the model's identity: cost without benefit.
- Politeness or rudeness as a lever: sign flips across models and years.

## Model notes (Claude family, September 2026)

- Fable 5.1: batch independent tool calls; finishes tasks without check-ins when told
  the user is away; suppressing structure can hide structure the content needs.
- Opus 5: remove self-verification instructions (over-verifies); with thinking off it
  can emit internal tags; sensitive to the word "think".
- Sonnet 5: reads literally; spell out the deliverable and format; benefits most from
  P4 and P5.
- All: prefill unsupported; use Structured Outputs or "respond directly without
  preamble"; `effort` controls depth, only `ultrathink` is a recognised keyword in
  Claude Code.
