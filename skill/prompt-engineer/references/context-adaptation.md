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

### Subagent / delegated task
- Self-contained: the subagent has no conversation memory. Include every fact.
- Say what to return and in what shape (the parent reads it, not the user).
- Say what not to do (no edits, no commits, read-only) and a stop condition.

## Project-specific substitution checklist

When rewriting, replace every generic phrase with the project's own:
- "the codebase" -> the actual repo name and language
- "the tests" -> the actual command (`pytest -q`, `npm test`)
- "the style guide" -> the CLAUDE.md rule or a linked file
- "the user" -> the real audience from README or product docs
- "recent changes" -> the commit or branch name
- "a good example" -> a path to an existing example in the repo
