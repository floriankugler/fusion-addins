"""Lift-up hatch hinges (Häfele Free space 1.11) as hardware.

A lift-up hatch hangs from a hinge on each carcass side panel. Both hinge
halves are positioned from the hinge reference, the underside of the
carcass top where it meets the side panel's inner front edge (the
manufacturer's drilling template is pushed up against the top), with the
hatch modelled closed, its inner face against the carcass front or up to
2 mm in front of it (`lib.hatch_hinges.MAX_HATCH_GAP`).

Mounted on the cabinet, `cab.mount(hinge, hatch=hatch, sides=(left,
right), top=top)` drills what the hatch_hinge add-in drills:

- into each side panel's inner face a column of 5 mm holes 37 behind its
  front edge, 102, 134 and 166 below the reference, `carcass_depth` deep
  (12 by default);
- into the hatch's inner face the pilot holes for each mounting plate's
  screws, 25 in from the side panel's inner face, 12 and 76 below the
  reference, `pilot=(diameter, depth)` (2 x 4 by default).

It checks what the add-in checks: the hatch's thickness (16 to 28 mm),
that it is closed, the side panels' flush front edges, how far the hatch
top reaches above the reference (the overlap A, at most the hinge's A_max
for the hatch thickness and opening angle; it is never chosen), that the
holes and the mounting plate fit on their boards, and that no part takes
the closed hinge's space. And it places the hinges as boxes (`HingeShape`),
one body per hinge named by the hatch's own left and right, seen standing
in front of it.

The hinge dictates around it how far the hatch top may reach
(`max_overlap`, `highest_hatch_top`) and how far down the closed hinges
reach inside (`lowest`), so cabinet code never repeats those numbers.

Sources: the hole positions, overlap limits, mounting plate footprint and
probe points of `lib.hatch_hinges` (Häfele's installation manual, checked
against Häfele's STEP model 372.27.300, 2026-10-07); the hinge boxes
measured on Häfele's CAD model of 372.27.300 (`HINGE_SHAPES`, 2026-10-12).
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, cast

from shapely.geometry import Point

from lib import hatch_hinges as data

from ..core import directions
from ..core.directions import Axis, Direction, Frame
from ..core.errors import LangError, one_of
from ..core.layout_types import BoxDict, HardwareBodyLayout
from ..core.ops import Hole, Pocket
from ..core.part import Board, Face
from ..core.refs import Pos, PosLike, as_pos
from ..core.scope import Scope

#: Geometric tolerance of the checks, mm (the add-in's 1e-4 cm).
TOLERANCE = 1e-3

#: Opening angles, degrees: the full opening and the one with the limiter
#: fitted. Which ones a model offers is in its spec.
Opening = Literal[107, 90]

#: Two ends of a box along one direction, mm.
Extent = tuple[float, float]
#: A box in a hinge's frame: its extents inward from the side panel's
#: inner face, back from the carcass front edge, and below the underside
#: of the carcass top (the hinge reference).
HingeBox = tuple[Extent, Extent, Extent]

Point3 = dict[Axis, float]


@dataclass(frozen=True)
class HingeShape:
    """A closed hinge as boxes in its frame (`HingeBox`, the add-in's frame:
    inward from the side panel's inner face, back from the carcass front
    edge, below the underside of the carcass top): the mounting plate on
    the hatch and the rest of the hinge. The space it takes, not its
    detail; the drilling data stays in `lib.hatch_hinges`."""
    #: The mounting plate. It sits on the hatch, so its front lies on the
    #: hatch's inner face whatever the table says (where it was measured);
    #: its back end stays, so it keeps meeting the arm across the gap.
    plate: HingeBox
    #: The arm and the housing, fixed to the side panel.
    body: dict[str, HingeBox]

    def boxes(self, gap: float) -> dict[str, HingeBox]:
        """The boxes with the hatch's inner face `gap` in front of the
        carcass."""
        inward, (_, back), below = self.plate
        return {"plate": (inward, (-gap, back), below), **self.body}

    @property
    def lowest(self) -> float:
        """The closed hinge's lowest point below the reference."""
        return max(below for _, _, (_, below) in (self.plate, *self.body.values()))


#: The hinges' boxes per model name, mm, in the frame of `HingeShape`, for
#: the left hinge (the right one is its mirror image across the cabinet).
#: Free space 1.11: measured on Häfele's CAD model of 372.27.300 (the glTF
#: from Häfele's CAD box, closed, opening angle 0; 2026-10-12), without
#: the two dowels in carcass holes 1 and 3. The hinge reaches from 1.9
#: below the reference (the add-in's reading of the STEP: 1.8) to 169
#: below, 0 to 35.2 inward and -0.3 to 62.8 back; its front is the STEP's
#: hatch inner face, 0.3 in front of the carcass. The boxes touch the side
#: panel and the hatch.
HINGE_SHAPES: dict[str, HingeShape] = {
    data.FREE_SPACE_1_11.name: HingeShape(
        # inward and below as the add-in's plate_inward and plate_below
        plate=((15.5, 34.5), (-0.3, 3.5), (5.0, 83.0)),
        body={
            "arm": ((2.3, 35.2), (3.5, 62.8), (1.9, 62.0)),
            "housing_upper": ((4.0, 35.2), (3.5, 50.0), (62.0, 92.0)),
            "housing_lower": ((0.0, 24.5), (4.8, 58.0), (92.0, 169.0)),
        },
    ),
}


@dataclass(frozen=True)
class _Frame:
    """Where the hinges hang: `up`, `back` from the hatch into the carcass,
    and the reference's height on the up axis."""
    up: Direction
    back: Direction
    reference: float


@dataclass(frozen=True)
class _Hinge:
    """One hinge: its side panel and where that panel is."""
    side: Board
    #: The hatch's own left or right, seen standing in front of it.
    which: str
    #: From the side panel into the cabinet.
    inward: Direction
    #: The side panel's inner face, on the inward axis.
    inner: float
    #: The carcass front edge, the side panel's front face, on the back axis.
    front: float
    #: From the hatch's inner face back to the carcass front.
    gap: float


class HatchHinge:
    """A lift-up hatch hinge model with the drilling settings: `opening`
    the angle the hinges are set to (the full one, or with the limiter;
    it decides how far the hatch top may reach above the carcass top's
    underside), `carcass_depth` the depth of the carcass holes (their
    diameter is the hinge's), `pilot` the (diameter, depth) of the pilot
    holes in the hatch, mm."""

    def __init__(self, spec: data.HingeSpec, opening: Opening = 107,
                 carcass_depth: float = data.CARCASS_HOLE_DEPTH,
                 pilot: tuple[float, float] = (data.PILOT_DIAMETER, data.PILOT_DEPTH)):
        one_of(opening, Opening, "HatchHinge(opening=)")
        if opening not in (spec.opening, spec.limited_opening):
            raise LangError(f"{spec.name} opens to {spec.opening} degrees, or {spec.limited_opening} with the "
                            f"limiter; not {opening}.")
        if spec.name not in HINGE_SHAPES:
            raise LangError(f"{spec.name}: no hinge shape to draw it with.")
        if carcass_depth <= 0:
            raise LangError(f"{spec.name}: the carcass hole depth must be greater than zero.")
        diameter, depth = pilot
        if diameter <= 0 or depth <= 0:
            raise LangError(f"{spec.name}: the pilot holes' diameter and depth must be greater than zero.")
        self.spec = spec
        self.opening: int = opening
        self.carcass_depth = float(carcass_depth)
        self.pilot = (float(diameter), float(depth))

    @property
    def name(self) -> str:
        return self.spec.name

    @property
    def limited(self) -> bool:
        """Whether the opening is limited (the limiter is fitted)."""
        return self.opening != self.spec.opening

    @property
    def shape(self) -> HingeShape:
        return HINGE_SHAPES[self.spec.name]

    # -- what the hinge dictates ---------------------------------------------------------------

    def max_overlap(self, hatch_thickness: float) -> float:
        """How far the top of a hatch `hatch_thickness` thick may reach above
        the underside of the carcass top at this opening (A_max), mm: the
        manual's table, linear in between."""
        self._check_thickness(hatch_thickness)
        return self.spec.overlap_limit(hatch_thickness, self.limited)

    def highest_hatch_top(self, top: Board | PosLike, hatch_thickness: float) -> Pos:
        """The highest the top edge of a hatch `hatch_thickness` thick may
        be, as a position: `max_overlap` above the underside of the carcass
        top (`top`, the board or the position of its underside)."""
        reference, up = _reference(top, "highest_hatch_top(top=)")
        return Pos(up.axis, reference.value + up.sign * self.max_overlap(hatch_thickness))

    def lowest(self, top: Board | PosLike) -> Pos:
        """The closed hinges' lowest point inside the cabinet, as a
        position: a shelf whose upper face lies at or below it stays clear
        of them. `top` is the carcass top or the position of its
        underside."""
        reference, up = _reference(top, "lowest(top=)")
        return Pos(up.axis, reference.value - up.sign * self.shape.lowest)

    def hinge_boxes(self, gap: float = 0.0) -> dict[str, HingeBox]:
        """One closed hinge's boxes in its own frame (see `HingeBox`), the
        hatch's inner face `gap` in front of the carcass."""
        return self.shape.boxes(gap)

    # -- mounting -------------------------------------------------------------------------------

    def mount(self, scope: Scope, /, **options: object) -> None:
        """`cab.mount(hinge, hatch=hatch, sides=(left, right), top=top)`:
        drills the side panels (one or both, a hinge on each) and the
        closed hatch for the hinges, positioned from the underside of the
        carcass top `top` (the board, or the position of its underside),
        and places the hinges."""
        allowed = {"hatch", "sides", "top"}
        if set(options) - allowed or allowed - set(options):
            raise LangError(f"{self.name}: mount() takes hatch=, sides=(left, right) and top=, "
                            f"got {sorted(options)}.", scope.path)
        if any(item["name"] == "hinges" for item in scope.hardware):
            raise LangError(f"{self.name}: this scope has hatch hinges already; mount the hinges of another "
                            "hatch in a scope of its own.", scope.path)
        hatch = options["hatch"]
        if not isinstance(hatch, Board):
            raise LangError(f"{self.name}: hatch= must be the hatch board.", scope.path)
        sides = _boards(options["sides"], scope.path, self.name)
        top = options["top"]
        if isinstance(top, Board):
            if top is hatch or any(top is s for s in sides):
                raise LangError(f"{self.name}: top= must be the carcass top, not the hatch or a side panel.",
                                scope.path)
        reference, _ = _reference(cast(Board | PosLike, top), f"{self.name}: mount(top=)")
        if any(s is hatch for s in sides):
            raise LangError(f"{self.name}: the hatch cannot be one of the side panels.", hatch.path)
        frame, hinges = self._layout(scope, hatch, sides, reference)
        self._drill(frame, hatch, hinges)
        self._place(scope, frame, hinges)

    def _check_thickness(self, thickness: float, path: str | None = None) -> None:
        spec = self.spec
        if not spec.min_hatch_thickness - TOLERANCE <= thickness <= spec.max_hatch_thickness + TOLERANCE:
            raise LangError(f"The hatch is {_mm(thickness)} thick; the {spec.name} fits hatches from "
                            f"{_mm(spec.min_hatch_thickness)} to {_mm(spec.max_hatch_thickness)}.", path)

    def _layout(self, scope: Scope, hatch: Board, sides: list[Board], reference: Pos) -> tuple[_Frame, list[_Hinge]]:
        """Where the hinges go, after the add-in's checks in its order.
        Raises LangError when the hinges cannot be placed."""
        spec = self.spec
        up = scope.frame.direction("top")
        if reference.axis != up.axis:
            raise LangError(f"{self.name}: top= must be a height, the underside of the carcass top.", scope.path)
        if hatch.t_axis == up.axis:
            raise LangError(f"{self.name}: the hatch must stand upright, closing the cabinet's front.", hatch.path)
        thickness = hatch.thickness
        self._check_thickness(thickness, hatch.path)
        depth_axis = hatch.t_axis
        hatch_box = hatch.box()
        hatch_middle = hatch_box.center_point()
        hinges: list[_Hinge] = []
        back: Direction | None = None
        for side in sides:
            if side.t_axis in (up.axis, depth_axis):
                raise LangError(f"{self.name}: the side panels must stand upright, perpendicular to the hatch.",
                                side.path)
            sb = side.box()
            # From the hatch into the carcass: toward the side panel.
            to_side = (sb.lo[depth_axis] + sb.hi[depth_axis]) / 2 - hatch_middle[_AXES.index(depth_axis)]
            side_back = scope.frame.direction_of(depth_axis, 1 if to_side > 0 else -1)
            if back is None:
                back = side_back
            elif side_back.sign != back.sign:
                raise LangError(f"{self.name}: both side panels must stand behind the hatch.", side.path)
            front = sb.hi[depth_axis] if back.sign < 0 else sb.lo[depth_axis]
            hatch_inner = hatch_box.hi[depth_axis] if back.sign > 0 else hatch_box.lo[depth_axis]
            gap = (front - hatch_inner) * back.sign
            if gap < -TOLERANCE:
                raise LangError(f"The hatch reaches {_mm(-gap)} into the carcass at {side.path}. Model the closed "
                                "hatch in front of the carcass.", hatch.path)
            if gap > data.MAX_HATCH_GAP + TOLERANCE:
                raise LangError(f"The hatch must be modelled in its closed position, against the carcass front "
                                f"(it is {_mm(gap)} in front of {side.path}).", hatch.path)
            # The inner face is the one toward the middle of the hatch.
            t = side.t_axis
            middle = hatch_middle[_AXES.index(t)]
            if sb.lo[t] - TOLERANCE < middle < sb.hi[t] + TOLERANCE:
                raise LangError(f"{self.name}: the side panel stands in the middle of the hatch; the hinges go on "
                                "the side panels at the hatch's ends.", side.path)
            inward = scope.frame.direction_of(t, 1 if middle > sb.hi[t] else -1)
            inner = sb.hi[t] if inward.sign > 0 else sb.lo[t]
            right = _cross(scope.frame, back, up)
            # Seen from the front, the left side panel's inner face points right.
            which = "left" if _same(inward, right) else "right"
            hinges.append(_Hinge(side, which, inward, inner, front, gap))
        assert back is not None
        if len(hinges) == 2:
            first, second = hinges
            if _same(first.inward, second.inward):
                raise LangError(f"{self.name}: the two side panels must be on opposite sides of the cabinet.",
                                second.side.path)
            if abs(first.front - second.front) > TOLERANCE:
                raise LangError(f"The front edges of the two side panels are {_mm(abs(first.front - second.front))} "
                                "apart in depth; the hatch closes against both, so they must be flush.",
                                second.side.path)
        hinges.sort(key=lambda h: h.which)       # left, then right
        frame = _Frame(up, back, reference.value)

        overlap = (hatch_box.hi[up.axis] if up.sign > 0 else hatch_box.lo[up.axis]) - reference.value
        overlap *= up.sign
        limit = spec.overlap_limit(thickness, self.limited)
        if overlap > limit + TOLERANCE:
            hint = "" if self.limited else (f" ({_mm(spec.limited_max_overlap)} with the opening limited to "
                                            f"{spec.limited_opening}°)")
            raise LangError(f"The hatch top reaches {_mm(overlap)} above the underside of the carcass top. The "
                            f"{spec.name} allows at most {_mm(limit)} for a {_mm(thickness)} hatch{hint}.",
                            hatch.path)

        carcass_radius = spec.carcass_hole_diameter / 2
        pilot_diameter, pilot_depth = self.pilot
        hatch_face = _face(hatch, back)
        parts = _module_of(scope).all_parts()
        for h in hinges:
            side_face = _face(h.side, h.inward)
            if not _points_on_face(side_face, self._carcass_holes(frame, h), carcass_radius, (up, back)):
                raise LangError("The carcass holes do not fit on the side panel's inner face.", h.side.path)
            plate = [self._point(frame, h, inward, -h.gap, below)
                     for inward in spec.plate_inward for below in spec.plate_below]
            if not _points_on_face(hatch_face, plate, 0.0, (up, h.inward)):
                raise LangError(f"The hinge's mounting plate does not fit on the hatch. It covers "
                                f"{_mm(spec.plate_below[0])} to {_mm(spec.plate_below[1])} below the underside of "
                                "the carcass top.", hatch.path)
            if not _points_on_face(hatch_face, self._hatch_holes(frame, h), pilot_diameter / 2, (up, h.inward)):
                raise LangError("The pilot holes do not fit on the hatch.", hatch.path)
            if self.carcass_depth >= h.side.thickness - TOLERANCE:
                raise LangError(f"The carcass hole depth must be less than the side panel thickness "
                                f"({_mm(h.side.thickness)}).", h.side.path)
            probes = [self._point(frame, h, *point) for point in spec.probe_points]
            obstacle = next((p for p in parts if any(_material_at(p, q) for q in probes)), None)
            if obstacle is not None:
                raise LangError(f"The {h.which} hinge would collide with {obstacle.path}. The hinges are positioned "
                                "from the underside of the carcass top (top=); keep other parts out of the space "
                                "the closed hinge takes.", h.side.path)
        if pilot_depth >= thickness - TOLERANCE:
            raise LangError(f"The pilot hole depth must be less than the hatch thickness ({_mm(thickness)}).",
                            hatch.path)
        return frame, hinges

    def _point(self, frame: _Frame, h: _Hinge, inward: float, back: float, below: float) -> Point3:
        """A point in world coordinates, `inward` from the side panel's inner
        face, `back` from the carcass front and `below` the reference."""
        return {h.inward.axis: h.inner + h.inward.sign * inward,
                frame.back.axis: h.front + frame.back.sign * back,
                frame.up.axis: frame.reference - frame.up.sign * below}

    def _carcass_holes(self, frame: _Frame, h: _Hinge) -> list[Point3]:
        spec = self.spec
        return [self._point(frame, h, 0.0, spec.carcass_hole_back,
                            spec.carcass_first_hole_below + i * spec.carcass_hole_pitch)
                for i in range(spec.carcass_hole_count)]

    def _hatch_holes(self, frame: _Frame, h: _Hinge) -> list[Point3]:
        spec = self.spec
        return [self._point(frame, h, spec.hatch_hole_inward, -h.gap,
                            spec.hatch_first_hole_below + i * spec.hatch_hole_pitch)
                for i in range(spec.hatch_hole_count)]

    def _drill(self, frame: _Frame, hatch: Board, hinges: list[_Hinge]) -> None:
        """The carcass holes into each side panel's inner face, named
        `hinge_1` to `hinge_3` from the top, and the pilot holes into the
        hatch's inner face, `hinge_left_1`, `hinge_left_2`, ..."""
        diameter, depth = self.pilot
        hatch_face = _face(hatch, frame.back)
        for h in hinges:
            side_face = _face(h.side, h.inward)
            for i, p in enumerate(self._carcass_holes(frame, h), 1):
                h.side.add_hole(side_face, _uv(h.side, p), self.spec.carcass_hole_diameter, self.carcass_depth,
                                name=h.side.unique_op_name(f"hinge_{i}"))
            for i, p in enumerate(self._hatch_holes(frame, h), 1):
                hatch.add_hole(hatch_face, _uv(hatch, p), diameter, depth,
                               name=hatch.unique_op_name(f"hinge_{h.which}_{i}"))

    def _place(self, scope: Scope, frame: _Frame, hinges: list[_Hinge]) -> None:
        """Records the hinges as boxes, a body per hinge named by the hatch's
        own left and right, seen standing in front of it (also in a module
        written without front=, whose left is the hatch's right)."""
        bodies: list[HardwareBodyLayout] = []
        for h in hinges:
            starts = ((h.inward, h.inner), (frame.back, h.front), (-frame.up, frame.reference))
            boxes = [_world_box(starts, box) for box in self.hinge_boxes(h.gap).values()]
            bodies.append(HardwareBodyLayout(name=h.which, boxes=boxes))
        scope.place_hardware("hinges", bodies)


_AXES: tuple[Axis, Axis, Axis] = ("x", "y", "z")


def _mm(value: float) -> str:
    """A length for messages, as the add-in writes it: `24.5 mm`, `18 mm`."""
    return f"{value:.1f}".rstrip("0").rstrip(".") + " mm"


def _boards(value: object, path: str, name: str) -> list[Board]:
    """`sides=`: one side panel, or one or two in a tuple or list."""
    items: list[object] = [value] if isinstance(value, Board) else (
        list(cast(Sequence[object], value)) if isinstance(value, (tuple, list)) else [])
    if not 1 <= len(items) <= 2 or not all(isinstance(b, Board) for b in items):
        raise LangError(f"{name}: sides= must be the side panel that carries a hinge, or both side panels.", path)
    boards = cast(list[Board], items)
    if len(boards) == 2 and boards[0] is boards[1]:
        raise LangError(f"{name}: name two different side panels.", path)
    return boards


def _reference(top: Board | PosLike, what: str) -> tuple[Pos, Direction]:
    """The hinge reference's height and the up direction: the underside of
    the carcass top board, or a position given for it."""
    if isinstance(top, Board):
        up = top.scope.frame.direction("top")
        if top.t_axis != up.axis:
            raise LangError(f"{what} must be the carcass top, lying flat, or the height of its underside.", top.path)
        return _face(top, -up).position, up
    up = directions.current_frame().direction("top")
    pos = as_pos(top, what)
    if pos.axis != up.axis:
        raise LangError(f"{what}: {pos} is not a height; give the carcass top or the height of its underside.")
    return pos, up


def _face(board: Board, direction: Direction) -> Face:
    """The board's face pointing along `direction`, named in the board's
    own frame."""
    return board.face(board.scope.frame.direction_of(direction.axis, direction.sign))


def _same(a: Direction, b: Direction) -> bool:
    """Whether two directions point the same way, whatever frames name them."""
    return a.axis == b.axis and a.sign == b.sign


def _cross(frame: Frame, a: Direction, b: Direction) -> Direction:
    """The direction of a x b, for two perpendicular directions."""
    (ax, ay, az), (bx, by, bz) = a.vector, b.vector
    v = (ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx)
    i = next(k for k in range(3) if v[k])
    return frame.direction_of(_AXES[i], v[i])


def _uv(board: Board, p: Point3) -> tuple[float, float]:
    """A world point in the frame of the board's outline."""
    return (p[board.u_axis], p[board.v_axis])


def _module_of(scope: Scope) -> Scope:
    """The module the scope belongs to: the parts the hinges must clear."""
    s = scope
    while not s.is_module and s.parent is not None:
        s = s.parent
    return s


def _in_op(board: Board, face: Face, uv: tuple[float, float]) -> bool:
    """Whether the point lies inside a pocket or hole made from `face`."""
    point = Point(*uv)
    for op in board.ops:
        if isinstance(op, Pocket) and op.face == face.world_name:
            if op.shape.geometry.buffer(-TOLERANCE).contains(point):
                return True
        elif isinstance(op, Hole) and op.face == face.world_name:
            if point.distance(Point(op.u, op.v)) < op.d / 2 - TOLERANCE:
                return True
    return False


def _points_on_face(face: Face, centres: list[Point3], radius: float, directions_: tuple[Direction, Direction]) -> bool:
    """True when every centre, and its rim along both directions when
    `radius` is set, lies on the face: inside the board's outline and not
    in a pocket or hole made from that face (the add-in's isPointOnFace)."""
    board = face.part
    outline = board.outline.geometry
    offsets = [(0.0, 0.0)]
    if radius > 0:
        offsets += [(radius, 0.0), (-radius, 0.0), (0.0, radius), (0.0, -radius)]
    first, second = directions_
    for centre in centres:
        for a, b in offsets:
            p = dict(centre)
            p[first.axis] += first.sign * a
            p[second.axis] += second.sign * b
            uv = _uv(board, p)
            if outline.distance(Point(*uv)) > TOLERANCE or _in_op(board, face, uv):
                return False
    return True


def _material_at(part: Board, p: Point3) -> bool:
    """Whether the part's material contains the point: inside its outline
    and thickness, not in one of its pockets or holes. Points on its
    surface do not count."""
    b = part.box()
    t, u, v = part.t_axis, part.u_axis, part.v_axis
    if not b.lo[t] + TOLERANCE < p[t] < b.hi[t] - TOLERANCE:
        return False
    point = Point(p[u], p[v])
    if not part.outline.geometry.buffer(-TOLERANCE).contains(point):
        return False
    for op in part.ops:
        if not isinstance(op, (Pocket, Hole)):
            continue
        face = directions.frame.direction(op.face)
        lo, hi = (b.hi[t] - op.depth, b.hi[t]) if face.sign > 0 else (b.lo[t], b.lo[t] + op.depth)
        if not lo - TOLERANCE <= p[t] <= hi + TOLERANCE:
            continue
        if isinstance(op, Pocket):
            if op.shape.geometry.buffer(TOLERANCE).contains(point):
                return False
        elif point.distance(Point(op.u, op.v)) <= op.d / 2 + TOLERANCE:
            return False
    return True


def _world_box(starts: tuple[tuple[Direction, float], ...], box: HingeBox) -> BoxDict:
    """A hinge box in world coordinates: each of its extents measured
    along a direction from a world position."""
    lo, hi = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
    for (direction, start), (a, b) in zip(starts, box):
        ends = sorted((start + direction.sign * a, start + direction.sign * b))
        i = _AXES.index(direction.axis)
        lo[i], hi[i] = ends
    return {"min": lo, "max": hi}
