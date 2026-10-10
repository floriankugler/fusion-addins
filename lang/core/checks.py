"""Checks that run on the layout, before any geometry exists."""
from __future__ import annotations

from typing import TYPE_CHECKING

from shapely.geometry import box as shapely_box

from . import directions
from .box import Box
from .ops import Pocket
from .scope import Scope
from .shapes import Shape

if TYPE_CHECKING:
    from .part import Board


def no_interference(scope: Scope) -> list[str]:
    """Pairs of parts in the scope (and below) whose material overlaps. A
    part's material is its outline through its thickness minus its pockets,
    so a floor sitting in a groove does not count. Pockets in narrow faces
    are not taken into account yet."""
    parts = scope.all_parts()
    problems: list[str] = []
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            if not a.box().overlaps(b.box()):
                continue
            region = a.box().intersection(b.box())
            if _has_material(a, region) and _has_material(b, region):
                problems.append(f"{a.path} overlaps {b.path}")
    return problems


def _has_material(part: Board, region: Box, tolerance: float = 1e-6) -> bool:
    """Whether the part's material reaches into `region`: the outline
    within it, minus the pockets deep enough to span the region's range
    along the thickness axis."""
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
        if band[0] <= t0 + tolerance and t1 <= band[1] + tolerance:
            material = material.difference(op.shape)
    return material.area > tolerance


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
