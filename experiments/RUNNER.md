# Runner protocol

For one task id T (e.g. write-1):

1. Prompts live in experiments/prompts/T/P0.txt ... P9.txt (already expanded).
2. For each model M in {fable, opus, sonnet} and each pattern P in P0..P9:
   - Read the prompt file.
   - Launch a subagent with the Agent tool: subagent_type "general-purpose", model M,
     prompt = the EXACT file contents and nothing else (no preamble, no mention of an
     experiment, no instruction to write files). The subagent's final message is the run
     output.
   - Save the subagent's final message verbatim to experiments/results/T/M/P.md
     (create directories). If the subagent produced files instead of text, append the
     file contents after the message under a line "--- files ---".
3. Run up to 10 subagents in parallel (one tool-call block with several Agent calls,
   run_in_background: false is fine when you need the result immediately; or launch in
   background and collect). Retry a run once if it errors; if it fails twice, write
   "ERROR: <reason>" in the file.
4. Do not edit, trim, or "clean up" outputs. Do not score them.
5. When done, write experiments/results/T/manifest.json listing every file with its
   word count, and reply with a one-line summary.

## Isolation (mandatory)

Subagents inherit the session's working directory. The runs must be launched from a
session whose working directory is an EMPTY sandbox, never from the project folder:
a first attempt from the project folder was contaminated because a subagent found the
task spec (with the hidden rubric) in experiments/ and read it. All harness paths in
the runner prompt are absolute. After a batch, run experiments/check_contamination.py
on the task; any output that mentions the experiment, a rubric, a fixture, or a
file path in the project is marked contaminated and re-run.
