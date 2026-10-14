"""The workshop the nest is made for: the machine's bed, the saw, the
spacing, and the stock on hand.

It is read from a workshop file (TOML, `examples/workshop.toml`), and the
command line may give any of it instead (`python -m lang.nest --bed
2000x1000 --sheet 2470x1240`). Sizes are millimetres, a piece of stock's
along its grain first (`2470x1240`: the grain runs along the 2470); areas
are square metres.

    bed = [2000, 1000]          # the machine's bed, either way round
    spacing = 10                # between two parts
    margin = 10                 # from a part to its blank's edge
    kerf = 4                    # the saw's cut
    max_cuts = 5                # saw cuts per sheet at most
    keep_across = 300           # a rest is kept as stock from 300 mm across
    keep_area = 0.25            # ... and 0.25 m2
    seconds = 20                # the nest's time per material

    [[sheet]]                   # for every material, as many as needed
    size = [2470, 1240]

    [[sheet]]                   # for one material, two of them
    material = "birch 15"
    size = [1525, 1525]
    count = 2

    [[offcut]]                  # one offcut on hand
    material = "birch 15"
    size = [1250, 600]

A sheet without a material is on hand for every material, one with a
material for that one only; both count. An offcut always names its
material. The keys and their defaults are `Workshop`'s fields.
"""
from __future__ import annotations

import math
import re
import tomllib
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from ..core.errors import LangError

#: Seconds the nest of one material may take, unless the workshop says.
SECONDS = 20.0


@dataclass(frozen=True)
class Sheet:
    """A size of sheet on hand: `length` along the grain, `width` across."""
    length: float
    width: float
    #: How many are on hand; None: as many as needed (bought).
    count: int | None = None
    #: The material it is for (a layout's label, `birch 15`); None: every one.
    material: str | None = None

    def label(self) -> str:
        return f"{self.length:g}x{self.width:g}" + (f"*{self.count}" if self.count is not None else "")


@dataclass(frozen=True)
class Offcut:
    """A piece of stock on hand, used before any sheet: `length` along the
    grain, `width` across."""
    material: str
    length: float
    width: float

    def label(self) -> str:
        return f"{self.material}:{self.length:g}x{self.width:g}"


@dataclass(frozen=True)
class Workshop:
    #: The machine's bed (mm); a blank goes on it either way round. None: not given.
    bed: tuple[float, float] | None = None
    #: The least gap between two parts (mm).
    spacing: float = 10.0
    #: The least gap from a part to its blank's edge (mm).
    margin: float = 10.0
    #: The saw's cut (mm).
    kerf: float = 4.0
    #: Saw cuts per sheet at most [Florian, 2026-10-14: about 5].
    max_cuts: int = 5
    #: A rest of a sheet is kept as stock from this across (mm) ...
    keep_across: float = 300.0
    #: ... and this area (m2) [Florian, 2026-10-14]; anything smaller is waste.
    keep_area: float = 0.25
    #: The nest's time per material (s).
    seconds: float = SECONDS
    sheets: tuple[Sheet, ...] = field(default=())
    offcuts: tuple[Offcut, ...] = field(default=())

    def sheets_for(self, material: str) -> list[Sheet]:
        return [s for s in self.sheets if s.material is None or s.material == material]

    def offcuts_for(self, material: str) -> list[Offcut]:
        return [o for o in self.offcuts if o.material == material]

    def keeps(self, w: float, h: float) -> bool:
        """Whether a rest of w x h is worth keeping as stock."""
        return min(w, h) >= self.keep_across - 1e-9 and w * h >= self.keep_area * 1e6 - 1e-6

    def fits_bed(self, w: float, h: float) -> bool:
        """Whether a blank of w x h goes on the bed, either way round."""
        assert self.bed is not None
        return fits(w, h, self.bed)


def fits(w: float, h: float, bed: tuple[float, float], tolerance: float = 1e-6) -> bool:
    """Whether w x h goes into `bed`, either way round."""
    return ((w <= bed[0] + tolerance and h <= bed[1] + tolerance)
            or (w <= bed[1] + tolerance and h <= bed[0] + tolerance))


_SIZE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*$", re.IGNORECASE)


def parse_size(text: str, what: str) -> tuple[float, float]:
    """`2470x1240` as (2470, 1240)."""
    m = _SIZE.match(text)
    if m is None:
        raise LangError(f"{what}: {text!r} is not a size like 2470x1240.")
    w, h = float(m.group(1)), float(m.group(2))
    _positive(w, what)
    _positive(h, what)
    return w, h


def parse_sheet(text: str) -> Sheet:
    """`[MATERIAL:]LxW[*COUNT]`: `2470x1240`, `birch 15:1525x1525*2`."""
    material, _, rest = text.rpartition(":")
    size, star, count = rest.partition("*")
    length, width = parse_size(size, f"--sheet {text}")
    n = _count(count, f"--sheet {text}") if star else None
    return Sheet(length, width, n, material.strip() or None)


def parse_offcut(text: str) -> Offcut:
    """`MATERIAL:LxW`, `birch 15:1250x600`."""
    material, colon, size = text.rpartition(":")
    if not colon or not material.strip():
        raise LangError(f"--offcut {text}: name its material, as in 'birch 15:1250x600'.")
    length, width = parse_size(size, f"--offcut {text}")
    return Offcut(material.strip(), length, width)


def read_workshop(path: str | Path) -> Workshop:
    """The workshop file at `path` (see the module's doc)."""
    try:
        data = tomllib.loads(Path(path).read_text())
    except tomllib.TOMLDecodeError as error:
        raise LangError(f"{path}: {error}") from None
    return workshop_from(data, str(path))


_KEYS = {"bed", "spacing", "margin", "kerf", "max_cuts", "keep_across", "keep_area", "seconds", "sheet", "offcut"}


def workshop_from(data: dict[str, Any], where: str = "the workshop") -> Workshop:
    unknown = sorted(set(data) - _KEYS)
    if unknown:
        raise LangError(f"{where}: unknown key {', '.join(unknown)} (the keys: {', '.join(sorted(_KEYS))}).")
    kwargs: dict[str, Any] = {}
    if "bed" in data:
        kwargs["bed"] = _pair(data["bed"], f"{where}: bed")
    for key in ("spacing", "margin", "kerf", "keep_across", "keep_area", "seconds"):
        if key in data:
            kwargs[key] = _number(data[key], f"{where}: {key}", zero=key in ("spacing", "margin", "kerf",
                                                                             "keep_across", "keep_area"))
    if "max_cuts" in data:
        kwargs["max_cuts"] = _count(data["max_cuts"], f"{where}: max_cuts", zero=True)
    sheets: list[Sheet] = []
    for k, entry in enumerate(_tables(data.get("sheet", []), f"{where}: sheet")):
        what = f"{where}: sheet {k + 1}"
        _only(entry, {"size", "count", "material"}, what)
        if "size" not in entry:
            raise LangError(f"{what}: give its size, as size = [2470, 1240].")
        length, width = _pair(entry["size"], f"{what}: size")
        count = _count(entry["count"], f"{what}: count") if "count" in entry else None
        sheets.append(Sheet(length, width, count, _material(entry.get("material"), what)))
    offcuts: list[Offcut] = []
    for k, entry in enumerate(_tables(data.get("offcut", []), f"{where}: offcut")):
        what = f"{where}: offcut {k + 1}"
        _only(entry, {"size", "material"}, what)
        if "size" not in entry or "material" not in entry:
            raise LangError(f"{what}: give its material and size, as material = \"birch 15\" and "
                            "size = [1250, 600].")
        length, width = _pair(entry["size"], f"{what}: size")
        material = _material(entry["material"], what)
        assert material is not None
        offcuts.append(Offcut(material, length, width))
    return Workshop(**kwargs, sheets=tuple(sheets), offcuts=tuple(offcuts))


def with_overrides(workshop: Workshop, *, bed: tuple[float, float] | None = None,
                   sheets: list[Sheet] | None = None, offcuts: list[Offcut] | None = None,
                   **numbers: float | int | None) -> Workshop:
    """The workshop with what the command line gives instead: sheets and
    offcuts replace the file's of their kind, numbers replace its numbers."""
    changes: dict[str, Any] = {k: v for k, v in numbers.items() if v is not None}
    if bed is not None:
        changes["bed"] = bed
    if sheets is not None:
        changes["sheets"] = tuple(sheets)
    if offcuts is not None:
        changes["offcuts"] = tuple(offcuts)
    return replace(workshop, **changes)


def check_workshop(workshop: Workshop) -> None:
    """Refuses a workshop the nest cannot work with."""
    if workshop.bed is None:
        raise LangError("No bed given: the workshop file's bed = [2000, 1000], or --bed 2000x1000.")
    if 2 * workshop.margin >= min(workshop.bed):
        raise LangError(f"The margin {workshop.margin:g} leaves nothing of the bed "
                        f"{workshop.bed[0]:g} x {workshop.bed[1]:g}.")
    if workshop.seconds <= 0:
        raise LangError(f"seconds must be more than 0, not {workshop.seconds:g}.")


# -- reading values ------------------------------------------------------------------------

def _tables(value: object, what: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(v, dict) for v in value):  # pyright: ignore[reportUnknownVariableType]
        raise LangError(f"{what}: write each as a [[table]].")
    return value  # pyright: ignore[reportUnknownVariableType]


def _only(entry: dict[str, Any], keys: set[str], what: str) -> None:
    unknown = sorted(set(entry) - keys)
    if unknown:
        raise LangError(f"{what}: unknown key {', '.join(unknown)} (the keys: {', '.join(sorted(keys))}).")


def _material(value: object, what: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise LangError(f"{what}: material is a material's name and thickness, as \"birch 15\".")
    return value.strip()


def _number(value: object, what: str, zero: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise LangError(f"{what}: {value!r} is not a number.")
    if value < 0 or (value == 0 and not zero):
        raise LangError(f"{what}: {value!r} must be more than 0.")
    return float(value)


def _positive(value: float, what: str) -> None:
    if not value > 0:
        raise LangError(f"{what}: {value:g} must be more than 0.")


def _pair(value: object, what: str) -> tuple[float, float]:
    if isinstance(value, str):
        return parse_size(value, what)
    if not isinstance(value, list) or len(value) != 2:  # pyright: ignore[reportUnknownArgumentType]
        raise LangError(f"{what}: give two numbers, as [2470, 1240].")
    a, b = (_number(v, what) for v in value)  # pyright: ignore[reportUnknownVariableType]
    return a, b


def _count(value: object, what: str, zero: bool = False) -> int:
    if isinstance(value, str):
        try:
            value = int(value)
        except ValueError:
            raise LangError(f"{what}: {value!r} is not a whole number.") from None
    if isinstance(value, bool) or not isinstance(value, int):
        raise LangError(f"{what}: {value!r} is not a whole number.")
    if value < 0 or (value == 0 and not zero):
        raise LangError(f"{what}: {value} must be more than 0.")
    return value
