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
face (the hidden one), unless `face=` names one. They are named
`catch_<hatch>_<n>` in the panel and `catch_<panel>_<n>` in the hatch, n
numbering on past the catches an earlier mount put on the same pair: the
edge named first, along each edge as the other hardware numbers, from the
bottom on an upright edge, from the panel's own left, seen from its show
face, on a level one, and toward the world axis' positive end on a panel
lying flat (`common.numbering`).

`scope.mount(catch, opening=panel.opening, edge=panel.opening.left,
hatch=hatch)` spaces `count` catches (4) over the straight edge that
`edge` names and the one across the opening from it: the edge named takes
the larger half, the first and last catch on an edge sit `end` (40) from
the ends of its straight part (where the rounded corners begin), the rest
evenly between, and a single catch is centred (`lib.stations`). With
`BallCatch(at=[...])` a catch goes to each point instead, moved square
onto the nearest straight edge of the opening. The straight edges and their ends come from
the opening's shape: its lines, between the arcs `lang.emit.arcs` finds.

It refuses what the add-in refuses: an opening that is not a hole inside
the panel, a hatch that is not flush with it on the catch face or not
under every ball, a slot narrower or wider than the catch takes, a catch
less than half the holder's width (14 mm) from the end of its straight
edge or less than a holder's width from its neighbour, a holder without
its 28 x 15 mm of panel beside the opening or a ball without its 14 x 15
mm of hatch beside the slot, pilot holes that do not fit on their faces
(`Board.hole_fits`) and pilot holes as deep as a board is thick; and,
beyond the add-in, catches so close that their pilot holes meet.

The catches are placed too, one body of boxes per catch (`CATCH_SHAPES`,
measured on Ganter's CAD model), `catch_1`, ... in an item
`<hatch>_catches`: the holder on the panel with its stop webs down the
opening's edge, its jaw reaching over the slot, and the ball part on the
hatch, in the jaw.

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
from typing import TYPE_CHECKING, Literal

from shapely.geometry import LineString, Point, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from lib import ball_catches as data
from lib.stations import stations as spread

from ..core import cutouts as cutout_geometry
from ..core.directions import AXES, Direction, InnerOuter
from ..core.errors import LangError, one_of
from ..core.layout_types import BoxDict, HardwareBodyLayout
from ..core.material import SheetMaterial
from ..core.ops import Cut
from ..core.part import Anchor, Board, Face, Operation, board
from ..core.refs import Pos, PosLike, Side, as_pos
from ..core.shapes import Shape
from ..emit.arcs import Curve2, Line2, fit
from ..joints.common import big_face, face_choice, hidden_face, make_spacing
from .common import TOLERANCE, Point2, check_hole_size, check_pilot_depth, mm, numbering

if TYPE_CHECKING:
    from ..core.scope import Scope

#: The catches of `lib.ball_catches`, by name.
CatchModel = Literal["GN 450"]
#: The face the catches are screwed to: a big face of the panel, a box side
#: or direction it faces, or inner/outer; None for the hidden face.
CatchFace = Face | Side | Direction | InnerOuter | None

#: How far inside a face the probes along its border sit, mm (the add-in's
#: 0.01 cm).
PROBE_INSET = 0.1


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
    outward over the panel positive; `rise` out of the catch face,
    negative into the slot."""
    width: float
    across: tuple[float, float]
    rise: tuple[float, float]


@dataclass(frozen=True)
class CatchShape:
    """A catch, closed, as boxes, for the layout's `hardware`: the space it
    takes, not its detail. The holder sits on the panel beside the opening,
    its stop webs reach down the opening's edge into the slot, its jaw
    reaches over the slot, and the ball part sits on the hatch with its
    ball in the jaw, so the boxes join and a catch is one body. The holder
    is placed by its screw, the ball part by its own, so the ball sits
    where the drilled holes put it."""
    #: On the panel, beside the opening.
    holder: PartBox
    #: The holder's stop webs against the opening's edge, in the slot.
    webs: PartBox
    #: The holder's jaw, over the slot and the hatch's edge.
    jaw: PartBox
    #: On the hatch, its ball in the jaw.
    ball: PartBox

    def parts(self) -> tuple[PartBox, ...]:
        return (self.holder, self.webs, self.jaw, self.ball)


#: Per catch model. GN 450-28-14 measured on Ganter's CAD model (STEP,
#: 2026-10-12): the holder 28 wide and 16 high, its screw 8.4 from the stop
#: webs' face on the opening's edge (as the drilling data has it); the
#: webs 11 deep into the slot and 2.1 across; the jaw 18.8 wide, from the
#: webs to 18.5 inside the contour, 1 above the hatch's face; the ball part
#: 14 across its ball and 13.5 high, centred on its screw, here 9.4 inside
#: the contour (the model's assembly has it at 10.15).
CATCH_SHAPES: dict[str, CatchShape] = {
    "GN 450": CatchShape(
        holder=PartBox(width=28.0, across=(-2.1, 15.5), rise=(0.0, 16.0)),
        webs=PartBox(width=28.0, across=(-2.1, 0.0), rise=(-11.0, 0.0)),
        jaw=PartBox(width=18.8, across=(-18.5, -2.1), rise=(1.0, 15.0)),
        ball=PartBox(width=14.0, across=(-16.4, -2.4), rise=(0.0, 13.5)),
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

    def __init__(self, model: CatchModel = "GN 450", *, count: int | None = None,
                 end: float = data.DEFAULT_END_OFFSET, at: Sequence[Anchor] | None = None,
                 pilot: tuple[float, float] = (data.PILOT_DIAMETER, data.PILOT_DEPTH), gap: float | None = None):
        self.spec = data.CATCHES[one_of(model, CatchModel, "BallCatch()")]
        #: The boxes the catches are drawn as.
        self.shape = CATCH_SHAPES[model]
        if at is not None:
            if count is not None:
                raise LangError(f"{self.name}: give count= or at=, not both.")
            if not at:
                raise LangError(f"{self.name}: at= is empty.")
        else:
            count = make_spacing(self.name, count if count is not None else data.DEFAULT_COUNT, None).count
            assert count is not None
            if end < 0:
                raise LangError(f"{self.name}: end must not be negative.")
            half = self.spec.holder_width / 2
            if (count + 1) // 2 > 1 and end < half - TOLERANCE:
                raise LangError(f"{self.name}: end must be at least {mm(half)}: the {mm(self.spec.holder_width)} "
                                "wide holder must sit on the straight part of the edge.")
        self.pilot = check_hole_size(self.name, "pilot", pilot)
        lo, hi = self.spec.min_gap, self.spec.max_gap
        if gap is None:
            gap = (lo + hi) / 2
        elif not lo <= gap <= hi:
            raise LangError(f"{self.name}: the slot must be {lo:g} to {hi:g} mm wide, not {gap:g}.")
        #: The catches on the edge named and the one opposite; None with at=.
        self.count: int | None = count
        #: From the ends of an edge's straight part to its first and last catch.
        self.end = float(end)
        #: Points the catches are moved onto the opening's straight edges from.
        self.at: tuple[Anchor, ...] | None = tuple(at) if at is not None else None
        #: The slot between the opening and the hatch that `hatch()` leaves.
        self.gap: float = float(gap)

    @property
    def name(self) -> str:
        return f"{self.spec.name} ball catch"

    # -- the hatch -----------------------------------------------------------------------------------

    def hatch(self, name: str, opening: Operation, material: SheetMaterial | None = None, face: CatchFace = None) -> Board:
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
        geometry = cutout_geometry.inset(cut.shape.polygons()[0], self.gap)
        if geometry.is_empty:
            raise LangError(f"{self.name}: the opening {opening.name!r} is too small for a hatch with a "
                            f"{self.gap:g} mm slot.", panel.path)
        shape = Shape(geometry)
        x0, y0, x1, y1 = shape.bounds
        stock = material if material is not None else panel.material
        assert isinstance(stock, SheetMaterial)        # a panel with an opening is a board, never a slat
        hatch = board(name, stock, shape)
        frame = hatch.scope.frame
        inward = frame.direction_of(catch_face.axis, -catch_face.direction.sign)
        hatch.on(Pos(catch_face.axis, catch_face.value), toward=inward)
        hatch.between(Pos(panel.u_axis, x0), Pos(panel.u_axis, x1), Pos(panel.v_axis, y0), Pos(panel.v_axis, y1))
        show = panel.show_face.direction
        hatch.show(frame.direction_of(show.axis, show.sign))
        return hatch

    # -- mounting ------------------------------------------------------------------------------------

    def mount(self, scope: Scope, /, *, opening: Operation, hatch: Board, edge: PosLike | None = None,
              face: CatchFace = None) -> None:
        """`scope.mount(catch, opening=panel.opening, edge=panel.opening.left,
        hatch=hatch)`: drills the panel for the holders and the hatch for
        the balls, on the edge `edge` names (a position, the opening's side
        in a direction) and the one across from it, or at the catch's `at=`
        points (then without `edge=`), and places the catches. `face=`
        names the face they are screwed to, the panel's hidden face by
        default. Nothing is drilled unless every catch fits."""
        if self.at is None and edge is None:
            raise LangError(f"{self.name}: mount() needs edge=, the straight edge of the opening the catches "
                            f"go on, e.g. edge={opening.part.name}.{opening.name}.left.", opening.part.path)
        if self.at is not None and edge is not None:
            raise LangError(f"{self.name}: with at= each catch goes to the nearest straight edge; leave out edge=.",
                            opening.part.path)
        plan = self._plan(opening, hatch, edge, face)
        first = self._first_number(plan)
        self._drill(plan, first)
        self._place(scope, plan, first)

    def _plan(self, opening: Operation, hatch: Board, edge: PosLike | None, face: CatchFace) -> _Plan:
        """Finds the edges, works out every hole and checks it, in the
        add-in's order."""
        spec = self.spec
        panel = opening.part
        cut = self._opening_cut(opening)
        catch_face = self._catch_face(panel, face)
        hatch_face = self._hatch_face(panel, catch_face, hatch)
        region = panel.face_region(catch_face)
        edges = self._straight_edges(panel, opening, cut, region)
        if not edges:
            raise LangError(f"{self.name}: the opening {opening.name!r} has no straight edges for the holders to "
                            "bear on.", panel.path)
        if edge is not None:
            sides = self._spaced(panel, opening, edges, as_pos(edge, "mount(edge=)"))
        else:
            sides = self._at_points(panel, hatch, edges)
        hatch_region = hatch.face_region(hatch_face)
        catches = sorted((c for side in sides for c in side.catches), key=lambda c: c.number)
        for c in catches:
            if not _on(hatch_region, c.ball):
                raise LangError(f"{self.name}: there is no hatch under the ball of catch {c.number}: {hatch.path} "
                                f"must fill the opening, a {spec.min_gap:g} to {spec.max_gap:g} mm slot all round.",
                                panel.path)
        for part in (panel, hatch):
            check_pilot_depth(self.name, part, self.pilot[1], "pilot")
        gaps: list[float] = []
        for side in sides:
            gap = float(LineString([side.a, side.b]).distance(hatch.outline.geometry))
            if not spec.min_gap - TOLERANCE <= gap <= spec.max_gap + TOLERANCE:
                raise LangError(f"{self.name}: the slot between {panel.path} and {hatch.path} is {mm(gap)} wide "
                                f"at {side.label}; the {spec.name} needs {mm(spec.min_gap)} to "
                                f"{mm(spec.max_gap)}.", panel.path)
            self._check_fit(panel, catch_face, hatch, hatch_face, side, gap, region, hatch_region)
            gaps.append(gap)
        self._check_apart(catches, panel, hatch)
        return _Plan(panel, hatch, catch_face, hatch_face, sides, gaps)

    def _check_apart(self, catches: list[_Catch], panel: Board, hatch: Board) -> None:
        """No two catches' holes meet: each is checked against what was
        there before, not against the others [found by fuzzing,
        2026-10-13: in an opening 20 mm tall, the balls on its two edges
        faced each other 1.2 apart]."""
        d = self.pilot[0]
        for i, a in enumerate(catches):
            for b in catches[i + 1:]:
                for board, p, q in ((panel, a.holder, b.holder), (hatch, a.ball, b.ball)):
                    if math.dist(p, q) < d - TOLERANCE:
                        raise LangError(f"{self.name}: catches {a.number} and {b.number} are too close: their "
                                        f"pilot holes in {board.path} meet.", panel.path)

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
        number = 1
        for side, n in zip(sides, counts):
            length = side.length
            if n == 1:
                if length < spec.holder_width - TOLERANCE:
                    raise LangError(f"{self.name}: {side.label} is {mm(length)} long, shorter than the "
                                    f"{mm(spec.holder_width)} wide holder.", panel.path)
                distances = [length / 2]
            else:
                distances = spread(length, n, self.end)
                if distances[1] - distances[0] < spec.holder_width - TOLERANCE:
                    needed = 2 * self.end + (n - 1) * spec.holder_width
                    raise LangError(f"{self.name}: {side.label} is {mm(length)} long; {n} catches "
                                    f"{mm(self.end)} from its ends need {mm(needed)}.", panel.path)
            order = self._order(panel, side)
            side.catches = [self._catch(side, d, number + (k if order > 0 else n - 1 - k))
                            for k, d in enumerate(distances)]
            number += n
        return sides

    def _order(self, panel: Board, side: _Straight) -> int:
        """+1 when the catches on `side` are numbered from its end `a`, -1
        from `b`: as the other hardware numbers along an edge
        (`common.numbering`), seen from the panel's show face [Florian,
        2026-10-13; they were numbered from the lower coordinates, which on
        a level edge of an upright panel is the left only facing one way]."""
        i = 0 if abs(side.along[0]) >= abs(side.along[1]) else 1
        axis = (panel.u_axis, panel.v_axis)[i]
        return numbering(-panel.show_face.direction, axis) * (1 if side.along[i] > 0 else -1)

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
                                f"of {side.label}; the {mm(spec.holder_width)} wide holder needs {mm(half)} on "
                                "both sides.", panel.path)
            side.catches.append(self._catch(side, distance, number))
        for side in sides:
            side.catches.sort(key=lambda c: c.distance)
            for first, second in zip(side.catches, side.catches[1:]):
                spacing = second.distance - first.distance
                if spacing < spec.holder_width - TOLERANCE:
                    low, high = sorted((first.number, second.number))
                    raise LangError(f"{self.name}: points {low} and {high} of at= are {mm(spacing)} apart; the "
                                    f"holders are {mm(spec.holder_width)} wide.", panel.path)
        return sides

    def _check_fit(self, panel: Board, face: Face, hatch: Board, hatch_face: Face, side: _Straight, gap: float,
                   region: BaseGeometry, hatch_region: BaseGeometry) -> None:
        """Each part needs its mounting surface beside the slot and the
        ball's base on the hatch, and the pilot holes must fit on their
        faces (`Board.hole_fits`)."""
        spec = self.spec
        pilot = self.pilot[0]
        base_radius = max(spec.ball_base_diameter / 2, pilot / 2)
        for c in side.catches:
            holder = [side.at(c.distance + sign * spec.holder_width / 2, outward)
                      for sign in (-1, 1) for outward in (PROBE_INSET, spec.mounting_depth)]
            if not all(_on(region, p) for p in holder) or not panel.hole_fits(face, c.holder, pilot):
                raise LangError(f"{self.name}: the holder of catch {c.number} does not fit on {panel.path}; it needs "
                                f"{mm(spec.holder_width)} x {mm(spec.mounting_depth)} beside the opening and its "
                                "pilot hole on the panel.", panel.path)
            ball = [side.at(c.distance + sign * spec.ball_width / 2, -(gap + inward))
                    for sign in (-1, 1) for inward in (PROBE_INSET, spec.mounting_depth)]
            if (not all(_on(hatch_region, p) for p in ball + _rim(side, c.ball, base_radius))
                    or not hatch.hole_fits(hatch_face, c.ball, pilot)):
                raise LangError(f"{self.name}: the ball of catch {c.number} does not fit on the hatch; it needs "
                                f"{mm(spec.ball_width)} x {mm(spec.mounting_depth)} beside the slot.", panel.path)

    # -- machining and placing -------------------------------------------------------------------------

    def _drill(self, plan: _Plan, first: int) -> None:
        """A pilot hole per holder in the panel and per ball in the hatch,
        from their catch faces; named `catch_<hatch>_<n>` and
        `catch_<panel>_<n>`, n counting from `first`."""
        panel, hatch = plan.panel, plan.hatch
        diameter, depth = self.pilot
        for c in plan.catches():
            n = first + c.number - 1
            panel.add_hole(plan.face, c.holder, diameter, depth, name=f"catch_{hatch.name}_{n}")
        for c in plan.catches():
            n = first + c.number - 1
            hatch.add_hole(plan.hatch_face, c.ball, diameter, depth, name=f"catch_{panel.name}_{n}")

    def _first_number(self, plan: _Plan) -> int:
        """The number of the first catch: 1, or past the catches an earlier
        mount put on the same panel and hatch."""
        first = 1
        while (plan.panel.has_operation(f"catch_{plan.hatch.name}_{first}")
               or plan.hatch.has_operation(f"catch_{plan.panel.name}_{first}")):
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
        scope.place_hardware(scope.unique_hardware_name(f"{plan.hatch.name}_catches"), bodies)

    def _catch_body(self, plan: _Plan, side: _Straight, c: _Catch, gap: float) -> list[BoxDict]:
        """A catch as the boxes of its `CatchShape`: the holder, its webs
        and its jaw from the panel's catch face, the ball part from the
        hatch's face, all measured from the opening's contour. On an edge at
        an angle to the axes each box is the axis-aligned box around it."""
        shape = self.shape
        # (width, from and to across the edge, outward from the contour; the face; height)
        parts = [(part.width, part.across[0], part.across[1], face, part.rise)
                 for part, face in ((shape.holder, plan.face), (shape.webs, plan.face), (shape.jaw, plan.face),
                                    (shape.ball, plan.hatch_face))]
        boxes: list[BoxDict] = []
        for width, across0, across1, face, (rise0, rise1) in parts:
            corners = [side.at(c.distance + s * width / 2, across) for s in (-1, 1) for across in (across0, across1)]
            lo: dict[str, float] = {}
            hi: dict[str, float] = {}
            for i, axis in enumerate((plan.panel.u_axis, plan.panel.v_axis)):
                lo[axis], hi[axis] = min(p[i] for p in corners), max(p[i] for p in corners)
            ends = [face.value + face.direction.sign * rise for rise in (rise0, rise1)]
            lo[face.axis], hi[face.axis] = min(ends), max(ends)
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


def _on(region: BaseGeometry, p: Point2) -> bool:
    """Whether the point lies on the face, give or take the tolerance (the
    add-in's `isPointOnFace`)."""
    return float(region.distance(Point(p))) <= TOLERANCE


def _rim(side: _Straight, center: Point2, radius: float) -> list[Point2]:
    """Four points `radius` from `center`, along the edge and square to it:
    where the ball's base must lie on the hatch."""
    return [_moved(center, direction, sign * radius) for direction in (side.along, side.outward) for sign in (-1, 1)]

