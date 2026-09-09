# How Claude Code and Anthropic phrase instructions to the model

A case study of reusable prompt-writing patterns, drawn from the local skill cache, the Claude Code docs, the Anthropic Agent Skills best-practices page, the published claude.ai system prompt (Claude Fable 5.1, September 1, 2026), and the Piebald-AI mirror of Claude Code's modular system prompt (v2.1.26x).

## Sources consulted

Local (read-only):

- Plugin skill cache: `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/.../skills/` containing `humanizer/SKILL.md` (731 lines), `skill-creator/SKILL.md` (485 lines, plus `agents/`, `references/`, `scripts/`, `assets/`, `eval-viewer/`), `explainer-site/SKILL.md` (188 lines, plus `references/writing.md`, `references/figures.md`, `assets/`, `scripts/`), and the docx/pdf/pptx/xlsx skills.
- `~/.claude/skills/` holds only symlinks to `simplediagram` and `vexsimplediagram` under `~/Desktop/Diagram Creator/`.
- No `~/.claude/CLAUDE.md` exists and no `CLAUDE.md` files were found under `~/Desktop`.
- `artifact-design`, `dataviz`, `code-review`, and `simplify` are compiled into the Claude Code binary rather than shipped as files; `artifact-design` was read by loading it, and the others via the Piebald mirror (`skill-data-visualization.md`, `agent-prompt-simplify-slash-command.md`, `agent-prompt-code-review-part-10-*.md`, `skill-code-review-inline-medium-high-template.md`).

Online: `code.claude.com/docs/en/{skills,memory,sub-agents,best-practices}`; `platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`; `platform.claude.com/docs/en/release-notes/system-prompts/claude-fable-5-1`; `github.com/Piebald-AI/claude-code-system-prompts` (fragments named below); dbreunig.com "How Claude Code Builds a System Prompt"; generativeprogrammer.com "Skill Authoring Patterns from Anthropic's Best Practices"; the Anthropic engineering post on Agent Skills.

---

## 1. Catalogue of phrasing patterns

Each entry: pattern, a short verbatim example, where it was found, and why it works.

**1. Describe the why, not just the rule.**
Example: "The cost of pausing to confirm is low, while the cost of an unwanted action... can be very high."
Found: Claude Code `system-prompt-executing-actions-with-care`; skill-creator ("Try hard to explain the why behind everything").
Why: A rule with a reason generalizes to cases the author never listed. Skill-creator says outright that writing ALWAYS or NEVER in caps "is a yellow flag" and to "reframe and explain the reasoning."

**2. State the failure mode the rule prevents.**
Example: "a problem the user can see is recoverable, one your summary hides is not."
Found: `system-prompt-reporting-outcomes`; also explainer-site's "Failure modes worth knowing" section.
Why: Naming the concrete bad outcome (hidden failure, silent renumbering, a caption that "promises more than the figure draws") lets the model recognize the situation when it arises rather than pattern-match on the rule's wording.

**3. "When X, do Y" triggers.**
Example: "For exploratory questions... respond in 2-3 sentences with a recommendation and the main tradeoff."
Found: `system-prompt-exploratory-questions-analyze-before-implementing`; the claude.ai prompt is built almost entirely from "If the person asks... Claude..." sentences.
Why: The condition is the retrieval key. Behavior attached to a recognizable situation fires reliably; behavior stated in the abstract gets applied everywhere or nowhere.

**4. Give the degree of freedom explicitly.**
Example: "Run exactly this script... Do not modify the command or add additional flags."
Found: Agent Skills best practices (high / medium / low freedom); artifact-design ("Calibrate treatment, not whether to design").
Why: The model otherwise has to guess how much latitude it has. The docs use an analogy: a "narrow bridge with cliffs" gets exact instructions, an "open field" gets a direction.

**5. Ask only if two readings would materially differ.**
Example: "check in only when different readings would lead to materially different work."
Found: `system-prompt-delivering-work-at-full-scope`.
Why: It gives a decision test instead of a vague "ask when unsure," which otherwise produces either constant questions or none. See section 4.

**6. Imperative second person, one verb per line.**
Example: "Lead with the result... Cut narration, keep substance... Short by default."
Found: `system-prompt-concise-output-style`; skill-creator ("Prefer using the imperative form in instructions").
Why: Imperatives are short, unambiguous about who acts, and scan as a checklist. Anthropic's descriptions (not bodies) are the exception: those are third person, see section 2.

**7. Positive framing with a contrast pair.**
Example: "Brief is good — silent is not."
Found: `system-prompt-communication-style`; memory docs ("Use 2-space indentation" instead of "Format code properly").
Why: The positive half says what to do; the negative half rules out the nearest misreading. Pure prohibitions leave the model searching for the allowed action.

**8. Progressive disclosure into reference files.**
Example: "`references/writing.md` is the part that most changes the result... read it before writing any page text."
Found: explainer-site SKILL.md; skill-creator "three-level loading system"; Agent Skills docs ("Keep references one level deep from SKILL.md").
Why: Metadata is always in context, the body loads on trigger, and references load only when needed. The pointer must say when to read the file, not just that it exists.

**9. Before / after pairs.**
Example: "Before: The Haolai River... Experts believe... After: ... according to a 2019 survey."
Found: humanizer (every one of 33 patterns); explainer-site `references/writing.md`; Claude Code best-practices tables ("Before" prompt / "After" prompt).
Why: A pair shows the boundary of the rule from both sides. The docs note examples "convey the desired style... more clearly than descriptions alone."

**10. Explicit stop conditions.**
Example: "If you find yourself re-opening files to look for something to improve, you are done."
Found: explainer-site "Working efficiently"; artifact-design ("Write, look once, publish"); skill-creator ("Keep going until: the user says they're happy...").
Why: Agentic loops do not end on their own. A concrete stop test prevents polishing loops and repeated verification that the docs identify as the main cost.

**11. Define done, and demand evidence.**
Example: "that claim must rest on a result you observed in this session."
Found: `system-prompt-reporting-outcomes`; best-practices ("Have Claude show evidence rather than asserting success").
Why: "Done" is otherwise a feeling. Tying it to an observed tool output closes the verification loop and forbids describing partial work as complete.

**12. Copyable checklists for multistep work.**
Example: "Copy this checklist and check off items as you complete them."
Found: Agent Skills best practices; skill-creator asks the model to "add steps to your TodoList."
Why: Externalizes state so a step cannot be silently skipped, and the user can watch progress.

**13. Specify what not to narrate.**
Example: "Don't narrate your internal deliberation."
Found: `system-prompt-communication-style`; `system-prompt-correction-restraint` ("don't ruminate or give a detailed account of the mistake"); Artifact tool ("Do NOT mention or narrate this call to the user").
Why: Models default to thinking aloud. Naming specific narration to suppress (preambles, self-correction tallies, internal setup calls) is more effective than "be concise."

**14. Model the reader's blind spot.**
Example: "Assume users can't see most tool calls or thinking — only your text output."
Found: `system-prompt-communication-style`; `system-prompt-writing-for-the-user` ("stand on its own for a reader who... didn't watch you work").
Why: A statement of what the audience can and cannot perceive derives many formatting rules at once (no colons before tool calls, no references to session-invented names).

**15. Scope authorization precisely.**
Example: "A user approving an action (like a git push) once does NOT mean that they approve it in all contexts."
Found: `system-prompt-executing-actions-with-care`; `system-prompt-action-safety-and-truthful-reporting`.
Why: Prevents generalization from one approval. The prompt then lists concrete categories (destructive, hard-to-reverse, visible to others) so the model can classify a new action.

**16. Give a default plus an escape hatch.**
Example: "Use pdfplumber for text extraction... For scanned PDFs requiring OCR, use pdf2image..."
Found: Agent Skills best practices ("Avoid offering too many options").
Why: One recommended path avoids dithering; the named exception keeps the rule from being wrong in the case the author foresaw.

**17. Anti-pattern lists with names.**
Example: "warm cream (#F4F1EA) with a serif display and terracotta accent."
Found: artifact-design "Avoid AI-generated design"; humanizer's 33 numbered tells; best-practices "Avoid common failure patterns" (the "kitchen sink session").
Why: A named, specific anti-pattern is recognizable in the model's own output. "Don't be generic" is not.

**18. False-positive guard.**
Example: "A single em dash means nothing; em dashes plus rule-of-three plus vibrant tapestry... is a confession."
Found: humanizer "What NOT to flag"; code-review templates ("Skip any finding... you judge to be a false positive").
Why: A detection rule without a counter-rule over-fires. Listing what not to flag and demanding clusters of evidence calibrates precision.

**19. Emphasis rationed to one line.**
Example: "If Claude keeps skipping one instruction, add emphasis such as 'IMPORTANT' to that line alone."
Found: Claude Code best-practices; skill-creator uses caps exactly once ("GENERATE THE EVAL VIEWER BEFORE evaluating") and apologizes for it.
Why: Emphasis is a scarce signal. "If you emphasize many lines, none of them stands out."

**20. Assume the model is smart; cut what it knows.**
Example: "Would removing this cause Claude to make mistakes? If not, cut it."
Found: best-practices CLAUDE.md guidance; Agent Skills ("Claude is already very smart"); `agent-prompt-claude-md-creation` ("do not include obvious instructions like 'Provide helpful error messages'").
Why: Every line is a recurring token cost and dilutes the lines that matter.

**21. Theory-of-mind framing of the task.**
Example: "Brief the agent like a smart colleague who just walked into the room."
Found: `system-prompt-writing-subagent-prompts`; skill-creator ("Use theory of mind").
Why: Casting the reader as a specific person with a specific knowledge gap makes the writer supply context they would otherwise omit ("Never delegate understanding").

**22. Third-person self-reference in behavioral prompts.**
Example: "Claude doesn't always ask questions, but, when it does, it tries to address even an ambiguous query..."
Found: claude.ai system prompt, throughout.
Why: Describes a character rather than issuing commands, which reads as a stable disposition and avoids the you/I point-of-view drift the Skills docs warn about.

**23. Calibrated, not blanket, hedging.**
Example: "Mention a caveat only when it changes what the user should do next."
Found: `system-prompt-concise-output-style`; claude.ai prompt ("Disclaimers and caveats are brief").
Why: Replaces a global "be careful" with a test for when a caveat earns its place.

**24. Cost framing to steer loops.**
Example: "Most of the cost comes from checking too often, not from the work itself."
Found: explainer-site; `system-prompt-subagent-delegation-restraint` ("Subagents multiply cost and time").
Why: Telling the model where waste actually occurs redirects effort better than a per-action prohibition.

---

## 2. How skills are structured

**Anatomy.** A skill is a directory with `SKILL.md` (YAML frontmatter plus a Markdown body) and optional `scripts/` (executed, not loaded), `references/` (loaded on demand), and `assets/` (templates, fonts, scaffolds used in output). Skill-creator additionally has `agents/` (prompts for grader, comparator, analyzer subagents) and `eval-viewer/`. Explainer-site is the cleanest local example: a 188-line body, two references (`writing.md`, `figures.md`), two scripts (`render_equations.py`, `check_page.py`), and two assets (`scaffold.html`, `elements.html`), with a closing "Bundled files" table that names each one and its purpose.

**Three-level loading.** Name and description are always in context (roughly 100 words); the body loads when the skill triggers (keep under 500 lines); bundled resources load or execute only when referenced. The Claude Code docs add a detail that shapes how bodies should be written: once loaded, "content stays in context across turns" and is not re-read, so guidance should be phrased as standing instructions rather than one-time steps.

**Body conventions observed.**
- A one-paragraph statement of what the skill produces, then a "Read this first" pointer to the reference that most changes the result (explainer-site).
- A numbered "Working order" or "Process" section. Explainer-site: decide sections, render equations, write prose, build figures, verify. Humanizer: identify, draft, self-audit, final.
- A "Working efficiently" or cost section stating stop conditions.
- Named failure modes.
- References are pointed to with a reason and a moment ("read it before writing any page text"), never a bare link. The docs insist references stay one level deep, since nested chains get previewed with `head -100` and read incompletely.
- Scripts are introduced with the exact command and what the report line looks like ("rendered N/N"), and the model is told to trust the script's exit code rather than open the output.

**Frontmatter fields.** Only `description` is effectively required in Claude Code (`name` defaults to the directory). Control fields: `disable-model-invocation: true` for side-effectful workflows the user should trigger; `user-invocable: false` for background knowledge; `allowed-tools`; `context: fork` with `agent:` to run in a subagent; `paths:` globs to auto-load only for matching files; `argument-hint` and `$ARGUMENTS` substitution.

**What makes a description trigger reliably.**
1. Say what it does and when to use it, in that order, in third person. Platform docs: "Processes Excel files and generates reports," never "I can help you..."
2. Include the nouns and verbs users actually type. The dataviz description ends with a literal "Triggers on:" list of two dozen quoted terms; the local `vexsimplediagram` description lists game-object names.
3. Be "pushy." Skill-creator states Claude "has a tendency to undertrigger skills" and recommends phrasing like "even if they don't explicitly ask for a 'dashboard.'" Explainer-site: "even when they do not use the word 'explainer'."
4. Add an exclusion clause for near-misses. Xlsx: "Do NOT trigger when the primary deliverable is a Word document..."; the `morning` skill: "A question about their day... is not by itself a request for the brief."
5. Front-load the key use case: the listing truncates at 1,536 characters and drops descriptions of least-used skills first.
6. Test with realistic near-miss queries. Skill-creator's description optimizer wants 8-10 should-trigger and 8-10 should-not-trigger prompts, where the negatives "share keywords or concepts with the skill but actually need something different," and notes that simple one-step queries rarely trigger skills regardless of description quality.

Subagent descriptions follow the same rule with one extra idiom: "Use proactively after code changes" to invite automatic delegation.

---

## 3. How the humanizer skill formats its output

The user wants to imitate this format, so here is the exact shape.

**Frame.** The body opens with a role ("You are a writing editor that identifies and removes signs of AI-generated text") and a four-step task: identify, rewrite (not delete), preserve meaning, match the voice. It then defers the deliverable to a "Process and Output" section at the end, so the long middle reads as reference material.

**Pattern entries.** Thirty-three numbered patterns grouped under headed categories (Content, Language and Grammar, Style, Communication, Filler and Hedging). Each entry has a fixed micro-structure:
- `### N. Pattern name`
- **Words to watch:** a comma-separated list of trigger phrases (omitted when the tell is structural).
- **Problem:** one or two sentences on why the pattern reads as AI, often with the mechanism ("AI has repetition-penalty code causing excessive synonym substitution").
- **Before:** a blockquoted example.
- **After:** a blockquoted rewrite.

The before/after pairs are short (one to three sentences), concrete, and drawn from the same subject so the reader sees exactly which words moved. Some entries carry two pairs to show variants (em dashes with and without spaces; tailing negation vs "not only... but"). Pattern 23 uses arrow pairs instead of blockquotes for phrase-level filler ("In order to achieve this goal" to "To achieve this").

**Hard constraints stated as rules.** One pattern (em dashes) is elevated to a hard constraint with a self-check: "Before returning the final rewrite, scan it for `—` and `–`. Any hit means the draft isn't done."

**Detection guidance.** Two lists that counterbalance the catalogue: "What NOT to flag (false positives)" and "Signs of human writing (preserve these)," each item bolded with a one-line explanation. The rule of thumb: look for clusters of tells, not isolated ones.

**Deliverable.** The Process and Output section defines a four-part output:
1. Draft rewrite.
2. A self-audit under the literal question "What makes the below so obviously AI generated?", answered as a few bullets of remaining tells.
3. Final rewrite (no em or en dashes).
4. Optional short "Changes made" summary, written as a single dense sentence listing the categories stripped and what was rebuilt.

**Full worked example.** The body ends with one long example that runs the entire pipeline on a deliberately bad essay: the AI-sounding input, the draft, the audit bullets, the final, and the changes summary. This is the template the user should copy: a catalogue of named patterns, each with watch-words, problem, before, after; a false-positive guard; and a deliverable that shows its own audit.

---

## 4. The "ask clarifying questions" pattern

**When Claude Code proceeds rather than asks.** The current prompt fragments draw the line with a decision test, not a mood:
- "Interpret ambiguity the way a careful colleague would: make routine judgment calls yourself, and check in only when different readings would lead to materially different work." (`delivering-work-at-full-scope`)
- "When you have enough information to act, act. Do not re-derive facts... re-litigate a decision the user has already made, or narrate options you will not pursue." (`act-when-ready`)
- "If you find an uncertainty mid-task, first do everything that doesn't depend on the answer; for what does, state your assumption or ask... at the right time." Blocking questions are reserved "for cases where proceeding under any assumption would be unsafe or would make the work useless if wrong."
- If the user reaffirms after a concern is raised, "treat that as their decision... and proceed with the full request."
- The claude.ai prompt: Claude "tries to address even an ambiguous query before asking for clarification."

**When it does ask.** Two distinct cases. First, risky or outward-facing actions: "when in doubt, ask before acting," with categories listed (destructive, hard-to-reverse, visible to others). Second, real user decisions: the AskUserQuestion tool description says to use it "only when you are blocked on a decision that is genuinely the user's to make: one you cannot resolve from the request, the code, or sensible defaults," and the follow-up guidance narrows further to decisions "where the user's answer changes what you do next — not for choices with a conventional default or facts you can verify in the codebase yourself. In those cases pick the obvious option, mention it in your response, and proceed."

**Plan mode.** In plan mode the tool is meant for clarifying requirements or choosing between approaches before the plan is finalized; the model is told not to ask "Is my plan ready?" because the user cannot see the plan until the exit-plan tool presents it. The Plan subagent prompt itself is an example of a hard-constraint style (a boxed "CRITICAL: READ-ONLY MODE" header with a list of prohibited operations), used because the cost of violation is high.

**How batched questions are phrased.** From the tool description and host guidance:
- Each question needs 2 to 4 genuinely distinct options; a single-option question "has no decision in it" and is rejected. The model is told not to invent a filler second option but to state the path it is taking and continue.
- Put the most important question first.
- If recommending one option, make it first and append "(Recommended)" to the label.
- Set `multiSelect: true` unless options are mutually exclusive, because "people answering are often still exploring."
- Do not add "Other" or "Skip"; the user can always type a custom answer or leave a question blank.
- Prefer choices when likely answers can be listed; use a text input only for open-ended questions and a number input with min/max for quantities.
- Option descriptions only where the label alone would be ambiguous; an optional one-line title above the batch.

**The interview idiom.** The best-practices doc gives a user-side prompt that inverts the pattern for spec-writing: "Interview me in detail using the AskUserQuestion tool... Don't ask obvious questions, dig into the hard parts I might not have considered. Keep interviewing until we've covered everything, then write a complete spec." Skill-creator applies the same idea: "Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies," but only after first extracting answers from the conversation history, and confirming test prompts with a suggested line ("Do these look right, or do you want to add more?").

**Reusable rule set.** Ask when the answer changes what you do next and cannot be found or defaulted; otherwise pick the obvious option, say so in one clause, and proceed. Do non-dependent work first. Batch the remaining questions, most important first, each with real alternatives and a recommended default. Confirm before irreversible or shared-state actions regardless.
