"""Where a tabbed part's tabs go on its outer contour (`proposals/cam.md`,
Holding, Proposed 2: the rules Florian called good), Fusion-free.

The sites are Auto Setup's (`lib/auto_setup/tabs.py`), on the contour as
lines and arcs (`lang.emit.arcs.fit`): straight stretches and wide arcs, a
tab width from a convex corner and three from a concave one (a tab jammed
into an inside corner is hard to trim), none on an arc tighter than
`MIN_ARC_RADIUS` while the contour has anything else, sampled every
`SPACING` with the middle of a short stretch; on a contour with no such
stretch, the middle of its longest curve.

Of those the plan takes the ones it may: none under a chamfer or where a
pocket thins the part nearby, none whose neighbour across the kerf is
nothing (the blank's edge, a cut through). Each has a weight: an edge the
layout knows is hidden (against another board, a lip, in a groove) is
preferred to a plain one, a neighbour already cut free (released before
this part) is worth little. The tabs are then spread about the part: the
first where weight times the distance from the centroid is largest, each
next where weight times the distance to the tabs placed is, at least
`SEPARATION` tab widths apart, since two tabs are a hinge line. As many as
`tab_count` gives for the contour's length, at least the least count.
"""
from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from shapely.geometry import LineString, Point

from ..emit.arcs import Arc2, Circle2, Curve2, Line2, fit

Point2 = tuple[float, float]

#: Tab density (mm): one tab per 50 on a 200 mm contour, widening linearly
#: to one per 300 on a 3000 mm one, clamped outside (Auto Setup's).
DENSITY_SHORT = (200.0, 50.0)
DENSITY_LONG = (3000.0, 300.0)
#: Corner clearances, in tab widths.
CONVEX_MARGIN = 1.0
CONCAVE_MARGIN = 3.0
#: The least distance between two tabs, in tab widths.
SEPARATION = 2.0
#: A junction turning less than this (sine) is smooth, no corner.
SMOOTH_SIN = 0.09
#: Arcs tighter than this (mm) take no tabs while the contour offers more.
MIN_ARC_RADIUS = 40.0
#: Sites are this far apart along a stretch (mm).
SPACING = 25.0
#: Weights: a hidden edge, a plain one, a neighbour already cut free.
HIDDEN = 1.0
PLAIN = 0.6
LOOSE = 0.3


def tab_count(perimeter: float, least: int) -> int:
    """Tabs for a contour this long: Auto Setup's density, at least `least`."""
    (l0, s0), (l1, s1) = DENSITY_SHORT, DENSITY_LONG
    if perimeter <= l0:
        spacing = s0
    elif perimeter >= l1:
        spacing = s1
    else:
        spacing = s0 + (perimeter - l0) / (l1 - l0) * (s1 - s0)
    return max(least, round(perimeter / spacing))


@dataclass(frozen=True)
class _Curve:
    curve: Curve2
    length: float
    start: float


def _sweep(c: Arc2) -> float:
    """The arc's angle, from `a` through `mid` to `b`."""
    def ang(p: Point2) -> float:
        return math.atan2(p[1] - c.center[1], p[0] - c.center[0])
    a, m, b = ang(c.a), ang(c.mid), ang(c.b)
    ccw = _ccw(c)
    first = (m - a) % (2 * math.pi) if ccw else (a - m) % (2 * math.pi)
    second = (b - m) % (2 * math.pi) if ccw else (m - b) % (2 * math.pi)
    return first + second


def _ccw(c: Arc2) -> bool:
    return (c.a[0] - c.center[0]) * (c.mid[1] - c.center[1]) - (c.a[1] - c.center[1]) * (c.mid[0] - c.center[0]) > 0


def _length(c: Curve2) -> float:
    if isinstance(c, Line2):
        return math.dist(c.a, c.b)
    if isinstance(c, Arc2):
        return c.radius * _sweep(c)
    return 2 * math.pi * c.radius


def _at(c: Curve2, s: float) -> Point2:
    """The point `s` along a curve from its start."""
    if isinstance(c, Line2):
        n = math.dist(c.a, c.b)
        f = s / n if n > 0 else 0.0
        return (c.a[0] + (c.b[0] - c.a[0]) * f, c.a[1] + (c.b[1] - c.a[1]) * f)
    if isinstance(c, Arc2):
        a0 = math.atan2(c.a[1] - c.center[1], c.a[0] - c.center[0])
        a = a0 + (s / c.radius if _ccw(c) else -s / c.radius)
    else:
        a = s / c.radius
    return (c.center[0] + c.radius * math.cos(a), c.center[1] + c.radius * math.sin(a))


def _dir(c: Curve2, at_end: bool) -> Point2:
    if isinstance(c, Line2):
        n = math.dist(c.a, c.b)
        return ((c.b[0] - c.a[0]) / n, (c.b[1] - c.a[1]) / n) if n > 0 else (0.0, 0.0)
    if isinstance(c, Arc2):
        p = c.b if at_end else c.a
        rx, ry = p[0] - c.center[0], p[1] - c.center[1]
        n = math.hypot(rx, ry)
        return (-ry / n, rx / n) if _ccw(c) else (ry / n, -rx / n)
    return (0.0, 0.0)


class Contour:
    """A closed contour as lines and arcs, the part on its left."""

    def __init__(self, ring: Sequence[Sequence[float]]):
        curves = fit(ring)
        self.curves: list[_Curve] = []
        s = 0.0
        for c in curves:
            n = _length(c)
            self.curves.append(_Curve(c, n, s))
            s += n
        self.perimeter = s

    def point(self, s: float) -> Point2:
        s %= self.perimeter
        for c in self.curves:
            if s <= c.start + c.length or c is self.curves[-1]:
                return _at(c.curve, min(max(s - c.start, 0.0), c.length))
        raise AssertionError

    def concave(self, k: int) -> bool:
        """Whether the corner at the start of curve `k` is concave (an inside
        corner of the part)."""
        before, after = self.curves[k - 1].curve, self.curves[k].curve
        t1, t2 = _dir(before, True), _dir(after, False)
        cross = t1[0] * t2[1] - t1[1] * t2[0]
        return cross < -SMOOTH_SIN

    def sites(self, width: float) -> list[tuple[float, Point2]]:
        """The tab sites (see the module's doc), each with how far along the
        contour it lies."""
        intervals: list[tuple[float, float]] = []
        tight: list[tuple[float, float]] = []
        n = len(self.curves)
        if n == 1 and isinstance(self.curves[0].curve, Circle2):
            intervals = [(0.0, self.perimeter)]
        else:
            margins = [width * (CONCAVE_MARGIN if self.concave(k) else CONVEX_MARGIN) for k in range(n)]
            for k, c in enumerate(self.curves):
                start, end = c.start + margins[k], c.start + c.length - margins[(k + 1) % n]
                if end > start:
                    intervals.append((start, end))
        for c in self.curves:
            if isinstance(c.curve, (Arc2, Circle2)) and c.curve.radius < MIN_ARC_RADIUS:
                tight.append((c.start, c.start + c.length))
        kept = _minus(intervals, tight) or intervals
        out: list[tuple[float, Point2]] = []
        for start, end in kept:
            count = max(1, round((end - start) / SPACING))
            for k in range(count):
                s = start + (k + 0.5) * (end - start) / count
                out.append((s, self.point(s)))
        if not out and self.curves:
            longest = max(self.curves, key=lambda c: c.length)
            s = longest.start + longest.length / 2
            out.append((s, self.point(s)))
        return out


def _minus(intervals: list[tuple[float, float]], spans: list[tuple[float, float]]) -> list[tuple[float, float]]:
    for s0, s1 in spans:
        left: list[tuple[float, float]] = []
        for a, b in intervals:
            if s1 <= a or s0 >= b:
                left.append((a, b))
                continue
            if a < s0:
                left.append((a, s0))
            if s1 < b:
                left.append((s1, b))
        intervals = left
    return intervals


def choose(sites: Sequence[tuple[Point2, float]], centroid: Point2, count: int, separation: float) -> list[Point2]:
    """Up to `count` of the weighted sites, spread (see the module's doc)."""
    chosen: list[Point2] = []
    left = [(p, w) for p, w in sites if w > 0]
    while left and len(chosen) < count:
        def score(entry: tuple[Point2, float]) -> float:
            p, w = entry
            if not chosen:
                return w * math.dist(p, centroid)
            return w * min(math.dist(p, c) for c in chosen)
        best = max(left, key=score)
        if chosen and min(math.dist(best[0], c) for c in chosen) < separation - 1e-9:
            break
        chosen.append(best[0])
        left = [e for e in left if e is not best and min(math.dist(e[0], c) for c in chosen) >= separation - 1e-9]
    return chosen


def place(ring: Sequence[Sequence[float]], width: float, least: int, centroid: Point2,
          weight: Callable[[Point2], float]) -> tuple[list[Point2], int]:
    """The tabs on a contour: its sites weighted by `weight` (0 leaves one
    out), spread; and how many it should have had. A site on an arc is
    put onto the ring's polygon, which the emitter draws the arc through."""
    contour = Contour(ring)
    want = tab_count(contour.perimeter, least)
    line = LineString([*ring, ring[0]])

    def onto(p: Point2) -> Point2:
        q = line.interpolate(line.project(Point(p)))
        return (float(q.x), float(q.y))

    weighted = [(q, weight(q)) for q in (onto(p) for _s, p in contour.sites(width))]
    return choose(weighted, centroid, want, SEPARATION * width), want
