"""Contours: polylines from the master, as limits of a board.

A contour is one sketch of the master, sampled to a polyline in world
millimetres (`lang.master`). Given to `between()`, it limits the board the
way the board's plane meets it:

- In the board's own plane (the contour's normal is the thickness axis),
  it is projected along the thickness. A closed contour bounds the outline:
  the board is what lies inside it. An open one is an edge the board stops
  at: it limits the axis across its chord (the line from its first to its
  last point), the board keeps the side its other limit on that axis is
  on, and the edge follows the contour, `batten.between(top, profile)`.
  It must run one way along its chord's axis: one that runs back along
  itself, an overhang, is an error (a lip is a closed contour), and so is
  one that runs straight back over itself, a spike, in any direction.
- In a perpendicular plane, the board fits over its whole thickness: its
  section across that plane, from one big face to the other, keeps clear
  of the contour. A closed contour gives a stretch on the axis the two
  planes share, `batten.between(top, profile, floor_outline)`; an open one
  a position on it, and must run one way through the board's thickness,
  without a spike.

`contour.gap(n)` keeps n mm of clearance, measured in the contour's
plane; `contour.into(n)` reaches n mm past it. All of it is polyline math
with shapely; nothing is projected in Fusion.
"""
from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import NamedTuple, cast

import shapely
from shapely import make_valid
from shapely.geometry import LineString, MultiPolygon, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from .box import Box
from .directions import AXES, Axis
from .errors import LangError
from .shapes import Shape
from .geometry import NARROWEST, clean, parts_of, polygons_of

Point3 = tuple[float, float, float]
Point2 = tuple[float, float]
#: How far an open contour is extended past its ends, and how far its
#: removed side reaches (mm).
_FAR = 1e5
#: A contour is planar when its points lie this close to its plane (mm).
_PLANAR = 0.01
#: A closed contour must hold the board this far inside its faces, so that
#: a contour edge lying exactly in a face does not count as crossing it.
_INSIDE = 1e-6
#: How far (mm) an open contour may run back along the way it runs: nothing
#: narrower is meant, and the snapshot rounds its points to 1e-4.
_BACK = NARROWEST


@dataclass(frozen=True, eq=False)
class Contour:
    """A sketch of the master as a polyline, world mm. `between()` takes it
    as a limit; `gap()` and `into()` give it a clearance."""
    name: str
    points: tuple[Point3, ...]
    closed: bool
    #: The sketch plane.
    origin: Point3
    normal: Point3

    def __repr__(self) -> str:
        return f"Contour({self.name!r}, {len(self.points)} points, {'closed' if self.closed else 'open'})"

    @property
    def normal_axis(self) -> Axis:
        """The world axis the contour's plane is perpendicular to."""
        for i, axis in enumerate(AXES):
            if abs(abs(self.normal[i]) - 1.0) < 1e-6:
                return axis
        raise LangError(f"contour {self.name!r} lies in a tilted plane; only axis-aligned contours are limits.")

    @property
    def plane_value(self) -> float:
        return self.origin[AXES.index(self.normal_axis)]

    def coords(self, a: Axis, b: Axis) -> list[Point2]:
        """The points as (a, b) pairs."""
        ia, ib = AXES.index(a), AXES.index(b)
        return [(p[ia], p[ib]) for p in self.points]

    def check_planar(self) -> None:
        i = AXES.index(self.normal_axis)
        off = max(abs(p[i] - self.plane_value) for p in self.points)
        if off > _PLANAR:
            raise LangError(f"contour {self.name!r} is not planar (a point lies {off:g} mm off its plane).")

    def polygon(self, a: Axis, b: Axis) -> BaseGeometry:
        """A closed contour as an area in (a, b)."""
        if not self.closed:
            raise LangError(f"contour {self.name!r} is open; this needs a closed one.")
        if len(self.points) < 3:
            raise LangError(f"contour {self.name!r} is closed around nothing ({len(self.points)} points).")
        return _area(make_valid(Polygon(self.coords(a, b))))

    def gap(self, n: float) -> ContourLimit:
        """As a limit: n mm of clearance to the contour."""
        return ContourLimit(self, float(n))

    def into(self, n: float) -> ContourLimit:
        """As a limit: reaching n mm past the contour."""
        return ContourLimit(self, -float(n))


@dataclass(frozen=True)
class ContourLimit:
    """A contour as a `between()` limit, with the clearance the board keeps
    to it; negative reaches past it."""
    contour: Contour
    gap: float = 0.0


class End(NamedTuple):
    """Where an open contour across the board puts the board's end on an
    axis, and the side of it the board lies on (+1: toward higher values)."""
    value: float
    side: int
    name: str


def as_contour_limit(limit: Contour | ContourLimit) -> ContourLimit:
    return limit if isinstance(limit, ContourLimit) else ContourLimit(limit)


def _area(g: BaseGeometry) -> BaseGeometry:
    """The polygonal part of a geometry (make_valid may add lines)."""
    if isinstance(g, (Polygon, MultiPolygon)):
        return g
    parts = polygons_of(g)
    return unary_union(parts) if parts else Polygon()


def round_offset(area: BaseGeometry, distance: float) -> BaseGeometry:
    """The area grown by `distance` (shrunk when it is negative); round
    joins keep a clearance exact at corners. GEOS simplifies what it
    offsets, by about a hundredth of the distance and only ever toward more
    clearance, and how depends on where a ring starts, which way it runs
    and the points along its edges: so the area is given to it in one
    form, those points dropped (the same outline run the other way with
    points added along it kept 26.03 mm instead of a 26 mm gap [found by
    fuzzing, 2026-10-14]). (An offset of its own, a rectangle along every
    segment and a disc about every vertex, would be exact, but GEOS unites
    such pieces wrongly, without an error, where their edges nearly
    coincide, as along a strip twice the distance wide.)"""
    if not distance:
        return area
    polygons = [Polygon(_ring_without_edge_points(p.exterior.coords),
                        [_ring_without_edge_points(h.coords) for h in p.interiors]) for p in polygons_of(area)]
    grown = shapely.normalize(polygons[0] if len(polygons) == 1 else MultiPolygon(polygons)).buffer(distance)
    # (cleaned: an area shrunk by half its width leaves a sliver of no width, invalid [found by
    # fuzzing, 2026-10-14: a slot 1 mm wide shrunk by 0.5])
    return clean(grown)


def _ring_without_edge_points(coords: Iterable[Sequence[float]]) -> list[Point2]:
    """A ring's vertices without those that lie on the edge between their
    neighbours (within 1e-9 mm) or on the one before. (Simplifying it does
    not drop them all: a point Douglas-Peucker splits at stays.)"""
    out: list[Point2] = []
    for c in list(coords)[:-1]:
        p = (float(c[0]), float(c[1]))
        while len(out) >= 2 and _on_edge(out[-2], out[-1], p):
            out.pop()
        if not out or p != out[-1]:
            out.append(p)
    changed = True
    while changed and len(out) > 3:
        changed = False
        if _on_edge(out[-2], out[-1], out[0]) or out[-1] == out[0]:
            out.pop()
            changed = True
        elif _on_edge(out[-1], out[0], out[1]):
            out.pop(0)
            changed = True
    return out


def _on_edge(a: Point2, b: Point2, c: Point2) -> bool:
    """Whether b lies on the edge from a to c, within 1e-9 mm."""
    dx, dy = c[0] - a[0], c[1] - a[1]
    length2 = dx * dx + dy * dy
    if length2 == 0:
        return False
    t = ((b[0] - a[0]) * dx + (b[1] - a[1]) * dy) / length2
    return 0 < t < 1 and abs((b[0] - a[0]) * dy - (b[1] - a[1]) * dx) <= 1e-9 * math.sqrt(length2)


class _OpenEdge:
    """An open contour in the board's plane: the edge the board stops at on
    axis `a` (across its chord), following it along axis `b`."""

    def __init__(self, limit: ContourLimit, a: Axis, b: Axis, path: str):
        self.limit, self.path = limit, path
        self.a: Axis = a
        self.b: Axis = b
        c = limit.contour
        self.points_ab = c.coords(a, b)
        values = [p[0] for p in self.points_ab]
        self.lo, self.hi = min(values), max(values)
        #: +1 when the board lies on the high side of the contour on `a`.
        self.side = 0

    @property
    def name(self) -> str:
        return self.limit.contour.name

    def choose_side(self, reference: float) -> None:
        if reference > self.hi:
            self.side = 1
        elif reference < self.lo:
            self.side = -1
        else:
            raise LangError(
                f"contour {self.name!r}: the board's other limit on {self.a} ({reference:g}) lies within "
                f"the contour's reach ({self.lo:g} to {self.hi:g}), so the side the board is on is unclear.",
                self.path)

    def far(self) -> float:
        """A value on `a` past the contour, on the side away from the board;
        the trim then moves the edge onto the contour."""
        margin = abs(self.limit.gap) + 1.0
        return self.lo - margin if self.side > 0 else self.hi + margin

    def removed(self, u: Axis) -> BaseGeometry:
        """The region beyond the contour (grown by the clearance), in the
        board's (u, v)."""
        region = _beyond([(b, a) for a, b in self.points_ab], self.side, self.limit.gap)
        # (b, a) -> (u, v)
        if self.a == u:
            return _swap(region)
        return region


def _beyond(points: list[Point2], side: int, gap: float) -> BaseGeometry:
    """What lies beyond an open contour, away from the board (`side` +1:
    the board toward higher second coordinates), grown by the clearance:
    the contour given as (b, a) points, run along b in increasing order,
    extended along b past both ends and closed far away on that side."""
    pts = list(points)
    if pts[0][0] > pts[-1][0]:
        pts.reverse()
    values = [p[1] for p in pts]
    lo_b, hi_b = pts[0][0] - _FAR, pts[-1][0] + _FAR
    far_a = min(values) - _FAR if side > 0 else max(values) + _FAR
    ring = [(lo_b, pts[0][1])] + pts + [(hi_b, pts[-1][1]), (hi_b, far_a), (lo_b, far_a)]
    return round_offset(_area(make_valid(Polygon(ring))), gap)


def _swap(g: BaseGeometry) -> BaseGeometry:
    from shapely import affinity
    return affinity.affine_transform(g, [0, 1, 1, 0, 0, 0])


class ContourLimits:
    """The contour limits of one board, classified against its plane. The
    board asks it for ends, stretches and edges per in-plane axis, and
    for the trim of its outline."""

    def __init__(self, limits: Sequence[ContourLimit], t: Axis, t_lo: float, t_hi: float,
                 u: Axis, v: Axis, path: str):
        self.t: Axis = t
        self.u: Axis = u
        self.v: Axis = v
        self.t_lo, self.t_hi, self.path = t_lo, t_hi, path
        #: Closed contours in the board's plane, as areas in (u, v).
        self.areas: list[tuple[str, BaseGeometry]] = []
        #: Open contours in the board's plane, by the axis they limit.
        self.edges: dict[Axis, list[_OpenEdge]] = {u: [], v: []}
        #: Closed contours in a perpendicular plane: (name, area in (t, s)) by the shared axis s.
        self.sections: dict[Axis, list[tuple[str, BaseGeometry]]] = {u: [], v: []}
        #: Open contours in a perpendicular plane: (limit, line in (t, s)) by s.
        self.crossings: dict[Axis, list[tuple[ContourLimit, LineString]]] = {u: [], v: []}
        for limit in limits:
            self._classify(limit)

    def __bool__(self) -> bool:
        return bool(self.areas or any(self.edges.values()) or any(self.sections.values())
                    or any(self.crossings.values()))

    def _classify(self, limit: ContourLimit) -> None:
        c = limit.contour
        try:
            n = c.normal_axis
            c.check_planar()
        except LangError as error:
            raise LangError(error.message, self.path) from None
        if n == self.t:
            if c.closed:
                self.areas.append((c.name, round_offset(c.polygon(self.u, self.v), -limit.gap)))
                return
            (u0, v0), (u1, v1) = c.coords(self.u, self.v)[0], c.coords(self.u, self.v)[-1]
            du, dv = abs(u1 - u0), abs(v1 - v0)
            if abs(du - dv) < 1e-6:
                raise LangError(f"contour {c.name!r}: its chord runs diagonally, so the axis it limits "
                                "is unclear.", self.path)
            a, b = (self.u, self.v) if du < dv else (self.v, self.u)
            self._one_way(c, b, "along its chord")
            self._no_spike(c)
            self.edges[a].append(_OpenEdge(limit, a, b, self.path))
            return
        s: Axis = next(x for x in AXES if x not in (n, self.t))
        if c.closed:
            self.sections[s].append((c.name, round_offset(c.polygon(self.t, s), -limit.gap)))
        else:
            self._one_way(c, self.t, "through the board's thickness")
            self._no_spike(c)
            self.crossings[s].append((limit, LineString(c.coords(self.t, s))))

    def _one_way(self, c: Contour, along: Axis, way: str) -> None:
        """An open contour must run one way along `along`: no point of it
        more than `_BACK` behind the furthest it has reached, run from its
        first point toward its last. One that runs back along itself, an
        overhang, leaves the board no clear side: it is refused [decided by
        Florian, 2026-10-14]."""
        back = _runs_back([p[AXES.index(along)] for p in c.points])
        if back > _BACK:
            raise LangError(f"contour {c.name!r} runs back along {along} by {back:g} mm, an overhang; an open "
                            f"contour must run one way {way}: draw a lip as a closed contour.", self.path)

    def _no_spike(self, c: Contour) -> None:
        """An open contour must not run straight back over itself, in any
        direction, for more than `_BACK`: such a spike encloses nothing the
        board could keep clear of, so it is refused, as a line drawn twice
        is in a closed sketch [decided by Florian, 2026-10-14; the board kept
        its clearance from the rest of the contour and crossed the spike]."""
        length, at = _spike(c.points)
        if length > _BACK:
            where = ", ".join(f"{v:g}" for v in at)
            raise LangError(f"contour {c.name!r} runs straight back over itself for {length:g} mm, a spike at "
                            f"({where}); draw an open contour once along its way.", self.path)

    # -- per axis -----------------------------------------------------------------

    def edges_on(self, axis: Axis) -> list[_OpenEdge]:
        return self.edges[axis]

    def ends(self, axis: Axis, reference: float | None, explicit: bool) -> list[End]:
        """The board's ends on `axis` from open contours in perpendicular
        planes. The board lies on the side of `reference`: its other limit
        on the axis (`explicit`), else an open contour in its plane there or
        the middle of its room. It keeps the clearance over its whole
        thickness: what lies beyond the contour, grown by the clearance, is
        projected onto the axis from the band between the board's faces,
        and the board ends where that stops, on the stretch its other limit
        lies in. (The tighter of the contour's crossings at the two faces
        missed it bending toward the board between them; its offset could
        pass the other limit or the room's middle, which put the board
        across the contour, and fell short of a face the contour only just
        crossed, or not, as the contour ran [found by fuzzing, 2026-10-14].)"""
        out: list[End] = []
        for limit, line in self.crossings[axis]:
            name = limit.contour.name
            for t in (self.t_lo, self.t_hi):
                self._crossing(name, line, t)
            if reference is None:
                raise LangError(f"contour {name!r}: give another limit on {axis} so the side the board "
                                "is on is known.", self.path)
            reach = abs(limit.gap) + 1.0
            lo, hi = min(line.bounds[1], reference) - reach, max(line.bounds[3], reference) + reach
            band = shapely_box(self.t_lo, lo, self.t_hi, hi)
            within = [float(c[1]) for part in parts_of(line.intersection(band))
                      for c in cast(Sequence[Sequence[float]], getattr(part, "coords", []))]
            side = 1 if reference > max(within) else -1 if reference < min(within) else 0
            if side == 0:
                raise LangError(f"contour {name!r} crosses the board between its other limits on {axis}.",
                                self.path)
            beyond = _beyond([(float(t), float(s)) for t, s in line.coords], side, limit.gap)
            free = _free(band.intersection(beyond), lo, hi)
            if explicit:
                free = [p for p in free if p[0] - 1e-9 <= reference <= p[1] + 1e-9]
            if not free:
                what = "past the board's other limit" if explicit else "over all of the board's room"
                raise LangError(f"contour {name!r}: its clearance reaches {what} on {axis}.", self.path)
            out.append(End(min(p[0] for p in free) if side > 0 else max(p[1] for p in free), side, name))
        return out

    def _crossing(self, name: str, line: LineString, t: float) -> float:
        values = _crossings(line, t)
        if len(values) != 1:
            what = "does not reach" if not values else f"crosses {len(values)} times"
            raise LangError(f"contour {name!r} {what} the board's face at {self.t}={t:g}; "
                            "an open contour must cross each face once.", self.path)
        return values[0]

    def stretch(self, axis: Axis, values: Sequence[float], centre: float | None) -> tuple[float, float] | None:
        """The stretch on `axis` that closed contours leave: the bounds of
        those in the board's plane, and where those in perpendicular planes
        hold the board over its whole thickness (`_fits`). Where that
        falls into several stretches, the board's limits on the axis pick
        one: a single limit the stretch it lies in, two limits the one
        stretch between them (more is an error: the contour would cut the
        board in two), no limit the one around the room's `centre`."""
        lo, hi = float("-inf"), float("inf")
        found = False
        for name, area in self.areas:
            b = area.bounds
            if area.is_empty:
                raise LangError(f"contour {name!r} leaves nothing of the board.", self.path)
            i = 0 if axis == self.u else 1
            lo, hi = max(lo, b[i]), min(hi, b[i + 2])
            found = True
        for name, area in self.sections[axis]:
            pieces = self._fits(area)
            if not pieces:
                raise LangError(f"the board lies outside contour {name!r} (between {self.t}="
                                f"{self.t_lo:g} and {self.t_hi:g}).", self.path)
            if len(pieces) > 1:
                pieces = self._pick(name, axis, pieces, values, centre)
            lo, hi = max(lo, pieces[0][0]), min(hi, pieces[0][1])
            found = True
        if not found:
            return None
        if hi <= lo:
            raise LangError(f"the contours leave no room on {axis}.", self.path)
        return lo, hi

    def _pick(self, name: str, axis: Axis, pieces: list[tuple[float, float]], values: Sequence[float],
              centre: float | None) -> list[tuple[float, float]]:
        stretches = ", ".join(f"{a:.1f} to {b:.1f}" for a, b in pieces)
        if len(values) >= 2:
            a, b = sorted(values[:2])
            chosen = [p for p in pieces if min(p[1], b) - max(p[0], a) > 1e-9]
            if len(chosen) > 1:
                raise LangError(f"contour {name!r} cuts the board into {len(chosen)} pieces on {axis} "
                                f"({stretches}); give one end to take one piece.", self.path)
        else:
            point = values[0] if values else centre
            chosen = [p for p in pieces if point is not None and p[0] - 1e-9 <= point <= p[1] + 1e-9]
        if len(chosen) != 1:
            where = "the board's limit" if values else "the middle of the board's room"
            raise LangError(f"contour {name!r} leaves several stretches on {axis} ({stretches}) and "
                            f"{where} lies in none of them; give a limit inside the one meant.", self.path)
        return chosen

    def _fits(self, area: BaseGeometry) -> list[tuple[float, float]]:
        """The stretches of the shared axis over which the board's section
        across the contour's plane, from face to face, lies inside the
        area (in (t, s)): what the pieces of that band outside the area,
        projected onto the axis, leave. (Sections at the two faces alone
        missed a notch of the contour between them, and the board ran into
        it [found by fuzzing, 2026-10-14].)"""
        if area.is_empty:
            return []
        lo, hi = area.bounds[1] - 1.0, area.bounds[3] + 1.0
        band = shapely_box(self.t_lo + _INSIDE, lo, self.t_hi - _INSIDE, hi)
        return _free(band.difference(area), lo, hi)

    # -- the outline ------------------------------------------------------------------

    def trim(self, outline: Shape) -> Shape:
        """The outline cut to the contours in the board's own plane."""
        g = outline.geometry
        for _, area in self.areas:
            g = g.intersection(area)
        for edges in self.edges.values():
            for edge in edges:
                g = g.difference(edge.removed(self.u))
        trimmed = Shape(_area(g), outline.axes)
        polygons = trimmed.polygons()
        if not polygons or trimmed.area < 1e-6:
            raise LangError("the contours leave nothing of the board.", self.path)
        if len(polygons) > 1:
            raise LangError(f"the contours split the board into {len(polygons)} pieces.", self.path)
        return trimmed

    @property
    def trims(self) -> bool:
        return bool(self.areas or any(self.edges.values()))


def _crossings(line: LineString, t: float) -> list[float]:
    """Where the line (in (t, s)) meets the line t = const, as s values; a
    stretch lying along it counts with both ends."""
    lo, hi = line.bounds[1] - _FAR, line.bounds[3] + _FAR
    hit = line.intersection(LineString([(t, lo), (t, hi)]))
    values: set[float] = set()
    for part in parts_of(hit):
        coords = cast(Sequence[Sequence[float]], getattr(part, "coords", []))
        values.update(round(float(c[1]), 9) for c in coords)
    return sorted(values)


def _spike(points: Sequence[Point3]) -> tuple[float, Point3]:
    """The longest stretch a polyline runs straight back over itself, and
    where it turns: at each vertex where it reverses (within 1e-3 rad), the
    shorter of the straight runs into and out of it; 0 where it never turns
    straight back."""
    pts = [p for i, p in enumerate(points) if i == 0 or math.dist(p, points[i - 1]) > 1e-9]
    steps = [tuple(q - p for p, q in zip(a, b)) for a, b in zip(pts, pts[1:])]
    units = [tuple(x / math.hypot(*d) for x in d) for d in steps]
    lengths = [math.hypot(*d) for d in steps]

    def along(k: int, way: int) -> float:
        """The straight run of steps from step k on, going `way` (-1 back)."""
        run, j = 0.0, k
        while 0 <= j < len(units) and sum(x * y for x, y in zip(units[j], units[k])) > math.cos(1e-3):
            run, j = run + lengths[j], j + way
        return run

    best: tuple[float, Point3] = (0.0, pts[0])
    for k in range(len(units) - 1):
        if sum(x * y for x, y in zip(units[k], units[k + 1])) < -math.cos(1e-3):
            best = max(best, (min(along(k, -1), along(k + 1, 1)), pts[k + 1]))
    return best


def _runs_back(values: Sequence[float]) -> float:
    """How far a run of coordinates goes back behind the furthest it has
    reached, run from its first toward its last (0 when it runs one way)."""
    sign = 1.0 if values[-1] >= values[0] else -1.0
    furthest, back = -math.inf, 0.0
    for v in values:
        furthest = max(furthest, sign * v)
        back = max(back, furthest - sign * v)
    return back


def _free(blocked: BaseGeometry, lo: float, hi: float) -> list[tuple[float, float]]:
    """What is left of `lo` to `hi` on the second axis when each piece of
    `blocked` (in (t, s)) is projected onto it."""
    taken = sorted((float(p.bounds[1]), float(p.bounds[3])) for p in polygons_of(blocked))
    out: list[tuple[float, float]] = []
    here = lo
    for b0, b1 in taken:
        if b0 > here:
            out.append((here, b0))
        here = max(here, b1)
    if hi > here:
        out.append((here, hi))
    return [p for p in out if p[1] - p[0] > 1e-9]


def footprint(box: Box, outline: Shape | None, t: Axis, n: Axis) -> BaseGeometry:
    """A part's shadow on a plane perpendicular to `n`, in the plane's two
    axes in x, y, z order: the outline when the part lies in that plane,
    else its box."""
    others: list[Axis] = [x for x in AXES if x != n]
    a, b = others
    if outline is not None and t == n:
        return outline.geometry
    return shapely_box(box.lo[a], box.lo[b], box.hi[a], box.hi[b])
