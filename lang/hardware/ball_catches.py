"""Ball catches (Ganter GN 450) that hold an inspection hatch in its
opening, as hardware.

The opening is a through cut in a board, named, with its rounded corners
part of the 2D shape: `panel.cut(rect(width=400, depth=300).rounded(20),
at=panel.top.center, name="opening")`. The hatch is a board of its own in
the opening, flush with the panel on the face the catches are screwed to,
with a slot of 2.5 to 3.5 mm all round: `catch.hatch("hatch",
panel.opening)` makes it, the opening shrunk by `catch.gap` (3 mm unless
the catch says otherwise), so the slot's width never appears in a build.

Mounted, the catches pre-drill both boards as the ball_catch add-in does.
Each catch sits on a straight edge of the opening, where its holder's stop
webs bear on the panel's edge; on the perpendicular to that edge through
the catch go a pilot hole for the holder's screw in the panel, 8.4 mm
outside the opening's contour, and one for the ball's screw in the hatch,
9.4 mm inside the contour (so 6.4 mm from the hatch's edge with a 3 mm
slot), each 2 mm across and 4 deep unless `pilot=` says otherwise, from
the face the catches are screwed to: the big face that is not the show
face (the hidden one), unless `face=` names one.

`scope.mount(catch, opening=panel.opening, edge=panel.opening.left,
hatch=hatch)` spaces `count` catches (4) over the straight edge that
`edge` names and the one across the opening from it: the edge named takes
the larger half, the first and last catch on an edge sit `end` (40) from
the ends of its straight part (where the rounded corners begin), the rest
evenly between, and a single catch is centred. With `BallCatch(at=[...])`
a catch goes to each point instead, moved square onto the nearest
straight edge of the opening. The straight edges and their ends come from
the opening's shape: its lines, between the arcs `lang.emit.arcs` finds.

It refuses what the add-in refuses: an opening that is not a hole inside
the panel, a hatch that is not flush with it on the catch face or not
under every ball, a slot narrower or wider than the catch takes, a catch
less than half the holder's width (14 mm) from the end of its straight
edge or less than a holder's width from its neighbour, a holder without
its 28 x 15 mm of panel beside the opening or a ball without its 14 x 15
mm of hatch beside the slot, and pilot holes as deep as a board is thick.

The catches are placed too, one body of boxes per catch standing out of
the catch face (`CATCH_SHAPES`, from Ganter's catalogue drawing): the
holder on the panel, its jaw reaching over the slot, and the ball part on
the hatch, in the jaw.

Sources: Ganter GN 450-28-14 catalog drawing via `lib.ball_catches`
(holder hole 8.4 mm out, ball hole 9.4 mm in, slot 2.5 to 3.5 mm, 15 mm
of mounting surface, holder 28 and ball 14 mm wide); the placement rules
and defaults are the ball_catch add-in's (`addins-src/ball_catch/main.py`)
and Florian's choices for it (2026-10-07).
"""
from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, cast

from shapely.geometry import LineString, Point, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

from lib import ball_catches as data

from ..core import cutouts as cutout_geometry
from ..core.directions import AXES, Direction, InnerOuter
from ..core.errors import LangError, one_of
from ..core.layout_types import BoxDict, HardwareBodyLayout
from ..core.material import Material
from ..core.ops import Cut, Hole, Pocket, VGroove
from ..core.part import Anchor, Board, Face, Operation, board
from ..core.refs import Pos, Side, as_pos
from ..core.shapes import Shape
from ..emit.arcs import Arc2, Circle2, Curve2, Line2, fit
from ..joints.common import big_face, face_choice, hidden_face

if TYPE_CHECKING:
    from ..core.scope import Scope

#: The catches of `lib.ball_catches`, by name.
CatchModel = Literal["GN 450"]
#: The face the catches are screwed to: a big face of the panel, a box side
#: or direction it faces, or inner/outer; None for the hidden face.
CatchFace = Face | Side | Direction | InnerOuter | None

#: Geometric tolerance of the checks, mm (the add-in's 1e-4 cm).
TOLERANCE = 1e-3
#: How far inside a face the probes along its border sit, mm (the add-in's
#: 0.01 cm).
PROBE_INSET = 0.1
#: The hatch's arcs get a vertex at least every this many degrees, so the
#: emitter draws them as arcs again (`lang.emit.arcs`).
_ARC_STEP = math.radians(1.0)

Point2 = tuple[float, float]


def _mm(value: float) -> str:
    return f"{value:.1f}".rstrip("0").rstrip(".") + " mm"


def _moved(p: Point2, direction: Point2, distance: float) -> Point2:
    return (p[0] + direction[0] * distance, p[1] + direction[1] * distance)


def _dot(a: Point2, b: Point2) -> float:
    return a[0] * b[0] + a[1] * b[1]


def _towards(a: Point2, b: Point2) -> Point2:
    return (b[0] - a[0], b[1] - a[1])


@dataclass
class _Catch:
    #: Counts from 1: along the edge named, then the one opposite, or in
    #: the order of `at=`.
    number: int
    #: From the start of its edge's straight part.
    distance: float
    holder: Point2
    ball: Point2


@dataclass
class _Straight:
    """A straight edge of the opening in the panel's face frame (its (u,
    v) world coordinates), from its end with the lower coordinates to the
    other, and the catches on it."""
    a: Point2
    b: Point2
    #: Unit vector from `a` to `b`.
    along: Point2
    #: Unit vector square to the edge, away from the opening into the panel.
    outward: Point2
    #: How the messages name it: "the opening's left edge".
    label: str
    #: Sorted along the edge.
    catches: list[_Catch] = field(default_factory=list[_Catch])

    @property
    def length(self) -> float:
        return math.dist(self.a, self.b)

    def distance_along(self, p: Point2) -> float:
        return _dot(_towards(self.a, p), self.along)

    def at(self, distance: float, outward: float = 0.0) -> Point2:
        return _moved(_moved(self.a, self.along, distance), self.outward, outward)


@dataclass
class _Plan:
    """Everything a mount machines and places, worked out and checked."""
    panel: Board
    hatch: Board
    face: Face
    hatch_face: Face
    sides: list[_Straight]
    #: The slot's width at each side.
    gaps: list[float]

    def catches(self) -> list[_Catch]:
        return sorted((c for side in self.sides for c in side.catches), key=lambda c: c.number)


@dataclass(frozen=True)
class PartBox:
    """One part of a catch as a box, mm: `width` along the edge, centred on
    the catch; `across` square to the edge, from the opening's contour,
    outward over the panel positive; `height` out of the catch face."""
    width: float
    across: tuple[float, float]
    height: float


@dataclass(frozen=True)
class CatchShape:
    """A catch, closed, as three boxes standing out of the catch face, for
    the layout's `hardware`: the space it takes, not its detail. The holder
    sits on the panel beside the opening, its jaw reaches over the slot,
    and the ball part sits on the hatch with its ball in the jaw, so the
    boxes overlap and a catch is one body."""
    #: On the panel, beside the opening.
    holder: PartBox
    #: The holder's jaw, over the slot and the hatch's edge.
    jaw: PartBox
    #: On the hatch, its ball in the jaw.
    ball: PartBox


#: Per catch model. GN 450-28-14 from Ganter's catalogue drawing
#: (ganternorm.com, GN 450 sketch, 2026-10-12; no CAD download): the holder
#: b = 28 wide and 16 deep, its screw 8.4 from its stop webs on the
#: opening's edge, 16 high; the jaw between the stop ridges 18.5 wide,
#: reaching 11 from the stop webs; the ball part d = 14 across its ball on
#: a 13.5 high mount, its screw 9.4 inside the contour.
CATCH_SHAPES: dict[str, CatchShape] = {
    "GN 450": CatchShape(
        holder=PartBox(width=28.0, across=(0.0, 16.0), height=16.0),
        jaw=PartBox(width=18.5, across=(-11.0, 0.0), height=16.0),
        ball=PartBox(width=14.0, across=(-16.4, -2.4), height=13.5),
    ),
}


class BallCatch:
    """Ball catches of one model with their placement and drilling:
    `count` catches spaced `end` from the ends of the edges' straight
    parts, or one at each point of `at` (anchors on a big face of the
    panel or the hatch); `pilot` holes as (diameter, depth) in mm for the
    holder's and the ball's screws; `gap`, the slot between the opening
    and the hatch that `hatch()` leaves (the middle of what the catch
    takes, 3 mm for the GN 450). The defaults are the add-in's: 4 catches,
    40 from the ends, pilot holes 2 x 4."""

    def __init__(self, model: CatchModel = "GN 450", count: int | None = None, end: float = data.DEFAULT_END_OFFSET,
                 at: Sequence[Anchor] | None = None, pilot: tuple[float, float] = (data.PILOT_DIAMETER, data.PILOT_DEPTH),
                 gap: float | None = None):
        self.spec = data.CATCHES[one_of(model, CatchModel, "BallCatch()")]
        #: The boxes the catches are drawn as.
        self.shape = CATCH_SHAPES[model]
        if count is not None and at is not None:
            raise LangError(f"{self.name}: give count= or at=, not both.")
        if count is not None and count < 1:
            raise LangError(f"{self.name}: count must be at least 1, not {count}.")
        if end < 0:
            raise LangError(f"{self.name}: end must not be negative, not {end:g}.")
        if at is not None:
            if not at:
                raise LangError(f"{self.name}: at= is empty.")
            for anchor in at:
                if not isinstance(anchor, Anchor):    # pyright: ignore[reportUnnecessaryIsInstance]
                    raise LangError(f"{self.name}: at= takes points on a face, such as "
                                    f"panel.bottom.left(panel.opening.left).front(200), not {anchor!r}.")
        diameter, depth = pilot
        if diameter <= 0:
            raise LangError(f"{self.name}: the pilot diameter must be greater than zero.")
        if depth <= 0:
            raise LangError(f"{self.name}: the pilot depth must be greater than zero.")
        lo, hi = self.spec.min_gap, self.spec.max_gap
        if gap is None:
            gap = (lo + hi) / 2
        elif not lo <= gap <= hi:
            raise LangError(f"{self.name}: the slot must be {lo:g} to {hi:g} mm wide, not {gap:g}.")
        #: The catches on the edge named and the one opposite; None with at=.
        self.count: int | None = None if at is not None else (count if count is not None else data.DEFAULT_COUNT)
        #: From the ends of an edge's straight part to its first and last catch.
        self.end = float(end)
        #: Points the catches are moved onto the opening's straight edges from.
        self.at: tuple[Anchor, ...] | None = tuple(at) if at is not None else None
        self.pilot = (float(diameter), float(depth))
        #: The slot between the opening and the hatch that `hatch()` leaves.
        self.gap: float = float(gap)

    @property
    def name(self) -> str:
        return f"{self.spec.name} ball catch"

    # -- the hatch -----------------------------------------------------------------------------------

    def hatch(self, name: str, opening: Operation, material: Material | None = None, face: CatchFace = None) -> Board:
        """A board named `name` in `opening`, the named through cut of a
        panel: the opening's shape shrunk by `gap` all round (its arcs stay
        true arcs), of the panel's material unless `material` says
        otherwise, flush with the panel on the catch face (`face`, the
        panel's hidden face by default), so a hatch as thick as the panel
        is flush on both faces. It shows the face the panel shows; its
        grain is left to the build."""
        panel = opening.part
        cut = self._opening_cut(opening)
        catch_face = self._catch_face(panel, face)
        geometry = _inset(cut.shape.polygons()[0], self.gap)
        if geometry.is_empty:
            raise LangError(f"{self.name}: the opening {opening.name!r} is too small for a hatch with a "
                            f"{self.gap:g} mm slot.", panel.path)
        shape = Shape(geometry)
        x0, y0, x1, y1 = shape.bounds
        hatch = board(name, material if material is not None else panel.material, shape)
        frame = hatch.scope.frame
        inward = frame.direction_of(catch_face.axis, -catch_face.direction.sign)
        hatch.on(Pos(catch_face.axis, catch_face.value), toward=inward)
        hatch.between(Pos(panel.u_axis, x0), Pos(panel.u_axis, x1), Pos(panel.v_axis, y0), Pos(panel.v_axis, y1))
        show = panel.show_face.direction
        hatch.show(frame.direction_of(show.axis, show.sign))
        return hatch

    # -- mounting ------------------------------------------------------------------------------------

    def mount(self, scope: Scope, /, **options: object) -> None:
        """`scope.mount(catch, opening=panel.opening, edge=panel.opening.left,
        hatch=hatch)`: drills the panel for the holders and the hatch for
        the balls, on the edge `edge` names (a position, the opening's side
        in a direction) and the one across from it, or at the catch's `at=`
        points (then without `edge=`), and places the catches. `face=`
        names the face they are screwed to, the panel's hidden face by
        default. Nothing is drilled unless every catch fits."""
        allowed = {"opening", "hatch", "edge", "face"}
        unknown = set(options) - allowed
        if unknown or "opening" not in options or "hatch" not in options:
            raise LangError(f"{self.name}: mount() takes opening=, hatch=, edge= and face=, got {sorted(options)}.")
        opening, hatch = options["opening"], options["hatch"]
        if not isinstance(opening, Operation):
            raise LangError(f"{self.name}: opening= is a named through cut of the panel, such as panel.opening, "
                            f"not {opening!r}.")
        if not isinstance(hatch, Board):
            raise LangError(f"{self.name}: hatch= is the board in the opening, not {hatch!r}.")
        edge = options.get("edge")
        if self.at is None and edge is None:
            raise LangError(f"{self.name}: mount() needs edge=, the straight edge of the opening the catches "
                            f"go on, e.g. edge={opening.part.name}.{opening.name}.left.", opening.part.path)
        if self.at is not None and edge is not None:
            raise LangError(f"{self.name}: with at= each catch goes to the nearest straight edge; leave out edge=.",
                            opening.part.path)
        plan = self._plan(opening, hatch, edge, cast(CatchFace, options.get("face")))
        first = self._first_number(plan)
        self._drill(plan, first)
        self._place(scope, plan, first)

    def _plan(self, opening: Operation, hatch: Board, edge: object, face: CatchFace) -> _Plan:
        """Finds the edges, works out every hole and checks it, in the
        add-in's order."""
        spec = self.spec
        panel = opening.part
        cut = self._opening_cut(opening)
        catch_face = self._catch_face(panel, face)
        hatch_face = self._hatch_face(panel, catch_face, hatch)
        region = _face_region(panel, catch_face)
        edges = self._straight_edges(panel, opening, cut, region)
        if not edges:
            raise LangError(f"{self.name}: the opening {opening.name!r} has no straight edges for the holders to "
                            "bear on.", panel.path)
        if self.at is None:
            sides = self._spaced(panel, opening, edges, as_pos(edge, "mount(edge=)"))
        else:
            sides = self._at_points(panel, hatch, edges)
        hatch_region = _face_region(hatch, hatch_face)
        catches = sorted((c for side in sides for c in side.catches), key=lambda c: c.number)
        for c in catches:
            if not _on(hatch_region, c.ball):
                raise LangError(f"{self.name}: there is no hatch under the ball of catch {c.number}: {hatch.path} "
                                f"must fill the opening, a {spec.min_gap:g} to {spec.max_gap:g} mm slot all round.",
                                panel.path)
        depth = self.pilot[1]
        for part, what in ((panel, "panel"), (hatch, "hatch")):
            if depth >= part.thickness - TOLERANCE:
                raise LangError(f"{self.name}: the pilot depth ({_mm(depth)}) must be less than the {what}'s "
                                f"thickness ({_mm(part.thickness)}).", part.path)
        gaps: list[float] = []
        for side in sides:
            gap = float(LineString([side.a, side.b]).distance(hatch.outline.geometry))
            if not spec.min_gap - TOLERANCE <= gap <= spec.max_gap + TOLERANCE:
                raise LangError(f"{self.name}: the slot between {panel.path} and {hatch.path} is {_mm(gap)} wide "
                                f"at {side.label}; the {spec.name} needs {_mm(spec.min_gap)} to "
                                f"{_mm(spec.max_gap)}.", panel.path)
            self._check_fit(panel, side, gap, region, hatch_region)
            gaps.append(gap)
        return _Plan(panel, hatch, catch_face, hatch_face, sides, gaps)

    def _opening_cut(self, opening: Operation) -> Cut:
        """The opening's cut: a through cut, one piece, a hole inside the
        panel (the add-in needs an inner loop of the face)."""
        panel, op = opening.part, opening.op
        if not isinstance(op, Cut):
            raise LangError(f"{self.name}: {opening.name!r} is not a through cut; the opening is "
                            f"{panel.name}.cut(shape, name=...).", panel.path)
        polygons = op.shape.polygons()
        if len(polygons) != 1:
            raise LangError(f"{self.name}: the opening {opening.name!r} is not one piece.", panel.path)
        exterior = unary_union([Polygon(p.exterior) for p in panel.outline.polygons()])
        hole = Polygon(polygons[0].exterior)
        if not exterior.contains(hole) or exterior.boundary.distance(hole) <= TOLERANCE:
            raise LangError(f"{self.name}: the opening {opening.name!r} reaches the edge of {panel.path}; it must "
                            "be a hole inside the board.", panel.path)
        return op

    def _catch_face(self, panel: Board, face: CatchFace) -> Face:
        if isinstance(face, Face):
            if face.part is not panel or not face.is_big:
                raise LangError(f"{self.name}: face={face!r} is not a big face of {panel.path}.", panel.path)
            return face
        return big_face(self.name, panel, face_choice(f"{self.name}(face=)", face), hidden_face(panel))

    def _hatch_face(self, panel: Board, face: Face, hatch: Board) -> Face:
        """The hatch's face the balls are screwed to: flush with the
        panel's catch face (the add-in looks for a face of another body in
        that plane)."""
        if hatch is panel:
            raise LangError(f"{self.name}: the hatch must be a board of its own, not the panel.", panel.path)
        if hatch.t_axis != panel.t_axis:
            raise LangError(f"{self.name}: {hatch.path} does not lie in the plane of {panel.path}.", panel.path)
        hatch_face = hatch.face(hatch.scope.frame.direction_of(face.axis, face.direction.sign))
        if abs(hatch_face.value - face.value) > TOLERANCE:
            raise LangError(f"{self.name}: {hatch.path} is not flush with {panel.path} on the {face.name} face the "
                            f"catches are screwed to ({hatch_face.value:g} and {face.value:g}).", panel.path)
        return hatch_face

    def _straight_edges(self, panel: Board, opening: Operation, cut: Cut, region: BaseGeometry) -> list[_Straight]:
        """The lines of the opening's contour, collinear pieces joined, each
        from its lower end, with its outward side toward the panel."""
        ring = [(float(x), float(y)) for x, y in list(cut.shape.polygons()[0].exterior.coords)[:-1]]
        lines = _joined_lines(fit(ring))
        out: list[_Straight] = []
        frame = panel.scope.frame
        axes = (panel.u_axis, panel.v_axis)
        for a, b in lines:
            if _before(b, a):
                a, b = b, a
            length = math.dist(a, b)
            along = ((b[0] - a[0]) / length, (b[1] - a[1]) / length)
            outward = (-along[1], along[0])
            middle = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            if not _on(region, _moved(middle, outward, PROBE_INSET)):
                outward = (-outward[0], -outward[1])
            label = "a straight edge of the opening"
            for i in (0, 1):
                if abs(abs(outward[i]) - 1) < 1e-9:
                    label = f"the opening's {frame.direction_of(axes[i], 1 if outward[i] > 0 else -1).name} edge"
            out.append(_Straight(a, b, along, outward, label))
        return out

    def _catch(self, side: _Straight, distance: float, number: int) -> _Catch:
        spec = self.spec
        return _Catch(number, distance, side.at(distance, spec.holder_hole_outward),
                      side.at(distance, -spec.ball_hole_inward))

    def _spaced(self, panel: Board, opening: Operation, edges: list[_Straight], edge: Pos) -> list[_Straight]:
        """The edge named takes the larger half of the catches, the one
        opposite the rest. A single catch on an edge is centred; more run
        from `end` to `end`, evenly spaced."""
        spec = self.spec
        assert self.count is not None
        axes = (panel.u_axis, panel.v_axis)
        if edge.axis not in axes:
            raise LangError(f"{self.name}: edge={edge} is not in the plane of the opening.", panel.path)
        i = axes.index(edge.axis)
        named = [e for e in edges if abs(e.a[i] - edge.value) <= TOLERANCE and abs(e.b[i] - edge.value) <= TOLERANCE]
        if len(named) != 1:
            which = "no straight edge lies" if not named else f"{len(named)} straight edges lie"
            raise LangError(f"{self.name}: {which} at {edge} on the opening {opening.name!r}; name one of its "
                            f"edges, e.g. edge={panel.name}.{opening.name}.left.", panel.path)
        selected = named[0]
        counts = [(self.count + 1) // 2, self.count // 2]
        sides = [selected]
        if counts[1]:
            sides.append(self._opposite(panel, selected, edges))
        half = spec.holder_width / 2
        number = 1
        for side, n in zip(sides, counts):
            length = side.length
            if n == 1:
                if length < spec.holder_width - TOLERANCE:
                    raise LangError(f"{self.name}: {side.label} is {_mm(length)} long, shorter than the "
                                    f"{_mm(spec.holder_width)} wide holder.", panel.path)
                distances = [length / 2]
            else:
                if self.end < half - TOLERANCE:
                    raise LangError(f"{self.name}: end must be at least {_mm(half)}: the "
                                    f"{_mm(spec.holder_width)} wide holder must sit on the straight part of the "
                                    "edge.", panel.path)
                spacing = (length - 2 * self.end) / (n - 1)
                if spacing < spec.holder_width - TOLERANCE:
                    needed = 2 * self.end + (n - 1) * spec.holder_width
                    raise LangError(f"{self.name}: {side.label} is {_mm(length)} long; {n} catches "
                                    f"{_mm(self.end)} from its ends need {_mm(needed)}.", panel.path)
                distances = [self.end + k * spacing for k in range(n)]
            side.catches = [self._catch(side, d, number + k) for k, d in enumerate(distances)]
            number += n
        return sides

    def _opposite(self, panel: Board, selected: _Straight, edges: list[_Straight]) -> _Straight:
        """The straight edge across the opening from the one named: it runs
        parallel, faces it, and overlaps it the most (the nearest one on a
        tie)."""
        length = selected.length
        candidates: list[tuple[int, float, _Straight]] = []
        for e in edges:
            if e is selected or abs(e.along[0] * selected.along[1] - e.along[1] * selected.along[0]) > 1e-9:
                continue
            across = -_dot(selected.outward, _towards(selected.a, e.a))
            if across <= TOLERANCE:
                continue
            ends = sorted(selected.distance_along(p) for p in (e.a, e.b))
            overlap = min(ends[1], length) - max(ends[0], 0.0)
            if overlap <= TOLERANCE or _dot(e.outward, selected.outward) >= 0:
                continue
            candidates.append((round(overlap / TOLERANCE), -across, e))
        if not candidates:
            raise LangError(f"{self.name}: the opening has no straight edge opposite {selected.label}; place the "
                            "catches with at= instead.", panel.path)
        return max(candidates, key=lambda c: c[:2])[2]

    def _at_points(self, panel: Board, hatch: Board, edges: list[_Straight]) -> list[_Straight]:
        """Each point goes square onto the nearest straight edge of the
        opening."""
        spec = self.spec
        assert self.at is not None
        half = spec.holder_width / 2
        sides: list[_Straight] = []
        for number, anchor in enumerate(self.at, 1):
            if anchor.part is not panel and anchor.part is not hatch:
                raise LangError(f"{self.name}: point {number} of at= lies on {anchor.part.path}, not on "
                                f"{panel.path} or {hatch.path}.", panel.path)
            if not anchor.face.is_big:
                raise LangError(f"{self.name}: point {number} of at= lies on a narrow face; name a point on a big "
                                "face.", panel.path)
            point, _ = anchor.resolve()
            nearest: tuple[float, _Straight, float] | None = None
            for e in edges:
                distance = e.distance_along(point)
                foot = e.at(min(max(distance, 0.0), e.length))
                offset = math.dist(foot, point)
                if nearest is None or offset < nearest[0]:
                    nearest = (offset, e, distance)
            assert nearest is not None
            _, side, distance = nearest
            if not any(s is side for s in sides):
                sides.append(side)
            if not half - TOLERANCE <= distance <= side.length - half + TOLERANCE:
                raise LangError(f"{self.name}: point {number} of at= is too close to the end of the straight part "
                                f"of {side.label}; the {_mm(spec.holder_width)} wide holder needs {_mm(half)} on "
                                "both sides.", panel.path)
            side.catches.append(self._catch(side, distance, number))
        for side in sides:
            side.catches.sort(key=lambda c: c.distance)
            for first, second in zip(side.catches, side.catches[1:]):
                spacing = second.distance - first.distance
                if spacing < spec.holder_width - TOLERANCE:
                    low, high = sorted((first.number, second.number))
                    raise LangError(f"{self.name}: points {low} and {high} of at= are {_mm(spacing)} apart; the "
                                    f"holders are {_mm(spec.holder_width)} wide.", panel.path)
        return sides

    def _check_fit(self, panel: Board, side: _Straight, gap: float, region: BaseGeometry,
                   hatch_region: BaseGeometry) -> None:
        """Each part needs its mounting surface beside the slot, and the
        pilot holes must land on their faces."""
        spec = self.spec
        pilot_radius = self.pilot[0] / 2
        base_radius = max(spec.ball_base_diameter / 2, pilot_radius)
        for c in side.catches:
            holder = [side.at(c.distance + sign * spec.holder_width / 2, outward)
                      for sign in (-1, 1) for outward in (PROBE_INSET, spec.mounting_depth)]
            if not all(_on(region, p) for p in holder + _rim(side, c.holder, pilot_radius)):
                raise LangError(f"{self.name}: the holder of catch {c.number} does not fit on {panel.path}; it needs "
                                f"{_mm(spec.holder_width)} x {_mm(spec.mounting_depth)} beside the opening.",
                                panel.path)
            ball = [side.at(c.distance + sign * spec.ball_width / 2, -(gap + inward))
                    for sign in (-1, 1) for inward in (PROBE_INSET, spec.mounting_depth)]
            if not all(_on(hatch_region, p) for p in ball + _rim(side, c.ball, base_radius)):
                raise LangError(f"{self.name}: the ball of catch {c.number} does not fit on the hatch; it needs "
                                f"{_mm(spec.ball_width)} x {_mm(spec.mounting_depth)} beside the slot.", panel.path)

    # -- machining and placing -------------------------------------------------------------------------

    def _drill(self, plan: _Plan, first: int) -> None:
        """A pilot hole per holder in the panel and per ball in the hatch,
        from their catch faces; named `holder_<hatch>_<n>` and
        `ball_<panel>_<n>`, n counting from `first`."""
        panel, hatch = plan.panel, plan.hatch
        diameter, depth = self.pilot
        for c in plan.catches():
            n = first + c.number - 1
            panel.add_hole(plan.face, c.holder, diameter, depth, name=f"holder_{hatch.name}_{n}")
        for c in plan.catches():
            n = first + c.number - 1
            hatch.add_hole(plan.hatch_face, c.ball, diameter, depth, name=f"ball_{panel.name}_{n}")

    def _first_number(self, plan: _Plan) -> int:
        """The number of the first catch: 1, or past the catches an earlier
        mount put on the same panel and hatch."""
        first = 1
        while (plan.panel.has_operation(f"holder_{plan.hatch.name}_{first}")
               or plan.hatch.has_operation(f"ball_{plan.panel.name}_{first}")):
            first += 1
        return first

    def _place(self, scope: Scope, plan: _Plan, first: int) -> None:
        """The catches as bodies of boxes, named `catch_<n>` like their
        holes, in an item `<hatch>_catches`."""
        bodies: list[HardwareBodyLayout] = []
        for side, gap in zip(plan.sides, plan.gaps):
            for c in side.catches:
                bodies.append(HardwareBodyLayout(name=f"catch_{first + c.number - 1}",
                                                 boxes=self._catch_body(plan, side, c, gap)))
        bodies.sort(key=lambda b: int(b["name"].rsplit("_", 1)[1]))
        base = f"{plan.hatch.name}_catches"
        taken = {item["name"] for item in scope.hardware}
        name, k = base, 2
        while name in taken:
            name, k = f"{base}_{k}", k + 1
        scope.place_hardware(name, bodies)

    def _catch_body(self, plan: _Plan, side: _Straight, c: _Catch, gap: float) -> list[BoxDict]:
        """A catch as the boxes of its `CatchShape`: the holder and its jaw
        on the panel's catch face, the ball part on the hatch's face, all
        measured from the opening's contour. On an edge at an angle to the
        axes each box is the axis-aligned box around it."""
        shape = self.shape
        # (width, from and to across the edge, outward from the contour; the face; height)
        parts = [(part.width, part.across[0], part.across[1], face, part.height)
                 for part, face in ((shape.holder, plan.face), (shape.jaw, plan.face), (shape.ball, plan.hatch_face))]
        boxes: list[BoxDict] = []
        for width, across0, across1, face, height in parts:
            corners = [side.at(c.distance + s * width / 2, across) for s in (-1, 1) for across in (across0, across1)]
            lo: dict[str, float] = {}
            hi: dict[str, float] = {}
            for i, axis in enumerate((plan.panel.u_axis, plan.panel.v_axis)):
                lo[axis], hi[axis] = min(p[i] for p in corners), max(p[i] for p in corners)
            out = face.value + face.direction.sign * height
            lo[face.axis], hi[face.axis] = min(face.value, out), max(face.value, out)
            boxes.append({"min": [lo[a] for a in AXES], "max": [hi[a] for a in AXES]})
        return boxes


def _joined_lines(curves: Sequence[Curve2]) -> list[tuple[Point2, Point2]]:
    """The lines of a closed ring of curves, consecutive collinear lines
    joined into one."""
    def collinear(p: tuple[Point2, Point2], q: tuple[Point2, Point2]) -> bool:
        u, w = _towards(*p), _towards(*q)
        nu, nw = math.hypot(*u), math.hypot(*w)
        return (math.dist(p[1], q[0]) <= 1e-9 and nu > 0 and nw > 0
                and abs(u[0] * w[1] - u[1] * w[0]) <= 1e-9 * nu * nw and _dot(u, w) > 0)

    pieces = [(c.a, c.b) if isinstance(c, Line2) else None for c in curves]
    out: list[tuple[Point2, Point2]] = []
    previous: tuple[Point2, Point2] | None = None
    for piece in pieces:
        if piece is not None:
            if previous is not None and collinear(out[-1], piece):
                out[-1] = (out[-1][0], piece[1])
            else:
                out.append(piece)
        previous = piece
    # The ring's last line may continue in its first.
    if len(out) > 1 and pieces[0] is not None and pieces[-1] is not None and collinear(out[-1], out[0]):
        out[0] = (out[-1][0], out[0][1])
        out.pop()
    return [(a, b) for a, b in out if math.dist(a, b) > TOLERANCE]


def _before(p: Point2, q: Point2) -> bool:
    """Whether `p` comes before `q`: by its first coordinate, or by its
    second where the first is the same."""
    if abs(p[0] - q[0]) > 1e-9:
        return p[0] < q[0]
    return p[1] < q[1]


def _inset(polygon: Polygon, d: float) -> BaseGeometry:
    """The polygon's outline moved `d` inward, as Fusion offsets a sketch
    loop: lines move square to themselves and meet where they met, so a
    sharp corner stays sharp, and arcs keep their centres, so a corner
    rounded with r becomes one rounded with r - d. Exact: worked out on the
    lines and arcs the polygon stands for (`lang.emit.arcs.fit`), with the
    arcs' vertices on their circles and the lines where they belong.
    Outlines it cannot offset that way (an arc or a line vanishing) are
    left to `cutouts.grown`, which is exact up to a few ten-thousandths of
    a millimetre where a line meets an arc."""
    ring = [(float(x), float(y)) for x, y in list(orient(polygon, 1.0).exterior.coords)[:-1]]
    curves = fit(ring)
    if len(curves) == 1 and isinstance(curves[0], Circle2):
        circle = curves[0]
        return cutout_geometry.circle_geometry(circle.center, circle.radius - d) if circle.radius > d else Polygon()
    moved = [_moved_curve(c, d) for c in curves]
    n = len(moved)
    joints: list[Point2 | None] = [_joint(moved[k], moved[(k + 1) % n]) for k in range(n)]
    points: list[Point2] = []
    for k, curve in enumerate(moved):
        start, end = joints[k - 1], joints[k]
        if start is None or end is None:
            return cutout_geometry.grown(polygon, -d)
        points.append(start)
        if isinstance(curve, Arc2):
            points += _arc_between(curve, start, end)
    out = Polygon(points)
    reference = cutout_geometry.grown(polygon, -d)
    if not out.is_valid or out.is_empty or out.hausdorff_distance(reference) > 0.01:
        return reference
    return out


def _moved_curve(curve: Curve2, d: float) -> Curve2:
    """A line or arc of a counter-clockwise ring moved `d` to its left,
    into the ring."""
    if isinstance(curve, Line2):
        (ax, ay), (bx, by) = curve.a, curve.b
        length = math.hypot(bx - ax, by - ay)
        nx, ny = -(by - ay) / length, (bx - ax) / length
        return Line2((ax + nx * d, ay + ny * d), (bx + nx * d, by + ny * d))
    assert isinstance(curve, Arc2)
    (ax, ay), (mx, my), (bx, by) = curve.a, curve.mid, curve.b
    left = (mx - ax) * (by - my) - (my - ay) * (bx - mx) > 0     # turning left: the centre is inside
    radius = curve.radius - d if left else curve.radius + d
    c = curve.center

    def on(p: Point2) -> Point2:
        dx, dy = p[0] - c[0], p[1] - c[1]
        k = radius / math.hypot(dx, dy)
        return (c[0] + dx * k, c[1] + dy * k)
    return Arc2(on(curve.a), on(curve.mid), on(curve.b), c, radius) if radius > 1e-9 else Line2(c, c)


def _joint(p: Curve2, q: Curve2) -> Point2 | None:
    """Where the moved curve `p` ends and `q` begins: their common end
    where they met tangentially, else where they cross (nearest the ends);
    None when they do not."""
    end, start = _ends(p)[1], _ends(q)[0]
    if math.dist(end, start) <= 1e-6:
        return ((end[0] + start[0]) / 2, (end[1] + start[1]) / 2)
    near = ((end[0] + start[0]) / 2, (end[1] + start[1]) / 2)
    if isinstance(p, Line2) and isinstance(q, Line2):
        return _lines_cross(p, q)
    if isinstance(p, Arc2) and isinstance(q, Arc2):
        return _circles_cross(p, q, near)
    line, arc = (p, q) if isinstance(p, Line2) else (q, p)
    assert isinstance(line, Line2) and isinstance(arc, Arc2)
    return _line_circle_cross(line, arc, near)


def _ends(curve: Curve2) -> tuple[Point2, Point2]:
    assert not isinstance(curve, Circle2)
    return curve.a, curve.b


def _lines_cross(p: Line2, q: Line2) -> Point2 | None:
    (ax, ay), (bx, by) = p.a, p.b
    (cx, cy), (dx, dy) = q.a, q.b
    ux, uy, wx, wy = bx - ax, by - ay, dx - cx, dy - cy
    den = ux * wy - uy * wx
    if abs(den) < 1e-12:
        return None
    t = ((cx - ax) * wy - (cy - ay) * wx) / den
    return (ax + t * ux, ay + t * uy)


def _line_circle_cross(line: Line2, arc: Arc2, near: Point2) -> Point2 | None:
    (ax, ay), (bx, by) = line.a, line.b
    (cx, cy), r = arc.center, arc.radius
    length = math.hypot(bx - ax, by - ay)
    if length == 0:
        return None
    ux, uy = (bx - ax) / length, (by - ay) / length
    fx, fy = ax - cx, ay - cy
    b = fx * ux + fy * uy
    disc = b * b - (fx * fx + fy * fy - r * r)
    if disc < 0:
        return None
    points = [(ax + t * ux, ay + t * uy) for t in (-b - math.sqrt(disc), -b + math.sqrt(disc))]
    return min(points, key=lambda x: math.dist(x, near))


def _circles_cross(p: Arc2, q: Arc2, near: Point2) -> Point2 | None:
    (pc, pr), (qc, qr) = (p.center, p.radius), (q.center, q.radius)
    dist = math.dist(pc, qc)
    if dist == 0 or dist > pr + qr or dist < abs(pr - qr):
        return None
    along = (dist * dist + pr * pr - qr * qr) / (2 * dist)
    h = math.sqrt(max(pr * pr - along * along, 0.0))
    ux, uy = (qc[0] - pc[0]) / dist, (qc[1] - pc[1]) / dist
    mx, my = pc[0] + along * ux, pc[1] + along * uy
    return min([(mx - h * uy, my + h * ux), (mx + h * uy, my - h * ux)], key=lambda x: math.dist(x, near))


def _arc_between(arc: Arc2, start: Point2, end: Point2) -> list[Point2]:
    """The vertices strictly between `start` and `end` on the arc's circle,
    the way the arc turns, at most `_ARC_STEP` apart."""
    c, r = arc.center, arc.radius
    (ax, ay), (mx, my), (bx, by) = arc.a, arc.mid, arc.b
    ccw = (mx - ax) * (by - my) - (my - ay) * (bx - mx) > 0
    a0 = math.atan2(start[1] - c[1], start[0] - c[0])
    a1 = math.atan2(end[1] - c[1], end[0] - c[0])
    sweep = (a1 - a0) % (2 * math.pi) if ccw else -((a0 - a1) % (2 * math.pi))
    steps = max(4, math.ceil(abs(sweep) / _ARC_STEP))
    return [(c[0] + r * math.cos(a0 + sweep * i / steps), c[1] + r * math.sin(a0 + sweep * i / steps))
            for i in range(1, steps)]


def _face_region(part: Board, face: Face) -> BaseGeometry:
    """A big face as an area in the outline's frame: the outline less the
    pockets, holes and V-grooves made into that face, and the pockets and
    holes from the other face that go through."""
    region: BaseGeometry = part.outline.geometry
    name, other = face.world_name, _opposite_name(part, face)
    removed: list[BaseGeometry] = []
    for op in part.ops:
        if isinstance(op, (Pocket, Hole)):
            through = op.depth >= part.thickness - 1e-9
            if op.face == name or (op.face == other and through):
                removed.append(op.shape.geometry if isinstance(op, Pocket)
                               else cutout_geometry.circle_geometry((op.u, op.v), op.d / 2))
        elif isinstance(op, VGroove) and op.face == name:
            removed.append(LineString([(op.u0, op.v0), (op.u1, op.v1)]).buffer(op.depth, cap_style="flat"))
    return region.difference(unary_union(removed)) if removed else region


def _opposite_name(part: Board, face: Face) -> str:
    """The world name of the big face across the board from `face`."""
    return part.face(part.scope.frame.direction_of(face.axis, -face.direction.sign)).world_name


def _on(region: BaseGeometry, p: Point2) -> bool:
    """Whether the point lies on the face, give or take the tolerance (the
    add-in's `isPointOnFace`)."""
    return float(region.distance(Point(p))) <= TOLERANCE


def _rim(side: _Straight, center: Point2, radius: float) -> list[Point2]:
    return [_moved(center, direction, sign * radius) for direction in (side.along, side.outward) for sign in (-1, 1)]

