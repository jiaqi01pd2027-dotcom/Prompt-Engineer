# code-2: Debug a short Python snippet (coding)

## Hidden rubric (never shown to the model under test)

Situation the prompt-writer knows: the snippet contains exactly two real bugs and one
deliberate red herring.

Bug 1 (mutable default argument), `tag_records`: `tags=[]` is created once at function
definition time and `tags.append("processed")` mutates it, so every call that relies on
the default accumulates another "processed" (the demo's second default call prints
`['processed', 'processed']`), and callers that pass their own list get it mutated too.
Correct fix: `tags=None`, then build a new list (`tags = list(tags) if tags else []`)
before appending.

Bug 2 (off-by-one in a range), `moving_average`: `range(len(values) - window)` drops the
final window. For `[1, 2, 3, 4]` with window 2 it returns `[1.5, 2.5]` instead of
`[1.5, 2.5, 3.5]`. Correct fix: `range(len(values) - window + 1)`.

Red herring (NOT a bug), `number_lines`: `enumerate(lines, start=1)` is intentional; the
docstring asks for 1-based numbering and the output `'1: alpha'` is correct. Changing it
to `start=0` or removing `start` is a regression.

Score signals (each 0-2, judge totals to 10 then normalises):
- BUG1: identifies the mutable default in `tag_records` and explains that the list is shared across calls (2 = found and correctly explained, 1 = found but explanation wrong or vague, 0 = missed).
- BUG2: identifies the off-by-one in `moving_average` and gives the `+ 1` (or equivalent) fix (2 = found and fixed, 1 = found but fix wrong, 0 = missed).
- HERRING: leaves `number_lines` unchanged and, if it mentions it at all, says it is correct (2 = untouched or explicitly cleared, 1 = flagged as suspicious but not changed, 0 = "fixed").
- CODE: provides the full corrected snippet that runs and matches the expected outputs below (2 = all three checks pass, 1 = two, 0 = fewer).
- FORM: no invented bugs (style nits, "add type hints", "add error handling" are not bugs), explanations are one to three sentences each, nothing else.

Expected outputs of the corrected code:
- `tag_records([{"id": 1}])` called twice in a row returns `[{'id': 1, 'tags': ['processed']}]` both times.
- `caller = ["urgent"]; tag_records([{"id": 1}], caller); caller == ["urgent"]` is True.
- `moving_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]`.
- `number_lines(["alpha", "beta"]) == ["1: alpha", "2: beta"]`.

Objective checks: the runner extracts the last fenced Python block and runs the four
expectations above; also greps the prose for "mutable default" (or "default argument")
and "off-by-one" (or "off by one" / "range"); fails the HERRING check if the extracted
code contains `enumerate(lines)` or `start=0`.

## Shared material (appears verbatim in every variant where the prompt refers to it)

<code>
def tag_records(records, tags=[]):
    """Attach `tags` plus a 'processed' marker to every record."""
    tags.append("processed")
    return [dict(record, tags=list(tags)) for record in records]


def moving_average(values, window):
    """Return the average of every consecutive `window`-sized slice."""
    averages = []
    for start in range(len(values) - window):
        chunk = values[start:start + window]
        averages.append(sum(chunk) / window)
    return averages


def number_lines(lines):
    """Prefix each line with its 1-based line number, e.g. '1: first'."""
    return [f"{index}: {line}" for index, line in enumerate(lines, start=1)]


if __name__ == "__main__":
    print(tag_records([{"id": 1}]))
    print(tag_records([{"id": 2}]))
    print(moving_average([1, 2, 3, 4], 2))
    print(number_lines(["alpha", "beta"]))
</code>

## Variants

### P0 bare
This code is broken, can you fix it?

<code>...</code>

### P1 specific
Find and fix the bugs in the Python snippet below. It contains two genuine bugs: for
each one, say which function it is in, explain why it is wrong, and show the corrected
code. Do not change anything that already works.

<code>...</code>

### P2 role
You are a senior Python reviewer who is known for precise, no-nonsense code reviews.
Find and fix the bugs in the Python snippet below. It contains two genuine bugs: for
each one, say which function it is in, explain why it is wrong, and show the corrected
code. Do not change anything that already works.

<code>...</code>

### P3 context
Find and fix the bugs in the Python snippet below. It contains two genuine bugs: for
each one, say which function it is in, explain why it is wrong, and show the corrected
code. Do not change anything that already works.

Background you should use: this module is part of a data-cleaning pipeline. Users
reported that records processed later in a batch pick up duplicate "processed" tags,
and that the moving average of a 4-item list with window 2 comes back with only two
values when the analyst expects three. The line-numbering helper feeds a diff viewer
whose lines are numbered from 1, matching how editors display them.

<code>...</code>

### P4 constraints
Find and fix the bugs in the Python snippet below. It contains two genuine bugs: for
each one, say which function it is in, explain why it is wrong, and show the corrected
code. Do not change anything that already works.

Constraints: report exactly two bugs, no more. Do not rewrite or restyle working code.
Do not add type hints, docstring changes, input validation, or new features. Do not
"fix" anything you cannot demonstrate is producing wrong output. Keep each explanation
to three sentences at most. Return the entire corrected snippet in one code block.

<code>...</code>

### P5 format
Find and fix the bugs in the Python snippet below. It contains two genuine bugs: for
each one, say which function it is in, explain why it is wrong, and show the corrected
code. Do not change anything that already works.

Output format: three sections with the headings "Bug 1", "Bug 2" and "Corrected code".
Under "Bug 1" and "Bug 2", exactly three lines:
Function: <name>
Problem: <one or two sentences>
Fix: <one sentence>
Under "Corrected code", one fenced ```python block with the full corrected snippet.
No other sections.

<code>...</code>

### P6 fewshot
Find and fix the bugs in the Python snippet below. It contains two genuine bugs: for
each one, say which function it is in, explain why it is wrong, and show the corrected
code. Do not change anything that already works.

Here are two review findings in the style we want:

<example>
Function: total_price
Problem: `for i in range(1, len(items))` skips the first item, so the total is missing
items[0].
Fix: iterate over `items` directly, or use `range(len(items))`.
</example>

<example>
Function: build_index
Problem: `cache={}` in the signature is a mutable default; the same dict is reused on
every call, so keys from earlier calls leak into later ones.
Fix: default to `None` and create a fresh dict inside the function.
</example>

<code>...</code>

### P7 cot
Find and fix the bugs in the Python snippet below. It contains two genuine bugs: for
each one, say which function it is in, explain why it is wrong, and show the corrected
code. Do not change anything that already works.

Before answering, think step by step: trace what each function returns for the inputs
in the `__main__` block, compare with what its docstring promises, and for anything that
looks suspicious decide whether it actually produces wrong output before calling it a
bug. Show your reasoning briefly, then give the final answer under a heading "Findings:".

<code>...</code>

### P8 fullstack
You are a senior Python reviewer who is known for precise, no-nonsense code reviews.

Goal: find and fix the bugs in the snippet below so the pipeline stops producing
duplicate tags and truncated moving averages, without touching anything that works.

Context: this module is part of a data-cleaning pipeline. Users reported that records
processed later in a batch pick up duplicate "processed" tags, and that the moving
average of a 4-item list with window 2 comes back with two values instead of three.
The line-numbering helper feeds a diff viewer whose lines are numbered from 1, matching
how editors display them.

Constraints: there are exactly two genuine bugs; report exactly two. Do not restyle
working code, add type hints, add validation, or change docstrings. Do not "fix"
anything you cannot show is producing wrong output. Three sentences maximum per
explanation.

Format: three sections headed "Bug 1", "Bug 2" and "Corrected code". The first two
each contain exactly the lines "Function:", "Problem:", "Fix:"; the third contains one
fenced ```python block with the full corrected snippet. No other sections.

<code>...</code>

### P9 interview
Find and fix the bugs in the Python snippet below. Before answering, ask me any
clarifying questions you need (expected behaviour, how the functions are called,
what counts as a bug). I have answered them below; use the answers.

<code>...</code>

Q: How many bugs should I expect? A: Exactly two. Anything beyond that is probably a
false positive.
Q: How is `tag_records` used? A: Called many times in a batch, usually without passing
`tags`. Later records are coming back with several "processed" entries.
Q: What should `moving_average([1, 2, 3, 4], 2)` return? A: Three values: 1.5, 2.5,
3.5. Right now we only get two.
Q: Is the 1-based numbering in `number_lines` intentional? A: Yes. It feeds a diff
viewer that numbers from 1. Leave it alone.
Q: Do you want style changes or type hints? A: No. Only the fixes, a short explanation
of each, and the full corrected snippet in one code block.
