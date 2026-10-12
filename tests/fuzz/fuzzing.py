"""What the fuzz tests share: strategies that draw sizes and 2D shapes the
way the language makes them (rectangles, circles at the resolutions the
language uses, slots, rounded rectangles, and booleans and offsets of
them), each knowing the circles its arcs lie on, and checks of what
`lang.emit.arcs.fit` makes of their rings.

A drawn shape is a recipe (frozen dataclasses), so a failing example
prints as something that can be built again by hand."""
from __future__ import annotations

import math
from collections.abc import Callable, Generator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Literal

import numpy as np
import shapely
from hypothesis import strategies as st
from shapely import affinity
from shapely.geometry import LinearRing, MultiLineString, Point, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from lang.core import cutouts
from lang.core.geometry import polygons_of
from lang.core.scope import registry
from lang.emit.arcs import MAX_STEP, MIN_SEGMENTS, MIN_STEP, Arc2, Circle2, Curve2, Line2, fit

Point2 = tuple[float, float]
Circle = tuple[Point2, float]


@contextmanager
def fresh() -> Generator[None]:
    """A fresh build for one example: Hypothesis runs many in one test, and
    the conftest fixture resets the registry only once per test."""
    registry.reset()
    try:
        yield
    finally:
        registry.reset()


# -- numbers ------------------------------------------------------------------------------------

def floats(lo: float, hi: float) -> st.SearchStrategy[float]:
    """Floats from `lo` to `hi` as a build file could have them: none
    below 1e-9 but 0 (1e-308 is no size, and makes GEOS fail on degenerate
    shapes)."""
    def sane(x: float) -> float:
        # (1e-290 is no size either: tiny values become the bound or 0)
        return x if abs(x) >= 1e-9 else 0.0 if lo <= 0 <= hi else lo
    return st.floats(lo, hi, allow_nan=False, allow_infinity=False, allow_subnormal=False).map(sane)


def sizes(lo: float, hi: float) -> st.SearchStrategy[float]:
    """Sizes in mm as build files write them (whole and half millimetres),
    which line things up exactly, mixed with arbitrary ones."""
    whole = st.integers(math.ceil(lo), math.floor(hi)).map(float)
    half = st.integers(math.ceil(2 * lo), math.floor(2 * hi)).map(lambda n: n / 2)
    return st.one_of(whole, half, floats(lo, hi))


def shifts() -> st.SearchStrategy[Point2]:
    """Where a shape lies: near the origin, or as far away as the van's parts."""
    far = sizes(-6000, 6000)
    return st.one_of(st.just((0.0, 0.0)), st.tuples(far, far))


# -- shapes -------------------------------------------------------------------------------------

#: How a circle is made: the cutouts' exact circles (a vertex every degree),
#: `circle()` (32 segments a quarter), and shapely's 16 and 8 a quarter, the
#: coarsest the arcs are still found in (11.25 degrees a step).
CircleKind = Literal["exact", "q32", "q16", "q8"]


@dataclass(frozen=True)
class Rect:
    cx: float
    cy: float
    w: float
    h: float
    angle: float = 0.0

    def sagitta(self, grow: float) -> float:
        return 0.0

    def geometry(self) -> BaseGeometry:
        g = shapely_box(self.cx - self.w / 2, self.cy - self.h / 2, self.cx + self.w / 2, self.cy + self.h / 2)
        return affinity.rotate(g, self.angle, origin=(self.cx, self.cy)) if self.angle else g

    def circles(self) -> list[Circle]:
        return []

    def truth(self) -> BaseGeometry:
        return self.geometry()


@dataclass(frozen=True)
class Circ:
    cx: float
    cy: float
    r: float
    kind: CircleKind = "exact"

    def geometry(self) -> BaseGeometry:
        if self.kind == "exact":
            return cutouts.circle_geometry((self.cx, self.cy), self.r)
        quad = {"q32": 32, "q16": 16, "q8": 8}[self.kind]
        return Point(self.cx, self.cy).buffer(self.r, quad_segs=quad)

    def circles(self) -> list[Circle]:
        return [((self.cx, self.cy), self.r)]

    def truth(self) -> BaseGeometry:
        return Point(self.cx, self.cy).buffer(self.r, quad_segs=FINE)

    def sagitta(self, grow: float) -> float:
        step = math.radians(1.0) if self.kind == "exact" else math.pi / 2 / {"q32": 32, "q16": 16, "q8": 8}[self.kind]
        return _sagitta(self.r + abs(grow), step)


@dataclass(frozen=True)
class Slot:
    x0: float
    y0: float
    x1: float
    y1: float
    width: float
    quad: int = 8

    def geometry(self) -> BaseGeometry:
        from shapely.geometry import LineString
        return LineString([(self.x0, self.y0), (self.x1, self.y1)]).buffer(self.width / 2, quad_segs=self.quad)

    def circles(self) -> list[Circle]:
        return [((self.x0, self.y0), self.width / 2), ((self.x1, self.y1), self.width / 2)]

    def truth(self) -> BaseGeometry:
        from shapely.geometry import LineString
        return LineString([(self.x0, self.y0), (self.x1, self.y1)]).buffer(self.width / 2, quad_segs=FINE)

    def sagitta(self, grow: float) -> float:
        return _sagitta(self.width / 2 + abs(grow), math.pi / 2 / self.quad)


@dataclass(frozen=True)
class Rounded:
    """A rectangle with its corners rounded exactly (`Shape.rounded`)."""
    cx: float
    cy: float
    w: float
    h: float
    r: float
    angle: float = 0.0

    def geometry(self) -> BaseGeometry:
        g = Rect(self.cx, self.cy, self.w, self.h, self.angle).geometry()
        assert isinstance(g, Polygon)
        out = cutouts.filleted(g, self.r)
        assert out is not None, self
        return out

    def circles(self) -> list[Circle]:
        hw, hh = self.w / 2 - self.r, self.h / 2 - self.r
        a = math.radians(self.angle)
        out: list[Circle] = []
        for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
            x, y = sx * hw, sy * hh
            out.append(((self.cx + x * math.cos(a) - y * math.sin(a), self.cy + x * math.sin(a) + y * math.cos(a)),
                        self.r))
        return out

    def sagitta(self, grow: float) -> float:
        return _sagitta(self.r + abs(grow), math.radians(1.0))

    def truth(self) -> BaseGeometry:
        rect = Rect(self.cx, self.cy, self.w, self.h, self.angle).geometry()
        return rect.buffer(-self.r, join_style="mitre").buffer(self.r, quad_segs=FINE)


#: The true shapes are drawn with this many segments a quarter circle (0.4
#: degrees a step), for comparing with what the language's polygons stand for.
FINE = 225


def _sagitta(r: float, step: float) -> float:
    """How far a chord turning `step` lies inside the circle of radius `r`."""
    return r * (1 - math.cos(step / 2))


Primitive = Rect | Circ | Slot | Rounded
Combine = Literal["union", "difference", "intersection"]


@dataclass(frozen=True)
class Recipe:
    """A primitive, combined with others in turn, then grown by `grow`
    (`cutouts.grown`, as the cutouts offset what they keep material
    around) when given, then moved by `shift`."""
    base: Primitive
    steps: tuple[tuple[Combine, Primitive], ...] = ()
    grow: float | None = None
    shift: Point2 = (0.0, 0.0)

    def geometry(self) -> BaseGeometry:
        """The shape as the language makes it."""
        return self._made(lambda p: p.geometry(), lambda g, d: cutouts.grown(g, d))

    def truth(self) -> BaseGeometry:
        """The shape the recipe means, its arcs drawn finely: what the
        lines and arcs found in `geometry()` should draw."""
        return self._made(lambda p: p.truth(), lambda g, d: g.buffer(d, join_style="mitre", mitre_limit=100.0))

    def _made(self, make: Callable[[Primitive], BaseGeometry],
              grow: Callable[[BaseGeometry, float], BaseGeometry]) -> BaseGeometry:
        g = make(self.base)
        for how, p in self.steps:
            other = make(p)
            g = unary_union([g, other]) if how == "union" else g.difference(other) if how == "difference" \
                else g.intersection(other)
        if self.grow is not None and not g.is_empty:
            g = grow(g, self.grow)
        if self.shift != (0.0, 0.0):
            g = affinity.translate(g, *self.shift)
        return g

    @property
    def sagitta(self) -> float:
        """How far the shape's polygon may lie inside the true arcs it stands
        for: its coarsest arc's chords' sagitta, after the offset."""
        grow = self.grow or 0.0
        return max([self.base.sagitta(grow)] + [p.sagitta(grow) for _, p in self.steps])

    @property
    def slack(self) -> float:
        """How far the radius of an arc may be off its circle: an offset of a
        polygon standing for an arc, its corners mitred, lies on a circle up
        to half a percent of the offset off the true one."""
        return 0.0051 * abs(self.grow) if self.grow is not None else 0.0

    def circles(self) -> list[Circle]:
        """The circles the shape's arcs can lie on."""
        found = self.base.circles() + [c for _, p in self.steps for c in p.circles()]
        if self.grow is not None:
            d = self.grow
            found = [(c, r + s * d) for c, r in found for s in (1, -1) if r + s * d > 1e-9]
        dx, dy = self.shift
        return [((c[0] + dx, c[1] + dy), r) for c, r in found]


def _within(extent: float) -> st.SearchStrategy[float]:
    return sizes(-extent, extent)


@st.composite
def primitives(draw: st.DrawFn, extent: float = 200.0) -> Primitive:
    """A primitive centred within `extent` of the origin."""
    kind = draw(st.sampled_from(["rect", "circle", "slot", "rounded"]))
    cx, cy = draw(_within(extent)), draw(_within(extent))
    angle = draw(st.one_of(st.just(0.0), st.just(90.0), st.just(45.0), floats(0, 180)))
    if kind == "rect":
        return Rect(cx, cy, draw(sizes(1, 2 * extent)), draw(sizes(1, 2 * extent)), angle)
    if kind == "circle":
        return Circ(cx, cy, draw(sizes(0.5, extent)), draw(st.sampled_from(["exact", "q32", "q16", "q8"])))
    if kind == "slot":
        length = draw(st.one_of(st.just(0.0), sizes(0.1, extent)))      # a circle, or a slot as joints make them
        a = math.radians(angle)
        return Slot(cx, cy, cx + length * math.cos(a), cy + length * math.sin(a), draw(sizes(1, extent)),
                    draw(st.sampled_from([8, 16, 32])))
    w, h = draw(sizes(2, 2 * extent)), draw(sizes(2, 2 * extent))
    r = draw(floats(0.1, 0.49)) * min(w, h)
    return Rounded(cx, cy, w, h, r, angle)


@st.composite
def recipes(draw: st.DrawFn, grow: bool = True) -> Recipe:
    base = draw(primitives())
    combine: list[Combine] = ["union", "difference", "intersection"]
    steps = tuple(draw(st.lists(st.tuples(st.sampled_from(combine), primitives()), max_size=3)))
    grown = draw(st.one_of(st.none(), sizes(-30, 30).filter(lambda d: abs(d) > 1e-6))) if grow else None
    return Recipe(base, steps, grown, draw(shifts()))


def rings_of(g: BaseGeometry) -> list[list[Point2]]:
    """Every ring of every polygon, as the layout writes them: no closing
    point, exteriors counter-clockwise, holes clockwise."""
    from shapely.geometry.polygon import orient
    out: list[list[Point2]] = []
    for poly in polygons_of(g):
        poly = orient(poly, 1.0)
        for ring in [poly.exterior, *poly.interiors]:
            out.append([(float(x), float(y)) for x, y in list(ring.coords)[:-1]])
    return out


# -- what `fit` makes of a ring -----------------------------------------------------------------

def arc_sweep(arc: Arc2) -> tuple[float, bool]:
    """The arc's sweep (radians, positive) and whether it turns counter-clockwise."""
    (ax, ay), (mx, my), (bx, by) = arc.a, arc.mid, arc.b
    ccw = (mx - ax) * (by - my) - (my - ay) * (bx - mx) > 0
    c = arc.center

    def angle(p: Point2) -> float:
        return math.atan2(p[1] - c[1], p[0] - c[0])

    def part(p: Point2, q: Point2) -> float:
        d = angle(q) - angle(p)
        return (d if ccw else -d) % (2 * math.pi)
    return part(arc.a, arc.mid) + part(arc.mid, arc.b), ccw


def sample(curves: Sequence[Curve2], step: float = math.radians(0.2)) -> list[Point2]:
    """The curves as a closed ring of points (no closing point), arcs and
    circles at most `step` apart."""
    out: list[Point2] = []
    for c in curves:
        if isinstance(c, Line2):
            out.append(c.a)
        elif isinstance(c, Circle2):
            n = max(16, math.ceil(2 * math.pi / step))
            out += [(c.center[0] + c.radius * math.cos(2 * math.pi * i / n),
                     c.center[1] + c.radius * math.sin(2 * math.pi * i / n)) for i in range(n)]
        else:
            sweep, ccw = arc_sweep(c)
            n = max(2, math.ceil(sweep / step))
            a0 = math.atan2(c.a[1] - c.center[1], c.a[0] - c.center[0])
            s = 1.0 if ccw else -1.0
            out.append(c.a)
            out += [(c.center[0] + c.radius * math.cos(a0 + s * sweep * i / n),
                     c.center[1] + c.radius * math.sin(a0 + s * sweep * i / n)) for i in range(1, n)]
    return out


def ends(c: Curve2) -> tuple[Point2, Point2] | None:
    return None if isinstance(c, Circle2) else (c.a, c.b)


def on_known(center: Point2, radius: float, circles: Sequence[Circle], tol: float = 1e-6, slack: float = 0.0) -> bool:
    """Whether the circle is one of `circles`; its radius within `slack`, its
    centre within a hundredth of that (two circles of a short coarse slot,
    offset, blur into one)."""
    return any(math.dist(center, c) <= tol + 0.01 * slack and abs(radius - r) <= tol + slack for c, r in circles)


def fit_problems(ring: Sequence[Point2], circles: Sequence[Circle] | None, slack: float = 0.0) -> list[str]:
    """What is wrong with `fit(ring)`: curves that do not join up, arcs on
    circles the shape has none of (radii within `slack`: an offset of a
    coarse polygon's arc lies on a circle up to half a percent of the
    offset smaller or larger), a drawn ring that crosses itself, runs of
    vertices on a circle drawn as a fan of lines. Without `circles` (a
    layout's rings, whose circles are not known), only whether the curves
    join up and the drawn ring does not cross itself.
    Lines shorter than a micrometre are fine: the emitter leaves them out."""
    problems: list[str] = []
    curves = fit(ring)
    if not curves:
        return ["fit returned nothing"]
    if any(isinstance(c, Circle2) for c in curves) and len(curves) > 1:
        problems.append("a full circle among other curves")
    for k, c in enumerate(curves):
        e, f = ends(c), ends(curves[(k + 1) % len(curves)])
        if e is not None and f is not None and e[1] != f[0]:
            problems.append(f"curve {k} ends at {e[1]}, the next starts at {f[0]}")
        if circles is not None and isinstance(c, (Arc2, Circle2)) and not on_known(c.center, c.radius, circles,
                                                                                    1e-6, slack):
            problems.append(f"curve {k} is an arc about {c.center} with radius {c.radius}, on none of the "
                            "shape's circles")
    drawn = sample(curves)
    if len(drawn) >= 3:
        drawn_ring = LinearRing(drawn)
        if not drawn_ring.is_simple and not degenerate(ring):
            problems.append("the drawn ring crosses itself")
    if circles is not None:
        problems += missed_arcs(ring, curves, circles)
    return problems


def degenerate(ring: Sequence[Point2]) -> bool:
    """Whether the ring passes a point twice, give or take a micrometre,
    turns back on itself, or is a sliver: a hairline spike a boolean left
    (a circle added and taken away again), which no drawing of it can keep
    apart. Open (2026-10-12): whether the
    language should refuse, clean or keep such geometry."""
    seen: set[tuple[int, int]] = set()
    for x, y in ring:
        key = (round(x * 1e6), round(y * 1e6))
        if key in seen:
            return True
        seen.add(key)
    # a sliver: two polygons of one circle, made at different resolutions,
    # leave crescents a few micrometres wide that are nothing on the true
    # circle (average width = 2 area / perimeter)
    if len(ring) >= 3:
        outline = LinearRing(ring)
        if 2 * abs(Polygon(ring).area) < 0.02 * outline.length:
            return True
    # a spike: the ring turns back on itself at a vertex
    n = len(ring)
    for k in range(n):
        a, p, b = ring[k - 1], ring[k], ring[(k + 1) % n]
        ax, ay, bx, by = p[0] - a[0], p[1] - a[1], b[0] - p[0], b[1] - p[1]
        if abs(math.atan2(ax * by - ay * bx, ax * bx + ay * by)) > math.radians(178):
            return True
    return False


def _covered(p: Point2, center: Point2, radius: float, curves: Sequence[Curve2]) -> bool:
    for c in curves:
        if not isinstance(c, (Arc2, Circle2)) or math.dist(c.center, center) > 1e-6 or abs(c.radius - radius) > 1e-6:
            continue
        if isinstance(c, Circle2):
            return True
        sweep, ccw = arc_sweep(c)
        d = math.atan2(p[1] - center[1], p[0] - center[0]) - math.atan2(c.a[1] - center[1], c.a[0] - center[0])
        if (d if ccw else -d) % (2 * math.pi) <= sweep + 1e-9:
            return True
    return False


def missed_arcs(ring: Sequence[Point2], curves: Sequence[Curve2], circles: Sequence[Circle]) -> list[str]:
    """Runs of the ring's vertices on one of the shape's circles, long
    enough to be an arc even after a boolean cut its ends, whose middle
    vertex no arc of that circle covers: drawn as a fan of flat faces."""
    n = len(ring)
    problems: list[str] = []
    for center, radius in circles:
        on = [abs(math.dist(p, center) - radius) <= 1e-9 for p in ring]
        if all(on) or not any(on):
            whole = all(on) and n >= MIN_SEGMENTS + 3 and _regular([*ring, ring[0]], center)
            if whole and not _covered(ring[0], center, radius, curves):
                problems.append(f"the ring is the circle about {center} r {radius}, drawn as lines")
            continue
        start = next(i for i in range(n) if not on[i])
        run: list[Point2] = []
        for k in range(1, n + 1):
            i = (start + k) % n
            if on[i]:
                run.append(ring[i])
                continue
            if len(run) >= MIN_SEGMENTS + 3 and _regular(run, center):
                mid = run[len(run) // 2]
                if not _covered(mid, center, radius, curves):
                    problems.append(f"{len(run)} vertices on the circle about {center} r {radius} not drawn "
                                    f"as an arc (around {mid})")
            run = []
    return problems


def _regular(run: Sequence[Point2], center: Point2) -> bool:
    """Whether the run turns one way about `center` in steps an arc has."""
    steps = []
    for p, q in zip(run, run[1:]):
        a = math.atan2(p[1] - center[1], p[0] - center[0])
        b = math.atan2(q[1] - center[1], q[0] - center[0])
        steps.append(math.remainder(b - a, 2 * math.pi))
    return all(MIN_STEP <= abs(s) <= MAX_STEP for s in steps) and (all(s > 0 for s in steps)
                                                                     or all(s < 0 for s in steps))


def recipe_problems(recipe: Recipe) -> list[str]:
    """What is wrong with what `fit` makes of the rings of the recipe's
    shape: each ring's problems (`fit_problems`), and drawn rings that lie
    farther from the true shape than its coarsest arcs' polygons do,
    magnified where two arcs cross at a shallow angle (10 degrees at the
    least, `arcs._GLANCING`): their crossing then lies up to 1 / sin(10)
    times as far from where their polygons cross.

    Shapes offset by `grow` are not compared with the true shape: where an
    arc meets a line or arc at a corner the offset extends, `grown` mitres
    the tangents and `fit` meets the offset circles, which differ (up to a
    millimetre for a lens grown by 26). Fusion's sketch offset meets the
    offset circles, as `fit` does (checked in Fusion 2026-10-12); `grown`
    is to follow, and then this comparison can include them."""
    circles, slack = recipe.circles(), recipe.slack
    rings = rings_of(recipe.geometry())
    problems = [p for ring in rings for p in fit_problems(ring, circles, slack)]
    if recipe.grow is not None:
        return problems
    truth = recipe.truth()
    true_rings = rings_of(truth)
    if len(true_rings) != len(rings) or any(degenerate(r) for r in rings + true_rings):
        # Shapes that touch (a circle in a square that holds it exactly) or
        # coincide (a circle taken away again at another resolution) part
        # differently as polygons and as true curves: nothing to compare,
        # and the slivers and horns they leave are nothing on the true
        # curves, so drawn on them they touch themselves (open, see
        # `degenerate`).
        return [p for p in problems if p != "the drawn ring crosses itself"]
    drawn = [sample(fit(ring), math.radians(0.5)) for ring in rings]
    if not rings or truth.is_empty:
        if rings and sum(abs(Polygon(r).area) for r in rings) > 1e-3:
            problems.append("the true shape is empty, the shape is not")
        return problems
    largest = max([r for _, r in circles], default=0.0)
    # (twice that: below 10 degrees `fit` leaves the vertex where the
    # polygons cross, which may lie a little farther off)
    bound = 2 * (2 * recipe.sagitta + _sagitta(largest, math.pi / 2 / FINE)) / math.sin(math.radians(10)) + 1e-6
    off = max(_farthest([p for d in drawn for p in d], truth.boundary),
              _farthest([p for r in rings_of(truth) for p in r], MultiLineString([LinearRing(d) for d in drawn
                                                                                   if len(d) >= 3])))
    if off > bound:
        problems.append(f"the drawn rings lie {off:.3g} off the true shape (at most {bound:.3g})")
    return problems


def _farthest(points: Sequence[Point2], geometry: BaseGeometry) -> float:
    """The largest distance of the points from `geometry`."""
    if not points or geometry.is_empty:
        return 0.0
    shapely.prepare(geometry)
    return float(np.max(shapely.distance(shapely.points(np.array(points)), geometry)))


# -- polygons of lines, and corners rounded or cut off without the language -------------------------

@dataclass(frozen=True)
class Star:
    """A polygon around (cx, cy), its vertices at the angles given (degrees,
    rising) and distances: corners of every sharpness, convex and concave."""
    cx: float
    cy: float
    vertices: tuple[tuple[float, float], ...]

    def geometry(self) -> BaseGeometry:
        """The polygon, or nothing when its gaps of more than 180 degrees make
        it cross itself."""
        g = Polygon([(self.cx + d * math.cos(math.radians(a)), self.cy + d * math.sin(math.radians(a)))
                     for a, d in self.vertices])
        return g if g.is_valid else Polygon()


@dataclass(frozen=True)
class Lines:
    """A polygon of lines only: rectangles united and subtracted, or a star,
    its largest piece."""
    base: Rect | Star
    steps: tuple[tuple[Combine, Rect], ...] = ()
    shift: Point2 = (0.0, 0.0)

    def polygon(self) -> Polygon | None:
        g = self.base.geometry()
        for how, p in self.steps:
            other = p.geometry()
            g = unary_union([g, other]) if how == "union" else g.difference(other)
        pieces = [p for p in polygons_of(g) if p.is_valid and p.area > 1.0]
        if not pieces:
            return None
        out = max(pieces, key=lambda p: p.area)
        return affinity.translate(out, *self.shift) if self.shift != (0.0, 0.0) else out


@st.composite
def stars(draw: st.DrawFn) -> Star:
    n = draw(st.integers(3, 10))
    angles = sorted(set(draw(st.lists(floats(0, 359.9), min_size=n, max_size=n))))
    if len(angles) < 3:
        angles = [0.0, 120.0, 240.0]
    return Star(draw(_within(100)), draw(_within(100)),
                tuple((a, draw(sizes(5, 200))) for a in angles))


@st.composite
def line_polygons(draw: st.DrawFn) -> Lines:
    angle = st.one_of(st.just(0.0), st.just(45.0), floats(0, 90))
    rects = st.builds(Rect, _within(100), _within(100), sizes(2, 300), sizes(2, 300), angle)
    base: Rect | Star = draw(st.one_of(rects, stars()))
    combine: list[Combine] = ["union", "difference"]
    steps = tuple(draw(st.lists(st.tuples(st.sampled_from(combine), rects), max_size=3)))
    return Lines(base, steps, draw(shifts()))


def _corners_of(ring: Sequence[Point2]) -> list[tuple[Point2, Point2, Point2, float]]:
    """Per vertex: the vertex, the unit directions in and out, and the turn
    (radians, positive to the left)."""
    n = len(ring)
    out: list[tuple[Point2, Point2, Point2, float]] = []
    for k in range(n):
        a, p, b = ring[k - 1], ring[k], ring[(k + 1) % n]
        li, lo = math.dist(a, p), math.dist(p, b)
        din = ((p[0] - a[0]) / li, (p[1] - a[1]) / li)
        dout = ((b[0] - p[0]) / lo, (b[1] - p[1]) / lo)
        turn = math.atan2(din[0] * dout[1] - din[1] * dout[0], din[0] * dout[0] + din[1] * dout[1])
        out.append((p, din, dout, turn))
    return out


#: Corners turning less than this are joints, not corners (`cutouts._MIN_CORNER`).
MIN_CORNER = math.radians(2.0)


def _changed_ring(ring: Sequence[Point2], cut: Callable[[float], float],
                  between: Callable[[Point2, Point2, Point2, float, float], list[Point2]]) -> list[Point2] | None:
    """The ring with each corner replaced: `cut(turn)` is how far along both
    edges the corner's change reaches, `between(p, din, dout, turn, reach)`
    the points that replace it. None when an edge is too short."""
    corners = _corners_of(ring)
    reach = [cut(t) if abs(t) >= MIN_CORNER else 0.0 for _, _, _, t in corners]
    n = len(ring)
    for k in range(n):
        if reach[k] + reach[(k + 1) % n] > math.dist(ring[k], ring[(k + 1) % n]) + 1e-7:
            return None
    out: list[Point2] = []
    for (p, din, dout, t), d in zip(corners, reach):
        out += between(p, din, dout, t, d) if d > 0 else [p]
    return out


def reference_fillet(poly: Polygon, r: float) -> Polygon | None:
    """`poly` (lines only) with every corner rounded with `r`, worked out
    from the tangent lengths r tan(turn / 2); None when an edge is too
    short for its two arcs or the arcs run into each other."""
    def between(p: Point2, din: Point2, dout: Point2, t: float, d: float) -> list[Point2]:
        a = (p[0] - din[0] * d, p[1] - din[1] * d)
        b = (p[0] + dout[0] * d, p[1] + dout[1] * d)
        s = 1.0 if t > 0 else -1.0
        c = (a[0] - din[1] * r * s, a[1] + din[0] * r * s)
        return cutouts._arc_points(c, r, a, b, t > 0)  # pyright: ignore[reportPrivateUsage]
    return _reference(poly, lambda t: r * math.tan(abs(t) / 2), between)


def reference_chamfer(poly: Polygon, size: float) -> Polygon | None:
    """`poly` (lines only) with every corner cut off `size` along both edges."""
    def between(p: Point2, din: Point2, dout: Point2, t: float, d: float) -> list[Point2]:
        return [(p[0] - din[0] * d, p[1] - din[1] * d), (p[0] + dout[0] * d, p[1] + dout[1] * d)]
    return _reference(poly, lambda t: size, between)


def _reference(poly: Polygon, cut: Callable[[float], float],
               between: Callable[[Point2, Point2, Point2, float, float], list[Point2]]) -> Polygon | None:
    from shapely.geometry.polygon import orient
    poly = orient(poly, 1.0)
    rings: list[list[Point2]] = []
    for ring in [poly.exterior, *poly.interiors]:
        pts: list[Point2] = []
        for x, y in list(ring.coords)[:-1]:
            if not pts or math.dist(pts[-1], (x, y)) > 1e-9:
                pts.append((float(x), float(y)))
        if len(pts) > 1 and math.dist(pts[0], pts[-1]) <= 1e-9:
            pts.pop()
        changed = _changed_ring(pts, cut, between)
        if changed is None:
            return None
        rings.append(changed)
    out = Polygon(rings[0], rings[1:])
    return out if out.is_valid else None


def offset_problems(recipe: Recipe) -> list[str]:
    """What is wrong with `cutouts.grown` of the recipe's shape before its
    offset (the offset itself is `recipe.grow`): pieces that are invalid,
    an outward offset that does not hold the shape grown with round corners
    or reaches past the one grown with mitred corners, an inward one that
    reaches past the round one (each give or take the polygon's sagitta,
    as its arcs go onto their true circles)."""
    d = recipe.grow
    if d is None:
        return []
    shape = Recipe(recipe.base, recipe.steps).geometry()
    if shape.is_empty:
        return []
    got = cutouts.grown(shape, d)
    problems: list[str] = []
    if not got.is_valid:
        problems.append("the offset is not a valid shape")
        return problems
    slack = 2.5 * recipe.sagitta + 1e-6
    small, large = (shape.buffer(d - slack * (1 if d > 0 else -1), quad_segs=64),
                    shape.buffer(d + slack, join_style="mitre", mitre_limit=100.0))
    tol = 1e-6 * max(1.0, shape.length)
    if d > 0:
        if small.difference(got).area > tol:
            problems.append(f"the offset misses {small.difference(got).area:.3g} mm2 of the round offset")
        if got.difference(large).area > tol:
            problems.append(f"the offset reaches {got.difference(large).area:.3g} mm2 past the mitred offset")
    elif got.difference(shape.buffer(d + slack, quad_segs=64)).area > tol:
        problems.append(f"the inset reaches {got.difference(shape.buffer(d + slack, quad_segs=64)).area:.3g} mm2 "
                        "past the round inset")
    return problems
