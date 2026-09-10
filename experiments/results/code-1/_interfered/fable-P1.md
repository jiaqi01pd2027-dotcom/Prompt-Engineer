All 13 valid and 25 invalid cases pass. Here's the function:

```python
import re

_SECONDS_PER = {
    "Y": 365 * 24 * 3600,
    "M": 30 * 24 * 3600,
    "W": 7 * 24 * 3600,
    "D": 24 * 3600,
    "H": 3600,
    "TM": 60,  # minutes (the M that appears after T)
    "S": 1,
}

# P[nY][nM][nD][T[nH][nM][n(.n)S]]   or   PnW
# Only the seconds field may carry a fraction; ISO permits ',' or '.' as the separator.
_DURATION_RE = re.compile(
    r"^P"
    r"(?:"
    r"(?P<W>\d+)W"
    r"|"
    r"(?:(?P<Y>\d+)Y)?"
    r"(?:(?P<M>\d+)M)?"
    r"(?:(?P<D>\d+)D)?"
    r"(?:T"
    r"(?:(?P<H>\d+)H)?"
    r"(?:(?P<TM>\d+)M)?"
    r"(?:(?P<S>\d+(?:[.,]\d+)?)S)?"
    r")?"
    r")$"
)


def parse_iso_duration(s: str) -> "float | int":
    """Convert an ISO-8601 duration string to a total number of seconds.

    Supports the designator form ``PnYnMnDTnHnMnS`` (any subset of components,
    in order) and the week form ``PnW``. Only the seconds component may be
    fractional. Uses 1 year = 365 days and 1 month = 30 days.

    Returns an ``int`` unless fractional seconds are present, in which case a
    ``float`` is returned.

    Raises ``ValueError`` for anything that is not a valid ISO-8601 duration.
    """
    if not isinstance(s, str):
        raise TypeError(f"expected str, got {type(s).__name__}")

    m = _DURATION_RE.fullmatch(s)
    if m is None:
        raise ValueError(f"invalid ISO-8601 duration: {s!r}")

    fields = {k: v for k, v in m.groupdict().items() if v is not None}

    # "P" on its own carries no components.
    if not fields:
        raise ValueError(f"invalid ISO-8601 duration: {s!r}")

    # "T" must be followed by at least one time component ("P1DT", "PT").
    if "T" in s and not (fields.keys() & {"H", "TM", "S"}):
        raise ValueError(f"invalid ISO-8601 duration: {s!r}")

    total = 0
    for key, value in fields.items():
        if key == "S" and ("." in value or "," in value):
            amount = float(value.replace(",", "."))
        else:
            amount = int(value)
        total += amount * _SECONDS_PER[key]

    return total
```

Saved at `/Users/tigerzhang/Library/Application Support/Claude/scratch-workspaces/2fbbb0d4-c0ac-4496-944c-ccd44cde89cd/afc2d717-2ef6-43fb-8872-1739b1232e4c/scratch-2026-09-09-1a35d2/iso_duration.py`.

**How it works**

- One regex encodes the grammar: either `PnW` on its own, or `P` followed by optional `Y`/`M`/`D` and an optional `T` block with `H`/`M`/`S`. Because the date-side `M` and time-side `M` are separate named groups (`M` vs `TM`), the `T` separator is what disambiguates months from minutes, and a time unit appearing without `T` (e.g. `P1S`, `P1H`) fails to match.
- Fractions are permitted only in the `S` group (`\d+(?:[.,]\d+)?`), so `P1.5D` and `PT1.5M` are rejected. Both `.` and `,` are accepted as the decimal separator, since ISO-8601 allows either.
- Two post-checks cover what a regex with all-optional groups can't: a bare `P` (no components) and a dangling `T` (`PT`, `P1DT`).
- Return type is `int` when there's no fractional part (`PT36H` -> `129600`), `float` otherwise (`PT1.5S` -> `1.5`).

**Verified results**

| Input | Output |
|---|---|
| `P1Y2M3DT4H5M6S` | `36993906` |
| `P2W` | `1209600` |
| `PT1.5S` | `1.5` |
| `PT36H` | `129600` |
| `P1DT12H` | `129600` |

Rejected with `ValueError`: `""`, `P`, `PT`, `P1DT`, `1Y`, `T1H`, `P1S`, `P1H`, `P1.5D`, `PT1.5M`, `P1Y1W`, `P1D1Y` (wrong order), `PT1S1M`, `p1d`, leading/trailing whitespace, `P1Yx`, `PT.5S`, `PT1.S`, `-P1D`, `P-1D`.

**Deliberate strictness choices** (easy to relax if you need to):
- Uppercase only; lowercase designators are rejected.
- Weeks cannot be combined with other components (`P1W1D` is invalid), per the original ISO-8601 grammar.
- No sign prefix; negative durations raise.
- A non-`str` argument raises `TypeError` rather than `ValueError`.
