Done. The function and its tests are in the scratchpad:

- `/private/tmp/claude-501/.../scratchpad/iso_duration.py` — the implementation (shown above)
- `/private/tmp/claude-501/.../scratchpad/test_iso_duration.py` — 12 `unittest` cases, all passing

**How it works.** A single anchored, verbose regex enforces the ISO-8601 grammar: leading `P`, date components in `Y M W D` order, an optional `T` section with `H M S`, and a fraction (`.` or `,`) permitted only on seconds. Anything the regex rejects raises `ValueError`; two post-checks catch strings that are structurally valid but semantically empty (`"P"`, `"PT"`, `"P1DT"`). Integer components are summed as `int`, so the result is an `int` unless the seconds carry a fraction, in which case it becomes a `float`. Arbitrary-precision ints mean huge day counts don't overflow.

**Verified behaviours** (spec examples plus edge cases):
- `"P1Y2M3DT4H5M6S"` → 36993906, `"P2W"` → 1209600, `"PT1.5S"` → 1.5, `"PT36H"` → 129600, `"P1DT12H"` → 129600
- `"P1MT1M"` correctly distinguishes date-month from time-minute
- `"PT1,5S"` accepts the ISO comma decimal separator
- Rejected: `""`, `"P"`, `"PT"`, `"P1H"`, `"P1S"`, `"P1DT"`, `"P1.5D"`, `"PT1.5H"`, `"PT.5S"`, wrong order (`"P1D1Y"`), duplicates (`"P1Y1Y"`), whitespace, sign prefixes, lowercase, full-width digits
- Non-`str` input raises `TypeError` rather than `ValueError`, since that's a programming error, not a parse error

**Two things worth knowing:**

1. While I was testing, the file on disk was replaced with a different implementation than the one I first wrote. I kept that version as the base and made one fix to it: it used `\d` without `re.ASCII`, so `"PT１S"` (full-width digit) parsed successfully instead of raising. I added the `re.ASCII` flag.

2. That on-disk version lets weeks combine with other components (`"P1W1D"` → 8 days). Strict ISO-8601 only permits `PnW` standalone. The spec you gave doesn't list combined weeks as invalid, so I kept the relaxed behaviour and pinned it in a test. If you want strict ISO, replace the `W` line in the regex with an alternation, `^P(?:(?P<W>\d+)W|<Y/M/D/T form>)$`, and the corresponding test flips to expecting `ValueError`.

--- files ---
(scratchpad/iso_duration.py was shared with and overwritten by concurrent runs fable-P4 and fable-P6; final on-disk content at collection time:)

from __future__ import annotations

import re

_SECONDS_PER = {
    "Y": 365 * 86400,
    "M": 30 * 86400,
    "W": 7 * 86400,
    "D": 86400,
    "H": 3600,
    "TM": 60,
    "S": 1,
}

# Weeks ("PnW") are an alternative form and may not be combined with any
# other component, so they get their own branch of the alternation.
_DURATION_RE = re.compile(
    r"""^P
        (?:
            (?P<W>\d+)W
          |
            (?:(?P<Y>\d+)Y)?
            (?:(?P<M>\d+)M)?
            (?:(?P<D>\d+)D)?
            (?:T
                (?:(?P<H>\d+)H)?
                (?:(?P<TM>\d+)M)?
                (?:(?P<S>\d+(?:[.,]\d+)?)S)?
            )?
        )
        $""",
    re.VERBOSE | re.ASCII,  # ASCII: reject Unicode digits such as "１"
)


def parse_iso_duration(s: str) -> "float | int":
    """Convert an ISO-8601 duration string (e.g. "P1Y2M3DT4H5M6S", "P2W",
    "PT1.5S") into a total number of seconds.

    Uses 365 days per year and 30 days per month. Returns an int unless the
    seconds component carries a fraction, in which case a float is returned.
    Raises ValueError for anything that is not a valid ISO-8601 duration.
    """
    if not isinstance(s, str):
        raise TypeError(f"expected str, got {type(s).__name__}")

    m = _DURATION_RE.fullmatch(s)
    if m is None:
        if not s.startswith("P"):
            raise ValueError(f"duration must start with 'P': {s!r}")
        raise ValueError(f"invalid ISO-8601 duration: {s!r}")

    parts = {k: v for k, v in m.groupdict().items() if v is not None}
    if not parts:
        raise ValueError(f"no components in {s!r}")
    # "P1DT" -- a T separator with nothing after it is not allowed.
    if "T" in s and not any(k in parts for k in ("H", "TM", "S")):
        raise ValueError(f"'T' separator without any time components in {s!r}")

    total = 0
    for key, value in parts.items():
        if key == "S" and ("." in value or "," in value):
            total += float(value.replace(",", ".")) * _SECONDS_PER[key]
        else:
            total += int(value) * _SECONDS_PER[key]
    return total
