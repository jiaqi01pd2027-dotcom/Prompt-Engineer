# Literature Review: How Prompt Phrasing Changes LLM Output Quality

Compiled 2026-09-10. All arXiv IDs, authors and venues were checked against arxiv.org, ACL Anthology, or the publishing lab's page. Numbers are taken from abstracts or results tables where they could be fetched; where a figure could not be confirmed from a primary source it is marked "figure not verified". Each bullet ends with a one-line implication for people who write prompts.

---

## 1. Reasoning scaffolds: CoT, zero-shot CoT, self-consistency, ToT, ReAct, Reflexion

- **Wei et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." NeurIPS 2022. arXiv:2201.11903.** https://arxiv.org/abs/2201.11903
  Method: prepend eight hand-written exemplars whose answers include intermediate reasoning steps. Key numbers: PaLM 540B on GSM8K rises from roughly 18% (standard few-shot) to 57% (CoT), then to 58% with an external calculator; the gain is an emergent property of scale and is absent or negative in small models. Implication: showing worked reasoning in examples buys large gains on multi-step math and symbolic tasks, but only with sufficiently large models.

- **Kojima et al. (2022). "Large Language Models are Zero-Shot Reasoners." NeurIPS 2022. arXiv:2205.11916.** https://arxiv.org/abs/2205.11916
  Method: append the single phrase "Let's think step by step" before the answer, with no exemplars. Key numbers (InstructGPT text-davinci-002): MultiArith 17.7% -> 78.7%; GSM8K 10.4% -> 40.7%; comparable relative gains reported for PaLM 540B. Implication: a single trigger phrase can unlock most of the benefit of few-shot CoT, so the cheapest reasoning intervention is a one-line instruction rather than curated examples.

- **Wang et al. (2022). "Self-Consistency Improves Chain of Thought Reasoning in Language Models." ICLR 2023. arXiv:2203.11171.** https://arxiv.org/abs/2203.11171
  Method: sample many CoT paths at non-zero temperature and majority-vote the final answer. Key numbers (abstract): GSM8K +17.9, SVAMP +11.0, AQuA +12.2, StrategyQA +6.4, ARC-challenge +3.9 absolute points over greedy CoT. Implication: prompt phrasing is not the only lever; the same prompt sampled N times and aggregated beats a single greedy answer, at N-times the cost.

- **Yao et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." NeurIPS 2023. arXiv:2305.10601.** https://arxiv.org/abs/2305.10601
  Method: the model generates several candidate "thoughts" per step, self-evaluates them, and searches (BFS/DFS) with backtracking. Key numbers: Game of 24 with GPT-4 goes from 4% (CoT) to 74% (ToT). Implication: for search-like problems, prompting the model to propose, evaluate and prune alternatives beats a single linear chain, but requires a multi-call harness rather than one prompt.

- **Yao et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023. arXiv:2210.03629.** https://arxiv.org/abs/2210.03629
  Method: interleave free-text "Thought" steps with tool "Action"/"Observation" steps in the prompt. Key numbers (abstract): beats imitation- and RL-based baselines by +34 absolute success on ALFWorld and +10 on WebShop with only one or two in-context examples; reduces hallucination on HotpotQA/FEVER relative to CoT alone. Implication: when a tool is available, ask the model to alternate reasoning and tool use rather than reason in one block; this is the basis of most agent prompts.

- **Shinn et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." NeurIPS 2023. arXiv:2303.11366.** https://arxiv.org/abs/2303.11366
  Method: after a failed attempt, the model writes a natural-language self-reflection that is stored in memory and prepended to the next trial. Key numbers (abstract): HumanEval pass@1 91% vs 80% for the GPT-4 baseline. Implication: a prompt that feeds back the previous failure and asks "what went wrong and what will you change" is a cheap, weight-free way to improve iterative tasks.

- **Sprague et al. (2024). "To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning." ICLR 2025. arXiv:2409.12183.** https://arxiv.org/abs/2409.12183
  Method: meta-analysis of over 100 papers plus new runs on 20 datasets and 14 models. Key numbers: CoT gains concentrate on math/logic; up to 95% of the CoT gain on MMLU comes from questions containing "=" in the question or output. Implication: do not reflexively add "think step by step" to non-math tasks; the evidence for benefit outside symbolic reasoning is weak.

---

## 2. The Prompt Report (taxonomy and technique count)

- **Schulhoff et al. (2024). "The Prompt Report: A Systematic Survey of Prompt Engineering Techniques." arXiv:2406.06608.** https://arxiv.org/abs/2406.06608
  Method: PRISMA-style systematic review of the prompting literature, plus a meta-analysis on MMLU and a case study. Key numbers: a vocabulary of 33 terms, a taxonomy of 58 text-based LLM prompting techniques and 40 for other modalities. The taxonomy groups text techniques into six families: in-context learning (few-shot), zero-shot (role, style, emotion, rephrase), thought generation (CoT variants), decomposition (least-to-most, plan-and-solve), ensembling (self-consistency, mixture of reasoning experts), and self-criticism (self-refine, chain-of-verification). The case study (suicide-risk "entrapment" detection) reports that a human expert reached F1 about 0.53 after roughly 20 hours of manual iteration, while a DSPy-optimised prompt produced in minutes was better and, after light human edits, reached roughly 0.6 (exact F1 values figure not verified). Implication: the space of named techniques is large, but the report's own finding is that few-shot and CoT variants dominate measured gains, and that automated optimisation can beat expert manual iteration.

---

## 3. Role / persona prompting

- **Zheng et al. (2023). "When 'A Helpful Assistant' Is Not Really Helpful: Personas in System Prompts Do Not Improve Performances of Large Language Models." Findings of EMNLP 2024. arXiv:2311.10054.** https://arxiv.org/abs/2311.10054 (earlier title: "Is 'A Helpful Assistant' the Best Role for Large Language Models?")
  Method: 162 roles across 6 interpersonal-relationship types and 8 expertise domains, 4 LLM families, 2,410 factual questions. Key finding: adding a persona to the system prompt does not improve accuracy over a no-persona control; gender, type and domain of the persona shift accuracy in inconsistent ways; picking the best persona per question would help, but automatic persona selection performs no better than random. Implication: "You are an expert X" is not a reliable accuracy lever for factual QA; treat it as a style control, not a correctness control.

- **Kong et al. (2023). "Better Zero-Shot Reasoning with Role-Play Prompting." NAACL 2024. arXiv:2308.07702.** https://arxiv.org/abs/2308.07702
  Method: a two-turn role-play setup in which the model first acknowledges a role before answering. Key numbers (ChatGPT): AQuA 53.5% -> 63.8%; Last Letter 23.8% -> 84.2%. The authors argue role-play acts as an implicit CoT trigger. Implication: persona gains, where they appear, look like a side effect of inducing reasoning rather than a property of the role itself.

- **Kim, Yang & Jung (2024). "Persona is a Double-edged Sword: Mitigating the Negative Impact of Role-playing Prompts in Zero-shot Reasoning Tasks." arXiv:2408.08631.** https://arxiv.org/abs/2408.08631
  Method: ensemble a role-play prompt with a neutral prompt ("Jekyll & Hyde"). Key numbers: +9.98 points average accuracy across 12 datasets with GPT-4 over either single prompt; LLM-generated personas are more stable than hand-written ones. Implication: personas can hurt as often as they help; if you use one, hedge it with a neutral run.

- **Basil, Shapiro, Shapiro, Mollick, Mollick & Meincke (2025). "Playing Pretend: Expert Personas Don't Improve Factual Accuracy." Wharton Generative AI Labs technical report, Dec 2025.** https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/
  Method: 6 models (GPT-4o, GPT-4o-mini, o3-mini, o4-mini, Gemini 2.0 Flash, Gemini 2.5 Flash), GPQA Diamond (198 q) and MMLU-Pro (300 q), 12 persona conditions including three low-knowledge personas. Key finding: no expert persona consistently improved GPQA; on MMLU-Pro 5 of 6 models showed no significant improvement and there were 9 instances of significant degradation; low-knowledge personas reliably hurt. Implication: on current frontier models, expert personas are at best neutral for factual accuracy.

---

## 4. Principled Instructions (Bsharat et al.)

- **Bsharat, Myrzakhan & Shen (2023). "Principled Instructions Are All You Need for Questioning LLaMA-1/2, GPT-3.5/4." arXiv:2312.16171.** https://arxiv.org/abs/2312.16171
  Method: 26 hand-written principles (e.g., drop politeness phrases; state the audience; break complex tasks into steps; use "Your task is" and "You MUST"; announce a penalty; offer a tip; use few-shot; "think step by step"; use delimiters; let the model ask clarifying questions) tested on the authors' ATLAS benchmark (20 questions per principle) with LLaMA-1/2 7B-70B, GPT-3.5 and GPT-4, judged by humans on "boosting" (quality) and "correctness". Key numbers (paper HTML): average quality improvement about 50% across models, 57.7% for GPT-4; correctness improvement 36.4% for GPT-4; relative correctness gains exceed 20% for larger models. Principle 14 (let the model ask you questions) improved every question it was applied to. Caveats: small per-principle samples, human-rated quality, and the Wharton tip/threat study below fails to replicate the incentive principles. Implication: structural principles (audience, task delimiters, step decomposition, clarifying questions) have the best support; incentive-style principles (tips, penalties) do not replicate on newer models.

---

## 5. Prompt sensitivity: format, position and tone

- **Sclar, Choi, Tsvetkov & Suhr (2023). "Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting." ICLR 2024. arXiv:2310.11324.** https://arxiv.org/abs/2310.11324
  Method: FormatSpread, a search over hundreds of semantically equivalent formats (separators, casing, spacing) for few-shot prompts. Key numbers: performance differences of up to 76 accuracy points on LLaMA-2-13B from formatting alone; the spread does not shrink with model size, more shots, or instruction tuning. Implication: a single-format benchmark score is not a property of the model; when comparing prompts, hold formatting fixed or sample over formats.

- **Liu et al. (2023). "Lost in the Middle: How Language Models Use Long Contexts." TACL 2024. arXiv:2307.03172.** https://arxiv.org/abs/2307.03172
  Method: multi-document QA and key-value retrieval while moving the relevant document through the context. Key finding: a U-shaped curve; accuracy is highest when the answer is at the start or end of the context and drops substantially in the middle, even for models marketed as long-context. Implication: put the most important content at the beginning or end of the prompt, never buried in the middle.

- **He et al. (2024). "Does Prompt Formatting Have Any Impact on LLM Performance?" arXiv:2411.10541.** https://arxiv.org/abs/2411.10541
  Method: the same content rendered as plain text, Markdown, JSON and YAML across reasoning, code and translation tasks on GPT-3.5-turbo and GPT-4 family models. Key numbers: GPT-3.5-turbo varies by up to 40% on a code-translation task depending on template; GPT-4 is markedly more robust; no single format wins everywhere. Implication: format choice matters most for smaller/older models; test JSON vs Markdown vs prose per task rather than assuming one is best.

- **Mao, Middleton & Niranjan (2023). "Do prompt positions really matter?" Findings of NAACL 2024. arXiv:2305.14493.** https://arxiv.org/abs/2305.14493
  Method: systematic variation of where the instruction sits relative to the input across NLP tasks, including instruction-tuned models. Key finding: positions used in prior work are often sub-optimal and position substantially changes accuracy (exact deltas figure not verified). Implication: instruction placement is a tunable variable, not a convention.

- **Yin et al. (2024). "Should We Respect LLMs? A Cross-Lingual Study on the Influence of Prompt Politeness on LLM Performance." SICon 2024 (ACL workshop). arXiv:2402.14531.** https://arxiv.org/abs/2402.14531 ; https://aclanthology.org/2024.sicon-1.2/
  Method: politeness levels in English, Chinese and Japanese across summarisation, understanding and bias-detection tasks. Key finding: impolite prompts often degrade performance, but very polite prompts do not guarantee gains; the best level differs by language (per-model score deltas figure not verified). Implication: avoid rudeness, but do not expect flattery to help; tone effects are language- and model-specific.

- **Dobariya & Kumar (2025). "Mind Your Tone: Investigating How Prompt Politeness Affects LLM Accuracy (short paper)." arXiv:2510.04950.** https://arxiv.org/abs/2510.04950
  Method: 50 MCQ questions x 5 tone variants (Very Polite to Very Rude) = 250 prompts on ChatGPT-4o. Key numbers: accuracy 80.8% (Very Polite) to 84.8% (Very Rude); rude prompts consistently outperformed polite ones. Follow-up: **Dobariya & Kumar (2026). "Mind Your Tone: Does Tone Alter LLM Performance?" AMCIS 2026. arXiv:2605.29027** extends to GPT-5-nano, Gemini 2.5 Flash and Flash Lite and a 570-question MMLU subset with seven tones, finding tone effects are systematic but highly model-dependent. Implication: the sign of the politeness effect flips between models and years; it is a source of variance to control, not a technique to rely on.

- **Meincke, Mollick, Mollick & Shapiro (2025). "Prompting Science Report 1: Prompt Engineering is Complicated and Contingent." Wharton Generative AI Labs. arXiv:2503.04818.** https://arxiv.org/abs/2503.04818
  Method: each GPQA/MMLU-Pro question run 100 times under polite vs commanding phrasing and different formatting. Key finding: polite or commanding phrasing produces question-specific differences that largely wash out on aggregate; benchmark outcomes also depend heavily on the correctness threshold chosen. Implication: report variance across repeated runs; single-run prompt comparisons are unreliable.

---

## 6. Emotional stimuli

- **Li et al. (2023). "Large Language Models Understand and Can be Enhanced by Emotional Stimuli" (EmotionPrompt). arXiv:2307.11760.** https://arxiv.org/abs/2307.11760
  Method: append psychology-derived sentences such as "This is very important to my career" to prompts; 45 tasks; Flan-T5-Large, Vicuna, Llama 2, BLOOM, ChatGPT, GPT-4; human study with 106 participants. Key numbers (abstract): 8.00% relative improvement on Instruction Induction, 115% on BIG-Bench, 10.9% average improvement in the human study on performance/truthfulness/responsibility. Caveat: the BIG-Bench baseline is very low, which inflates the relative figure. Implication: emotional framing was reported to help older open models, but see the replication below.

- **Meincke, Mollick, Mollick & Shapiro (2025). "I'll pay you or I'll kill you - but will you care?" Wharton Generative AI Labs technical report, Aug 2025.** https://gail.wharton.upenn.edu/research-and-insights/techreport-threaten-or-tip/
  Method: 5 models (Gemini 1.5/2.0 Flash, GPT-4o, GPT-4o-mini, o4-mini), GPQA Diamond and 100 MMLU-Pro engineering questions, 9 conditions including $1,000 and "trillion dollar" tips, threats, and emotional appeals including the EmotionPrompt-style career line. Key numbers: only 5 of 45 GPQA comparisons and 10 of 45 MMLU-Pro comparisons were significant, all with negligible effect sizes; per-question swings ranged from +36 to -35 points but were unpredictable; one model-specific outlier ("mom's cancer" prompt, roughly +10 points on Gemini 2.0 Flash). Implication: tips, threats and emotional appeals do not produce reliable gains on 2025 models; the per-question volatility they introduce is a reason to avoid them.

---

## 7. Negative instructions, constraints and instruction-following benchmarks

- **Zhou et al. (2023). "Instruction-Following Evaluation for Large Language Models" (IFEval). arXiv:2311.07911.** https://arxiv.org/abs/2311.07911
  Method: 541 prompts containing 25 types of programmatically verifiable instructions (word counts, "no commas", "respond in JSON", end with a phrase, etc.) in 9 categories; strict and loose scoring at prompt and instruction level. Key numbers (Table 3): GPT-4 prompt-level strict 76.89%, instruction-level strict 83.57%, loose 79.30%/85.37%; PaLM 2 S 43.07%/55.76%/46.95%/59.11%. Implication: even GPT-4 missed roughly one in four prompts with verifiable constraints; stack fewer constraints per prompt and verify them mechanically.

- **Qin et al. (2024). "SysBench: Can Large Language Models Follow System Messages?" arXiv:2408.10943.** https://arxiv.org/abs/2408.10943
  Method: 500 hand-built system messages with six constraint types and multi-turn conversations; measures constraint violation, instruction misjudgement and multi-turn instability. Key finding: all three failure modes are common, and adherence to system-message constraints decays over turns (per-model numbers figure not verified). Implication: constraints placed only in the system prompt erode across a long conversation and may need restating.

- **Truong et al. (2023). "Language models are not naysayers: An analysis of language models on negation benchmarks." *SEM 2023. arXiv:2306.08189.** https://arxiv.org/abs/2306.08189 ; https://aclanthology.org/2023.starsem-1.10/
  Method: GPT-Neo, GPT-3 and InstructGPT across negation benchmarks and prompt variants. Key finding: LLMs are frequently insensitive to the presence of negation, fail to capture its lexical semantics, and fail to reason under it. Implication: "do not X" is parsed less reliably than "do Y"; prefer positive phrasing of the desired behaviour.

- **Rana (2026). "Semantic Gravity Wells: Why Negative Constraints Backfire." arXiv:2601.08070.** https://arxiv.org/abs/2601.08070
  Method: mechanistic study of "do not use word X" constraints over 40,000 samples; defines semantic pressure (the model's prior probability of the forbidden token). Key numbers: violation probability follows p = sigma(-2.40 + 2.27 * P0); 87.5% of violations are "priming failures" where naming the forbidden word activates it; suppression signals are 4.4x weaker in failures than in successes. Implication: naming what to avoid primes the model to produce it; when a forbidden term is already likely, describe the target behaviour instead of the banned one.

- **Yang et al. (2025). "What Prompts Don't Say: Understanding and Managing Underspecification in LLM Prompts." arXiv:2505.13360.** https://arxiv.org/abs/2505.13360
  Key numbers: LLMs infer unstated requirements only 41.1% of the time; under-specified prompts are about 2x as likely to regress across model or prompt changes; accuracy can drop by more than 20% when a requirement is left implicit; a requirements-aware optimiser gains 4.8% on average. Implication: unstated constraints are the main source of silent regressions; write them down, then check them.

---

## 8. Automatic prompt optimisation

- **Zhou et al. (2022). "Large Language Models Are Human-Level Prompt Engineers" (APE). ICLR 2023. arXiv:2211.01910.** https://arxiv.org/abs/2211.01910
  Method: an LLM proposes candidate instructions from input-output pairs; candidates are scored on a held-out set and the best retained. Key numbers: APE instructions match or beat human-written ones on 19/24 Instruction Induction tasks; the discovered zero-shot CoT prompt "Let's work this out in a step by step way to be sure we have the right answer" scores 82.0% on MultiArith and 43.0% on GSM8K vs 78.7% and 40.7% for "Let's think step by step". Claim: machine-written prompts are human-level. Implication: small wording changes to a CoT trigger produce measurable, search-discoverable gains.

- **Yang et al. (2023). "Large Language Models as Optimizers" (OPRO). ICLR 2024. arXiv:2309.03409.** https://arxiv.org/abs/2309.03409
  Method: the optimiser LLM sees previous prompts with their scores and proposes better ones. Key numbers (Table 1, PaLM 2-L scorer): "Take a deep breath and work on this problem step-by-step" 80.2% on GSM8K vs 71.8% for "Let's think step by step" and 34.0% for no instruction; up to +8% over human prompts on GSM8K and up to +50% on Big-Bench Hard tasks. Implication: the best instruction wording is model-specific and non-obvious; treat it as a parameter to search, not a phrase to remember.

- **Khattab et al. (2023). "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines." ICLR 2024. arXiv:2310.03714.** https://arxiv.org/abs/2310.03714
  Method: declare modules and a metric; a "teleprompter" bootstraps demonstrations and instructions automatically. Key numbers (abstract): compiled pipelines let GPT-3.5 and llama2-13b-chat beat standard few-shot prompting by over 25% and 65% respectively, and beat pipelines with expert-created demonstrations by 5-46% and 16-40%; GSM8K accuracy moves from 4-20% to 49-88% depending on model. Implication: bootstrapped demonstrations from a metric reliably beat expert-written examples; hand-writing few-shot examples is rarely the best use of time when a metric exists.

- **Suzgun & Kalai (2024). "Meta-Prompting: Enhancing Language Models with Task-Agnostic Scaffolding." arXiv:2401.12954.** https://arxiv.org/abs/2401.12954
  Method: one "conductor" LM decomposes the task and spawns fresh "expert" instances of the same model with tailored instructions, then verifies and integrates. Key numbers (GPT-4, with Python interpreter, on Game of 24, Checkmate-in-One and Python Programming Puzzles): +17.1% over standard prompting, +17.3% over expert (dynamic) prompting, +15.2% over multipersona prompting. Implication: a task-agnostic scaffold that lets the model write its own sub-prompts outperforms hand-crafted expert prompts on these puzzle tasks.

- **Fernando et al. (2023). "Promptbreeder: Self-Referential Self-Improvement via Prompt Evolution." arXiv:2309.16797.** https://arxiv.org/abs/2309.16797
  Method: evolutionary search over task-prompts where the mutation-prompts themselves also evolve; population 50, 20-30 generations. Key numbers (PaLM 2-L, zero-shot): GSM8K 83.9% vs 59.3% for Plan-and-Solve+; SVAMP 90.2% vs 75.7%; AQuA-RAT 62.2% vs 46.0%. Implication: evolved prompts beat the best published hand-written reasoning prompts on the same model, again showing that human prompt wording is far from optimal.

- **Yuksekgonul et al. (2024). "TextGrad: Automatic 'Differentiation' via Text." arXiv:2406.07496 (later published in Nature, 2025).** https://arxiv.org/abs/2406.07496
  Method: LLM-generated textual critiques are back-propagated through a compound system to edit prompts, code or solutions. Key numbers (abstract): GPT-4o zero-shot GPQA 51% -> 55%; 20% relative gain on LeetCode-Hard. Implication: iterative critique-and-edit loops can improve prompts and outputs without labelled data, but gains on hard QA are a few points, not the 50% seen on narrow BBH tasks.

- Cross-cutting note: **Zhang et al. (2024). "Revisiting OPRO: The Limitations of Small-Scale LLMs as Optimizers." arXiv:2405.10276** reports that OPRO-style optimisation fails when the optimiser model is small (figure not verified). Implication: machine-written-beats-human claims hold when a strong model does the writing and a reliable metric does the scoring.

---

## 9. Clarifying questions and ambiguity resolution

- **Zhang & Choi (2023). "Clarify When Necessary: Resolving Ambiguity Through Interaction with LMs." arXiv:2311.09469.** https://arxiv.org/abs/2311.09469
  Method: three sub-tasks (when to ask, what to ask, how to use the answer); introduces intent-sim, which estimates entropy over plausible user intents to decide whether asking is worthwhile. Key finding: intent-sim consistently beats existing uncertainty estimators at identifying predictions that benefit from clarification on QA, MT and NLI (numeric gains figure not verified). Implication: asking should be gated on estimated intent ambiguity, not asked by default.

- **Mu et al. (2023). "ClarifyGPT: Empowering LLM-based Code Generation with Intention Clarification." arXiv:2310.10996.** https://arxiv.org/abs/2310.10996
  Method: detect ambiguity via a code-consistency check (sample several solutions; disagreement implies ambiguity), then ask targeted questions and regenerate. Key numbers: GPT-4 Pass@1 on MBPP-sanitized 70.96% -> 80.80%; average over four benchmarks 68.02% -> 75.75% (GPT-4) and 58.55% -> 67.22% (ChatGPT). Implication: for code, one round of clarification is worth roughly 8-10 Pass@1 points.

- **Wang et al. (2024). "Learning to Ask: When LLM Agents Meet Unclear Instruction." EMNLP 2025. arXiv:2409.00557.** https://arxiv.org/abs/2409.00557
  Method: NoisyToolBench of real, under-specified tool-use instructions; Ask-when-Needed (AwN) prompting makes the agent ask instead of hallucinating missing arguments; ToolEvaluator scores accuracy and interaction cost. Key finding: LLMs tend to fabricate missing arguments; AwN significantly outperforms existing tool-use frameworks (numbers figure not verified). Implication: agents should be prompted to stop and ask when a required argument is absent.

- **Vijayvargiya, Zhou, Yerukola, Sap & Neubig (2025). "Ambig-SWE: Interactive Agents to Overcome Underspecificity in Software Engineering." ICLR 2026. arXiv:2502.13069.** https://arxiv.org/abs/2502.13069
  Method: an underspecified variant of SWE-Bench Verified; agents may query a simulated user. Key numbers: interaction improves performance by up to 74% over non-interactive settings on underspecified tasks, but models struggle to tell well-specified from underspecified issues. Implication: the bottleneck is detecting ambiguity, not exploiting the answer; prompts that explicitly instruct "ask before acting if X is unspecified" close much of the gap.

- 2025-2026 follow-ups (existence verified, figures not verified): ClarEval (arXiv:2603.00187) and ClarifyCodeBench (arXiv:2607.00711) benchmark clarification skills of code agents; "Structured Uncertainty guided Clarification for LLM Agents" (arXiv:2511.08798) and "Uncertainty-Aware Clarification in LLM Agents with Information Gain" (arXiv:2606.03135) gate questions on structured uncertainty; CaRT (arXiv:2510.08517) trains agents to know when they have enough information. Implication: the field has converged on "ask only when uncertainty is high" as the target behaviour.

---

## 10. Few-shot prompting: how many, which order, what matters

- **Min et al. (2022). "Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?" EMNLP 2022. arXiv:2202.12837.** https://arxiv.org/abs/2202.12837
  Method: replace gold labels in demonstrations with random labels across 12 models including GPT-3. Key finding: random labels barely hurt classification and multiple-choice accuracy; what matters is exposure to the label space, the input distribution and the output format. Implication: demonstrations mostly teach format and domain, so a few well-formatted examples beat many carefully labelled ones.

- **Lu et al. (2022). "Fantastically Ordered Prompts and Where to Find Them: Overcoming Few-Shot Prompt Order Sensitivity." ACL 2022. arXiv:2104.08786.** https://arxiv.org/abs/2104.08786
  Key finding: reordering the same examples can move a model between near state-of-the-art and near random; good orders do not transfer across models; an entropy-based probing method gives a 13% relative improvement on average across 11 classification tasks. Implication: example order is a hidden hyperparameter; randomise or select it, and do not assume an order tuned on one model works on another.

- **Zhao et al. (2021). "Calibrate Before Use: Improving Few-Shot Performance of Language Models." ICML 2021. arXiv:2102.09690.** https://arxiv.org/abs/2102.09690
  Key finding: majority-label bias, recency bias (answers near the end of the prompt) and common-token bias explain much of few-shot instability; contextual calibration with a content-free input improves accuracy by up to 30.0 absolute points and reduces variance. Implication: balance label frequency in examples and put no systematic pattern in the last example.

- **Agarwal et al. (2024). "Many-Shot In-Context Learning." NeurIPS 2024. arXiv:2404.11018.** https://arxiv.org/abs/2404.11018
  Key finding (Gemini 1.5 Pro, up to 1M tokens): moving from few-shot to hundreds or thousands of shots yields significant gains across generative and discriminative tasks; model-generated rationales (Reinforced ICL) or even inputs alone (Unsupervised ICL) work in the many-shot regime. Implication: with long-context models the answer to "how many examples" shifts from "a handful" to "as many as the budget allows", subject to the position effects in Section 12.

- Related caveat from the reasoning-model literature: DeepSeek-R1's report (Section 11) and Cheng & Mastropaolo (Section 12) both find few-shot examples can degrade output for reasoning models and larger code models.

---

## 11. Does prompt engineering still matter for reasoning models and coding agents? (2025-2026)

- **Meincke, Mollick, Mollick & Shapiro (2025). "Prompting Science Report 2: The Decreasing Value of Chain of Thought in Prompting." Wharton Generative AI Labs. arXiv:2506.07142.** https://arxiv.org/abs/2506.07142 ; https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/
  Method: GPQA Diamond, each question 25 times per condition, with and without an explicit CoT instruction, on non-reasoning and reasoning models. Key numbers: reasoning models gain little (o3-mini +2.9%, o4-mini +3.1% on average); Gemini 2.5 Flash loses 13.1 and 7.1 points at the 100% and 90% correctness thresholds; CoT adds 20-80% more latency. Implication: for models that reason internally, an explicit "think step by step" is mostly cost with negligible or negative benefit.

- **Liu et al. (2024). "Mind Your Step (by Step): Chain-of-Thought can Reduce Performance on Tasks where Thinking Makes Humans Worse." arXiv:2410.21333.** https://arxiv.org/abs/2410.21333
  Method: six tasks from cognitive psychology where deliberation hurts humans (implicit statistical learning, face recognition, exception-laden classification, etc.). Key numbers: in three of six tasks CoT causes large drops, up to 36.3 absolute points for o1-preview relative to GPT-4o. Implication: CoT is a task-dependent choice; for pattern-recognition and implicit-learning tasks, ask for the answer directly.

- **DeepSeek-AI (2025). "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning." arXiv:2501.12948.** https://arxiv.org/abs/2501.12948
  Key finding (prompt-engineering section): R1 is prompt-sensitive; few-shot prompting consistently degrades its performance; the authors recommend describing the problem directly and specifying the output format zero-shot. Implication: for RL-trained reasoning models, remove exemplars and reasoning instructions and keep the task statement and output spec.

- **OpenAI. "Reasoning best practices" (developer documentation, 2025).** https://developers.openai.com/api/docs/guides/reasoning-best-practices
  Guidance: keep prompts simple and direct; avoid CoT instructions because the model reasons internally; use delimiters; limit extra context in RAG; give specific guidelines and describe the end goal. Implication: vendor guidance converges with the empirical findings above: for o-series models, specification beats scaffolding.

- **Cheng & Mastropaolo (2026). "An Empirical Study on the Effects of System Prompts in Instruction-Tuned Models for Code Generation." arXiv:2602.15228.** https://arxiv.org/abs/2602.15228
  Method: 360 configurations (4 models x 5 system prompts of increasing specificity x 3 prompting strategies x 2 languages x 2 temperatures). Key findings: more specific system prompts do not monotonically improve correctness; for larger code-specialised models few-shot examples can hurt relative to zero-shot; Java is far more sensitive to system-prompt changes than Python. Implication: system-prompt detail should be tuned per model and language, and defaults copied from other setups can lower correctness.

- **Gloaguen, Mündler, Müller, Raychev & Vechev (2026). "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" arXiv:2602.11988.** https://arxiv.org/abs/2602.11988
  Method: SWE-bench tasks plus real repository issues with developer-committed context files, across several agents. Key numbers: context files do not generally improve task success and raise inference cost by over 20% on average; repository overviews are ineffective; explicit instructions are followed but do not lift success; files help when they specify non-standard practices. Related: **"On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents" (arXiv:2601.20404)** reports 29% lower median runtime and 17% fewer output tokens when AGENTS.md is present (figure not verified); **Jiang & Nam (2025). "Beyond the Prompt: An Empirical Study of Cursor Rules." arXiv:2512.18925** and **"Agent READMEs" (arXiv:2511.12884**, 2,303 context files from 1,925 repositories) characterise what developers actually write (tests 75.9%, implementation 70.8%, architecture 68.1%, security 14.8%). Implication: for coding agents, the persistent prompt should state only what the agent cannot infer from the repo (conventions, commands, non-standard rules); generic overviews add cost without benefit.

- **"How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions" (2026). arXiv:2605.29442.** https://arxiv.org/abs/2605.29442
  Key finding: across 11,579 Cursor/Copilot IDE sessions in 1,300 repositories, developers rarely specify tasks fully upfront and instead refine progressively while managing agent behaviour (quantitative failure rates figure not verified). Implication: agent prompts are conversations, not one-shot specs; design the initial prompt to invite refinement and clarification.

---

## 12. System vs user prompt placement and instruction position in long context

- Base results carried over from earlier sections: Liu et al. (2023) U-shape (Section 5); Mao et al. (2023) showing common instruction positions are sub-optimal (Section 5); SysBench showing system-message constraints decay over turns (Section 7); Cheng & Mastropaolo (2026) showing system-prompt specificity is non-monotonic for code (Section 11).

- **Anthropic. "Long context prompting tips" (Claude developer documentation).** https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips
  Guidance: put long documents (about 20K+ tokens) at the top and the query/instructions at the end; Anthropic reports that placing the query at the end improved response quality by up to 30% in internal tests with complex multi-document inputs (vendor-reported, methodology not published). Also: wrap documents in XML tags and ask for grounding quotes first. Implication: with large inputs, the instruction goes last; with short inputs the effect is smaller and position can be tested.

- **Wu et al. (2024). "LIFBench: Evaluating the Instruction Following Performance and Stability of Large Language Models in Long-Context Scenarios." ACL 2025. arXiv:2411.07037.** https://arxiv.org/abs/2411.07037
  Method: 2,766 instructions over three long-context scenarios and 11 tasks, 20 models, six length intervals from 4K to 128K, instruction always placed at the end. Key numbers: most models decline significantly beyond 16K-32K tokens; GPT-4o is the most stable (overall 0.758); Llama-3.1-70B-Instruct drops sharply; the "recognition" capability degrades fastest. Implication: instruction following, not just retrieval, degrades with length; shorten context or restate instructions near the end.

- **IHEval (2025). "Evaluating Language Models on Following the Instruction Hierarchy." arXiv:2502.08745.** https://arxiv.org/abs/2502.08745
  Key finding: models frequently fail to prioritise system-prompt instructions over conflicting user-turn instructions, especially when the conflict is subtle (numbers figure not verified). Implication: do not rely on the system prompt "winning" a conflict; make user-turn instructions consistent with it or restate the priority explicitly.

- Practitioner synthesis: no controlled study found in this review isolates "same text in system slot vs user slot" on modern chat models with published effect sizes; the closest evidence (SysBench, IHEval, Cheng & Mastropaolo) shows system-prompt instructions are followed imperfectly and decay over turns, while long-context work shows end-of-prompt placement of the task instruction is safest.

---

## Cross-topic conclusions for prompt writers

1. Structure beats phrasing: reasoning scaffolds, tool interleaving and feedback loops give the largest replicated gains (Sections 1, 8), but shrink or invert on 2025 reasoning models (Section 11).
2. Phrasing tricks (personas, politeness, tips, threats, emotion) are inconsistent and model-specific, and mostly vanish on aggregate (Sections 3, 5, 6).
3. Formatting and position are large uncontrolled variance sources (up to 76 points, Sclar; up to 40%, He; U-shape, Liu); hold them fixed or sample over them when comparing prompts.
4. Negative and under-specified instructions fail predictably (Section 7); positive, explicit, checkable requirements are the safe default.
5. Machine-optimised prompts beat human ones whenever a metric exists (Section 8); treat wording as a searchable parameter.
6. Clarifying questions on detected ambiguity give some of the largest single-intervention gains for agents (Section 9); detection, not exploitation, is the hard part.

---

## Consolidated bibliography

Format: Authors (Year). Title. Venue. arXiv ID. URL.

1. Agarwal, R., Singh, A., Zhang, L. M., et al. (2024). Many-Shot In-Context Learning. NeurIPS 2024. arXiv:2404.11018. https://arxiv.org/abs/2404.11018
2. Anthropic (2024-2025). Long context prompting tips. Claude developer documentation. https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips
3. Basil, S., Shapiro, I., Shapiro, D., Mollick, E., Mollick, L., & Meincke, L. (2025). Playing Pretend: Expert Personas Don't Improve Factual Accuracy. Wharton Generative AI Labs technical report. https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/
4. Bsharat, S. M., Myrzakhan, A., & Shen, Z. (2023). Principled Instructions Are All You Need for Questioning LLaMA-1/2, GPT-3.5/4. arXiv:2312.16171. https://arxiv.org/abs/2312.16171
5. Cheng, Z., & Mastropaolo, A. (2026). An Empirical Study on the Effects of System Prompts in Instruction-Tuned Models for Code Generation. arXiv:2602.15228. https://arxiv.org/abs/2602.15228
6. DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning. arXiv:2501.12948. https://arxiv.org/abs/2501.12948
7. Dobariya, O., & Kumar, A. (2025). Mind Your Tone: Investigating How Prompt Politeness Affects LLM Accuracy (short paper). arXiv:2510.04950. https://arxiv.org/abs/2510.04950
8. Dobariya, O., & Kumar, A. (2026). Mind Your Tone: Does Tone Alter LLM Performance? AMCIS 2026. arXiv:2605.29027. https://arxiv.org/abs/2605.29027
9. Fernando, C., Banarse, D., Michalewski, H., Osindero, S., & Rocktäschel, T. (2023). Promptbreeder: Self-Referential Self-Improvement via Prompt Evolution. arXiv:2309.16797. https://arxiv.org/abs/2309.16797
10. Gloaguen, T., Mündler, N., Müller, M., Raychev, V., & Vechev, M. (2026). Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? arXiv:2602.11988. https://arxiv.org/abs/2602.11988
11. He, J., Rungta, M., Koleczek, D., Sekhon, A., Wang, F. X., & Hasan, S. (2024). Does Prompt Formatting Have Any Impact on LLM Performance? arXiv:2411.10541. https://arxiv.org/abs/2411.10541
12. IHEval authors (2025). IHEval: Evaluating Language Models on Following the Instruction Hierarchy. arXiv:2502.08745. https://arxiv.org/abs/2502.08745
13. Jiang, S., & Nam, D. (2025). Beyond the Prompt: An Empirical Study of Cursor Rules. arXiv:2512.18925. https://arxiv.org/abs/2512.18925
14. Khattab, O., Singhvi, A., Maheshwari, P., et al. (2023). DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines. ICLR 2024. arXiv:2310.03714. https://arxiv.org/abs/2310.03714
15. Kim, J., Yang, N., & Jung, K. (2024). Persona is a Double-edged Sword: Mitigating the Negative Impact of Role-playing Prompts in Zero-shot Reasoning Tasks. arXiv:2408.08631. https://arxiv.org/abs/2408.08631
16. Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large Language Models are Zero-Shot Reasoners. NeurIPS 2022. arXiv:2205.11916. https://arxiv.org/abs/2205.11916
17. Kong, A., Zhao, S., Chen, H., Li, Q., Qin, Y., Sun, R., & Zhou, X. (2023). Better Zero-Shot Reasoning with Role-Play Prompting. NAACL 2024. arXiv:2308.07702. https://arxiv.org/abs/2308.07702
18. Li, C., Wang, J., Zhang, Y., et al. (2023). Large Language Models Understand and Can be Enhanced by Emotional Stimuli. arXiv:2307.11760. https://arxiv.org/abs/2307.11760
19. Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). Lost in the Middle: How Language Models Use Long Contexts. TACL 2024. arXiv:2307.03172. https://arxiv.org/abs/2307.03172
20. Liu, R., Geng, J., Wu, A. J., Sucholutsky, I., Lombrozo, T., & Griffiths, T. L. (2024). Mind Your Step (by Step): Chain-of-Thought can Reduce Performance on Tasks where Thinking Makes Humans Worse. arXiv:2410.21333. https://arxiv.org/abs/2410.21333
21. Lu, Y., Bartolo, M., Moore, A., Riedel, S., & Stenetorp, P. (2022). Fantastically Ordered Prompts and Where to Find Them: Overcoming Few-Shot Prompt Order Sensitivity. ACL 2022. arXiv:2104.08786. https://arxiv.org/abs/2104.08786
22. Mao, J., Middleton, S. E., & Niranjan, M. (2023). Do prompt positions really matter? Findings of NAACL 2024. arXiv:2305.14493. https://arxiv.org/abs/2305.14493
23. Meincke, L., Mollick, E. R., Mollick, L., & Shapiro, D. (2025a). Prompting Science Report 1: Prompt Engineering is Complicated and Contingent. arXiv:2503.04818. https://arxiv.org/abs/2503.04818
24. Meincke, L., Mollick, E. R., Mollick, L., & Shapiro, D. (2025b). Prompting Science Report 2: The Decreasing Value of Chain of Thought in Prompting. arXiv:2506.07142. https://arxiv.org/abs/2506.07142
25. Meincke, L., Mollick, E. R., Mollick, L., & Shapiro, D. (2025c). I'll pay you or I'll kill you - but will you care? Wharton Generative AI Labs technical report. https://gail.wharton.upenn.edu/research-and-insights/techreport-threaten-or-tip/
26. Min, S., Lyu, X., Holtzman, A., Artetxe, M., Lewis, M., Hajishirzi, H., & Zettlemoyer, L. (2022). Rethinking the Role of Demonstrations: What Makes In-Context Learning Work? EMNLP 2022. arXiv:2202.12837. https://arxiv.org/abs/2202.12837
27. Mu, F., Shi, L., Wang, S., Yu, Z., Zhang, B., Wang, C., Liu, S., & Wang, Q. (2023). ClarifyGPT: Empowering LLM-based Code Generation with Intention Clarification. arXiv:2310.10996. https://arxiv.org/abs/2310.10996
28. OpenAI (2025). Reasoning best practices. OpenAI developer documentation. https://developers.openai.com/api/docs/guides/reasoning-best-practices
29. Qin, Y., Zhang, T., et al. (2024). SysBench: Can Large Language Models Follow System Messages? arXiv:2408.10943. https://arxiv.org/abs/2408.10943
30. Rana, S. (2026). Semantic Gravity Wells: Why Negative Constraints Backfire. arXiv:2601.08070. https://arxiv.org/abs/2601.08070
31. Schulhoff, S., Ilie, M., Balepur, N., et al. (2024). The Prompt Report: A Systematic Survey of Prompt Engineering Techniques. arXiv:2406.06608. https://arxiv.org/abs/2406.06608
32. Sclar, M., Choi, Y., Tsvetkov, Y., & Suhr, A. (2023). Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting. ICLR 2024. arXiv:2310.11324. https://arxiv.org/abs/2310.11324
33. Shinn, N., Cassano, F., Berman, E., Gopinath, A., Narasimhan, K., & Yao, S. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning. NeurIPS 2023. arXiv:2303.11366. https://arxiv.org/abs/2303.11366
34. Sprague, Z., Yin, F., Rodriguez, J. D., et al. (2024). To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning. ICLR 2025. arXiv:2409.12183. https://arxiv.org/abs/2409.12183
35. Suzgun, M., & Kalai, A. T. (2024). Meta-Prompting: Enhancing Language Models with Task-Agnostic Scaffolding. arXiv:2401.12954. https://arxiv.org/abs/2401.12954
36. Truong, T. H., Baldwin, T., Verspoor, K., & Cohn, T. (2023). Language models are not naysayers: An analysis of language models on negation benchmarks. *SEM 2023. arXiv:2306.08189. https://arxiv.org/abs/2306.08189
37. Vijayvargiya, S., Zhou, X., Yerukola, A., Sap, M., & Neubig, G. (2025). Ambig-SWE: Interactive Agents to Overcome Underspecificity in Software Engineering. ICLR 2026. arXiv:2502.13069. https://arxiv.org/abs/2502.13069
38. Wang, W., et al. (2024). Learning to Ask: When LLM Agents Meet Unclear Instruction. EMNLP 2025. arXiv:2409.00557. https://arxiv.org/abs/2409.00557
39. Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., & Zhou, D. (2022). Self-Consistency Improves Chain of Thought Reasoning in Language Models. ICLR 2023. arXiv:2203.11171. https://arxiv.org/abs/2203.11171
40. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., & Zhou, D. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. NeurIPS 2022. arXiv:2201.11903. https://arxiv.org/abs/2201.11903
41. Wu, X., et al. (2024). LIFBench: Evaluating the Instruction Following Performance and Stability of Large Language Models in Long-Context Scenarios. ACL 2025. arXiv:2411.07037. https://arxiv.org/abs/2411.07037
42. Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q. V., Zhou, D., & Chen, X. (2023). Large Language Models as Optimizers. ICLR 2024. arXiv:2309.03409. https://arxiv.org/abs/2309.03409
43. Yang, C., Shi, Y., Ma, Q., Liu, M. X., Kästner, C., & Wu, T. (2025). What Prompts Don't Say: Understanding and Managing Underspecification in LLM Prompts. arXiv:2505.13360. https://arxiv.org/abs/2505.13360
44. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR 2023. arXiv:2210.03629. https://arxiv.org/abs/2210.03629
45. Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao, Y., & Narasimhan, K. (2023). Tree of Thoughts: Deliberate Problem Solving with Large Language Models. NeurIPS 2023. arXiv:2305.10601. https://arxiv.org/abs/2305.10601
46. Yin, Z., et al. (2024). Should We Respect LLMs? A Cross-Lingual Study on the Influence of Prompt Politeness on LLM Performance. SICon 2024. arXiv:2402.14531. https://arxiv.org/abs/2402.14531
47. Yuksekgonul, M., Bianchi, F., Boen, J., Liu, S., Huang, Z., Guestrin, C., & Zou, J. (2024). TextGrad: Automatic "Differentiation" via Text. arXiv:2406.07496. https://arxiv.org/abs/2406.07496
48. Zhang, M. J. Q., & Choi, E. (2023). Clarify When Necessary: Resolving Ambiguity Through Interaction with LMs. arXiv:2311.09469. https://arxiv.org/abs/2311.09469
49. Zhao, T. Z., Wallace, E., Feng, S., Klein, D., & Singh, S. (2021). Calibrate Before Use: Improving Few-Shot Performance of Language Models. ICML 2021. arXiv:2102.09690. https://arxiv.org/abs/2102.09690
50. Zheng, M., Pei, J., Logeswaran, L., Lee, M., & Jurgens, D. (2023). When "A Helpful Assistant" Is Not Really Helpful: Personas in System Prompts Do Not Improve Performances of Large Language Models. Findings of EMNLP 2024. arXiv:2311.10054. https://arxiv.org/abs/2311.10054
51. Zhou, J., Lu, T., Mishra, S., Brahma, S., Basu, S., Luan, Y., Zhou, D., & Hou, L. (2023). Instruction-Following Evaluation for Large Language Models. arXiv:2311.07911. https://arxiv.org/abs/2311.07911
52. Zhou, Y., Muresanu, A. I., Han, Z., Paster, K., Pitis, S., Chan, H., & Ba, J. (2022). Large Language Models Are Human-Level Prompt Engineers. ICLR 2023. arXiv:2211.01910. https://arxiv.org/abs/2211.01910

Additional 2025-2026 items cited for existence only (figures not verified): ClarEval arXiv:2603.00187; ClarifyCodeBench arXiv:2607.00711; Structured Uncertainty guided Clarification arXiv:2511.08798; Uncertainty-Aware Clarification with Information Gain arXiv:2606.03135; CaRT arXiv:2510.08517; Agent READMEs arXiv:2511.12884; On the Impact of AGENTS.md Files arXiv:2601.20404; How Coding Agents Fail Their Users arXiv:2605.29442; Revisiting OPRO arXiv:2405.10276.
