# Anthropic's Official Prompting Guidance: Research Note

Compiled 2026-09-10 from Anthropic's platform docs (platform.claude.com), Claude Code docs (code.claude.com), and the Anthropic engineering blog. All quotations are verbatim from the pages listed under Sources. Quotes are kept short (under 15 words) and attributed by section.

## 0. A note on document structure (important for citation)

The per-technique pages that used to live under `/docs/build-with-claude/prompt-engineering/` (be-clear-and-direct, multishot-prompting, chain-of-thought, use-xml-tags, system-prompts, prefill-claudes-response, chain-prompts, long-context-tips, extended-thinking-tips, claude-4-best-practices, prompt-generator, prompt-improver, prompt-templates-and-variables) **all now 301-redirect to one consolidated page**: "Prompting best practices" (`.../claude-prompting-best-practices`). The overview page calls it "the living reference; start there." The overview itself is now a short gate page whose only substantive content is a set of preconditions: "A clear definition of the success criteria," "Some ways to empirically test against those criteria," and "A first draft prompt you want to improve."

The prompt generator and improver no longer have doc pages; the overview links a "Prompt generator notebook" (the Colab metaprompt recipe) with the text "Don't have a first draft prompt? Generate one with the metaprompt recipe." Templates-and-variables content survives only as `{{VARIABLE}}` placeholders in the long-context examples.

The consolidated page is organized in three parts: "Model-specific guidance," "Techniques for all current models," and "Migration considerations." It carries an explicit epistemic caveat: "Where a technique names a specific model, treat it as measured on that model."

---

## 1. Core techniques (from "Prompting best practices")

### 1.1 Be clear and direct

- **Recommended phrasing.** "Claude responds well to clear, explicit instructions." The governing metaphor: "Think of Claude as a brilliant but new employee who lacks context." Payoff claim: "The more precisely you explain what you want, the better the result."
- **Golden rule (heuristic test).** "Show your prompt to a colleague with minimal context on the task." Then: "If they'd be confused, Claude will be too."
- **Concrete tactics.** "Be specific about the desired output format and constraints." Use "numbered lists or bullet points when the order or completeness of steps matters."
- **Canonical example.** Less effective: "Create an analytics dashboard." More effective adds: "Go beyond the basics to create a fully-featured implementation."
- **When it helps.** Any time you want "above and beyond" behavior; the doc says to "explicitly request it rather than relying on the model to infer this."
- **When it hurts / caveat.** The Claude Code guide adds a counterpoint: "Vague prompts can be useful when you're exploring and can afford to course-correct." Example: "what would you improve in this file?"

### 1.2 Add context / explain the why

- **Recommended phrasing.** "Providing context or motivation behind your instructions... can help Claude better understand your goals."
- **Canonical example.** Less effective: "NEVER use ellipses." More effective: "Your response will be read aloud by a text-to-speech engine, so never use ellipses."
- **Claude-specific claim.** "Claude is smart enough to generalize from the explanation." This is the doc's stated reason to prefer rationale over bare prohibitions.

### 1.3 Avoid over-prescriptive / aggressive language (ALWAYS, NEVER, CRITICAL)

This is one of the strongest Claude-specific claims in the current docs and appears in several places:

- Tool-use section: newer models "are also more responsive to the system prompt than previous models." Consequence: prompts written to fix undertriggering "may now overtrigger." Fix: "dial back any aggressive language." The doc's own before/after: "CRITICAL: You MUST use this tool when..." should become "Use this tool when...".
- Overthinking section: "Remove over-prompting." And: "Instructions like 'If in doubt, use [tool]' will cause overtriggering." Preferred replacement: "Use [tool] when it would enhance your understanding of the problem."
- Migration list, item 6: "Tune anti-laziness prompting... dial back that guidance."
- Claude Code CLAUDE.md guidance: "If you emphasize many lines, none of them stands out." Only add "IMPORTANT" to "that line alone" when one instruction keeps being skipped.
- Skills best-practices page, however, permits escalation as a last resort when observed behavior demands it: "using stronger language such as 'MUST filter' instead of 'always filter'."

**Interpretation for the paper:** Anthropic frames emphatic modifiers as a scarce resource whose value decays with use, and as a generation-specific liability (calibrated for older, lazier models).

### 1.4 Tell Claude what to do, not what not to do

- Format-control section, item 1: "Tell Claude what to do instead of what not to do." Instead of "Do not use markdown in your response," try "Your response should be composed of smoothly flowing prose paragraphs."
- Related: "Match your prompt style to the desired output," with the claim that "removing markdown from your prompt can reduce the volume of markdown in the output."

### 1.5 Use examples (multishot / few-shot)

- **Claim.** "Examples are one of the most reliable ways to steer Claude's output format, tone, and structure."
- **Three properties.** "Relevant: Mirror your actual use case closely." "Diverse: Cover edge cases and vary enough." "Structured: Wrap examples in `<example>` tags."
- **Quantity.** "Include 3–5 examples for best results."
- **Meta-tip.** "ask Claude to evaluate your examples for relevance and diversity."
- **When it hurts.** The "diverse" bullet warns examples can cause Claude to "pick up unintended patterns." The context-engineering blog is more pointed: avoid "a laundry list of edge cases" and instead "curate a set of diverse, canonical examples." Its slogan: "examples are the 'pictures' worth a thousand words."
- **With thinking.** "Multishot examples work with thinking." Put `<thinking>` tags inside examples and "It will generalize that style."
- **Model-specific.** The Fable 5.1 page recommends fixing unmarked quotation of sources by adding "one complete example of a correct response" plus a `<rationale>` explaining why it is correct.

### 1.6 XML tags

- **Claim.** "XML tags help Claude parse complex prompts unambiguously." Wrapping each content type "reduces misinterpretation."
- **Practices.** "Use consistent, descriptive tag names across your prompts." "Nest tags when content has a natural hierarchy."
- **Named tags in the docs.** `<instructions>`, `<context>`, `<input>`, `<example>`/`<examples>`, `<documents>`/`<document index="n">`/`<source>`/`<document_content>`, `<quotes>`, `<thinking>`/`<answer>`. Anthropic's own sample system-prompt blocks are XML-wrapped: `<default_to_action>`, `<use_parallel_tool_calls>`, `<investigate_before_answering>`, `<frontend_aesthetics>`, `<avoid_excessive_markdown_and_bullet_points>`.
- **Format control.** "Use XML format indicators," e.g., writing prose "in `<smoothly_flowing_prose_paragraphs>` tags."
- **Context-engineering blog.** Recommends "XML tagging or Markdown headers to delineate these sections."

### 1.7 Role prompting / system prompts

- **Claim.** "Setting a role in the system prompt focuses Claude's behavior and tone." "Even a single sentence makes a difference." Example: "You are a helpful coding assistant specializing in Python."
- **Model identity.** Sample: "The assistant is Claude, created by Anthropic."
- **Right altitude (blog).** System prompts should be "specific enough to guide behavior effectively, yet flexible enough." Two failure modes: "brittle if-else hardcoded prompts" vs prompts "overly general or falsely assume shared context." Target "the minimal set of information that fully outlines your expected behavior." Method: start minimal on the best model, then add instructions "based on actual failure modes."

### 1.8 Chain of thought / thinking

Current models mostly replace manual CoT with API-level thinking:

- **Adaptive thinking.** "Claude dynamically decides when and how much to think." Calibrated by "the `effort` parameter and query complexity." Claim: "adaptive thinking reliably drives better performance than extended thinking."
- **Prefer general instructions.** "A prompt like 'think thoroughly' often produces better reasoning than a hand-written step-by-step plan." Reason: "Claude's reasoning frequently exceeds what a human would prescribe."
- **Manual CoT as fallback.** "When thinking is off, you can still encourage step-by-step reasoning." Use "`<thinking>` and `<answer>`" tags. Caveat on Opus 5 with thinking disabled: it "can occasionally emit internal XML tags into its visible output."
- **Guiding interleaved thinking.** Sample: "After receiving tool results, carefully reflect on their quality."
- **Suppressing thinking.** Sample: "Thinking adds latency and should only be used when it will meaningfully improve answer quality."
- **Overthinking.** Sample: "choose an approach and commit to it." "Avoid revisiting decisions unless you encounter new information."
- **Self-check.** "Before you finish, verify your answer against [test criteria]." Exception: on Opus 5 "verification instructions... can cause over-verification"; the doc says to "remove these instructions rather than rewriting them."
- **Word sensitivity.** With thinking disabled, Opus 4.5 "is particularly sensitive to the word 'think'"; use "consider," "evaluate," or "reason through."
- **"Think hard" levels.** The old Claude Code tiers (think / think hard / think harder / ultrathink) are gone. Current Claude Code docs: "Claude Code recognizes the keyword" `ultrathink` and "adds an in-context instruction," but "think", "think hard", and "think more" are passed "through as ordinary prompt text." Depth is now controlled by `effort` (`low`/`medium`/`high`/`xhigh`/`max`), and "The effort scale is calibrated per model."
- **`budget_tokens` deprecated.** "On Claude 4.7 and later models, setting `budget_tokens` returns a 400 error."

### 1.9 Prefill

- **Status.** "Prefilled responses... on the last assistant turn are no longer supported" from Claude 4.6 on; requests "return a 400 error." Rationale: "most use cases of prefill no longer require it."
- **Migration by use case.** Formatting: use Structured Outputs; "Try asking the model to conform to your output structure first." Preambles: "Respond directly without preamble." Refusals: "Claude is much better at appropriate refusals now." Continuations: move to the user turn, "Continue from where you left off." Context hydration: "inject... reminders into the user turn" or use compaction.
- **Prefill vs extended thinking.** The current docs no longer discuss prefill interacting with thinking because prefill itself is unsupported on thinking-era models; the relevant constraint is now the append-only history rule (see 1.13).

### 1.10 Chain complex prompts

- "Explicit prompt chaining... is still useful when you need to inspect intermediate outputs or enforce a specific pipeline." Claim: "Claude handles most multistep reasoning internally."
- "The most common chaining pattern is self-correction: generate a draft → have Claude review it... → refine."
- Blog ("Building effective agents") names prompt chaining as the first of five patterns and advises "finding the simplest solution possible, and only increasing complexity when needed."

### 1.11 Long context

- **Ordering.** "Put longform data at the top." Claim: "Queries at the end can improve response quality by up to 30 percent."
- **Structure.** Wrap each document in `<document>` with `<document_content>` and `<source>` subtags.
- **Grounding.** "ask Claude to quote relevant parts of the documents first." Rationale: "helps Claude focus on the relevant content and ignore the rest."

### 1.12 Parallel tool calls

- **Claim.** "Claude's latest models run independent tool calls in parallel." Prompting "can boost this to ~100%."
- **Sample block** `<use_parallel_tool_calls>`: "make all of the independent tool calls in parallel"; "Never use placeholders or guess missing parameters."
- **Reverse steer.** "Execute operations sequentially with brief pauses between each step."
- **Fable 5.1 nuance.** In coding/computer-use loops it "may issue them one per turn." Fix: a one-sentence turn-scoped system message, "First privately list what you need next; then request every item..."; "send the parallel-calls instruction as a turn-scoped system message after each round."

### 1.13 Append-only history / thinking blocks

- "Pass thinking blocks back unchanged and keep history append-only." Editing earlier turns "invalidates every later thinking block." Move per-turn reminders to "turn-scoped system messages." Same edits "restart the prompt cache."

### 1.14 Agentic-action calibration

- **Tool triggering.** "If you say 'can you suggest some changes,' Claude will sometimes provide suggestions rather than implementing them." Say instead "Change this function to improve its performance."
- **Two opposite dials.** `<default_to_action>` ("implement changes rather than only suggesting them") vs `<do_not_act_before_instructions>` ("Do not jump into implementation").
- **Asking clarifying questions.** The docs treat clarification as a tunable trade-off, not a virtue. Fable 5.1 autonomous prompt: "asking 'Want me to…?' or 'Shall I…?' will block the work"; "Stop only for destructive actions or genuine scope changes." Scope prompt: "check in only when different readings would lead to materially different work." Warning: the block "can also make the model less likely to ask about ambiguous requests." Claude Code, by contrast, recommends deliberately eliciting questions at spec time: "Interview me in detail using the AskUserQuestion tool" and "dig into the hard parts I might not have considered."
- **Safety.** Sample: "Consider the reversibility and potential impact of your actions." "do not use destructive actions as a shortcut."
- **Over-engineering.** "The right amount of complexity is the minimum needed for the current task." Fable 5.1: unrequested extras and committed test code "drop substantially with no measurable change in task success" under an explicit leave-out instruction.
- **Hallucination.** `<investigate_before_answering>`: "Never speculate about code you have not opened."
- **Test gaming.** "Tests are there to verify correctness, not to define the solution."
- **Subagents.** Opus 4.6 "has a strong predilection for subagents"; damping sample: "For simple tasks... work directly rather than delegating."
- **Long-horizon.** "do not stop tasks early due to token budget concerns." State prompts: "Review progress.txt, tests.json, and the git logs." Fable 5.1 finish-the-task prompt: "The user is not watching in real time," and "If it is a plan... do that work now with tool calls."

### 1.15 Format and verbosity

- Latest models are "More direct and grounded," "Less verbose," may "skip verbal summaries after tool calls." Ask explicitly: "provide a quick summary of the work you've done."
- Anti-formatting blocks are now generation-sensitive: on Fable 5.1 "a block like this can suppress structure the content needs." Replacement rule: "Use lists and bullet points when asked to, or when the content is multifaceted."
- Writing density fix: "Please remove all mannered prose."

---

## 2. Claude Code best practices (code.claude.com/docs/en/best-practices)

The engineering-blog URL now redirects here. Its organizing constraint: "Claude's context window fills up fast, and performance degrades as it fills."

- **Verification first.** "Give Claude a check it can run: tests, a build, a screenshot." "Have Claude show evidence rather than asserting success."
- **Explore, plan, code, commit.** "Separate research and planning from implementation." Skip planning when "you could describe the diff in one sentence."
- **Specificity table.** "The more precise your instructions, the fewer corrections you'll need." Before: "add tests for foo.py." After: "covering the edge case where the user is logged out. avoid mocks."
- **CLAUDE.md.** "Would removing this cause Claude to make mistakes?" If not, cut it. "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" Exclude "Anything Claude can figure out by reading code."
- **Hooks vs instructions.** "CLAUDE.md instructions... are advisory, hooks are deterministic."
- **Course-correct.** "After two failed corrections, `/clear` and write a better initial prompt."
- **Adversarial review.** "Report gaps, not style preferences." Caveat: "A reviewer prompted to find gaps will usually report some."

---

## 3. How Anthropic phrases its own skills and system prompts

Observed conventions across the sample prompts and Skill docs:

1. **Imperative, second-person voice for instructions.** Every sample block addresses the model directly: "Never speculate," "Use subagents when," "Before ending your turn, check your last paragraph." Skill *descriptions* are the exception: "Always write in third person" because "inconsistent point-of-view can cause discovery problems."
2. **Rationale attached to rules.** Anthropic practices what it preaches in 1.2. Examples: parallel calls are justified "to increase speed and efficiency"; targeted edits because "a rewrite costs more output tokens and time"; the autonomy prompt explains that questions "will block the work."
3. **Define the anti-pattern rather than forbid the word.** The mannered-prose instruction is a paragraph defining the failure ("substitutes metaphor and flourish for direct statement") followed by a positive rule, "say what you mean."
4. **Calibrated degrees of freedom.** Skills page: "Match the level of specificity to the task's fragility and variability." High freedom for "Multiple approaches are valid"; low freedom for "Operations are fragile and error-prone," phrased as "Run exactly this script" and "Do not modify the command." Analogy: "Narrow bridge with cliffs on both sides" vs "Open field with no hazards." Templates come in two strengths: "ALWAYS use this exact template structure" vs "a sensible default format, but use your best judgment."
5. **Escape hatches instead of option lists.** "Provide a default (with escape hatch)"; "Avoid offering too many options."
6. **Assume intelligence; cut explanation.** "Default assumption: Claude is already very smart." "Only add context Claude doesn't already have." "Does this paragraph justify its token cost?" Claude Code: "State what to do rather than narrating how or why" (skill bodies are a recurring cost).
7. **Progressive disclosure.** Three levels: metadata "always loaded" (~100 tokens), SKILL.md "loaded when triggered" (under 5k tokens), resources "loaded as needed." "Keep SKILL.md body under 500 lines." "Keep references one level deep from SKILL.md." Long files get a table of contents so Claude "can see the full scope... even when previewing." Blog framing: like "a table of contents, then specific chapters, and finally a detailed appendix"; bundled context is "effectively unbounded."
8. **Descriptions carry both what and when.** "must say both what the Skill does and when to use it." Bad: "Helps with documents."
9. **Consistent terminology.** "Choose one term and use it throughout the Skill."
10. **Workflows as checklists and feedback loops.** "provide a checklist that Claude can copy into its response." "Run validator → fix errors → repeat."
11. **Evaluation before documentation.** "Create evaluations BEFORE writing extensive documentation." Iterate with two Claude instances: "Claude A helps you design... Claude B tests them."
12. **Positional emphasis.** Fable 5.1 autonomy block: "The opening sentence... carries much of the effect. Keep it as written."
13. **Place instructions where they bind.** User-message placement is sometimes preferred over system ("Add it to a user message (preferred)"); per-turn nudges go in turn-scoped system messages.

---

## 4. Tools and context (engineering blog)

- **Building effective agents.** "the most successful implementations weren't using complex frameworks." Principles: "Maintain simplicity," "Prioritize transparency by explicitly showing the agent's planning steps," "Carefully craft your agent-computer interface (ACI)." Tool tips: "Put yourself in the model's shoes. Is it obvious how to use this tool?" "Poka-yoke your tools." SWE-bench fix: require absolute filepaths.
- **Writing tools for agents.** "Tools are a new kind of software which reflects a contract between deterministic systems and non-deterministic agents." "think of how you would describe your tool to a new hire." Use `user_id` not `user`. "we restrict tool responses to 25,000 tokens by default." Errors should give "specific and actionable improvements, rather than opaque error codes."
- **Context engineering.** "the set of strategies for curating and maintaining the optimal set of tokens." Goal: "the smallest possible set of high-signal tokens." Tools must be "self-contained, robust to error, and extremely clear." Strategies: just-in-time retrieval (Claude Code uses "head and tail"), compaction, "notes persisted to memory outside of the context window," and sub-agents returning "distilled summaries."
- **Agent Skills blog.** "like putting together an onboarding guide for a new hire." Authoring: "Start with evaluation," "Structure for scale," "Think from Claude's perspective," "Iterate with Claude." Code gives "deterministic reliability."

---

## 5. Summary of Claude-specific claims worth citing

| Claim | Source |
|---|---|
| "The more precisely you explain what you want, the better the result." | Prompting best practices, Be clear and direct |
| "Claude is smart enough to generalize from the explanation." | Prompting best practices, Add context |
| Newer models "may now overtrigger"; replace "CRITICAL: You MUST" with "Use this tool when..." | Prompting best practices, Tool usage |
| "Queries at the end can improve response quality by up to 30 percent." | Prompting best practices, Long context |
| "'think thoroughly' often produces better reasoning than a hand-written step-by-step plan." | Prompting best practices, Thinking |
| Prefill on last assistant turn returns "a 400 error" on 4.6+ | Prompting best practices, Migrating away from prefill |
| Parallel calls promptable "to ~100%" | Prompting best practices, Parallel tool calling |
| "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" | Claude Code best practices |
| Only `ultrathink` is a recognized keyword; "think hard" is "ordinary prompt text" | Claude Code model-config |
| "Default assumption: Claude is already very smart." | Skill authoring best practices |
| "Keep SKILL.md body under 500 lines." | Skill authoring best practices; Claude Code skills |
| Tool responses capped at "25,000 tokens by default" in Claude Code | Writing tools for agents |

---

## Sources

Pages actually fetched and read:

- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview (redirect target of `/docs/en/docs/build-with-claude/prompt-engineering/overview`)
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (redirect target of be-clear-and-direct, multishot-prompting, chain-of-thought, use-xml-tags, system-prompts, prefill-claudes-response, chain-prompts, long-context-tips, extended-thinking-tips, claude-4-best-practices, prompt-generator, prompt-improver, prompt-templates-and-variables)
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/best-practices (redirect target of https://www.anthropic.com/engineering/claude-code-best-practices)
- https://code.claude.com/docs/en/model-config
- https://www.anthropic.com/engineering/building-effective-agents
- https://www.anthropic.com/engineering/writing-tools-for-agents
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

Not fetched (referenced only): https://platform.claude.com/docs/en/about-claude/models/migration-guide; the per-model pages for Fable 5, Sonnet 5, Opus 5, Opus 4.8; https://claude.com/blog/best-practices-for-prompt-engineering.
