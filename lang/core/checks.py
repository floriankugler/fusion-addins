"""Checks that run on the layout, before any geometry exists."""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

from shapely.geometry import Point
from shapely.geometry import box as shapely_box

from . import directions
from .box import Box
from .contours import Contour, footprint
from .directions import AXES, Axis
from .errors import LangError
from .ops import Hole, Pocket
from .scope import Check, Scope
from .shapes import Shape

if TYPE_CHECKING:
    from .part import Board


def no_interference(scope: Scope) -> list[str]:
    """Parts and hardware in the scope (and below) whose material overlaps:
    pairs of parts, a hardware body and a part, and two hardware bodies.

    A part's material is its outline through its thickness minus its
    pockets and holes, so a floor sitting in a groove does not count, nor
    a latch sitting in its hole. Where pockets and holes reach only part of
    the way through, the material is looked at slab by slab between their
    ends, so a pocket from one face and a hole from the other that make
    room only together count too [found by fuzzing, 2026-10-14: they did
    only where one of them spanned all of the range in question]. Parallel
    parts must have material in the same place, so a hatch in a rounded
    opening, whose box reaches into the opening's corners, does not count.
    Perpendicular parts must also pass through each other, as `crossing`
    has it but slab by slab: along the axis both their planes contain, the
    stretches where each has material must overlap, so two lapped battens,
    each filling half of the box they share, do not count either, nor a
    divider standing in a groove whose end is notched clear of the
    material beside it. A hardware body is the union of its boxes
    (`Scope.place_hardware`): it overlaps a part where one of its boxes
    reaches into the part's material, and another body where two of their
    boxes overlap; the boxes of one body may overlap each other. Touching
    is not overlapping. Pockets and holes in narrow faces are not taken
    into account yet."""
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


_TOLERANCE = 1e-6


def _hardware_bodies(scope: Scope) -> list[tuple[str, list[Box]]]:
    """Every hardware body in the scope and below, by its path
    (`<item path>.<body name>`), with its boxes."""
    return [(f"{item['path']}.{body['name']}",
             [Box(dict(zip(AXES, b["min"])), dict(zip(AXES, b["max"])), scope.frame) for b in body["boxes"]])
            for item in scope.all_hardware() for body in item["bodies"]]


def _parts_meet(a: Board, b: Board, region: Box) -> bool:
    """Whether two parts have material in one place within `region`."""
    if a.t_axis == b.t_axis:
        return any(_material(a, slab).intersection(_material(b, slab)).area > _TOLERANCE
                   for slab in _slabs(region, a.t_axis, a, b))
    axis: Axis = next(x for x in AXES if x not in (a.t_axis, b.t_axis))
    for slab in _slabs(region, a.t_axis, a):
        for cell in _slabs(slab, b.t_axis, b):
            spans_a, spans_b = _spans(a, cell, axis), _spans(b, cell, axis)
            if any(min(p[1], q[1]) - max(p[0], q[0]) > _TOLERANCE for p in spans_a for q in spans_b):
                return True
    return False


def _spans(part: Board, region: Box, axis: Axis) -> list[tuple[float, float]]:
    """The stretches along `axis` (one of the part's in-plane axes) where
    the part has material within `region`."""
    i = 0 if axis == part.u_axis else 1
    return [(float(g.bounds[i]), float(g.bounds[i + 2])) for g in _material(part, region).polygons()
            if g.area > _TOLERANCE]


def _box_hits(part: Board, box: Box) -> bool:
    """Whether a box reaches into the part's material."""
    b = part.box()
    return box.overlaps(b) and _has_material(part, box.intersection(b))


def _has_material(part: Board, region: Box) -> bool:
    """Whether the part has material within `region`, slab by slab."""
    return any(_material(part, slab).area > _TOLERANCE for slab in _slabs(region, part.t_axis, part))


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


def _material(part: Board, region: Box) -> Shape:
    """The part's material inside `region`, seen along its thickness: the
    outline within the region, minus the pockets and holes deep enough to
    span the region's range along the thickness axis."""
    b = part.box()
    t, u, v = part.t_axis, part.u_axis, part.v_axis
    window = Shape(shapely_box(region.lo[u], region.lo[v], region.hi[u], region.hi[v]))
    material = part.outline.intersection(window)
    t0, t1 = max(region.lo[t], b.lo[t]), min(region.hi[t], b.hi[t])
    for lo, hi, op in _bands(part):
        if lo <= t0 + _TOLERANCE and t1 <= hi + _TOLERANCE:
            material = material.difference(op.shape if isinstance(op, Pocket) else _hole_shape(op))
    return material


def _hole_shape(hole: Hole) -> Shape:
    """A hole's circle as a polygon whose sides touch the circle from
    outside, so a box in the hole with its corners on the circle does not
    hit the slivers of material a polygon inside the circle would leave;
    one side a degree, so it takes no more than 3.8e-5 r beyond the circle
    [found by fuzzing, 2026-10-14: with 64 sides, 0.06 mm around a 100 mm
    hole, and a box reaching that far past the circle did not count]."""
    n = 4 * _HOLE_SEGMENTS
    r = hole.d / 2 / math.cos(math.pi / n)
    return Shape(Point(hole.u, hole.v).buffer(r, quad_segs=_HOLE_SEGMENTS))


_HOLE_SEGMENTS = 90


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
    the placeholder box it stands in."""
    box = scope.box
    if box is None:
        return []
    problems: list[str] = []
    for part in scope.all_parts():
        b = part.box()
        out = [f"{name} by {amount:g}" for name, amount in _overhang(b, box) if amount > 1e-6]
        if out:
            problems.append(f"{part.path} reaches out of {scope.path}'s box: {', '.join(out)}")
    return problems


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
    other by its box."""
    if not contour.closed:
        raise LangError(f"inside(): contour {contour.name!r} is open; the check needs a closed one.")
    n = contour.normal_axis
    others: list[Axis] = [a for a in AXES if a != n]
    allowed = contour.polygon(others[0], others[1])
    if gap:
        allowed = allowed.buffer(-gap)

    def check(scope: Scope) -> list[str]:
        problems: list[str] = []
        for part in scope.all_parts():
            shadow = footprint(part.box(), part.outline, part.t_axis, n)
            outside = shadow.difference(allowed).area
            if outside > 1e-6:
                clearance = f" with {gap:g} mm clearance" if gap else ""
                problems.append(f"{part.path} is not inside {contour.name}{clearance} "
                                f"({outside:.0f} mm² outside)")
        return problems

    check.__name__ = f"inside({contour.name})"
    return check
