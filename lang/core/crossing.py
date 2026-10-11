"""Crossings: two perpendicular boards whose material passes through each
other, as battens across and along a floor do before they are lapped.

Two boards in perpendicular planes share one axis, the line their planes
meet along (`axis`). Each board's material at the other's thickness,
projected onto that axis, gives a set of stretches; the boards cross where
those overlap. That is exact for the boards' outlines (through cuts
included); pockets are not taken into account.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from shapely.geometry import box as shapely_box

from .directions import AXES, Axis

if TYPE_CHECKING:
    from .part import Board

Span = tuple[float, float]


@dataclass(frozen=True)
class Crossing:
    """Where boards `a` and `b` pass through each other: from `lo` to `hi`
    along `axis`, the axis both their planes contain."""
    a: Board
    b: Board
    axis: Axis
    lo: float
    hi: float


def _spans(part: Board, band_axis: Axis, band: Span, axis: Axis) -> list[Span]:
    """The part's outline within `band` on `band_axis`, projected onto
    `axis`: the stretches where it has material."""
    u, v = part.u_axis, part.v_axis
    big = 1e9
    lo = {u: -big, v: -big}
    hi = {u: big, v: big}
    lo[band_axis], hi[band_axis] = band
    inside = part.outline.geometry.intersection(shapely_box(lo[u], lo[v], hi[u], hi[v]))
    i = 0 if axis == u else 1
    spans: list[Span] = []
    for g in getattr(inside, "geoms", [inside]):
        if g.is_empty or g.area <= 1e-9:
            continue
        b = g.bounds
        spans.append((float(b[i]), float(b[i + 2])))
    return spans


def crossing(a: Board, b: Board, tolerance: float = 1e-6) -> Crossing | None:
    """How perpendicular boards `a` and `b` cross, or None when they are
    parallel or their material does not pass through each other."""
    ta, tb = a.t_axis, b.t_axis
    if ta == tb or not a.box().overlaps(b.box()):
        return None
    axis: Axis = next(x for x in AXES if x not in (ta, tb))
    ab, bb = a.box(), b.box()
    spans_a = _spans(a, tb, (bb.lo[tb], bb.hi[tb]), axis)
    spans_b = _spans(b, ta, (ab.lo[ta], ab.hi[ta]), axis)
    shared = [(max(p[0], q[0]), min(p[1], q[1])) for p in spans_a for q in spans_b
              if min(p[1], q[1]) - max(p[0], q[0]) > tolerance]
    if not shared:
        return None
    return Crossing(a, b, axis, min(s[0] for s in shared), max(s[1] for s in shared))
