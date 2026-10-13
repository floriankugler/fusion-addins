"""Fuzzing the corner kernels on polygons of lines: `cutouts.filleted`
(behind `Shape.rounded()`, `Board.fillet()` and the cutouts' rounding) and
`cutouts.chamfered` (`Board.chamfer()` on outline corners) must round or
cut off every corner exactly as a construction from the tangent lengths
does, and refuse only where that construction does not fit."""
import math

from hypothesis import given
from hypothesis import strategies as st

from fuzzing import Lines, floats, hairline, line_polygons, reference_chamfer, reference_fillet
from lang.core import cutouts


@given(line_polygons(), st.one_of(st.sampled_from([1.0, 3.0, 6.0, 8.0, 20.0]), floats(0.1, 40)))
def test_every_corner_is_rounded_as_the_tangent_lengths_say(shape: Lines, r: float):
    poly = shape.polygon()
    if poly is None or hairline(poly):        # (no arc fits a wall of no thickness: open, see `hairline`)
        return
    got, want = cutouts.filleted(poly, r), reference_fillet(poly, r)
    if want is None:
        assert got is None or got.is_valid
        return
    assert got is not None, "refused, though every arc fits"
    assert got.is_valid
    # (an arc's steps are whole degrees, the ones at its ends up to 1.6: `cutouts._END`)
    assert got.hausdorff_distance(want) <= r * (1 - math.cos(math.radians(0.8))) + 1e-6
    assert cutouts.corner_points(got) == []


@given(line_polygons(), st.one_of(st.sampled_from([1.0, 3.0, 10.0]), floats(0.1, 30)))
def test_every_corner_is_cut_off_as_named(shape: Lines, size: float):
    poly = shape.polygon()
    if poly is None or hairline(poly):
        return
    corners = [p for p, _ in cutouts.corner_points(poly)]
    got, want = cutouts.chamfered(poly, size, corners), reference_chamfer(poly, size)
    if want is None:
        assert got is None or got.is_valid
        return
    assert got is not None, "refused, though every cut fits"
    assert got.hausdorff_distance(want) <= 1e-6
