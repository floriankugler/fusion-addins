"""Positions, lengths and the algebra between them.

A `Pos` is a coordinate on one world axis, in millimetres. Lengths are plain
floats. The rules (design/placement.md):

- position +/- length gives a position;
- position - position gives a length (same axis only);
- a weighted mix of positions whose weights add up to 1 gives a position,
  also with positions taken away (`a + b - c`);
- anything else is an error.

`Pos + Pos` therefore yields an intermediate `Affine` sum that only becomes
a position once its weights add up to one, scaled as in `(a + b) / 2` or
with a position taken from it as in `a + b - c`.

`Side` is a position with an inward direction, the face of a box; moved
into or out of the box (`into`, `gap`) it is still one. A part's face moved
by `gap()` or `into()` is one too, its inward direction the face's, away
from the part; moved again it keeps the face's in and out (`from_face`).
Anything with a `position` attribute (a `Side`, a part's `Face`, a master's
plane) is accepted where a position is expected; `as_pos` does the
coercion, and `PositionArithmetic` gives such a class the algebra above.

A position with a direction (a `Side`, a part's `Face`, through
`DirectedArithmetic`) has the algebra too, but for a length added or taken
away: along the world axis that moves inward in one frame and outward in
another, so it is an error naming `into()` and `gap()`, which say which
way [decided by Florian, 2026-10-15, syntax.md item 1].
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from typing import Never, NoReturn, Protocol, overload, runtime_checkable

from . import directions
from .directions import Axis, Direction, InnerOuter
from .errors import LangError, one_of

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
    def __add__(self, other: Pos | HasPosition) -> Affine: ...
    @overload
    def __add__(self, other: Affine) -> Pos | Affine: ...

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
    @overload
    def __sub__(self, other: Affine) -> Pos | Affine: ...

    def __sub__(self, other: Number | Pos | Affine | HasPosition) -> Pos | Affine | float:
        if isinstance(other, (int, float)):
            return Pos(self.axis, self.value - other)
        if isinstance(other, Affine):
            return Affine(self.axis, [(1.0, self.value)]) - other
        other_pos = as_pos(other)
        _same_axis(self, other_pos)
        return self.value - other_pos.value

    def __mul__(self, other: Number) -> Affine:
        return Affine(self.axis, [(float(other), self.value)])

    __rmul__ = __mul__

    def __truediv__(self, other: Number) -> Affine:
        return Affine(self.axis, [(1.0 / other, self.value)])

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
    the weights add up to one; `as_pos` checks that. A position taken from
    it makes another such sum, so `a + b - c` is a position [decided by
    Florian, 2026-10-14]."""

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

    def __sub__(self, other: Number | Pos | Affine | HasPosition) -> Pos | Affine:
        if isinstance(other, (int, float)):
            raise LangError(f"a length goes with one position, not with a sum of positions whose weights add up to "
                            f"{self.weight:g}: move a position, or the mix once its weights add up to 1.")
        if not isinstance(other, Affine):
            pos = as_pos(other)
            other = Affine(pos.axis, [(1.0, pos.value)])
        if other.axis != self.axis:
            raise LangError(f"Cannot combine positions on different axes ({self.axis} and {other.axis}).")
        return Affine(self.axis, self.terms + [(-w, v) for w, v in other.terms]).resolved()

    def __mul__(self, other: Number) -> Pos | Affine:
        return Affine(self.axis, [(w * other, v) for w, v in self.terms]).resolved()

    __rmul__ = __mul__

    def __truediv__(self, other: Number) -> Pos | Affine:
        return self * (1.0 / other)

    def __str__(self) -> str:
        return f"<sum of positions on {self.axis}, weights {self.weight:g}>"


PosLike = Pos | Affine | HasPosition


class PositionArithmetic(ABC):
    """The position algebra for a class that stands for a position, such
    as a part's face or a master's plane: it computes with `position`."""

    @property
    @abstractmethod
    def position(self) -> Pos: ...

    @overload
    def __add__(self, other: Number) -> Pos: ...
    @overload
    def __add__(self, other: Pos | HasPosition) -> Affine: ...
    @overload
    def __add__(self, other: Affine) -> Pos | Affine: ...

    def __add__(self, other: Number | Pos | Affine | HasPosition) -> Pos | Affine:
        return self.position + other

    def __radd__(self, other: Number) -> Pos:
        return self.position + other

    @overload
    def __sub__(self, other: Number) -> Pos: ...
    @overload
    def __sub__(self, other: Pos | HasPosition) -> float: ...
    @overload
    def __sub__(self, other: Affine) -> Pos | Affine: ...

    def __sub__(self, other: Number | Pos | Affine | HasPosition) -> Pos | Affine | float:
        return self.position - other

    def __mul__(self, other: Number) -> Affine:
        return self.position * other

    def __rmul__(self, other: Number) -> Affine:
        return self.position * other

    def __truediv__(self, other: Number) -> Affine:
        return self.position / other


class DirectedArithmetic(ABC):
    """The position algebra for a position with a direction: a box side, a
    side moved by `into()` or `gap()`, a part's face. A position added or
    taken away, `*` and `/` work as for a bare position, so `(bottom.top +
    top.bottom) / 2` is the middle and `top.bottom - bottom.top` a length;
    a length added or taken away is an error, for the type checker and when
    the build runs, since along the world axis it moves inward in one frame
    and outward in another: `into()` and `gap()` say which way [decided by
    Florian, 2026-10-15, syntax.md item 1]."""

    @property
    @abstractmethod
    def position(self) -> Pos: ...

    @abstractmethod
    def _directed(self) -> tuple[str, str, str | None]:
        """What it is (`"a side"`), how the error writes it
        (`"kitchen.front"`) and the error's path."""

    def _length_refused(self, op: str, n: object, first: bool = False) -> LangError:
        """The error for `self op n`, or `n op self` when the number is
        `first`."""
        noun, label, path = self._directed()
        number, amount = (f"{n:g}", f"{abs(n):g}") if isinstance(n, (int, float)) else (repr(n), "n")
        written = f"{number} {op} {label}" if first else f"{label} {op} {number}"
        return LangError(f"{written}: {noun} has a direction; write {label}.into({amount}) or "
                         f"{label}.gap({amount}).", path)

    @overload
    def __add__(self, other: Pos | HasPosition) -> Affine: ...
    @overload
    def __add__(self, other: Affine) -> Pos | Affine: ...

    def __add__(self, other: Number | Pos | Affine | HasPosition) -> Pos | Affine:
        if isinstance(other, (int, float)):
            raise self._length_refused("+", other)
        return self.position + other

    def __radd__(self, other: Never) -> NoReturn:
        """Only a number reaches here (a position adds itself first)."""
        raise self._length_refused("+", other, first=True)

    @overload
    def __sub__(self, other: Pos | HasPosition) -> float: ...
    @overload
    def __sub__(self, other: Affine) -> Pos | Affine: ...

    def __sub__(self, other: Number | Pos | Affine | HasPosition) -> Pos | Affine | float:
        if isinstance(other, (int, float)):
            raise self._length_refused("-", other)
        return self.position - other

    def __mul__(self, other: Number) -> Affine:
        return self.position * other

    def __rmul__(self, other: Number) -> Affine:
        return self.position * other

    def __truediv__(self, other: Number) -> Affine:
        return self.position / other


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
class Side(DirectedArithmetic):
    """A position with a direction pointing inward, into the box it bounds;
    for a part's face moved by `gap()` or `into()`, the face's direction,
    away from the part (`lang.core.faces.Face.gap`). `on()` uses the
    direction to decide where a board's thickness goes. `into()` and
    `gap()` move it and keep its direction; a length added with `+` or
    `-` is an error (`DirectedArithmetic`). Scaled, it is a position in a
    mix like any other (`0.5 * cab.bottom + 0.5 * cab.top`) [found by
    fuzzing, 2026-10-14: it had no `*` or `/`]."""

    axis: Axis
    value: float
    inward: Direction
    #: Made from a part's face (`Face.gap()`, `Face.into()`): moved again it
    #: keeps the face's in and out, `into()` toward the part, against
    #: `inward`, and `gap()` away from it, so `back.inner.gap(15).gap(5)` is
    #: 20 in front of the back [decided by Florian, 2026-10-15].
    from_face: bool = False
    #: How an error writes it (`kitchen.front`, `back.inner.gap(15)`).
    label: str | None = field(default=None, compare=False, repr=False)

    def __post_init__(self) -> None:
        if self.inward.axis != self.axis:
            raise ValueError("A side's inward direction must lie on its axis.")

    @property
    def position(self) -> Pos:
        return Pos(self.axis, self.value)

    @property
    def outward(self) -> Direction:
        return -self.inward

    @property
    def _into_sign(self) -> int:
        """The sign on the axis of a move by `into()`."""
        return -self.inward.sign if self.from_face else self.inward.sign

    def into(self, n: float) -> Side:
        """This side moved `n` into the box, its inward direction kept, so a
        board lies on it with its thickness inward, `on(cab.bottom.into(60))`
        [decided by Florian, 2026-10-14: it was a bare position, which
        needed toward=]; one made from a face moves into the face's part."""
        return replace(self, value=self.value + self._into_sign * n, label=_moved_label(self.label, "into", n))

    def gap(self, n: float) -> Side:
        """This side moved `n` out of the box, its inward direction kept;
        one made from a face moves away from the face's part."""
        return replace(self, value=self.value - self._into_sign * n, label=_moved_label(self.label, "gap", n))

    def _directed(self) -> tuple[str, str, str | None]:
        return "a side", self.label or "side", None

    def __repr__(self) -> str:
        made = ", from a face" if self.from_face else ""
        return f"Side({self.axis}, {self.value:g}, inward={self.inward.name}{made})"


def _moved_label(label: str | None, how: str, n: float) -> str | None:
    """The label of a side `label` moved by `into(n)` or `gap(n)`."""
    return f"{label}.{how}({n:g})" if label else None


def spread(start: PosLike, end: PosLike, pitch: float | None = None, count: int | None = None) -> list[Pos]:
    """Positions from `start` to `end` on one axis, in that order.

    With `count`, that many positions including both ends (one position is
    centred). With `pitch`, as many as fit at that spacing, centred within
    the span so the leftover is shared at both ends; a span within a
    nanometre of a whole number of pitches fits that many [found by
    fuzzing, 2026-10-14: rounding left one a hair short at some places,
    and it fitted one position fewer there; and the positions ran from the
    lower coordinate, whichever end came first]."""
    a, b = as_pos(start, "spread start"), as_pos(end, "spread end")
    _same_axis(a, b)
    if count is not None and pitch is not None:
        raise LangError("spread: give pitch= or count=, not both.")
    lo, hi = sorted((a.value, b.value))
    span = hi - lo
    if count is not None:
        if count < 1:
            raise LangError("spread: count must be at least 1.")
        if count == 1:
            return [Pos(a.axis, (lo + hi) / 2)]
        values = [lo + span * i / (count - 1) for i in range(count)]
    else:
        if pitch is None or pitch <= 0:
            raise LangError("spread: give a positive pitch or a count.")
        n = int((span + EPS) // pitch) + 1
        rest = span - (n - 1) * pitch
        values = [lo + rest / 2 + i * pitch for i in range(n)]
    if a.value > b.value:
        values.reverse()
    return [Pos(a.axis, v) for v in values]


class HasName(Protocol):
    @property
    def name(self) -> str: ...


class FaceOfPart(Protocol):
    """A face of a part, as `to()` takes it (`lang.core.part.Face`)."""
    @property
    def name(self) -> str: ...
    @property
    def part(self) -> object: ...


@dataclass(frozen=True)
class ToFace:
    """Depth of a cut or hole: to the named face of the same part, plus an
    offset (negative stops short of it). `part` is the part whose face was
    named, None for `"inner"` and `"outer"`; the operation checks that it
    is its own."""
    face: str
    offset: float = 0.0
    part: object = field(default=None, compare=False)


def to(face: FaceOfPart | InnerOuter, offset: float = 0.0) -> ToFace:
    """A depth reaching a face of the same part, `to(side.outer, -3)`
    stopping 3 mm short of it. `"inner"` and `"outer"` name the face
    without naming the part, for the chained form. A positive offset would
    reach past the face, out of the part, and is an error where it is used."""
    if isinstance(face, str):
        return ToFace(one_of(face, InnerOuter, "to()"), offset)
    return ToFace(face.name, offset, face.part)


class Through:
    def __repr__(self) -> str:
        return "through"


through = Through()

DepthSpec = Number | ToFace | Through

__all__ = [
    "Pos", "Affine", "Side", "HasPosition", "HasName", "FaceOfPart", "PositionArithmetic", "DirectedArithmetic",
    "PosLike", "Number",
    "DepthSpec", "ToFace", "Through", "to", "through", "spread", "as_pos",
]

# re-exported for callers that only need the frame
_ = directions
