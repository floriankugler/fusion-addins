"""How the parts hold on the vacuum bed under skin and release
(`proposals/cam.md`, Holding, decided 2026-10-17).

Every contour is roughed to a skin and cut free at the end of the setup.
Until then the skin seals every kerf and the sheet is one airtight plate;
each contour released opens a slot through it onto the bleed-through
spoilboard, and the vacuum under what is still attached drops. So the
parts that hold least go first, while the sheet is sealed (`release_order`):
by their hold, the footprint shrunk by `cam.tab_margin` where air leaks
in at every free edge (`regions.hold`, cm²), smallest first; parts that
hold alike in the order that travels least, each from where the last one
was, from the blank's corner.

Tabs are the safety net for the smallest and skinniest [Florian,
2026-10-17]: a part whose footprint shrunk by the margin keeps less than
`cam.tab_area`, or nothing (narrower than twice the margin), gets them
(`needs_tabs`); `cam.tabs("forced")` or `"none"` on a part overrides.
"""
from __future__ import annotations

import math
from collections.abc import Sequence
from typing import TypeVar

from shapely.geometry.base import BaseGeometry

from .regions import eroded

T = TypeVar("T")
Point2 = tuple[float, float]

#: Holds closer than this (cm²) are alike: the order goes by travel.
SAME_HOLD = 0.01


def needs_tabs(footprint: BaseGeometry, margin: float, area: float) -> bool:
    """Whether a part holds too little: its footprint shrunk by `margin`
    (mm) keeps less than `area` (cm²), or nothing."""
    held = eroded(footprint, margin)
    return held.is_empty or held.area / 100.0 < area


def release_order(parts: Sequence[tuple[str, float, Point2]]) -> list[str]:
    """Parts (path, hold in cm², centre) in the order they are released."""
    order: list[str] = []
    left = sorted(parts, key=lambda p: p[1])
    at: Point2 = (0.0, 0.0)
    while left:
        least = left[0][1]
        alike = [p for p in left if p[1] - least <= SAME_HOLD]
        nearest = min(alike, key=lambda p: (math.dist(at, p[2]), p[0]))
        order.append(nearest[0])
        at = nearest[2]
        left.remove(nearest)
    return order


def by_travel(items: Sequence[tuple[T, Point2]], start: Point2 = (0.0, 0.0)) -> list[T]:
    """Items in the order that travels least, each the nearest to the last."""
    left = list(items)
    out: list[T] = []
    at = start
    while left:
        k = min(range(len(left)), key=lambda i: math.dist(at, left[i][1]))
        item, at = left.pop(k)
        out.append(item)
    return out
