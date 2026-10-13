"""Fuzzing `geometry.clean` on what shapely's booleans leave of the
shapes the language makes (`Recipe.raw`, `Lines.raw`): the cleaned
geometry is valid and has nothing left to clean (no points on top of each
other, no spikes, nothing narrower than `NARROWEST`, no walls of no width),
cleaning it again changes nothing, and it differs from the raw one only by
what was too thin to keep."""
from hypothesis import given
from hypothesis import strategies as st
from shapely.geometry.base import BaseGeometry

from fuzzing import line_polygons, recipes
from lang.core import geometry
from lang.core.geometry import NARROWEST, clean, polygons_of


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
