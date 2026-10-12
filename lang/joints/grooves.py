"""Grooves: a panel set into grooves in the boards around it, as a drawer
floor in its box (see `lang.core.contact`).

`floor.join(l, r, f, k, using=groove(5, clearance=(0.5, 0.5)))`: the panel
is placed between the boards' faces, so it meets each of them edge-on. The
join moves each edge of the panel that lies on a named board's face `depth`
into that board, a corner between two such edges with both, and cuts every
board a groove for what then lies in it: a pocket from the face the panel
meets, named `groove_<panel>`. The panel's box stays where it was placed
(`Board.add_to_outline`), as with tenons. Either board may make the call,
`left.join(floor, using=groove(5))` grooving the left side alone; the
boards at a corner of the panel go into one join, so that the corner goes
into both, and a later join at a corner an earlier one moved is an error.

`clearance=(depth, height)`: the groove's bottom lies `depth` beyond the
panel's edge and its ends as far beyond the panel's corners; it is `height`
wider than the panel is thick, all of it above a panel lying flat, whose
underside stays on the groove's lower wall (what a drawer slide measures
its cut-outs and hook holes from), half of it on either side of a panel
that stands.

A groove is as long as the panel needs: it stops inside its board where the
board goes on past the panel's corner, and runs out of it where the board
ends first, as into a box joint's gap. At a corner of the panel either way
is covered by the board the corner goes into, so nothing shows. An end that
runs out where the panel's edge beside it goes into no board of the join (a
floor running on under a back that stands on it) may show; its board gets a
note for the layout's problems. A groove as deep as its board is thick
would show on the far face, an error. Since the grooves take everything in
their way, they also take the fillets a box joint's cutter keeps at the
roots of the fingers, which reach into the panel's corner where it lies
near the end of a finger.

`chamfer=` (3) cuts the panel's corners between two grooved edges at 45
degrees, that much along each edge, so that it goes in easily: a change of
its outline, inside the grooves (at most twice the depth, else it would
show). None or 0 leaves them square.

A router leaves its radius in the two inside corners at each end where a
groove stops inside its board: `dogbones="corner"` (the default, as on
tenons and half laps) relieves them on the bisector, bulging a little past
the groove's edges, where at a corner of the panel the end of the board the
corner goes into covers them; `"hidden"` centres them on the groove's end,
bulging past the end only; None leaves them. For a `tool=` mm cutter,
`relief=` wider (`lang.core.dogbones`). They are part of the groove's
pocket.
"""
from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import ClassVar

from shapely.geometry import Point, Polygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

from ..core import corners as corner_geometry
from ..core.contact import Contact
from ..core.directions import Axis
from ..core.dogbones import DogBones, corner_relief, hidden_relief
from ..core.errors import LangError, one_of
from ..core.part import Board, Face
from ..core.shapes import Shape, box_shape
from .common import EPS, Point2, touching

#: How far from a corner the probes for material lie, mm.
_PROBE = 0.01


@dataclass(frozen=True)
class Groove:
    depth: float
    #: (depth, height): beyond the panel's edges, and wider than the panel.
    clearance: tuple[float, float]
    chamfer: float
    dogbones: DogBones | None
    tool: float
    relief: float
    label: ClassVar[str] = "groove"

    def join(self, part: Board, /, partners: list[Board]) -> None:
        # Every panel is planned, and every check made, before any board
        # changes, so a failed join changes none.
        found: list[Contact] = []
        for other in partners:
            here = touching(part, other)
            if not here:
                raise LangError(f"groove: {other.path} does not touch this board with an end or edge on a face.",
                                part.path)
            found.extend(here)
        panels: dict[int, list[Contact]] = {}
        for c in found:
            panels.setdefault(id(c.edge_on), []).append(c)
        plans = [self._plan(contacts) for contacts in panels.values()]
        for plan in plans:
            plan.apply()

    # -- one panel and the boards it goes into -----------------------------------------------

    def _plan(self, contacts: list[Contact]) -> _Plan:
        panel = contacts[0].edge_on
        old = panel.outline
        plan = _Plan(panel)
        grown: list[Polygon] = []
        chamfered: list[corner_geometry.Named] = []
        for poly in old.polygons():
            ring = _ring(poly)
            n = len(ring)
            moved = [_contact_of(panel, ring[i], ring[(i + 1) % n], contacts) for i in range(n)]
            if not any(moved):
                grown.append(poly)
                continue
            for i, c in enumerate(moved):
                if c is not None:
                    self._check_edge(panel, c, ring[i], ring[(i + 1) % n])
            corners = [self._corner(ring, moved, i) for i in range(n)]
            grown.append(Polygon(corners, [list(r.coords) for r in orient(poly, 1.0).interiors]))
            for i, c in enumerate(moved):
                if c is None:
                    continue
                before = moved[i - 1]
                plan.add(self._groove(c, corners[i], corners[(i + 1) % n], before is not None,
                                      moved[(i + 1) % n] is not None))
                if before is not None and _convex(_direction(ring, i - 1), _direction(ring, i)):
                    chamfered.append(corner_geometry.Named(
                        corners[i], f"the corner in {before.face_on.path} and {c.face_on.path}"))
        geometry = unary_union(grown)
        if not geometry.is_valid or geometry.area < old.area - EPS:
            raise LangError("groove: moving the edges into the grooves leaves no proper outline.", panel.path)
        shape = Shape(geometry, old.axes)
        if self.chamfer > 0 and chamfered:
            # cut off as chamfer() cuts off a corner of the outline
            clipped = corner_geometry.clip_corners(shape, chamfered, self.chamfer, panel.path)
            if shape.difference(clipped).intersection(old).area > EPS:
                raise LangError(f"groove: a {self.chamfer:g} mm chamfer reaches out of the grooves at this panel's "
                                f"corners, where it shows; at most twice the depth ({2 * self.depth:g}).", panel.path)
            shape = clipped
        plan.outline = shape
        return plan

    def _check_edge(self, panel: Board, c: Contact, p: Point2, q: Point2) -> None:
        """An edge to move: it lies within the panel's box, else an earlier
        join moved the edge beside it into another board."""
        board = c.face_on
        b, i = panel.box(), _index(panel, c.axis)
        lo, hi = sorted((p[i], q[i]))
        if lo < b.lo[c.axis] - EPS or hi > b.hi[c.axis] + EPS:
            raise LangError(f"groove: the edge on {board.path} reaches past the panel's box ({c.axis} "
                            f"{b.lo[c.axis]:g} to {b.hi[c.axis]:g}) into a board an earlier join set it into; "
                            f"name the boards at its corners in one join, so that the corner goes into both.",
                            panel.path)
        clearance = self.clearance[0]
        if self.depth + clearance >= board.thickness - EPS:
            raise LangError(f"groove: a groove {self.depth:g} deep, {clearance:g} beyond the panel's edge, would go "
                            f"through {board.path} ({board.thickness:g} thick) and show on its far face.",
                            panel.path)

    def _corner(self, ring: list[Point2], moved: list[Contact | None], i: int) -> Point2:
        """Vertex i once the edges into the boards have moved: where the
        lines of the edges before and after it now cross."""
        before, after = moved[i - 1], moved[i]
        if before is None and after is None:
            return ring[i]
        p1, d1 = _line(ring, i - 1, self.depth if before else 0.0)
        p2, d2 = _line(ring, i, self.depth if after else 0.0)
        cross = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(cross) < 1e-12:
            # Two edges in one line, which `_ring` does not leave: the
            # vertex moves with the one that moves.
            return _onto(ring[i], p2, d2) if after else _onto(ring[i], p1, d1)
        s = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / cross
        return (p1[0] + s * d1[0], p1[1] + s * d1[1])

    def _groove(self, c: Contact, start: Point2, end: Point2, start_joined: bool, end_joined: bool) -> _Cut:
        """The groove in the board for one moved edge, from its new `start`
        to its `end`, each of which went into another board of the join
        when `*_joined`."""
        panel, board = c.edge_on, c.face_on
        t = panel.t_axis
        i = _index(panel, c.axis)
        ends = sorted([(start[i], start_joined), (end[i], end_joined)])
        clearance, height = self.clearance
        a0, a1 = ends[0][0] - clearance, ends[1][0] + clearance
        below, above = self._height(panel, height)
        pb = panel.box()
        w0, w1 = pb.lo[t] - below, pb.hi[t] + above
        frame = _Frame(board, c.axis, t)
        shape = frame.rect(a0, a1, w0, w1)
        material = board.outline.geometry
        reliefs: list[Shape] = []
        notes: list[str] = []
        for a, s_a, joined in ((a0, -1, ends[0][1]), (a1, 1, ends[1][1])):
            beyond = material.contains(Point(frame.point(a + s_a * _PROBE, (w0 + w1) / 2)))
            if not beyond and not joined:
                end_name = board.scope.frame.direction_of(c.axis, s_a).name
                notes.append(f"{board.path}: the groove for {panel.path} runs out of it at its {end_name} end, "
                             "where it shows unless something covers it.")
            if self.dogbones is None:
                continue
            for w, s_w in ((w0, -1), (w1, 1)):
                around = [frame.point(a + s_a * _PROBE, w - s_w * _PROBE),     # past the end
                          frame.point(a - s_a * _PROBE, w + s_w * _PROBE),     # past the edge
                          frame.point(a + s_a * _PROBE, w + s_w * _PROBE)]     # past both
                if all(material.contains(Point(p)) for p in around):
                    reliefs.append(self._relief(frame, (a, w), s_a, s_w, w1 - w0, panel, board))
        for relief in reliefs:
            shape = shape.union(relief)
        return _Cut(board, c.face, shape, self.depth + clearance, notes)

    def _height(self, panel: Board, height: float) -> tuple[float, float]:
        """How much of the clearance in height goes below and above the
        panel: all above a panel lying flat, half either side else."""
        top = panel.scope.frame.direction("top")
        if top.axis != panel.t_axis:
            return height / 2, height / 2
        return (0.0, height) if top.sign > 0 else (height, 0.0)

    def _relief(self, frame: _Frame, corner: tuple[float, float], s_a: int, s_w: int, width: float,
                panel: Board, board: Board) -> Shape:
        """The dog bone in the groove's corner at its end `s_a` and edge
        `s_w`; the end runs across the groove, the edge along it."""
        if self.tool > width + EPS:
            raise LangError(f"groove: the groove for {panel.path} is {width:g} wide, narrower than the "
                            f"{self.tool:g} mm tool its dog bones are for; give a smaller tool= or dogbones=None.",
                            board.path)
        point = frame.point(*corner)
        across = frame.direction(0.0, -s_w)          # along the end, into the groove
        back = frame.direction(-s_a, 0.0)            # along the edge, back into the groove
        if self.dogbones == "hidden":
            r = (self.tool + self.relief) / 2
            if width < 2 * r - EPS:
                raise LangError(f"groove: hidden dog bones are {2 * r:g} across, wider than the "
                                f"{width:g} mm groove for {panel.path}; use corner dog bones or a smaller tool.",
                                board.path)
            a, w = corner
            if not board.outline.geometry.contains(Point(frame.point(a + s_a * (r + _PROBE), w - s_w * r))):
                raise LangError(f"groove: hidden dog bones would break out of {board.path} past the end of the "
                                f"groove for {panel.path}; use corner dog bones or a smaller tool.", board.path)
            return hidden_relief(point, across, self.tool, self.relief)
        return corner_relief(point, across, back, self.tool, self.relief)


@dataclass
class _Cut:
    """A groove to cut: its board, the face it is cut from, its shape in
    the board's outline frame, its depth and the notes it leaves."""
    board: Board
    face: Face
    shape: Shape
    depth: float
    notes: list[str]


@dataclass
class _Plan:
    """What a join does to one panel: its new outline, and per board the
    groove for it."""
    panel: Board
    outline: Shape | None = None
    cuts: list[_Cut] = field(default_factory=list[_Cut])

    def add(self, cut: _Cut) -> None:
        for i, other in enumerate(self.cuts):
            if other.board is cut.board:
                self.cuts[i] = _Cut(cut.board, cut.face, other.shape.union(cut.shape), cut.depth,
                                    other.notes + cut.notes)
                return
        self.cuts.append(cut)

    def apply(self) -> None:
        panel = self.panel
        assert self.outline is not None
        panel.add_to_outline(self.outline)
        for cut in self.cuts:
            board = cut.board
            board.add_pocket(cut.face, cut.shape, cut.depth, name=board.unique_op_name(f"groove_{panel.name}"))
            board.notes.extend(cut.notes)


class _Frame:
    """Points of a groove in its board's outline frame, by (along the
    groove, across it: the panel's thickness axis)."""

    def __init__(self, board: Board, along: Axis, across: Axis):
        self.board = board
        self.along: Axis = along
        self.across: Axis = across

    def point(self, a: float, w: float) -> Point2:
        coords: dict[Axis, float] = {self.along: a, self.across: w}
        return (coords[self.board.u_axis], coords[self.board.v_axis])

    def direction(self, a: float, w: float) -> Point2:
        """A direction by (along, across); the frame only swaps axes."""
        return self.point(a, w)

    def rect(self, a0: float, a1: float, w0: float, w1: float) -> Shape:
        (u0, v0), (u1, v1) = self.point(a0, w0), self.point(a1, w1)
        return box_shape(min(u0, u1), min(v0, v1), max(u0, u1), max(v0, v1))


# -- the panel's outline ---------------------------------------------------------------------

def _ring(poly: Polygon) -> list[Point2]:
    """The polygon's exterior, counter-clockwise, without the vertices
    that lie in the middle of a straight edge."""
    points: list[Point2] = [(float(x), float(y)) for x, y in list(orient(poly, 1.0).exterior.coords)[:-1]]
    changed = True
    while changed and len(points) > 3:
        changed = False
        for i in range(len(points)):
            a, b, c = points[i - 1], points[i], points[(i + 1) % len(points)]
            cross = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
            if abs(cross) <= 1e-9 * max(1.0, math.dist(a, b) * math.dist(b, c)):
                del points[i]
                changed = True
                break
    return points


def _index(panel: Board, axis: Axis) -> int:
    """Which coordinate of the panel's outline frame lies on `axis`."""
    return 0 if panel.u_axis == axis else 1


def _contact_of(panel: Board, p: Point2, q: Point2, contacts: Sequence[Contact]) -> Contact | None:
    """The contact whose board the edge from p to q lies on, with the
    panel on the near side of that board's face, if any."""
    for c in contacts:
        n, a = _index(panel, c.face.axis), _index(panel, c.axis)
        if abs(p[n] - c.plane) > EPS or abs(q[n] - c.plane) > EPS:
            continue
        lo, hi = sorted((p[a], q[a]))
        if min(hi, c.hi) - max(lo, c.lo) <= EPS:
            continue
        # outward (to the right of the counter-clockwise edge) must point into the board
        d = (q[0] - p[0], q[1] - p[1])
        outward = (d[1], -d[0])[n]
        if outward * c.end.direction.sign > 0:
            return c
    return None


def _direction(ring: list[Point2], i: int) -> Point2:
    """The unit vector along edge i, from vertex i to vertex i + 1."""
    p, q = ring[i % len(ring)], ring[(i + 1) % len(ring)]
    length = math.dist(p, q)
    return ((q[0] - p[0]) / length, (q[1] - p[1]) / length)


def _line(ring: list[Point2], i: int, offset: float) -> tuple[Point2, Point2]:
    """Edge i's line moved `offset` outward: a point on it and its direction."""
    d = _direction(ring, i)
    p = ring[i % len(ring)]
    return (p[0] + d[1] * offset, p[1] - d[0] * offset), d


def _onto(point: Point2, origin: Point2, d: Point2) -> Point2:
    """`point` projected onto the line through `origin` along `d`."""
    s = (point[0] - origin[0]) * d[0] + (point[1] - origin[1]) * d[1]
    return (origin[0] + s * d[0], origin[1] + s * d[1])


def _convex(before: Point2, after: Point2) -> bool:
    """Whether a counter-clockwise ring turns left at a vertex, its edges
    running along `before` into it and `after` out of it."""
    return before[0] * after[1] - before[1] * after[0] > EPS


def groove(depth: float, *, clearance: tuple[float, float] = (0.0, 0.0), chamfer: float | None = 3.0,
           dogbones: DogBones | None = "corner", tool: float = 6.0, relief: float = 0.1) -> Groove:
    """A groove `depth` deep for each board named (or, written from a board,
    for each panel named), `clearance=(depth, height)` the room beyond the
    panel's edges and above it, `chamfer` along both edges at the panel's
    corners between two grooves (None or 0 for none), dog bones for a
    `tool` mm cutter, `relief` wider, where a groove stops inside its
    board: on the corners (`"corner"`), along the groove's end
    (`"hidden"`), or None."""
    if depth <= 0:
        raise LangError(f"groove: depth must be positive, got {depth:g}.")
    if min(clearance) < 0:
        raise LangError("groove: clearance must not be negative.")
    size = 0.0 if chamfer is None else float(chamfer)
    if size < 0:
        raise LangError("groove: chamfer must not be negative.")
    if size > 2 * depth + EPS:
        raise LangError(f"groove: a {size:g} mm chamfer reaches out of a {depth:g} mm groove at the panel's corners, "
                        f"where it shows; at most twice the depth ({2 * depth:g}).")
    if dogbones is not None:
        one_of(dogbones, DogBones, "groove(dogbones=)")
    if tool <= 0:
        raise LangError("groove: tool must be positive.")
    if relief < 0:
        raise LangError("groove: relief must not be negative.")
    return Groove(float(depth), (float(clearance[0]), float(clearance[1])), size, dogbones, float(tool),
                  float(relief))
