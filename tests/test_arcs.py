"""Arcs recovered from the layout's polygons (`lang.emit.arcs`)."""
import math

import pytest
from shapely.geometry import Point, Polygon, box

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


def test_two_arcs_with_one_chord_between_them_meet_at_their_crossing():
    """Found by fuzzing: two overlapping circles offset with mitred joins
    (`grown`, as a cutout keeps material around them) leave a single short
    chord between the two arcs. Both arcs reached for it, one for each of
    its ends, so they overlapped and did not join."""
    from lang.core.cutouts import circle_geometry, grown
    shape = Shape(grown(circle_geometry((0, 1), 1).union(circle_geometry((0, 0), 1)), 1))
    curves = fit(_ring(shape))
    assert _kinds(curves) == "AA"
    for c, d in zip(curves, curves[1:] + curves[:1]):
        assert isinstance(c, Arc2) and isinstance(d, Arc2) and c.b == d.a
        assert _on_circle(c.b, (0, 1), 2) and _on_circle(c.b, (0, 0), 2)


def test_a_rounded_ring_started_near_an_arc_s_end_keeps_the_arc_whole():
    """Every corner rounded with arcs of a vertex per degree, the ring
    starting three vertices before an arc ends: those three would be too few
    for an arc of their own, so the fit starts where a line meets an arc."""
    from lang.core.cutouts import fillet
    (piece,) = fillet(box(0, 0, 100, 60), 8)
    ring = list(piece.exterior.coords)[:-1]
    for start in range(len(ring)):
        curves = fit(ring[start:] + ring[:start])
        assert sorted(_kinds(curves)) == ["A"] * 4 + ["L"] * 4, start


def _joined_and_simple(ring: list[tuple[float, float]]) -> list[Line2 | Arc2 | Circle2]:
    from shapely.geometry import LinearRing
    curves = fit(ring)
    for c, d in zip(curves, curves[1:] + curves[:1]):
        assert not isinstance(c, Circle2) and not isinstance(d, Circle2) and c.b == d.a
    drawn: list[tuple[float, float]] = []
    for c in curves:
        assert not isinstance(c, Circle2)
        drawn.append(c.a)
        if isinstance(c, Arc2):
            # the arc every tenth of a degree, the way it turns through mid
            (ax, ay), (mx, my), (bx, by), (ox, oy) = c.a, c.mid, c.b, c.center
            ccw = (mx - ax) * (by - my) - (my - ay) * (bx - mx) > 0
            a0, am, a1 = (math.atan2(y - oy, x - ox) for x, y in (c.a, c.mid, c.b))
            sign = 1 if ccw else -1
            sweep = (sign * (am - a0)) % (2 * math.pi) + (sign * (a1 - am)) % (2 * math.pi)
            n = math.ceil(math.degrees(sweep) * 10)
            drawn += [(ox + c.radius * math.cos(a0 + sign * sweep * k / n),
                       oy + c.radius * math.sin(a0 + sign * sweep * k / n)) for k in range(1, n)]
    assert LinearRing(drawn).is_simple
    return curves


def test_an_arc_reaching_for_the_start_of_another_arc_meets_it_where_the_circles_cross():
    """Found by fuzzing: a circle of the cutouts' kind and a coarse one (8
    segments a quarter) united and offset 11 inward. The coarse arc reached
    for the first vertex of the fine one and moved it along the fine arc's
    first chord, off the fine circle, which then got a wrong centre."""
    from shapely.geometry.polygon import orient
    from lang.core.cutouts import _arc_targets, _onto_circles, circle_geometry  # pyright: ignore[reportPrivateUsage]
    # offset as `grown` did then: mitred, its arcs put back on their circles
    united = circle_geometry((-110, 92), 169.5).union(Point(73, 25).buffer(200, quad_segs=8))
    assert isinstance(united, Polygon)
    buffered = united.buffer(-11, join_style="mitre", mitre_limit=100.0)
    assert isinstance(buffered, Polygon)
    shape = _onto_circles(buffered, _arc_targets(united, -11))
    ring = [(float(x), float(y)) for x, y in list(orient(shape, 1.0).exterior.coords)[:-1]]
    curves = _joined_and_simple(ring)
    arcs = [c for c in curves if isinstance(c, Arc2)]
    assert sorted((round(a.center[0], 6), round(a.center[1], 6), round(a.radius, 6)) for a in arcs) == \
        [(-110, 92, 158.5), (73, 25, 189)]
    meeting = [c.b for c, d in zip(curves, curves[1:] + curves[:1]) if isinstance(c, Arc2) and isinstance(d, Arc2)]
    assert len(meeting) == 1
    assert _on_circle(meeting[0], (-110, 92), 158.5) and _on_circle(meeting[0], (73, 25), 189)


def test_a_vertex_moved_onto_an_arc_stays_short_of_the_next_vertex():
    """Found by fuzzing: where three shapes meet within a millimetre, an arc
    reached for a vertex followed by a line 1.4 long, and the line's crossing
    with the arc's circle lay past that line's far end: the drawn ring ran
    back on itself."""
    from shapely import affinity
    from shapely.geometry.polygon import orient
    from shapely.ops import unary_union
    from lang.core.cutouts import circle_geometry, filleted
    cx, cy = -95.05993986624881, 165.25231422302477
    rounded = filleted(affinity.rotate(box(cx - 149.5, cy - 93.5, cx + 149.5, cy + 93.5), 45, origin=(cx, cy)), 18.7)
    assert rounded is not None
    shape = unary_union([circle_geometry((145.29664200454295, 177.5), 123), rounded])
    shape = unary_union([shape.difference(circle_geometry((-2.8072725530149967, -178.5), 102.5)),
                         Point(199.5, 200).buffer(165, quad_segs=8)])
    moved = affinity.translate(shape, 4992, 1525)
    assert isinstance(moved, Polygon)
    shape = orient(moved, 1.0)
    for ring in [shape.exterior, *shape.interiors]:
        _joined_and_simple([(float(x), float(y)) for x, y in list(ring.coords)[:-1]])


@pytest.mark.parametrize("quad", [16, 32])
def test_a_bump_where_a_small_circle_touches_a_large_one_from_inside_keeps_its_arc(quad: int):
    """Found by fuzzing: a circle of 0.5 touching one of 1 from inside pokes
    out of its coarser polygon in a tiny bump. Drawn with 16 segments a
    quarter, both its junctions went to the point the circles touch at, the
    bump's arc vanished and the drawn ring crossed itself; with 32, the
    point lay inside the bump's run, and its arc went the long way round."""
    from shapely.geometry import LineString
    from shapely.geometry.polygon import orient
    from shapely.ops import unary_union
    shape = unary_union([box(-0.5, -0.5, 0.5, 0.5), LineString([(0, 0), (0.5, 0)]).buffer(1, quad_segs=8),
                         Point(1, 0).buffer(0.5, quad_segs=quad)])
    assert isinstance(shape, Polygon)
    ring = [(float(x), float(y)) for x, y in list(orient(shape, 1.0).exterior.coords)[:-1]]
    _joined_and_simple(ring)


def test_a_rounded_corner_touching_a_large_circle_from_inside_does_not_close_into_a_circle():
    """Found by fuzzing: a rounded rectangle's corner of 0.5 touches a
    circle of 2 from inside, its bump starting on the point they touch at;
    its end went there too, and the arc came out a whole circle."""
    from shapely.geometry import LineString
    from shapely.geometry.polygon import orient
    from shapely.ops import unary_union
    from lang.core.cutouts import filleted
    rounded = filleted(box(-1, -2, 1, 2), 0.5)
    assert rounded is not None
    shape = unary_union([box(-0.5, -0.5, 0.5, 0.5), LineString([(0, 0), (0.5, 0)]).buffer(2, quad_segs=8), rounded])
    assert isinstance(shape, Polygon)
    ring = [(float(x), float(y)) for x, y in list(orient(shape, 1.0).exterior.coords)[:-1]]
    assert all(c.a != c.b for c in _joined_and_simple(ring) if isinstance(c, Arc2))


def test_a_line_running_into_an_arc_tangentially_is_no_chord_of_it():
    """Found by fuzzing: a notch cut 4 short of where a rounded rectangle's
    side runs into its corner arc left a piece of the side that lies as
    near the circle as a chord does; it was taken for one, and the arc ran
    on along its circle to the notch, bending the side 0.16 off. A chord
    lies inside its circle, a line touching it outside."""
    from shapely.geometry.polygon import orient
    from lang.core.cutouts import filleted
    rounded = filleted(box(0, 0, 200, 100), 50)
    assert rounded is not None
    notched = rounded.difference(box(145, 99, 146, 101))
    assert isinstance(notched, Polygon)
    shape = orient(notched, 1.0)
    curves = _joined_and_simple([(float(x), float(y)) for x, y in list(shape.exterior.coords)[:-1]])
    assert Line2((150, 100), (146, 100)) in curves
