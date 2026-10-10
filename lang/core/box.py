"""A box: a region of space with six named sides."""
from __future__ import annotations

from . import directions
from .directions import AXES
from .errors import LangError
from .refs import Pos, Side, as_pos


class Box:
    def __init__(self, lo: dict[str, float], hi: dict[str, float]):
        self.lo = {a: float(lo[a]) for a in AXES}
        self.hi = {a: float(hi[a]) for a in AXES}
        for a in AXES:
            if self.hi[a] < self.lo[a]:
                raise LangError(f"Box: {a} extent is negative ({self.lo[a]} > {self.hi[a]}).")

    @classmethod
    def from_size(cls, width: float, depth: float, height: float, origin=(0.0, 0.0, 0.0)) -> "Box":
        """A box by extents named as the frame names them, with its minimum
        corner at `origin`."""
        f = directions.frame
        size = {f.axis_of_extent("width"): width,
                f.axis_of_extent("depth"): depth,
                f.axis_of_extent("height"): height}
        lo = dict(zip(AXES, origin))
        hi = {a: lo[a] + size[a] for a in AXES}
        return cls(lo, hi)

    @classmethod
    def from_sides(cls, **sides) -> "Box":
        """A box from positions named by direction, e.g.
        `Box.from_sides(left=..., right=..., ...)`. All six are required."""
        f = directions.frame
        lo, hi = {}, {}
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

    # -- sides and extents -------------------------------------------------

    def side(self, direction) -> Side:
        d = directions.frame.direction(direction)
        value = self.hi[d.axis] if d.sign > 0 else self.lo[d.axis]
        return Side(d.axis, value, inward=-d)

    def __getattr__(self, name: str):
        f = directions.frame
        if f.is_direction(name):
            return self.side(name)
        if name in f.extents:
            return self.extent(name)
        raise AttributeError(name)

    def extent(self, axis_or_name: str) -> float:
        f = directions.frame
        if axis_or_name in f.extents:
            axis = f.axis_of_extent(axis_or_name)
        elif axis_or_name in AXES:
            axis = axis_or_name
        else:
            axis = f.direction(axis_or_name).axis
        return self.hi[axis] - self.lo[axis]

    def center(self, axis_or_name: str) -> Pos:
        axis = axis_or_name if axis_or_name in AXES else directions.frame.direction(axis_or_name).axis
        return Pos(axis, (self.lo[axis] + self.hi[axis]) / 2)

    def center_point(self) -> tuple[float, float, float]:
        return tuple((self.lo[a] + self.hi[a]) / 2 for a in AXES)

    # -- derived boxes -----------------------------------------------------

    def split(self, axis_or_name: str, n: int, gap: float = 0.0) -> list["Box"]:
        """`n` equal boxes along an axis, from its minimum to its maximum,
        with `gap` between them."""
        axis = axis_or_name if axis_or_name in AXES else directions.frame.direction(axis_or_name).axis
        if n < 1:
            raise LangError("split: n must be at least 1.")
        total = self.extent(axis) - gap * (n - 1)
        if total <= 0:
            raise LangError(f"split: {n} bays with gap {gap} do not fit in {self.extent(axis)}.")
        size = total / n
        boxes = []
        for i in range(n):
            lo = dict(self.lo)
            hi = dict(self.hi)
            lo[axis] = self.lo[axis] + i * (size + gap)
            hi[axis] = lo[axis] + size
            boxes.append(Box(lo, hi))
        return boxes

    def shrunk(self, **by_direction) -> "Box":
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

    def with_side(self, direction, value: float) -> "Box":
        d = directions.frame.direction(direction)
        lo, hi = dict(self.lo), dict(self.hi)
        (hi if d.sign > 0 else lo)[d.axis] = float(value)
        return Box(lo, hi)

    def overlaps(self, other: "Box", tolerance: float = 1e-6) -> bool:
        return all(self.lo[a] < other.hi[a] - tolerance and other.lo[a] < self.hi[a] - tolerance
                   for a in AXES)

    def as_dict(self) -> dict:
        return {"min": [self.lo[a] for a in AXES], "max": [self.hi[a] for a in AXES]}

    def __repr__(self) -> str:
        return "Box(" + ", ".join(f"{a}=[{self.lo[a]:g}, {self.hi[a]:g}]" for a in AXES) + ")"
