"""Parts: boards with placement modifiers, faces and operations.

A board is created with its identity (`board(name, material)`), placed with
order-free modifiers (`on`, `between`, `center`, `inset`, `grain`, `show`,
`manual`) and machined with ordered operations (`cut`, `pocket`, `hole`,
`chamfer`). Every modifier returns the board. Placement is resolved lazily
the first time a face, the box or the layout is asked for; from then on the
placement modifiers are frozen.
"""
from __future__ import annotations

from typing import Any

from . import directions
from .directions import AXES, Direction
from .errors import LangError
from .material import Material
from .ops import Chamfer, Cut, EdgeOp, Hole, Pocket
from .refs import Pos, Side, ToFace, as_pos, through, _is_number
from .shapes import Shape, parse_anchor, rect
from . import scope as scopes


def _axis_of(value) -> str:
    return as_pos(value).axis


class Face:
    """One of the six faces of a board, named by world direction."""

    def __init__(self, part: "Board", direction: Direction):
        self.part = part
        self.direction = direction

    @property
    def axis(self) -> str:
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
        return self.direction.name

    # Edge of this face with another: `side.front.inner`
    def __getattr__(self, name: str):
        f = directions.frame
        if f.is_direction(name) or name in ("inner", "outer"):
            other = self.part.face(name)
            return Edge(self.part, self, other)
        raise AttributeError(name)

    # Arithmetic as a position
    def __add__(self, other):
        return self.position + other

    def __radd__(self, other):
        return other + self.position

    def __sub__(self, other):
        return self.position - other

    def __mul__(self, other):
        return self.position * other

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self.position / other

    def __repr__(self) -> str:
        return f"Face({self.part.path}.{self.name})"


class Edge:
    def __init__(self, part: "Board", a: Face, b: Face):
        if a.axis == b.axis:
            raise LangError(f"{a.name}.{b.name} is not an edge: both faces lie on {a.axis}.", part.path)
        self.part, self.a, self.b = part, a, b

    @property
    def name(self) -> str:
        return f"{self.a.name}.{self.b.name}"

    def __repr__(self) -> str:
        return f"Edge({self.part.path}.{self.name})"


class Board:
    def __init__(self, name: str, material: Material, shape: Shape | None = None):
        if not name or "." in name:
            raise LangError(f"Part name {name!r} must be non-empty and contain no dots.")
        self.name = name
        self.material = material
        self._shape = shape
        self.scope = scopes.current()
        self.scope._register(self)
        # placement, set once each
        self._on: Side | None = None
        self._limits: list[Any] = []
        self._center: Pos | None = None
        self._inset: float = 0.0
        self._grain: str | None = None
        self._show: str | None = None
        self.manual_part: bool = False
        self._set: set[str] = set()
        # resolved
        self._box = None
        self._t_axis: str | None = None
        self._u_axis: str | None = None
        self._v_axis: str | None = None
        self._outline: Shape | None = None
        self.ops: list = []
        self._named_ops: dict[str, Any] = {}

    # -- identity ----------------------------------------------------------

    @property
    def path(self) -> str:
        prefix = self.scope.path
        return f"{prefix}.{self.name}" if prefix else self.name

    @property
    def thickness(self) -> float:
        return self.material.t

    def __repr__(self) -> str:
        return f"Board({self.path})"

    # -- placement modifiers (order-free, settable once) --------------------

    def _placement(self, key: str) -> None:
        if self._box is not None:
            raise LangError(f"{key}() after the placement was used; placement is frozen.", self.path)
        if key in self._set:
            raise LangError(f"{key}() given twice.", self.path)
        self._set.add(key)

    def on(self, ref, side: str | Direction | None = None) -> "Board":
        """Which plane the board's outer big face lies in, and where the
        thickness goes. A box side knows its inward direction; a bare
        position needs `side=`, the direction the thickness extends to."""
        self._placement("on")
        if isinstance(ref, Side) and side is None:
            self._on = ref
        elif isinstance(ref, Face) and side is None:
            # Sitting on another part's face: thickness goes away from that part.
            self._on = Side(ref.axis, ref.value, inward=ref.direction)
        else:
            if side is None:
                raise LangError("on(): a bare position needs side=, the direction the thickness goes.", self.path)
            d = directions.frame.direction(side)
            pos = as_pos(ref, "on()")
            if d.axis != pos.axis:
                raise LangError(f"on(): side {d.name} is not on the axis of {pos}.", self.path)
            self._on = Side(pos.axis, pos.value, inward=d)
        return self

    def between(self, *limits) -> "Board":
        """Limits on the in-plane axes: positions, box sides, faces or
        parts. A part means its face nearest to this board. Missing limits
        default to the enclosing scope's box."""
        self._placement("between")
        self._limits = list(limits)
        return self

    def center(self, pos) -> "Board":
        """The board's thickness is centred on this position; the position's
        axis becomes the thickness axis."""
        self._placement("center")
        self._center = as_pos(pos, "center()")
        return self

    def inset(self, n: float) -> "Board":
        """Shrinks the outline by `n` on every in-plane side of its box."""
        self._placement("inset")
        self._inset = float(n)
        return self

    def grain(self, axis_or_direction: str) -> "Board":
        self._placement("grain")
        a = axis_or_direction
        self._grain = a if a in AXES else directions.frame.direction(a).axis
        return self

    def show(self, face: str) -> "Board":
        """The visible big face: `outer`, `inner`, or a direction."""
        self._placement("show")
        self._show = face
        return self

    def manual(self) -> "Board":
        self._placement("manual")
        self.manual_part = True
        return self

    # -- resolution --------------------------------------------------------

    def box(self):
        if self._box is None:
            self._resolve()
        return self._box

    @property
    def t_axis(self) -> str:
        self.box()
        return self._t_axis

    @property
    def u_axis(self) -> str:
        self.box()
        return self._u_axis

    @property
    def v_axis(self) -> str:
        self.box()
        return self._v_axis

    @property
    def outline(self) -> Shape:
        self.box()
        return self._outline

    @outline.setter
    def outline(self, shape: Shape) -> None:
        self._outline = shape

    def _resolve(self) -> None:
        from .box import Box
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
        self._t_axis = t_axis
        self._u_axis, self._v_axis = [a for a in AXES if a != t_axis]

        lo = {t_axis: t_lo}
        hi = {t_axis: t_hi}
        scope_box = self.scope.box
        for axis in (self._u_axis, self._v_axis):
            values = self._limit_values(axis, scope_box)
            if len(values) == 2:
                a, b = sorted(values)
            elif len(values) == 1:
                if scope_box is None:
                    raise LangError(f"only one limit on {axis} and no enclosing box to supply the other.", self.path)
                v = values[0]
                centre = (scope_box.lo[axis] + scope_box.hi[axis]) / 2
                a, b = (v, scope_box.hi[axis]) if v < centre else (scope_box.lo[axis], v)
            else:
                if self._shape is not None:
                    # An explicit shape carries its own extent; it sits at the
                    # box minimum, or at the origin without a box.
                    base = scope_box.lo[axis] if scope_box is not None else 0.0
                    size = self._shape.width if axis == self._u_axis else self._shape.height
                    a, b = base, base + size
                elif scope_box is None:
                    raise LangError(f"no limits on {axis} and no enclosing box.", self.path)
                else:
                    a, b = scope_box.lo[axis], scope_box.hi[axis]
            a += self._inset
            b -= self._inset
            if b <= a:
                raise LangError(f"extent on {axis} is not positive ({a:g} to {b:g}).", self.path)
            lo[axis], hi[axis] = a, b
        self._box = Box(lo, hi)
        ua, va = self._u_axis, self._v_axis
        if self._shape is not None:
            self._outline = self._shape.moved(lo[ua] - self._shape.bounds[0], lo[va] - self._shape.bounds[1])
        else:
            self._outline = rect(hi[ua] - lo[ua], hi[va] - lo[va]).moved(lo[ua], lo[va])
        if self._grain is None and self.material.grain:
            self._grain = self.scope.default_grain
        if self._grain is not None and self._grain == t_axis:
            raise LangError(f"grain {self._grain} is the thickness axis.", self.path)

    def _limit_values(self, axis: str, scope_box) -> list[float]:
        values = []
        for limit in self._limits:
            if isinstance(limit, Board):
                lb = limit.box()
                if limit.t_axis != axis:
                    continue
                # the face of `limit` nearest to this board's side of the box
                centre = (scope_box.lo[axis] + scope_box.hi[axis]) / 2 if scope_box else (lb.lo[axis] + lb.hi[axis]) / 2
                values.append(lb.hi[axis] if lb.hi[axis] <= centre else lb.lo[axis])
                continue
            pos = as_pos(limit, f"between() limit {limit!r}")
            if pos.axis == axis:
                values.append(pos.value)
        if len(values) > 2:
            raise LangError(f"more than two limits on {axis}.", self.path)
        return values

    # -- faces -------------------------------------------------------------

    def face(self, name: str | Direction) -> Face:
        if isinstance(name, Face):
            return name
        if name in ("inner", "outer"):
            return self._inner_outer(name)
        d = directions.frame.direction(name)
        return Face(self, d)

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
        toward_centre = directions.frame.direction_of(t, 1 if centre > b.hi[t] else -1)
        d = toward_centre if which == "inner" else -toward_centre
        return Face(self, d)

    @property
    def show_face(self) -> Face:
        if self._show is not None:
            return self.face(self._show)
        try:
            return self.face("outer")
        except LangError:
            return Face(self, directions.frame.direction_of(self.t_axis, 1))

    def __getattr__(self, name: str):
        if name.startswith("_"):
            raise AttributeError(name)
        f = directions.frame
        if f.is_direction(name) or name in ("inner", "outer"):
            return self.face(name)
        named = self.__dict__.get("_named_ops", {})
        if name in named:
            return named[name]
        raise AttributeError(name)

    def big_faces(self) -> tuple[Face, Face]:
        self.box()
        return (Face(self, directions.frame.direction_of(self.t_axis, 1)),
                Face(self, directions.frame.direction_of(self.t_axis, -1)))

    # -- 2D frames ---------------------------------------------------------

    def _face_frame(self, face: Face):
        """For a big face: anchors in the outline's (u, v) frame. Returns
        (u_names, v_names, frame_kind). For a narrow face: s along the face,
        t across the thickness."""
        f = directions.frame
        b = self.box()
        if face.is_big:
            u_names = {f.direction_of(self.u_axis, -1).name: 0.0, f.direction_of(self.u_axis, 1).name: 1.0}
            v_names = {f.direction_of(self.v_axis, -1).name: 0.0, f.direction_of(self.v_axis, 1).name: 1.0}
            return u_names, v_names, (self.u_axis, self.v_axis)
        s_axis = self.v_axis if face.axis == self.u_axis else self.u_axis
        s_names = {f.direction_of(s_axis, -1).name: 0.0, f.direction_of(s_axis, 1).name: 1.0}
        t_names = {f.direction_of(self.t_axis, -1).name: 0.0, f.direction_of(self.t_axis, 1).name: 1.0}
        return s_names, t_names, (s_axis, self.t_axis)

    def _resolve_at(self, face: Face, at, shape: Shape | None):
        """Resolves an `at=` spec on a face to a point in that face's frame
        (world coordinates on its two axes) and the shape's matching anchor
        fractions. Returns (point, anchor)."""
        u_names, v_names, (ua, va) = self._face_frame(face)
        b = self.box()
        lo = {ua: b.lo[ua], va: b.lo[va]}
        hi = {ua: b.hi[ua], va: b.hi[va]}
        if isinstance(at, str):
            name, extras = at, ()
        elif isinstance(at, (tuple, list)) and at and isinstance(at[0], str):
            name, extras = at[0], tuple(at[1:])
        else:
            raise LangError(f"at= must be an anchor name or (anchor, offsets...), got {at!r}.", self.path)
        anchor = parse_anchor(name, u_names, v_names)
        point = [lo[ua] + anchor.fu * (hi[ua] - lo[ua]), lo[va] + anchor.fv * (hi[va] - lo[va])]
        # Offsets: in the order of the axes the anchor names (first named
        # axis first); numbers move inward from the named edge or away from
        # the centre; positions replace the coordinate.
        order = []
        for part in name.split("."):
            order.append(ua if part in u_names else va)
        for axis in (ua, va):
            if axis not in order:
                order.append(axis)
        if len(extras) > 2:
            raise LangError(f"at= takes at most two offsets, got {len(extras)}.", self.path)
        for axis, extra in zip(order, extras):
            idx = 0 if axis == ua else 1
            frac = anchor.fu if axis == ua else anchor.fv
            if _is_number(extra):
                if frac == 0.0:
                    point[idx] += extra
                elif frac == 1.0:
                    point[idx] -= extra
                else:
                    point[idx] += extra
            else:
                pos = as_pos(extra, "at= offset")
                if pos.axis != axis:
                    raise LangError(f"at=: position {pos} is not on this face's {axis} axis.", self.path)
                point[idx] = pos.value
        return (point[0], point[1]), anchor

    def _place_shape(self, face: Face, shape: Shape, at) -> Shape:
        point, anchor = self._resolve_at(face, at, shape)
        su, sv = shape.anchor_point(anchor)
        return shape.moved(point[0] - su, point[1] - sv)

    def _depth(self, face: Face, depth) -> tuple[float, str, bool]:
        t = self.thickness
        if depth is through:
            return t, "through", True
        if isinstance(depth, ToFace):
            target = self.face(depth.face)
            if target.axis != face.axis:
                raise LangError(f"depth to({depth.face!r}) is not opposite the face the operation is on.", self.path)
            if target.direction == face.direction:
                raise LangError(f"depth to({depth.face!r}) names the face itself.", self.path)
            extent = self.box().extent(face.axis)
            return extent + depth.offset, f"to({depth.face}, {depth.offset:g})", abs(depth.offset) < 1e-9
        if _is_number(depth):
            if depth <= 0:
                raise LangError(f"depth must be positive, got {depth}.", self.path)
            return float(depth), f"{depth:g}", False
        raise LangError(f"depth must be a number, to(face, offset) or through; got {depth!r}.", self.path)

    # -- operations (ordered) -------------------------------------------------

    def _record(self, op, name: str | None):
        self.ops.append(op)
        if name:
            if name in self._named_ops:
                raise LangError(f"operation name {name!r} used twice.", self.path)
            self._named_ops[name] = op

    def cut(self, shape: Shape, at="center", name: str | None = None, chamfer: float = 0.0) -> "Board":
        """A through cut, positioned on the show face; it changes the outline."""
        face = self.show_face
        placed = self._place_shape(face, shape, at)
        self.outline = self.outline.difference(placed)
        if self.outline.is_empty():
            raise LangError("the cut removes the whole board.", self.path)
        self._record(Cut(placed, name, chamfer), name)
        return self

    def pocket(self, shape: Shape, face="show", at="center", depth=None,
               name: str | None = None, chamfer: float = 0.0) -> "Board":
        f = self.show_face if face == "show" else self.face(face)
        if depth is None:
            raise LangError("pocket() needs a depth.", self.path)
        d, spec, _ = self._depth(f, depth)
        if f.is_big:
            placed = self._place_shape(f, shape, at)
            self._record(Pocket(placed, f.name, d, spec, name, chamfer), name)
        else:
            point, anchor = self._resolve_at(f, at, shape)
            su, sv = shape.anchor_point(anchor)
            self._record(EdgeOp(f.name, Pocket(shape.moved(-su, -sv), f.name, d, spec, name, chamfer),
                                point[0], point[1]), name)
        return self

    def hole(self, d: float, face="show", at="center", depth=None,
             name: str | None = None, chamfer: float = 0.0) -> "Board":
        f = self.show_face if face == "show" else self.face(face)
        if depth is None:
            raise LangError("hole() needs a depth.", self.path)
        if d <= 0:
            raise LangError(f"hole diameter must be positive, got {d}.", self.path)
        dep, spec, thru = self._depth(f, depth)
        point, _ = self._resolve_at(f, at, None)
        if f.is_big:
            self._record(Hole(point[0], point[1], float(d), f.name, dep, spec, name, chamfer, thru), name)
        else:
            self._record(EdgeOp(f.name, Hole(0.0, 0.0, float(d), f.name, dep, spec, name, chamfer, thru),
                                point[0], point[1]), name)
        return self

    def chamfer(self, what, size: float, face="show") -> "Board":
        f = self.show_face if face == "show" else self.face(face)
        if isinstance(what, Edge):
            what = what.name
        elif isinstance(what, Face):
            raise LangError("chamfer(): name an edge (two faces), the outline, or an operation.", self.path)
        if what != "outline" and what not in self._named_ops:
            parts = what.split(".")
            if len(parts) != 2:
                raise LangError(f"chamfer(): {what!r} is neither an edge, 'outline' nor an operation name.", self.path)
            self.face(parts[0]), self.face(parts[1])
        self._record(Chamfer(what, float(size), f.name), None)
        return self

    # -- block form --------------------------------------------------------

    def __enter__(self) -> "Board":
        return self

    def __exit__(self, *exc) -> None:
        return None

    # -- layout --------------------------------------------------------------

    def to_layout(self) -> dict:
        b = self.box()
        origin = {a: b.lo[a] for a in AXES}
        return {
            "path": self.path,
            "kind": "board",
            "material": self.material.label,
            "thickness": self.thickness,
            "axes": {"t": self.t_axis, "u": self.u_axis, "v": self.v_axis},
            "box": b.as_dict(),
            "origin": [origin[a] for a in AXES],
            "outline": [[list(p) for p in ring] for ring in self.outline.rings()],
            "grain": self._grain,
            "show": self.show_face.name,
            "manual": self.manual_part,
            "ops": [_op_to_layout(op) for op in self.ops],
        }


def _op_to_layout(op) -> dict:
    if isinstance(op, Cut):
        return {"kind": "cut", "name": op.name, "chamfer": op.chamfer,
                "shape": [[list(p) for p in r] for r in op.shape.rings()]}
    if isinstance(op, Pocket):
        return {"kind": "pocket", "name": op.name, "face": op.face, "depth": op.depth,
                "depth_spec": op.depth_spec, "chamfer": op.chamfer,
                "shape": [[list(p) for p in r] for r in op.shape.rings()]}
    if isinstance(op, Hole):
        return {"kind": "hole", "name": op.name, "face": op.face, "u": op.u, "v": op.v, "d": op.d,
                "depth": op.depth, "depth_spec": op.depth_spec, "through": op.through, "chamfer": op.chamfer}
    if isinstance(op, Chamfer):
        return {"kind": "chamfer", "what": op.what, "size": op.size, "face": op.face}
    if isinstance(op, EdgeOp):
        inner = _op_to_layout(op.op)
        return {"kind": "edge", "face": op.face, "s": op.s, "t": op.t, "op": inner}
    raise TypeError(op)


def board(name: str, material: Material, shape: Shape | None = None) -> Board:
    return Board(name, material, shape)
