"""The values a nest runs with: the machine's bed, the saw, the gaps, the
nest's time, and the stock, the sheets it may buy and the pieces on hand.

A nest's values come from the build's settings (`keys`), resolved per nest
from the layout (`resolve`), its stock from each material's sheet size
(`sheet_material(..., size=)`, the one size its sheets are bought in
[decided 2026-10-16]) and from the inventory (`inventory`). Sizes are
millimetres, a piece of stock's along its grain first (`2500x1250`: the
grain runs along the 2500); areas are square metres.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from ..core.errors import LangError


@dataclass(frozen=True)
class Sheet:
    """A material's sheet, bought as many as needed: `length` along the
    grain, `width` across."""
    material: str
    length: float
    width: float

    def label(self) -> str:
        return f"{self.length:g}x{self.width:g}"


@dataclass(frozen=True)
class OnHand:
    """Stock on hand (the inventory), full sheets and offcuts alike: a
    material's piece, `length` along the grain, `width` across, and how
    many there are. Used before anything is bought."""
    material: str
    length: float
    width: float
    count: int = 1

    def label(self) -> str:
        return f"{self.length:g}x{self.width:g}"

    def spelled(self) -> str:
        """As the nest file lists the stock given: `birch 15:1250x600*2`."""
        return f"{self.material}:{self.label()}" + (f"*{self.count}" if self.count != 1 else "")


@dataclass(frozen=True)
class Workshop:
    """A nest's values, resolved (`resolve.workshop_of`), each a nesting
    key's (`keys`), its default here."""
    #: The machine's bed (mm); a blank goes on it either way round. None: not given.
    bed: tuple[float, float] | None = None
    #: The least gap between two parts (mm); a part that asks for more is
    #: given it by the nest's items (`Item.spacing`).
    spacing: float = 10.0
    #: The least gap from a part to its blank's edge (mm).
    margin: float = 10.0
    #: The saw's cut (mm).
    kerf: float = 4.0
    #: Saw cuts per sheet at most, a target [Florian, 2026-10-14: about 5].
    max_cuts: int = 5
    #: A rest of a sheet is kept as stock from this across (mm) ...
    keep_across: float = 300.0
    #: ... and this area (m2) [Florian, 2026-10-14]; anything smaller is waste.
    keep_area: float = 0.25
    #: The nest's time per material at most (s), `rate` seconds a part, at
    #: least `least_seconds` (`nest_seconds`).
    seconds: float = 40.0
    rate: float = 0.6
    least_seconds: float = 5.0
    #: Whether refill empties a bought sheet into the others (`refilling`).
    refill: bool = True
    #: What may be bought, a size per material.
    sheets: tuple[Sheet, ...] = field(default=())
    #: What is on hand, used first.
    on_hand: tuple[OnHand, ...] = field(default=())

    def sheet_for(self, material: str) -> Sheet | None:
        return next((s for s in self.sheets if s.material == material), None)

    def on_hand_for(self, material: str) -> list[OnHand]:
        return [o for o in self.on_hand if o.material == material]

    def nest_seconds(self, parts: int) -> float:
        """The nest's time for a material of `parts` parts."""
        return min(self.seconds, max(self.least_seconds, self.rate * parts))

    def keeps(self, w: float, h: float) -> bool:
        """Whether a rest of w x h is worth keeping as stock."""
        return min(w, h) >= self.keep_across - 1e-9 and w * h >= self.keep_area * 1e6 - 1e-6

    @property
    def saw_kerf(self) -> float:
        """The kerf as the saw plan takes it: rounded up to a tenth of a
        millimetre, the plan's unit (`sawing`)."""
        return saw_kerf(self.kerf)

    def fits_bed(self, w: float, h: float) -> bool:
        """Whether a blank of w x h goes on the bed, either way round."""
        assert self.bed is not None
        return fits(w, h, self.bed)


def saw_kerf(kerf: float) -> float:
    """`kerf` rounded up to a tenth of a millimetre."""
    return math.ceil(kerf * 10 - 1e-9) / 10


def fits(w: float, h: float, bed: tuple[float, float], tolerance: float = 1e-6) -> bool:
    """Whether w x h goes into `bed`, either way round."""
    return ((w <= bed[0] + tolerance and h <= bed[1] + tolerance)
            or (w <= bed[1] + tolerance and h <= bed[0] + tolerance))


def check_workshop(workshop: Workshop) -> None:
    """Refuses values the nest cannot work with."""
    if workshop.bed is None:
        raise LangError("No bed given: use(nesting.bed((2000, 1000))) at the root of the build, or on the nest.")
    if 2 * workshop.margin >= min(workshop.bed):
        raise LangError(f"The margin {workshop.margin:g} leaves nothing of the bed "
                        f"{workshop.bed[0]:g} x {workshop.bed[1]:g}.")
    if workshop.seconds <= 0 or workshop.least_seconds <= 0:
        raise LangError(f"The nest's time must be more than 0 (seconds {workshop.seconds:g}, least_seconds "
                        f"{workshop.least_seconds:g}).")
