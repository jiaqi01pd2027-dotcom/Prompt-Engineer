Done. The function lives at `/Users/tigerzhang/Library/Application Support/Claude/scratch-workspaces/2fbbb0d4-c0ac-4496-944c-ccd44cde89cd/afc2d717-2ef6-43fb-8872-1739b1232e4c/scratch-2026-09-09-1a35d2/iso_duration.py`.

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

**How it works.** A single anchored regex enforces the ISO grammar: the leading `P`, unit order (Y, M, D, then `T`, then H, M, S), digits-only for every unit except seconds (which may take `.` or `,`), and either the `PnW` week form *or* the designator form, not both. The regex distinguishes the two `M`s by position, so `P1M` is a month (2,592,000 s) and `PT1M` is a minute (60 s). Two post-checks handle cases the regex alone accepts: a bare `P` (every group empty) and a dangling `T` with nothing after it (`PT`, `P1DT`). The result is an `int` unless fractional seconds appear, then a `float`.

**Verified.** All five spec examples give the expected values (`P1Y2M3DT4H5M6S` → 36,993,906; `P2W` → 1,209,600; `PT1.5S` → 1.5; `PT36H` and `P1DT12H` → 129,600). Every required rejection raises `ValueError`: no leading `P`, empty `P`, `P1H`/`P1S` without `T`, fractions outside seconds (`P1.5D`, `PT1.5H`), unknown characters, plus wrong order, duplicate units, lowercase, whitespace, negatives, and dangling `T`.

**Two judgement calls worth knowing about.** Weeks are exclusive per strict ISO 8601, so `P1W1D` is rejected; if you'd rather allow mixing, the regex change is small. And a non-string argument raises `TypeError` rather than `ValueError`, which is the conventional Python distinction; flip it if your callers expect `ValueError` for everything.
