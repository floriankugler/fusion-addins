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

`clearance=(depth, height)`, in that order (Florian kept the pair): the
groove's bottom lies `depth` beyond the panel's edge and its ends as far
beyond the panel's corners; it is `height` wider than the panel is thick,
the play in total as with the other joints, half of it on either side of
the panel, a floor lying flat included (Florian, 2026-10-12): the floor
stays where it was placed, which is what a drawer slide measures its
cut-outs and hook holes from, and its groove reaches half the clearance
below it.

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
groove stops inside its board: `dogbones="hidden"` (the default, Florian
2026-10-12) centres the reliefs on the groove's end, touching its edges and
bulging past the end only, where the board must go on far enough (else an
error); `"corner"` puts them on the bisector, as on tenons and half laps,
bulging a little past the groove's edges too, where at a corner of the
panel the end of the board the corner goes into covers them; None leaves
them. For a `tool=` mm cutter, `relief=` wider (`lang.core.dogbones`). They
are part of the groove's pocket. The tool is only for the reliefs, so it is
checked against the groove's width only where a relief goes: a tool wider
than the groove is an error there, and passes where the groove runs out at
both ends or with `dogbones=None`.
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
from .common import (EPS, Names, Point2, PROBE, find_contacts, hidden_far_side, hidden_fits, hidden_width, other_of,
                     reported)


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
        panels: dict[int, list[Contact]] = {}
        for _, found in find_contacts(self.label, part, partners):
            for c in found:
                panels.setdefault(id(c.edge_on), []).append(c)
        plans = [self._plan(part, contacts) for contacts in panels.values()]
        names = Names(self.label)
        for plan in plans:
            plan.apply(part, names)
        names.commit()

    # -- one panel and the boards it goes into -----------------------------------------------

    def _plan(self, part: Board, contacts: list[Contact]) -> _Plan:
        """What the join does to one panel; its errors are reported on
        `part`, the board whose join() was called (`reported`)."""
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
                    with reported(self.label, part, other_of(c, part)):
                        self._check_edge(panel, c, ring[i], ring[(i + 1) % n])
            corners = [self._corner(ring, moved, i) for i in range(n)]
            grown.append(Polygon(corners, [list(r.coords) for r in orient(poly, 1.0).interiors]))
            for i, c in enumerate(moved):
                if c is None:
                    continue
                before = moved[i - 1]
                with reported(self.label, part, other_of(c, part)):
                    plan.add(self._groove(c, corners[i], corners[(i + 1) % n], before is not None,
                                          moved[(i + 1) % n] is not None))
                if before is not None and _convex(_direction(ring, i - 1), _direction(ring, i)):
                    chamfered.append(corner_geometry.Named(
                        corners[i], f"the corner in {before.face_on.path} and {c.face_on.path}"))
        with reported(self.label, part, None if part is panel else panel):
            geometry = unary_union(grown)
            if not geometry.is_valid or geometry.area < old.area - EPS:
                raise LangError(f"moving the edges of {panel.path} into the grooves leaves no proper outline.")
            shape = Shape(geometry, old.axes)
            if self.chamfer > 0 and chamfered:
                # cut off as chamfer() cuts off a corner of the outline
                clipped = corner_geometry.clip_corners(shape, chamfered, self.chamfer, panel.path)
                if shape.difference(clipped).intersection(old).area > EPS:
                    raise LangError(f"a {self.chamfer:g} mm chamfer reaches out of the grooves at {panel.path}'s "
                                    f"corners, where it shows; at most twice the depth ({2 * self.depth:g}).")
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
            raise LangError(f"the edge of {panel.path} on {board.path} reaches past {panel.path}'s box ({c.axis} "
                            f"{b.lo[c.axis]:g} to {b.hi[c.axis]:g}) into a board an earlier join set it into; "
                            f"name the boards at its corners in one join, so that the corner goes into both.")
        clearance = self.clearance[0]
        if self.depth + clearance >= board.thickness - EPS:
            raise LangError(f"a groove {self.depth:g} deep, {clearance:g} beyond the panel's edge, would go through "
                            f"{board.path} ({board.thickness:g} thick) and show on its far face.")

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
        pb = panel.box()
        w0, w1 = pb.lo[t] - height / 2, pb.hi[t] + height / 2
        frame = _Frame(board, c.axis, t)
        shape = frame.rect(a0, a1, w0, w1)
        material = board.outline.geometry
        reliefs: list[Shape] = []
        notes: list[str] = []
        for a, s_a, joined in ((a0, -1, ends[0][1]), (a1, 1, ends[1][1])):
            beyond = material.contains(Point(frame.point(a + s_a * PROBE, (w0 + w1) / 2)))
            if not beyond and not joined:
                end_name = board.scope.frame.direction_of(c.axis, s_a).name
                notes.append(f"{board.path}: the groove for {panel.path} runs out of it at its {end_name} end, "
                             "where it shows unless something covers it.")
            if self.dogbones is None:
                continue
            for w, s_w in ((w0, -1), (w1, 1)):
                around = [frame.point(a + s_a * PROBE, w - s_w * PROBE),     # past the end
                          frame.point(a - s_a * PROBE, w + s_w * PROBE),     # past the edge
                          frame.point(a + s_a * PROBE, w + s_w * PROBE)]     # past both
                if all(material.contains(Point(p)) for p in around):
                    reliefs.append(self._relief(frame, (a, w), s_a, s_w, w1 - w0, panel, board))
        for relief in reliefs:
            shape = shape.union(relief)
        return _Cut(board, c.face, shape, self.depth + clearance, notes)

    def _relief(self, frame: _Frame, corner: tuple[float, float], s_a: int, s_w: int, width: float,
                panel: Board, board: Board) -> Shape:
        """The dog bone in the groove's corner at its end `s_a` and edge
        `s_w`; the end runs across the groove, the edge along it."""
        if self.tool > width + EPS:
            raise LangError(f"the groove for {panel.path} is {width:g} wide, narrower than the {self.tool:g} mm "
                            "tool its dog bones are for; give a smaller tool= or dogbones=None.")
        point = frame.point(*corner)
        across = frame.direction(0.0, -s_w)          # along the end, into the groove
        back = frame.direction(-s_a, 0.0)            # along the edge, back into the groove
        if self.dogbones == "hidden":
            if not hidden_fits(width, self.tool, self.relief):
                raise LangError(f"hidden dog bones are {hidden_width(self.tool, self.relief):g} across, wider than "
                                f"the {width:g} mm groove for {panel.path}; use corner dog bones or a smaller tool.")
            # centred on the end, bulging past it
            far = hidden_far_side(corner, (0.0, -s_w), (s_a, 0.0), self.tool, self.relief)
            if not board.outline.geometry.contains(Point(frame.point(*far))):
                raise LangError(f"hidden dog bones would break out of {board.path} past the end of the groove for "
                                f"{panel.path}; use corner dog bones or a smaller tool.")
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

    def apply(self, part: Board, names: Names) -> None:
        """Changes the panel and the boards; errors are reported on `part`,
        the board whose join() was called."""
        panel = self.panel
        assert self.outline is not None
        with reported(Groove.label, part, None if part is panel else panel):
            panel.add_to_outline(self.outline)
        for cut in self.cuts:
            board = cut.board
            with reported(Groove.label, part, board if part is panel else panel):
                board.add_pocket(cut.face, cut.shape, cut.depth, name=names(board, f"groove_{panel.name}", panel))
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
           dogbones: DogBones | None = "hidden", tool: float = 6.0, relief: float = 0.1) -> Groove:
    """A groove `depth` deep for each board named (or, written from a board,
    for each panel named), `clearance=(depth, height)` the room beyond the
    panel's edges (depth, beyond each edge and end) and around it (height,
    in total, half on either side), `chamfer` along both edges at the
    panel's corners between two grooves (None or 0 for none), dog bones for
    a `tool` mm cutter, `relief` wider, where a groove stops inside its
    board: past the groove's end (`"hidden"`), on the corners
    (`"corner"`), or None. The tool is checked against the groove's width
    only where a relief goes, as it cuts nothing else."""
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
