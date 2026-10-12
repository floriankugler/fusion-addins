"""Parts: boards with placement modifiers, faces and operations.

A board is created with its identity (`board(name, material)`), placed with
order-free modifiers (`on`, `between`, `center`, `inset`, `grain`, `show`,
`manual`) and machined with ordered operations (`cut`, `pocket`, `hole`,
`chamfer`, `fillet`). Every modifier returns the board. Placement is
resolved lazily the first time a face, the box or the layout is asked for;
from then on the placement modifiers are frozen.

A fillet (`panel.fillet(panel.front.left, 20)`, see `corners.py`) rounds
corners of the outline through the board, and a chamfer on an edge through
the board cuts one off; like a cut, each changes the outline at once.

A cutout (`side.cutout()`, see `cutouts.py`) opens up a face inside a
border, keeping material around everything the board has so far; it is an
ordered operation like the others, so it goes after the joins whose holes
it must spare, and an operation made later inside one of its openings is
an error.

Dog bones (`side.dogbones()`, see `dogbones.py`) are an ordered operation
too: they go into the inside corners the board has where the call is
written, so a board relieves its corners after the cuts and joins that
make them.

Faces and edges are properties named by direction (`side.front`,
`side.front.inner`), so editors can complete them; project aliases go
through `face()` and `edge()`. A point on a face for `at=` is named
through the face: `side.inner.front(37).bottom(z)` is 37 mm behind the
front edge of the inner face at height `z`, `side.outer.bottom.front` the
corner. `Face`, `Edge`, `Anchor`, `Outline` and `Operation` live in
`faces.py` and are imported from here too.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from collections.abc import Sequence
from typing import Literal, Protocol, Self, Union

from shapely.geometry import LineString, Point, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

from lib import cutout_patterns as cutout_data

from . import corners as corner_geometry
from . import cutouts as cutout_geometry
from . import directions
from . import dogbones as dogbone_geometry
from . import scope as scopes
from .box import Box
from .contours import Contour, ContourLimit, ContourLimits, as_contour_limit
from .directions import AXES, Axis, Direction, ExtentName, InnerOuter
from .errors import LangError, one_of
from .faces import Anchor, Edge, Face, Operation, Outline
from .geometry import parts_of
from .layout_types import (ChamferLayout, CutLayout, EdgeOpLayout, HoleLayout, OpLayout,
                           PartLayout, PocketLayout, Rings, VGrooveLayout)
from .material import Material
from .ops import Chamfer, Cut, EdgeOp, Hole, Op, Pocket, VGroove
from .refs import Affine, DepthSpec, HasPosition, Pos, PosLike, Side, Through, ToFace, as_pos, through
from .shapes import Shape, box_shape

Point2 = tuple[float, float]
#: How far a point may lie off a face and still be on it, mm (the add-ins'
#: 1e-4 cm): `hole_fits`.
ON_FACE_TOLERANCE = 1e-3
#: What `between()` takes: positions, box sides, faces, parts (their nearest
#: face), contours, and boxes (their sides on the board's in-plane axes).
Limit = Union[Pos, Affine, HasPosition, "Board", "PartLimit", Contour, ContourLimit, Box]
#: What `dogbones(at=)` takes: a named operation itself (not its name), a big face, the outline.
DogBoneTarget = Union["Operation", "Face", "Outline"]
#: What `fillet()` rounds: the corner an edge through the board names, the
#: corners a named through cut made, every corner of the outline.
CornerTarget = Union["Edge", "Operation", "Outline"]
#: What `chamfer()` takes: an edge, a face's outline, a named operation.
ChamferTarget = Union["Edge", "Outline", "Operation", Op]


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
        if shape is not None:
            self._check_area(shape, "board()")
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
        #: The openings of the cutouts made so far, by operation name.
        self._cutouts: list[tuple[str, BaseGeometry]] = []
        #: Notes for the layout's problems, such as cutout pieces left out.
        self.notes: list[str] = []

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
        """Limits on the in-plane axes: positions, box sides, faces, parts,
        contours or boxes. A part means its face toward the board: the face
        toward the other limit on that axis, or toward the middle of the
        enclosing box when it is the only one; `part.into(n)` and
        `part.gap(n)` move that face. A box gives both ends on each
        in-plane axis, `between(drawer_box)`. Missing limits default to the
        enclosing scope's box. A limit that limits neither in-plane axis (a
        position on the thickness axis, a board parallel to this one) is an
        error."""
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
            self._grain = self.scope.frame.axis_of_extent(one_of(along, ExtentName, "grain()", self.path))
        else:
            self._grain = along.axis
        return self

    def show(self, face: Face | Side | Direction | InnerOuter) -> Self:
        """The visible big face: `"inner"` or `"outer"` relative to the
        enclosing box, a box side or direction (`show(cab.front)`), or one
        of this board's own faces (`side.show(side.inner)`)."""
        self._placement("show")
        if isinstance(face, str):
            self._show = one_of(face, InnerOuter, "show()", self.path)
        else:
            if isinstance(face, Face):
                if face.part is not self:
                    raise LangError(f"show(): {face!r} is not a face of this board.", self.path)
                d = face.direction
            else:
                d = face.outward if isinstance(face, Side) else face
            # named in this board's frame, also for a side of an enclosing box
            self._show = self.scope.frame.direction_of(d.axis, d.sign)
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
        used: set[int] = set()
        # An axis an open contour limits goes last, after the one it runs along.
        for axis in sorted((u_axis, v_axis), key=lambda a: bool(contours.edges_on(a))):
            a, b = self._extent(axis, scope_box, shape, contours, used)
            a += self._inset
            b -= self._inset
            if b <= a:
                raise LangError(f"extent on {axis} is not positive ({a:g} to {b:g}).", self.path)
            lo[axis], hi[axis] = a, b
        self._check_limits_used(used, t_axis)
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
                contours: ContourLimits, used: set[int]) -> tuple[float, float]:
        """The board's range on one in-plane axis, before the inset: from
        two limits; from one limit and an open contour's far side, a
        contour's stretch or the box side opposite; from a contour's
        stretch alone; from an explicit shape; or the enclosing box. The
        stretches closed contours leave then cut it down (tighter wins)."""
        values = self._limit_values(axis, scope_box, used)
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

    def _limit_values(self, axis: Axis, scope_box: Box | None, used: set[int]) -> list[float]:
        """The limits' values on one in-plane axis; the indexes of the limits
        that gave one go into `used`. A part gives the face toward the
        other limit on the axis, or toward the middle of the enclosing box
        when there is none (or two others, which is an error below)."""
        values: list[float] = []
        parts: list[tuple[int, Board, float]] = []
        for i, limit in enumerate(self._limits):
            if isinstance(limit, (Contour, ContourLimit)):
                used.add(i)                 # contours check themselves (`ContourLimits`)
                continue
            if isinstance(limit, Box):
                values += [limit.lo[axis], limit.hi[axis]]
                used.add(i)
                continue
            if isinstance(limit, (Board, PartLimit)):
                part, offset = (limit, 0.0) if isinstance(limit, Board) else (limit.part, limit.offset)
                if part.t_axis == axis:
                    parts.append((i, part, offset))
                continue
            pos = as_pos(limit, f"between() limit {limit!r}")
            if pos.axis == axis:
                values.append(pos.value)
                used.add(i)
        positions = list(values)
        for i, part, offset in parts:
            lb = part.box()
            others = positions + [(p.box().lo[axis] + p.box().hi[axis]) / 2 for j, p, _ in parts if j != i]
            if len(others) == 1:
                toward = others[0]
            elif scope_box is not None:
                toward = (scope_box.lo[axis] + scope_box.hi[axis]) / 2
            else:
                toward = (lb.lo[axis] + lb.hi[axis]) / 2
            # the face toward `toward`, moved by `offset` into the part
            values.append(lb.hi[axis] - offset if toward >= (lb.lo[axis] + lb.hi[axis]) / 2 else lb.lo[axis] + offset)
            used.add(i)
        if len(values) > 2:
            raise LangError(f"more than two limits on {axis}.", self.path)
        return values

    def _check_limits_used(self, used: set[int], t_axis: Axis) -> None:
        """An error for a `between()` limit that limited neither in-plane
        axis, which would otherwise be dropped without a word."""
        for i, limit in enumerate(self._limits):
            if i in used:
                continue
            if isinstance(limit, (Board, PartLimit)):
                part = limit if isinstance(limit, Board) else limit.part
                raise LangError(f"between(): {part.path} is parallel to this board, so it limits neither of its "
                                f"in-plane axes; name the boards it lies between.", self.path)
            raise LangError(f"between(): {limit!r} lies on the board's thickness axis ({t_axis}), so it limits "
                            "nothing; the thickness comes from on() or center().", self.path)

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

    def __getattr__(self, name: str) -> Operation:
        """Named operations are reachable as attributes (`left.toekick`); a
        misspelt method name is then an `Operation` to the type checker,
        which reports the call."""
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

    def _check_area(self, shape: Shape, what: str) -> None:
        """An error for a shape without area, such as what a difference
        leaves of a shape inside another: an operation with it would do
        nothing, and nothing would say so."""
        if shape.is_empty() or shape.area <= 1e-6:
            raise LangError(f"{what}: the shape is empty (it has no area), so it would do nothing.", self.path)

    def _place_shape(self, shape: Shape, anchor: Anchor) -> Shape:
        """The shape in the frame of the anchor's face, with its matching
        side or corner on the anchor's point."""
        ua, va = self.face_axes(anchor.face)
        placed = shape.in_plane(ua, va, self.path)
        point, shape_anchor = anchor.resolve()
        su, sv = placed.anchor_point(shape_anchor)
        return placed.moved(point[0] - su, point[1] - sv)

    def _depth(self, face: Face, depth: DepthSpec) -> tuple[float, str, bool]:
        """Depth in mm from `face`, its spec as text, and whether it goes
        through. Through and `to()` measure the board from `face` to the
        opposite face: its thickness from a big face, its length or width
        from a narrow one. A depth reaching past the opposite face is an
        error."""
        b = self.box()
        extent = b.hi[face.axis] - b.lo[face.axis]
        if isinstance(depth, Through):
            return extent, "through", True
        if isinstance(depth, ToFace):
            if depth.part is not None and depth.part is not self:
                path = getattr(depth.part, "path", repr(depth.part))
                raise LangError(f"depth to({path}.{depth.face}) names a face of another part; to() reaches a "
                                "face of the board the operation is on.", self.path)
            target = self.face(depth.face)
            if target.axis != face.axis:
                raise LangError(f"depth to({depth.face!r}) is not opposite the face the operation is on.", self.path)
            if target.direction == face.direction:
                raise LangError(f"depth to({depth.face!r}) names the face itself.", self.path)
            if depth.offset > 1e-9:
                raise LangError(f"depth to({depth.face!r}, {depth.offset:g}) reaches past that face, out of the "
                                "board; use through, or a negative offset to stop short of it.", self.path)
            return extent + depth.offset, f"to({depth.face}, {depth.offset:g})", abs(depth.offset) < 1e-9
        if depth <= 0:
            raise LangError(f"depth must be positive, got {depth}.", self.path)
        if depth > extent + 1e-6:
            raise LangError(f"depth {depth:g} reaches past the opposite face, {extent:g} from the {face.name} "
                            "face; use through to go all the way.", self.path)
        return float(depth), f"{depth:g}", False

    # -- operations (ordered) -----------------------------------------------------------------

    def _record(self, op: Op, name: str | None) -> None:
        if self._cutouts and not isinstance(op, Chamfer):
            footprint = self._footprint(op)
            for cutout, opening in self._cutouts:
                if footprint.intersection(opening).area > 1e-6:
                    what = f"the {op.kind} {name!r}" if name else f"a {op.kind}"
                    raise LangError(
                        f"{what} lies in the cutout {cutout!r}, which was made before it: make the cutout "
                        "after it, or keep material there with keep=.", self.path)
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
        self._check_area(shape, "cut()")
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
        self._record(Cut(placed, name, chamfer), name)       # may refuse it; then the outline stays
        self.outline = cut

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

    def pocket(self, shape: Shape, at: Anchor | Edge | None = None, *, depth: DepthSpec,
               name: str | None = None, chamfer: float = 0.0) -> Self:
        """A pocket of `shape` from the face the anchor names (the centre of
        the show face by default), `depth` deep."""
        self._check_area(shape, "pocket()")
        anchor = self._anchor(at)
        f = anchor.face
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

    def hole(self, d: float, at: Anchor | Edge | None = None, *, depth: DepthSpec,
             name: str | None = None, chamfer: float = 0.0) -> Self:
        """A hole of diameter `d` at the anchor's point, into the face the
        anchor names (the centre of the show face by default), `depth`
        deep."""
        anchor = self._anchor(at)
        f = anchor.face
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

    def chamfer(self, what: ChamferTarget | Sequence[ChamferTarget], size: float) -> Self:
        """A chamfer along an edge (`side.front.inner`), along a face's
        outline (`side.outer.outline`), or along a named operation of this
        board (`side.toekick`); or along each of a list of them.

        An edge through the board, where two narrow faces meet
        (`panel.front.left` on a board lying flat, `side.front.bottom` on
        one standing), is a corner of the outline: the chamfer cuts it off,
        `size` along both its edges, and changes the outline at once, as
        `fillet()` rounds a corner (see there)."""
        items: list[object] = list(what) if isinstance(what, (list, tuple)) else [what]
        corners = [e for e in items if isinstance(e, Edge) and e.part is self and e.through]
        if corners:
            if size <= 0:
                raise LangError(f"chamfer(): the size must be positive, got {size:g}.", self.path)
            named = self._outline_corners(corners, "chamfer")
            self._reshape(corner_geometry.clip_corners(self.outline, named, float(size), self.path),
                          f"chamfer({size:g})")
        for item in items:
            if not any(item is e for e in corners):
                self._chamfer_along(item, float(size))
        return self

    def _chamfer_along(self, what: object, size: float) -> None:
        """A chamfer along an edge of a big face, a face's outline or an
        operation's contour, recorded as an operation."""
        if isinstance(what, Operation):
            what = what.op
        if isinstance(what, Edge):
            if what.part is not self:
                raise LangError(f"chamfer(): {what!r} is not an edge of this board.", self.path)
            self._record(Chamfer(what.world_name, size, what.a.world_name), None)
        elif isinstance(what, Outline):
            if what.face.part is not self:
                raise LangError(f"chamfer(): {what.face!r} is not a face of this board.", self.path)
            self._record(Chamfer("outline", size, what.face.world_name), None)
        elif isinstance(what, VGroove):
            raise LangError("chamfer(): a V-groove has no rim to chamfer; its flanks are 45 degrees already.",
                            self.path)
        elif isinstance(what, (Cut, Pocket, Hole, EdgeOp)):
            name = next((n for n, op in self._named_ops.items() if op is what), None)
            if name is None:
                raise LangError("chamfer(): the operation is not a named operation of this board.", self.path)
            face = self.show_face.world_name if isinstance(what, Cut) else what.face
            self._record(Chamfer(name, size, face), None)
        else:
            raise LangError(f"chamfer() takes edges, outlines and operations themselves, not {what!r}.", self.path)

    def fillet(self, what: CornerTarget | Sequence[CornerTarget], radius: float) -> Self:
        """Rounds corners of the outline with `radius`, through the
        board: the corner where two narrow faces meet (`panel.front.left`
        on a board lying flat, `side.front.bottom` on one standing), the
        corners a named through cut made in the outline (`panel.notch`),
        every corner of the outline's outer boundary (`panel.top.outline`),
        or each of a list of them. A convex corner loses material, a
        concave one gains it; the arcs are exact and tangent to the edges,
        as `Shape.rounded()` makes them (see `lang.core.corners`).

        It changes the outline at once, as a cut does, so everything after
        it meets the rounded corners: contacts and the joints made on them,
        the checks, dog bones. A corner must exist when it is named (a cut,
        a joint, or an earlier fillet or chamfer may have taken it); a
        radius too large for the edges next to a corner, or one taking
        material where an operation made before it lies, is an error. The
        edges along a big face (`panel.front.top`) are not rounded:
        roundovers are not modeled; chamfer them."""
        if radius <= 0:
            raise LangError(f"fillet(): the radius must be positive, got {radius:g}.", self.path)
        items: list[object] = list(what) if isinstance(what, (list, tuple)) else [what]
        named = self._outline_corners(items, "fillet")
        self._reshape(corner_geometry.round_corners(self.outline, named, float(radius), self.path),
                      f"fillet({radius:g})")
        return self

    def _outline_corners(self, items: Sequence[object], method: str) -> list[corner_geometry.Named]:
        """The corners of the outline that `items` name for `method`
        (`fillet` or `chamfer`): edges through the board, the corners of
        named through cuts, every corner of the outline's outer boundary.
        An error for anything else and for a corner the outline no longer
        has."""
        what = f"{method}()"
        if not items:
            raise LangError(f"{what}: name the corners, e.g. {method}({self.name}.{self._corner_example()}, ...).",
                            self.path)
        found = corner_geometry.find(self.outline)
        u, v = self.u_axis, self.v_axis

        def where(p: Point2) -> str:
            return f"{u} {p[0]:g}, {v} {p[1]:g}"

        named: list[corner_geometry.Named] = []
        for item in items:
            if isinstance(item, str):
                raise LangError(f"{what} takes edges, operations and outlines themselves, not the name {item!r}: "
                                f"write {self.name}.{self._corner_example()} or {self.name}.{item}.", self.path)
            if isinstance(item, Edge):
                named.append(self._edge_corner(item, found, method))
            elif isinstance(item, Outline):
                face = item.face
                if face.part is not self:
                    raise LangError(f"{what}: {face!r} is not a face of this board.", self.path)
                if not face.is_big:
                    raise LangError(f"{what}: {face!r} is a narrow face; name a big face's outline.", self.path)
                corners = [p for p, outer in found if outer]
                if not corners:
                    raise LangError(f"{what}: the outline has no corners (it is round).", self.path)
                named += [corner_geometry.Named(p, f"the outline's corner at {where(p)}") for p in corners]
            elif isinstance(item, Operation):
                if item.part is not self:
                    raise LangError(f"{what}: {item!r} is not an operation of this board.", self.path)
                op = item.op
                if not isinstance(op, Cut):
                    raise LangError(f"{what}: the {op.kind} {item.name!r} is not a through cut, so it made no corners "
                                    "of the outline; give a pocket's shape round corners with rounded().", self.path)
                contour = op.shape.geometry.boundary
                corners = [p for p, _ in found if contour.distance(Point(p)) <= corner_geometry.ON_CONTOUR]
                if not corners:
                    raise LangError(f"{what}: the cut {item.name!r} left no corners in the outline (it is round, "
                                    "or later cuts took them).", self.path)
                named += [corner_geometry.Named(p, f"the corner of {item.name!r} at {where(p)}") for p in corners]
            else:
                raise LangError(f"{what} takes edges through the board, through cuts and outlines, not {item!r}.",
                                self.path)
        unique: list[corner_geometry.Named] = []
        for c in named:
            if not any(math.dist(c.point, d.point) <= 1e-6 for d in unique):
                unique.append(c)
        return unique

    def _edge_corner(self, edge: Edge, found: list[tuple[Point2, bool]], method: str) -> corner_geometry.Named:
        """The corner of the outline an edge through the board names: the
        corner of the board's box where its two faces meet."""
        what = f"{method}()"
        if edge.part is not self:
            raise LangError(f"{what}: {edge!r} is not an edge of this board.", self.path)
        if not edge.through:
            big = edge.a if edge.a.is_big else edge.b
            raise LangError(
                f"{what}: {edge.name} runs along the {big.name} face, not through the board. A fillet rounds a "
                f"corner of the outline, where two narrow faces meet ({self._corner_example()}); roundovers along "
                "a face are not modeled, chamfer() the edge instead.", self.path)
        b = self.box()
        coords = {f.axis: (b.hi[f.axis] if f.direction.sign > 0 else b.lo[f.axis]) for f in (edge.a, edge.b)}
        point = (coords[self.u_axis], coords[self.v_axis])
        match = next((p for p, _ in found if math.dist(p, point) <= 1e-6), None)
        if match is None:
            raise LangError(
                f"{what}: the outline has no corner at {edge.name} any more: a cut or a joint, or an earlier fillet "
                f"or chamfer took it. The corners a cut made are named by the cut, {method}({self.name}.<cut>, ...).",
                self.path)
        return corner_geometry.Named(match, edge.name)

    def _corner_example(self) -> str:
        """The name of an edge through this board, for messages: front.left
        on a board lying flat, front.bottom on one standing."""
        frame = self.scope.frame
        return f"{frame.direction_of(self.u_axis, -1).name}.{frame.direction_of(self.v_axis, -1).name}"

    def _reshape(self, shape: Shape, what: str) -> None:
        """Makes `shape`, the outline with corners rounded or cut off, the
        outline. An error when that takes material where an operation made
        before lies (a pocket, hole or groove, a joint's), as the operation
        would then hang over the new edge; through cuts are the outline's own."""
        removed = self.outline.geometry.difference(shape.geometry)
        for op in self.ops:
            if isinstance(op, (Cut, Chamfer)):
                continue
            if self._footprint(op).intersection(removed).area > 1e-6:
                inner = op.op if isinstance(op, EdgeOp) else op
                label = f"the {inner.kind} {inner.name!r}" if inner.name else f"a {inner.kind}"
                raise LangError(f"{what} takes material where {label} lies, which was made before it: make it "
                                "smaller, or make it first, before the operation or joint (connectors joined after "
                                "it keep to the shorter contact).", self.path)
        self.outline = shape

    def cutout(self, what: Face | Shape | None = None, at: Anchor | Edge | None = None, *,
               pattern: cutout_geometry.Pattern | None = None, border: float = cutout_data.OUTER_INSET,
               around: float = cutout_data.INNER_INSET, depth: DepthSpec = through,
               radius: float = cutout_data.FILLET_RADIUS, chamfer: float = 0.0,
               keep: Board | Box | Sequence[Board | Box] = (), name: str | None = None) -> Self:
        """Cuts out a big face inside a border, as the Face Cutout add-in
        does: `border=` mm of the outline stays, and `around=` mm around
        everything the board has so far (its holes and through cuts,
        pockets and holes in either big face, holes into its narrow faces,
        V-grooves), and around where the boards and boxes in `keep=` lie on
        it, such as a shelf meeting the board in the middle.

        `what` is the face to cut from, by default the big face that is
        not the show face (the inner face, usually the machined one, so the
        chamfer stays off the visible face), or a region shape placed with
        `at=` on a big face: then only that region is cut out, still inside
        the border. `pattern=` leaves more material: `cross(width)` or
        `triangles(columns, rows, spacing)`. `depth=` makes it a pocket
        (`to(side.outer, -3)` leaves 3 mm); `radius=` rounds every corner
        of the openings (0 leaves them sharp), and pieces too small for it
        are left out; `chamfer=` puts a 45 degree chamfer on their rims at
        the face cut from only.

        A cutout spares only what exists when it is made, so write it after
        the joins and holes it must leave material around; an operation
        made later inside an opening is an error. Without tabs, material
        kept around a feature in the middle of a through cutout would fall
        out, which is an error too."""
        for label, value in (("border", border), ("around", around), ("radius", radius), ("chamfer", chamfer)):
            if value < 0:
                raise LangError(f"cutout(): {label} must not be negative, got {value:g}.", self.path)
        face, region = self._cutout_face(what, at)
        d, spec, thru = self._depth(face, depth)
        if chamfer > 0 and chamfer >= d - 1e-9:
            raise LangError(f"cutout(): the chamfer ({chamfer:g}) must be smaller than the depth ({d:g}).",
                            self.path)
        name = name or self.unique_op_name("cutout")
        if name in self._named_ops:
            raise LangError(f"operation name {name!r} used twice.", self.path)

        exterior = unary_union([Polygon(p.exterior) for p in self.outline.polygons()])
        inset = cutout_geometry.grown(exterior, -border)
        if inset.is_empty:
            raise LangError(f"cutout(): border={border:g} leaves nothing of the face to cut out.", self.path)
        area = inset if region is None else inset.intersection(region)
        if area.is_empty:
            raise LangError("cutout(): the region lies outside the border.", self.path)
        kept = [(label, cutout_geometry.grown(g, around)) for label, g in self._kept_footprints(keep)]
        cut_region = area.difference(unary_union([g for _, g in kept])) if kept else area
        if cut_region.area <= 1e-6:
            raise LangError("cutout(): the material kept leaves nothing to cut out.", self.path)
        frame = self._pattern_frame(pattern, (region if region is not None else inset).bounds)
        result = cutout_geometry.openings(cut_region, frame, pattern, radius, self.path)
        if not result.pieces:
            raise LangError(f"cutout(): every piece is too small for radius={radius:g}.", self.path)
        opening = result.geometry
        shape = Shape(opening)
        if thru:
            self._check_islands(opening, kept, name)
            self._cut_through(shape, name, 0.0)
        else:
            self._record(Pocket(shape, face.world_name, d, spec, name), name)
        if chamfer > 0:
            self._record(Chamfer(name, float(chamfer), face.world_name), None)
        self._cutouts.append((name, opening))
        if result.dropped:
            self.notes.append(f"{self.path}: cutout {name!r} left out {result.dropped} piece(s) too small for "
                              f"the {radius:g} mm corner radius.")
        return self

    def _cutout_face(self, what: Face | Shape | None, at: Anchor | Edge | None) -> tuple[Face, BaseGeometry | None]:
        """The face a cutout is cut from and its region, if one is given."""
        if isinstance(what, Shape):
            self._check_area(what, "cutout()")
            anchor = self._anchor(at) if at is not None else self._default_cutout_face().center
            if not anchor.face.is_big:
                raise LangError("cutout(): place the region on a big face.", self.path)
            return anchor.face, self._place_shape(what, anchor).geometry
        if at is not None:
            raise LangError("cutout(): at= places a region shape; give the shape first.", self.path)
        if what is None:
            return self._default_cutout_face(), None
        if what.part is not self:
            raise LangError(f"cutout(): {what!r} is not a face of this board.", self.path)
        if not what.is_big:
            raise LangError(f"cutout(): {what!r} is a narrow face; a cutout is made from a big face.", self.path)
        return what, None

    def _default_cutout_face(self) -> Face:
        show = self.show_face
        return next(f for f in self.big_faces() if f.direction != show.direction)

    def _pattern_frame(self, pattern: cutout_geometry.Pattern | None,
                       bounds: tuple[float, float, float, float]) -> cutout_geometry.PatternFrame:
        """Where a pattern is laid out: the rectangle `bounds`, the columns
        along `along=` or the longer side, from the corner `start=` or the
        one at the bottom, front and left."""
        u0, v0, u1, v1 = bounds
        u, v = self.u_axis, self.v_axis
        columns: Literal[0, 1] = 0 if u1 - u0 >= v1 - v0 else 1
        start = [0, 0]
        for i, axis in enumerate((u, v)):
            d = next(self.scope.frame.direction(n) for n in ("bottom", "front", "left")
                     if self.scope.frame.direction(n).axis == axis)
            start[i] = d.sign
        if isinstance(pattern, cutout_geometry.Triangles):
            if pattern.along is not None:
                axis = self.scope.frame.axis_of_extent(pattern.along)
                if axis not in (u, v):
                    raise LangError(f"triangles(): along={pattern.along!r} is the board's thickness.", self.path)
                columns = 0 if axis == u else 1
            if pattern.start is not None:
                anchor = pattern.start
                if anchor.part is not self or not anchor.face.is_big:
                    raise LangError("triangles(): start= names a corner of a big face of this board.", self.path)
                _, corner = anchor.resolve()
                if not (corner.names_u and corner.names_v):
                    raise LangError("triangles(): start= must name a corner, e.g. side.inner.bottom.front.",
                                    self.path)
                start = [1 if corner.fu > 0.5 else -1, 1 if corner.fv > 0.5 else -1]
        return cutout_geometry.PatternFrame(bounds, columns, (start[0], start[1]))

    def _footprint(self, op: Op) -> BaseGeometry:
        """The area an operation takes up in the outline's frame."""
        if isinstance(op, (Cut, Pocket)):
            return op.shape.geometry
        if isinstance(op, Hole):
            return cutout_geometry.circle_geometry((op.u, op.v), op.d / 2 + op.chamfer)
        if isinstance(op, VGroove):
            return LineString([(op.u0, op.v0), (op.u1, op.v1)]).buffer(op.depth, cap_style="flat")
        if isinstance(op, EdgeOp):
            extents = Operation(self, "", op).extents()
            u, v = self.u_axis, self.v_axis
            return shapely_box(extents[u][0], extents[v][0], extents[u][1], extents[v][1])
        return Polygon()

    def _kept_footprints(self, keep: Board | Box | Sequence[Board | Box]) -> list[tuple[str, BaseGeometry]]:
        """What a cutout keeps material around, with a label each: the
        board's holes, its operations, and the boards and boxes in `keep`."""
        found: list[tuple[str, BaseGeometry]] = []
        for poly in self.outline.polygons():
            for hole in poly.interiors:
                g = Polygon(hole)
                cut = next((op for op in self.ops if isinstance(op, Cut) and op.shape.geometry.intersects(g)), None)
                found.append((f"the cut {cut.name!r}" if cut is not None and cut.name else "a hole", g))
        for op in self.ops:
            if isinstance(op, (Cut, Chamfer)):
                continue
            name = op.op.name if isinstance(op, EdgeOp) else op.name
            found.append((f"the {op.kind} {name!r}" if name else f"a {op.kind}", self._footprint(op)))
        u, v, t = self.u_axis, self.v_axis, self.t_axis
        for item in [keep] if isinstance(keep, (Board, Box)) else list(keep):
            if isinstance(item, Board):
                rb = item.box()
                g = (item.outline.geometry if item.t_axis == t
                     else shapely_box(rb.lo[u], rb.lo[v], rb.hi[u], rb.hi[v]))
                label = item.path
            else:
                g = shapely_box(item.lo[u], item.lo[v], item.hi[u], item.hi[v])
                label = "a box"
            if g.intersection(self.outline.geometry).area <= 1e-6:
                raise LangError(f"cutout(): keep= {label} does not lie on this board.", self.path)
            found.append((label, g))
        return found

    def _check_islands(self, opening: BaseGeometry, kept: list[tuple[str, BaseGeometry]], name: str) -> None:
        """A through cutout must not cut kept material free."""
        rest = self.outline.geometry.difference(opening)
        pieces = sorted(parts_of(rest), key=lambda g: -g.area)
        if len(pieces) <= len(self.outline.polygons()):
            return
        islands = pieces[len(self.outline.polygons()):]
        labels = [label for label, g in kept if any(g.intersects(i) for i in islands)]
        around = ", ".join(dict.fromkeys(labels)) or "material"
        raise LangError(f"the cutout {name!r} cuts the material kept around {around} free, and it would fall out: "
                        "keep it connected to the border with keep=, or cut out a region that leaves it out.",
                        self.path)

    def cutout_in(self, area: BaseGeometry) -> str | None:
        """The name of a cutout of this board with an opening in `area`
        (in the outline's frame), if any."""
        for name, opening in self._cutouts:
            if opening.intersection(area).area > 1e-6:
                return name
        return None

    def dogbones(self, tool: float = 6.0, relief: float = 0.1,
                 at: DogBoneTarget | Sequence[DogBoneTarget] | None = None) -> Self:
        """Dog bones in every inside corner of the board, as the
        dog_bones_native add-in makes them: a circle `relief` wider than
        the `tool`, on the corner's bisector, reaching just past the
        corner, through the board or as deep as the pocket the corner is
        in. `at=` limits them to the corners of named operations, given
        as the operations themselves (`side.toekick`), not their names, of
        a big face (`side.inner`: what it shows, through cuts and its own
        pockets, as when the add-in is given a face), or of the outline's
        outer boundary (`side.outer.outline`).

        Like every operation it acts where it is written: it relieves the
        corners the board has at the call, so it goes after the cuts and
        joins whose corners it should relieve [decided by Florian
        2026-10-12]; corners made later get none. Corners relieved already
        (by a joint's own dog bones, a hole over them, an earlier call) and
        rounded ones get none; see `lang.core.dogbones`. When a relief
        cannot be made (it would split the board), the board is left as it
        was."""
        if tool <= 0:
            raise LangError(f"dogbones(): tool must be positive, got {tool:g}.", self.path)
        if relief < 0:
            raise LangError(f"dogbones(): relief must not be negative, got {relief:g}.", self.path)
        targets: tuple[dogbone_geometry.Target, ...] | None = None
        if at is not None:
            items: list[object] = [at] if isinstance(at, (str, Operation, Face, Outline)) else list(at)
            if not items:
                raise LangError("dogbones(): at= is empty.", self.path)
            targets = tuple(self._dogbone_target(item) for item in items)
        request = dogbone_geometry.Request(float(tool), float(relief), targets)
        saved = self._state()
        try:
            self._relieve(request)
        except BaseException:
            self._restore(saved)
            raise
        return self

    def _relieve(self, request: dogbone_geometry.Request) -> None:
        """Cuts the reliefs a `dogbones()` call asks for into the corners
        the board has now: through cuts where a corner is one of the
        outline, else pockets as deep as what lies beside the corner."""
        for relief in dogbone_geometry.reliefs(self, request):
            shape = relief.shape
            for _, opening in self._cutouts:
                # A cutout's sharp corner: its opening is empty already.
                shape = shape.difference(Shape(opening))
            if shape.area <= 1e-9:
                continue
            name = self.unique_op_name(relief.name)
            if relief.face is None:
                self.add_cut(shape, name=name)
            else:
                face = next(f for f in self.big_faces() if f.world_name == relief.face)
                self.add_pocket(face, shape, through if relief.depth is None else relief.depth, name=name)

    def _dogbone_target(self, item: object) -> dogbone_geometry.Target:
        if isinstance(item, str):
            raise LangError(f"dogbones(at=) takes the operation itself, not its name {item!r}: "
                            f"write {self.name}.{item} (or {self.name}.op({item!r})) once the operation is made.",
                            self.path)
        if not isinstance(item, (Operation, Face, Outline)):
            raise LangError(f"dogbones(at=) takes operations, big faces or an outline, not {item!r}.", self.path)
        if isinstance(item, Operation):
            if item.part is not self:
                raise LangError(f"dogbones(at=): {item!r} is not an operation of this board.", self.path)
            return dogbone_geometry.Target("operation", item.name)
        face = item.face if isinstance(item, Outline) else item
        if face.part is not self:
            raise LangError(f"dogbones(at=): {face!r} is not a face of this board.", self.path)
        if isinstance(item, Outline):
            return dogbone_geometry.Target("outline")
        if not face.is_big:
            raise LangError(f"dogbones(at=): {face!r} is a narrow face; name a big face.", self.path)
        return dogbone_geometry.Target("face", face.world_name)

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
        self._check_area(shape, "add_pocket()")
        d, spec, _ = self._depth(face, depth)
        self._record(Pocket(shape, face.world_name, d, spec, name), name)
        return self

    def add_cut(self, shape: Shape, name: str | None = None) -> Self:
        """A through cut with `shape` already in the outline's frame (world
        coordinates on its two axes); see `add_pocket`."""
        self._check_area(shape, "add_cut()")
        self._cut_through(shape, name, 0.0)
        return self

    def add_edge_pocket(self, face: Face, shape: Shape, depth: float, name: str | None = None,
                        offset: float = 0.0) -> Self:
        """A pocket into a narrow face, `shape` already placed in the face's
        frame (world coordinates on its (s, t) axes, see `face_axes`),
        `depth` deep from a plane `offset` in front of the face; see
        `add_pocket`. A box joint's grooves along its fingers are cut so."""
        if face.part is not self:
            raise LangError(f"add_edge_pocket(): {face!r} is not a face of this board.", self.path)
        if face.is_big:
            raise LangError(f"add_edge_pocket(): {face!r} is a big face; this takes a narrow face.", self.path)
        if depth <= 0:
            raise LangError(f"depth must be positive, got {depth}.", self.path)
        self._check_area(shape, "add_edge_pocket()")
        world = face.world_name
        self._record(EdgeOp(world, Pocket(shape, world, float(depth), f"{depth:g}", name), offset=float(offset)),
                     name)
        return self

    def add_to_outline(self, shape: Shape) -> Self:
        """Widens the outline by `shape`, in the outline's frame: material a
        joint adds, such as tenons growing out of the board's end. The
        board's box, its placement, stays as it was."""
        self._check_area(shape, "add_to_outline()")
        self.outline = self.outline.union(shape)
        return self

    def add_hole(self, face: Face, point: Point2, d: float, depth: DepthSpec, name: str | None = None,
                 chamfer: float = 0.0) -> Self:
        """A hole into a big face at `point` in the face's frame; see
        `add_pocket`. A chamfer on its edge is a 90 degree countersink."""
        self._big_face_of_mine(face, "add_hole()")
        if d <= 0:
            raise LangError(f"hole diameter must be positive, got {d}.", self.path)
        dep, spec, thru = self._depth(face, depth)
        self._record(Hole(point[0], point[1], float(d), face.world_name, dep, spec, name, float(chamfer), thru), name)
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

    # -- where hardware fits on a face -------------------------------------------------------------

    def _taken_from(self, face: Face) -> list[BaseGeometry]:
        """What the operations took from a big face, in the outline's
        frame: the pockets, holes and V-grooves made into it (a hole with
        its countersink), and the pockets and holes through from the other
        face."""
        name = face.world_name
        taken: list[BaseGeometry] = []
        for op in self.ops:
            if isinstance(op, (Pocket, Hole, VGroove)) and op.face == name:
                taken.append(self._footprint(op))
            elif isinstance(op, (Pocket, Hole)) and op.depth >= self.thickness - 1e-9:
                taken.append(op.shape.geometry if isinstance(op, Pocket)
                             else cutout_geometry.circle_geometry((op.u, op.v), op.d / 2))
        return taken

    def face_region(self, face: Face) -> BaseGeometry:
        """A big face as an area in the outline's frame (see `face_axes`),
        where hardware can bear on it or drill into it: the outline less
        what the operations took from that face (`_taken_from`)."""
        self._big_face_of_mine(face, "face_region()")
        taken = self._taken_from(face)
        region = self.outline.geometry
        return region.difference(unary_union(taken)) if taken else region

    def hole_fits(self, face: Face, point: Point2, d: float) -> bool:
        """Whether a hole `d` across at `point` (in the face's frame) lies on
        the big face `face`: its centre and the four points its radius away
        along the face's axes on `face_region()`, give or take
        `ON_FACE_TOLERANCE`, as the add-ins probe a face (`isPointOnFace`),
        and its circle clear of the holes, pockets and V-grooves made
        before. Hardware checks every hole with it before it drills one."""
        self._big_face_of_mine(face, "hole_fits()")
        taken = self._taken_from(face)
        region = self.outline.geometry.difference(unary_union(taken)) if taken else self.outline.geometry
        u, v = point
        r = d / 2
        probes = [(u, v), (u - r, v), (u + r, v), (u, v - r), (u, v + r)]
        if any(region.distance(Point(p)) > ON_FACE_TOLERANCE for p in probes):
            return False
        if r <= ON_FACE_TOLERANCE:
            return True
        circle = Point(u, v).buffer(r - ON_FACE_TOLERANCE, quad_segs=16)
        return not any(circle.intersects(g) for g in taken)

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
        # A failed join changes no board, whatever check inside it fails.
        saved = [(board, board._state()) for board in [self, *named]]
        try:
            using.join(self, named)
        except BaseException:
            for board, state in saved:
                board._restore(state)
            raise
        return self

    def _state(self) -> _BoardState:
        """What operations and joins change, for `join()` to restore; it
        resolves the placement, which a join needs anyway."""
        return _BoardState(list(self.ops), dict(self._named_ops), self.outline, list(self._cutouts),
                           list(self.notes))

    def _restore(self, state: _BoardState) -> None:
        self.ops, self._named_ops, self._outline = list(state.ops), dict(state.named_ops), state.outline
        self._cutouts, self.notes = list(state.cutouts), list(state.notes)

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
            "box": b.as_dict(),
            "origin": [b.lo[a] for a in AXES],
            "outline": _rings(self.outline),
            "grain": self._grain,
            "show": self.show_face.world_name,
            "machine": self.machine_face.world_name,
            "grained": self.material.grain,
            "manual": self.manual_part,
            "ops": [_op_to_layout(op) for op in self.ops],
            "faces": self._face_names(),
        }

    def _face_names(self) -> dict[str, list[str]]:
        """Each face's names in the build file, by world name: the
        direction in the scope's frame, and inner or outer for the big
        faces when the board does not straddle the scope's centre."""
        names = {directions.frame.name_of(d): [d.name] for d in self.scope.frame.directions()}
        try:
            inner = self._inner_outer("inner")
        except LangError:
            return names
        names[inner.world_name].append("inner")
        names[Face(self, -inner.direction).world_name].append("outer")
        return names


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
    """The shape's polygons one after the other, each its exterior ring
    (counter-clockwise) and then its holes (clockwise)."""
    rings: Rings = []
    for poly in shape.polygons():
        poly = orient(poly, 1.0)
        for ring in [poly.exterior] + list(poly.interiors):
            rings.append([[float(c[0]), float(c[1])] for c in list(ring.coords)[:-1]])
    return rings


def _op_to_layout(op: Op) -> OpLayout:
    if isinstance(op, Cut):
        cut: CutLayout = {"kind": "cut", "name": op.name, "chamfer": op.chamfer, "shape": _rings(op.shape)}
        return cut
    if isinstance(op, Pocket):
        return _pocket_to_layout(op)
    if isinstance(op, Hole):
        return _hole_to_layout(op)
    if isinstance(op, Chamfer):
        chamfer: ChamferLayout = {"kind": "chamfer", "what": op.what, "size": op.size, "face": op.face}
        return chamfer
    if isinstance(op, VGroove):
        groove: VGrooveLayout = {"kind": "vgroove", "name": op.name, "face": op.face, "start": [op.u0, op.v0],
                                 "end": [op.u1, op.v1], "depth": op.depth}
        return groove
    inner = _hole_to_layout(op.op) if isinstance(op.op, Hole) else _pocket_to_layout(op.op)
    edge: EdgeOpLayout = {"kind": "edge", "face": op.face, "s": op.s, "t": op.t, "op": inner}
    if op.offset:
        edge["offset"] = op.offset
    return edge


def _pocket_to_layout(op: Pocket) -> PocketLayout:
    return {"kind": "pocket", "name": op.name, "face": op.face, "depth": op.depth, "depth_spec": op.depth_spec,
            "chamfer": op.chamfer, "shape": _rings(op.shape)}


def _hole_to_layout(op: Hole) -> HoleLayout:
    return {"kind": "hole", "name": op.name, "face": op.face, "u": op.u, "v": op.v, "d": op.d, "depth": op.depth,
            "depth_spec": op.depth_spec, "through": op.through, "chamfer": op.chamfer}


@dataclass(frozen=True)
class _BoardState:
    """A board's operations and outline at one moment (`Board._state`)."""
    ops: list[Op]
    named_ops: dict[str, Op]
    outline: Shape | None
    cutouts: list[tuple[str, BaseGeometry]]
    notes: list[str]


def board(name: str, material: Material, shape: Shape | None = None) -> Board:
    return Board(name, material, shape)
