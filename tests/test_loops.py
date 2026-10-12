"""The emitter's geometry that needs no Fusion (`lang.emit.loops`): loop
winding, and whether a point lies on a line, an arc or a circle, as the
emitter finds a chamfer's edges by their midpoints."""
import math

from lang.emit.loops import dist_to_segment, newell_normal, on_arc, on_curve, oriented, polygon_loop
from lang.emit.plan import Arc, Circle, Line, Loop, loop_points

UP = (0.0, 0.0, 1.0)
DOWN = (0.0, 0.0, -1.0)


def _at(angle_deg: float, r: float = 10.0) -> tuple[float, float, float]:
    a = math.radians(angle_deg)
    return (r * math.cos(a), r * math.sin(a), 0.0)


def _arc(start: float, mid: float, end: float) -> Arc:
    return Arc(_at(start), _at(mid), _at(end), (0.0, 0.0, 0.0), 10.0)


def test_newell_normal_follows_the_winding():
    square = [(0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (2.0, 2.0, 0.0), (0.0, 2.0, 0.0)]
    assert newell_normal(square) == (0.0, 0.0, 8.0)          # twice the area, counter-clockwise about +z
    assert newell_normal(square[::-1]) == (0.0, 0.0, -8.0)


def test_oriented_winds_a_loop_for_the_normal_asked_for():
    loop = polygon_loop([(0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (2.0, 2.0, 0.0), (0.0, 2.0, 0.0)])
    assert oriented(loop, UP) == loop
    turned = oriented(loop, DOWN)
    assert newell_normal(loop_points(turned))[2] < 0
    assert turned[0] == Line((0.0, 0.0, 0.0), (0.0, 2.0, 0.0))       # the last edge, run back
    arc = _arc(0, 90, 180)                                   # a D: the arc over the top, a line back
    d: Loop = [arc, Line(arc.b, arc.a)]
    assert oriented(d, UP) == d
    assert oriented(d, DOWN) == [Line(arc.a, arc.b), Arc(arc.b, arc.mid, arc.a, arc.center, arc.radius)]
    circle = Circle((0.0, 0.0, 0.0), 5.0)
    assert oriented([circle], DOWN) == [circle]


def test_a_point_is_on_an_arc_between_its_ends_either_way_round():
    ccw = _arc(10, 45, 80)                   # counter-clockwise about +z
    cw = _arc(80, 45, 10)                    # the same arc, the other way
    for arc in (ccw, cw):
        assert on_arc(_at(30), arc, UP) and on_arc(_at(10), arc, UP) and on_arc(_at(80), arc, UP)
        assert not on_arc(_at(100), arc, UP) and not on_arc(_at(-30), arc, UP)
    # seen from below the same points lie on it: the winding is read from the middle point
    assert on_arc(_at(30), ccw, DOWN) and not on_arc(_at(100), ccw, DOWN)


def test_an_arc_across_the_seam_at_zero_degrees():
    arc = _arc(-30, 0, 30)
    assert on_arc(_at(350), arc, UP) and on_arc(_at(0), arc, UP) and on_arc(_at(20), arc, UP)
    assert not on_arc(_at(180), arc, UP) and not on_arc(_at(40), arc, UP)
    back = _arc(30, 0, -30)
    assert on_arc(_at(350), back, UP) and not on_arc(_at(180), back, UP)


def test_on_curve_within_a_tolerance():
    line = Line((0.0, 0.0, 0.0), (10.0, 0.0, 0.0))
    assert on_curve((5.0, 0.005, 0.0), line, UP, 0.01)
    assert not on_curve((5.0, 0.02, 0.0), line, UP, 0.01)
    assert not on_curve((10.5, 0.0, 0.0), line, UP, 0.01)       # past the end
    circle = Circle((0.0, 0.0, 0.0), 10.0)
    assert on_curve(_at(200), circle, UP, 0.01) and not on_curve(_at(200, 10.1), circle, UP, 0.01)
    assert on_curve(_at(45), _arc(0, 45, 90), UP, 0.01) and not on_curve(_at(135), _arc(0, 45, 90), UP, 0.01)
    assert dist_to_segment((5.0, 3.0, 0.0), (0.0, 0.0, 0.0), (10.0, 0.0, 0.0)) == 3.0
