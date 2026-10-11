"""Arcs recovered from the layout's polygons (`lang.emit.arcs`)."""
import math

import pytest
from shapely.geometry import Point, box

from lang import *
from lang.core.shapes import Shape, slot_shape
from lang.emit.arcs import Arc2, Circle2, Line2, fit


def _ring(shape: Shape) -> list[tuple[float, float]]:
    (ring,) = shape.rings()
    return ring


def _kinds(curves: list[Line2 | Arc2 | Circle2]) -> str:
    return "".join({Line2: "L", Arc2: "A", Circle2: "C"}[type(c)] for c in curves)


def test_a_circle_is_one_circle():
    (c,) = fit(_ring(circle(15, center=(503.2, 1200.7))))
    assert isinstance(c, Circle2)
    assert c.center == pytest.approx((503.2, 1200.7), abs=1e-9) and c.radius == pytest.approx(7.5, abs=1e-9)


def test_a_slot_is_two_lines_and_two_arcs():
    curves = fit(_ring(slot_shape((30.7, 7.5), (43.3, 7.5), 4)))   # a Domino slot, 4 high
    assert sorted(_kinds(curves)) == ["A", "A", "L", "L"]
    arcs = [c for c in curves if isinstance(c, Arc2)]
    assert sorted(round(a.center[0], 9) for a in arcs) == [30.7, 43.3]
    assert all(a.radius == pytest.approx(2, abs=1e-9) for a in arcs)
    # each arc runs between the ends of the straight sides, through its far point
    left = next(a for a in arcs if a.center[0] < 40)
    assert {(round(p[0], 9), round(p[1], 9)) for p in (left.a, left.b)} == {(30.7, 9.5), (30.7, 5.5)}


def test_curves_follow_the_ring_and_close_it():
    for shape in (slot_shape((0, 0), (20, 5), 6), rect(width=100, depth=40).rounded(8),
                  Shape(box(0, 0, 50, 30).difference(Point(50, 30).buffer(10)))):
        curves = fit(_ring(shape))
        ends = [(c.a, c.b) for c in curves if not isinstance(c, Circle2)]
        for (_, b), (a, _) in zip(ends, ends[1:] + ends[:1]):
            assert a == b


def test_rounded_corners_are_arcs():
    curves = fit(_ring(rect(width=100, depth=40).rounded(8)))
    assert sorted(_kinds(curves)) == ["A"] * 4 + ["L"] * 4
    assert all(c.radius == pytest.approx(8, abs=1e-9) for c in curves if isinstance(c, Arc2))


def test_a_ring_starting_inside_an_arc_gets_it_whole():
    ring = _ring(slot_shape((0, 0), (20, 0), 6))
    shifted = ring[5:] + ring[:5]                       # starts in the middle of an end
    assert sorted(_kinds(fit(shifted))) == ["A", "A", "L", "L"]


def test_polygons_stay_polygons():
    octagon = [(math.cos(k * math.pi / 4), math.sin(k * math.pi / 4)) for k in range(8)]
    assert _kinds(fit(octagon)) == "L" * 8
    assert _kinds(fit(_ring(rect(width=100, depth=40)))) == "LLLL"
    # curves sampled every 0.1 mm with the master's rounding (0.1 micrometre) are left alone
    for radius in (1.5, 3.0, 5.0, 8.0, 11.0, 12.0, 100.0, 2000.0):
        kinds = _kinds(fit(_sampled(radius)))
        assert "A" not in kinds and "C" not in kinds, radius


def _sampled(radius: float) -> list[tuple[float, float]]:
    step = 0.1 / radius
    return [(round(radius * math.cos(k * step), 4), round(radius * math.sin(k * step), 4))
            for k in range(min(2000, int(1.5 * math.pi / step)))] + [(0.0, 0.0)]


def test_a_cut_corner_keeps_its_arc():
    # a rectangle with a quarter circle taken out of one corner: one arc, the rest lines
    curves = fit(_ring(Shape(box(0, 0, 50, 30).difference(Point(50, 30).buffer(10)))))
    arcs = [c for c in curves if isinstance(c, Arc2)]
    assert len(arcs) == 1 and arcs[0].center == pytest.approx((50, 30), abs=1e-9)


def _on_circle(p: tuple[float, float], center: tuple[float, float], r: float) -> bool:
    return abs(math.dist(p, center) - r) < 1e-9


def test_a_corner_relief_meets_the_rectangle_exactly():
    # a mortise corner at the origin, the relief on its bisector inside, through the corner
    d = 6.0
    o = d / (2 * math.sqrt(2))
    shape = Shape(box(0, 0, 50, 15).union(Point(o, o).buffer((d + 0.1) / 2, quad_segs=16)))
    curves = fit(_ring(shape))
    (arc,) = [c for c in curves if isinstance(c, Arc2)]
    assert arc.center == pytest.approx((o, o), abs=1e-9) and arc.radius == pytest.approx(3.05, abs=1e-9)
    # its ends lie on the circle and on the rectangle's edges, where the lines pick up
    ends = {(round(p[0], 9), round(p[1], 9)) for p in (arc.a, arc.b)}
    assert all(_on_circle(p, (o, o), 3.05) for p in (arc.a, arc.b))
    assert sorted(min(abs(p[0]), abs(p[1])) for p in ends) == pytest.approx([0, 0], abs=1e-12)
    for c in curves:                                   # no stray chord pieces left
        if isinstance(c, Line2):
            assert math.dist(c.a, c.b) > 1


def test_a_relief_cut_from_an_outline_is_one_arc_between_lines():
    # the root of a tab: the board below y = 0, the tab at x >= 0, the relief outside the corner
    o = 6 / (2 * math.sqrt(2))
    board = box(-50, -20, 50, 0).union(box(0, 0, 50, 30))
    curves = fit(_ring(Shape(board.difference(Point(-o, o).buffer(3.05, quad_segs=16)))))
    (arc,) = [c for c in curves if isinstance(c, Arc2)]
    assert all(_on_circle(p, (-o, o), 3.05) for p in (arc.a, arc.b, arc.mid))
    for p in (arc.a, arc.b):
        assert abs(p[0]) < 1e-12 or abs(p[1]) < 1e-12        # on the tab's side or on the shoulder


def test_two_overlapping_circles_meet_at_their_crossing():
    shape = Shape(Point(0, 0).buffer(7.5, quad_segs=16).union(Point(11.2, 0).buffer(7.5, quad_segs=16)))
    curves = fit(_ring(shape))
    assert _kinds(curves) == "AA"
    for c in curves:
        assert isinstance(c, Arc2)
        for p in (c.a, c.b):
            assert _on_circle(p, (0, 0), 7.5) and _on_circle(p, (11.2, 0), 7.5)
