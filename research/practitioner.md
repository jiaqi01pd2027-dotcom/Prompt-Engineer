# Practitioner Guides to Prompt Engineering: A Comparative Research Note

Date: 2026-09-10
Scope: six families of practitioner sources (Prompting Guide, OpenAI, Google, the Claude Code skills community, meta-prompting tools, and cross-model comparisons), read with WebFetch/WebSearch. Each source gets its own section; the final section is a technique-by-technique consensus/disagreement table.

---

## 1. Prompting Guide (promptingguide.ai, DAIR.AI)

### Introduction pages

**Settings.** Temperature and top-p both trade determinism for diversity; the guide's operational rule is to tune one or the other, not both, and likewise choose between frequency and presence penalty. Max length caps cost and rambling; stop sequences are a cheap structural control (e.g., emit "11" to cut a list at ten items). It notes that results vary across LLM versions, which foreshadows the "adapt to model updates" advice in Google's whitepaper.

**Basics and elements.** A prompt decomposes into four optional parts: instruction, context, input data, and output indicator. The basics page shows the smallest possible improvement, "The sky is" versus "Complete the sentence: The sky is", and introduces the Q:/A: pattern and the zero-shot/few-shot distinction, framing few-shot as in-context learning.

**Tips.** Five rules: start simple and iterate; lead with an action verb and separate the instruction with a delimiter such as `###`; be specific and descriptive; avoid imprecision ("use 2-3 sentences" beats "keep it short"); and say what to do rather than what not to do. The guide's example for the last rule replaces "DO NOT ask for interests" with an instruction to recommend from trending titles without asking preferences. The guide is explicit that this is "an iterative process that requires a lot of experimentation."

**Examples.** Seven task families (summarization, extraction, QA, classification, conversation, code, reasoning). Two notes matter for this project: classification shows that without explicit labels the model falls back on learned biases, and the reasoning section admits this is "one of the most difficult tasks" and that decomposition into steps is the main lever.

### Technique pages

| Technique | Core idea | Caveats the guide records |
|---|---|---|
| Zero-shot | Instruction-tuned/RLHF models do many tasks with no demos | Fall back to few-shot when it fails |
| Few-shot | Demonstrations condition format and label space | Min et al.: label space, input distribution, and format matter more than label correctness; few-shot alone fails on multi-step reasoning |
| Chain-of-thought | Intermediate reasoning steps; zero-shot CoT via "Let's think step by step"; Auto-CoT clusters questions and generates chains | Emergent only in sufficiently large models |
| Meta-prompting (Zhang et al.) | Structure-and-syntax-first prompts using abstracted examples | Assumes the model already knows the domain; weak on truly novel tasks |
| Self-consistency | Sample several CoT paths, take the majority answer | Cost multiplies with samples |
| Generated knowledge | Generate facts first, then answer | Answer confidence swings with which knowledge was generated |
| Prompt chaining | Split into sub-prompts whose outputs feed forward | Gains transparency, controllability, reliability; example is extract-quotes-then-answer, with quotes wrapped in XML |
| Tree of thoughts | Search over intermediate thoughts with lookahead/backtracking | Hulbert's single-prompt "three experts" version approximates it cheaply |
| ReAct | Interleave Thought/Action/Observation with tools | Beats CoT on FEVER, trails on HotpotQA; ReAct+CoT-SC hybrid is best |
| Reflexion | Actor, evaluator, self-reflection with episodic memory | Depends on the model's ability to self-evaluate; memory windows limit long tasks |
| APE | Model generates candidate instructions, scores them | Found "Let's work this out in a step by step way to be sure we have the right answer"; OPRO found "Take a deep breath" |

### Prompt Hub and agents/context engineering

The Prompt Hub is a test-suite-style library organized by capability (classification, coding, creativity, evaluation, extraction, math, QA, reasoning, summarization, truthfulness, adversarial prompting), not a how-to guide. The context-engineering page for agents reframes prompting as designing everything in the window: system prompt, task constraints, tool descriptions, memory, and error-handling patterns. Its five principles are eliminate ambiguity, make expectations explicit, build observability, iterate on observed behaviour, and balance flexibility against constraints. The example system prompt forces the agent either to run a search or to state why one is unnecessary, so tasks cannot be skipped silently.

**Assessment.** Prompting Guide is the broadest catalogue and the most research-cited, but it is descriptive rather than prescriptive: it rarely tells you which technique to reach for first. Its opinions on placement (instruction first, delimiter), positive framing, and iteration are shared by every vendor below.

---

## 2. OpenAI (GPT-4.1 guide, GPT-5 guide, prompt engineering page)

### GPT-4.1 prompting guide

The guide is built around agentic coding results. Three system-prompt "reminders" together lifted SWE-bench Verified by roughly 20 points:

1. **Persistence**: keep working "until the user's query is completely resolved, before ending your turn."
2. **Tool-calling**: if unsure about file contents or codebase structure, "use your tools to read files" rather than guess.
3. **Planning** (optional): "plan extensively before each function call, and reflect extensively" on the results.

Other findings: pass tools through the API `tools` field rather than pasting descriptions into the prompt (+2%); prompting-induced planning, i.e., making a non-reasoning model think out loud, added about 4%; and the SWE-bench prompt names under-testing as "the NUMBER ONE failure mode."

For long context, put instructions at both the start and the end; if only one, above the context beats below. Delimiter ranking from their experiments: Markdown headers first, XML close behind (good for nesting and metadata), JSON worst for document collections. GPT-4.1 follows instructions "more literally" than predecessors, so ambiguous or conflicting rules cause visible failures; later instructions win when rules conflict. Common failure modes: hallucinated tool calls when told to "always" use a tool, parroting sample phrases verbatim, and over-explaining. Their recommended skeleton: Role and Objective, Instructions (with sub-sections), Reasoning Steps, Output Format, Examples, Context.

### GPT-5 prompting guide

GPT-5 shifts the dial from "make it thorough" to "make it stop." Controls include `reasoning_effort`, explicit tool-call budgets ("maximum of 2 tool calls") with escape hatches, and early-stop criteria such as stop once "top hits converge (~70%)". Persistence text is kept for autonomy ("keep going until the user's query is completely resolved") and extended with "never stop or hand back to the user when you encounter uncertainty." Tool preambles (plan, narrate progress, summarise what was done versus planned) are recommended for user experience. A separate `verbosity` parameter controls answer length independently of reasoning, and can be overridden locally ("high verbosity for writing code").

The guide's strongest warning is about contradictions: because GPT-5 follows instructions with "surgical precision," conflicting rules waste reasoning tokens as the model tries to reconcile them. It gives a healthcare scheduling example where "always look up" collides with "do not look up in emergencies" until an explicit hierarchy is written.

The guide also documents a metaprompt for using GPT-5 to fix its own prompts:

> When asked to optimize prompts, give answers from your own perspective - explain what specific phrases could be added to, or deleted from, this prompt to more consistently elicit the desired behavior or prevent the undesired one. Here's a prompt: [PROMPT]. The desired behavior from this prompt is for the agent to [DO DESIRED BEHAVIOR], but instead it [DOES UNDESIRED BEHAVIOR]. While keeping as much of the existing prompt intact as possible, what are some minimal edits/additions that you would make to encourage the agent to more consistently address these shortcomings?

Markdown is off by default in the API; to enable it, say to use Markdown "only where semantically correct," and re-issue that instruction every few turns in long chats.

### OpenAI prompt engineering page (platform docs)

The general page codifies the message hierarchy (developer > user > assistant, "like a function and its arguments"), few-shot in the developer message, Markdown headers and XML tags as section boundaries, and a four-part skeleton: Identity, Instructions, Examples, Context. Its most useful framing is the split between model families: reasoning models want "high-level guidance" (a senior colleague who needs only goals) while GPT models need "very precise instructions" (a junior colleague).

### How OpenAI differs from Anthropic

- **Direction of the agentic nudge.** OpenAI's guides add persistence and "plan extensively" reminders to make models more autonomous. Anthropic's current best-practices page says the opposite for recent Claude models: dial back "CRITICAL: You MUST" language because they now overtrigger, and remove anti-laziness prompting when migrating. Anthropic's Opus 5 notes even say to delete self-verification instructions because the model over-verifies.
- **Instruction placement.** OpenAI: start and end for long context. Anthropic: static content first for caching, documents at the top with the query at the end; XML-wrapped documents. Google (Gemini 3): context first, then the instruction with an anchor phrase.
- **Delimiter preference.** OpenAI ranks Markdown first, XML second. Anthropic leads with XML tags. Google says either, but be consistent.
- **Prefill.** Anthropic's console improver historically added assistant prefills; Anthropic now says prefill is unsupported from Claude 4.6 onward and to use direct instructions or structured outputs instead. OpenAI never had the pattern.
- **Contradictions.** Both vendors now warn that literal-following models are damaged by conflicting rules; OpenAI frames it as wasted reasoning, Anthropic as ambiguity for a "brilliant but new employee."

---

## 3. Google (Gemini prompt design strategies, Gemini 3 guide, Boonstra whitepaper)

### Prompt design strategies (ai.google.dev)

Google's page is the most emphatic on examples: "We recommend to always include few-shot examples in your prompts." Use two to five, keep the format identical across examples, and avoid so many that the model overfits. The page also covers adding context (a router's manual rather than generic advice), input/output/example prefixes, breaking a task into components (sequential chaining, parallel fan-out and aggregate), parameter tuning (temperature, top-k/p, max tokens, stop sequences), and iteration strategies: rephrase, switch to an analogous task, reorder components. A distinctive tip: if a safety fallback fires, raise temperature. The "things to avoid" list is inconsistent example formatting, vague instructions, overfitting on examples, and omitting needed context.

### Gemini 3 developer guide

For Gemini 3 the advice changes tone: be precise and direct, keep prompts concise, and drop the scaffolding used to make Gemini 2.5 reason because Gemini 3 "may over-analyze" verbose prompts. Use `thinking_level` rather than prompt tricks. Choose XML or Markdown and stick with one. Put behavioural constraints at the system level or at the start of the prompt; for large data, put the question after the data and bridge with "Based on the information above." Keep temperature at the default 1.0; lowering it can cause looping on reasoning tasks. Default verbosity is low, so ask explicitly for conversational tone. Philipp Schmid's companion post adds a persistence line for agents, "Continue working until the user's query is COMPLETELY resolved," and a self-check question about intent versus literal words, while cautioning that "there is no 'perfect' template."

### Boonstra whitepaper (Google/Kaggle, 2024)

**Technique list (12):** general/zero-shot; one-shot and few-shot; system prompting; contextual prompting; role prompting; step-back prompting; chain of thought; self-consistency; tree of thoughts; ReAct; automatic prompt engineering; code prompting.

**Best-practices section:**

1. Provide examples ("a powerful teaching tool").
2. Design with simplicity: concise and clear "for both you and the model."
3. Be specific about the output.
4. Use instructions over constraints; positive instructions beat lists of prohibitions.
5. Control max token length, in config or in the prompt.
6. Use variables in prompts so they can be reused.
7. Experiment with input formats and writing styles (question vs statement vs instruction).
8. For few-shot classification, mix up the classes so order is not learned.
9. Adapt to model updates.
10. Experiment with output formats; use JSON/XML for extraction, ranking, classification.
11. JSON repair and schemas: structured outputs can be truncated; validate and repair.
12. Experiment together with other prompt engineers; variance between attempts is expected.
13. CoT best practices: put the answer after the reasoning; temperature 0 for reasoning.
14. Document the various prompt attempts.

The documentation template (Table 21) records name/version, goal, model, temperature, token limit, top-k, top-p, prompt, output, plus status (OK / NOT OK / SOMETIMES OK) and feedback. Recommended starting settings: temperature 0.2 / top-k 30 / top-p 0.95 for general use; 0.9/40/0.99 for creative; 0.1/20/0.9 for conservative; 0 for math, code, and CoT. Note the tension with the Gemini 3 guide, which now says leave temperature at 1.0: the whitepaper predates thinking models.

---

## 4. Claude Code community skills

Skills are folders with a `SKILL.md` whose YAML frontmatter carries `name` and `description`; the description is what Claude scans (~100 tokens) to decide whether to load the full instructions (<5k tokens), with reference files loaded only on demand. This progressive-disclosure design means the description doubles as a trigger rubric, and most authors write it as "Use when the user says X, Y, Z."

### Humanizer (blader/humanizer; also matsuikentaro1/humanizer_academic)

The most-starred single skill. Frontmatter description: an agent skill that removes signs of AI-generated writing. Body organized as 25 patterns in five groups (staging instead of stating; rhythm by rule; inflation and borrowed authority; formatting by rule; leftovers from chat and draft), each with a before/after pair. Workflow: identify the strongest markers first, redraft without preserving the original structure, critique the draft, produce the final. A hard rule: it does not invent facts. Invoked as `/humanizer` or in plain language; installable via `npx skills add`. Structurally it is a rubric-driven editing skill: the pattern list is the rubric, the before/after pairs are the few-shot examples.

### Prompt-improvement skills

- **severity1/claude-code-prompt-improver.** Two layers: hooks (`UserPromptSubmit`, `PreToolUse`, `SubagentStart`) run a ~189-token evaluation that self-grades prompt clarity; only vague prompts load the skill. The skill runs Research (Glob/Grep/web via cheaper Explore agents) → Questions (1-6, grounded in what the research found) → Clarify → Execute. Prefix escapes (`*` skips checks). Its before/after story is turn count: "fix the bug" goes from three rounds of back-and-forth to one AskUserQuestion with concrete options.
- **christabone/claude-prompt-improvement.** A `SKILL.md`, a 10-point `CHECKLIST.md` (XML tags, variables, role, examples, CoT, clarity, output format, constraints, context, decomposition), a condensed techniques reference, and Python pattern detectors. Output is the rewritten prompt plus a change log. Example: a vague code-review request becomes role + criteria + XML-tagged code + output format. It also ships a fetcher that hashes Anthropic's docs to detect guidance changes.
- **wagnersza/prompt-improver.** The "AI Question Method": rewrite prompts to treat the model as a senior partner, with "flashlight intent," multiple open reconciliation questions instead of one closed task, and named artifacts plus an explicit thesis the model is invited to dispute. Diagnosis dimensions: senior-partner framing, flashlight intent, synthesis surface, data anchors, model fit, failure modes. Output: diagnosis, improved prompt, model settings. Model-specific tuning notes (remove self-verification for Opus 5; expect literal reading on Sonnet 5).
- **ndpvt-web/prompt-improver.** Clarify with repeated `AskUserQuestion` until ambiguity is gone; confirmed answers become "axioms"; the rewritten prompt carries reasoning directives and a verification step tracing each decision to an axiom. "quick improve" skips questions and labels guesses ASSUMED. Example: "read sales data and send a weekly report" gains confirmed data format, delivery channel, and audience.
- **nidhinjs/prompt-master.** Explicitly position-aware: a primacy zone (identity, hard rule "confirm the target tool first"), a middle zone (nine-dimension intent extraction table, per-tool routing for 20+ targets, diagnostic checklist), and a recency zone (verification questions: constraints in the first 30%? strongest signal word used? token audit passed?). Before/after: "Write a summary" → "Generate a 150-word executive summary in bullet format with key metrics."
- **Jeffallan/claude-skills prompt-engineer.** Description: writes, refactors, and evaluates prompts, generating templates, schemas, rubrics, and test suites. Five-step workflow with an 80%-accuracy checkpoint before iterating, "change one variable at a time," and deliverables that include test cases, settings, and limitations.
- **46ki75 prompt-evaluation-claude-code.** Runs an eval loop using Claude Code subagents as graders, no external harness.

### Common structure across skills

1. Frontmatter description doubling as trigger criteria.
2. A workflow of numbered phases, nearly always beginning with clarify/interview or research.
3. A rubric or checklist (10 techniques, 9 dimensions, 25 patterns).
4. Before/after pairs as few-shot demonstrations.
5. A fixed output contract (rewritten prompt + rationale, or three blocks).
6. Increasingly, model-specific tuning tables, reflecting the vendor guidance that recent models overtrigger on aggressive language.

The obra/superpowers collection (`/brainstorm`, `/write-plan`, `/execute-plan`) shows the same shape applied to workflow scaffolding rather than prompt rewriting.

---

## 5. Meta-prompting tools and templates

### Anthropic prompt improver (Console) and metaprompt notebook

The Console improver runs five transformations: add a chain-of-thought section, standardize examples into XML, enrich examples with reasoning that matches the new structure, rewrite for structure and grammar, and add an assistant prefill. Reported results: +30% accuracy on a multilabel classification test, 100% word-count adherence on a summarization task. The workbench also generates synthetic examples and scores against "ideal outputs" on a five-point scale. The older metaprompt notebook (claude-cookbooks/misc/metaprompt.ipynb) is a long multishot prompt containing half a dozen exemplar prompts; the user supplies a task and optional variable names and gets a first-draft template. Anthropic's overview page sets prerequisites before any of this: success criteria, an empirical test, and a first draft.

### OpenAI prompt generator (Playground "Generate")

The published meta-prompt opens: "Given a task description or existing prompt, produce a detailed system prompt to guide a language model in completing the task effectively." Its guideline headings are Understand the Task, Minimal Changes, Reasoning Before Conclusions, Examples, Clarity and Conciseness, Formatting, Preserve User Content, Constants, Output Format. The required output is a one-line task instruction, optional details, then Steps, Output Format, Examples (1-3, with placeholders), and Notes. A separate edit meta-prompt prepends a `<reasoning>` block that grades the existing prompt on simplicity, reasoning order, structure, example quality, complexity, and specificity before editing.

### Widely shared community templates

1. **Prompt Creator / interview loop** (Medium, SHRM, many reposts):
   > I want you to become my Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. ... You will generate: a) Revised prompt, b) Suggestions, c) Questions ... We will continue this iterative process ... until it's complete.
   Variants add a 1-10 rating and end with "ask me what the prompt should be about."

2. **Five-minute rewrite** (Towards Data Science):
   > Act as an expert Prompt Engineer. I'll give you a messy prompt. Reason step by step to improve it. Write the final prompt as an elegant template with clear sections. Use lists, placeholders, and examples.
   The code variant adds a required `###Improved Prompt###` marker for parsing.

3. **Gap-analysis improver** (PromptHub / IntuitionLabs pattern): instruct the model to (1) identify the intended task, (2) list what is clearly specified, (3) list what is ambiguous or missing, (4) identify missing constraints, (5) rewrite with gaps addressed.

4. **OpenAI's GPT-5 minimal-edit metaprompt** (quoted in full in section 2).

5. **Meta-Expert conductor** (Stanford/OpenAI meta-prompting paper, reproduced by PromptHub): "You are Meta-Expert, an extremely clever expert with the unique ability to collaborate with multiple experts..." The conductor decomposes the task, drafts expert sub-prompts, and integrates answers.

Also in circulation: the "prompt enhancer" pattern (auto-expand a terse request with context, examples, and format before sending; scooter-lacroix/claude-code-prompt-enhancer and Hashaam101/prompt-optimizer implement it as always-on), and the research lineage (APE, OPRO, LCP, PromptAgent, DSPy, TextGrad) that PromptHub catalogues.

**Observation.** All five templates share the same move: role assignment + explicit reasoning + a fixed output contract. They differ on whether to interview the user first (Prompt Creator, severity1, ndpvt-web) or to rewrite immediately with placeholders (TDS, OpenAI generator). The interview pattern is the community's answer to the vendors' "eliminate ambiguity" advice.

---

## 6. Other-model perspective: how each vendor describes a good prompt

Vendor documents, read directly:

- **Anthropic (Claude).** Clear and explicit; the "brilliant but new employee" framing and the "show it to a colleague" test. Add the motivation behind instructions. Examples: 3-5, relevant, diverse, wrapped in `<example>` tags. XML tags for anything mixing instructions, context, and input. A one-sentence role in the system prompt "makes a difference." Tell Claude what to do, not what not to do. Recent models are more proactive: remove "CRITICAL: You MUST" phrasing, remove self-verification for Opus 5, and note that Opus 4.5 with thinking off is sensitive to the word "think." Explicit chaining is "still useful" for inspecting intermediates, with self-correction (draft → review → refine) as the common pattern. Prefill is deprecated from 4.6.
- **OpenAI (GPT).** Precise, literal instructions with an explicit hierarchy; Markdown headers first, XML second; instructions at start and end of long contexts; persistence and planning reminders for agents; reasoning models want goals, GPT models want steps; contradictory rules are the main failure source.
- **Google (Gemini).** Always include few-shot examples with consistent formatting (strategies page); for Gemini 3, be concise and direct, keep temperature at 1.0, use `thinking_level` instead of reasoning scaffolds, context before question with an anchor phrase, constraints at the top.

Third-party comparisons (joanmedia.dev, dataunboxed, promptessor, promptbuilder, geekflare) converge on a shorthand: Claude rewards XML and detailed, explicit prompts and follows long instruction lists most faithfully; GPT-4.1/GPT-5 are the most literal and steerable, with later instructions overriding earlier ones; Gemini 3 is literal and terse by default and wants grounding context. These posts are secondary and partly marketing; the claim that a format can swing results "30%" between models is unsourced. Where they cite vendor pages the claims match what I read above. One caution: several posts still recommend "think step by step" scaffolding, which all three vendors now say is unnecessary or harmful on thinking-enabled models.

When users ask the chatbots themselves what makes a good prompt, published transcripts (geekflare, techpoint, tomsguide) show each model reciting the same five items (goal, context, constraints, format, examples); the differentiation lives in the vendor docs, not in the models' self-descriptions.

---

## 7. Consensus vs disagreement

Legend: PG = Prompting Guide; OA = OpenAI; GG = Google; AN = Anthropic docs; CC = Claude Code skills community; MP = meta-prompting tools.

| Technique | Endorsed by | Caveats | Model-specific notes |
|---|---|---|---|
| Role / persona | PG (conversation examples), GG (role prompting), AN (one sentence in system prompt), OA (Identity/Role section), CC (checklists), MP (every template opens with a role) | OA and GG treat it as one section among several, not a multiplier; wagnersza reframes it as "senior partner" rather than "expert" | AN: role in system prompt; OA: developer message |
| Context / background | All six | GG: give the actual reference material, not generic; AN: also give the *motivation* behind rules | Gemini 3 and AN: context before the question; OA: instructions at both ends |
| Constraints (explicit, specific) | All six | OA/GPT-5 and AN warn that conflicting constraints are the top failure; nidhinjs: put critical constraints in the first 30% | GPT: later rule wins on conflict; Gemini 3: constraints at system level or top |
| Negatives ("do not") | Discouraged by PG, GG whitepaper, AN ("tell what to do instead"); tolerated by OA as guardrails | Positive phrasing plus an alternative is the consensus; negative-only lists get parroted or ignored | AN: models still respect "do not include" lists reliably; GPT-4.1: "always/never" tool rules cause hallucinated calls |
| Output format specification | All six | GG: JSON/XML for extraction; handle truncation/repair; OA: JSON is a poor *input* delimiter | AN: XML format indicators; GPT-5: Markdown off by default, must be enabled; Gemini 3: low verbosity default |
| Few-shot examples | PG, GG (strongest: "always include"), AN (3-5, diverse, tagged), OA, CC, MP (improver enriches examples) | PG: format and label space matter more than correctness; few-shot alone fails on reasoning; GG/AN: too many or too uniform examples overfit; GPT-4.1: sample phrases get copied verbatim | AN: `<example>` tags; GG: mix class order |
| Chain-of-thought | PG (core), GG whitepaper (answer after reasoning, temp 0), OA (prompting-induced planning, +4%), AN (manual CoT as fallback), MP (improver adds a CoT section) | Vendors now agree explicit CoT is unnecessary on thinking models: GPT-5 uses `reasoning_effort`, Gemini 3 `thinking_level`, Claude adaptive thinking; Gemini 3 "may over-analyze" verbose scaffolds | AN: avoid the word "think" on Opus 4.5 with thinking off; Opus 5 over-verifies if asked to check |
| Interview / clarify first | CC (severity1, ndpvt-web, Prompt Creator template), PG context-engineering ("eliminate ambiguity") | OA GPT-5 persistence prompts say the opposite for agents: deduce rather than ask; balance depends on cost of a wrong guess | Claude Code: AskUserQuestion; hooks can gate on a clarity score |
| Prompt chaining / decomposition | PG, GG (sequential and parallel), OA (split tasks), AN ("still useful" for inspection), CC (task decomposition checklist item) | AN: recent models chain internally; explicit chaining is for observability and pipeline control | AN: self-correction chain (draft → review → refine) |
| Self-critique / reflection | PG (Reflexion, self-consistency), AN (self-check line for coding/math), GG (Schmid's intent check), MP (OpenAI edit meta-prompt reasons first) | Reflexion depends on accurate self-evaluation; Opus 5 should *not* be told to verify; self-consistency multiplies cost | GPT-5: minimal-reasoning mode benefits from a brief summary before answering |
| Meta-prompting (prompts that write prompts) | PG (APE, meta-prompting page), OA (generator, GPT-5 metaprompt), AN (console improver, metaprompt notebook), MP, CC | PG: structure-first meta-prompts assume domain knowledge; OA: "minimal changes" principle; AN: needs success criteria and evals first or you cannot tell if it helped | AN improver adds XML + CoT + (formerly) prefill; OA generator emits Markdown sections |
| Templating / variables | GG whitepaper (variables), AN (variable inputs in XML tags, metaprompt variable names), OA (placeholders in examples), CC (christabone variable detector), PG (implicit in Prompt Hub) | Keep static content first for caching (AN); document versions (GG Table 21) | none beyond placement |
| System prompts | All six | OA: developer message is prioritised over user; AN: role and behavioural rules live there; Gemini 3: behavioural constraints at system level | GPT-5: re-issue formatting rules every 3-5 turns; AN: prefill deprecated, use system instruction |
| Voice dictation | Not addressed by any source read | No practitioner guide covered dictated prompts; the closest is Anthropic's colleague test and severity1's "type vibes" premise, which imply terse spoken input needs an improver or interview step | Treat as an open gap for this project |

### Where the sources genuinely disagree

1. **How hard to push agents.** OpenAI (both guides) and Schmid for Gemini add persistence and planning reminders; Anthropic tells you to remove them for Claude 4.5+ and to lower `effort` if the model over-explores. This is a real model-generation split, not a style difference.
2. **Delimiters.** OpenAI: Markdown > XML > JSON. Anthropic: XML. Google: either, consistently. Third-party posts inflate this into large performance gaps without evidence.
3. **Temperature.** Boonstra: 0 for reasoning. Gemini 3 guide: leave at 1.0 or risk loops. The whitepaper is pre-thinking-model advice.
4. **Ask vs act.** Community skills interview the user; GPT-5 guidance for agents is to resolve ambiguity by deduction. Both are right for their setting (interactive chat vs autonomous run).
5. **Prefill.** Recommended by the 2024 Anthropic improver, removed from Claude 4.6 onward.

### Where everyone agrees

Clear, specific, positively phrased instructions; examples in a consistent format; explicit output format; context before question; separate sections with visible delimiters; iterate empirically and document attempts; and, for anything beyond a chat, define success criteria before you optimise the prompt.

---

## Sources

Prompting Guide
- https://www.promptingguide.ai/introduction/settings
- https://www.promptingguide.ai/introduction/basics
- https://www.promptingguide.ai/introduction/elements
- https://www.promptingguide.ai/introduction/tips
- https://www.promptingguide.ai/introduction/examples
- https://www.promptingguide.ai/techniques/zeroshot
- https://www.promptingguide.ai/techniques/fewshot
- https://www.promptingguide.ai/techniques/cot
- https://www.promptingguide.ai/techniques/meta-prompting
- https://www.promptingguide.ai/techniques/consistency
- https://www.promptingguide.ai/techniques/knowledge
- https://www.promptingguide.ai/techniques/prompt_chaining
- https://www.promptingguide.ai/techniques/tot
- https://www.promptingguide.ai/techniques/react
- https://www.promptingguide.ai/techniques/reflexion
- https://www.promptingguide.ai/techniques/ape
- https://www.promptingguide.ai/prompts
- https://www.promptingguide.ai/agents/context-engineering

OpenAI
- https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
- https://developers.openai.com/api/docs/guides/prompt-engineering
- https://developers.openai.com/api/docs/guides/prompt-generation

Google
- https://ai.google.dev/gemini-api/docs/prompting-strategies
- https://ai.google.dev/gemini-api/docs/gemini-3
- https://www.philschmid.de/gemini-3-prompt-practices
- https://archive.org/stream/whitepaper-prompt-engineering-v-4/whitepaper_Prompt%20Engineering_v4_djvu.txt (Boonstra whitepaper full text; Kaggle page https://www.kaggle.com/whitepaper-prompt-engineering returned only a title)

Anthropic
- https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/overview
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- https://claude.com/blog/prompt-improver
- https://github.com/anthropics/claude-cookbooks/blob/main/misc/metaprompt.ipynb (via search)

Claude Code community
- https://github.com/blader/humanizer
- https://github.com/severity1/claude-code-prompt-improver
- https://github.com/christabone/claude-prompt-improvement
- https://github.com/wagnersza/prompt-improver
- https://github.com/ndpvt-web/prompt-improver
- https://github.com/nidhinjs/prompt-master/blob/main/SKILL.md
- https://github.com/Jeffallan/claude-skills/blob/main/skills/prompt-engineer/SKILL.md
- https://github.com/travisvn/awesome-claude-skills
- https://github.com/46ki75/skills/blob/main/skills/prompt-evaluation-claude-code/SKILL.md (via search)

Meta-prompting and comparisons
- https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting
- https://towardsdatascience.com/how-to-improve-any-prompt-in-less-than-5-minutes-chat-ui-and-code-8a819e2fa2ba/
- https://medium.com/@mcraddock/the-art-of-prompt-crafting-3fe057b8b566 (Prompt Creator template, via search)
- https://www.joanmedia.dev/ai-blog/model-specific-prompting-how-claude-gpt-and-gemini-differ
- https://promptessor.com/blog/how-to-write-prompts-for-chatgpt-claude-gemini-and-grok-in-2026
- https://www.dataunboxed.io/blog/prompt-engineering-best-practices-complete-comparison-matrix (404 at fetch time; summary via search snippet only)
- https://geekflare.com/guides/chatgpt-vs-claude-vs-gemini-comparison/ (via search)
