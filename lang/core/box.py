"""A box: a region of space with six named sides."""
from __future__ import annotations

from . import directions
from .directions import AXES, Axis, Direction
from .errors import LangError
from .refs import Pos, PosLike, Side, as_pos


class Box:
    def __init__(self, lo: dict[Axis, float], hi: dict[Axis, float]):
        self.lo: dict[Axis, float] = {a: float(lo[a]) for a in AXES}
        self.hi: dict[Axis, float] = {a: float(hi[a]) for a in AXES}
        for a in AXES:
            if self.hi[a] < self.lo[a]:
                raise LangError(f"Box: {a} extent is negative ({self.lo[a]} > {self.hi[a]}).")

    @classmethod
    def from_size(cls, width: float, depth: float, height: float,
                  origin: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> Box:
        """A box by extents named as the frame names them, with its minimum
        corner at `origin`."""
        f = directions.frame
        size: dict[Axis, float] = {
            f.axis_of_extent("width"): width,
            f.axis_of_extent("depth"): depth,
            f.axis_of_extent("height"): height,
        }
        lo: dict[Axis, float] = {"x": origin[0], "y": origin[1], "z": origin[2]}
        hi: dict[Axis, float] = {a: lo[a] + size[a] for a in AXES}
        return cls(lo, hi)

    @classmethod
    def from_sides(cls, **sides: PosLike) -> Box:
        """A box from positions named by direction, e.g.
        `Box.from_sides(left=..., right=..., ...)`. All six are required."""
        f = directions.frame
        lo: dict[Axis, float] = {}
        hi: dict[Axis, float] = {}
        for name, value in sides.items():
            d = f.direction(name)
            pos = as_pos(value, f"Box side {name}")
            if pos.axis != d.axis:
                raise LangError(f"Box side {name} needs a position on {d.axis}, got {pos}.")
            (hi if d.sign > 0 else lo)[d.axis] = pos.value
        missing = [a for a in AXES if a not in lo or a not in hi]
        if missing:
            raise LangError(f"Box.from_sides: missing sides on {', '.join(missing)}.")
        return cls(lo, hi)

    # -- sides -----------------------------------------------------------------

    def side(self, direction: str | Direction) -> Side:
        d = directions.frame.direction(direction)
        value = self.hi[d.axis] if d.sign > 0 else self.lo[d.axis]
        return Side(d.axis, value, inward=-d)

    @property
    def front(self) -> Side:
        return self.side("front")

    @property
    def back(self) -> Side:
        return self.side("back")

    @property
    def left(self) -> Side:
        return self.side("left")

    @property
    def right(self) -> Side:
        return self.side("right")

    @property
    def top(self) -> Side:
        return self.side("top")

    @property
    def bottom(self) -> Side:
        return self.side("bottom")

    # -- extents ----------------------------------------------------------------

    def extent(self, axis_or_name: str) -> float:
        axis = directions.frame.axis_of(axis_or_name)
        return self.hi[axis] - self.lo[axis]

    @property
    def width(self) -> float:
        return self.extent("width")

    @property
    def depth(self) -> float:
        return self.extent("depth")

    @property
    def height(self) -> float:
        return self.extent("height")

    def center(self, axis_or_name: str) -> Pos:
        axis = directions.frame.axis_of(axis_or_name)
        return Pos(axis, (self.lo[axis] + self.hi[axis]) / 2)

    def center_point(self) -> tuple[float, float, float]:
        return ((self.lo["x"] + self.hi["x"]) / 2,
                (self.lo["y"] + self.hi["y"]) / 2,
                (self.lo["z"] + self.hi["z"]) / 2)

    # -- derived boxes ------------------------------------------------------------

    def split(self, axis_or_name: str, n: int, gap: float = 0.0) -> list[Box]:
        """`n` equal boxes along an axis, from its minimum to its maximum,
        with `gap` between them."""
        axis = directions.frame.axis_of(axis_or_name)
        if n < 1:
            raise LangError("split: n must be at least 1.")
        total = self.extent(axis) - gap * (n - 1)
        if total <= 0:
            raise LangError(f"split: {n} bays with gap {gap} do not fit in {self.extent(axis)}.")
        size = total / n
        boxes: list[Box] = []
        for i in range(n):
            lo = dict(self.lo)
            hi = dict(self.hi)
            lo[axis] = self.lo[axis] + i * (size + gap)
            hi[axis] = lo[axis] + size
            boxes.append(Box(lo, hi))
        return boxes

    def shrunk(self, **by_direction: float) -> Box:
        """A copy with sides moved inward by the given amounts, keyed by
        direction name."""
        lo, hi = dict(self.lo), dict(self.hi)
        for name, amount in by_direction.items():
            d = directions.frame.direction(name)
            if d.sign > 0:
                hi[d.axis] -= amount
            else:
                lo[d.axis] += amount
        return Box(lo, hi)

    def with_side(self, direction: str | Direction, value: float) -> Box:
        d = directions.frame.direction(direction)
        lo, hi = dict(self.lo), dict(self.hi)
        (hi if d.sign > 0 else lo)[d.axis] = float(value)
        return Box(lo, hi)

    def overlaps(self, other: Box, tolerance: float = 1e-6) -> bool:
        return all(self.lo[a] < other.hi[a] - tolerance and other.lo[a] < self.hi[a] - tolerance
                   for a in AXES)

    def as_dict(self) -> dict[str, list[float]]:
        return {"min": [self.lo[a] for a in AXES], "max": [self.hi[a] for a in AXES]}

    def __repr__(self) -> str:
        return "Box(" + ", ".join(f"{a}=[{self.lo[a]:g}, {self.hi[a]:g}]" for a in AXES) + ")"
