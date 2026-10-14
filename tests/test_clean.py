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


@pytest.mark.parametrize("r, turn", [(200, 0.0), (500, 0.0), (2000, 7.3)])
def test_one_circle_drawn_twice_coincides_at_any_radius(r: float, turn: float):
    """`circle()` drew 32 segments a quarter, fillets a vertex every whole
    degree: from a radius of about 200 the crescents between the two
    drawings of a rounded corner's arc were too thick to clean, and a
    circle cut on it split the shape in 32 pieces. Every circle and arc
    has its vertices on the whole degrees about its centre now, also on a
    board turned by a part of a degree."""
    a = math.radians(turn)
    board = Shape(affinity.rotate(box(0, 0, 3 * r, 4 * r), turn, origin=(0, 0))).rounded(r)
    centre = (r * math.cos(a) - r * math.sin(a), r * math.sin(a) + r * math.cos(a))
    assert len(board.difference(circle(2 * r, centre)).polygons()) == 1


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


def test_a_spike_out_and_back_to_the_same_point_goes_whatever_its_length():
    """Found by fuzzing dog bones: a level's ring ran 0.07 mm out and back
    to a point 1e-12 from where it left, and the vertex beside the spike
    was taken for a 43 degree inside corner, at one place of the board
    only. With the points either side of a vertex the same, the ring runs
    out and back along itself: a spike, however long."""
    for length in (0.07, 5.0):
        ring = [(0, 0), (10, 0), (10, 10), (5, 10), (5 + length * 0.6, 10 + length * 0.8), (5 - 1e-12, 10), (0, 10)]
        spiked = Polygon(ring)
        assert spiked.is_valid
        (cleaned,) = polygons_of(clean(spiked))
        assert list(cleaned.exterior.coords) == [(0, 0), (10, 0), (10, 10), (5, 10), (0, 10), (0, 0)]


def test_a_spike_beside_an_edge_in_line_with_it_goes_too():
    """Found by fuzzing: a union and difference left a spike 200 mm out
    whose way back ran along another edge in line with it; without the
    spike the ring ran along itself there, invalid, and clean kept the
    spike rather than make it worse. What is left is made valid now, as an
    invalid input is: two pieces, all the area, no spike."""
    ring = [(30.337985425689457, -74.0311194046845), (23.502206085828806, -57.92703247462465),
            (9.42172606141327, -72.00751249904019), (9.767766952966362, -72.35355339059328),
            (8.353553390593262, -73.76776695296637), (6.232233047033624, -71.64644660940672),
            (7.064448147192326, -70.81423150924802), (8.83972759919888, -72.58951096125458),
            (153.08951096125458, 71.66027240080109),                    # the spike's tip
            (25.027484546414023, -56.40175401403944), (32.17899513259434, -73.24965714770595)]
    spiked = Polygon(ring)
    assert spiked.is_valid
    cleaned = clean(spiked)
    assert cleaned.is_valid and cleaned.area == pytest.approx(spiked.area)
    assert len(polygons_of(cleaned)) == 2 and cleaned.bounds[2] < 33


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


def test_wider_pieces_a_hairline_joins_stay():
    """Found by fuzzing the checks: a hardware box 0.09 longer than the
    pocket it stands in at either end, as wide as it, its sides 6e-14 off
    the pocket's. What the pocket leaves of the box is the two ends, joined
    along one side by a hairline 89 mm long: narrow on average, it went
    altogether, and the box's overlap with the board was not reported.
    Opened, the two ends stay, their vertices where they were."""
    piece = box(248.93532181880647, -253.53000500000002, 338.61817343027985, -251.52999499999999)
    pocket = box(249.02674762454316, -253.53000499999996, 338.5267476245432, -251.52999499999999)
    ends = sorted(polygons_of(clean(piece.difference(pocket))), key=lambda p: p.bounds)
    assert [p.bounds for p in ends] == [(248.93532181880647, -253.53000500000002, 249.02674762454316, -251.52999499999999),
                                        (338.5267476245432, -253.53000500000002, 338.61817343027985, -251.52999499999999)]
    assert clean(box(0, 0, 10, 0.005).union(box(0, 0, 1e-14, 30))).is_empty     # narrow all over: it goes


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


def test_a_collection_is_cleaned_to_its_areas():
    """Found by fuzzing: a shape intersected with the circle it had just
    lost is a collection of lines, points and polygons of no area (2e-18
    mm2); it was left as it was, invalid. A shape is an area: the lines
    and points go, and the polygons are cleaned."""
    from shapely.geometry import GeometryCollection, LineString
    square = box(0, 0, 10, 10)
    assert clean(GeometryCollection([square, LineString([(20, 0), (30, 0)]), Point(40, 0)])).equals(square)
    lost = Point(0, 34).buffer(1.0)
    left = Point(0, 0).buffer(34.5).union(lost).difference(lost).intersection(lost)
    assert clean(left).is_empty and Shape(left).is_empty()


def test_a_ring_a_move_rounds_into_a_crossing_is_made_valid():
    """Found by fuzzing: a circle with a polygon of 64 sides drawn in it
    taken out leaves 64 crescents, two of which nearly touch where the
    drawings' vertices nearly coincide. Moved 11 down, the rounding
    crossed them in a figure of eight, which clean left as it was, invalid.
    Cleaned, they are the crescents again."""
    crescents = circle_geometry((-4, 4), 14).difference(Point(-4, 4).buffer(14, quad_segs=16))
    moved = affinity.translate(crescents, 0, -11)
    assert crescents.is_valid and not moved.is_valid
    cleaned = clean(moved)
    assert cleaned.is_valid
    assert cleaned.symmetric_difference(affinity.translate(clean(crescents), 0, -11)).area < 1e-9


def test_a_piece_with_a_hairline_tail_keeps_the_piece():
    """Found by fuzzing the placement: what a dado left of a side where a
    shelf sat in it, a strip 0.2 by 7 mm, came with a hairline 175 mm long
    and 6e-14 wide along the dado's edge (the two edges a rounding apart),
    and the strip and hairline together were narrower than 0.01 mm on
    average: the strip was dropped with it, and the side did not overlap a
    shelf reaching into that strip, where the module lay at the origin. The
    hairline goes first, as a spike, then the strip is judged; a hole
    likewise."""
    y1, y2 = 302.98609239092434, 302.9860923909243
    tailed = [(194.5, y1), (194.5, y2), (19.355946959201994, y2), (19.355946959201994, 296),
              (19.155946959201994, 296), (19.155946959201994, y1)]
    strip = box(19.155946959201994, 296, 19.355946959201994, y1)
    (piece,) = polygons_of(clean(Polygon(tailed)))
    assert piece.symmetric_difference(strip).area < 1e-9
    holed = Polygon([(0, 200), (300, 200), (300, 400), (0, 400)], [tailed])
    (piece,) = polygons_of(clean(holed))
    assert len(piece.interiors) == 1 and piece.area == pytest.approx(300 * 200 - strip.area)
