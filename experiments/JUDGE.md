# Blind judge protocol

Input: experiments/judge/<task>/bundle.md. It contains the hidden rubric, the shared
material, and N outputs labelled O01..ONN in random order. You do not know which prompt
pattern or model produced any output, and you must not guess.

For EVERY output, score 0-10 on each dimension:
- correctness: factual/logical accuracy against the rubric and expected answers
- completeness: covers everything the rubric requires, nothing missing
- adherence: follows the explicit and implicit requirements of the task (length, format,
  banned phrases, sign-off, etc. as listed in the rubric)
- usefulness: could the requester use this as-is with no edits
- concision: no filler, no padding, no restating the task; length appropriate

Also record:
- objective: pass/fail of each "Objective checks" item in the rubric (as a dict)
- notes: one sentence on the single biggest strength or flaw

Rules:
- Score independently; do not curve. Two identical outputs get identical scores.
- Extra reasoning shown before a final answer is fine if the final answer is clearly
  marked; penalise concision only if the requester would have to cut it.
- An output that asks questions instead of answering, when the answers were already
  provided, scores low on completeness and usefulness.
- Do not reward length.

Write experiments/judge/<task>/scores.json as:
{"O01": {"correctness": 8, "completeness": 7, "adherence": 9, "usefulness": 8,
         "concision": 6, "objective": {"...": true}, "notes": "..."}, ...}
Then list your top 3 output ids in a "top3" key, and finish with a one-line summary.
