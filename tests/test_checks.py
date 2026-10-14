"""The design checks: `no_interference` with hardware (bodies made of world
boxes against the parts' material and against each other), and
`fits_sheet`."""

from lang import *
from lang.core.layout_types import BoxDict, HardwareBodyLayout
from helpers import ply18


ply10 = material("birch", t=10)


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
        b = board("b", material("birch", t=9, sheet=(57, 243))).on(m.left).between(
            m.bottom + 0.1, m.bottom + 243.1, m.front, m.front + 57)
    assert b.outline.height > 243
    assert fits_sheet(m) == []
    with module("n", Box.from_size(width=300, depth=300, height=500)) as n:
        board("b", material("birch", t=9, sheet=(57, 243))).on(n.left).between(n.bottom, n.bottom + 243.01,
                                                                               n.front, n.front + 57)
    assert fits_sheet(n) == ["n.b (57 x 243.01) does not fit a 57 x 243 sheet"]
