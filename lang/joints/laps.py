"""Half laps: two boards that cross each other (`lang.core.crossing`), each
notched to half the height they share, so they slot together flush.

`long.join(battens, using=half_lap(toward=floor.top))` laps the board with
each board named, all of which it must cross: its own notches open toward
the given side, the other boards' notches the opposite way. The
split lies in the middle of the height both boards have at the crossing,
or at `at=`, a position. `clearance=` widens every notch by that much on
each side. Each notch is a through cut named `lap_<other board>`.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..core.box import Box
from ..core.crossing import Crossing, crossing
from ..core.directions import AXES, Axis, Direction
from ..core.errors import LangError
from ..core.part import Board
from ..core.refs import PosLike, Side, as_pos

#: How far a notch reaches past the board's edge, so it opens cleanly.
_PAST = 1.0


@dataclass(frozen=True)
class HalfLap:
    toward: Direction
    at: float | None = None
    clearance: float = 0.0

    def join(self, part: Board, /, partners: list[Board]) -> None:
        # Every crossing is checked before any board is cut.
        laps: list[tuple[Board, Crossing, float]] = []
        for other in partners:
            c = crossing(part, other)
            if c is None:
                raise LangError(f"half_lap: {other.path} does not cross this board.", part.path)
            laps.append((other, c, self._split(part, other, c)))
        for other, c, split in laps:
            self._lap(part, other, c, split)

    def _split(self, part: Board, other: Board, c: Crossing) -> float:
        if self.toward.axis != c.axis:
            raise LangError(f"half_lap: toward={self.toward.name} does not run along the line where it meets "
                            f"{other.path} ({c.axis}).", part.path)
        split = self.at if self.at is not None else (c.lo + c.hi) / 2
        if not c.lo < split < c.hi:
            raise LangError(f"half_lap: the split at {c.axis}={split:g} lies outside the height it shares "
                            f"with {other.path} ({c.lo:g} to {c.hi:g}).", part.path)
        return split

    def _lap(self, part: Board, other: Board, c: Crossing, split: float) -> None:
        d = self.toward
        pb, ob = part.box(), other.box()
        low = min(pb.lo[c.axis], ob.lo[c.axis]) - _PAST
        high = max(pb.hi[c.axis], ob.hi[c.axis]) + _PAST
        # This board's notch opens toward `toward`, the other's the other way.
        mine = (split, high) if d.sign > 0 else (low, split)
        theirs = (low, split) if d.sign > 0 else (split, high)
        part.cut(self._notch(part, other, c.axis, mine), name=part.unique_op_name(f"lap_{other.name}"))
        other.cut(self._notch(other, part, c.axis, theirs), name=other.unique_op_name(f"lap_{part.name}"))

    def _notch(self, part: Board, other: Board, axis: Axis, span: tuple[float, float]) -> Box:
        """The region cut from `part`: through its thickness, as wide as
        `other` is thick (plus the clearance), over `span` along `axis`."""
        pb, ob = part.box(), other.box()
        t, w = part.t_axis, other.t_axis
        lo: dict[Axis, float] = {t: pb.lo[t], w: ob.lo[w] - self.clearance, axis: span[0]}
        hi: dict[Axis, float] = {t: pb.hi[t], w: ob.hi[w] + self.clearance, axis: span[1]}
        return Box({a: lo[a] for a in AXES}, {a: hi[a] for a in AXES})


def half_lap(toward: Side | Direction, at: PosLike | None = None, clearance: float = 0.0) -> HalfLap:
    """A half lap with each board named in `join()`. `toward` is the side this
    board's notches open to (`floor.top`: notched from the top, the other
    boards from below); `at` a position for the split instead of the middle
    of the shared height; `clearance` widens each notch per side."""
    direction = toward.outward if isinstance(toward, Side) else toward
    split = as_pos(at, "half_lap(at=)") if at is not None else None
    if split is not None and split.axis != direction.axis:
        raise LangError(f"half_lap: at={split} is not on the axis of toward={direction.name}.")
    if clearance < 0:
        raise LangError("half_lap: clearance must not be negative.")
    return HalfLap(direction, split.value if split is not None else None, float(clearance))
