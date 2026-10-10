"""A box: a region of space with six named sides.

The coordinates are world millimetres; the names of the sides and extents
come from the box's frame, by default the frame of the scope the box was
made in, so a module's box names its sides the module's way."""
from __future__ import annotations

from . import directions
from .directions import AXES, Axis, Direction, ExtentName, Frame
from .errors import LangError
from .refs import Pos, PosLike, Side, as_pos

_SIDE_NAMES = ("front", "back", "left", "right", "top", "bottom")


class Box:
    def __init__(self, lo: dict[Axis, float], hi: dict[Axis, float], frame: Frame | None = None):
        self.lo: dict[Axis, float] = {a: float(lo[a]) for a in AXES}
        self.hi: dict[Axis, float] = {a: float(hi[a]) for a in AXES}
        self.frame: Frame = frame if frame is not None else directions.current_frame()
        for a in AXES:
            if self.hi[a] < self.lo[a]:
                raise LangError(f"Box: {a} extent is negative ({self.lo[a]} > {self.hi[a]}).")

    @classmethod
    def from_size(cls, width: float, depth: float, height: float,
                  origin: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> Box:
        """A box by extents named as the current frame names them, with its
        minimum corner at `origin`."""
        f = directions.current_frame()
        size: dict[Axis, float] = {
            f.axis_of_extent("width"): width,
            f.axis_of_extent("depth"): depth,
            f.axis_of_extent("height"): height,
        }
        lo: dict[Axis, float] = {"x": origin[0], "y": origin[1], "z": origin[2]}
        hi: dict[Axis, float] = {a: lo[a] + size[a] for a in AXES}
        return cls(lo, hi, f)

    @classmethod
    def from_sides(cls, *, front: PosLike, back: PosLike, left: PosLike, right: PosLike,
                   top: PosLike, bottom: PosLike) -> Box:
        """A box from the positions of its six sides, named as the current
        frame names them."""
        f = directions.current_frame()
        lo: dict[Axis, float] = {}
        hi: dict[Axis, float] = {}
        sides = {"front": front, "back": back, "left": left, "right": right, "top": top, "bottom": bottom}
        for name, value in sides.items():
            d = f.direction(name)
            pos = as_pos(value, f"Box side {name}")
            if pos.axis != d.axis:
                raise LangError(f"Box side {name} needs a position on {d.axis}, got {pos}.")
            (hi if d.sign > 0 else lo)[d.axis] = pos.value
        return cls(lo, hi, f)

    def in_frame(self, frame: Frame) -> Box:
        """The same region with its sides named by another frame."""
        return Box(self.lo, self.hi, frame)

    # -- sides -----------------------------------------------------------------

    def side(self, direction: str | Direction) -> Side:
        d = self.frame.direction(direction)
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

    def extent(self, name: ExtentName) -> float:
        axis = self.frame.axis_of_extent(name)
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

    def center(self, name: ExtentName) -> Pos:
        """The middle of the box along one extent, as a position."""
        axis = self.frame.axis_of_extent(name)
        return Pos(axis, (self.lo[axis] + self.hi[axis]) / 2)

    def center_point(self) -> tuple[float, float, float]:
        return ((self.lo["x"] + self.hi["x"]) / 2,
                (self.lo["y"] + self.hi["y"]) / 2,
                (self.lo["z"] + self.hi["z"]) / 2)

    # -- derived boxes ------------------------------------------------------------

    def split(self, name: ExtentName, n: int, gap: float = 0.0) -> list[Box]:
        """`n` equal boxes along one extent (`split("height", 3)` stacks
        three bays), with `gap` between them."""
        axis = self.frame.axis_of_extent(name)
        if n < 1:
            raise LangError("split: n must be at least 1.")
        total = self.extent(name) - gap * (n - 1)
        if total <= 0:
            raise LangError(f"split: {n} bays with gap {gap} do not fit in {self.extent(name)}.")
        size = total / n
        boxes: list[Box] = []
        for i in range(n):
            lo = dict(self.lo)
            hi = dict(self.hi)
            lo[axis] = self.lo[axis] + i * (size + gap)
            hi[axis] = lo[axis] + size
            boxes.append(Box(lo, hi, self.frame))
        return boxes

    def shrunk(self, *, front: float = 0.0, back: float = 0.0, left: float = 0.0, right: float = 0.0,
               top: float = 0.0, bottom: float = 0.0) -> Box:
        """A copy with sides moved inward by the given amounts."""
        lo, hi = dict(self.lo), dict(self.hi)
        amounts = (front, back, left, right, top, bottom)
        for name, amount in zip(_SIDE_NAMES, amounts):
            if amount == 0.0:
                continue
            d = self.frame.direction(name)
            if d.sign > 0:
                hi[d.axis] -= amount
            else:
                lo[d.axis] += amount
        return Box(lo, hi, self.frame)

    def grown(self, *, front: float = 0.0, back: float = 0.0, left: float = 0.0, right: float = 0.0,
              top: float = 0.0, bottom: float = 0.0) -> Box:
        """A copy with sides moved outward by the given amounts; the mirror
        image of `shrunk`. This is how a part gets room around it:
        `floor.box().grown(top=0.5)`."""
        return self.shrunk(front=-front, back=-back, left=-left, right=-right, top=-top, bottom=-bottom)

    def with_sides(self, *, front: PosLike | None = None, back: PosLike | None = None,
                   left: PosLike | None = None, right: PosLike | None = None,
                   top: PosLike | None = None, bottom: PosLike | None = None) -> Box:
        """A copy with the given sides moved to positions, e.g.
        `bay.with_sides(front=drawer_face.back)`."""
        box = self
        values = (front, back, left, right, top, bottom)
        for name, value in zip(_SIDE_NAMES, values):
            if value is None:
                continue
            d = self.frame.direction(name)
            pos = as_pos(value, f"with_sides({name}=)")
            if pos.axis != d.axis:
                raise LangError(f"with_sides: {name} needs a position on {d.axis}, got {pos}.")
            box = box.with_side(d, pos.value)
        return box

    def with_side(self, direction: str | Direction, value: float) -> Box:
        """One side moved to a coordinate, by direction; `with_sides` is the
        form for build files."""
        d = self.frame.direction(direction)
        lo, hi = dict(self.lo), dict(self.hi)
        (hi if d.sign > 0 else lo)[d.axis] = float(value)
        return Box(lo, hi, self.frame)

    def overlaps(self, other: Box, tolerance: float = 1e-6) -> bool:
        return all(self.lo[a] < other.hi[a] - tolerance and other.lo[a] < self.hi[a] - tolerance
                   for a in AXES)

    def intersection(self, other: Box) -> Box:
        """The common region; only meaningful when the boxes overlap."""
        return Box({a: max(self.lo[a], other.lo[a]) for a in AXES},
                   {a: min(self.hi[a], other.hi[a]) for a in AXES}, self.frame)

    def as_dict(self) -> dict[str, list[float]]:
        return {"min": [self.lo[a] for a in AXES], "max": [self.hi[a] for a in AXES]}

    def __repr__(self) -> str:
        return "Box(" + ", ".join(f"{a}=[{self.lo[a]:g}, {self.hi[a]:g}]" for a in AXES) + ")"
