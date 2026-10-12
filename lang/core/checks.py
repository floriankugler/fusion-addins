"""Checks that run on the layout, before any geometry exists."""
from __future__ import annotations

from typing import TYPE_CHECKING

from shapely.geometry import box as shapely_box

from . import directions
from .box import Box
from .contours import Contour, footprint
from .crossing import crossing
from .directions import AXES, Axis
from .errors import LangError
from .ops import Pocket
from .scope import Check, Scope
from .shapes import Shape

if TYPE_CHECKING:
    from .part import Board


def no_interference(scope: Scope) -> list[str]:
    """Pairs of parts in the scope (and below) whose material overlaps. A
    part's material is its outline through its thickness minus its pockets,
    so a floor sitting in a groove does not count. Parallel parts must have
    material in the same place, so a hatch in a rounded opening, whose box
    reaches into the opening's corners, does not count. Perpendicular parts
    must also pass through each other (`crossing`), so two lapped battens,
    each filling half of the box they share, do not count either. Pockets
    in narrow faces are not taken into account yet."""
    parts = scope.all_parts()
    problems: list[str] = []
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            if not a.box().overlaps(b.box()):
                continue
            region = a.box().intersection(b.box())
            if a.t_axis == b.t_axis:
                if _material(a, region).intersection(_material(b, region)).area <= _TOLERANCE:
                    continue
            elif not (_has_material(a, region) and _has_material(b, region)) or crossing(a, b) is None:
                continue
            problems.append(f"{a.path} overlaps {b.path}")
    return problems


_TOLERANCE = 1e-6


def _has_material(part: Board, region: Box) -> bool:
    return _material(part, region).area > _TOLERANCE


def _material(part: Board, region: Box) -> Shape:
    """The part's material inside `region`, seen along its thickness: the
    outline within the region, minus the pockets deep enough to span the
    region's range along the thickness axis."""
    b = part.box()
    t, u, v = part.t_axis, part.u_axis, part.v_axis
    window = Shape(shapely_box(region.lo[u], region.lo[v], region.hi[u], region.hi[v]))
    material = part.outline.intersection(window)
    t0, t1 = max(region.lo[t], b.lo[t]), min(region.hi[t], b.hi[t])
    for op in part.ops:
        if not isinstance(op, Pocket):
            continue
        face = directions.frame.direction(op.face)
        band = (b.hi[t] - op.depth, b.hi[t]) if face.sign > 0 else (b.lo[t], b.lo[t] + op.depth)
        if band[0] <= t0 + _TOLERANCE and t1 <= band[1] + _TOLERANCE:
            material = material.difference(op.shape)
    return material


def fits_sheet(scope: Scope) -> list[str]:
    problems: list[str] = []
    for part in scope.all_parts():
        sheet = part.material.sheet
        if sheet is None:
            continue
        w, h = part.outline.width, part.outline.height
        if not ((w <= sheet[0] and h <= sheet[1]) or (w <= sheet[1] and h <= sheet[0])):
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
