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
- In a perpendicular plane, it is sectioned at both big faces of the board
  and the tighter result wins, so the board fits over its whole
  thickness. A closed contour gives a stretch on the axis the two planes
  share, `batten.between(top, profile, floor_outline)`; an open one a
  position on it.

`contour.gap(n)` keeps n mm of clearance, measured in the contour's
plane; `contour.into(n)` reaches n mm past it. All of it is polyline math
with shapely; nothing is projected in Fusion.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import cast

from shapely import make_valid
from shapely.geometry import LineString, MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from .box import Box
from .directions import AXES, Axis
from .errors import LangError
from .shapes import Shape

Point3 = tuple[float, float, float]
Point2 = tuple[float, float]
#: How far an open contour is extended past its ends, and how far its
#: removed side reaches (mm).
_FAR = 1e5
#: A contour is planar when its points lie this close to its plane (mm).
_PLANAR = 0.01
#: Faces are sectioned this far inside the board, so that a contour edge
#: lying exactly in a face does not count as crossing it.
_INSIDE = 1e-6


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


def as_contour_limit(limit: Contour | ContourLimit) -> ContourLimit:
    return limit if isinstance(limit, ContourLimit) else ContourLimit(limit)


def _area(g: BaseGeometry) -> BaseGeometry:
    """The polygonal part of a geometry (make_valid may add lines)."""
    if isinstance(g, (Polygon, MultiPolygon)):
        return g
    parts = [p for p in getattr(g, "geoms", []) if isinstance(p, (Polygon, MultiPolygon))]
    return unary_union(parts) if parts else Polygon()


def _offset(area: BaseGeometry, distance: float) -> BaseGeometry:
    """Grown (positive) or shrunk; round joins keep the clearance exact."""
    return area.buffer(distance) if distance else area


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
        # Run along b in increasing order, then extend both ends along b and
        # close the region on the far side.
        pts = [(b, a) for a, b in self.points_ab]
        if pts[0][0] > pts[-1][0]:
            pts.reverse()
        lo_b, hi_b = pts[0][0] - _FAR, pts[-1][0] + _FAR
        far_a = self.lo - _FAR if self.side > 0 else self.hi + _FAR
        ring = [(lo_b, pts[0][1])] + pts + [(hi_b, pts[-1][1]), (hi_b, far_a), (lo_b, far_a)]
        region = _offset(_area(make_valid(Polygon(ring))), self.limit.gap)
        # (b, a) -> (u, v)
        if self.a == u:
            return _swap(region)
        return region


def _swap(g: BaseGeometry) -> BaseGeometry:
    from shapely import affinity
    return affinity.affine_transform(g, [0, 1, 1, 0, 0, 0])


class ContourLimits:
    """The contour limits of one board, classified against its plane. The
    board asks it for values, stretches and far ends per in-plane axis, and
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
                self.areas.append((c.name, _offset(c.polygon(self.u, self.v), -limit.gap)))
                return
            (u0, v0), (u1, v1) = c.coords(self.u, self.v)[0], c.coords(self.u, self.v)[-1]
            du, dv = abs(u1 - u0), abs(v1 - v0)
            if abs(du - dv) < 1e-6:
                raise LangError(f"contour {c.name!r}: its chord runs diagonally, so the axis it limits "
                                "is unclear.", self.path)
            a, b = (self.u, self.v) if du < dv else (self.v, self.u)
            self.edges[a].append(_OpenEdge(limit, a, b, self.path))
            return
        s: Axis = next(x for x in AXES if x not in (n, self.t))
        if c.closed:
            self.sections[s].append((c.name, _offset(c.polygon(self.t, s), -limit.gap)))
        else:
            self.crossings[s].append((limit, LineString(c.coords(self.t, s))))

    # -- per axis -----------------------------------------------------------------

    def edges_on(self, axis: Axis) -> list[_OpenEdge]:
        return self.edges[axis]

    def values(self, axis: Axis, reference: float | None) -> list[float]:
        """Positions on `axis` from open contours in perpendicular planes:
        where each crosses the two faces, the tighter of the two. The board
        lies on the side of `reference`."""
        out: list[float] = []
        for limit, line in self.crossings[axis]:
            name = limit.contour.name
            raw = [self._crossing(name, line, t) for t in (self.t_lo, self.t_hi)]
            if reference is None:
                raise LangError(f"contour {name!r}: give another limit on {axis} so the side the board "
                                "is on is known.", self.path)
            side = 1 if reference > max(raw) else -1 if reference < min(raw) else 0
            if side == 0:
                raise LangError(f"contour {name!r} crosses the board between its other limits on {axis}.",
                                self.path)
            if limit.gap:
                raw = self._offset_crossings(limit, line, raw, side)
            out.append(max(raw) if side > 0 else min(raw))
        return out

    def _offset_crossings(self, limit: ContourLimit, line: LineString, raw: list[float],
                          side: int) -> list[float]:
        """The crossings of the line offset by the clearance, measured in
        its plane: toward the board for a gap, away from it for into."""
        toward = side if limit.gap > 0 else -side
        for distance in (abs(limit.gap), -abs(limit.gap)):
            moved = line.offset_curve(distance)
            if not isinstance(moved, LineString) or moved.is_empty:
                continue
            values = [_crossings(moved, t) for t in (self.t_lo, self.t_hi)]
            if all(len(v) == 1 for v in values) and (values[0][0] - raw[0]) * toward > 0:
                return [v[0] for v in values]
        raise LangError(f"contour {limit.contour.name!r}: the clearance moves it off the board.", self.path)

    def _crossing(self, name: str, line: LineString, t: float) -> float:
        values = _crossings(line, t)
        if len(values) != 1:
            what = "does not reach" if not values else f"crosses {len(values)} times"
            raise LangError(f"contour {name!r} {what} the board's face at {self.t}={t:g}; "
                            "an open contour must cross each face once.", self.path)
        return values[0]

    def stretch(self, axis: Axis, values: Sequence[float], centre: float | None) -> tuple[float, float] | None:
        """The stretch on `axis` that closed contours leave: the bounds of
        those in the board's plane, and the sections of those in
        perpendicular planes at both faces (tighter wins). Where a section
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
            pieces = None
            for t in (self.t_lo + _INSIDE, self.t_hi - _INSIDE):
                at_face = self._section(area, t)
                pieces = at_face if pieces is None else _intersect(pieces, at_face)
            pieces = [p for p in pieces or [] if p[1] - p[0] > 1e-9]
            if not pieces:
                raise LangError(f"the board lies outside contour {name!r} (sectioned at {self.t}="
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

    def _section(self, area: BaseGeometry, t: float) -> list[tuple[float, float]]:
        lo, hi = area.bounds[1] - 1.0, area.bounds[3] + 1.0
        hit = area.intersection(LineString([(t, lo), (t, hi)]))
        out: list[tuple[float, float]] = []
        for g in getattr(hit, "geoms", [hit]):
            if isinstance(g, LineString) and not g.is_empty:
                ys = [float(y) for _, y in g.coords]
                out.append((min(ys), max(ys)))
        return sorted(out)

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
    for part in getattr(hit, "geoms", [hit]):
        if part.is_empty:
            continue
        coords = cast(Sequence[Sequence[float]], getattr(part, "coords", []))
        values.update(round(float(c[1]), 9) for c in coords)
    return sorted(values)


def _intersect(a: list[tuple[float, float]], b: list[tuple[float, float]]) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for a0, a1 in a:
        for b0, b1 in b:
            lo, hi = max(a0, b0), min(a1, b1)
            if hi > lo:
                out.append((lo, hi))
    return out


def footprint(box: Box, outline: Shape | None, t: Axis, n: Axis) -> BaseGeometry:
    """A part's shadow on a plane perpendicular to `n`, in the plane's two
    axes in x, y, z order: the outline when the part lies in that plane,
    else its box."""
    others: list[Axis] = [x for x in AXES if x != n]
    a, b = others
    if outline is not None and t == n:
        return outline.geometry
    from shapely.geometry import box as shapely_box
    return shapely_box(box.lo[a], box.lo[b], box.hi[a], box.hi[b])
