"""Checks that run on the layout, before any geometry exists."""
from __future__ import annotations

import math
from functools import cache
from typing import TYPE_CHECKING

from shapely import affinity
from shapely.geometry import MultiPolygon, Point
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry

from . import directions
from .box import Box
from .contours import Contour, footprint, round_offset
from .directions import AXES, Axis
from .errors import LangError
from .geometry import polygons_of
from .ops import Hole, Pocket
from .scope import Check, Scope

if TYPE_CHECKING:
    from .part import Board


def no_interference(scope: Scope) -> list[str]:
    """Parts and hardware in the scope (and below) whose material overlaps:
    pairs of parts, a hardware body and a part, and two hardware bodies.

    An overlap counts where it is deeper than 1e-6 mm in every direction,
    in a board's plane as across its thickness; touching, within 1e-6 mm,
    does not [decided by Florian, 2026-10-14: the material was cleaned
    first, which took out overlaps narrower than 0.01 mm in a board's plane
    while ones as thin across the thickness counted]. A part's material is
    its outline through its thickness minus its pockets and holes, so a
    floor sitting in a groove does not count, nor a latch sitting in its
    hole. Where pockets and holes reach only part of the way through, the
    material is looked at slab by slab between their ends, so a pocket from
    one face and a hole from the other that make room only together count
    too [found by fuzzing, 2026-10-14: they did only where one of them
    spanned all of the range in question]. Parallel parts must have
    material in the same place, so a hatch in a rounded opening, whose box
    reaches into the opening's corners, does not count. Perpendicular parts
    must also pass through each other, as `crossing` has it but slab by
    slab: along the axis both their planes contain, the stretches where
    each has material must overlap, so two lapped battens, each filling
    half of the box they share, do not count either, nor a divider standing
    in a groove whose end is notched clear of the material beside it. A
    hardware body is the union of its boxes (`Scope.place_hardware`): it
    overlaps a part where one of its boxes reaches into the part's
    material, and another body where two of their boxes overlap; the boxes
    of one body may overlap each other. Material a part has outside its
    placement box (tenons, a box joint's fingers) is not looked at, nor
    pockets and holes in narrow faces, yet."""
    parts = scope.all_parts()
    problems: list[str] = []
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            if a.box().overlaps(b.box()) and _parts_meet(a, b, a.box().intersection(b.box())):
                problems.append(f"{a.path} overlaps {b.path}")
    bodies = _hardware_bodies(scope)
    for path, boxes in bodies:
        for part in parts:
            if any(_box_hits(part, box) for box in boxes):
                problems.append(f"{path} overlaps {part.path}")
    for i, (path_a, boxes_a) in enumerate(bodies):
        for path_b, boxes_b in bodies[i + 1:]:
            if any(a.overlaps(b) for a in boxes_a for b in boxes_b):
                problems.append(f"{path_a} overlaps {path_b}")
    return problems


#: How deep (mm) material must overlap, in every direction, to count;
#: boxes overlap by more than this along each axis (`Box.overlaps`).
_TOLERANCE = 1e-6


def _hardware_bodies(scope: Scope) -> list[tuple[str, list[Box]]]:
    """Every hardware body in the scope and below, by its path
    (`<item path>.<body name>`), with its boxes."""
    return [(f"{item['path']}.{body['name']}",
             [Box(dict(zip(AXES, b["min"])), dict(zip(AXES, b["max"])), scope.frame) for b in body["boxes"]])
            for item in scope.all_hardware() for body in item["bodies"]]


def _parts_meet(a: Board, b: Board, region: Box) -> bool:
    """Whether two parts have material in one place within `region`,
    deeper than the tolerance every way."""
    if a.t_axis == b.t_axis:
        return any(_deep(_material(a, slab).intersection(_material(b, slab)))
                   for slab in _slabs(region, a.t_axis, a, b))
    axis: Axis = next(x for x in AXES if x not in (a.t_axis, b.t_axis))
    for slab in _slabs(region, a.t_axis, a):
        for cell in _slabs(slab, b.t_axis, b):
            spans_a, spans_b = _spans(a, cell, axis), _spans(b, cell, axis)
            # (each part's material shrunk by half the tolerance: where both stretches meet, the
            # two have a cube of the tolerance in common)
            if any(min(p[1], q[1]) >= max(p[0], q[0]) for p in spans_a for q in spans_b):
                return True
    return False


def _spans(part: Board, region: Box, axis: Axis) -> list[tuple[float, float]]:
    """The stretches along `axis` (one of the part's in-plane axes) where
    the part has material within `region` deeper than half the tolerance
    every way in its plane."""
    i = 0 if axis == part.u_axis else 1
    return [(float(g.bounds[i]), float(g.bounds[i + 2])) for g in polygons_of(_shrunk(_material(part, region)))]


def _box_hits(part: Board, box: Box) -> bool:
    """Whether a box reaches into the part's material."""
    b = part.box()
    return box.overlaps(b) and _has_material(part, box.intersection(b))


def _has_material(part: Board, region: Box) -> bool:
    """Whether the part has material within `region`, slab by slab, deeper
    than the tolerance in its plane."""
    return any(_deep(_material(part, slab)) for slab in _slabs(region, part.t_axis, part))


def _shrunk(g: BaseGeometry) -> BaseGeometry:
    """`g` shrunk by half the tolerance: what is left is where a disc as
    wide as the tolerance fits."""
    return g.buffer(-_TOLERANCE / 2) if not g.is_empty else g


def _deep(g: BaseGeometry) -> bool:
    """Whether a disc as wide as the tolerance fits into `g`."""
    return any(not _shrunk(p).is_empty for p in polygons_of(g))


def _bands(part: Board) -> list[tuple[float, float, Pocket | Hole]]:
    """The part's pockets and holes in its big faces, each with the range
    it takes along the thickness."""
    b = part.box()
    t = part.t_axis
    out: list[tuple[float, float, Pocket | Hole]] = []
    for op in part.ops:
        if isinstance(op, (Pocket, Hole)):
            face = directions.frame.direction(op.face)
            lo, hi = (b.hi[t] - op.depth, b.hi[t]) if face.sign > 0 else (b.lo[t], b.lo[t] + op.depth)
            out.append((lo, hi, op))
    return out


def _slabs(region: Box, axis: Axis, *parts: Board) -> list[Box]:
    """`region` cut along `axis` where a pocket or hole of the parts ends
    (parts lying across that axis), into slabs thicker than the tolerance:
    each pocket or hole spans a slab or misses it."""
    lo, hi = region.lo[axis], region.hi[axis]
    ends = sorted({e for part in parts if part.t_axis == axis for band in _bands(part) for e in band[:2]
                   if lo < e < hi})
    cuts = [lo]
    for e in ends:
        if e - cuts[-1] > _TOLERANCE and hi - e > _TOLERANCE:
            cuts.append(e)
    cuts.append(hi)
    return [Box({**region.lo, axis: s0}, {**region.hi, axis: s1}, region.frame) for s0, s1 in zip(cuts, cuts[1:])]


def _material(part: Board, region: Box) -> BaseGeometry:
    """The part's material inside `region`, seen along its thickness: the
    outline within the region, minus the pockets and holes deep enough to
    span the region's range along the thickness axis. As the booleans
    leave it, not cleaned: what is narrower than 0.01 mm counts here, and
    `_deep` judges it."""
    b = part.box()
    t, u, v = part.t_axis, part.u_axis, part.v_axis
    window = shapely_box(region.lo[u], region.lo[v], region.hi[u], region.hi[v])
    # (its areas only: a window in a notch of the outline, touching it along the notch's edge,
    # meets it in a line [found by fuzzing the placement, 2026-10-14: "Shape is not an area"])
    material = _areas(part.outline.geometry.intersection(window))
    t0, t1 = max(region.lo[t], b.lo[t]), min(region.hi[t], b.hi[t])
    for lo, hi, op in _bands(part):
        if lo <= t0 + _TOLERANCE and t1 <= hi + _TOLERANCE:
            gone = op.shape.geometry if isinstance(op, Pocket) else _hole_shape(op)
            if gone.intersects(window):
                material = _areas(material.difference(gone))
    return material


def _areas(g: BaseGeometry) -> BaseGeometry:
    """The polygons of a boolean's result, without its lines and points."""
    found = polygons_of(g)
    return found[0] if len(found) == 1 else MultiPolygon(found)


def _hole_shape(hole: Hole) -> BaseGeometry:
    """A hole's circle as a polygon whose sides touch the circle from
    outside, so a box in the hole with its corners on the circle does not
    hit the slivers of material a polygon inside the circle would leave;
    with so many sides that it takes no more than a quarter of the
    tolerance beyond the circle [found by fuzzing, 2026-10-14: with 64
    sides, 0.06 mm around a 100 mm hole, and a box reaching that far past
    the circle did not count; a side a degree, 3.8e-5 r, until overlaps
    of 1e-6 counted]."""
    return _circle_around(hole.u, hole.v, hole.d / 2)


@cache
def _circle_around(u: float, v: float, r: float) -> BaseGeometry:
    quarter = math.ceil(math.pi / math.acos(1 / (1 + _TOLERANCE / 4 / r)) / 4)
    n = 4 * min(quarter, _MOST_SEGMENTS)
    return Point(u, v).buffer(r / math.cos(math.pi / n), quad_segs=n // 4)


#: Segments a quarter at most for a hole's circle: holes up to 430 mm
#: across stay within the tolerance.
_MOST_SEGMENTS = 8192


def fits_sheet(scope: Scope) -> list[str]:
    """Parts whose outline does not fit their material's sheet, either way
    round. A part as large as its sheet fits, give or take 1e-6 mm: its
    extent is a difference of world coordinates, which far from the origin
    comes out a little larger [found by fuzzing, 2026-10-14: a part from
    -1219.9 to -976.9 is 243.0000000000001 high]."""
    problems: list[str] = []
    for part in scope.all_parts():
        sheet = part.material.sheet
        if sheet is None:
            continue
        w, h = part.outline.width, part.outline.height
        a, b = w - _TOLERANCE, h - _TOLERANCE
        if not ((a <= sheet[0] and b <= sheet[1]) or (a <= sheet[1] and b <= sheet[0])):
            problems.append(f"{part.path} ({w:g} x {h:g}) does not fit a {sheet[0]:g} x {sheet[1]:g} sheet")
    return problems


def inside_box(scope: Scope) -> list[str]:
    """Parts that reach out of the scope's box, e.g. a module's parts out of
    the placeholder box it stands in, by where their material lies
    (`_extent`)."""
    box = scope.box
    if box is None:
        return []
    problems: list[str] = []
    for part in scope.all_parts():
        b = _extent(part)
        out = [f"{name} by {amount:g}" for name, amount in _overhang(b, box) if amount > _TOLERANCE]
        if out:
            problems.append(f"{part.path} reaches out of {scope.path}'s box: {', '.join(out)}")
    return problems


def _extent(part: Board) -> Box:
    """Where a part's material lies: its outline's extent in its plane and
    its thickness. Joints take the outline past the placement box (tenons,
    a box joint's fingers, a floor grown into its grooves), and a cut
    across an end stops it short of it [decided by Florian, 2026-10-14:
    `inside_box` and `inside()` took the placement box]."""
    b = part.box()
    lo, hi = dict(b.lo), dict(b.hi)
    lo[part.u_axis], lo[part.v_axis], hi[part.u_axis], hi[part.v_axis] = part.outline.bounds
    return Box(lo, hi, b.frame)


def _overhang(part: Box, box: Box) -> list[tuple[str, float]]:
    out: list[tuple[str, float]] = []
    for axis in AXES:
        low, high = box.frame.direction_of(axis, -1).name, box.frame.direction_of(axis, 1).name
        out.append((low, box.lo[axis] - part.lo[axis]))
        out.append((high, part.hi[axis] - box.hi[axis]))
    return out


def inside(contour: Contour, gap: float = 0.0) -> Check:
    """A check that the scope's parts stay inside a closed contour, seen
    along its plane's normal (a plan-view outline from above), with at
    least `gap` of clearance: `check(inside(van.contour("Bodenumriss"),
    gap=5))`. A part in the contour's plane is taken by its outline, any
    other by where its material lies (`_extent`: its outline's extent,
    past its placement box where a joint grew it [decided by Florian,
    2026-10-14], and its thickness). A part may reach 1e-6 mm past the
    contour (or into the clearance), the tolerance of the other checks,
    measured as a distance [found by fuzzing, 2026-10-14: by area, a
    board 1627 long 1e-9 into the clearance was outside]; anything further
    out counts, however little its area, as an overlap that deep does in
    `no_interference` [decided by Florian, 2026-10-14: a corner 1e-4 past
    the contour, 5e-9 mm2, was inside]."""
    if not contour.closed:
        raise LangError(f"inside(): contour {contour.name!r} is open; the check needs a closed one.")
    n = contour.normal_axis
    others: list[Axis] = [a for a in AXES if a != n]
    offsets: dict[tuple[Axis, Axis], BaseGeometry] = {}

    def allowed_for(part: Board) -> BaseGeometry:
        """The clearance offset as `between()` offsets it for this part, the
        same call in the same axis order, so the two agree however GEOS
        simplifies it (a mirrored area simplifies otherwise, a hundredth of
        the gap [found by fuzzing, 2026-10-14]), with the tolerance, in x,
        y, z order."""
        order: tuple[Axis, Axis] = (others[0], others[1])
        if part.t_axis != n:
            s: Axis = next(x for x in others if x != part.t_axis)
            order = (part.t_axis, s)
        if order not in offsets:
            grown = round_offset(contour.polygon(*order), -gap).buffer(_TOLERANCE)
            offsets[order] = grown if order == (others[0], others[1]) else \
                affinity.affine_transform(grown, [0, 1, 1, 0, 0, 0])
        return offsets[order]

    def check(scope: Scope) -> list[str]:
        problems: list[str] = []
        for part in scope.all_parts():
            allowed = allowed_for(part)
            extent = _extent(part)
            if part.t_axis != n:
                # (across the contour, as `between()` holds it: from just inside its faces, where
                # a steep contour edge lets the faces themselves reach a little further)
                extent = Box({**extent.lo, part.t_axis: extent.lo[part.t_axis] + _TOLERANCE},
                             {**extent.hi, part.t_axis: extent.hi[part.t_axis] - _TOLERANCE}, extent.frame)
            shadow = footprint(extent, part.outline, part.t_axis, n)
            outside = shadow.difference(allowed)
            if outside.is_empty:
                continue
            # (how far past the tolerance it reaches, which a rounding along the edge leaves at 0;
            # all of it where the clearance leaves nothing of the contour)
            beyond = math.inf if allowed.is_empty else max(
                (allowed.distance(Point(c)) for g in polygons_of(outside) for c in g.exterior.coords), default=0.0)
            if beyond > 1e-9:
                how = "the clearance leaves nothing" if allowed.is_empty else f"{_TOLERANCE + beyond:.3g} mm out"
                clearance = f" with {gap:g} mm clearance" if gap else ""
                problems.append(f"{part.path} is not inside {contour.name}{clearance} "
                                f"({how}, {outside.area:.3g} mm² outside)")
        return problems

    check.__name__ = f"inside({contour.name})"
    return check
