"""The faces of a board and what is named through them.

`Face` is one of a board's six faces, named by direction in the frame of
the board's scope; it is also a position (its plane), so it works in
`on()`, `between()` and the position algebra, and moved by `gap()` or
`into()` it is a `Side` that keeps the face's side. `Edge` is where two
faces meet: a chamfer's target, a corner of the outline when both faces
are narrow, and an `at=` point in the middle of the first face's edge.
`Anchor` is a point on a face for `at=`, named by the edges it is measured
from (`side.inner.front(37).bottom(z)`). `Outline` is a big face's
outer contour, and `Operation` a named operation of a board, whose edges
are positions (`left.toekick.top`).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from . import directions
from .directions import Axis, Direction
from .errors import LangError
from .ops import Chamfer, Cut, EdgeOp, Hole, Op, VGroove
from .refs import HasPosition, Number, Pos, PositionArithmetic, Side, as_pos
from .shapes import Anchor as ShapeAnchor

if TYPE_CHECKING:
    from .part import Board

Point2 = tuple[float, float]


class Face(PositionArithmetic):
    """One of the six faces of a board. Its direction is named in the frame
    of the board's scope, whatever frame named it when it was asked for,
    so `name` reads as the build file writes it."""

    def __init__(self, part: Board, direction: Direction):
        self.part = part
        self.direction = part.scope.frame.direction_of(direction.axis, direction.sign)

    @property
    def axis(self) -> Axis:
        return self.direction.axis

    @property
    def position(self) -> Pos:
        """The face's plane as a position on its axis."""
        b = self.part.box()
        return Pos(self.axis, b.hi[self.axis] if self.direction.sign > 0 else b.lo[self.axis])

    @property
    def value(self) -> float:
        return self.position.value

    def gap(self, n: float) -> Side:
        """The face's plane moved `n` out of the part. It keeps the face's
        side, as a box side moved by `gap()` keeps its own: a board lies on
        it away from the part without `toward=`, as on the face itself,
        `on(back.inner.gap(15))`; anywhere else it is a position
        [decided by Florian, 2026-10-15: it was a bare position, which
        needed toward=]."""
        return Side(self.axis, self.value + self.direction.sign * n, inward=self.direction)

    def into(self, n: float) -> Side:
        """The face's plane moved `n` into the part, behind the face; it
        keeps the face's side, as `gap()` does."""
        return Side(self.axis, self.value - self.direction.sign * n, inward=self.direction)

    @property
    def is_big(self) -> bool:
        return self.axis == self.part.t_axis

    @property
    def name(self) -> str:
        """The direction name in the part's frame."""
        return self.direction.name

    @property
    def world_name(self) -> str:
        """The direction name in the world frame, as the layout stores it."""
        return directions.frame.name_of(self.direction)

    # -- edges: this face with another ---------------------------------------------

    def edge(self, other: str | Direction | Face) -> Edge:
        other_face = other if isinstance(other, Face) else self.part.face(other)
        return Edge(self.part, self, other_face)

    @property
    def front(self) -> Edge:
        return self.edge("front")

    @property
    def back(self) -> Edge:
        return self.edge("back")

    @property
    def left(self) -> Edge:
        return self.edge("left")

    @property
    def right(self) -> Edge:
        return self.edge("right")

    @property
    def top(self) -> Edge:
        return self.edge("top")

    @property
    def bottom(self) -> Edge:
        return self.edge("bottom")

    @property
    def inner(self) -> Edge:
        return self.edge("inner")

    @property
    def outer(self) -> Edge:
        return self.edge("outer")

    # -- points and contours on this face -------------------------------------------

    @property
    def center(self) -> Anchor:
        """The middle of the face, as an `at=` anchor."""
        return Anchor(self)

    @property
    def outline(self) -> Outline:
        """The face's outer contour, for `chamfer()`, `fillet()` and
        `dogbones(at=)`."""
        return Outline(self)

    def __repr__(self) -> str:
        return f"Face({self.part.path}.{self.name})"


class Edge:
    """The edge where face `a` meets face `b`. For `chamfer()` it is that
    edge, and where two narrow faces meet, a corner of the outline, which
    `fillet()` rounds; for `at=` it is the middle of that edge of face `a`,
    from which an offset, `side.inner.front(37)`, or a corner,
    `side.outer.bottom.front`, continues as an `Anchor`."""

    def __init__(self, part: Board, a: Face, b: Face):
        if a.axis == b.axis:
            raise LangError(f"{a.name}.{b.name} is not an edge: both faces lie on {a.axis}.", part.path)
        self.part, self.a, self.b = part, a, b

    @property
    def name(self) -> str:
        return f"{self.a.name}.{self.b.name}"

    @property
    def through(self) -> bool:
        """Whether the edge runs through the board, where two narrow faces
        meet: a corner of the outline (`panel.front.left` on a board lying
        flat)."""
        return not (self.a.is_big or self.b.is_big)

    @property
    def world_name(self) -> str:
        return f"{self.a.world_name}.{self.b.world_name}"

    def __repr__(self) -> str:
        return f"Edge({self.part.path}.{self.name})"

    # -- as an anchor on face a -----------------------------------------------------

    @property
    def anchor(self) -> Anchor:
        return Anchor(self.a).toward(self.b.direction)

    def __call__(self, value: Number | Pos | HasPosition) -> Anchor:
        """A point `value` inside this edge: a number is a distance from the
        edge, a position is taken as it is."""
        return self.anchor(value)

    def _corner(self, name: str) -> Anchor:
        return self.anchor.toward(name)

    @property
    def front(self) -> Anchor:
        return self._corner("front")

    @property
    def back(self) -> Anchor:
        return self._corner("back")

    @property
    def left(self) -> Anchor:
        return self._corner("left")

    @property
    def right(self) -> Anchor:
        return self._corner("right")

    @property
    def top(self) -> Anchor:
        return self._corner("top")

    @property
    def bottom(self) -> Anchor:
        return self._corner("bottom")

    @property
    def inner(self) -> Anchor:
        return self._corner("inner")

    @property
    def outer(self) -> Anchor:
        return self._corner("outer")


class Anchor:
    """A point on a face for `at=`, named by the edges it is measured from.

    `face.center` is the middle; `face.front` the middle of the front edge;
    `face.front(37)` 37 mm inside that edge; `face.bottom.front` the corner;
    `face.front(37).bottom(z)` 37 mm behind the front edge at the position
    `z`. A number measures from the edge it follows, a position is taken as
    it is and must lie on that edge's axis. An axis that is not named stays
    centred. When a shape is placed, the shape's own side or corner of the
    same name goes onto the point, so the shape extends into the face.
    """

    def __init__(self, face: Face, named: dict[Axis, tuple[Direction, float | Pos | None]] | None = None,
                 last: Axis | None = None):
        self.face = face
        self._named: dict[Axis, tuple[Direction, float | Pos | None]] = dict(named or {})
        self._last: Axis | None = last

    @property
    def part(self) -> Board:
        return self.face.part

    def __repr__(self) -> str:
        parts = [f"{d.name}({v})" if v is not None else d.name for d, v in self._named.values()]
        return f"Anchor({self.part.path}.{self.face.name}" + "".join("." + p for p in parts) + ")"

    def toward(self, name: str | Direction) -> Anchor:
        """This anchor moved onto the edge of its face in the given
        direction (`inner`/`outer` and aliases included)."""
        d = self.part.face(name).direction
        if d.axis == self.face.axis:
            raise LangError(f"{self!r}: {d.name} is not an edge of the {self.face.name} face.", self.part.path)
        if d.axis in self._named:
            raise LangError(f"{self!r}: {d.name} and {self._named[d.axis][0].name} lie on the same axis.",
                            self.part.path)
        named = dict(self._named)
        named[d.axis] = (d, None)
        return Anchor(self.face, named, d.axis)

    def __call__(self, value: Number | Pos | HasPosition) -> Anchor:
        last = self._last
        if last is None:
            raise LangError(f"{self!r}: name an edge to measure from, e.g. face.front(37).", self.part.path)
        d, existing = self._named[last]
        if existing is not None:
            raise LangError(f"{self!r}: {d.name} already has a value.", self.part.path)
        if isinstance(value, (int, float)):
            resolved: float | Pos = float(value)
        else:
            pos = as_pos(value, "anchor")
            if pos.axis != d.axis:
                raise LangError(f"{self!r}: position {pos} is not on the axis of {d.name}.", self.part.path)
            resolved = pos
        named = dict(self._named)
        named[last] = (d, resolved)
        return Anchor(self.face, named, last)

    @property
    def front(self) -> Anchor:
        return self.toward("front")

    @property
    def back(self) -> Anchor:
        return self.toward("back")

    @property
    def left(self) -> Anchor:
        return self.toward("left")

    @property
    def right(self) -> Anchor:
        return self.toward("right")

    @property
    def top(self) -> Anchor:
        return self.toward("top")

    @property
    def bottom(self) -> Anchor:
        return self.toward("bottom")

    @property
    def inner(self) -> Anchor:
        return self.toward("inner")

    @property
    def outer(self) -> Anchor:
        return self.toward("outer")

    def resolve(self) -> tuple[Point2, ShapeAnchor]:
        """The point in the face's 2D frame (world coordinates on its two
        axes) and the matching anchor of a shape placed there."""
        b = self.part.box()
        axes = self.part.face_axes(self.face)
        coords: list[float] = []
        fractions: list[float] = []
        flags: list[bool] = []
        for axis in axes:
            if axis in self._named:
                d, value = self._named[axis]
                edge = b.hi[axis] if d.sign > 0 else b.lo[axis]
                if value is None:
                    coord = edge
                elif isinstance(value, Pos):
                    coord = value.value
                else:
                    coord = edge - d.sign * value
                coords.append(coord)
                fractions.append(1.0 if d.sign > 0 else 0.0)
                flags.append(True)
            else:
                coords.append((b.lo[axis] + b.hi[axis]) / 2)
                fractions.append(0.5)
                flags.append(False)
        return (coords[0], coords[1]), ShapeAnchor(fractions[0], fractions[1], flags[0], flags[1])


@dataclass(frozen=True)
class Outline:
    """A face's outer contour, as a `chamfer()` target; for `fillet()` the
    corners of the outline's outer boundary, the same from either big
    face."""
    face: Face


class Operation:
    """A named operation of a board, reached as `side.toekick` or
    `side.op("toekick")`. Its edges are positions named by direction, so
    `side.toekick.top` is the upper edge of the notch and
    `side.groove.floor` the bottom of the pocket; it is also what
    `chamfer()` takes to chamfer the operation's contour, and what
    `fillet()` takes to round the corners a through cut made."""

    def __init__(self, part: Board, name: str, op: Op):
        self.part = part
        self.name = name
        self.op = op

    def __repr__(self) -> str:
        return f"Operation({self.part.path}.{self.name})"

    def extents(self) -> dict[Axis, tuple[float, float]]:
        """The region the operation occupies, per world axis."""
        part = self.part
        b = part.box()
        op = self.op
        extents: dict[Axis, tuple[float, float]] = {}
        if isinstance(op, Chamfer):
            raise LangError(f"{self!r}: a chamfer has no edges to refer to.", part.path)
        if isinstance(op, EdgeOp):
            face = directions.frame.direction(op.face)
            s_axis, t_axis = part.face_axes(Face(part, face))
            inner = op.op
            if isinstance(inner, Hole):
                r = inner.d / 2
                extents[s_axis] = (op.s - r, op.s + r)
                extents[t_axis] = (op.t - r, op.t + r)
            else:
                u0, v0, u1, v1 = inner.shape.bounds
                extents[s_axis] = (u0 + op.s, u1 + op.s)
                extents[t_axis] = (v0 + op.t, v1 + op.t)
            value = (b.hi[face.axis] if face.sign > 0 else b.lo[face.axis]) + face.sign * op.offset
            extents[face.axis] = _span(value, value - face.sign * inner.depth)
            return extents
        u, v = part.u_axis, part.v_axis
        if isinstance(op, Hole):
            r = op.d / 2
            extents[u] = (op.u - r, op.u + r)
            extents[v] = (op.v - r, op.v + r)
        elif isinstance(op, VGroove):
            w = op.depth                    # half the width at the face
            extents[u] = (min(op.u0, op.u1) - w, max(op.u0, op.u1) + w)
            extents[v] = (min(op.v0, op.v1) - w, max(op.v0, op.v1) + w)
        else:
            u0, v0, u1, v1 = op.shape.bounds
            extents[u] = (u0, u1)
            extents[v] = (v0, v1)
        if not isinstance(op, Cut):
            face = directions.frame.direction(op.face)
            value = b.hi[face.axis] if face.sign > 0 else b.lo[face.axis]
            extents[face.axis] = _span(value, value - face.sign * op.depth)
        return extents

    def side(self, name: str | Direction) -> Pos:
        """The operation's edge in the given direction, as a position."""
        d = self.part.scope.frame.direction(name)
        extents = self.extents()
        if d.axis not in extents:
            raise LangError(f"{self!r}: a through cut has no {d.name} edge in the thickness.", self.part.path)
        lo, hi = extents[d.axis]
        return Pos(d.axis, hi if d.sign > 0 else lo)

    @property
    def front(self) -> Pos:
        return self.side("front")

    @property
    def back(self) -> Pos:
        return self.side("back")

    @property
    def left(self) -> Pos:
        return self.side("left")

    @property
    def right(self) -> Pos:
        return self.side("right")

    @property
    def top(self) -> Pos:
        return self.side("top")

    @property
    def bottom(self) -> Pos:
        return self.side("bottom")

    @property
    def floor(self) -> Pos:
        """The bottom of a pocket or hole: its end away from the face it
        is cut from."""
        op = self.op
        inner = op.op if isinstance(op, EdgeOp) else op
        if isinstance(inner, (Cut, Chamfer)):
            raise LangError(f"{self!r}: only a pocket or hole has a floor.", self.part.path)
        face = directions.frame.direction(op.face if isinstance(op, EdgeOp) else inner.face)
        lo, hi = self.extents()[face.axis]
        return Pos(face.axis, lo if face.sign > 0 else hi)


def _span(a: float, b: float) -> tuple[float, float]:
    return (a, b) if a <= b else (b, a)
