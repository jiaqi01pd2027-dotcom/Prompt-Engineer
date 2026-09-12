# Adapting a prompt to the project it lives in

The rewrite that wins is the one that uses facts the user already has lying around.
Before grading, spend a minute collecting them. Only read; never modify.

## What to collect (in order, stop when you have enough)

1. **Where the prompt will run.** Ask or infer: Claude Code in this repo, claude.ai chat,
   an API system prompt, or a subagent. This changes the shape of the rewrite more than
   anything else (see "Targets" below).
2. **Project identity.** `CLAUDE.md`, `README.md`, `package.json` / `pyproject.toml` /
   `Cargo.toml` / `go.mod`, top-level directory listing. Note: language, framework,
   test command, lint command, naming conventions, and anything the CLAUDE.md forbids.
3. **Recent activity.** `git log --oneline -15`, `git status --short`, current branch.
   Recent commits tell you what "the feature" probably refers to.
4. **The thing the prompt points at.** If the prompt names a file, function, endpoint,
   doc, or dataset, open it and pull the exact identifiers, signatures, and sizes.
5. **Existing conventions for the deliverable.** If the user wants a test, look at an
   existing test; a doc, an existing doc; a commit message, `git log` style; an email,
   any prior email in the repo or notes. Quote one as a few-shot example in the rewrite.
6. **Verification available.** Test runner, type checker, build, preview server,
   screenshot tools. The rewrite should tell the model to use them.

If there is no project (scratch session, chat prompt), collect the same facts from the
user in the interview instead, but keep it to what changes the output.

## Targets

### Claude Code / agentic
- Lead with the goal and what "done" means (tests pass, page renders, PR opened).
- Name files and commands exactly; the model can read the rest itself, so say "read X
  first" rather than pasting X.
- Ask for a short plan first on anything touching more than two files; say whether to
  proceed without confirmation.
- Say how to verify and what not to touch (generated files, unrelated refactors).
- Prefer "when you are unsure between two readings, ask" over long defensive lists.
- Mention parallelism if independent (e.g. "run the three checks in parallel").

### claude.ai / chat
- Role + goal + context + constraints + format (the hierarchy). Paste the material the
  model cannot see, delimited with XML tags.
- Ask for the interview form when the user does not know what context matters:
  "ask me up to 5 questions, then write it".
- Give 1-3 examples of the wanted voice when style matters more than facts.

### API system prompt / reusable template
- Put stable identity, rules, and format in the system prompt; put the per-request
  material in the user turn.
- Turn the user's specifics into `{{variables}}` and list them.
- Add explicit output schema and one worked example; say what to do on bad input.
- Describe the why behind each rule (Claude generalises better from reasons).

### Writing (essay, article, letter, report), in chat or in a Cowork folder
- Collect, in this order, and stop when you have enough: the assignment or brief
  verbatim (the question asked, not a paraphrase); who reads or grades it and against
  what (rubric, word limit, format, deadline); the user's stance or thesis, or the two
  or three true things they want in it; sources or facts allowed, and whether anything
  may be invented (default: nothing); one sample of the user's own writing for voice;
  what to avoid and why (clichés, AI-sounding openers, a topic already covered).
- In a Cowork folder, look for: brief.*, assignment.*, prompt.*, rubric.*, any prior
  draft (v1, draft, old), feedback or comments files, style guides, notes, and sources.
  Quote the assignment question and the rubric lines into the rewrite; point at the
  sample by file name for voice ("match the voice of essays/2025-scholarship.docx").
- The rewrite states the deliverable as a file when in Cowork ("write it to
  drafts/essay-v2.md") and as a pasted text in chat. Say what the model must not do:
  invent quotes, statistics, or experiences; open with a definition or a rhetorical
  question; exceed the limit. Say the self-check: word count, rubric lines, no
  invented facts, read aloud once.
- Structure is a decision the user owns: if the brief gives sections, name them; if
  not, ask for an outline first (rewrite C) or supply the arc in one line.
- Role: use only for voice ("write as I would, a first-year student who is direct and
  a little dry"), never "you are an award-winning essayist".
- A prior draft the user wants replaced is a negative pointer ("not the openers of
  old-cover-letter.md"), not a voice sample; a voice sample is writing the user
  endorses. If the folder has none, describe the voice in five words and ask for one.
- If "sources" are the user's notes rather than the readings, say so in the rewrite
  and forbid quoting from them; leave `[add example from X]` markers instead.
- Name the draft format now (.md) and the final format the brief expects (.docx, PDF,
  a web form) so the conversion is a known follow-up, not a surprise.

### Subagent / delegated task
- Self-contained: the subagent has no conversation memory. Include every fact.
- Say what to return and in what shape (the parent reads it, not the user).
- Say what not to do (no edits, no commits, read-only) and a stop condition.

## Cowork specifics

Cowork sessions work in a folder, not a repo: there is no git log, tests, or CLAUDE.md
unless the user added one. Treat the folder listing as the manifest, the newest file
as "recent activity", and any file named like a brief, rubric, or notes as the
project's rules. Outputs are files, so every rewrite names the output path and format
(.md, .docx) and says whether to overwrite or create a new version. Interview with the
batched question tool as usual; if the tool is absent, a numbered list with defaults.

## Project-specific substitution checklist

When rewriting, replace every generic phrase with the project's own:
- "the codebase" -> the actual repo name and language
- "the tests" -> the actual command (`pytest -q`, `npm test`)
- "the style guide" -> the CLAUDE.md rule or a linked file
- "the user" -> the real audience from README or product docs
- "recent changes" -> the commit hash or branch name
- "a good example" -> a path to an existing example in the repo
- "the stubs", "the deps", "the handler" -> the function, package, or file by name
- "the repo" in a subagent brief -> the absolute path (the subagent has no cwd context)
- "my essay" -> the assignment question quoted, the grader, the limit, the file to write
- "my voice" -> the path or paste of one sample the model should match
