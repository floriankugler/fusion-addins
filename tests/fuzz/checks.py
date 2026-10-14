"""Random scenes for fuzzing the design checks (`lang.core.checks`) as
`boards.py` fuzzes the cutouts: a case is plain data, built with the
language's own calls, and checked from the outside.

A scene is a few boards (planks) and hardware items in a module. The
first plank lies anywhere; every other one is placed against one before
it, parallel or across it, each of its ranges below, above, inside, along
or across the other's, touching it, apart by a gap or overlapping by
amounts around 1e-9, 1e-6 and 0.01 mm, or set into one of its pockets or
holes (a hatch in a recess, a divider in a groove, a dowel in a hole, its
corners on the circle or near it). The planks have outlines, holes,
pockets, through cuts, notches and rounded corners as `boards.py` draws
them, now and then a tab added to the outline past their box (as a
tenon's), and a sheet as large as they are, give or take a little. The
hardware boxes stand in holes with a flange on the face, lie against or in
a plank, or against another box. The module's box is the scene's, grown
or shrunk a little on each side; a closed contour may lie around it.

Each scene is built twice, placed otherwise: its axes turned and mirrored,
moved far and by fractions, in another world frame, in a module or a
cabinet, its planks declared in another order. `run_case` works out the
truth from each build's layout, read as the emitter reads it
(`lang.emit.plan.PartFrame`): boards in one plane slab by slab along their
thickness with exact 2D booleans (holes as circles drawn inside and around
them), boards across each other from the preview's meshes (manifold
booleans), hardware boxes exactly. The checks' verdicts and the pairs they
name must match it, and the same verdicts must come out of both builds.

What counts (mm): an overlap at least `ACROSS` deep along an axis and
`WIDE` wide in a plane must be reported; one at most `TOUCH` deep (or a
mesh film up to `FILM` thick) never; in between either (`clean` takes out
what is narrower than 0.01 mm, so an overlap that narrow in a board's plane
is not material). `inside_box`, `fits_sheet` and `inside(contour)` alike,
from the placement boxes, the outlines' extents and the shadows.

Known and open (marked `KNOWN`, 2026-10-14): an overlap narrower than 0.01
mm in a board's plane is not reported, though one as thin across the
thickness is; and material a part has past its placement box (a tab, a
tenon) is not looked at."""
from __future__ import annotations

import math
import re
import traceback
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import numpy as np
from hypothesis import strategies as st
from shapely import affinity
from shapely.geometry import Point, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from boards import KNOWN
from fuzzing import floats, fresh, sizes
from lang import (Box, LangError, Pos, Shape, board, cabinet, fits_sheet, inside, inside_box, material, module,
                  no_interference, scope, through)
from lang.core import directions
from lang.core.contours import Contour
from lang.core.directions import AXES, Axis, Frame
from lang.core.geometry import polygons_of
from lang.core.layout_types import BoxDict, HardwareBodyLayout, OpLayout, PartLayout
from lang.core.part import Board
from lang.core.scope import Scope
from lang.core.shapes import slot_shape
from lang.emit.plan import LayoutFrame, PartFrame, pieces
from lang.preview.mesh import mesh_part

#: An overlap along an axis (the boards' thickness, a box's sides) at least
#: this deep must be reported: ten times the checks' tolerance of 1e-6.
ACROSS = 1e-5
#: An overlap in a board's plane at least this wide must be reported:
#: `clean` takes out pieces narrower than 0.01 mm on average, and a
#: triangle 0.025 wide is 0.01 wide on average.
WIDE = 0.025
#: An overlap at most this deep in some direction is touching, which is
#: never reported (rounding at 6 m is 1e-12).
TOUCH = 1e-7
#: The meshes' booleans leave a film where faces coincide (joints.py
#: measured 3.6e-6): a shared volume no thicker than this is touching.
FILM = 1e-4
#: Sides of the polygons a hole's circle is drawn with, inside and around
#: it: the truth lies between the two (a sagitta of r * 1.2e-6; for the
#: meshes, which need not be as fine, r * 7.5e-5).
_CIRCLE = 2048
_MESH_CIRCLE = 256

Outline = Literal["rect", "rounded", "taper", "slot"]
FeatureKind = Literal["hole", "pocket", "cut", "notch", "vgroove", "fillet"]
Range = tuple[float, float]


# -- the scene, as data ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Feature:
    """An operation on a plank in its own frame: (p, q) mm from the low
    corner of its two in-plane scene axes (in ascending order). A hole `a`
    across, a pocket `a` by `b` turned by `angle` (a circle when `b` is 0),
    a through cut of that shape, a notch (a cut over the edge), a V-groove
    `a` long turned by `angle`, `b` deep (which the checks do not count as
    missing material, as documented), or every corner of the outline
    rounded with `a`; `face` is the big face, +1 on the high side of the
    plank's scene axis, -1 on the low; `depth` a fraction of the
    thickness, None for through."""
    kind: FeatureKind
    face: int
    p: float
    q: float
    a: float
    b: float = 0.0
    angle: float = 0.0
    depth: float | None = None


@dataclass(frozen=True)
class Plank:
    """A board: thick `t` along scene axis `axis` from `at`, from `lo` to
    `hi` on the other two (ascending); a tab (p0, q0, p1, q1 in its frame)
    added to its outline past its box, as joints add tenons; `sheet` the
    material's sheet size; declared in the sub-scope with `sub`."""
    t: float
    axis: int
    at: float
    lo: tuple[float, float]
    hi: tuple[float, float]
    outline: Outline = "rect"
    outline_r: float = 0.0
    features: tuple[Feature, ...] = ()
    tab: tuple[float, float, float, float] | None = None
    sheet: tuple[float, float] | None = None
    sub: bool = False

    def range(self, i: int) -> Range:
        """Its extent on scene axis `i`."""
        if i == self.axis:
            return (self.at, self.at + self.t)
        k = _others(self.axis).index(i)
        return (self.lo[k], self.hi[k])


@dataclass(frozen=True)
class HardwareBox:
    lo: tuple[float, float, float]
    hi: tuple[float, float, float]


@dataclass(frozen=True)
class Item:
    """A hardware item: bodies, each one or more boxes (scene mm)."""
    bodies: tuple[tuple[HardwareBox, ...], ...]
    sub: bool = False


@dataclass(frozen=True)
class ContourSpec:
    """A closed contour in the plane across scene axis `axis` at `at`, its
    ring on the two other scene axes (ascending), checked with `gap`."""
    axis: int
    at: float
    ring: tuple[tuple[float, float], ...]
    gap: float


@dataclass(frozen=True)
class Placement:
    """Where a scene is built: scene axis i is world axis `AXES[perm[i]]`,
    times `signs[i]`, moved by `offset` (world x, y, z); in world frame
    `FRAMES[frame]`, as a module or a cabinet facing world direction
    `cabinet` (an index into the frame's directions, top and bottom left
    out); planks declared in `order`, hardware items reversed or not."""
    perm: tuple[int, int, int]
    signs: tuple[int, int, int]
    offset: tuple[float, float, float]
    frame: int = 0
    cabinet: int | None = None
    order: tuple[int, ...] = ()
    reversed_items: bool = False


@dataclass(frozen=True)
class Scene:
    planks: tuple[Plank, ...]
    items: tuple[Item, ...]
    #: The module's box: the scene's grown by these (scene axis 0 low, high, axis 1 low, ...).
    margins: tuple[float, float, float, float, float, float]
    contour: ContourSpec | None
    places: tuple[Placement, Placement]


#: World frames to build in: the van's, a cabinet's facing +y, one with top
#: along y, and a mirrored one.
FRAMES = (Frame(), Frame(front="+y", left="-x", top="+z"), Frame(front="+z", left="+x", top="+y"),
          Frame(front="-x", left="+y", top="+z"))


def _others(axis: int) -> tuple[int, int]:
    a, b = (i for i in range(3) if i != axis)
    return a, b


# -- strategies --------------------------------------------------------------------------------

#: How far one range reaches into another (negative: a gap): touching, the
#: tolerances either side of the checks', a hundredth, or anything small.
_OFFSETS = st.one_of(st.sampled_from([0.0, 0.0, 0.0, 1e-9, -1e-9, 1e-6, -1e-6, 0.01, -0.01, 0.03, -0.03, 0.5, -0.5]),
                     floats(-3, 3))


def _thickness() -> st.SearchStrategy[float]:
    return st.one_of(st.sampled_from([6.0, 9.0, 12.0, 15.0, 18.0, 24.0]), sizes(3, 40))


@st.composite
def _range_near(draw: st.DrawFn, ref: Range, length: float | None) -> Range:
    """A range against `ref`: below or above it (touching, apart or into
    it by an offset), inside it, flush with its low or high end, across it
    or over either end; `length` long, or any length."""
    lo, hi = ref
    d = draw(_OFFSETS)
    size = length if length is not None else draw(st.one_of(sizes(5, 600), st.just(hi - lo)))
    mode = draw(st.sampled_from(["below", "above", "inside", "flush_low", "flush_high", "across", "over_low",
                                 "over_high"]))
    if mode == "below":
        return (lo + d - size, lo + d)
    if mode == "above":
        return (hi - d, hi - d + size)
    if mode == "inside":
        size = min(size, hi - lo) if length is None else size
        start = lo + draw(floats(0, 1)) * max(0.0, hi - lo - size)
        return (start, start + size)
    if mode == "flush_low":
        return (lo - d, lo - d + size)
    if mode == "flush_high":
        return (hi + d - size, hi + d)
    if mode == "across":
        if length is not None:
            mid = (lo + hi) / 2
            return (mid - size / 2, mid + size / 2)
        return (lo - draw(sizes(0, 100)) - d, hi + draw(sizes(0, 100)) + d)
    if mode == "over_low":
        start = lo - size + draw(floats(0, 1)) * size
        return (start, start + size)
    start = hi - draw(floats(0, 1)) * size
    return (start, start + size)


def _offset(extent: float) -> st.SearchStrategy[float]:
    near = sizes(0, min(60.0, extent))
    return st.one_of(floats(0, extent), near, near.map(lambda d: extent - d))


@st.composite
def _features(draw: st.DrawFn, size: tuple[float, float], t: float) -> Feature:
    kind: FeatureKind = draw(st.sampled_from(["hole", "hole", "pocket", "pocket", "pocket", "cut", "notch", "vgroove",
                                              "fillet"]))
    p, q = draw(_offset(size[0])), draw(_offset(size[1]))
    depth = draw(st.one_of(st.none(), floats(0.05, 0.95), st.just(0.5)))
    face = draw(st.sampled_from([1, -1]))
    if kind == "hole":
        return Feature(kind, face, p, q, draw(st.one_of(sizes(2, 40), sizes(40, 120))), depth=depth)
    if kind in ("pocket", "cut", "notch"):
        angle = draw(st.one_of(st.just(0.0), st.just(0.0), st.just(45.0), floats(0, 180)))
        a, b = draw(sizes(2, 160)), draw(st.one_of(st.just(0.0), sizes(2, 160)))
        return Feature(kind, face, p, q, a, b, angle, depth)
    if kind == "vgroove":
        return Feature(kind, face, p, q, draw(sizes(1, 300)), draw(floats(0.2, 0.45)) * t, draw(floats(0, 180)))
    return Feature(kind, 1, 0, 0, draw(sizes(1, 60)))


@st.composite
def _plank(draw: st.DrawFn, axis: int, ranges: dict[int, Range], t: float) -> Plank:
    """A plank with the given ranges on its two in-plane scene axes."""
    a, b = _others(axis)
    lo, hi = (ranges[a][0], ranges[b][0]), (ranges[a][1], ranges[b][1])
    size = (hi[0] - lo[0], hi[1] - lo[1])
    outline: Outline = draw(st.sampled_from(["rect", "rect", "rect", "rounded", "taper", "slot"]))
    outline_r = draw(floats(0.05, 0.45)) * min(size) if outline in ("rounded", "taper") else 0.0
    feats = tuple(draw(st.lists(_features(size, t), max_size=4)))
    tab = None
    if draw(st.integers(0, 7)) == 0:
        # (over the low edge on q or the high one on p, overlapping the outline by 1 mm)
        p0 = draw(floats(0, 0.8)) * size[0]
        q0 = draw(floats(0, 0.8)) * size[1]
        reach, width = draw(st.one_of(sizes(1, 40), st.sampled_from([0.01, 0.03]))), draw(sizes(2, 60))
        tab = (p0, -reach, p0 + width, 1.0) if draw(st.booleans()) else (size[0] - 1.0, q0, size[0] + reach, q0 + width)
    sheet = None
    if not any(f.kind in ("cut", "notch") for f in feats) and draw(st.booleans()):
        dw, dh = draw(_OFFSETS), draw(_OFFSETS)
        w, h = size[0] - dw, size[1] - dh
        sheet = (h, w) if draw(st.booleans()) else (w, h)
        if min(sheet) <= 0:
            sheet = None
    return Plank(t, axis, ranges[axis][0], lo, hi, outline, outline_r, feats, tab, sheet, draw(st.integers(0, 4)) == 0)


def _scene_range(p: Plank, f: Feature) -> tuple[int, int, Range, Range] | None:
    """A feature's footprint bounds as ranges on the plank's two in-plane
    scene axes; None for one that is not a hole or an upright pocket."""
    a, b = _others(p.axis)
    if f.kind == "hole" or (f.kind == "pocket" and f.b <= 0):
        r = f.a / 2
        return a, b, (p.lo[0] + f.p - r, p.lo[0] + f.p + r), (p.lo[1] + f.q - r, p.lo[1] + f.q + r)
    if f.kind == "pocket" and f.angle == 0.0:
        return a, b, (p.lo[0] + f.p - f.a / 2, p.lo[0] + f.p + f.a / 2), (p.lo[1] + f.q - f.b / 2,
                                                                          p.lo[1] + f.q + f.b / 2)
    return None


@st.composite
def _into(draw: st.DrawFn, ref: Plank, length: dict[int, float]) -> dict[int, Range] | None:
    """Ranges on the three scene axes that set something into one of the
    plank's holes or pockets: a rectangle in the circle, its corners on it
    or a little in or out, or in the pocket's bounds, a little in or out;
    from its face to the bottom, give or take a little, or through. The
    lengths given (a plank's thickness) are kept; None when the plank has
    no such feature."""
    found = [(f, r) for f in ref.features if (r := _scene_range(ref, f)) is not None]
    if not found:
        return None
    f, (a, b, ra, rb) = draw(st.sampled_from(found))
    d = draw(_OFFSETS)
    ranges: dict[int, Range] = {}
    if f.kind == "hole" or f.b <= 0:
        rho = max(0.5, f.a / 2 - d)                # the corners' distance from the centre
        turn = draw(st.one_of(st.just(math.pi / 4), floats(0.1, 1.4)))
        half = {a: rho * math.cos(turn), b: rho * math.sin(turn)}
        for axis in (a, b):
            if axis in length:
                half[axis] = length[axis] / 2
        centre = {a: (ra[0] + ra[1]) / 2, b: (rb[0] + rb[1]) / 2}
        for axis in (a, b):
            ranges[axis] = (centre[axis] - half[axis], centre[axis] + half[axis])
    else:
        for axis, r in ((a, ra), (b, rb)):
            m = draw(st.one_of(st.just(-d), sizes(0, 10)))
            if axis in length:
                mid = (r[0] + r[1]) / 2
                ranges[axis] = (mid - length[axis] / 2, mid + length[axis] / 2)
            else:
                ranges[axis] = (r[0] + m, r[1] - m) if r[1] - r[0] > 2 * m + 1 else r
    k = ref.axis
    deep = ref.t if f.depth is None else max(0.1, f.depth * ref.t)
    top, bottom = (ref.at + ref.t, ref.at + ref.t - deep) if f.face > 0 else (ref.at, ref.at + deep)
    e = draw(_OFFSETS)
    if k in length:
        lo = bottom - e if f.face > 0 else bottom + e - length[k]
        ranges[k] = (lo, lo + length[k])
    else:
        beyond = draw(sizes(0, 100))
        if f.depth is None and draw(st.booleans()):
            ranges[k] = (ref.at - beyond, ref.at + ref.t + draw(sizes(0, 100)))      # through and out
        else:
            ranges[k] = (bottom - e, top + beyond) if f.face > 0 else (top - beyond, bottom + e)
    return ranges


@st.composite
def _near(draw: st.DrawFn, ref: Plank, length: dict[int, float]) -> dict[int, Range]:
    """Ranges on the three scene axes against the plank's, or set into it."""
    if draw(st.integers(0, 2)) == 0:
        into = draw(_into(ref, length))
        if into is not None:
            return into
    return {i: draw(_range_near(ref.range(i), length.get(i))) for i in range(3)}


@st.composite
def _box_near(draw: st.DrawFn, ref: HardwareBox) -> dict[int, Range]:
    return {i: draw(_range_near((ref.lo[i], ref.hi[i]), None)) for i in range(3)}


def _box(ranges: dict[int, Range]) -> HardwareBox | None:
    if any(ranges[i][1] - ranges[i][0] <= 1e-3 for i in range(3)):
        return None
    return HardwareBox((ranges[0][0], ranges[1][0], ranges[2][0]), (ranges[0][1], ranges[1][1], ranges[2][1]))


@st.composite
def _mounted(draw: st.DrawFn, ref: Plank) -> tuple[HardwareBox, ...]:
    """A body standing in one of the plank's holes or pockets, with a flange
    on its face as wide as the hole and a little (or not), touching the
    face, off it or in it by an offset; or a box against the plank."""
    into = draw(_into(ref, {}))
    if into is None:
        box = _box(draw(_near(ref, {})))
        return () if box is None else (box,)
    core = _box(into)
    if core is None:
        return ()
    k = ref.axis
    # (which face the core came in from: the one its range reaches past)
    face = 1 if into[k][1] > ref.at + ref.t - 1e-9 else -1
    flange: dict[int, Range] = {}
    for i in range(3):
        if i == k:
            d, h = draw(_OFFSETS), draw(sizes(1, 20))
            flange[i] = (ref.at + ref.t - d, ref.at + ref.t - d + h) if face > 0 else (ref.at + d - h, ref.at + d)
        else:
            grow = draw(st.one_of(st.just(0.0), sizes(0, 10)))
            flange[i] = (into[i][0] - grow, into[i][1] + grow)
    second = _box(flange)
    return (core,) if second is None or draw(st.integers(0, 3)) == 0 else (core, second)


@st.composite
def _placements(draw: st.DrawFn, planks: int) -> Placement:
    perm = draw(st.permutations([0, 1, 2]))
    signs = draw(st.tuples(st.sampled_from([1, -1]), st.sampled_from([1, -1]), st.sampled_from([1, -1])))
    far = st.one_of(st.just(0.0), floats(-6000, 6000), sizes(-6000, 6000), st.sampled_from([0.1, 1234.56, -3000.3]))
    offset = draw(st.tuples(far, far, far))
    order = tuple(draw(st.permutations(list(range(planks)))))
    return Placement((perm[0], perm[1], perm[2]), signs, offset, draw(st.integers(0, len(FRAMES) - 1)),
                     draw(st.one_of(st.none(), st.integers(0, 3))), order, draw(st.booleans()))


@st.composite
def scenes(draw: st.DrawFn) -> Scene:
    t = draw(_thickness())
    axis = draw(st.integers(0, 2))
    size = st.one_of(sizes(40, 800), sizes(40, 800), sizes(40, 2500))
    first = draw(_plank(axis, {axis: (0.0, t), **{i: (0.0, draw(size)) for i in _others(axis)}}, t))
    planks = [first]
    for _ in range(draw(st.integers(0, 3))):
        ref = draw(st.sampled_from(planks))
        t = draw(_thickness())
        axis = draw(st.one_of(st.just(ref.axis), st.integers(0, 2)))
        ranges = draw(_near(ref, {axis: t}))
        if any(ranges[i][1] - ranges[i][0] < 1.0 for i in _others(axis)):
            continue
        planks.append(draw(_plank(axis, ranges, t)))
    items: list[Item] = []
    boxes: list[HardwareBox] = []
    for _ in range(draw(st.integers(0, 3))):
        bodies: list[tuple[HardwareBox, ...]] = []
        for _ in range(draw(st.integers(1, 2))):
            if boxes and draw(st.integers(0, 2)) == 0:
                one = _box(draw(_box_near(draw(st.sampled_from(boxes)))))
                body = () if one is None else (one,)
            else:
                body = draw(_mounted(draw(st.sampled_from(planks))))
            if body:
                bodies.append(body)
                boxes.extend(body)
        if bodies:
            items.append(Item(tuple(bodies), draw(st.integers(0, 4)) == 0))
    margin = st.one_of(sizes(0, 50), sizes(0, 50), _OFFSETS.map(lambda d: -d))
    margins = (draw(margin), draw(margin), draw(margin), draw(margin), draw(margin), draw(margin))
    contour = draw(st.one_of(st.none(), _contours(planks, boxes)))
    return Scene(tuple(planks), tuple(items), margins, contour,
                 (draw(_placements(len(planks))), draw(_placements(len(planks)))))


def _scene_bounds(planks: list[Plank] | tuple[Plank, ...],
                  boxes: list[HardwareBox] | tuple[HardwareBox, ...]) -> list[Range]:
    """The scene's extent on each scene axis: its planks' boxes and tabs
    and the hardware's."""
    out: list[Range] = []
    for i in range(3):
        spans = [p.range(i) for p in planks] + [(b.lo[i], b.hi[i]) for b in boxes]
        spans += [tab[i] for p in planks if (tab := _tab_ranges(p)) is not None and i in tab]
        out.append((min(s[0] for s in spans), max(s[1] for s in spans)))
    return out


@st.composite
def _contours(draw: st.DrawFn, planks: list[Plank], boxes: list[HardwareBox]) -> ContourSpec:
    """A rectangle around the scene's planks across a scene axis, each side
    out or in by a little, one corner cut off or not."""
    axis = draw(st.integers(0, 2))
    a, b = _others(axis)
    bounds = _scene_bounds(planks, [])
    gap = draw(st.sampled_from([0.0, 0.0, 2.0, 5.0]))
    m = [draw(st.one_of(_OFFSETS.map(lambda d: gap - d), sizes(0, 30))) for _ in range(4)]
    a0, a1 = bounds[a][0] - m[0], bounds[a][1] + m[1]
    b0, b1 = bounds[b][0] - m[2], bounds[b][1] + m[3]
    if a1 - a0 < 1 or b1 - b0 < 1:
        a0, a1, b0, b1 = a0 - 10, a1 + 10, b0 - 10, b1 + 10
    ring: list[tuple[float, float]] = [(a0, b0), (a1, b0), (a1, b1), (a0, b1)]
    if draw(st.booleans()):
        c = draw(floats(0.05, 0.45)) * min(a1 - a0, b1 - b0)
        ring = [(a0, b0), (a1 - c, b0), (a1, b0 + c), (a1, b1), (a0, b1)]
    return ContourSpec(axis, draw(floats(-500, 500)), tuple(ring), gap)


# -- building ---------------------------------------------------------------------------------

@dataclass
class Built:
    """A scene built at one placement: its module, its boards by plank
    index, which features each kept, the hardware's world boxes by body
    path, and the contour check."""
    scope: Scope
    boards: dict[int, Board]
    kept: dict[int, tuple[int, ...]]
    bodies: dict[str, list[BoxDict]] = field(default_factory=dict[str, list[BoxDict]])
    #: Why the language refused the features it did not keep, by plank and feature.
    refused: dict[tuple[int, int], str] = field(default_factory=dict[tuple[int, int], str])
    contour: Callable[[Scope], list[str]] | None = None


def _world(pl: Placement, i: int, r: Range) -> tuple[Axis, float, float]:
    """A range on scene axis `i` as the world axis and range it becomes."""
    axis = AXES[pl.perm[i]]
    a, b = pl.signs[i] * r[0] + pl.offset[pl.perm[i]], pl.signs[i] * r[1] + pl.offset[pl.perm[i]]
    return axis, min(a, b), max(a, b)


def _affine(pl: Placement, p: Plank, u: Axis) -> list[float]:
    """The map from the plank's (p, q) frame to the world (u, v) of its
    outline, for `affinity.affine_transform`."""
    a, b = _others(p.axis)
    sa, sb = pl.signs[a], pl.signs[b]
    ca, cb = sa * p.lo[0] + pl.offset[pl.perm[a]], sb * p.lo[1] + pl.offset[pl.perm[b]]
    if AXES[pl.perm[a]] == u:
        return [sa, 0.0, 0.0, sb, ca, cb]
    return [0.0, sb, sa, 0.0, cb, ca]


def _local_outline(p: Plank) -> BaseGeometry | None:
    a, b = p.hi[0] - p.lo[0], p.hi[1] - p.lo[1]
    if p.outline == "rect":
        return None
    if p.outline == "rounded":
        return Shape(shapely_box(0, 0, a, b)).rounded(p.outline_r).geometry
    if p.outline == "taper":
        return Polygon([(0, 0), (a, 0), (a, p.outline_r), (0, b)])
    if a < b:
        return slot_shape((a / 2, a / 2), (a / 2, b - a / 2), a).geometry
    return slot_shape((b / 2, b / 2), (a - b / 2, b / 2), b).geometry


def _local_shape(f: Feature) -> BaseGeometry:
    if f.b <= 0:
        return Point(f.p, f.q).buffer(f.a / 2, quad_segs=32)
    g = shapely_box(f.p - f.a / 2, f.q - f.b / 2, f.p + f.a / 2, f.q + f.b / 2)
    return affinity.rotate(g, f.angle, origin=(f.p, f.q)) if f.angle else g


def build(scene: Scene, pl: Placement, name: str = "m") -> Built:
    """The scene in a module (or cabinet) `name`, placed as `pl` says;
    LangError when the language refuses a plank's placement."""
    directions.set_frame(FRAMES[pl.frame])
    frame = directions.world_frame()
    bounds = _scene_bounds(scene.planks, [b for item in scene.items for body in item.bodies for b in body])
    lo: dict[Axis, float] = {}
    hi: dict[Axis, float] = {}
    for i in range(3):
        axis, a, b = _world(pl, i, (bounds[i][0] - scene.margins[2 * i], bounds[i][1] + scene.margins[2 * i + 1]))
        lo[axis], hi[axis] = a, b
    box = Box(lo, hi, frame)
    if pl.cabinet is not None:
        sideways = [d for d in frame.directions() if d.axis != frame.direction("top").axis]
        outer = cabinet(name, box, front=sideways[pl.cabinet % len(sideways)])
    else:
        outer = module(name, box)
    built = Built(outer, {}, {})
    with outer:
        sub = scope("sub")
        order = list(pl.order) if sorted(pl.order) == list(range(len(scene.planks))) else list(range(len(scene.planks)))
        for k in order:
            p = scene.planks[k]
            if p.sub:
                with sub:
                    built.boards[k], built.kept[k] = _build_plank(p, k, pl, built.refused)
            else:
                built.boards[k], built.kept[k] = _build_plank(p, k, pl, built.refused)
        items = list(enumerate(scene.items))
        for n, item in reversed(items) if pl.reversed_items else items:
            bodies: list[HardwareBodyLayout] = []
            for j, body in enumerate(item.bodies):
                boxes: list[BoxDict] = []
                for hb in body:
                    wlo, whi = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
                    for i in range(3):
                        axis, a, b = _world(pl, i, (hb.lo[i], hb.hi[i]))
                        wlo[AXES.index(axis)], whi[AXES.index(axis)] = a, b
                    boxes.append({"min": wlo, "max": whi})
                bodies.append({"name": f"b{j}", "boxes": boxes})
            holder = sub if item.sub else outer
            placed = holder.place_hardware(f"h{n}", bodies)
            for body_layout in placed["bodies"]:
                built.bodies[f"{placed['path']}.{body_layout['name']}"] = body_layout["boxes"]
    if scene.contour is not None:
        built.contour = inside(_contour(scene.contour, pl), gap=scene.contour.gap)
    return built


def _build_plank(p: Plank, k: int, pl: Placement, refused: dict[tuple[int, int], str]) -> tuple[Board, tuple[int, ...]]:
    t_axis, t_lo, _ = _world(pl, p.axis, p.range(p.axis))
    a, b = _others(p.axis)
    ua, ua0, ua1 = _world(pl, a, p.range(a))
    ub, ub0, ub1 = _world(pl, b, p.range(b))
    affine = _affine(pl, p, _plane(t_axis)[0])
    shape = _local_outline(p)
    stock = material("birch", t=p.t, sheet=p.sheet)
    x = board(f"p{k}", stock, None if shape is None else Shape(affinity.affine_transform(shape, affine)))
    up = directions.world_frame().direction_of(t_axis, 1)
    x.on(Pos(t_axis, t_lo), toward=up).between(Pos(ua, ua0), Pos(ua, ua1), Pos(ub, ub0), Pos(ub, ub1))
    x.box()
    kept: list[int] = []
    for n, f in enumerate(p.features):
        try:
            _apply(x, p, f, pl, affine, f"{f.kind}_{n}")
        except LangError as e:
            refused[(k, n)] = str(e)
            continue
        kept.append(n)
    if p.tab is not None:
        p0, q0, p1, q1 = p.tab
        x.add_to_outline(Shape(affinity.affine_transform(shapely_box(p0, q0, p1, q1), affine)))
    return x, tuple(kept)


def _apply(x: Board, p: Plank, f: Feature, pl: Placement, affine: list[float], name: str) -> None:
    sign = pl.signs[p.axis] * f.face
    face = x.face(directions.world_frame().direction_of(x.t_axis, sign))
    depth = through if f.depth is None else max(0.1, f.depth * p.t)
    if f.kind == "hole":
        a, b, d, e, du, dv = affine
        x.add_hole(face, (a * f.p + b * f.q + du, d * f.p + e * f.q + dv), f.a, depth, name)
    elif f.kind == "pocket":
        x.add_pocket(face, Shape(affinity.affine_transform(_local_shape(f), affine)), depth, name)
    elif f.kind in ("cut", "notch"):
        x.add_cut(Shape(affinity.affine_transform(_local_shape(f), affine)), name)
    elif f.kind == "vgroove":
        a, b, d, e, du, dv = affine
        end = (f.p + f.a * math.cos(math.radians(f.angle)), f.q + f.a * math.sin(math.radians(f.angle)))
        x.add_vgroove(face, (a * f.p + b * f.q + du, d * f.p + e * f.q + dv),
                      (a * end[0] + b * end[1] + du, d * end[0] + e * end[1] + dv), f.b, name)
    else:
        x.fillet(x.big_faces()[0].outline, f.a)


def _contour(c: ContourSpec, pl: Placement) -> Contour:
    """The contour spec as a master contour in world mm."""
    a, b = _others(c.axis)
    points: list[tuple[float, float, float]] = []
    for pa, pb in c.ring:
        w = [0.0, 0.0, 0.0]
        for i, v in ((c.axis, c.at), (a, pa), (b, pb)):
            axis, value, _ = _world(pl, i, (v, v))
            w[AXES.index(axis)] = value
        points.append((w[0], w[1], w[2]))
    normal = [0.0, 0.0, 0.0]
    normal[pl.perm[c.axis]] = 1.0
    return Contour("outline", tuple(points), True, points[0], (normal[0], normal[1], normal[2]))


# -- the truth ---------------------------------------------------------------------------------

Verdict = Literal["reported", "silent", "either"]


@dataclass(frozen=True)
class Truth:
    """What a check must say about a pair or a part: reported, silent or
    either (the overlap lies between touching and what must count); `what`
    says how deep, for the message; `known`, for one in between that the
    check leaves out, why that is known and open; `steady`, whether the
    check must say the same wherever the scene lies (not near its
    tolerances)."""
    verdict: Verdict
    what: str = ""
    known: str | None = None
    steady: bool = True


@dataclass
class _Solid:
    """A part as the truth reads it from the layout: its axes, box, outline
    (in its (u, v)) and the bands its pockets and holes take along its
    thickness, (from, to, the footprint with a hole's circle drawn inside
    it, and drawn around it)."""
    path: str
    t: Axis
    u: Axis
    v: Axis
    lo: dict[Axis, float]
    hi: dict[Axis, float]
    outline: BaseGeometry
    bands: list[tuple[float, float, BaseGeometry, BaseGeometry]]
    #: How far the circles drawn inside the holes lie inside them at most.
    sagitta: float = 0.0


def _rings_polygon(rings: list[list[list[float]]]) -> BaseGeometry:
    return unary_union([Polygon(piece[0], piece[1:]) for piece in pieces(rings)])


def _circle(u: float, v: float, r: float, around: bool, sides: int = _CIRCLE) -> Polygon:
    """A hole's circle as a polygon, its vertices on the circle (inside it)
    or its sides touching it (around it)."""
    angles = np.arange(sides) * (2 * math.pi / sides)
    rr = r / math.cos(math.pi / sides) if around else r
    return Polygon(np.column_stack([u + rr * np.cos(angles), v + rr * np.sin(angles)]))


def _solid(part: PartLayout, frame: LayoutFrame) -> _Solid:
    pf = PartFrame(part, frame)
    bands: list[tuple[float, float, BaseGeometry, BaseGeometry]] = []
    sagitta = 0.0
    for op in part["ops"]:
        if op["kind"] != "pocket" and op["kind"] != "hole":
            continue
        face = pf.face(op["face"])
        if not pf.is_big(face):
            continue                # (holes and pockets in narrow faces do not count yet, as documented)
        depth = min(op["depth"], pf.thickness)
        lo, hi = (face.value - depth, face.value) if face.sign > 0 else (face.value, face.value + depth)
        if op["kind"] == "pocket":
            g = _rings_polygon(op["shape"])
            bands.append((lo, hi, g, g))
        else:
            r = op["d"] / 2
            bands.append((lo, hi, _circle(op["u"], op["v"], r, False), _circle(op["u"], op["v"], r, True)))
            sagitta = max(sagitta, r * (1 - math.cos(math.pi / _CIRCLE)))
    return _Solid(part["path"], pf.t_axis, pf.u_axis, pf.v_axis, dict(pf.lo), dict(pf.hi),
                  _rings_polygon(part["outline"]), bands, sagitta)


def _prism(path: str, box: BoxDict, t: Axis) -> _Solid:
    """A hardware box as a solid along axis `t`."""
    lo: dict[Axis, float] = {a: box["min"][i] for i, a in enumerate(AXES)}
    hi: dict[Axis, float] = {a: box["max"][i] for i, a in enumerate(AXES)}
    u, v = _plane(t)
    return _Solid(path, t, u, v, lo, hi, shapely_box(lo[u], lo[v], hi[u], hi[v]), [])


def _plane(t: Axis) -> tuple[Axis, Axis]:
    """The two world axes across `t`, in x, y, z order (a board's u and v)."""
    others: list[Axis] = [a for a in AXES if a != t]
    return others[0], others[1]


def _extent(s: _Solid) -> tuple[dict[Axis, float], dict[Axis, float]]:
    """Where a solid's material lies: its thickness, and its outline's
    extent in its plane (which a tab may take past its box)."""
    u0, v0, u1, v1 = s.outline.bounds
    return {s.t: s.lo[s.t], s.u: u0, s.v: v0}, {s.t: s.hi[s.t], s.u: u1, s.v: v1}


def _apart(a: _Solid, b: _Solid) -> float:
    """How far apart two solids' extents lie at most along an axis
    (negative: by how much they overlap at least)."""
    (alo, ahi), (blo, bhi) = _extent(a), _extent(b)
    return max(max(alo[x], blo[x]) - min(ahi[x], bhi[x]) for x in AXES)


def _areas(g: BaseGeometry) -> BaseGeometry:
    """The polygons of a boolean's result, without its lines and points
    (GEOS fails on such collections in a further boolean)."""
    found = polygons_of(g)
    return found[0] if len(found) == 1 else unary_union(found) if found else Polygon()


def _at(s: _Solid, height: float, around: bool) -> BaseGeometry:
    """A solid's material at a height along its thickness, in its (u, v)."""
    gone = [band[3] if around else band[2] for band in s.bands if band[0] <= height <= band[1]]
    return _areas(s.outline.difference(unary_union(gone))) if gone else s.outline


def _wider(g: BaseGeometry, width: float) -> bool:
    """Whether a disc `width` across fits into a piece of `g`."""
    return any(not p.buffer(-width / 2, quad_segs=4).is_empty for p in polygons_of(g))


def _width(g: BaseGeometry) -> float:
    """How wide the widest piece of `g` is on average, as `clean` measures
    it (twice its area over its length), mm."""
    return max((2 * p.area / p.length for p in polygons_of(g) if p.length > 0), default=0.0)


def _in_one_plane(a: _Solid, b: _Solid, window: BaseGeometry | None = None) -> Truth:
    """Two solids in one plane (or a part and a box), slab by slab between
    the ends of their pockets' and holes' bands: an overlap at least
    `ACROSS` thick and `WIDE` wide is reported, one no thicker than `TOUCH`
    or narrower than that (and the holes' sagitta) is not."""
    t = a.t
    t0, t1 = max(a.lo[t], b.lo[t]), min(a.hi[t], b.hi[t])
    if t1 - t0 <= TOUCH or _apart(a, b) >= -TOUCH:
        return Truth("silent")
    ends = sorted({t0, t1} | {e for s in (a, b) for band in s.bands for e in band[:2] if t0 < e < t1})
    narrow = TOUCH + 2 * max(a.sagitta, b.sagitta)
    reported, silent, thin, wide, some = False, True, math.inf, False, False
    shared: list[BaseGeometry] = []
    for s0, s1 in zip(ends, ends[1:]):
        mid = (s0 + s1) / 2
        less = _areas(_at(a, mid, True).intersection(_at(b, mid, True)))
        more = _areas(_at(a, mid, False).intersection(_at(b, mid, False)))
        if window is not None:
            less, more = _areas(less.intersection(window)), _areas(more.intersection(window))
        if s1 - s0 > TOUCH and _wider(more, narrow):
            silent = False
            thin = min(thin, s1 - s0)
            shared.append(more)
            wide = wide or _wider(more, 0.009)
            some = some or _wider(more, 1e-4)
        if s1 - s0 >= ACROSS and _wider(less, WIDE):
            reported = True
    what = f"{t1 - t0:.3g} thick, {max((_width(g) for g in shared), default=0.0):.3g} wide on average"
    if reported:
        return Truth("reported", what)
    if silent:
        return Truth("silent")
    # (between: steady when the overlap is thick enough not to be near the checks' 1e-6, and
    # narrow enough in the plane that `clean` takes it out wherever it lies)
    known = None
    if thin >= 1e-4 and some:
        known = (f"{KNOWN} an overlap {what} in the boards' plane is not reported: `clean` takes out what is "
                 "narrower than 0.01 mm there, though an overlap as thin across the thickness is reported "
                 "(2026-10-14, open)")
    return Truth("either", what, known, thin >= 1e-4 and not wide)


def _box_window(a: _Solid, b: _Solid) -> BaseGeometry:
    """Where the two placement boxes overlap, in `a`'s (u, v)."""
    u0, v0 = max(a.lo[a.u], b.lo[a.u]), max(a.lo[a.v], b.lo[a.v])
    u1, v1 = min(a.hi[a.u], b.hi[a.u]), min(a.hi[a.v], b.hi[a.v])
    return shapely_box(u0, v0, u1, v1) if u1 > u0 and v1 > v0 else Polygon()


def _parallel_truth(a: _Solid, b: _Solid) -> Truth:
    truth = _in_one_plane(a, b)
    if truth.verdict == "reported" and _in_one_plane(a, b, _box_window(a, b)).verdict != "reported":
        return Truth("either", truth.what, _GROWTH, False)
    return truth


#: Material a part has outside its placement box, as a joint's tenons:
#: the checks look at it within the box only (DESIGN.md, the drawer
#: cabinet's floors; 2026-10-14, open).
_GROWTH = f"{KNOWN} the overlap lies outside the placement boxes, which the checks do not look past (open)"


def _bodies_truth(boxes_a: list[_Solid], boxes_b: list[_Solid]) -> Truth:
    """Two hardware bodies: boxes overlapping `ACROSS` deep on every axis
    are reported, boxes touching or apart are not."""
    depth = max(min(min(p.hi[x], q.hi[x]) - max(p.lo[x], q.lo[x]) for x in AXES) for p in boxes_a for q in boxes_b)
    if depth >= ACROSS:
        return Truth("reported", f"{depth:.3g} deep")
    if depth <= TOUCH:
        return Truth("silent")
    return Truth("either", f"{depth:.3g} deep", steady=False)


def _body_part_truth(boxes: list[BoxDict], path: str, part: _Solid) -> Truth:
    """A hardware body and a part: reported where one of its boxes must be,
    silent where all must be, else either, steady where every box's
    verdict is."""
    truths = [_parallel_truth(part, _prism(path, box, part.t)) for box in boxes]
    reported = [t for t in truths if t.verdict == "reported"]
    if reported:
        return reported[0]
    between = [t for t in truths if t.verdict == "either"]
    if not between:
        return Truth("silent")
    known = next((t.known for t in between if t.known is not None), None)
    return Truth("either", between[0].what, known, all(t.steady for t in between))


def _hole_pockets(part: PartLayout, around: bool) -> PartLayout:
    """The part with its holes as pockets of circles drawn inside or around
    them (the meshes draw holes with 24 sides), and no other operations:
    the checks do not count V-grooves, chamfers or what lies in narrow
    faces, as documented."""
    ops: list[OpLayout] = []
    for op in part["ops"]:
        if op["kind"] == "pocket":
            ops.append({**op, "chamfer": 0.0})
        elif op["kind"] == "hole":
            circle = _circle(op["u"], op["v"], op["d"] / 2, around, _MESH_CIRCLE)
            ring = [[float(x), float(y)] for x, y in circle.exterior.coords[:-1]]
            ops.append({"kind": "pocket", "name": op["name"], "face": op["face"], "depth": op["depth"],
                        "depth_spec": op["depth_spec"], "chamfer": 0.0, "shape": [ring]})
    out = part.copy()
    out["ops"] = ops
    return out


def _shared(a: Any, b: Any, region: Any = None) -> list[tuple[float, float]]:
    """The pieces two meshes share: each one's volume and thickness (its
    volume over the largest face of the box around it)."""
    import warnings
    import trimesh
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        common = trimesh.boolean.intersection([a, b] + ([region] if region is not None else []), engine="manifold")
        if not len(common.faces):
            return []
        out: list[tuple[float, float]] = []
        for piece in common.split(only_watertight=False):
            e = sorted(float(x) for x in piece.extents)
            out.append((abs(float(piece.volume)), abs(float(piece.volume)) / max(e[1] * e[2], 1e-300)))
        return out


class _Meshes:
    """The parts' preview meshes, made when first needed: holes drawn
    inside their circles (`more` material) or around them."""

    def __init__(self, parts: dict[str, PartLayout], frame: dict[str, str]):
        self.parts, self.frame = parts, frame
        self.made: dict[tuple[str, bool], Any] = {}

    def get(self, path: str, around: bool) -> Any:
        key = (path, around)
        if key not in self.made:
            self.made[key] = mesh_part(_hole_pockets(self.parts[path], around), self.frame, lambda _: None)
        return self.made[key]


def _across_truth(a: _Solid, b: _Solid, meshes: _Meshes) -> Truth:
    """Two parts across each other, from their meshes: a shared piece
    `WIDE` thick is reported (each part's thickness lies in the other's
    plane, so `clean` may take out anything thinner), one no thicker than
    the booleans' film is not."""
    if _apart(a, b) >= -TOUCH:
        return Truth("silent")
    more = (meshes.get(a.path, False), meshes.get(b.path, False))
    fewer = (meshes.get(a.path, True), meshes.get(b.path, True))
    if any(m is None or not m.is_volume for m in more + fewer):
        return Truth("either", "unmeshed", steady=False)
    shared = _shared(more[0], more[1])
    thickest = max((th for _, th in shared), default=0.0)
    if thickest <= FILM:
        return Truth("silent")
    less = _shared(fewer[0], fewer[1])
    if max((th for _, th in less), default=0.0) >= WIDE:
        what = f"{max(v for v, _ in less):.3g} mm3, {thickest:.3g} thick"
        import trimesh
        lo = [max(a.lo[x], b.lo[x]) for x in AXES]
        hi = [min(a.hi[x], b.hi[x]) for x in AXES]
        if any(h - l <= 0 for l, h in zip(lo, hi)):
            return Truth("either", what, _GROWTH, False)
        region = trimesh.creation.box(extents=[h - l for l, h in zip(lo, hi)])
        region.apply_translation([(l + h) / 2 for l, h in zip(lo, hi)])
        inside_boxes = _shared(fewer[0], fewer[1], region)
        if max((th for _, th in inside_boxes), default=0.0) < WIDE:
            return Truth("either", what, _GROWTH, False)
        return Truth("reported", what)
    known = None
    if thickest >= 1e-3:
        known = (f"{KNOWN} an overlap {thickest:.2g} mm thick of boards across each other is not reported: in "
                 "one board's plane it is narrower than the 0.01 mm `clean` keeps (2026-10-14, open)")
    return Truth("either", f"{thickest:.3g} thick", known, False)


# -- judging a build ---------------------------------------------------------------------------

@dataclass
class Judged:
    """A build's problems, what each check said and what the truth is, by
    key (`interference <path> <path>`, `box p<k> <axis> <side>`, `sheet
    p<k>`, `contour p<k>`), and the features each plank kept."""
    problems: list[str]
    said: dict[str, bool]
    truths: dict[str, Truth]
    kept: dict[int, tuple[int, ...]]
    refused: dict[tuple[int, int], str] = field(default_factory=dict[tuple[int, int], str])


def _compare(key: str, said: bool, truth: Truth, what: str) -> list[str]:
    if truth.verdict == "reported" and not said:
        return [f"{what} is not reported ({truth.what}) [{key}]"]
    if truth.verdict == "silent" and said:
        return [f"{what} is reported, though {_none(key)} [{key}]"]
    if truth.verdict == "either" and not said and truth.known is not None:
        return [f"{truth.known} [{key}]"]
    return []


def _none(key: str) -> str:
    return {"interference": "they only touch or lie apart", "box": "the part is inside the box",
            "sheet": "the part fits the sheet", "contour": "the part is inside the contour"}[key.split()[0]]


def judge(scene: Scene, pl: Placement, built: Built) -> Judged:
    """What is wrong with the checks' verdicts on one build."""
    frame = {d.name: d.code for d in directions.world_frame().directions()}
    parts = {b.path: b.to_layout() for b in built.boards.values()}
    said: dict[str, bool] = {}
    truths: dict[str, Truth] = {}
    problems: list[str] = []

    def record(key: str, verdict: bool, truth: Truth, what: str) -> None:
        said[key], truths[key] = verdict, truth
        problems.extend(_compare(key, verdict, truth, what))

    # no_interference: every pair of parts, of a body and a part, of two bodies
    reported: set[frozenset[str]] = set()
    for line in no_interference(built.scope):
        m = re.fullmatch(r"(\S+) overlaps (\S+)", line)
        if m is None:
            problems.append(f"no_interference says {line!r}")
            continue
        reported.add(frozenset((m.group(1), m.group(2))))
    solids = {p: _solid(part, LayoutFrame(frame)) for p, part in parts.items()}
    meshes = _Meshes(parts, frame)
    pairs: dict[frozenset[str], Truth] = {}
    paths = sorted(solids)
    for i, p in enumerate(paths):
        for q in paths[i + 1:]:
            a, b = solids[p], solids[q]
            pairs[frozenset((p, q))] = _parallel_truth(a, b) if a.t == b.t else _across_truth(a, b, meshes)
    bodies = sorted(built.bodies)
    for body in bodies:
        for p in paths:
            pairs[frozenset((body, p))] = _body_part_truth(built.bodies[body], body, solids[p])
    for i, body in enumerate(bodies):
        for other in bodies[i + 1:]:
            pairs[frozenset((body, other))] = _bodies_truth([_prism(body, x, "z") for x in built.bodies[body]],
                                                            [_prism(other, x, "z") for x in built.bodies[other]])
    for pair in reported - pairs.keys():
        problems.append(f"no_interference names a pair that is none: {sorted(pair)}")
    for pair, truth in pairs.items():
        record("interference " + " ".join(sorted(pair)), pair in reported, truth, " and ".join(sorted(pair)))

    # inside_box: each part's overhang past the module's box, by scene axis and side
    out: dict[str, float] = {}
    for line in inside_box(built.scope):
        m = re.fullmatch(r"(\S+) reaches out of (\S+)'s box: (.*)", line)
        if m is None:
            problems.append(f"inside_box says {line!r}")
            continue
        for item in m.group(3).split(", "):
            name, _, amount = item.partition(" by ")
            d = built.scope.frame.direction(name)
            i = pl.perm.index(AXES.index(d.axis))
            out[f"box {m.group(1)} {i} {d.sign * pl.signs[i]:+d}"] = float(amount)
    bounds = _scene_bounds(scene.planks, [x for item in scene.items for body in item.bodies for x in body])
    for k, x in built.boards.items():
        p = scene.planks[k]
        tab = _tab_ranges(p)
        for i in range(3):
            for side in (-1, 1):
                edge = bounds[i][0] - scene.margins[2 * i] if side < 0 else bounds[i][1] + scene.margins[2 * i + 1]
                reach = p.range(i)[0] if side < 0 else p.range(i)[1]
                amount = side * (reach - edge)
                key = f"box {x.path} {i} {side:+d}"
                truth = _amount_truth(amount)
                if tab is not None and truth.verdict != "reported" and i in tab:
                    with_tab = side * ((min if side < 0 else max)(reach, tab[i][0 if side < 0 else 1]) - edge)
                    if _amount_truth(with_tab).verdict == "reported":
                        truth = Truth("either", f"{with_tab:.3g}", _GROWTH, False)
                record(key, key in out, truth, f"{x.path} reaching out of the box ({amount:.3g} {i}{side:+d})")
                if key in out and truth.verdict == "reported" and abs(out[key] - amount) > max(1e-5 * amount, 1e-5):
                    problems.append(f"inside_box says {x.path} reaches out by {out[key]:g}, it is {amount:.6g} [{key}]")
    for key in out.keys() - truths.keys():
        problems.append(f"inside_box names a side that is none: {key}")

    # fits_sheet: the outline's extent in either orientation, as drawn (a rounded acute
    # corner, of a taper, lowers it: then as built, give or take the tolerance)
    unfit = {line.split(" (")[0] for line in fits_sheet(built.scope)}
    for k, x in built.boards.items():
        p = scene.planks[k]
        if p.sheet is None:
            continue
        exact = p.outline != "taper" or not any(p.features[n].kind == "fillet" for n in built.kept[k])
        if exact:
            local = _local_outline(p) or shapely_box(0, 0, p.hi[0] - p.lo[0], p.hi[1] - p.lo[1])
            if p.tab is not None:
                local = local.union(shapely_box(*p.tab))
            u0, v0, u1, v1 = local.bounds
            w, h = u1 - u0, v1 - v0
        else:
            w, h = x.outline.width, x.outline.height
        W, H = p.sheet
        margin = max(min(W - w, H - h), min(H - w, W - h))
        if margin >= (0 if exact else ACROSS):
            truth = Truth("silent")
        elif margin <= -ACROSS:
            truth = Truth("reported", f"{-margin:.3g} too large")
        else:
            truth = Truth("either", steady=False)
        record(f"sheet {x.path}", x.path in unfit, truth,
               f"{x.path} ({w:.6g} x {h:.6g} on {W:.6g} x {H:.6g}) not fitting")

    # inside(contour): the shadows along the contour's normal
    if built.contour is not None and scene.contour is not None:
        outside = {line.split(" is not inside")[0] for line in built.contour(built.scope)}
        contour = _contour(scene.contour, pl)
        n = contour.normal_axis
        a, b = _plane(n)
        allowed = contour.polygon(a, b)
        if scene.contour.gap:
            allowed = allowed.buffer(-scene.contour.gap, join_style="mitre")
        for k, x in built.boards.items():
            s = solids[x.path]
            truth = _shadow_truth(s, n, a, b, allowed)
            record(f"contour {x.path}", x.path in outside, truth, f"{x.path} outside the contour")
    return Judged(problems, said, truths, dict(built.kept), dict(built.refused))


def _amount_truth(amount: float) -> Truth:
    if amount >= ACROSS:
        return Truth("reported", f"{amount:.3g}")
    if amount <= TOUCH:
        return Truth("silent")
    return Truth("either", f"{amount:.3g}", steady=False)


def _tab_ranges(p: Plank) -> dict[int, Range] | None:
    """A plank's tab as ranges on its two in-plane scene axes."""
    if p.tab is None:
        return None
    a, b = _others(p.axis)
    p0, q0, p1, q1 = p.tab
    return {a: (p.lo[0] + p0, p.lo[0] + p1), b: (p.lo[1] + q0, p.lo[1] + q1)}


def _shadow_truth(s: _Solid, n: Axis, a: Axis, b: Axis, allowed: BaseGeometry) -> Truth:
    """A part's shadow against the allowed area: its outline in the
    contour's plane, its box across it (as `inside()` documents), or past
    its box by a tab (known)."""
    if s.t == n:
        shadow = s.outline
        grown = None
    else:
        shadow = shapely_box(s.lo[a], s.lo[b], s.hi[a], s.hi[b])
        (lo, hi) = _extent(s)
        grown = shapely_box(lo[a], lo[b], hi[a], hi[b])
    off = _areas(shadow.difference(allowed))
    if _wider(off, WIDE):
        return Truth("reported", f"{_width(off):.3g} out, {off.area:.3g} mm2")
    if grown is not None and _wider(_areas(grown.difference(allowed)), WIDE):
        return Truth("either", "past its box", _GROWTH, False)
    if not _wider(off, TOUCH):
        return Truth("silent")
    return Truth("either", f"{_width(off):.3g} out", steady=_width(off) >= 1e-4 and not 0.5e-6 <= off.area <= 2e-6)


# -- the case ---------------------------------------------------------------------------------

def _attempt(scene: Scene, pl: Placement) -> Judged | None:
    """The scene built at one placement and judged; None when the
    language refuses to build it (a plank's placement)."""
    with fresh():
        try:
            built = build(scene, pl)
        except LangError:
            return None
        return judge(scene, pl, built)


def run_case(scene: Scene) -> list[str]:
    """What is wrong with the checks on the scene, built at both its
    placements: each build's verdicts against its truth, and the steady
    verdicts of the two against each other."""
    try:
        first, second = _attempt(scene, scene.places[0]), _attempt(scene, scene.places[1])
    except Exception as e:
        frame = next((fr for fr in reversed(traceback.extract_tb(e.__traceback__))
                      if "/lang/" in fr.filename), traceback.extract_tb(e.__traceback__)[-1])
        return [f"{type(e).__name__} at {Path(frame.filename).name}:{frame.lineno}: {e}"]
    if first is None or second is None:
        return [] if first is None and second is None else ["the scene is refused at one placement only"]
    problems = first.problems + [p for p in second.problems if p not in first.problems]
    if first.kept != second.kept:
        differ = sorted(first.refused.keys() ^ second.refused.keys())
        why = "; ".join(first.refused.get(key) or second.refused.get(key) or "" for key in differ)
        return problems + [f"placed otherwise, the planks keep other features: {first.kept} against {second.kept} "
                           f"({why})"]
    for key in sorted(first.said.keys() & second.said.keys()):
        one, two = first.truths[key], second.truths[key]
        if one.verdict != "either" and two.verdict != "either" and one.verdict != two.verdict:
            problems.append(f"placed otherwise, the truth is {two.verdict} instead of {one.verdict} [{key}]")
        elif one.steady and two.steady and first.said[key] != second.said[key]:
            problems.append(f"placed otherwise, the verdict is {second.said[key]} instead of {first.said[key]} "
                            f"({one.what}) [{key}]")
    return problems


__all__ = ["Scene", "run_case", "scenes", "build", "judge"]
