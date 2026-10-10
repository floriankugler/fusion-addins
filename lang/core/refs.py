"""Positions, lengths and the algebra between them.

A `Pos` is a coordinate on one world axis, in millimetres. Lengths are plain
floats. The rules (DESIGN.md, Placement and references):

- position +/- length gives a position;
- position - position gives a length (same axis only);
- a weighted mix of positions whose weights add up to 1 gives a position;
- anything else is an error.

`Pos + Pos` therefore yields an intermediate `Affine` sum that only becomes
a position once it is scaled so that its weights add up to one, as in
`(a + b) / 2`.

`Side` is a position with an inward direction, the face of a box. Anything
with a `position` attribute (a `Side`, a part's `Face`) is accepted where a
position is expected; `as_pos` does the coercion.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, overload, runtime_checkable

from . import directions
from .directions import Axis, Direction
from .errors import LangError

Number = int | float
EPS = 1e-9


@runtime_checkable
class HasPosition(Protocol):
    @property
    def position(self) -> Pos: ...


@dataclass(frozen=True)
class Pos:
    axis: Axis
    value: float

    @overload
    def __add__(self, other: Number) -> Pos: ...
    @overload
    def __add__(self, other: Pos | Affine | HasPosition) -> Pos | Affine: ...

    def __add__(self, other: Number | Pos | Affine | HasPosition) -> Pos | Affine:
        if isinstance(other, (int, float)):
            return Pos(self.axis, self.value + other)
        if isinstance(other, Affine):
            return other + self
        other_pos = as_pos(other)
        _same_axis(self, other_pos)
        return Affine(self.axis, [(1.0, self.value), (1.0, other_pos.value)])

    def __radd__(self, other: Number) -> Pos:
        return Pos(self.axis, self.value + other)

    @overload
    def __sub__(self, other: Number) -> Pos: ...
    @overload
    def __sub__(self, other: Pos | HasPosition) -> float: ...

    def __sub__(self, other: Number | Pos | HasPosition) -> Pos | float:
        if isinstance(other, (int, float)):
            return Pos(self.axis, self.value - other)
        other_pos = as_pos(other)
        _same_axis(self, other_pos)
        return self.value - other_pos.value

    def __mul__(self, other: Number) -> Affine:
        return Affine(self.axis, [(float(other), self.value)])

    __rmul__ = __mul__

    def __truediv__(self, other: Number) -> Affine:
        return Affine(self.axis, [(1.0 / other, self.value)])

    def __float__(self) -> float:
        return float(self.value)

    def __str__(self) -> str:
        return f"{self.axis}={self.value:g}"

    def __repr__(self) -> str:
        return f"Pos({self.axis}, {self.value:g})"


def _same_axis(a: Pos, b: Pos) -> None:
    if a.axis != b.axis:
        raise LangError(f"Cannot combine positions on different axes ({a} and {b}).")


@dataclass(frozen=True)
class Affine:
    """A weighted sum of positions on one axis. It is a position only when
    the weights add up to one; `as_pos` checks that."""

    axis: Axis
    terms: list[tuple[float, float]]

    @property
    def weight(self) -> float:
        return sum(w for w, _ in self.terms)

    def resolved(self) -> Pos | Affine:
        if abs(self.weight - 1.0) < EPS:
            return Pos(self.axis, sum(w * v for w, v in self.terms))
        return self

    def __add__(self, other: Pos | Affine | HasPosition) -> Pos | Affine:
        if isinstance(other, Affine):
            if other.axis != self.axis:
                raise LangError(f"Cannot combine positions on different axes ({self.axis} and {other.axis}).")
            return Affine(self.axis, self.terms + other.terms).resolved()
        other_pos = as_pos(other)
        if other_pos.axis != self.axis:
            raise LangError(f"Cannot combine positions on different axes ({self.axis} and {other_pos.axis}).")
        return Affine(self.axis, self.terms + [(1.0, other_pos.value)]).resolved()

    __radd__ = __add__

    def __mul__(self, other: Number) -> Pos | Affine:
        return Affine(self.axis, [(w * other, v) for w, v in self.terms]).resolved()

    __rmul__ = __mul__

    def __truediv__(self, other: Number) -> Pos | Affine:
        return self * (1.0 / other)

    def __str__(self) -> str:
        return f"<sum of positions on {self.axis}, weights {self.weight:g}>"


PosLike = Pos | Affine | HasPosition


def as_pos(value: object, what: str = "position") -> Pos:
    """Coerces a Pos, an Affine whose weights add up to one, or anything with
    a `position` (Side, Face) to a Pos."""
    if isinstance(value, Pos):
        return value
    if isinstance(value, Affine):
        resolved = value.resolved()
        if isinstance(resolved, Pos):
            return resolved
        raise LangError(
            f"{what}: the weights of a sum of positions must add up to 1 "
            f"(they add up to {value.weight:g})."
        )
    if isinstance(value, HasPosition):
        return value.position
    raise LangError(f"{what}: expected a position, got {value!r}.")


@dataclass(frozen=True)
class Side:
    """A position with a direction pointing inward, into the box it bounds.
    `on()` uses the direction to decide where a board's thickness goes.
    Moving a side by a length keeps its direction."""

    axis: Axis
    value: float
    inward: Direction

    def __post_init__(self) -> None:
        if self.inward.axis != self.axis:
            raise ValueError("A side's inward direction must lie on its axis.")

    @property
    def position(self) -> Pos:
        return Pos(self.axis, self.value)

    @property
    def outward(self) -> Direction:
        return -self.inward

    def into(self, n: float) -> Pos:
        """A position `n` inside the box, past this side."""
        return Pos(self.axis, self.value + self.inward.sign * n)

    def gap(self, n: float) -> Pos:
        """A position `n` outside the box, before this side."""
        return Pos(self.axis, self.value - self.inward.sign * n)

    @overload
    def __add__(self, other: Number) -> Side: ...
    @overload
    def __add__(self, other: Pos | Affine | HasPosition) -> Pos | Affine: ...

    def __add__(self, other: Number | Pos | Affine | HasPosition) -> Side | Pos | Affine:
        if isinstance(other, (int, float)):
            return Side(self.axis, self.value + other, self.inward)
        return self.position + other

    @overload
    def __sub__(self, other: Number) -> Side: ...
    @overload
    def __sub__(self, other: Pos | HasPosition) -> float: ...

    def __sub__(self, other: Number | Pos | HasPosition) -> Side | float:
        if isinstance(other, (int, float)):
            return Side(self.axis, self.value - other, self.inward)
        return self.position - other

    def __repr__(self) -> str:
        return f"Side({self.axis}, {self.value:g}, inward={self.inward.name})"


def spread(start: PosLike, end: PosLike, pitch: float | None = None, count: int | None = None) -> list[Pos]:
    """Positions from `start` to `end` on one axis.

    With `count`, that many positions including both ends (one position is
    centred). With `pitch`, as many as fit at that spacing, centred within
    the span so the leftover is shared at both ends."""
    a, b = as_pos(start, "spread start"), as_pos(end, "spread end")
    _same_axis(a, b)
    lo, hi = sorted((a.value, b.value))
    span = hi - lo
    if count is not None:
        if count < 1:
            raise LangError("spread: count must be at least 1.")
        if count == 1:
            return [Pos(a.axis, (lo + hi) / 2)]
        return [Pos(a.axis, lo + span * i / (count - 1)) for i in range(count)]
    if pitch is None or pitch <= 0:
        raise LangError("spread: give a positive pitch or a count.")
    n = int(span // pitch) + 1
    rest = span - (n - 1) * pitch
    return [Pos(a.axis, lo + rest / 2 + i * pitch) for i in range(n)]


class HasName(Protocol):
    @property
    def name(self) -> str: ...


@dataclass(frozen=True)
class ToFace:
    """Depth of a cut or hole: to the named face of the same part, plus an
    offset (negative stops short of it)."""
    face: str
    offset: float = 0.0


def to(face: HasName | Literal["inner", "outer"], offset: float = 0.0) -> ToFace:
    """A depth reaching a face of the same part, `to(side.outer, -3)`
    stopping 3 mm short of it. `"inner"` and `"outer"` name the face
    without naming the part, for the chained form."""
    return ToFace(face if isinstance(face, str) else face.name, offset)


class Through:
    def __repr__(self) -> str:
        return "through"


through = Through()

DepthSpec = Number | ToFace | Through

__all__ = [
    "Pos", "Affine", "Side", "HasPosition", "HasName", "PosLike", "Number",
    "DepthSpec", "ToFace", "Through", "to", "through", "spread", "as_pos",
]

# re-exported for callers that only need the frame
_ = directions
