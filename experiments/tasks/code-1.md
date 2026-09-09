# code-1: Parse ISO-8601 durations (coding)

## Hidden rubric (never shown to the model under test)

Situation the prompt-writer knows: the function is for a billing service that stores
subscription intervals as ISO-8601 duration strings; the service only ever needs a
total number of seconds, and the team has agreed on fixed lengths of 365 days per year
and 30 days per month (calendar accuracy is not needed). Weeks appear on their own
(P2W) and never combine with other designators. Fractions are only ever allowed on the
seconds component. Anything malformed must raise ValueError so bad data never reaches
the database.

Expected behaviour (the runner imports the model's function as `parse_iso_duration`
and compares with `math.isclose(result, expected)`; int or float is accepted):

| # | input | expected |
|---|---|---|
| 1 | "P1Y2M3DT4H5M6S" | 36993906 |
| 2 | "P2W" | 1209600 |
| 3 | "PT1.5S" | 1.5 |
| 4 | "PT36H" | 129600 |
| 5 | "P1DT12H" | 129600 |
| 6 | "PT0S" | 0 |
| 7 | "P3M" | 7776000 |
| 8 | "1Y" | raises ValueError (no leading P) |
| 9 | "P" | raises ValueError (no components) |
| 10 | "P1S" | raises ValueError (time unit without T) |

Score signals (each 0-2, judge totals to 10 then normalises):
- CORRECT: passes tests 1-7 (2 = all pass, 1 = 5-6 pass, 0 = fewer).
- REJECT: raises ValueError, not another exception type, for tests 8-10 (2 = all three, 1 = two, 0 = fewer).
- CLEAN: single function with the exact name and signature, uses only the standard library, no input()/print() side effects, no global state.
- EXPLAIN: a short note of the assumptions made (year=365d, month=30d, weeks standalone, fractions only on seconds); no essay.
- FORM: code is in one fenced Python block; no unrelated helpers, CLI wrappers, or unit-test scaffolding beyond a few optional examples.

Objective checks: the runner extracts the first fenced Python block, imports it, runs
the 10 tests above; also checks `parse_iso_duration` is defined, that no third-party
import is present, and that tests 8-10 raise `ValueError` specifically.

## Shared material (appears verbatim in every variant where the prompt refers to it)

<spec>
Function name and signature: parse_iso_duration(s: str) -> float | int
Input examples that must work: "P1Y2M3DT4H5M6S", "P2W", "PT1.5S", "PT36H", "P1DT12H"
Unit lengths: 1 year = 365 days, 1 month = 30 days, 1 week = 7 days, 1 day = 24 hours.
Invalid input (no leading P, an empty "P", a time unit such as S or H without the T
separator, fractions anywhere except seconds, unknown characters) must raise ValueError.
</spec>

## Variants

### P0 bare
Write a Python function that turns an ISO duration string into seconds.

<spec>...</spec>

### P1 specific
Write a Python function `parse_iso_duration(s)` that converts an ISO-8601 duration
string into a total number of seconds. It must handle full strings like
"P1Y2M3DT4H5M6S", standalone weeks like "P2W", fractional seconds like "PT1.5S", and
any subset of components. Use 365 days per year and 30 days per month. Raise ValueError
for any string that is not a valid ISO-8601 duration.

<spec>...</spec>

### P2 role
You are a senior Python engineer who writes small, well-tested standard-library
utilities. Write a Python function `parse_iso_duration(s)` that converts an ISO-8601
duration string into a total number of seconds. It must handle full strings like
"P1Y2M3DT4H5M6S", standalone weeks like "P2W", fractional seconds like "PT1.5S", and
any subset of components. Use 365 days per year and 30 days per month. Raise ValueError
for any string that is not a valid ISO-8601 duration.

<spec>...</spec>

### P3 context
Write a Python function `parse_iso_duration(s)` that converts an ISO-8601 duration
string into a total number of seconds. It must handle full strings like
"P1Y2M3DT4H5M6S", standalone weeks like "P2W", fractional seconds like "PT1.5S", and
any subset of components. Use 365 days per year and 30 days per month. Raise ValueError
for any string that is not a valid ISO-8601 duration.

Background you should use: this runs inside a billing service that stores subscription
intervals as duration strings and only ever needs total seconds, so calendar-accurate
months and years are deliberately not required. Weeks always appear on their own and
never combine with other designators. Fractions only ever appear on the seconds
component. Malformed strings must fail loudly (ValueError) so bad data never reaches
the database; returning 0 or None for bad input is not acceptable.

<spec>...</spec>

### P4 constraints
Write a Python function `parse_iso_duration(s)` that converts an ISO-8601 duration
string into a total number of seconds. It must handle full strings like
"P1Y2M3DT4H5M6S", standalone weeks like "P2W", fractional seconds like "PT1.5S", and
any subset of components. Use 365 days per year and 30 days per month. Raise ValueError
for any string that is not a valid ISO-8601 duration.

Constraints: standard library only (no dateutil, no isodate). Exactly one function with
that exact name and signature; no classes, no CLI, no print statements. Do not accept
"P" or "PT" with no components. Do not accept a time unit (H, M, S) without the "T"
separator. Do not accept fractions on anything except seconds. Do not silently return 0
for bad input. Raise ValueError specifically, not a generic Exception.

<spec>...</spec>

### P5 format
Write a Python function `parse_iso_duration(s)` that converts an ISO-8601 duration
string into a total number of seconds. It must handle full strings like
"P1Y2M3DT4H5M6S", standalone weeks like "P2W", fractional seconds like "PT1.5S", and
any subset of components. Use 365 days per year and 30 days per month. Raise ValueError
for any string that is not a valid ISO-8601 duration.

Output format: exactly one fenced ```python block containing the function (with a
docstring listing the unit assumptions), followed by a bullet list titled
"Assumptions" with at most five bullets. No other prose, no test harness, no CLI.

<spec>...</spec>

### P6 fewshot
Write a Python function `parse_iso_duration(s)` that converts an ISO-8601 duration
string into a total number of seconds. It must handle full strings like
"P1Y2M3DT4H5M6S", standalone weeks like "P2W", fractional seconds like "PT1.5S", and
any subset of components. Use 365 days per year and 30 days per month. Raise ValueError
for any string that is not a valid ISO-8601 duration.

Examples of expected behaviour:

<example>
parse_iso_duration("P1DT12H")  ->  129600
</example>

<example>
parse_iso_duration("PT0.25S")  ->  0.25
</example>

<example>
parse_iso_duration("PT")  ->  raises ValueError("no components in 'PT'")
</example>

<spec>...</spec>

### P7 cot
Write a Python function `parse_iso_duration(s)` that converts an ISO-8601 duration
string into a total number of seconds. It must handle full strings like
"P1Y2M3DT4H5M6S", standalone weeks like "P2W", fractional seconds like "PT1.5S", and
any subset of components. Use 365 days per year and 30 days per month. Raise ValueError
for any string that is not a valid ISO-8601 duration.

Before writing code, think step by step: what is the grammar of a duration string,
which strings look valid but are not (empty P, units after a missing T, fractions in
the wrong place, weeks mixed with other units), and how will you detect each. Show your
reasoning briefly, then give the final code under a heading "Code:".

<spec>...</spec>

### P8 fullstack
You are a senior Python engineer who writes small, well-tested standard-library
utilities.

Goal: write `parse_iso_duration(s)` so that a billing service can convert any ISO-8601
duration string it stores into a total number of seconds, and reliably reject bad data.

Context: the service stores subscription intervals as duration strings such as
"P1Y2M3DT4H5M6S", "P2W", "PT1.5S", "PT36H" and "P1DT12H"; it only needs total seconds,
so the team fixed 1 year = 365 days and 1 month = 30 days. Weeks always appear alone.
Fractions only ever appear on seconds. Malformed strings must raise ValueError so they
never reach the database.

Constraints: standard library only. Exactly one function with that exact name and
signature; no classes, no CLI, no print statements. Reject "P" and "PT" with no
components, any time unit without the "T" separator, fractions on anything except
seconds, and any unknown characters. Raise ValueError specifically. Do not return 0 or
None for bad input.

Format: one fenced ```python block containing the function with a docstring that lists
the unit assumptions, then a bullet list titled "Assumptions" with at most five bullets.
Nothing else.

<spec>...</spec>

### P9 interview
Write a Python function `parse_iso_duration(s)` that converts an ISO-8601 duration
string into a total number of seconds. Before writing, ask me any clarifying questions
you need (unit lengths, which forms must be supported, how to treat bad input,
dependencies). I have answered them below; use the answers.

<spec>...</spec>

Q: How long are a year and a month? A: Fixed: 365 days and 30 days. Calendar accuracy
is not needed.
Q: Must weeks be supported, and can they combine with other units? A: Yes, "P2W" must
work. Weeks always appear alone; "P1W2D" should be rejected.
Q: Are fractional values allowed? A: Only on seconds, e.g. "PT1.5S". A fraction on any
other unit is invalid.
Q: What should happen for invalid strings? A: Raise ValueError. That includes a missing
leading P, an empty "P" or "PT", and time units without the T separator (e.g. "P1S").
Q: Can I use a library like dateutil? A: No, standard library only. One function, no
CLI, no printing.
Q: Return type? A: int or float is fine as long as the value is correct.
