"""Random masters and the boards their contours limit, for fuzzing contour
limits (`lang.core.contours`: `between()` given `van.contour(name)`) as
`boards.py` fuzzes the cutouts: a case is plain data, built with the
language's own calls, and checked from the outside.

A case is a room (the module's box) with a board in it, centred on its
thickness axis, and the master's contours, each a sketch as the snapshot
holds it: closed (a rectangle with notches, a star, a circle) or open (a
profile, a straight edge), its corners rounded by arcs sampled as the
snapshot writer samples them and rounded as it writes them, in the board's
own plane or in one perpendicular to it, anywhere along its normal. The
board's `between()` takes them, with `gap()`, `into()` or bare, among
positions, sides of the room and an end board. Everything is drawn in the
board's own axes (t, u, v; `room`, `at`, the contours' corners) and built
in the world by a `Variant`: those axes on any of the world's, anywhere.

`run_case` checks, from the outside:

- no other error than a LangError; a refusal is the same again and
  changes no other board;
- an accepted board lies inside what each contour allows: inside a closed
  one less its gap (or reaching `into` no further past it), on its side of
  an open one and at least the gap from it; in its own plane by its
  outline, in a perpendicular one by its section across that plane, over
  its whole thickness; and `checks.inside()` agrees for closed ones;
- it is the board worked out independently (`expected`): the other limits
  as `between()` reads them, the stretches where the board fits over its
  whole thickness found by projecting what lies outside the contour within
  the board's thickness onto the axis the planes share, an open contour's
  side as the region a large square is split into by it;
- the layout plans, draws and meshes;
- built again in another variant (other axes, another place, each contour
  reversed, started at another point, with points added along its
  segments, its plane moved along its normal, its normal turned round), it
  comes out the same in the board's frame, or is refused both times.

Two things are known and open, and marked `KNOWN` (see `_offset_noise`):
GEOS's simplification of what it offsets, and open contours that run back
along themselves.
"""
from __future__ import annotations

import math
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from hypothesis import strategies as st
from shapely import affinity, make_valid
from shapely.geometry import LineString, Point, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import split, unary_union

from boards import KNOWN, _pipeline_problems  # pyright: ignore[reportPrivateUsage]
from fuzzing import floats, fresh, sizes
from lang import Board, Box, LangError, Pos, board, inside, material, module
from lang.core.contours import Contour, round_offset
from lang.core.directions import AXES, Axis, world_frame
from lang.core.geometry import NARROWEST, clean, polygons_of
from lang.core.scope import Scope
from lang.core.snapshot_types import SNAPSHOT_VERSION, SnapshotDict
from lang.emit.snapshot_format import DECIMALS
from lang.master import Master

Point2 = tuple[float, float]
Point3 = tuple[float, float, float]
Range = tuple[float, float]

#: The snapshot writer samples curves so that no point of a curve is further
#: than this from its polyline (mm; `lang.emit.snapshot.STROKE_TOLERANCE`).
STROKE = 0.1
#: How far the reckoning extends an open contour past its ends (mm), and
#: half the side of the square it splits.
_EXTEND = 1e6
_SQUARE = 5e5
#: The board's faces are sectioned this far inside, as `contours._INSIDE`
#: does, so that a contour edge lying in a face does not count.
_INSIDE = 1e-6


# -- cases ------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class ContourSpec:
    """A sketch of the master: its corners in its plane's coordinates (the
    two of the board's axes t, u, v other than `normal`, in that order), in
    mm, each rounded with its radius (0: sharp), closed or open, in the
    plane `plane` mm along `normal` (0 t, 1 u, 2 v). A circle is its
    centre and radius."""
    closed: bool
    normal: int
    plane: float
    corners: tuple[Point2, ...]
    radii: tuple[float, ...]
    circle: bool = False


@dataclass(frozen=True)
class LimitSpec:
    """One of `between()`'s limits: a position `value` on the board's axis
    `axis` (1 u, 2 v), the room's side there (`value` 0 the low one, 1 the
    high one), an end board standing on that side, or the master's contour
    `index` with `gap` (negative: `into`; None: the bare contour)."""
    kind: Literal["pos", "side", "end", "contour"]
    axis: int = 1
    value: float = 0.0
    index: int = 0
    gap: float | None = 0.0


@dataclass(frozen=True)
class Variant:
    """How a case is built in the world: the world axis (0 x, 1 y, 2 z) of
    each of the board's axes t, u, v, the world point the board's origin
    lies at, and per contour: reversed, started `start` points on (a closed
    one), points added along every `split`-th segment (0: none), its plane
    moved `shift` along its normal, its normal turned round."""
    axes: tuple[int, int, int] = (2, 0, 1)
    origin: Point3 = (0.0, 0.0, 0.0)
    reverse: tuple[bool, ...] = ()
    start: tuple[int, ...] = ()
    split: tuple[int, ...] = ()
    shift: tuple[float, ...] = ()
    flip: tuple[bool, ...] = ()


@dataclass(frozen=True)
class ContourCase:
    """The room's extent on each of the board's axes t, u, v; the board's
    thickness `t`, centred at `at` on t; the master's contours; the
    limits, in the order `between()` is given them; an end board's
    thickness; and the two variants it is built in."""
    room: tuple[Range, Range, Range]
    t: float
    at: float
    contours: tuple[ContourSpec, ...]
    limits: tuple[LimitSpec, ...]
    end_t: float = 15.0
    base: Variant = field(default_factory=Variant)
    other: Variant = field(default_factory=Variant)


# -- sampling the sketches as the snapshot does -------------------------------------------------------

def _rounded(p: Point2) -> Point2:
    """As the snapshot writer writes a coordinate (`snapshot_format._r`)."""
    return (round(p[0], DECIMALS) + 0.0, round(p[1], DECIMALS) + 0.0)


def arc_points(centre: Point2, r: float, start: float, sweep: float) -> list[Point2]:
    """An arc sampled in equal steps whose chords stay within `STROKE` of
    it, both ends included."""
    step = 2 * math.acos(max(-1.0, 1 - STROKE / r)) if r > 0 else math.tau
    n = max(1, math.ceil(abs(sweep) / step - 1e-9))
    return [(centre[0] + r * math.cos(start + sweep * k / n), centre[1] + r * math.sin(start + sweep * k / n))
            for k in range(n + 1)]


def _fillet(prev: Point2, c: Point2, nxt: Point2, r: float) -> list[Point2]:
    """The corner `c` rounded with radius r, tangent to both edges, sampled;
    smaller where the edges are short (its tangent points no further from
    the corner than 0.45 of either edge), `[c]` where nothing turns."""
    l1, l2 = math.dist(prev, c), math.dist(c, nxt)
    if r <= 0 or l1 < 1e-9 or l2 < 1e-9:
        return [c]
    d1 = ((c[0] - prev[0]) / l1, (c[1] - prev[1]) / l1)
    d2 = ((nxt[0] - c[0]) / l2, (nxt[1] - c[1]) / l2)
    cross = d1[0] * d2[1] - d1[1] * d2[0]
    turn = math.atan2(abs(cross), d1[0] * d2[0] + d1[1] * d2[1])
    if turn < 1e-6 or turn > math.pi - 1e-3:
        return [c]
    r = min(r, 0.45 * min(l1, l2) / math.tan(turn / 2))
    reach = r * math.tan(turn / 2)
    t1 = (c[0] - d1[0] * reach, c[1] - d1[1] * reach)
    left = 1.0 if cross > 0 else -1.0
    centre = (t1[0] - d1[1] * r * left, t1[1] + d1[0] * r * left)
    start = math.atan2(t1[1] - centre[1], t1[0] - centre[0])
    return arc_points(centre, r, start, turn * left)


def polyline(spec: ContourSpec) -> list[Point2]:
    """The sketch as the snapshot holds it, in its plane's coordinates:
    its curves sampled and chained, a closed one without repeating its
    first point, every coordinate rounded as the writer rounds it."""
    if spec.circle:
        return [_rounded(p) for p in arc_points(spec.corners[0], spec.radii[0], 0.0, math.tau)[:-1]]
    corners = list(spec.corners)
    n = len(corners)
    out: list[Point2] = []
    for i, c in enumerate(corners):
        if not spec.closed and i in (0, n - 1):
            out.append(c)
        else:
            out.extend(_fillet(corners[i - 1], c, corners[(i + 1) % n], spec.radii[i]))
    return [_rounded(p) for p in out]


def _in_variant(points: list[Point2], closed: bool, variant: Variant, i: int) -> list[Point2]:
    """The points as the variant samples contour i: points added along
    every `split`-th segment, started elsewhere, reversed."""
    k = variant.split[i] if i < len(variant.split) else 0
    if k > 0:
        ring = points + points[:1] if closed else points
        more: list[Point2] = []
        for j, (p, q) in enumerate(zip(ring, ring[1:])):
            more.append(p)
            if j % k == 0:
                more += [(p[0] + f * (q[0] - p[0]), p[1] + f * (q[1] - p[1])) for f in (0.3, 0.5, 0.7)]
        points = more if closed else more + [points[-1]]
    s = variant.start[i] if i < len(variant.start) else 0
    if closed and s:
        s %= len(points)
        points = points[s:] + points[:s]
    if i < len(variant.reverse) and variant.reverse[i]:
        points = points[::-1]
    return points


def _plane_axes(normal: int) -> tuple[int, int]:
    """The board's axes a contour's plane coordinates are on."""
    a, b = [k for k in range(3) if k != normal]
    return a, b


# -- building in the world ----------------------------------------------------------------------------

@dataclass
class World:
    """A variant's map from the board's axes to the world's."""
    variant: Variant

    def axis(self, k: int) -> Axis:
        return AXES[self.variant.axes[k]]

    def at(self, k: int, value: float) -> float:
        """The world coordinate of `value` on the board's axis k."""
        return self.variant.origin[self.variant.axes[k]] + value

    def back(self, axis: Axis, value: float) -> float:
        return value - self.variant.origin[AXES.index(axis)]

    def point(self, c: Point3) -> Point3:
        w = list(self.variant.origin)
        for k in range(3):
            w[self.variant.axes[k]] += c[k]
        return (w[0], w[1], w[2])

    def box(self, extents: tuple[Range, Range, Range]) -> Box:
        lo: dict[Axis, float] = {}
        hi: dict[Axis, float] = {}
        for k in range(3):
            lo[self.axis(k)], hi[self.axis(k)] = self.at(k, extents[k][0]), self.at(k, extents[k][1])
        return Box(lo, hi)


def snapshot(case: ContourCase, variant: Variant) -> SnapshotDict:
    """The master as the variant's snapshot holds it, contour i named `c<i>`."""
    world = World(variant)
    contours: dict[str, Any] = {}
    for i, spec in enumerate(case.contours):
        shift = variant.shift[i] if i < len(variant.shift) else 0.0
        pa, pb = _plane_axes(spec.normal)
        points: list[list[float]] = []
        for p, q in _in_variant(polyline(spec), spec.closed, variant, i):
            c = [0.0, 0.0, 0.0]
            c[pa], c[pb], c[spec.normal] = p, q, spec.plane + shift
            points.append(list(world.point((c[0], c[1], c[2]))))
        o = [0.0, 0.0, 0.0]
        o[spec.normal] = spec.plane + shift
        normal = [0.0, 0.0, 0.0]
        normal[variant.axes[spec.normal]] = -1.0 if i < len(variant.flip) and variant.flip[i] else 1.0
        contours[f"c{i}"] = {"points": points, "closed": spec.closed,
                             "plane": {"origin": list(world.point((o[0], o[1], o[2]))), "normal": normal}}
    return {"version": SNAPSHOT_VERSION, "units": "mm", "source": "fuzz", "hash": "", "planes": {},
            "contours": contours, "boxes": {}, "parameters": {}, "problems": []}


@dataclass
class Built:
    """A case built in one variant: the module, the board under test, the
    end boards, the contours as `between()` got them."""
    world: World
    module: Scope
    board: Board
    ends: list[Board]
    contours: list[Contour]


def _side_name(world: World, k: int, high: bool) -> str:
    return world_frame().direction_of(world.axis(k), 1 if high else -1).name


def build(case: ContourCase, variant: Variant, name: str = "m") -> Built:
    """The case in the current build, as module `name`; nothing is resolved yet
    but the end boards."""
    world = World(variant)
    van = Master(Path("fuzz_snapshot.json"), snapshot(case, variant))
    contours = [van.contour(f"c{i}") for i in range(len(case.contours))]
    ends: list[Board] = []
    with module(name, world.box(case.room)) as m:
        limits: list[Any] = []
        for i, limit in enumerate(case.limits):
            if limit.kind == "pos":
                limits.append(Pos(world.axis(limit.axis), world.at(limit.axis, limit.value)))
            elif limit.kind == "side":
                limits.append(m.side(_side_name(world, limit.axis, limit.value > 0)))
            elif limit.kind == "end":
                end = board(f"end{i}", material("birch", t=case.end_t)).on(
                    m.side(_side_name(world, limit.axis, limit.value > 0)))
                end.box()
                ends.append(end)
                limits.append(end)
            else:
                c = contours[limit.index]
                limits.append(c if limit.gap is None else c.gap(limit.gap) if limit.gap >= 0 else c.into(-limit.gap))
        b = board("board", material("birch", t=case.t)).center(Pos(world.axis(0), world.at(0, case.at)))
        b.between(*limits)
    return Built(world, m, b, ends, contours)


@dataclass
class Outcome:
    """What a variant made of the case, in the board's frame: refused (with
    the message), or the board's box on t, u, v and its outline in (u, v)."""
    refused: str | None
    box: tuple[Range, Range, Range] | None = None
    outline: BaseGeometry | None = None


def outcome(built: Built) -> Outcome:
    b, world = built.board, built.world
    try:
        box = b.box()
    except LangError as e:
        return Outcome(e.message)
    extents: list[Range] = []
    for k in range(3):
        a = world.axis(k)
        extents.append((world.back(a, box.lo[a]), world.back(a, box.hi[a])))
    # (the outline is in the language's (u, v), the world axes in x, y, z order)
    u, v = b.u_axis, b.v_axis
    g = affinity.translate(b.outline.geometry, -world.variant.origin[AXES.index(u)],
                           -world.variant.origin[AXES.index(v)])
    if u != world.axis(1):
        g = affinity.affine_transform(g, [0, 1, 1, 0, 0, 0])
    return Outcome(None, (extents[0], extents[1], extents[2]), g)


# -- strategies -----------------------------------------------------------------------------------------

def _notched_corners(draw: st.DrawFn) -> list[Point2]:
    """A unit square, counter-clockwise, with rectangular or V notches
    into its sides (a wheel arch, a rib, a slot narrower than the board)."""
    square = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    out: list[Point2] = []
    for k in range(4):
        a, b = square[k], square[(k + 1) % 4]
        d = (b[0] - a[0], b[1] - a[1])
        inward = (-d[1], d[0])
        out.append(a)
        notches = sorted(draw(st.lists(st.tuples(floats(0.1, 0.9), floats(0.005, 0.4), floats(0.01, 0.4),
                                                 st.booleans()), max_size=2)))
        end = 0.05
        for s, w, depth, vee in notches:
            s0, s1 = max(s - w / 2, end + 0.02), min(s + w / 2, 0.95)
            if s1 - s0 < 0.002:
                continue
            end = s1

            def at(f: float, n: float) -> Point2:
                return (a[0] + d[0] * f + inward[0] * n, a[1] + d[1] * f + inward[1] * n)
            out += [at(s0, 0), at((s0 + s1) / 2, depth), at(s1, 0)] if vee else \
                [at(s0, 0), at(s0, depth), at(s1, depth), at(s1, 0)]
    return out


def _star_corners(draw: st.DrawFn) -> list[Point2]:
    n = draw(st.integers(3, 12))
    angles = sorted(set(draw(st.lists(floats(0, 359), min_size=n, max_size=n))))
    if len(angles) < 3:
        angles = [0.0, 120.0, 240.0]
    radii = draw(st.lists(floats(0.15, 0.5), min_size=len(angles), max_size=len(angles)))
    return [(0.5 + r * math.cos(math.radians(a)), 0.5 + r * math.sin(math.radians(a))) for a, r in zip(angles, radii)]


def _profile_points(draw: st.DrawFn) -> list[Point2]:
    """An open profile as (b, a) in the unit square, b running from 0 to 1
    (now and then back a little, an overhang): a straight edge, a random
    walk, steps, or ribs and valleys as the van floor has them."""
    kind = draw(st.sampled_from(["line", "walk", "walk", "steps", "ribs", "overhang"]))
    if kind == "line":
        return [(0.0, draw(floats(0, 1))), (1.0, draw(floats(0, 1)))]
    if kind == "ribs":
        level, depth = draw(floats(0.3, 1)), draw(floats(0.05, 0.3))
        points = [(0.0, level)]
        b = 0.0
        for _ in range(draw(st.integers(1, 5))):
            gap, top, bottom = draw(floats(0.003, 0.2)), draw(floats(0.003, 0.15)), draw(floats(0.0, 0.1))
            if b + gap + top > 0.98:
                break
            slope = (top - bottom) / 2 if top > bottom else 0.0
            b += gap
            points += [(b, level), (b + slope, level - depth), (b + top - slope, level - depth), (b + top, level)]
            b += top
        return points + [(1.0, level)]
    n = draw(st.integers(1, 9))
    bs = sorted(set(draw(st.lists(floats(0.01, 0.99), min_size=n, max_size=n))))
    points = [(0.0, draw(floats(0, 1)))] + [(b, draw(floats(0, 1))) for b in bs] + [(1.0, draw(floats(0, 1)))]
    if kind == "steps":
        stepped: list[Point2] = [points[0]]
        for p in points[1:]:
            stepped += [(p[0], stepped[-1][1]), p]
        return stepped
    if kind == "overhang" and len(points) > 3:
        i = draw(st.integers(1, len(points) - 3))
        points[i], points[i + 1] = (points[i + 1][0], points[i][1]), (points[i][0], points[i + 1][1])
    return points


def _radii(draw: st.DrawFn, n: int, scale: float) -> tuple[float, ...]:
    """Mostly sharp corners, some rounded, as the master's fillets are."""
    if not draw(st.booleans()):
        return (0.0,) * n
    return tuple(draw(st.lists(st.one_of(st.just(0.0), sizes(0.5, max(1.0, scale))), min_size=n, max_size=n)))


def _scaled(points: list[Point2], p: Range, q: Range) -> list[Point2]:
    return [(p[0] + x * (p[1] - p[0]), q[0] + y * (q[1] - q[0])) for x, y in points]


def _cover(draw: st.DrawFn, r: Range) -> Range:
    """A range over most of `r`, now and then short of an end or past it."""
    w = r[1] - r[0]
    return (r[0] + draw(floats(-0.3, 0.3)) * w, r[1] + draw(floats(-0.3, 0.3)) * w)


def _band(draw: st.DrawFn, lo: float, hi: float, least: float = 0.0) -> Range:
    """A range on t around the board's faces lo..hi: just past them, a
    little or far, now and then short of one; no nearer to them than
    `least` (an open contour ending in a face, within a rounding, ends
    there or not)."""
    t = hi - lo
    near = st.one_of(sizes(least, 3 * t), sizes(least, 3 * t), sizes(least, 600), sizes(least, 600),
                     sizes(least, t).map(lambda x: -x))
    return (lo - draw(near), hi + draw(near))


def _closed(draw: st.DrawFn, normal: int, p: Range, q: Range, plane: float) -> ContourSpec:
    kind = draw(st.sampled_from(["notched", "notched", "star", "circle"]))
    scale = 0.2 * min(p[1] - p[0], q[1] - q[0])
    if kind == "circle":
        r = max(1.0, min(p[1] - p[0], q[1] - q[0]) / 2)
        return ContourSpec(True, normal, plane, (((p[0] + p[1]) / 2, (q[0] + q[1]) / 2),), (r,), circle=True)
    corners = _scaled(_notched_corners(draw) if kind == "notched" else _star_corners(draw), p, q)
    if not Polygon(corners).is_valid:
        corners = _scaled([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)], p, q)
    if draw(st.booleans()):
        corners.reverse()                       # (clockwise, as a sketch may run)
    return ContourSpec(True, normal, plane, tuple(corners), _radii(draw, len(corners), scale))


def _open(draw: st.DrawFn, normal: int, along: int, b: Range, a: Range, plane: float) -> ContourSpec:
    """An open profile running along the plane coordinate `along` (0 or 1)
    over `b`, its other coordinate within `a`."""
    pts = [(b[0] + x * (b[1] - b[0]), a[0] + y * (a[1] - a[0])) for x, y in _profile_points(draw)]
    corners = pts if along == 0 else [(y, x) for x, y in pts]
    if draw(st.booleans()):
        corners.reverse()
    return ContourSpec(False, normal, plane, tuple(corners), _radii(draw, len(corners), 0.3 * (a[1] - a[0]) + 1))


Role = Literal["in closed", "in open", "perp closed", "perp open"]


@st.composite
def contour_cases(draw: st.DrawFn) -> ContourCase:
    t = draw(st.sampled_from([6.0, 9.0, 12.0, 15.0, 18.0, 24.0, 40.0]))
    room_t = (0.0, draw(sizes(max(30.0, t), 1000)))
    room: tuple[Range, Range, Range] = (room_t, (0.0, draw(sizes(50, 2000))), (0.0, draw(sizes(50, 2000))))
    at = draw(st.one_of(floats(room_t[0] + t / 2, room_t[1] - t / 2), sizes(room_t[0], room_t[1])))
    t0, t1 = at - t / 2, at + t / 2
    # As build files use them: a panel in an outline, an edge it stops at, a
    # batten across a floor profile ending at the outline, ends at contours
    # across; or anything.
    a1, a2 = draw(st.permutations([1, 2]))
    usual: list[list[tuple[Role, int]]] = [
        [("in closed", a1)], [("in open", a1)], [("in open", a1), ("perp closed", a2)],
        [("in closed", a1), ("in open", a1)], [("in closed", a1), ("perp closed", a2)], [("perp closed", a1)],
        [("perp open", a1)], [("perp closed", a1), ("perp open", a2)], [("perp open", a1), ("perp open", a2)],
        [("in open", a1), ("perp open", a2)], [("in closed", a1), ("in closed", a1)]]
    kinds: list[Role] = ["in closed", "in open", "perp closed", "perp open"]
    roles: list[tuple[Role, int]] = draw(st.one_of(
        st.sampled_from(usual), st.sampled_from(usual),
        st.lists(st.tuples(st.sampled_from(kinds), st.integers(1, 2)), min_size=1, max_size=3)))
    contours: list[ContourSpec] = []
    limits: list[LimitSpec] = []
    #: Per axis: where an open contour lies on it (-1 the low end, +1 the high end).
    ends: dict[int, int] = {}
    plane = st.one_of(st.just(0.0), sizes(-3000, 3000))
    for role, axis in roles:
        other = 3 - axis
        if role == "in closed":
            spec = _closed(draw, 0, _cover(draw, room[1]), _cover(draw, room[2]), draw(plane))
        elif role == "perp closed":
            # the contour's plane is (t, axis): its normal is the board's other axis
            spec = _closed(draw, other, _band(draw, t0, t1), _cover(draw, room[axis]), draw(plane))
        else:
            r = room[axis]
            w = r[1] - r[0]
            end = ends.setdefault(axis, draw(st.sampled_from([-1, 1])))
            a = sorted((r[0] + draw(floats(-0.1, 0.4)) * w, r[0] + draw(floats(-0.1, 0.4)) * w))
            if end > 0:
                a = sorted((r[1] - a[0] + r[0], r[1] - a[1] + r[0]))
            if role == "in open":
                # in (u, v): the profile runs along the other axis
                spec = _open(draw, 0, other - 1, _cover(draw, room[other]), (a[0], a[1]), draw(plane))
            else:
                spec = _open(draw, other, 0, _band(draw, t0, t1, NARROWEST), (a[0], a[1]), draw(plane))
        # (no clearance under 0.01 mm is meant)
        gap = draw(st.one_of(st.none(), st.just(0.0), sizes(0, 30), sizes(0, 20).map(lambda x: -x))
                   .map(lambda g: g if g is None or abs(g) >= NARROWEST else 0.0))
        limits.append(LimitSpec("contour", index=len(contours), gap=gap))
        contours.append(spec)
    for axis in (1, 2):
        r = room[axis]
        w = r[1] - r[0]
        # (an open contour is one end, so mostly one more limit there)
        count = draw(st.sampled_from([0, 1, 1, 1, 2] if axis in ends else [0, 0, 1, 1, 2]))
        for _ in range(count):
            kind: Literal["pos", "side", "end"] = draw(st.sampled_from(["pos", "pos", "pos", "side", "end"]))
            if kind != "pos":
                limits.append(LimitSpec(kind, axis, float(draw(st.integers(0, 1)))))
                continue
            end = ends.get(axis)
            # beside an open contour, mostly on the far side from it
            if end is not None and draw(st.integers(0, 3)):
                lo, hi = (0.45, 1.1) if end < 0 else (-0.1, 0.55)
            else:
                lo, hi = -0.1, 1.1
            limits.append(LimitSpec("pos", axis, draw(st.one_of(floats(r[0] + lo * w, r[0] + hi * w),
                                                                 sizes(r[0] + lo * w, r[0] + hi * w)))))
    order = draw(st.permutations(limits))
    n = len(contours)
    far = st.one_of(sizes(-6000, 6000), floats(-6000, 6000))
    base = Variant(tuple(draw(st.permutations([0, 1, 2]))), draw(st.one_of(st.just((0.0, 0.0, 0.0)),  # pyright: ignore[reportArgumentType]
                                                                                st.tuples(far, far, far))))
    other_variant = Variant(
        tuple(draw(st.permutations([0, 1, 2]))), draw(st.tuples(far, far, far)),  # pyright: ignore[reportArgumentType]
        tuple(draw(st.lists(st.booleans(), min_size=n, max_size=n))),
        tuple(draw(st.lists(st.integers(0, 50), min_size=n, max_size=n))),
        tuple(draw(st.lists(st.sampled_from([0, 0, 1, 3]), min_size=n, max_size=n))),
        tuple(draw(st.lists(st.one_of(st.just(0.0), far), min_size=n, max_size=n))),
        tuple(draw(st.lists(st.booleans(), min_size=n, max_size=n))))
    return ContourCase(room, t, at, tuple(contours), tuple(order), draw(st.sampled_from([12.0, 15.0, 18.0])),
                       base, other_variant)


# -- working out the board independently ---------------------------------------------------------------

class Refusal(Exception):
    """The board the case asks for is not one the rules allow."""


@dataclass
class Region:
    """What a contour limit allows of the plane it lies in, in its plane's
    coordinates: the region with the clearance taken off (or added), the
    region the contour bounds (inside a closed one, the board's side of an
    open one), and the contour as the clearance is measured from it."""
    allowed: BaseGeometry
    bounded: BaseGeometry
    contour: BaseGeometry


@dataclass
class Expected:
    box: tuple[Range, Range, Range]
    outline: BaseGeometry
    #: Per contour limit (by its index in `limits`): what it allows.
    regions: dict[int, Region]


def _round_offset(area: BaseGeometry, distance: float) -> BaseGeometry:
    """The area grown by `distance`, as `contours.round_offset` grows it:
    the offset is checked on its own (`test_fuzz_contours`, and the
    distances below); this reckons what the board does with it."""
    return round_offset(area, distance)


def _area(points: list[Point2]) -> BaseGeometry:
    poly = Polygon(points)
    if not poly.is_valid:
        poly = make_valid(poly)
    return unary_union(polygons_of(poly))


def _gap(limit: LimitSpec) -> float:
    return 0.0 if limit.gap is None else limit.gap


def side_region(points: list[Point2], along: int, side: int) -> tuple[BaseGeometry, LineString]:
    """The region on `side` of an open polyline (+1: toward the high values
    of the coordinate it does not run along), the polyline extended past
    both ends along coordinate `along`: one of the pieces it splits a
    large square into. Also the extended polyline."""
    across = 1 - along
    pts = list(points)
    if pts[0][along] > pts[-1][along]:
        pts.reverse()

    def at(b: float, a: float) -> Point2:
        return (b, a) if along == 0 else (a, b)
    line = LineString([at(pts[0][along] - _EXTEND, pts[0][across])] + pts
                      + [at(pts[-1][along] + _EXTEND, pts[-1][across])])
    square = shapely_box(-_SQUARE, -_SQUARE, _SQUARE, _SQUARE)
    middle = (pts[0][along] + pts[-1][along]) / 2
    probe = Point(at(middle, side * 0.9 * _SQUARE))
    pieces = [p for p in polygons_of(split(square, line)) if p.intersects(probe)]
    return (pieces[0] if pieces else Polygon()), line


def fits(allowed: BaseGeometry, t0: float, t1: float, inside: float = _INSIDE) -> list[Range]:
    """The stretches of s over which the board's section from t0 to t1 lies
    wholly in `allowed` (in (t, s)): all but the projections onto s of the
    pieces of that band outside it, the band `inside` within the faces (a
    closed contour's edge lying in a face does not count; an open one
    crossing it does)."""
    if allowed.is_empty:
        return []
    lo, hi = allowed.bounds[1] - 1.0, allowed.bounds[3] + 1.0
    band = shapely_box(t0 + inside, lo, t1 - inside, hi)
    blocked = sorted((p.bounds[1], p.bounds[3]) for p in polygons_of(band.difference(allowed)))
    out: list[Range] = []
    here = lo
    for b0, b1 in blocked:
        if b0 > here:
            out.append((here, b0))
        here = max(here, b1)
    if hi > here:
        out.append((here, hi))
    return [r for r in out if r[1] - r[0] > 1e-9 and r[0] > lo and r[1] < hi]


def _crossings(line: LineString, t: float) -> int:
    """How often the polyline (in (t, s)) meets the line t = const, a
    stretch along it counting twice (as `contours._crossings`)."""
    hit = line.intersection(LineString([(t, -_EXTEND), (t, _EXTEND)]))
    values: set[float] = set()
    for g in getattr(hit, "geoms", [hit]):
        if not g.is_empty:
            values.update(round(float(c[1]), 9) for c in g.coords)
    return len(values)


def _pick(pieces: list[Range], values: list[float], centre: float) -> Range:
    """The stretch the board's limits pick (as `between()` documents it)."""
    if len(pieces) == 1:
        return pieces[0]
    if len(values) >= 2:
        a, b = sorted(values[:2])
        chosen = [p for p in pieces if min(p[1], b) - max(p[0], a) > 1e-9]
    else:
        point = values[0] if values else centre
        chosen = [p for p in pieces if p[0] - 1e-9 <= point <= p[1] + 1e-9]
    if len(chosen) != 1:
        raise Refusal(f"the limits pick {len(chosen)} of the stretches {pieces}")
    return chosen[0]


def faces(case: ContourCase, variant: Variant) -> Range:
    """The board's faces on t, in its frame, as the variant's world has
    them (a face meeting a contour's end in one frame can miss it by a
    rounding in another)."""
    o = variant.origin[variant.axes[0]]
    centre = World(variant).at(0, case.at)
    return (centre - case.t / 2) - o, (centre + case.t / 2) - o


def expected(case: ContourCase, variant: Variant | None = None) -> Expected:
    """The board the case describes, worked out in its own frame, or a
    Refusal. The rules of `between()` decide which limits apply where; the
    geometry is reckoned here in its own way."""
    t0, t1 = faces(case, variant or case.base)
    regions: dict[int, Region] = {}
    areas: list[BaseGeometry] = []
    #: per axis it limits: the limit's index, the limit, its points in (u, v), the coordinate it runs along
    edges: dict[int, list[tuple[int, LimitSpec, list[Point2], int]]] = {1: [], 2: []}
    sections: dict[int, list[BaseGeometry]] = {1: [], 2: []}
    crossings: dict[int, list[tuple[int, LimitSpec, list[Point2]]]] = {1: [], 2: []}
    for i, limit in enumerate(case.limits):
        if limit.kind != "contour":
            continue
        spec = case.contours[limit.index]
        points = polyline(spec)
        g = _gap(limit)
        if spec.normal == 0:
            if spec.closed:
                area = _area(points)
                regions[i] = Region(_round_offset(area, -g), area, area.boundary)
                areas.append(regions[i].allowed)
                continue
            du, dv = abs(points[-1][0] - points[0][0]), abs(points[-1][1] - points[0][1])
            if abs(du - dv) < 1e-6:
                raise Refusal("the chord runs diagonally")
            # the axis it limits is the one across its chord; it runs along the other
            axis, along = (1, 1) if du < dv else (2, 0)
            edges[axis].append((i, limit, points, along))
            continue
        s = 3 - spec.normal                     # the axis the two planes share
        if spec.closed:
            area = _area(points)
            regions[i] = Region(_round_offset(area, -g), area, area.boundary)
            sections[s].append(regions[i].allowed)
        else:
            crossings[s].append((i, limit, points))

    extents: dict[int, Range] = {}
    for axis in sorted((1, 2), key=lambda k: bool(edges[k])):
        room = case.room[axis]
        centre = (room[0] + room[1]) / 2
        values = _values(case, axis)
        explicit = bool(values)
        if values:
            reference = sum(values) / len(values)
        elif edges[axis]:
            # the side of an open contour across the board is the one an open contour in its plane is on
            _, _, points, along = edges[axis][0]
            across = [p[1 - along] for p in points]
            reference = (min(across) + max(across)) / 2
        else:
            reference = centre
        #: The open contours across the board on this axis: (position, side).
        ends: list[tuple[float, int]] = []
        for i, limit, points in crossings[axis]:
            g = _gap(limit)
            pos, side = _open_position(points, g, reference, explicit, t0, t1)
            values.append(pos)
            ends.append((pos, side))
            region = side_region(points, 0, side)[0]
            regions[i] = Region(_round_offset(region, -g), region, LineString(points))
        stretch: Range | None = None
        for area in areas:
            if area.is_empty:
                raise Refusal("a closed contour leaves nothing")
            b = area.bounds
            k = 0 if axis == 1 else 1
            stretch = (max(stretch[0], b[k]), min(stretch[1], b[k + 2])) if stretch else (b[k], b[k + 2])
        for allowed in sections[axis]:
            pieces = fits(allowed, t0, t1)
            if not pieces:
                raise Refusal("the board lies outside a closed contour")
            piece = _pick(pieces, values, centre)
            stretch = (max(stretch[0], piece[0]), min(stretch[1], piece[1])) if stretch else piece
        if stretch is not None and stretch[1] <= stretch[0]:
            raise Refusal("the contours leave no room")
        if len(values) + len(edges[axis]) > 2:
            raise Refusal("more than two limits")
        if len(edges[axis]) > 1:
            raise Refusal("two open contours limit one axis")
        span = stretch if stretch is not None else room
        if len(values) == 2:
            a, b = sorted(values)
        elif edges[axis]:
            i, limit, points, along = edges[axis][0]
            across = [p[1 - along] for p in points]
            near = values[0] if values else (span[0] + span[1]) / 2
            side = 1 if near > max(across) else -1 if near < min(across) else 0
            if side == 0:
                raise Refusal("the board's other limit lies within the contour's reach")
            if not values:
                near = span[1] if side > 0 else span[0]
            region, line = side_region(points, along, side)
            g = _gap(limit)
            regions[i] = Region(_round_offset(region, -g), region, line)
            # from the contour (the trim finds where) to the other limit
            a, b = (-_EXTEND, near) if side > 0 else (near, _EXTEND)
        elif len(values) == 1:
            v = values[0]
            if ends:
                a, b = (v, span[1]) if ends[0][1] > 0 else (span[0], v)
            else:
                a, b = (v, span[1]) if v < (span[0] + span[1]) / 2 else (span[0], v)
        else:
            a, b = span
        # an open contour across the board gives its end on the contour's side
        for pos, side in ends:
            if (a < pos - 1e-9) if side > 0 else (b > pos + 1e-9):
                raise Refusal("the board would lie on the other side of an open contour")
        if stretch is not None:
            a, b = max(a, stretch[0]), min(b, stretch[1])
        if b - a < NARROWEST:
            raise Refusal(f"the extent on axis {axis} is {b - a:g}")
        extents[axis] = (a, b)
    rect = shapely_box(extents[1][0], extents[2][0], extents[1][1], extents[2][1])
    trims = areas + [regions[i].allowed for k in (1, 2) for i, *_ in edges[k]]
    outline: BaseGeometry = rect
    if trims:
        for allowed in trims:
            outline = outline.intersection(allowed)
        outline = clean(unary_union(polygons_of(outline)))
        pieces = polygons_of(outline)
        if not pieces or outline.area < 1e-6:
            raise Refusal("the contours leave nothing of the board")
        if len(pieces) > 1:
            raise Refusal(f"the contours split the board into {len(pieces)} pieces")
        u0, v0, u1, v1 = outline.bounds
        extents[1], extents[2] = (u0, u1), (v0, v1)
    return Expected(((t0, t1), extents[1], extents[2]), outline, regions)


def _values(case: ContourCase, axis: int) -> list[float]:
    """The positions the case's other limits give on `axis`: a position,
    the room's side, an end board's face toward the other limit there, or
    toward the room's middle."""
    room = case.room[axis]
    values: list[float] = []
    ends: list[tuple[float, float]] = []
    for limit in case.limits:
        if limit.axis != axis or limit.kind == "contour":
            continue
        if limit.kind == "pos":
            values.append(limit.value)
        elif limit.kind == "side":
            values.append(room[1] if limit.value > 0 else room[0])
        else:
            ends.append((room[1] - case.end_t, room[1]) if limit.value > 0 else (room[0], room[0] + case.end_t))
    positions = list(values)
    centre = (room[0] + room[1]) / 2
    for j, (lo, hi) in enumerate(ends):
        others = positions + [(e[0] + e[1]) / 2 for k, e in enumerate(ends) if k != j]
        toward = others[0] if len(others) == 1 else centre
        values.append(hi if toward >= (lo + hi) / 2 else lo)
    if len(values) > 2:
        raise Refusal("more than two limits")
    return values


def _open_position(points: list[Point2], gap: float, reference: float, explicit: bool, t0: float,
                   t1: float) -> tuple[float, int]:
    """Where an open contour in a perpendicular plane (in (t, s)) puts the
    board's end on s, and the side the board is on (+1: above it): the
    board keeps to the side of `reference` (its other limit, when
    `explicit`, else an open contour in its plane or the middle of the
    room) and the gap from the contour, over its whole thickness."""
    line = LineString(points)
    for t in (t0, t1):
        if _crossings(line, t) != 1:
            raise Refusal("the open contour does not cross a face once")
    inside = line.intersection(shapely_box(t0, -_EXTEND, t1, _EXTEND))
    s = [float(c[1]) for g in getattr(inside, "geoms", [inside]) if not g.is_empty for c in g.coords]
    side = 1 if reference > max(s) else -1 if reference < min(s) else 0
    if side == 0:
        raise Refusal("the open contour crosses the board between its other limits")
    region, _ = side_region(points, 0, side)
    pieces = fits(_round_offset(region, -gap), t0, t1, inside=0.0)
    if explicit:
        # the stretch the other limit lies in
        pieces = [p for p in pieces if p[0] - 1e-9 <= reference <= p[1] + 1e-9]
    if not pieces:
        raise Refusal("the clearance passes the board's other limit")
    return (min(p[0] for p in pieces), 1) if side > 0 else (max(p[1] for p in pieces), -1)


# -- the checks -------------------------------------------------------------------------------------------

def _slack(gap: float) -> float:
    """How much nearer than the gap a board may come to a contour (mm): the
    offsets' round joins are polygons inside their arcs, GEOS's steps up to
    1.5 times an eighth of a quarter turn (it rounds their number), and the
    faces are sectioned 1e-6 inside."""
    return abs(gap) * (1 - math.cos(0.75 * math.pi / 16)) + 1e-5


def _section(e: Expected | Outcome, spec: ContourSpec) -> BaseGeometry:
    """The board as the contour's plane sees it: its outline in (u, v) for
    a contour in its own plane, else its section across that plane."""
    assert e.box is not None and e.outline is not None
    if spec.normal == 0:
        return e.outline
    s = 3 - spec.normal
    return shapely_box(e.box[0][0], e.box[s][0], e.box[0][1], e.box[s][1])


def _limit_problems(case: ContourCase, got: Outcome, regions: dict[int, Region]) -> list[str]:
    """The board lies within what each contour allows and keeps its gap."""
    problems: list[str] = []
    for i, limit in enumerate(case.limits):
        if limit.kind != "contour" or i not in regions:
            continue
        spec = case.contours[limit.index]
        region = regions[i]
        g = _gap(limit)
        shape = _section(got, spec)
        what = (f"contour {limit.index} ({'closed' if spec.closed else 'open'}, "
                f"{'in its plane' if spec.normal == 0 else 'across it'})")
        # (what is narrower than NARROWEST is nothing: a face a rounding past a contour's edge)
        if g >= 0:
            outside = clean(shape.difference(region.bounded)).area
            if outside > 1e-6:
                problems.append(f"the board reaches {outside:.3g} mm2 past {what}")
            elif g > 0:
                near = shape.distance(region.contour)
                if near < g - _slack(g):
                    problems.append(f"the board comes {near:.4g} near {what}, its gap is {g:g}")
        else:
            past = clean(shape.difference(region.bounded).difference(region.contour.buffer(-g + _slack(g))))
            if past.area > 1e-6:
                problems.append(f"the board reaches further than {-g:g} past {what} ({past.area:.3g} mm2)")
    return problems


def _inside_problems(case: ContourCase, built: Built) -> list[str]:
    """`checks.inside()` with each closed contour's gap passes the board."""
    problems: list[str] = []
    for limit in case.limits:
        if limit.kind == "contour" and case.contours[limit.index].closed:
            found = inside(built.contours[limit.index], gap=_gap(limit))(built.module)
            problems += [f"inside(): {p}" for p in found if p.startswith(built.board.path)]
    return problems


def _same(a: Outcome | Expected, b: Outcome | Expected) -> tuple[str, float] | None:
    """How two boards in the board's frame differ, and by how much (mm),
    or None."""
    assert a.box is not None and b.box is not None and a.outline is not None and b.outline is not None
    for k in range(3):
        for end in (0, 1):
            off = abs(a.box[k][end] - b.box[k][end])
            if off > 1e-5:
                return (f"its {'tuv'[k]} {'low' if end == 0 else 'high'} end at {a.box[k][end]:.6g} against "
                        f"{b.box[k][end]:.6g}", off)
    d = a.outline.symmetric_difference(b.outline)
    if d.area > 1e-5 * max(1.0, a.outline.length) and clean(d).area > 1e-6:
        return f"the outlines differ by {d.area:.3g} mm2", a.outline.hausdorff_distance(b.outline)
    return None


#: Known and open (2026-10-14), so the checks mark them `KNOWN`:
#:
#: - GEOS simplifies what it offsets, by about a hundredth of the distance
#:   (a pass; up to 1.4 % seen) and only toward more clearance, and how
#:   depends on the form it is given. `contours.round_offset` gives it one
#:   form, but a mirrored area (the board's axes the other way round, or
#:   the reckoning's region against the language's) is another, so a
#:   clearance can differ by that much. Whether to offset exactly is
#:   Florian's to decide: an own offset of rectangles and discs was exact,
#:   but GEOS unites such pieces wrongly where their edges nearly coincide.
#: - An open contour that runs back along the direction it runs in (an
#:   overhang): which side of it the board fills is open. The language
#:   closes the region beyond it into a ring and makes that valid; the
#:   reckoning splits a square with it.
def _offset_noise(case: ContourCase) -> float:
    """How much GEOS's simplification may move a board (mm)."""
    return 0.02 * max((abs(_gap(limit)) for limit in case.limits if limit.kind == "contour"), default=0.0) + 1e-5


def overhangs(case: ContourCase) -> bool:
    """Whether an open contour the board takes runs back along the
    direction it runs in: along its chord in the board's plane, along t
    across it."""
    for limit in case.limits:
        if limit.kind != "contour" or case.contours[limit.index].closed:
            continue
        spec = case.contours[limit.index]
        pts = polyline(spec)
        along = 0
        if spec.normal == 0:
            along = 1 if abs(pts[-1][0] - pts[0][0]) < abs(pts[-1][1] - pts[0][1]) else 0
        steps = [q[along] - p[along] for p, q in zip(pts, pts[1:])]
        if any(d > 1e-9 for d in steps) and any(d < -1e-9 for d in steps):
            return True
    return False


def _known(case: ContourCase, problem: str, off: float | None = None) -> str:
    """The problem, marked known when it is one of the open items above."""
    if overhangs(case):
        return f"{KNOWN} an open contour runs back along itself; {problem}"
    if off is not None and off <= _offset_noise(case):
        return f"{KNOWN} offsets differ by GEOS's simplification; {problem}"
    return problem


def run_case(case: ContourCase) -> list[str]:
    """What is wrong with the board the case's contours limit."""
    try:
        with fresh():
            problems, first = _attempt(case, case.base, check=True)
        if [p for p in problems if not p.startswith(KNOWN)]:
            return problems
        with fresh():
            _, second = _attempt(case, case.other, check=False)
    except Exception as e:
        frame = next((fr for fr in reversed(traceback.extract_tb(e.__traceback__))
                      if "/lang/" in fr.filename), traceback.extract_tb(e.__traceback__)[-1])
        return [f"{type(e).__name__} at {Path(frame.filename).name}:{frame.lineno}: {e}"]
    if (first.refused is None) != (second.refused is None):
        return problems + [_known(case, f"one variant refuses, the other not: {first.refused or second.refused}")]
    if first.refused is None:
        diff = _same(first, second)
        if diff:
            return problems + [_known(case, f"another variant comes out otherwise: {diff[0]}", diff[1])]
    return problems


def _attempt(case: ContourCase, variant: Variant, check: bool) -> tuple[list[str], Outcome]:
    built = build(case, variant)
    ends = [(e.box(), e.outline.geometry.wkt) for e in built.ends]
    got = outcome(built)
    problems: list[str] = []
    if got.refused is not None:
        again = outcome(built)
        if again.refused != got.refused:
            problems.append(f"a refusal is not the same again: {got.refused!r}, then {again.refused!r}")
        if [(e.box(), e.outline.geometry.wkt) for e in built.ends] != ends:
            problems.append("a refusal changed another board")
    if not check:
        return problems, got
    try:
        want: Expected | None = expected(case, variant)
        reason = None
    except Refusal as r:
        want, reason = None, str(r)
    if got.refused is not None:
        if want is not None:
            problems.append(_known(case, f"refused ({got.refused}), though it fits"))
        return problems, got
    if want is None:
        problems.append(_known(case, f"accepted, though {reason}"))
        return problems, got
    problems += [_known(case, p) for p in _limit_problems(case, got, want.regions)]
    diff = _same(got, want)
    if diff:
        problems.append(_known(case, f"not the board worked out: {diff[0]}", diff[1]))
    problems += _inside_problems(case, built)
    problems += _pipeline_problems()
    return problems, got


__all__ = ["ContourCase", "ContourSpec", "KNOWN", "LimitSpec", "Variant", "contour_cases", "expected", "run_case"]
