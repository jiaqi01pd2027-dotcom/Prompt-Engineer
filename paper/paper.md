# Same Model, Different Words: How Prompt Phrasing Changes What Claude Produces

**Tiger Zhang**
September 2026

## Abstract

The same language model gives a generic answer to one phrasing of a request and a usable one to another. This paper asks which phrasing choices matter, by how much, and whether the answer depends on the task or the model. We review the published literature and vendor guidance, then run a controlled experiment: twelve tasks across six domains (coding, writing, analysis, extraction, reasoning, and agentic planning), each written in ten prompt patterns that hold the underlying task fixed and vary only the wording, each run as a fresh subagent on three Claude models (Fable 5.1, Opus 5, Sonnet 5), for 360 runs. Outputs were scored by a blind judge on correctness, completeness, adherence, usefulness, and concision, plus objective checks where the task allowed them. RESULTS_ABSTRACT. The findings are packaged as a Claude Code skill that collects project context, grades a draft prompt out of 100, interviews the user in one batch, and produces three rewrites with the patterns named, and as a website with the pattern library, results, and a live grader.

## 1. Introduction

Prompt engineering is programming in natural language. The instruction "write something about our product" and the instruction "you are a senior B2B copywriter; write a two-sentence LinkedIn ad for ops managers at mid-sized companies, confident but not salesy, ending with a call to action" go to the same model, and the difference in the result comes entirely from the words. Most people write the first kind. Two things make that costly now. Models are used for actions, not only text: they edit repositories, call tools, and send messages, so a vague prompt produces a vague action. And the models have changed under the advice: instructions that fixed lazy behaviour in 2024 now cause over-triggering, and the chain-of-thought cue that unlocked arithmetic in 2022 mostly adds latency on models that reason on their own.

This project has three parts. The research part collects what is known, from 52 papers and the current documentation of Anthropic, OpenAI, and Google, and adds a controlled experiment on the Claude family. The product part is a Claude Code skill, `/prompt-engineer`, that turns the findings into a repeatable workflow: read the project, grade the draft, ask the few questions that change the rewrite, rewrite three ways, and explain which patterns were used. The website presents the pattern library, the experiment results with a blind rating page, and a grader that runs the rubric in the browser.

Our contribution is not a new technique. It is a ranking, with evidence, of the techniques people already use, on the models people use today, plus a tool that applies the ranking to the prompt in front of you using facts from the project it will run in. That last step, adapting the generic advice to a specific codebase or document, is where most of the gain comes from and where most guides stop.

## 2. What is known

### 2.1 The hierarchy: goal, role, context, action, format

Practitioner guides converge on the same skeleton. The Prompting Guide decomposes a prompt into instruction, context, input data, and output indicator. Google's whitepaper and the two teaching videos that motivated this project describe a hierarchy of goal, role, context, action, and output format. Anthropic's documentation says the same in a different order and adds a test: show the prompt to a colleague with no context, and if they would be confused, so is the model.

The empirical support for specificity is strong. Yang et al. (2025) found that models infer unstated requirements only 41% of the time and that under-specified prompts are twice as likely to regress when the model or the prompt changes. Bsharat et al. (2023) reported quality gains of roughly 50% across 26 principles, but a Wharton replication (Meincke et al. 2025) showed that the structural principles (state the audience, delimit the task, decompose steps, let the model ask) hold while the incentive principles (tips, threats, emotional appeals) do not replicate on 2025 models.

### 2.2 Role prompting

The role is the most-recommended and least-supported element. Zheng et al. (2023) tested 162 personas across four model families on 2,410 factual questions and found no accuracy gain over a no-persona control. A December 2025 Wharton report on six frontier models found no expert persona that consistently improved GPQA and nine significant degradations on MMLU-Pro. Where role prompting does help (Kong et al. 2023), the mechanism looks like an accidental reasoning trigger. The practical reading is that a role sets voice and taste, not knowledge; it belongs in writing tasks and not in factual ones.

### 2.3 Context and the why

Anthropic's documentation asks for the motivation behind each rule ("this is read aloud by text-to-speech, so no ellipses") on the grounds that Claude generalises from the reason. The limit on context is placement and relevance. Liu et al. (2023) showed a U-shaped attention curve: material in the middle of a long prompt is used least. Gloaguen et al. (2026) evaluated repository context files for coding agents and found that generic overviews do not lift success and raise cost by over 20%, while non-standard rules the agent could not infer do help. Context earns its place when it is a fact the model cannot get elsewhere.

### 2.4 Constraints and negatives

Explicit constraints improve adherence, but with two limits. IFEval (Zhou et al. 2023) showed that even GPT-4 missed roughly one prompt in four when constraints were verifiable, so stacking many constraints in one prompt lowers the chance any one is met. Negation is parsed unreliably (Truong et al. 2023), and Rana (2026) showed that naming a forbidden word primes it: 87.5% of violations in 40,000 samples were priming failures. Anthropic's guidance is to say what to do instead of what not to do, and to drop "CRITICAL" and "ALWAYS" because current models over-trigger on them. Our reading is that a constraint should name the failure mode it prevents ("do not ask them to retry; they already tried twice"), which gives the model a reason and a positive alternative at once.

### 2.5 Format and examples

Format is a large, under-controlled variable. Sclar et al. (2023) found accuracy spreads of up to 76 points from formatting alone; He et al. (2024) found up to 40% swings on smaller models between plain text, Markdown, JSON, and YAML. Few-shot examples teach format and label space more than content (Min et al. 2022), which is why two or three examples in the wanted voice are the most reliable way to control style. Examples hurt on RL-trained reasoning models (DeepSeek-R1 report) and on some large code models (Cheng and Mastropaolo 2026), and example order is a hidden hyperparameter (Lu et al. 2022).

### 2.6 Reasoning cues

"Let's think step by step" moved GSM8K from 10% to 41% on InstructGPT (Kojima et al. 2022). On models that reason internally the picture reversed. Sprague et al. (2024) found chain-of-thought gains concentrate on math and symbolic tasks; the Wharton Report 2 (Meincke et al. 2025) found reasoning models gain about 3% for 20 to 80% more latency and one model lost 13 points; Liu et al. (2024) found losses of up to 36 points on tasks where deliberation hurts humans too. Anthropic's current advice is to prefer "think thoroughly" over a hand-written step plan and to control depth with the effort parameter.

### 2.7 Asking before acting

The interview pattern, where the model asks clarifying questions before producing anything, has the strongest recent evidence for agents. ClarifyGPT (Mu et al. 2023) raised GPT-4 pass@1 by roughly ten points on code generation with one round of questions. Ambig-SWE (Vijayvargiya et al. 2025) found interaction improves performance by up to 74% on under-specified software tasks, and that the hard part is detecting ambiguity, not using the answer. Anthropic's own prompts gate the behaviour with a decision test: check in only when different readings would lead to materially different work.

### 2.8 Machine-written prompts

APE (Zhou et al. 2022), OPRO (Yang et al. 2023), Promptbreeder, DSPy, and TextGrad all show that when a metric exists, a model searching over wordings beats a human writing them. OPRO's "Take a deep breath and work on this problem step-by-step" scored 80% on GSM8K against 72% for the human phrase. The Prompt Report's case study found a DSPy-optimised prompt produced in minutes beat twenty hours of expert iteration. The implication for a prompt-improvement tool is that the tool should propose several rewrites and let the user or a check pick, rather than assert one.

### 2.9 How Anthropic phrases its own instructions

We read Claude Code's skills and Anthropic's published system prompts as a case study and catalogued 24 phrasing patterns. The recurring ones: describe the why, not just the rule; state the failure mode the rule prevents; attach behaviour to a recognisable trigger ("when X, do Y"); state the degree of freedom; give a default with an escape hatch; define done and demand evidence; name anti-patterns specifically; ration emphasis to one line; and assume the model is smart and cut what it already knows. These are the patterns the skill applies when it rewrites.

## 3. Method

### 3.1 Tasks

Twelve tasks, two per domain:

| Domain | Task | Ground truth |
|---|---|---|
| coding | code-1 parse ISO-8601 durations | 10 hidden test cases |
| coding | code-2 find two bugs, ignore a red herring | expected findings |
| writing | write-1 support reply to a failed export | rubric with five signals and word limit |
| writing | write-2 LinkedIn post on a 4-day week | fact sheet, length, banned openers |
| analysis | analysis-1 meeting transcript to decisions and actions | 5 decisions, 6 owners |
| analysis | analysis-2 compare three fictional tools | invented facts and pricing |
| extraction | extract-1 feedback lines to ticket titles | expected area labels, 60 chars |
| extraction | extract-2 messy receipts to JSON | exact expected array |
| reasoning | reason-1 discount, tax, and change | one number |
| reasoning | reason-2 five-slot scheduling puzzle | unique assignment |
| agentic | agent-1 plan a feature in a described codebase | right files, migration, tests, a risk |
| agent-2 | agent-2 scope a vague product brief | facts, non-goals, milestones, risks |

Each task has a hidden rubric the model under test never sees, and shared material (a complaint, a transcript, receipts) that is identical across variants.

### 3.2 Patterns

Ten variants per task. P0 is a bare command. P1 is a precise task statement and is the base for P2 to P7, which each add exactly one element: role, context, constraints with negatives, output format, few-shot examples, or a chain-of-thought cue. P8 combines role, goal, context, constraints, and format in the hierarchy order. P9 tells the model to ask clarifying questions and supplies the answers in the same prompt, simulating an interview.

### 3.3 Models and isolation

Each variant was run as a fresh Claude Code subagent on Fable 5.1, Opus 5, and Sonnet 5 with the variant text as its entire input. Subagents ran from an empty directory. A first batch was discarded when we found that subagents launched from the project folder could open the hidden rubrics; a contamination check on every saved output scans for rubric-only strings, and any hit is re-run.

### 3.4 Scoring

A separate judge agent receives, per task, the hidden rubric and all outputs with model and pattern labels removed and order shuffled, and scores each output from 0 to 10 on correctness, completeness, adherence, usefulness, and concision, plus pass or fail on the rubric's objective checks. The judge is told not to reward length. Human ratings are collected on the website's blind rating page and reported separately when available.

### 3.5 Limitations

One judge model scores outputs from its own family. One run per cell, so per-cell numbers carry noise and only pattern-level and domain-level aggregates should be read. The tasks are short; long-context effects are not measured. The interview pattern is simulated with pre-supplied answers, which measures the value of the answers rather than the model's ability to ask well.

## 4. Results

RESULTS_SECTION

## 5. From findings to a tool

### 5.1 The skill

`/prompt-engineer` runs in Claude Code. It reads the project before judging: CLAUDE.md, README, manifests, recent commits, and any file the draft names. It grades the draft with a seven-dimension rubric out of 100 and shows one line of evidence per dimension. It asks three to six questions in one batch, skipping any the project already answers, then gives three rewrites: minimal (the two highest-value fixes), structured (the full hierarchy with project facts substituted for generic nouns), and interview or agentic (ask-first for chat; plan, verify, and define done for Claude Code). It names the patterns applied and the ones deliberately left out, and ends with what would push the score higher.

### 5.2 Why project substitution is the hard part

Every guide says "add context". The gain comes from the specific context: the real test command, an existing test to imitate, the branch name, the rule in CLAUDE.md. A prompt that says "follow the style guide" is worse than one that says "match tests/test_dates.py". Generic advice cannot supply these; a tool running inside the project can. The skill's context step exists for this reason, and its rubric scores context by whether the facts are project-specific, not by whether a context section exists.

### 5.3 Website

The site carries the pattern library with evidence strength, the results tables and charts, a blind side-by-side rating page whose scores are stored and can be merged with the judge scores, a grader that applies the rubric to a pasted prompt, and the paper.

## 6. Conclusions

CONCLUSIONS_SECTION

## References

REFERENCES_SECTION
