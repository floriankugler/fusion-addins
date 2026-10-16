"""The nest's settings (`lang.core.settings`, `design/nesting.md`): the
machine's bed, the saw, the gaps and the nest's time, each with the default
the nest had before they were settings, used where they hold:

    use(nesting.bed((2000, 1000)), nesting.kerf(3.2))       # the root: the workshop
    kitchen.use(nesting.margin(15))                         # a module
    front.use(nesting.spacing(20))                          # a part
    carcass.use(nesting.seconds(120))                       # a nest (`Scope.nest`)

Nothing reads them during the build, so they are never frozen; the layout
carries them, the parts' with their sources and each nest's own, and the
nest step reads them from there (`resolve`): a nest's own value, else its
parts', else the default. A part reads its value along its own chain (the
part, its scopes, the root), so parts of several modules may give
different values: for every key but `spacing` the nest needs one, and the
parts must agree or the nest is refused, naming two that differ (`AGREE`);
of two parts' spacings the larger holds between them (`MAX`).

Millimetres unless a key says otherwise; a size is along the grain first.
Plain Python without shapely, so a build file imports them without the
solvers (`from lang import nesting`).
"""
from __future__ import annotations

import math
from typing import Any, Literal

from ..core.errors import LangError
from ..core.settings import Setting

Join = Literal["agree", "max"]


def _number(value: object, what: str, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise LangError(f"{what} takes a number, not {value!r}.")
    if value < 0 or (positive and value == 0):
        raise LangError(f"{what}: {value!r} must be {'more than 0' if positive else '0 or more'}.")
    return float(value)


def _mm(value: object, what: str) -> float:
    return _number(value, what)


def _positive(value: object, what: str) -> float:
    return _number(value, what, positive=True)


def _count(value: object, what: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise LangError(f"{what} takes a whole number, 0 or more, not {value!r}.")
    return value


def _flag(value: object, what: str) -> bool:
    if not isinstance(value, bool):
        raise LangError(f"{what} takes True or False, not {value!r}.")
    return value


def _size(value: object, what: str) -> tuple[float, float]:
    if not isinstance(value, (tuple, list)) or len(value) != 2:  # pyright: ignore[reportUnknownArgumentType]
        raise LangError(f"{what} takes a size, two numbers in mm as (2000, 1000), not {value!r}.")
    a, b = (_positive(v, what) for v in value)  # pyright: ignore[reportUnknownVariableType]
    return a, b


#: The machine's bed (mm), either way round; a blank goes on it. No default:
#: a nest with none used anywhere along its parts is refused.
bed: Setting[tuple[float, float]] = Setting(
    ..., "nesting.bed", check=_size, to_layout=lambda v, _: [v[0], v[1]],
    hint="nest.use(nesting.bed((2000, 1000))) gives a nest its own, or ")
#: The saw's cut (mm).
kerf: Setting[float] = Setting(4.0, "nesting.kerf", check=_mm)
#: Saw cuts per sheet at most, a target: a sheet over it is reported
#: [Florian, 2026-10-14: about 5].
max_cuts: Setting[int] = Setting(5, "nesting.max_cuts", check=_count)
#: The least gap between two parts (mm); of two parts' spacings the larger
#: holds between them.
spacing: Setting[float] = Setting(10.0, "nesting.spacing", check=_mm)
#: The least gap from a part to its blank's edge (mm).
margin: Setting[float] = Setting(10.0, "nesting.margin", check=_mm)
#: A rest of a sheet is kept as stock from this across (mm) ...
keep_across: Setting[float] = Setting(300.0, "nesting.keep_across", check=_mm)
#: ... and this area (m2); anything smaller is waste [Florian, 2026-10-14].
keep_area: Setting[float] = Setting(0.25, "nesting.keep_area", check=_mm)
#: The nest's time per material at most (s) ...
seconds: Setting[float] = Setting(40.0, "nesting.seconds", check=_positive)
#: ... at `rate` seconds a part ...
rate: Setting[float] = Setting(0.6, "nesting.rate", check=_mm)
#: ... and at least this (s) [measured 2026-10-15: the examples' 62 parts of
#: birch 15 came out on 7 sheets in 20 s and on 5 in 40 s].
least_seconds: Setting[float] = Setting(5.0, "nesting.least_seconds", check=_positive)
#: Whether refill empties the bought sheet with the least on it into the
#: room on the others (`refilling`).
refill: Setting[bool] = Setting(True, "nesting.refill", check=_flag)

#: Every nesting key, in the order the nest file lists them.
KEYS: tuple[Setting[Any], ...] = (bed, kerf, max_cuts, spacing, margin, keep_across, keep_area, seconds, rate,
                                  least_seconds, refill)
#: How a nest takes a key its parts give: one value they agree on, or, for
#: the spacing between two parts, the larger of theirs.
JOINS: dict[str, Join] = {key.name: "max" if key is spacing else "agree" for key in KEYS}
