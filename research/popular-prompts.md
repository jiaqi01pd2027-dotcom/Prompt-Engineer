# Which prompts people actually use: a survey of shared prompts

Compiled 2026-09-27 and 28. Four source families were searched in parallel: GitHub prompt
and skill repositories, official vendor guides (Anthropic, OpenAI, Google,
promptingguide.ai, learnprompting.org), Reddit and Hacker News, and viral posts on X,
LinkedIn, Substack, and YouTube. A prompt counts as "used" when it recurs across
independent sources, or when a platform reports installs for that one prompt. Stars are
repo-level, so they measure a collection, not a prompt.

Checks: star counts were re-read from the GitHub API, install counts from skills.sh,
tweet figures from the fxtwitter mirror, Hacker News points from the Algolia API, and
r/PromptEngineering's top-of-year order from Reddit's RSS feed. All matched what the
search agents reported except one claim about Remotion, corrected under Caveats. Other
subreddit feeds were blocked on re-check, so their upvote counts come from press coverage
and are marked "reported". Quotes are kept under 15 words; the full text of each prompt
is at the linked source.

## The answer

The most-used prompt is **"interview me before you build"**. You give a one-line idea,
the model questions you until every decision is settled, then it writes the spec to a
file and a fresh session builds from it. Its chat form is the older one-liner "ask me
clarifying questions until you're 95% confident".

It is the only template in the top five of all three source families that rank prompts,
Anthropic's own guides include it, and it has the largest measured usage of any single
prompt.

- **Measured installs.** Matt Pocock's grill-me is the most-installed prompt on
  skills.sh at 1.2M. The one entry above it, find-skills, is a search utility.
- **GitHub.** Seven skill collections carry a version, including obra/superpowers,
  addyosmani/agent-skills, and Anthropic's own docs.
- **Viral posts.** Thariq Shihipar of the Claude Code team posted it on 2025-12-28:
  2.33M views, 14.6K bookmarks, and nineteen verified reposts and write-ups.
- **Reddit and Hacker News.** The 95%-confident form appears in fourteen places, and
  interview or Socratic forms in eleven more.
- **Official.** Anthropic put it on the Claude Code best-practices page and in the
  official prompt library.

A fill-in version, written for this note from the elements the copied versions share.
The originals are linked under Sources.

```
I want to build <one-line description>. Before any code, interview me.
Ask in rounds of 3 to 5 numbered questions, each with your recommended answer.
Cover how it works, what the user sees, edge cases, and tradeoffs. Skip the obvious,
and skip anything you can learn from the code yourself.
Keep going until no decision is open. Then write the spec to SPEC.md: the files and
interfaces involved, what is out of scope, and one end-to-end check that proves it works.
```

For a chat task, one line before the request does the same job: ask the model to put
clarifying questions to you until it is 95% confident it can do the task well.

Where audiences differ, and who leads on narrower measures:

- **General chat users** on Reddit repost anti-flattery prompts most: brutal honesty,
  no praise, "Absolute Mode". That family appears in more than twenty places.
- **Coding-agent users** on GitHub and X repost process prompts: interview first,
  verify, plan, critic loops.
- **Most-viewed advice:** "give Claude a way to verify its work". It headlines Boris
  Cherny's January thread, 8.23M views, and opens Anthropic's best-practices page. It
  is a clause added to prompts, not a prompt on its own.
- **Most-starred single prompt file:** the Karpathy-style CLAUDE.md, 215,501 stars.
- **Most-viewed single post:** Remotion's "make videos just with Claude Code", 18.85M
  views, which started the explainer-video prompt trend.

## Measured usage (verified 2026-09-27)

Per-prompt installs, skills.sh leaderboard (https://skills.sh/). This is the only public
per-prompt usage count found.

| Rank | Skill | Repo | Installs | What it is |
|---|---|---|---|---|
| 1 | find-skills | vercel-labs/skills | 3.6M | utility that searches for skills; not a prompt in the usual sense |
| 2 | grill-me | mattpocock/skills | 1.2M | interview the user until every decision is settled |
| 3 | agent-browser | vercel-labs/agent-browser | 954.8K | browser tool wrapper |
| 4 | frontend-design | anthropics/skills | 927.9K | anti-generic UI design guidance |
| 5 | setup-matt-pocock-skills | mattpocock/skills | 898.5K | installer |
| 6 | vercel-react-best-practices | vercel-labs/agent-skills | 747.3K | numbered React rules |
| 8 | teach | mattpocock/skills | 717.7K | tutoring prompt |

Repo stars, GitHub API.

| Repo | Stars | Created | Shape |
|---|---|---|---|
| obra/superpowers | 292,103 | 2025-10 | workflow skills: brainstorm, plan, TDD, verify, review |
| mattpocock/skills | 270,555 | 2026-02 | skills incl. grill-me, tdd, handoff |
| affaan-m/ECC | 268,205 | 2026-01 | 68 agents, 292 skills, rules per language |
| multica-ai/andrej-karpathy-skills | 215,501 | 2026-01 | one 358-word CLAUDE.md |
| anthropics/skills | 178,638 | 2025-09 | official SKILL.md examples |
| f/awesome-chatgpt-prompts | 171,405 | 2022-12 | 180 "act as X" chat prompts |
| DietrichGebert/ponytail | 146,802 | 2026-06 | anti-over-engineering skill |
| x1xhlol/system-prompts-and-models-of-ai-tools | 143,902 | 2025-03 | leaked product system prompts |
| JuliusBrussee/caveman | 108,033 | 2026-04 | terse-output skill |
| addyosmani/agent-skills | 99,416 | 2026-02 | 25 lifecycle skills incl. interview-me |
| dair-ai/Prompt-Engineering-Guide | 78,671 | 2022-12 | technique guide, not prompts |
| hesreallyhim/awesome-claude-code | 54,683 | 2025-04 | curated CLAUDE.md files and commands |
| blader/humanizer | 52,289 | 2026-01 | AI-writing-tells rewrite skill |
| PatrickJS/awesome-cursorrules | 40,840 | 2024-09 | Cursor rules by stack |
| anthropics/prompt-eng-interactive-tutorial | 38,327 | 2024-04 | Anthropic's tutorial |
| langgptai/awesome-claude-prompts | 5,506 | 2023-07 | Claude chat prompts |

The star mass has moved. The 2023 "act as X" chat lists still hold large star counts,
but their prompts recur nowhere else. Seven of the ten largest repos above were created
after September 2025 and hold coding-agent instructions: skills, CLAUDE.md files, rules.
The most-starred single prompt file is the Karpathy-style CLAUDE.md, 358 words in four
rules: think before coding, simplicity first, surgical changes, goal-driven execution.

## Ranked: templates that recur across independent sources

Order: first by how many of the four source families carry the template, then by
verified reach. First place is clear on both counts. Below it the order is a judgment
call, and the evidence columns are what to weigh.

| # | Template | Families | GitHub and skills | Viral posts | Official guides | Reddit and HN | Verified reach |
|---|---|---|---|---|---|---|---|
| 1 | Interview me first, or ask clarifying questions until 95% confident | 4 | 7 collections | 19 places | Anthropic docs and prompt library | 14 places, plus 11 interview or Socratic | grill-me 1.2M installs; origin post 2.33M views |
| 2 | Give it a check it can run; show evidence | 4 | 6 collections | Cherny and Karpathy threads | Anthropic, OpenAI, Google | "verify with citations", 5 places | Cherny thread 8.23M views |
| 3 | Plan before code | 4 | 7 collections | Cherny: put the effort into the plan | Anthropic four-phase workflow | 8 places | HN planning thread, 976 points |
| 4 | Simplicity and surgical changes | 4 | 7 collections | Karpathy rules | Anthropic overeagerness section | lazy-senior-dev post, about 1,900 upvotes (reported) | Karpathy CLAUDE.md 215.5K stars; ponytail 146.8K |
| 5 | A separate critic loops until the work passes a bar | 4 | 6 collections, plus the Ralph loop plugin | Gauntlet Loop 17 places; score-and-iterate 8 | Anthropic adversarial review step | 10 places; "rate 1-10, fix anything under 8" in 4 | Gauntlet demo 5.05M views |
| 6 | Write the lesson into CLAUDE.md | 4 | 3 collections | Cherny thread 2 | Anthropic prompt library | Cherny's rule on 6+ sites | Cherny thread 2, 9.24M views |
| 7 | Brutal honesty, no praise | 3 | Cursor anti-sycophancy rules | 11 places | none | 20+ places, the most on Reddit | Hassid post 1.09M views |
| 8 | Terse output, no filler | 3 | caveman skill | not ranked | Anthropic verbosity guidance | 12 places; caveman post about 10K upvotes (reported) | caveman 108K stars |
| 9 | Test first, then make it pass | 3 | 7 collections | Karpathy: tests first | Anthropic prompt library | not surfaced | superpowers TDD skill |
| 10 | Explainer or motion-graphics video from one prompt | 2 | Remotion skills | 19 places | none | not surfaced | Remotion post 18.85M views; 1.5M installs |

Honourable mentions:

- **The role opener**, "You are a senior X". It sits in almost every collection and in
  fifteen Reddit and HN places, but it is a fragment, not a prompt.
- **Structured fill-in frameworks** such as KERNEL, the top r/PromptEngineering post of
  the year, and role-context-task-format-constraints. Ten places.
- **Social-pressure hacks** such as "my boss is watching". Ten places, all on Reddit.
- **Memory self-insight**, asking the model what it knows about you. Nine places; one
  r/ChatGPT post reported at 10K upvotes.
- **ELI5**, nine places. **"ultrathink" and "ultracode"** effort words, fourteen.
- **The 2023 "act as X" chat prompts**, which hold 171K stars but recur nowhere else.

## The shape popular prompts share

Four generations of shared prompts, converging on one skeleton.

1. **Chat prompts, 2022-2023.** "I want you to act as X", then an "I will / you will"
   protocol, negative output limits, and a kickoff line. No examples, no checks.
2. **Leaked product system prompts.** Identity line, environment, an instruction to
   keep going until the task is resolved, sections by XML tag or header, emphatic
   NEVER rules, tool docs, refusal policy.
3. **Rules files: CLAUDE.md, .cursorrules, Copilot instructions.** Stack, commands,
   style, architecture, patterns with code, testing, a NEVER list. Kept short;
   Anthropic says under 200 lines and to cut any line whose removal changes nothing.
4. **Skills, 2025-2026.** A name and a description that doubles as the trigger, then a
   numbered process or decision ladder, rules, rationalisations to reject, red flags, a
   verification checklist, often intensity levels and a persistence clause.

Common order across all four: identity, context, process, constraints, output format,
verification, examples. Examples are the least common element in community prompts even
though every vendor guide recommends them.

Official guides agree on five elements only: a specific task, context kept separate from
instructions, an output format, delimiters between sections, and iterating against a
test. Role lines, chain-of-thought cues, and XML versus Markdown are contested; the
guides split on reasoning models in particular, where OpenAI and Anthropic now advise
against step-by-step cues.

## What this means for this project

- **It matches the paper's result.** The experiment measured this pattern as P9:
  8.75 of 10, second only to the full stack at 9.12, and best on the vague product
  brief. The most-used prompt online is the pattern the 360 runs found strongest after
  the full stack.
- **The most common line adds nothing measurable.** The role opener is the most
  frequent line in shared prompts. In the runs, adding a role to a specific prompt moved
  the mean from 7.09 to 6.94.
- **The full stack circulates as frameworks.** KERNEL and role-context-task-format-
  constraints are Reddit's version of the paper's P8. They spread as fill-in templates,
  not fixed prompts.
- **The skill already had the distinctive parts.** It asks in batches with a
  recommended default and looks facts up itself. Those two features separate the
  popular versions from older "ask me questions" prompts. The gap was rounds and a spec
  file, and the P9 entry in the skill's patterns reference now covers both.
- **What spreads is short and procedural.** The top coding templates are one or two
  sentences that hand the model a process: interview me, verify, loop until a critic
  passes it, write the lesson down. Long persona prompts collect stars but do not recur.
- **One open tension.** Anthropic staff said in July 2026 that Fable works better
  without long example lists and do-not lists, citing Claude Code's own system prompt.
  This project's runs found few-shot examples a solid addition, 8.12, on all three
  models. The runs tested task prompts, not system prompts, so both claims may hold.
- **The demand is visible.** A Claude skill that writes prompts is among the top twelve
  r/PromptEngineering posts of the year.
- **Both prompts saved on 2026-09-27 sit in the top ten.** The water-balloon prompt is
  a separate-critic loop, row 5. The motion-graphics prompt is the explainer-video
  trend, row 10.

## Caveats

- Stars are repo-level. Only skills.sh reports per-prompt installs, and an install is
  not a use.
- Reddit's HTML and JSON endpoints were blocked and its RSS feeds carry no vote counts.
  r/PromptEngineering's top-of-year order was re-checked and matched. The r/ClaudeAI and
  r/ClaudeCode feeds were rate-limited on re-check, so the caveman and lazy-senior-dev
  upvote counts are as reported by Decrypt and mcp.directory.
- Some Reddit figures, such as "400+ upvotes" for the 95%-confident prompt, come from
  aggregator sites without thread links. They support recurrence, not size.
- Place counts are lower bounds, and each search agent counted slightly differently.
- One agent reported Remotion's skill as the top non-platform skill on skills.sh. The
  leaderboard shows its largest skill at 547.3K installs, below grill-me's 1.2M.
- cursor.directory's popularity ranking returned HTTP 429 on three attempts; the claim
  that its most-copied rule is the Next.js/React/TypeScript rule rests on four secondary
  sources.
- Anthropic's classic prompt library now redirects to the consolidated best-practices
  page. Its replacement is the Claude Code prompt library, 52 copy-paste prompts.
- The "Interviewer" prompt in awesome-chatgpt-prompts is a mock job interview. It was
  not counted with the spec-interview prompts.
- Anthropic's Discord is not indexed. PromptBase and FlowGPT listing pages returned 403.

## Sources

- https://skills.sh/
- https://github.com/mattpocock/skills (skills/productivity/grilling/SKILL.md)
- https://github.com/multica-ai/andrej-karpathy-skills (CLAUDE.md)
- https://github.com/obra/superpowers (skills/brainstorming/SKILL.md)
- https://github.com/addyosmani/agent-skills (skills/interview-me/SKILL.md)
- https://github.com/f/awesome-chatgpt-prompts
- https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools
- https://github.com/hesreallyhim/awesome-claude-code
- https://github.com/PatrickJS/awesome-cursorrules
- https://code.claude.com/docs/en/best-practices
- https://code.claude.com/docs/en/prompt-library
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- https://developers.openai.com/api/docs/guides/prompt-engineering
- https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
- https://developers.openai.com/api/docs/guides/reasoning-best-practices
- https://ai.google.dev/gemini-api/docs/prompting-strategies
- https://www.promptingguide.ai/introduction/elements
- https://learnprompting.org/docs/basics/prompt_structure
- https://x.com/trq212/status/2005315275026260309
- https://velvetshark.com/stop-prompting-claude-code-let-it-interview-you
- https://x.com/bcherny/status/2007179832300581177
- https://x.com/bcherny/status/2017742741636321619
- https://x.com/karpathy/status/2015883857489522876
- https://x.com/mattshumer_/status/2081100592689324502
- https://x.com/Remotion/status/2013626968386765291
- https://skills.sh/remotion-dev/skills
- https://x.com/rubenhassid/status/2057325513962574280
- https://www.reddit.com/r/PromptEngineering/top/?t=year
- https://www.reddit.com/r/ClaudeAI/comments/1sble09/
- https://www.reddit.com/r/ClaudeCode/comments/1u3jlo0/
- https://news.ycombinator.com/item?id=47106686
- https://news.ycombinator.com/item?id=46098838
- https://news.ycombinator.com/item?id=40474716
