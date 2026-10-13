"""Cleaning what booleans of coincident edges leave (`geometry.clean`),
which every `Shape` gets: decided with Florian on 2026-10-13, after
fuzzing found spikes, slivers and walls of no width."""
import math

import pytest
from shapely import affinity
from shapely.geometry import Point, Polygon, box

from lang import *
from lang.core.cutouts import circle_geometry, filleted
from lang.core.geometry import clean, polygons_of
from lang.core.layout import build_layout
from lang.core.shapes import slot_shape
from tests.helpers import ply15


@pytest.mark.parametrize("cutter", ["cutouts", "circle"])
def test_a_circle_cut_on_a_rounded_corners_own_arc_takes_the_corner(cutter: str):
    """The two polygons of one arc (the corner's and the circle's) cross
    each other along it, and what lay between them fell apart into
    crescents up to 0.009 mm wide: the cut was refused as splitting the
    board, though it splits nothing."""
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15, rect(depth=300, width=400).rounded(50)).on(m.bottom)
        before = panel.outline.geometry
        hole = Shape(circle_geometry((50, 50), 50)) if cutter == "cutouts" else circle(100, center=(50, 50))
        panel.add_cut(hole)
    assert len(panel.outline.polygons()) == 1
    # less the crescents, 0.7 mm2 in all with the circle's 32 segments a quarter
    assert panel.outline.area == pytest.approx(before.difference(hole.geometry).area, abs=1.0)


def test_a_shape_added_and_taken_away_again_leaves_no_spike():
    """A diamond poking out of a square, added and taken away again, left
    a spike of no width 29 mm out from the square's corner along its edge:
    the board's box took it in (120.7 by 110 for a board 100 by 100)."""
    diamond = Shape(affinity.rotate(box(0, 60, 100, 160), 45, origin=(50, 110)))
    notched = Shape(box(0, 0, 100, 100)).union(diamond).difference(diamond)
    (ring,) = notched.rings()
    sides = 110 - 50 * math.sqrt(2) + 50          # where the diamond's lower sides leave the square
    assert len(ring) == 5 and notched.bounds == pytest.approx((0, 0, 100, sides))
    with module("m", Box.from_size(width=100, depth=100, height=100)) as m:
        board("panel", ply15, notched).on(m.bottom)
    (part,) = build_layout()["modules"][0]["parts"]
    lo, hi = part["box"]["min"], part["box"]["max"]
    assert [hi[0] - lo[0], hi[1] - lo[1]] == pytest.approx([100, notched.bounds[3]])


def test_a_band_cut_across_a_shape_exactly_as_tall_parts_it():
    """Found by fuzzing: both turned 1.16 degrees, the cut left the shape
    whole with the band as a hole whose edges lay on the outline's, 2e-15
    apart, instead of two pieces."""
    turn = 1.15625
    slab = Shape(affinity.rotate(box(-136.5, -29.875, 133.5, 105.125), turn, origin=(-1.5, 37.625)))
    band = Shape(affinity.rotate(box(-2.5, -29.875, -0.5, 105.125), turn, origin=(-1.5, 37.625)))
    parted = slab.difference(band)
    assert [len(p.interiors) for p in parted.polygons()] == [0, 0]
    assert sorted(p.area for p in parted.polygons()) == pytest.approx([134 * 135, 134 * 135])


def test_clean_keeps_what_is_meant_as_it_is():
    """A circle cut touching the board's edge (Fusion builds it), a rounded
    rectangle with a hole, a slot: nothing to clean, the same geometry."""
    touching = box(0, 0, 100, 100).difference(circle_geometry((50, 10), 10))
    rounded = filleted(box(0, 0, 300, 400), 50)
    assert rounded is not None
    holed = rounded.difference(Point(150, 200).buffer(20, quad_segs=32))
    slot = slot_shape((0, 0), (40, 0), 8).geometry
    for g in (touching, holed, slot):
        assert clean(g) is g
    assert polygons_of(clean(Polygon([(0, 0), (10, 0), (10, 0.005), (0, 0.005)]))) == []    # 5 um wide
    assert len(polygons_of(clean(Polygon([(0, 0), (10, 0), (10, 0.02), (0, 0.02)])))) == 1  # 20 um
