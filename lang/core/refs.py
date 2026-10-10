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
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from . import directions
from .errors import LangError

Number = Union[int, float]
EPS = 1e-9


def _is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


@dataclass(frozen=True)
class Pos:
    axis: str
    value: float

    def __post_init__(self):
        if self.axis not in directions.AXES:
            raise ValueError(f"Unknown axis {self.axis!r}.")

    # position +/- length
    def __add__(self, other):
        if _is_number(other):
            return Pos(self.axis, self.value + other)
        if isinstance(other, Pos):
            return Affine(self.axis, [(1.0, self.value), (1.0, _same_axis(self, other).value)])
        if isinstance(other, Affine):
            return other + self
        return NotImplemented

    def __radd__(self, other):
        if _is_number(other):
            return Pos(self.axis, self.value + other)
        return NotImplemented

    def __sub__(self, other):
        if _is_number(other):
            return Pos(self.axis, self.value - other)
        if isinstance(other, Pos):
            return self.value - _same_axis(self, other).value
        return NotImplemented

    def __rsub__(self, other):
        raise LangError(
            f"A length minus a position ({other} - {self}) has no meaning; "
            "subtract positions from positions or lengths from positions."
        )

    def __mul__(self, other):
        if _is_number(other):
            return Affine(self.axis, [(float(other), self.value)])
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        if _is_number(other):
            return Affine(self.axis, [(1.0 / other, self.value)]).resolved()
        return NotImplemented

    def __neg__(self):
        raise LangError(f"A negated position (-{self}) has no meaning.")

    def __float__(self):
        return float(self.value)

    def __str__(self) -> str:
        return f"{self.axis}={self.value:g}"

    def __repr__(self) -> str:
        return f"Pos({self.axis}, {self.value:g})"


def _same_axis(a: Pos, b: Pos) -> Pos:
    if a.axis != b.axis:
        raise LangError(f"Cannot combine positions on different axes ({a} and {b}).")
    return b


@dataclass(frozen=True)
class Affine:
    """A weighted sum of positions on one axis. It is a position only when
    the weights add up to one."""

    axis: str
    terms: list

    @property
    def weight(self) -> float:
        return sum(w for w, _ in self.terms)

    def resolved(self):
        if abs(self.weight - 1.0) < EPS:
            return Pos(self.axis, sum(w * v for w, v in self.terms))
        return self

    def __add__(self, other):
        if isinstance(other, Pos):
            _same_axis(Pos(self.axis, 0.0), other)
            return Affine(self.axis, self.terms + [(1.0, other.value)]).resolved()
        if isinstance(other, Affine):
            _same_axis(Pos(self.axis, 0.0), Pos(other.axis, 0.0))
            return Affine(self.axis, self.terms + other.terms).resolved()
        if _is_number(other):
            raise LangError(
                "Adding a length to a sum of positions is ambiguous; "
                "divide the sum first, then add the length."
            )
        return NotImplemented

    __radd__ = __add__

    def __mul__(self, other):
        if _is_number(other):
            return Affine(self.axis, [(w * other, v) for w, v in self.terms]).resolved()
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        if _is_number(other):
            return self * (1.0 / other)
        return NotImplemented

    def __str__(self) -> str:
        return f"<sum of positions on {self.axis}, weights {self.weight:g}>"


def as_pos(value, what: str = "position") -> Pos:
    """Coerces a Pos, Side, Face or resolved Affine to a Pos."""
    if isinstance(value, Pos):
        return Pos(value.axis, value.value)
    if isinstance(value, Affine):
        resolved = value.resolved()
        if isinstance(resolved, Pos):
            return resolved
        raise LangError(
            f"{what}: the weights of a sum of positions must add up to 1 "
            f"(they add up to {value.weight:g})."
        )
    if hasattr(value, "position"):
        return as_pos(value.position, what)
    raise LangError(f"{what}: expected a position, got {value!r}.")


class Side(Pos):
    """A position with a direction pointing inward, into the box or part
    it bounds. `on()` uses the direction to decide where a board's
    thickness goes. Moving a side keeps its direction."""

    def __init__(self, axis: str, value: float, inward: "directions.Direction"):
        object.__setattr__(self, "axis", axis)
        object.__setattr__(self, "value", float(value))
        object.__setattr__(self, "inward", inward)
        if inward.axis != axis:
            raise ValueError("A side's inward direction must lie on its axis.")

    def __add__(self, other):
        if _is_number(other):
            return Side(self.axis, self.value + other, self.inward)
        return Pos.__add__(self, other)

    def __sub__(self, other):
        if _is_number(other):
            return Side(self.axis, self.value - other, self.inward)
        return Pos.__sub__(self, other)

    @property
    def outward(self) -> "directions.Direction":
        return -self.inward

    def __repr__(self) -> str:
        return f"Side({self.axis}, {self.value:g}, inward={self.inward.name})"

    def __eq__(self, other):
        return isinstance(other, Side) and (self.axis, self.value, self.inward) == (
            other.axis, other.value, other.inward)

    def __hash__(self):
        return hash((self.axis, self.value, self.inward))


def spread(start, end, pitch: float | None = None, count: int | None = None) -> list[Pos]:
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


@dataclass(frozen=True)
class ToFace:
    """Depth of a cut or hole: to the named face of the same part, plus an
    offset (negative stops short of it)."""
    face: str
    offset: float = 0.0


def to(face: str, offset: float = 0.0) -> ToFace:
    return ToFace(face, offset)


class _Through:
    def __repr__(self):
        return "through"


through = _Through()
