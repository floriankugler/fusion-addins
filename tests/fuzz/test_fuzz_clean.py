"""Fuzzing `geometry.clean` on what shapely's booleans leave of the
shapes the language makes (`Recipe.raw`, `Lines.raw`): the cleaned
geometry is valid and has nothing left to clean (no points on top of each
other, no spikes, nothing narrower than `NARROWEST`, no walls of no width),
cleaning it again changes nothing, and it differs from the raw one only by
what was too thin to keep."""
import math

from hypothesis import given
from hypothesis import strategies as st
from shapely import affinity
from shapely.geometry import box
from shapely.geometry.base import BaseGeometry

from fuzzing import floats, line_polygons, recipes, sizes
from lang.core import geometry
from lang.core.geometry import NARROWEST, clean, polygons_of
from lang.core.shapes import Shape, circle


def _left_to_clean(g: BaseGeometry) -> list[str]:
    found: list[str] = []
    for poly in polygons_of(g):
        for ring in [poly.exterior, *poly.interiors]:
            if geometry._without_spikes(ring) is not None:  # pyright: ignore[reportPrivateUsage]
                found.append("a point on another, or a spike")
            if geometry._narrow(ring):  # pyright: ignore[reportPrivateUsage]
                found.append("a ring narrower than NARROWEST")
        if poly.interiors and geometry._has_walls(poly):  # pyright: ignore[reportPrivateUsage]
            found.append("a wall of no width")
    return found


@given(st.one_of(recipes().map(lambda r: r.raw()), line_polygons().map(lambda s: s.raw())))
def test_clean_leaves_nothing_to_clean_and_takes_only_what_is_too_thin(raw: BaseGeometry):
    cleaned = clean(raw)
    assert cleaned.is_empty or cleaned.is_valid
    assert _left_to_clean(cleaned) == []
    assert clean(cleaned) is cleaned
    # a piece or hole narrower than NARROWEST holds less than half of it
    # times its length; a spike and a wall hold nothing
    assert raw.symmetric_difference(cleaned).area <= NARROWEST / 2 * raw.length + 1e-9


@given(sizes(20, 2000), sizes(20, 2000), floats(0.05, 0.45), floats(0, 360), st.integers(0, 3))
def test_a_circle_cut_on_a_rounded_corners_own_arc_leaves_one_piece(w: float, h: float, share: float,
                                                                   turn: float, corner: int):
    """Every circle and arc has its vertices on the whole degrees about its
    centre, so the corner's arc and the circle coincide, at any size, any
    turn, any corner. Not their ends: an arc ends where it meets the line
    beside it, between whole degrees, and the circle's chord there passes
    inside it by up to r (1 - cos 0.5 degrees), 0.019 mm at a radius of
    500; where nothing joins that sliver to the rest (a radius of half the
    shape's width, its straight sides 1 mm long), it is a piece of its own
    (open, 2026-10-13)."""
    r = share * min(w, h)
    board = Shape(affinity.rotate(box(0, 0, w, h), turn, origin=(0, 0))).rounded(r)
    cx, cy = [(r, r), (w - r, r), (w - r, h - r), (r, h - r)][corner]
    a = math.radians(turn)
    centre = (cx * math.cos(a) - cy * math.sin(a), cx * math.sin(a) + cy * math.cos(a))
    assert len(board.difference(circle(2 * r, centre)).polygons()) == 1
