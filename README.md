# Prompt Engineer

A Claude Code skill, a website, and the research behind them, about how the wording of
a prompt changes what a model produces.

## The skill

`skill/prompt-engineer/` holds `/prompt-engineer`. Give it a rough draft and it reads
your project, grades the draft out of 100, asks the few questions the project cannot
answer, and gives three rewrites with the patterns named.

It works on code and agent prompts (Claude Code, API system prompts, subagent briefs)
and on writing (essays, articles, cover letters, reports), in chat or in a Cowork
document folder with a brief, a rubric, and past drafts.

Install:

```bash
git clone https://github.com/jiaqi01pd2027-dotcom/Prompt-Engineer.git
ln -s "$(pwd)/Prompt-Engineer/skill/prompt-engineer" ~/.claude/skills/prompt-engineer
```

Then, in any Claude Code or Cowork session: `/prompt-engineer fix the logout bug`, or
paste a prompt and ask for a grade.

## The evidence

`experiments/` holds 360 blind-judged runs: 12 tasks across six domains, each written
in 10 prompt patterns, each run on Fable 5.1, Opus 5, and Sonnet 5. A full-stack prompt
averaged 9.12 out of 10 against 5.46 for a bare command, and the ranking of patterns
was the same on all three models. Numbers are in `experiments/results/summary.md`.

The skill itself is tested the same way: eight drafts across three targets, each
recommended rewrite scored by an independent grader against the skill's own rubric.
Current mean 94 out of 100, every draft above 85.

## Layout

- `skill/prompt-engineer/` - `SKILL.md` plus four references: the rubric, the pattern
  catalogue with evidence, how to read a project or folder, and eight worked cases.
- `experiments/` - tasks, prompt variants, raw outputs, judge scores, aggregation.
- `paper/` - the write-up, in Markdown and PDF.
- `site/` - the website: pattern library, results, a live prompt grader.
- `research/` - literature and practitioner notes the paper draws on.

Author: Tiger Zhang.
