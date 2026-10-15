"""The design checks: `no_interference` with hardware (bodies made of world
boxes against the parts' material and against each other), `fits_sheet`
and `inside(contour)`."""

from shapely.geometry import box as shapely_box

from lang import *
from lang.core.contours import Contour
from lang.core.layout_types import BoxDict, HardwareBodyLayout
from lang.core.scope import registry
from helpers import ply18


ply10 = sheet_material("birch", t=10)


def _box(lo: tuple[float, float, float], hi: tuple[float, float, float]) -> BoxDict:
    return {"min": list(lo), "max": list(hi)}


def _pin(u: float, v: float, side: float | tuple[float, float], z0: float, z1: float) -> BoxDict:
    """A pin centred on (u, v), `side` wide (along u and v), from z0 to z1."""
    su, sv = side if isinstance(side, tuple) else (side, side)
    return _box((u - su / 2, v - sv / 2, z0), (u + su / 2, v + sv / 2, z1))


def _body(name: str, *boxes: BoxDict) -> HardwareBodyLayout:
    return {"name": name, "boxes": list(boxes)}


def _panel() -> tuple[Scope, Board]:
    """An 18 mm panel on the bottom of a 300 x 300 x 100 box: z 0 to 18,
    its outline in (x, y)."""
    with module("m", Box.from_size(width=300, depth=300, height=100)) as m:
        panel = board("panel", ply18).on(m.bottom)
    return m, panel


def test_a_hardware_box_reaching_into_a_board_overlaps_it():
    m, _ = _panel()
    m.place_hardware("latch", [_body("core", _pin(60, 60, 20, 10, 30))])
    assert no_interference(m) == ["m.latch.core overlaps m.panel"]


def test_a_hardware_box_touching_a_board_does_not_overlap_it():
    m, _ = _panel()
    m.place_hardware("catch", [_body("holder", _box((50, 50, -14), (70, 70, 0))),     # under the panel
                               _body("plate", _box((-5, 100, 0), (0, 120, 18)))])     # against its edge
    assert no_interference(m) == []


def test_a_hardware_box_in_a_hole_overlaps_only_the_material_around_it():
    """Holes count as missing material where they span the box's range
    along the thickness: a through hole all of it, a blind hole down to its
    bottom, from its own face."""
    with module("m", Box.from_size(width=300, depth=300, height=100)) as m:
        panel = board("panel", ply18).on(m.bottom)
        for v in (50, 150, 250):
            panel.add_hole(panel.top, (50, v), 20, through)
        for v in (50, 150):
            panel.add_hole(panel.top, (150, v), 20, 10)          # down to z 8
        for v in (50, 150):
            panel.add_hole(panel.bottom, (250, v), 20, 10)       # up to z 10
    m.place_hardware("pins", [
        _body("through", _pin(50, 50, 10, -5, 25)),
        _body("corners_on_the_circle", _pin(50, 150, (16, 12), -5, 25)),
        _body("wider", _pin(50, 250, 22, -5, 25)),
        _body("deep_enough", _pin(150, 50, 10, 8, 25)),
        _body("too_deep", _pin(150, 150, 10, 7, 25)),
        _body("from_below", _pin(250, 50, 10, -5, 10)),
        _body("hole_on_the_other_face", _pin(250, 150, 10, 13, 25)),
    ])
    assert no_interference(m) == ["m.pins.wider overlaps m.panel", "m.pins.too_deep overlaps m.panel",
                                  "m.pins.hole_on_the_other_face overlaps m.panel"]


def test_a_part_in_a_through_hole_of_another_does_not_overlap_it():
    """Holes are missing material for parts too: a dowel standing in a
    through hole."""
    with module("m", Box.from_size(width=300, depth=300, height=100)) as m:
        panel = board("panel", ply18).on(m.bottom)
        panel.add_hole(panel.top, (50, 50), 20, through)
        board("dowel", ply10).on(Pos("x", 45), toward=m.back).between(Pos("y", 45), Pos("y", 55))
    assert no_interference(m) == []


def test_two_hardware_bodies_that_overlap_are_reported():
    """Any two bodies, of one item or of two, also in a scope below; bodies
    that only touch are not."""
    with module("m", Box.from_size(width=300, depth=300, height=100)) as m:
        board("panel", ply18).on(m.bottom)
        with scope("door") as door:
            pass
    m.place_hardware("hinge", [_body("cup", _box((0, 0, 50), (20, 20, 60))),
                               _body("arm", _box((10, 10, 55), (30, 30, 65)))])
    door.place_hardware("catch", [_body("ball", _box((25, 25, 60), (40, 40, 70)))])
    m.place_hardware("plate", [_body("plate", _box((40, 40, 60), (50, 50, 70)))])   # touches the ball
    assert no_interference(m) == ["m.hinge.cup overlaps m.hinge.arm", "m.hinge.arm overlaps m.door.catch.ball"]


def test_the_boxes_of_one_body_may_overlap_each_other():
    m, _ = _panel()
    m.place_hardware("runner", [_body("left", _box((0, 0, 50), (100, 20, 60)), _box((50, 0, 55), (150, 20, 70)),
                                      _box((0, 0, 18), (150, 5, 50)))])            # stands on the panel
    assert no_interference(m) == []


def test_a_part_as_large_as_its_sheet_fits_it_far_from_the_origin():
    """Its height is a difference of world coordinates, -976.9 less
    -1219.9, which comes out 1e-13 more than 243 [found by fuzzing,
    2026-10-14]."""
    with module("m", Box.from_size(width=300, depth=300, height=500, origin=(0, 0, -1220))) as m:
        b = board("b", sheet_material("birch", t=9, size=(57, 243))).on(m.left).between(
            m.bottom.into(0.1), m.bottom.into(243.1), m.front, m.front.into(57))
    assert b.outline.height > 243
    assert fits_sheet(m) == []
    with module("n", Box.from_size(width=300, depth=300, height=500)) as n:
        board("b", sheet_material("birch", t=9, size=(57, 243))).on(n.left).between(n.bottom, n.bottom.into(243.01),
                                                                               n.front, n.front.into(57))
    assert fits_sheet(n) == ["n.b (57 x 243.01) does not fit a 57 x 243 sheet"]


def test_a_pocket_and_a_hole_that_make_room_together_leave_a_pin_clear():
    """A pocket 10 deep from the top and a hole 8 deep from the bottom: a
    pin through both hits nothing, though neither spans the panel alone
    [found by fuzzing, 2026-10-14]; one wider than the hole hits the
    material around it."""
    with module("m", Box.from_size(width=300, depth=300, height=100)) as m:
        panel = board("panel", ply18).on(m.bottom)
        for x in (50, 150):
            panel.pocket(rect(depth=20, width=20), at=panel.top.front(x - 10).left(40), depth=10)   # down to z 8
            panel.add_hole(panel.bottom, (x, 50), 10, 8)                                          # up to z 8
    m.place_hardware("pins", [_body("through", _pin(50, 50, 6, -5, 25)), _body("wider", _pin(150, 50, 12, -5, 25))])
    assert no_interference(m) == ["m.pins.wider overlaps m.panel"]


def test_parallel_boards_with_room_made_in_each_do_not_overlap():
    """Two boards lapped where they overlap, each pocketed 4 deep from the
    face toward the other, 8 mm of their thicknesses shared: neither
    pocket spans the 8 mm, together they make room [found by fuzzing,
    2026-10-14]. Pocketed 3 deep each, they meet."""
    for depth, expected in ((4, []), (3, ["m.a overlaps m.b"])):
        registry.reset()
        with module("m", Box.from_size(width=100, depth=300, height=100)) as m:
            a = board("a", ply18).on(m.bottom).between(m.front, m.front.into(200))                 # z 0 to 18
            b = board("b", ply18).on(m.bottom.into(10)).between(m.front.into(100), m.back)             # z 10 to 28
            a.pocket(rect(depth=100, width=100), at=a.top.back, depth=depth)
            b.pocket(rect(depth=100, width=100), at=b.bottom.front, depth=depth)
        assert no_interference(m) == expected


def test_a_divider_notched_clear_of_the_material_beside_its_groove_does_not_overlap():
    """A divider standing 5 mm into a shelf, half of its end in a pocket 5
    deep and the other half notched clear of the shelf: each has material
    where the boxes meet, and their outlines cross, but not where the
    other's material is [found by fuzzing, 2026-10-14]. Without the notch
    it stands on the shelf's material beside the pocket."""
    for notched, expected in ((True, []), (False, ["m.shelf overlaps m.divider"])):
        registry.reset()
        with module("m", Box.from_size(width=300, depth=300, height=100)) as m:
            shelf = board("shelf", ply18).on(m.bottom)
            shelf.pocket(rect(depth=40, width=50), at=shelf.top.front(40).left, depth=5)      # x 40 to 80, y 0 to 50
            divider = board("divider", ply18).on(Pos("x", 50), toward=m.back).between(
                m.left, m.left.into(100), m.bottom.into(13), m.bottom.into(60))
            if notched:
                divider.cut(rect(width=50, height=6), at=divider.outer.right.bottom)           # y 50 to 100, z 13 to 19
        assert no_interference(m) == expected


def test_a_box_reaching_past_a_large_hole_overlaps_the_material_around_it():
    """A square pin in a 100 mm hole, its corners 0.05 past the circle,
    reaches into the panel; on the circle or inside it, it does not. The
    hole was drawn with 64 sides around the circle, which took up to 0.06
    mm more than the hole there [found by fuzzing, 2026-10-14]."""
    with module("m", Box.from_size(width=500, depth=500, height=100)) as m:
        panel = board("panel", ply18).on(m.bottom)
        for x in (100, 250, 400):
            panel.add_hole(panel.top, (x, 100), 100, through)
    m.place_hardware("pins", [_body(name, _pin(x, 100, 2 * (50 + past) / 2 ** 0.5, -5, 25))
                              for name, x, past in (("past", 100, 0.05), ("on", 250, 0.0), ("inside", 400, -0.01))])
    assert no_interference(m) == ["m.pins.past overlaps m.panel"]


def test_a_long_board_touching_a_contour_is_inside_it():
    """A board 2390 long, 1e-9 past the contour or into its clearance,
    touches it; by area, 2.39e-6 mm2 outside, it was not inside [found by
    fuzzing, 2026-10-14]. 0.001 past, it is not."""
    floor = Contour("floor", ((0, 0, 0), (2400, 0, 0), (2400, 1200, 0), (0, 1200, 0)), True, (0, 0, 0), (0, 0, 1))
    for gap in (0.0, 5.0):
        for past, expected in ((1e-9, []), (1e-3, ["m.b is not inside floor"])):
            registry.reset()
            with module("m", Box.from_size(width=1200, depth=2400, height=100)) as m:
                board("b", ply18).on(m.bottom).between(Pos("x", 5), Pos("x", 2395), Pos("y", gap - past), Pos("y", 600))
            assert [p.split(" with")[0].split(" (")[0] for p in inside(floor, gap=gap)(m)] == expected


def test_a_corner_poking_past_a_contour_is_outside_it_however_little_its_area():
    """Decided by Florian, 2026-10-14: `inside()` reports a part reaching
    more than 1e-6 mm past the contour, as `no_interference` counts an
    overlap that deep. It also needed more than 1e-6 mm2 outside, so a
    board's corner 1e-4 past the contour's chamfered corner, 5e-9 mm2,
    passed as inside."""
    floor = Contour("floor", ((0, 0, 0), (2400, 0, 0), (2400, 1100, 0), (2300, 1200, 0), (0, 1200, 0)), True,
                    (0, 0, 0), (0, 0, 1))
    for past, expected in ((5e-7, []), (1e-4, ["m.b is not inside floor"])):
        registry.reset()
        with module("m", Box.from_size(width=1200, depth=2400, height=100)) as m:
            board("b", ply18).on(m.bottom).between(Pos("x", 2245), Pos("x", 2350 + past), Pos("y", 1100), Pos("y", 1150))
        assert [p.split(" (")[0] for p in inside(floor)(m)] == expected, past


def test_a_part_is_outside_a_contour_its_clearance_leaves_nothing_of():
    """Found by fuzzing the checks: measured by how far it reaches past the
    contour less its clearance, a board 6 thick across a contour 6 high,
    with 5 mm of clearance, which leaves nothing, was inside (the distance
    to nothing is 0)."""
    wall = Contour("wall", ((0, -5, 0), (0, 45, 0), (0, 45, 6), (0, -5, 6)), True, (0, 0, 0), (1, 0, 0))
    with module("m", Box.from_size(width=40, depth=40, height=6)) as m:
        board("b", sheet_material("birch", t=6)).on(m.bottom)
    assert [p.split(" (")[0] for p in inside(wall, gap=5)(m)] == ["m.b is not inside wall with 5 mm clearance"]
    assert inside(wall, gap=2)(m) != [] and inside(wall)(m) == []


def test_a_board_whose_outline_only_touches_where_another_crosses_it_meets_nothing_there():
    """Found by fuzzing the placement: `no_interference` looks at boards
    across each other cell by cell, and a cell lying in a notch of a
    shelf's outline, touching it along the notch's edge only, met it in a
    line: the check failed ("Shape is not an area") instead of finding no
    material there."""
    with module("m", Box.from_size(width=600, depth=400, height=720)) as m:
        panel = board("panel", ply18).on(m.bottom)
        panel.add_cut(Shape(shapely_box(15, -1, 401, 9)))           # the front 9 mm notched away from x = 15
        board("side", sheet_material("birch", t=6)).on(m.left).between(m.front.into(15))   # within the notch
    assert no_interference(m) == []


def test_an_overlap_deeper_than_a_micrometre_counts_in_the_plane_as_across_the_thickness():
    """Decided by Florian, 2026-10-14: an overlap counts where it is deeper
    than 1e-6 mm in every direction, in a board's plane as across its
    thickness; touching is within 1e-6 mm. Two boards side by side 0.005
    into each other were not reported (what is narrower than 0.01 mm in a
    board's plane was cleaned away), two stacked 0.005 into each other
    were. Within 5e-7, neither is."""
    for into, expected in ((0.005, ["m.a overlaps m.side_by_side", "m.a overlaps m.stacked"]), (5e-7, [])):
        registry.reset()
        with module("m", Box.from_size(width=300, depth=600, height=100)) as m:
            board("a", ply18).on(m.bottom).between(m.front, m.front.into(200))                         # z 0 to 18
            board("side_by_side", ply18).on(m.bottom).between(m.front.into(200 - into), m.front.into(400))
            board("stacked", ply18).on(m.bottom.into(18 - into)).between(m.front, m.front.into(100))
        assert no_interference(m) == expected


def test_a_divider_or_a_box_a_little_into_a_board_overlaps_it():
    """Decided by Florian, 2026-10-14 (as above): a divider standing 0.005
    into a shelf, its end narrower than 0.01 mm in the divider's plane
    there, was not reported, nor a hardware box reaching 0.005 into the
    shelf's edge; both are. 5e-7 in, they touch."""
    for into, expected in ((0.005, ["m.shelf overlaps m.divider", "m.pin.pin overlaps m.shelf"]), (5e-7, [])):
        registry.reset()
        with module("m", Box.from_size(width=300, depth=300, height=100)) as m:
            board("shelf", ply18).on(m.bottom).between(m.front, m.front.into(200))                     # z 0 to 18
            board("divider", ply18).on(Pos("x", 50), toward=m.back).between(m.bottom.into(18 - into), m.top)
        m.place_hardware("pin", [_body("pin", _box((200 - into, 100, 5), (220, 120, 10)))])
        assert no_interference(m) == expected


def test_a_part_reaches_out_of_its_box_where_its_material_does():
    """Decided by Florian, 2026-10-14: `inside_box` takes a part's outline
    where it lies, not its placement box. A tenon grown 12 past the end of
    a shelf flush with the module's side reaches out of the module by 12
    (it was inside); a board placed 10 past the back, its last 10 cut off,
    does not (it reached out by 10)."""
    with module("m", Box.from_size(width=300, depth=300, height=200)) as m:
        shelf = board("shelf", ply18).on(m.bottom).between(m.left.into(20), m.right)
        shelf.add_to_outline(Shape(shapely_box(100, 290, 150, 312)))       # a tenon out of the right end (y)
        cut = board("cut", ply18).on(m.top).between(Pos("x", 0), Pos("x", 310))
        cut.add_cut(Shape(shapely_box(300, -1, 311, 301)))                  # its last 10 on x cut off
    assert inside_box(m) == ["m.shelf reaches out of m's box: right by 12"]


def test_a_part_across_a_contour_is_inside_it_where_its_material_is():
    """Decided by Florian, 2026-10-14: `inside()` takes a part across the
    contour's plane by its outline's extent and its thickness, not its
    placement box: a standing board with a tenon 5 past the contour is not
    inside it; one placed 10 past it, its last 10 cut off, is."""
    floor = Contour("floor", ((0, 0, 0), (300, 0, 0), (300, 300, 0), (0, 300, 0)), True, (0, 0, 0), (0, 0, 1))
    with module("m", Box.from_size(width=300, depth=300, height=200)) as m:
        tenoned = board("tenoned", ply18).on(m.left).between(Pos("x", 0), Pos("x", 300))       # y 0 to 18
        tenoned.add_to_outline(Shape(shapely_box(300, 50, 305, 80)))        # (x, z): 5 past the back on x
        cut = board("cut", ply18).on(m.right).between(Pos("x", 0), Pos("x", 310))
        cut.add_cut(Shape(shapely_box(300, -1, 311, 201)))                  # its last 10 on x cut off
    assert [p.split(" (")[0] for p in inside(floor)(m)] == ["m.tenoned is not inside floor"]
