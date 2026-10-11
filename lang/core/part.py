"""Parts: boards with placement modifiers, faces and operations.

A board is created with its identity (`board(name, material)`), placed with
order-free modifiers (`on`, `between`, `center`, `inset`, `grain`, `show`,
`manual`) and machined with ordered operations (`cut`, `pocket`, `hole`,
`chamfer`). Every modifier returns the board. Placement is resolved lazily
the first time a face, the box or the layout is asked for; from then on the
placement modifiers are frozen.

Faces and edges are properties named by world direction (`side.front`,
`side.front.inner`), so editors can complete them; project aliases go
through `face()` and `edge()`. A point on a face for `at=` is named
through the face: `side.inner.front(37).bottom(z)` is 37 mm behind the
front edge of the inner face at height `z`, `side.outer.bottom.front` the
corner (see `Anchor`).
"""
from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence
from typing import Any, Literal, Protocol, Self, Union, overload

from . import directions
from . import scope as scopes
from .box import Box
from .contours import Contour, ContourLimit, ContourLimits, as_contour_limit
from .directions import AXES, Axis, Direction, ExtentName
from .errors import LangError
from .layout_types import (ChamferLayout, CutLayout, EdgeOpLayout, HoleLayout, OpLayout,
                           PartLayout, PocketLayout, Rings, VGrooveLayout)
from .material import Material
from .ops import Chamfer, Cut, EdgeOp, Hole, Op, Pocket, VGroove
from .refs import Affine, DepthSpec, HasPosition, Number, Pos, PosLike, Side, Through, ToFace, as_pos
from .shapes import Anchor as ShapeAnchor
from .shapes import Shape, box_shape

Point2 = tuple[float, float]
Limit = Union[Pos, Affine, HasPosition, "Board", "PartLimit", Contour, ContourLimit]


class Face:
    """One of the six faces of a board, named by world direction."""

    def __init__(self, part: Board, direction: Direction):
        self.part = part
        self.direction = direction

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

    def gap(self, n: float) -> Pos:
        """A position `n` outside the face."""
        return Pos(self.axis, self.value + self.direction.sign * n)

    def into(self, n: float) -> Pos:
        """A position `n` inside the part, behind the face."""
        return Pos(self.axis, self.value - self.direction.sign * n)

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
        """The face's outer contour, for `chamfer()`."""
        return Outline(self)

    # -- arithmetic as a position ------------------------------------------------------

    @overload
    def __add__(self, other: float) -> Pos: ...
    @overload
    def __add__(self, other: Pos | Affine | HasPosition) -> Pos | Affine: ...

    def __add__(self, other: float | Pos | Affine | HasPosition) -> Pos | Affine:
        return self.position + other

    def __radd__(self, other: float) -> Pos:
        return self.position + other

    @overload
    def __sub__(self, other: float) -> Pos: ...
    @overload
    def __sub__(self, other: Pos | HasPosition) -> float: ...

    def __sub__(self, other: float | Pos | HasPosition) -> Pos | float:
        return self.position - other

    def __mul__(self, other: float) -> Affine:
        return self.position * other

    __rmul__ = __mul__

    def __truediv__(self, other: float) -> Affine:
        return self.position / other

    def __repr__(self) -> str:
        return f"Face({self.part.path}.{self.name})"


class Edge:
    """The edge where face `a` meets face `b`. For `chamfer()` it is that
    edge; for `at=` it is the middle of that edge of face `a`, from which
    an offset, `side.inner.front(37)`, or a corner, `side.outer.bottom.front`,
    continues as an `Anchor`."""

    def __init__(self, part: Board, a: Face, b: Face):
        if a.axis == b.axis:
            raise LangError(f"{a.name}.{b.name} is not an edge: both faces lie on {a.axis}.", part.path)
        self.part, self.a, self.b = part, a, b

    @property
    def name(self) -> str:
        return f"{self.a.name}.{self.b.name}"

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
    """A face's outer contour, as a `chamfer()` target."""
    face: Face


class Operation:
    """A named operation of a board, reached as `side.toekick` or
    `side.op("toekick")`. Its edges are positions named by direction, so
    `side.toekick.top` is the upper edge of the notch and
    `side.groove.floor` the bottom of the pocket; it is also what
    `chamfer()` takes to chamfer the operation's contour."""

    def __init__(self, part: Board, name: str, op: Op):
        self.part = part
        self.name = name
        self.op = op

    def __repr__(self) -> str:
        return f"Operation({self.part.path}.{self.name})"

    def _extents(self) -> dict[Axis, tuple[float, float]]:
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
            value = b.hi[face.axis] if face.sign > 0 else b.lo[face.axis]
            extents[face.axis] = tuple(sorted((value, value - face.sign * inner.depth)))  # type: ignore[assignment]
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
            extents[face.axis] = tuple(sorted((value, value - face.sign * op.depth)))  # type: ignore[assignment]
        return extents

    def side(self, name: str | Direction) -> Pos:
        """The operation's edge in the given direction, as a position."""
        d = self.part.scope.frame.direction(name)
        extents = self._extents()
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
        lo, hi = self._extents()[face.axis]
        return Pos(face.axis, lo if face.sign > 0 else hi)


class Joint(Protocol):
    """A joint type that can join a board to others (see `lang.joints`):
    `partners` are the boards named in `join(...)`, each of which it must
    join or report as an error."""

    def join(self, part: Board, /, partners: list[Board]) -> None: ...


class Board:
    def __init__(self, name: str, material: Material, shape: Shape | None = None):
        if not name or "." in name:
            raise LangError(f"Part name {name!r} must be non-empty and contain no dots.")
        self.name = name
        self.material = material
        self._shape = shape
        self.scope = scopes.current()
        self.scope.register(self)
        # placement, set once each
        self._on: Side | None = None
        self._limits: list[Limit] = []
        self._center: Pos | None = None
        self._inset: float = 0.0
        self._grain: Axis | None = None
        self._show: str | Direction | None = None
        self.manual_part: bool = False
        self._set: set[str] = set()
        # resolved
        self._box: Box | None = None
        self._t_axis: Axis | None = None
        self._u_axis: Axis | None = None
        self._v_axis: Axis | None = None
        self._outline: Shape | None = None
        self.ops: list[Op] = []
        self._named_ops: dict[str, Op] = {}

    # -- identity ----------------------------------------------------------------------

    @property
    def path(self) -> str:
        prefix = self.scope.path
        return f"{prefix}.{self.name}" if prefix else self.name

    @property
    def thickness(self) -> float:
        return self.material.t

    def __repr__(self) -> str:
        return f"Board({self.path})"

    # -- placement modifiers (order-free, settable once) --------------------------------

    def _placement(self, key: str) -> None:
        if self._box is not None:
            raise LangError(f"{key}() after the placement was used; placement is frozen.", self.path)
        if key in self._set:
            raise LangError(f"{key}() given twice.", self.path)
        self._set.add(key)

    def on(self, ref: Side | Face | PosLike, toward: Side | Direction | None = None) -> Self:
        """Which plane the board's outer big face lies in, and where the
        thickness goes. A box side knows its inward direction; a part's face
        puts the thickness away from that part; a bare position needs
        `toward=`, the direction the thickness extends to, as a box side
        (`toward=cab.top`) or a direction."""
        self._placement("on")
        if isinstance(ref, Side) and toward is None:
            self._on = ref
        elif isinstance(ref, Face) and toward is None:
            self._on = Side(ref.axis, ref.value, inward=ref.direction)
        else:
            if toward is None:
                raise LangError("on(): a bare position needs toward=, the direction the thickness goes.", self.path)
            d = toward.outward if isinstance(toward, Side) else toward
            pos = as_pos(ref, "on()")
            if d.axis != pos.axis:
                raise LangError(f"on(): toward={d.name} is not on the axis of {pos}.", self.path)
            self._on = Side(pos.axis, pos.value, inward=d)
        return self

    def between(self, *limits: Limit) -> Self:
        """Limits on the in-plane axes: positions, box sides, faces or
        parts. A part means its face nearest to this board; `part.into(n)`
        and `part.gap(n)` move that face. Missing limits default to the
        enclosing scope's box."""
        self._placement("between")
        self._limits = list(limits)
        return self

    def into(self, n: float) -> PartLimit:
        """As a limit for another board: this board's nearest face, moved
        `n` into this board, e.g. a floor reaching into a groove."""
        return PartLimit(self, float(n))

    def gap(self, n: float) -> PartLimit:
        """As a limit for another board: this board's nearest face, moved
        `n` away from this board."""
        return PartLimit(self, -float(n))

    def center(self, pos: PosLike) -> Self:
        """The board's thickness is centred on this position; the position's
        axis becomes the thickness axis."""
        self._placement("center")
        self._center = as_pos(pos, "center()")
        return self

    def inset(self, n: float) -> Self:
        """Shrinks the outline by `n` on every in-plane side of its box."""
        self._placement("inset")
        self._inset = float(n)
        return self

    def grain(self, along: ExtentName | Side | Direction | Face) -> Self:
        """The grain direction: an extent (`grain("height")`), a box side or
        a direction (`grain(cab.top)`), or a face of a part."""
        self._placement("grain")
        if isinstance(along, str):
            self._grain = self.scope.frame.axis_of_extent(along)
        else:
            self._grain = along.axis
        return self

    def show(self, face: Face | Side | Direction | Literal["inner", "outer"]) -> Self:
        """The visible big face: `"inner"` or `"outer"` relative to the
        enclosing box, a box side or direction (`show(cab.front)`), or one
        of this board's own faces (`side.show(side.inner)`)."""
        self._placement("show")
        if isinstance(face, str):
            self._show = face
        elif isinstance(face, Face):
            if face.part is not self:
                raise LangError(f"show(): {face!r} is not a face of this board.", self.path)
            self._show = face.direction
        elif isinstance(face, Side):
            self._show = face.outward
        else:
            self._show = face
        return self

    def manual(self) -> Self:
        self._placement("manual")
        self.manual_part = True
        return self

    # -- resolution ------------------------------------------------------------------------

    def box(self) -> Box:
        if self._box is None:
            self._resolve()
        assert self._box is not None
        return self._box

    @property
    def t_axis(self) -> Axis:
        self.box()
        assert self._t_axis is not None
        return self._t_axis

    @property
    def u_axis(self) -> Axis:
        self.box()
        assert self._u_axis is not None
        return self._u_axis

    @property
    def v_axis(self) -> Axis:
        self.box()
        assert self._v_axis is not None
        return self._v_axis

    @property
    def outline(self) -> Shape:
        self.box()
        assert self._outline is not None
        return self._outline

    @outline.setter
    def outline(self, shape: Shape) -> None:
        self._outline = shape

    def _resolve(self) -> None:
        t = self.material.t
        if self._on is not None and self._center is not None:
            raise LangError("on() and center() both given; one decides the thickness axis.", self.path)
        if self._on is not None:
            t_axis = self._on.axis
            if self._on.inward.sign > 0:
                t_lo, t_hi = self._on.value, self._on.value + t
            else:
                t_lo, t_hi = self._on.value - t, self._on.value
        elif self._center is not None:
            t_axis = self._center.axis
            t_lo, t_hi = self._center.value - t / 2, self._center.value + t / 2
        else:
            raise LangError("no placement: give on() or center().", self.path)
        u_axis, v_axis = _in_plane(t_axis)
        self._t_axis, self._u_axis, self._v_axis = t_axis, u_axis, v_axis

        lo: dict[Axis, float] = {t_axis: t_lo}
        hi: dict[Axis, float] = {t_axis: t_hi}
        scope_box = self.scope.box
        shape = self._shape.in_plane(u_axis, v_axis, self.path) if self._shape is not None else None
        contours = ContourLimits(
            [as_contour_limit(c) for c in self._limits if isinstance(c, (Contour, ContourLimit))],
            t_axis, t_lo, t_hi, u_axis, v_axis, self.path)
        axis: Axis
        # An axis an open contour limits goes last, after the one it runs along.
        for axis in sorted((u_axis, v_axis), key=lambda a: bool(contours.edges_on(a))):
            a, b = self._extent(axis, scope_box, shape, contours)
            a += self._inset
            b -= self._inset
            if b <= a:
                raise LangError(f"extent on {axis} is not positive ({a:g} to {b:g}).", self.path)
            lo[axis], hi[axis] = a, b
        if shape is not None:
            sb = shape.bounds
            self._outline = shape.moved(lo[u_axis] - sb[0], lo[v_axis] - sb[1])
        else:
            self._outline = box_shape(lo[u_axis], lo[v_axis], hi[u_axis], hi[v_axis])
        if contours.trims:
            # The board's box is what the contours leave of the outline.
            self._outline = contours.trim(self._outline)
            ob = self._outline.bounds
            lo[u_axis], lo[v_axis], hi[u_axis], hi[v_axis] = ob
        self._box = Box(lo, hi)
        if self._grain is None and self.material.grain:
            self._grain = self.scope.default_grain
        if self._grain is not None and self._grain == t_axis:
            raise LangError(f"grain {self._grain} is the thickness axis.", self.path)

    def _extent(self, axis: Axis, scope_box: Box | None, shape: Shape | None,
                contours: ContourLimits) -> tuple[float, float]:
        """The board's range on one in-plane axis, before the inset: from
        two limits; from one limit and an open contour's far side, a
        contour's stretch or the box side opposite; from a contour's
        stretch alone; from an explicit shape; or the enclosing box. The
        stretches closed contours leave then cut it down (tighter wins)."""
        values = self._limit_values(axis, scope_box)
        box_centre = (scope_box.lo[axis] + scope_box.hi[axis]) / 2 if scope_box is not None else None
        reference = sum(values) / len(values) if values else box_centre
        values += contours.values(axis, reference)
        edges = contours.edges_on(axis)
        stretch = contours.stretch(axis, values, box_centre)
        if len(values) + len(edges) > 2:
            raise LangError(f"more than two limits on {axis}.", self.path)
        if len(edges) > 1:
            raise LangError(f"two open contours limit {axis}; give one of them as a position.", self.path)
        room = stretch if stretch is not None else (
            (scope_box.lo[axis], scope_box.hi[axis]) if scope_box is not None else None)
        if len(values) == 2:
            a, b = sorted(values)
        elif edges:
            # The board keeps the side of its other limit, or of the middle
            # of its room, up to the contour; the trim then follows it.
            edge = edges[0]
            if values:
                near = values[0]
                edge.choose_side(near)
            elif room is not None:
                edge.choose_side((room[0] + room[1]) / 2)
                near = room[1] if edge.side > 0 else room[0]
            else:
                raise LangError(f"contour {edge.name!r} limits {axis}, but nothing gives the other end.",
                                self.path)
            a, b = sorted((near, edge.far()))
        elif len(values) == 1:
            v = values[0]
            if room is None:
                raise LangError(f"only one limit on {axis} and no enclosing box to supply the other.", self.path)
            centre = (room[0] + room[1]) / 2
            a, b = (v, room[1]) if v < centre else (room[0], v)
        elif stretch is not None:
            a, b = stretch
        elif shape is not None:
            # An explicit shape carries its own extent; it sits at the box
            # minimum, or at the origin without a box.
            base = scope_box.lo[axis] if scope_box is not None else 0.0
            size = shape.width if axis == self._u_axis else shape.height
            a, b = base, base + size
        elif scope_box is None:
            raise LangError(f"no limits on {axis} and no enclosing box.", self.path)
        else:
            a, b = scope_box.lo[axis], scope_box.hi[axis]
        if stretch is not None:
            a, b = max(a, stretch[0]), min(b, stretch[1])
        return a, b

    def _limit_values(self, axis: Axis, scope_box: Box | None) -> list[float]:
        values: list[float] = []
        for limit in self._limits:
            if isinstance(limit, (Contour, ContourLimit)):
                continue
            if isinstance(limit, (Board, PartLimit)):
                part, offset = (limit, 0.0) if isinstance(limit, Board) else (limit.part, limit.offset)
                lb = part.box()
                if part.t_axis != axis:
                    continue
                # the face of `part` nearest to this board's side of the box,
                # moved by `offset` into the part
                centre = ((scope_box.lo[axis] + scope_box.hi[axis]) / 2 if scope_box
                          else (lb.lo[axis] + lb.hi[axis]) / 2)
                if lb.hi[axis] <= centre:
                    values.append(lb.hi[axis] - offset)
                else:
                    values.append(lb.lo[axis] + offset)
                continue
            pos = as_pos(limit, f"between() limit {limit!r}")
            if pos.axis == axis:
                values.append(pos.value)
        if len(values) > 2:
            raise LangError(f"more than two limits on {axis}.", self.path)
        return values

    # -- faces ---------------------------------------------------------------------------------

    def face(self, name: str | Direction | Face) -> Face:
        if isinstance(name, Face):
            return name
        if isinstance(name, str) and name in ("inner", "outer"):
            return self._inner_outer(name)
        return Face(self, self.scope.frame.direction(name))

    def _inner_outer(self, which: str) -> Face:
        """The big face toward (inner) or away from (outer) the enclosing
        scope's centre; an error when the board straddles that centre."""
        b = self.box()
        t = self.t_axis
        sb = self.scope.box
        if sb is None:
            raise LangError(f"{which}: no enclosing box to decide inner and outer.", self.path)
        centre = (sb.lo[t] + sb.hi[t]) / 2
        if b.lo[t] < centre < b.hi[t]:
            raise LangError(f"{which} is ambiguous: the board straddles the centre on {t}.", self.path)
        toward_centre = self.scope.frame.direction_of(t, 1 if centre > b.hi[t] else -1)
        return Face(self, toward_centre if which == "inner" else -toward_centre)

    @property
    def front(self) -> Face:
        return self.face("front")

    @property
    def back(self) -> Face:
        return self.face("back")

    @property
    def left(self) -> Face:
        return self.face("left")

    @property
    def right(self) -> Face:
        return self.face("right")

    @property
    def top(self) -> Face:
        return self.face("top")

    @property
    def bottom(self) -> Face:
        return self.face("bottom")

    @property
    def inner(self) -> Face:
        return self.face("inner")

    @property
    def outer(self) -> Face:
        return self.face("outer")

    @property
    def show_face(self) -> Face:
        if self._show is not None:
            return self.face(self._show)
        try:
            return self.face("outer")
        except LangError:
            return Face(self, self.scope.frame.direction_of(self.t_axis, 1))

    def big_faces(self) -> tuple[Face, Face]:
        return (Face(self, self.scope.frame.direction_of(self.t_axis, 1)),
                Face(self, self.scope.frame.direction_of(self.t_axis, -1)))

    @property
    def machine_face(self) -> Face:
        """The big face the board is machined from, the one that faces up
        on the machine: the one more pockets, holes and chamfers are made
        from (a cut's chamfer is on the show face), or the show face when
        both carry as many. Through cuts and operations on narrow faces do
        not count."""
        counts: dict[str, int] = {}
        for op in self.ops:
            if isinstance(op, (Pocket, Hole, Chamfer, VGroove)):
                face = op.face
            elif isinstance(op, Cut) and op.chamfer:
                face = self.show_face.world_name
            else:
                continue
            counts[face] = counts.get(face, 0) + 1
        show = self.show_face
        other = next(f for f in self.big_faces() if f.direction != show.direction)
        return other if counts.get(other.world_name, 0) > counts.get(show.world_name, 0) else show

    def has_operation(self, name: str) -> bool:
        return name in self._named_ops

    def op(self, name: str) -> Operation:
        """A named operation, e.g. the cut called "toekick"."""
        try:
            return Operation(self, name, self._named_ops[name])
        except KeyError:
            raise LangError(f"no operation named {name!r}.", self.path) from None

    def __getattr__(self, name: str) -> Any:
        """Named operations are reachable as attributes (`left.toekick`)."""
        named: dict[str, Op] = self.__dict__.get("_named_ops", {})
        if name in named:
            return Operation(self, name, named[name])
        raise AttributeError(name)

    # -- 2D frames ------------------------------------------------------------------------------

    def face_axes(self, face: Face) -> tuple[Axis, Axis]:
        """The two world axes of a face's 2D frame: for a big face the
        outline's (u, v), for a narrow face (s along the face, t across the
        thickness)."""
        if face.is_big:
            return (self.u_axis, self.v_axis)
        s_axis = self.v_axis if face.axis == self.u_axis else self.u_axis
        return (s_axis, self.t_axis)

    def _anchor(self, at: Anchor | Edge | None) -> Anchor:
        if at is None:
            return self.show_face.center
        if isinstance(at, Edge):
            at = at.anchor              # the middle of the edge
        if at.part is not self:
            raise LangError(f"at= names a point on {at.part.path}, not on this board.", self.path)
        return at

    def _place_shape(self, shape: Shape, anchor: Anchor) -> Shape:
        """The shape in the frame of the anchor's face, with its matching
        side or corner on the anchor's point."""
        ua, va = self.face_axes(anchor.face)
        placed = shape.in_plane(ua, va, self.path)
        point, shape_anchor = anchor.resolve()
        su, sv = placed.anchor_point(shape_anchor)
        return placed.moved(point[0] - su, point[1] - sv)

    def _depth(self, face: Face, depth: DepthSpec) -> tuple[float, str, bool]:
        """Depth in mm from `face`, its spec as text, and whether it goes through."""
        t = self.thickness
        if isinstance(depth, Through):
            return t, "through", True
        if isinstance(depth, ToFace):
            target = self.face(depth.face)
            if target.axis != face.axis:
                raise LangError(f"depth to({depth.face!r}) is not opposite the face the operation is on.", self.path)
            if target.direction == face.direction:
                raise LangError(f"depth to({depth.face!r}) names the face itself.", self.path)
            b = self.box()
            extent = b.hi[face.axis] - b.lo[face.axis]
            return extent + depth.offset, f"to({depth.face}, {depth.offset:g})", abs(depth.offset) < 1e-9
        if depth <= 0:
            raise LangError(f"depth must be positive, got {depth}.", self.path)
        return float(depth), f"{depth:g}", False

    # -- operations (ordered) -----------------------------------------------------------------

    def _record(self, op: Op, name: str | None) -> None:
        self.ops.append(op)
        if name:
            if name in self._named_ops:
                raise LangError(f"operation name {name!r} used twice.", self.path)
            self._named_ops[name] = op

    def cut(self, shape: Shape | Board | Box, at: Anchor | Edge | None = None, name: str | None = None,
            chamfer: float = 0.0) -> Self:
        """With a shape: a through cut at an anchor on a big face (the
        centre of the show face by default); it changes the outline. With
        a part or a box: removes the region that part occupies inside this
        board (its outline through its thickness) or that box covers; a
        pocket from the face the region enters through, or a through cut
        when it passes the whole thickness. Room around a part comes from
        `part.box().grown(...)`."""
        if isinstance(shape, (Board, Box)):
            if at is not None:
                raise LangError("cut(): at= is not used when cutting with a part or box.", self.path)
            return self._cut_region(shape, name, chamfer)
        anchor = self._anchor(at)
        if not anchor.face.is_big:
            raise LangError("cut(): a cut goes through the board; anchor it on a big face.", self.path)
        placed = self._place_shape(shape, anchor)
        self._cut_through(placed, name, chamfer)
        return self

    def _cut_through(self, placed: Shape, name: str | None, chamfer: float) -> None:
        cut = self.outline.difference(placed)
        if cut.is_empty():
            raise LangError("the cut removes the whole board.", self.path)
        if len(cut.polygons()) > len(self.outline.polygons()):
            raise LangError(f"the cut{f' {name}' if name else ''} splits the board in pieces.", self.path)
        self.outline = cut
        self._record(Cut(placed, name, chamfer), name)

    def _cut_region(self, region: Board | Box, name: str | None, chamfer: float) -> Self:
        b = self.box()
        t, u, v = self.t_axis, self.u_axis, self.v_axis
        rb = region.box() if isinstance(region, Board) else region
        label = region.path if isinstance(region, Board) else "box"
        if not b.overlaps(rb):
            raise LangError(f"cut(): {label} does not reach into this board.", self.path)
        overlap = b.intersection(rb)
        if isinstance(region, Box):
            shape = box_shape(rb.lo[u], rb.lo[v], rb.hi[u], rb.hi[v])
            t0, t1 = overlap.lo[t], overlap.hi[t]
        elif region.t_axis == t:
            # Parallel boards share the (u, v) frame: the outline as it is.
            shape = region.outline
            t0, t1 = overlap.lo[t], overlap.hi[t]
        else:
            # Perpendicular: the other board's plane contains this board's
            # thickness axis. Take its outline within this thickness, and
            # that section's extent along the axis the two planes share.
            ru, rv = region.u_axis, region.v_axis
            lo = {ru: rb.lo[ru], rv: rb.lo[rv]}
            hi = {ru: rb.hi[ru], rv: rb.hi[rv]}
            lo[t], hi[t] = b.lo[t], b.hi[t]
            strip = box_shape(lo[ru], lo[rv], hi[ru], hi[rv])
            section = region.outline.intersection(strip)
            if section.is_empty():
                raise LangError(f"cut(): {label} does not reach into this board.", self.path)
            s0, s1, s2, s3 = section.bounds
            bounds = {ru: (s0, s2), rv: (s1, s3)}
            free = rv if ru == t else ru              # the in-plane axis shared with this board
            span = {free: bounds[free], region.t_axis: (rb.lo[region.t_axis], rb.hi[region.t_axis])}
            shape = box_shape(span[u][0], span[v][0], span[u][1], span[v][1])
            t0, t1 = max(bounds[t][0], b.lo[t]), min(bounds[t][1], b.hi[t])
        eps = 1e-6
        if t0 <= b.lo[t] + eps and t1 >= b.hi[t] - eps:
            self._cut_through(shape, name, chamfer)
            return self
        if t1 >= b.hi[t] - eps:
            face = directions.frame.direction_of(t, 1)
            depth = b.hi[t] - t0
        elif t0 <= b.lo[t] + eps:
            face = directions.frame.direction_of(t, -1)
            depth = t1 - b.lo[t]
        else:
            raise LangError(
                f"cut(): {label} lies inside the thickness and reaches neither face; "
                "a pocket must start at a face.", self.path)
        # `face` is a world direction, as operations store their faces.
        self._record(Pocket(shape, face.name, depth, f"cut({label})", name, chamfer), name)
        return self

    def pocket(self, shape: Shape, at: Anchor | Edge | None = None, depth: DepthSpec | None = None,
               name: str | None = None, chamfer: float = 0.0) -> Self:
        """A pocket of `shape` from the face the anchor names (the centre of
        the show face by default), `depth` deep."""
        anchor = self._anchor(at)
        f = anchor.face
        if depth is None:
            raise LangError("pocket() needs a depth.", self.path)
        d, spec, _ = self._depth(f, depth)
        world = f.world_name
        if f.is_big:
            placed = self._place_shape(shape, anchor)
            self._record(Pocket(placed, world, d, spec, name, chamfer), name)
        else:
            sa, ta = self.face_axes(f)
            oriented = shape.in_plane(sa, ta, self.path)
            point, shape_anchor = anchor.resolve()
            su, sv = oriented.anchor_point(shape_anchor)
            self._record(EdgeOp(world, Pocket(oriented.moved(-su, -sv), world, d, spec, name, chamfer),
                                point[0], point[1]), name)
        return self

    def hole(self, d: float, at: Anchor | Edge | None = None, depth: DepthSpec | None = None,
             name: str | None = None, chamfer: float = 0.0) -> Self:
        """A hole of diameter `d` at the anchor's point, into the face the
        anchor names (the centre of the show face by default)."""
        anchor = self._anchor(at)
        f = anchor.face
        if depth is None:
            raise LangError("hole() needs a depth.", self.path)
        if d <= 0:
            raise LangError(f"hole diameter must be positive, got {d}.", self.path)
        dep, spec, thru = self._depth(f, depth)
        point, _ = anchor.resolve()
        world = f.world_name
        if f.is_big:
            self._record(Hole(point[0], point[1], float(d), world, dep, spec, name, chamfer, thru), name)
        else:
            self._record(EdgeOp(world, Hole(0.0, 0.0, float(d), world, dep, spec, name, chamfer, thru),
                                point[0], point[1]), name)
        return self

    def chamfer(self, what: Edge | Outline | Operation | Op, size: float) -> Self:
        """A chamfer along an edge (`side.front.inner`), along a face's
        outline (`side.outer.outline`), or along a named operation of this
        board (`side.toekick`)."""
        if isinstance(what, Operation):
            what = what.op
        if isinstance(what, Edge):
            if what.part is not self:
                raise LangError(f"chamfer(): {what!r} is not an edge of this board.", self.path)
            self._record(Chamfer(what.world_name, float(size), what.a.world_name), None)
        elif isinstance(what, Outline):
            if what.face.part is not self:
                raise LangError(f"chamfer(): {what.face!r} is not a face of this board.", self.path)
            self._record(Chamfer("outline", float(size), what.face.world_name), None)
        else:
            name = next((n for n, op in self._named_ops.items() if op is what), None)
            if name is None:
                raise LangError("chamfer(): the operation is not a named operation of this board.", self.path)
            face = self.show_face.world_name if isinstance(what, Cut) else what.face
            self._record(Chamfer(name, float(size), face), None)
        return self

    # -- operations at computed positions (joints and hardware) ------------------------------------

    def _big_face_of_mine(self, face: Face, what: str) -> None:
        if face.part is not self:
            raise LangError(f"{what}: {face!r} is not a face of this board.", self.path)
        if not face.is_big:
            raise LangError(f"{what}: {face!r} is a narrow face; this takes a big face.", self.path)

    def add_pocket(self, face: Face, shape: Shape, depth: DepthSpec, name: str | None = None) -> Self:
        """A pocket from a big face with `shape` already placed in the face's
        frame (world coordinates on the outline's two axes, see `face_axes`).
        For joints and hardware, which compute positions themselves; build
        files use `pocket()`."""
        self._big_face_of_mine(face, "add_pocket()")
        d, spec, _ = self._depth(face, depth)
        self._record(Pocket(shape, face.world_name, d, spec, name), name)
        return self

    def add_cut(self, shape: Shape, name: str | None = None) -> Self:
        """A through cut with `shape` already in the outline's frame (world
        coordinates on its two axes); see `add_pocket`."""
        self._cut_through(shape, name, 0.0)
        return self

    def add_to_outline(self, shape: Shape) -> Self:
        """Widens the outline by `shape`, in the outline's frame: material a
        joint adds, such as tenons growing out of the board's end. The
        board's box, its placement, stays as it was."""
        self.outline = self.outline.union(shape)
        return self

    def add_hole(self, face: Face, point: Point2, d: float, depth: DepthSpec, name: str | None = None) -> Self:
        """A hole into a big face at `point` in the face's frame; see
        `add_pocket`."""
        self._big_face_of_mine(face, "add_hole()")
        if d <= 0:
            raise LangError(f"hole diameter must be positive, got {d}.", self.path)
        dep, spec, thru = self._depth(face, depth)
        self._record(Hole(point[0], point[1], float(d), face.world_name, dep, spec, name, 0.0, thru), name)
        return self

    def add_vgroove(self, face: Face, start: Point2, end: Point2, depth: float, name: str | None = None) -> Self:
        """A 90 degree V-groove into a big face along the line from `start`
        to `end` in the face's frame, `depth` deep; see `add_pocket`."""
        self._big_face_of_mine(face, "add_vgroove()")
        if depth <= 0 or depth >= self.thickness:
            raise LangError(f"a V-groove must be between 0 and the board's thickness deep, got {depth:g}.",
                            self.path)
        if abs(start[0] - end[0]) + abs(start[1] - end[1]) < 1e-9:
            raise LangError("a V-groove needs two different ends.", self.path)
        self._record(VGroove(start[0], start[1], end[0], end[1], face.world_name, float(depth), name), name)
        return self

    def unique_op_name(self, base: str) -> str:
        """`base`, or `base_2`, `base_3`... when this board already has an
        operation of that name."""
        name, n = base, 2
        while name in self._named_ops:
            name, n = f"{base}_{n}", n + 1
        return name

    # -- relations ---------------------------------------------------------------------------------

    def join(self, *partners: Board | Sequence[Board], using: Joint) -> Self:
        """Joins this board to the boards named, with a joint type:
        `bottom.join(left, right, using=cabineo(count=3))`,
        `long.join(battens, using=half_lap(toward=floor.top))`. Boards come
        one by one or in lists. Every board named must meet this one the
        way the joint needs (a contact for a connector, a crossing for a
        half lap); nothing is joined that is not named. The joint adds
        operations to both boards."""
        named: list[Board] = []
        for p in partners:
            named.extend([p] if isinstance(p, Board) else p)
        if not named:
            raise LangError("join(): name the boards to join, e.g. join(left, right, using=...).", self.path)
        for i, p in enumerate(named):
            if p is self:
                raise LangError("join(): a board cannot be joined to itself.", self.path)
            if any(q is p for q in named[:i]):
                raise LangError(f"join(): {p.path} is named twice.", self.path)
        using.join(self, named)
        return self

    # -- block form -------------------------------------------------------------------------------

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    # -- layout ---------------------------------------------------------------------------------------

    def to_layout(self) -> PartLayout:
        b = self.box()
        return {
            "path": self.path,
            "kind": "board",
            "material": self.material.label,
            "thickness": self.thickness,
            "axes": {"t": self.t_axis, "u": self.u_axis, "v": self.v_axis},
            "box": b.as_dict(),  # type: ignore[typeddict-item]
            "origin": [b.lo[a] for a in AXES],
            "outline": _rings(self.outline),
            "grain": self._grain,
            "show": self.show_face.world_name,
            "machine": self.machine_face.world_name,
            "grained": self.material.grain,
            "manual": self.manual_part,
            "ops": [_op_to_layout(op) for op in self.ops],
        }


@dataclass(frozen=True)
class PartLimit:
    """A part as a `between()` limit with its nearest face moved: a
    positive `offset` into the part (`part.into(n)`), a negative one away
    from it (`part.gap(n)`)."""
    part: Board
    offset: float


def _in_plane(t_axis: Axis) -> tuple[Axis, Axis]:
    others: list[Axis] = [a for a in AXES if a != t_axis]
    return others[0], others[1]


def _rings(shape: Shape) -> Rings:
    return [[[u, v] for u, v in ring] for ring in shape.rings()]


def _op_to_layout(op: Op) -> OpLayout:
    if isinstance(op, Cut):
        cut: CutLayout = {"kind": "cut", "name": op.name, "chamfer": op.chamfer, "shape": _rings(op.shape)}
        return cut
    if isinstance(op, Pocket):
        pocket: PocketLayout = {"kind": "pocket", "name": op.name, "face": op.face, "depth": op.depth,
                                "depth_spec": op.depth_spec, "chamfer": op.chamfer, "shape": _rings(op.shape)}
        return pocket
    if isinstance(op, Hole):
        hole: HoleLayout = {"kind": "hole", "name": op.name, "face": op.face, "u": op.u, "v": op.v, "d": op.d,
                            "depth": op.depth, "depth_spec": op.depth_spec, "through": op.through,
                            "chamfer": op.chamfer}
        return hole
    if isinstance(op, Chamfer):
        chamfer: ChamferLayout = {"kind": "chamfer", "what": op.what, "size": op.size, "face": op.face}
        return chamfer
    if isinstance(op, VGroove):
        groove: VGrooveLayout = {"kind": "vgroove", "name": op.name, "face": op.face, "start": [op.u0, op.v0],
                                 "end": [op.u1, op.v1], "depth": op.depth}
        return groove
    inner = _op_to_layout(op.op)
    assert inner["kind"] in ("hole", "pocket")
    edge: EdgeOpLayout = {"kind": "edge", "face": op.face, "s": op.s, "t": op.t,
                          "op": inner}  # type: ignore[typeddict-item]
    return edge


def board(name: str, material: Material, shape: Shape | None = None) -> Board:
    return Board(name, material, shape)
