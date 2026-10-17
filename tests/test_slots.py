"""Slots (`Board.slot`): pockets with round ends, given by the centres of
their ends, as two anchors or as a centre with `centers=` and `along=`; and
the operation names a board keeps for itself."""
import math
from collections.abc import Callable

import pytest
from shapely.geometry import LineString

from lang import *
from lang.core.layout import build_layout
from lang.core.ops import Cut, Pocket, SlotLine
from lang.core.shapes import slot_shape
from lang.emit.plan import Arc, Line, PocketStep, plan_layout
from helpers import ply15

#: The module's box: x (depth) 0 to 300 from the front, y (width) 0 to 400 from the left, z 0 to 100.
BOX = Box.from_size(width=400, depth=300, height=100)


def _panel() -> tuple[Scope, Board]:
    """A board lying on the module's bottom, its top face (z 15) shown;
    its frame is (x, y)."""
    with module("m", BOX) as m:
        panel = board("panel", ply15).on(m.bottom).show(m.top)
    return m, panel


def _slot(panel: Board, name: str) -> Pocket:
    op = panel.op(name).op
    assert isinstance(op, Pocket) and op.slot is not None
    return op


# -- the two forms ------------------------------------------------------------------------------------

def test_a_slot_runs_between_the_centres_of_its_round_ends():
    m, panel = _panel()
    with m:
        top = panel.top
        panel.slot(8, top.front(40).left(100), top.front(40).left(300), depth=5, name="vent")
    op = _slot(panel, "vent")
    assert op.slot == SlotLine((40.0, 100.0), (40.0, 300.0), 8.0)
    assert (op.face, op.depth, op.depth_spec, op.chamfer) == ("top", 5, "5", 0)
    assert op.shape.geometry.symmetric_difference(slot_shape((40, 100), (40, 300), 8).geometry).area < 1e-9
    assert op.shape.area == pytest.approx(8 * 200 + math.pi * 4 ** 2, rel=1e-3)
    # a named slot's edges are positions, and it has a floor, as a pocket
    assert panel.vent.front == Pos("x", 36) and panel.vent.back == Pos("x", 44)
    assert panel.vent.left == Pos("y", 96) and panel.vent.right == Pos("y", 304)
    assert panel.vent.floor == Pos("z", 10)


def test_centers_and_along_give_a_slot_centred_on_at():
    m, panel = _panel()
    with m:
        top = panel.top
        panel.slot(8, at=top.front(40).left(200), centers=200, along="width", depth=5, name="by_extent")
        panel.slot(8, at=top.front(80).left(200), centers=200, along=m.left, depth=5, name="by_side")
        panel.slot(8, at=top.front(120).left(200), centers=200, along=panel.right, depth=5, name="by_face")
        panel.slot(8, at=top.front(160).left(200), centers=200, along=world_frame().direction("left"), depth=5,
                   name="by_direction")
        panel.slot(6, centers=20, along="depth", depth=3, name="centred")      # the show face's centre
    assert _slot(panel, "by_extent").slot == SlotLine((40.0, 100.0), (40.0, 300.0), 8.0)
    for name, x in (("by_side", 80.0), ("by_face", 120.0), ("by_direction", 160.0)):
        assert _slot(panel, name).slot == SlotLine((x, 100.0), (x, 300.0), 8.0)
    assert _slot(panel, "centred").slot == SlotLine((140.0, 200.0), (160.0, 200.0), 6.0)


def test_a_slot_may_lie_at_any_angle_and_its_ends_reach_fusion_as_arcs():
    m, panel = _panel()
    with m:
        top = panel.top
        panel.slot(10, top.front(50).left(50), top.front(150).left(120), depth=through, name="angled")
    op = _slot(panel, "angled")
    assert op.slot == SlotLine((50.0, 50.0), (150.0, 120.0), 10.0) and op.depth == 15
    ideal = LineString([(50, 50), (150, 120)]).buffer(5, quad_segs=256)
    assert op.shape.geometry.symmetric_difference(ideal).area < 0.05      # the chords of its arcs
    plan = plan_layout(build_layout())
    assert plan.problems == []
    (step,) = [s for s in plan.parts[0].steps if isinstance(s, PocketStep)]
    (loops,) = step.shapes
    (loop,) = loops
    arcs = [c for c in loop if isinstance(c, Arc)]
    assert len(arcs) == 2 and all(a.radius == pytest.approx(5) for a in arcs)
    assert len([c for c in loop if isinstance(c, Line)]) == 2


def test_two_anchors_on_one_axis_but_for_float_noise_make_a_straight_slot():
    m, panel = _panel()
    with m:
        top = panel.top
        panel.slot(8, top.front(40).left(100), top.front(40 + 1e-12).left(300), depth=5, name="vent")
        panel.slot(8, top.front(100).left(50), top.front(200).left(50 - 1e-12), depth=5, name="other")
    vent, other = _slot(panel, "vent").slot, _slot(panel, "other").slot
    assert vent is not None and other is not None
    assert vent.end[0] == vent.start[0] and other.end[1] == other.start[1]


def test_rows_of_slots_with_spread():
    m, panel = _panel()
    with m:
        top = panel.top
        for x in spread(panel.front.into(40), panel.back.into(40), pitch=20):
            panel.slot(6, at=top.front(x), centers=200, along="width", depth=through)
    slots = [op.slot for op in panel.ops if isinstance(op, Pocket) and op.slot is not None]
    assert [s.start[0] for s in slots] == [40 + 20 * i for i in range(12)]
    assert all((s.start[1], s.end[1]) == (100, 300) for s in slots)


def test_a_stepped_slot_is_two_slots_on_the_same_anchors():
    """The narrow part's end centres lie in the wide part, cut before: a
    slot's centres must be on the outline only, not on the face as a hole's."""
    m, panel = _panel()
    with m:
        top = panel.top
        a, b = top.front(60).left(100), top.front(60).left(140)
        panel.slot(12, a, b, depth=4, name="head")
        panel.slot(6, a, b, depth=through, name="shank", chamfer=0.5)
    assert (_slot(panel, "head").depth, _slot(panel, "shank").depth) == (4, 15)
    assert _slot(panel, "shank").chamfer == 0.5


def test_a_slot_takes_a_chamfer_and_is_chamfered_by_name():
    m, panel = _panel()
    with m:
        top = panel.top
        panel.slot(8, top.front(40).left(100), top.front(40).left(300), depth=5, name="a", chamfer=1)
        panel.slot(8, top.front(80).left(100), top.front(80).left(300), depth=5, name="b")
        panel.chamfer(panel.b, 0.5)
        with pytest.raises(LangError, match="must be smaller than 5"):
            panel.slot(8, top.front(120).left(100), top.front(120).left(300), depth=5, chamfer=5)
    assert _slot(panel, "a").chamfer == 1
    assert plan_layout(build_layout()).problems == []


def test_a_slot_runs_along_the_extent_its_cabinet_names():
    """In a cabinet opening toward the box's right, its width runs along
    the world's depth (x); the back's slot follows the cabinet's terms."""
    box = Box.from_size(width=600, depth=500, height=700)
    with module("cab", box, front=box.right) as cab:
        back = board("back", ply15).on(cab.back)
        back.slot(6, at=back.inner.center, centers=100, along="width", depth=through, name="vent")
    line = _slot(back, "vent").slot
    assert line is not None
    k = back.face_axes(back.inner).index(cab.frame.axis_of_extent("width"))
    assert cab.frame.axis_of_extent("width") == "x"
    assert abs(line.end[k] - line.start[k]) == pytest.approx(100) and line.end[1 - k] == line.start[1 - k]


def test_end_centres_on_the_board_edge_are_on_it():
    """A centre on the outline's edge, or within the tolerance of it, is on
    the board; the slot cuts what it reaches. Further off it is refused."""
    m, panel = _panel()
    with m:
        top = panel.top
        panel.slot(8, top.front(0).left(100), top.front(0).left(200), depth=5)
        panel.slot(8, top.front(-0.0005).left(250), top.front(-0.0005).left(350), depth=5)
        with pytest.raises(LangError, match="its start centre is off the board"):
            panel.slot(8, top.front(-0.002).left(100), top.front(40).left(100), depth=5)
    assert len(panel.ops) == 2


# -- refusals ------------------------------------------------------------------------------------------

def test_what_a_slot_refuses_leaves_the_board_as_it_was():
    m, panel = _panel()
    with m:
        other = board("other", ply15).on(m.top)
        top = panel.top
        a, b = top.front(40).left(100), top.front(40).left(300)
        cases: list[tuple[Callable[[], object], str]] = [
            (lambda: panel.slot(8, a, b, at=a, depth=5), "either two anchors"),    # type: ignore[call-overload]
            (lambda: panel.slot(8, a, depth=5), "give both anchors"),               # type: ignore[call-overload]
            (lambda: panel.slot(8, depth=5), "or centers= and along="),             # type: ignore[call-overload]
            (lambda: panel.slot(8, at=a, centers=20, depth=5), "or centers= and along="),  # type: ignore[call-overload]
            (lambda: panel.slot(8, a, panel.bottom.front(80), depth=5), "different faces, top and bottom"),
            (lambda: panel.slot(8, a, other.top.front(40), depth=5), "names a point on m.other"),
            (lambda: panel.slot(8, panel.front.left(50), panel.front.left(100), depth=5), "narrow face"),
            (lambda: panel.slot(8, at=panel.front.left(50), centers=20, along="width", depth=5), "narrow face"),
            (lambda: panel.slot(8, at=top.center, centers=20, along="height", depth=5), "does not lie in"),
            (lambda: panel.slot(8, at=top.center, centers=20, along="heigth", depth=5),   # type: ignore[arg-type]
             "slot\\(along=\\)"),
            (lambda: panel.slot(0.005, a, b, depth=5), "at least 0.01 mm wide"),
            (lambda: panel.slot(0, a, b, depth=5), "at least 0.01 mm wide"),
            (lambda: panel.slot(-8, a, b, depth=5), "at least 0.01 mm wide"),
            (lambda: panel.slot(8, at=top.center, centers=0.005, along="width", depth=5), "at least 0.01 mm apart"),
            (lambda: panel.slot(8, at=top.center, centers=-20, along="width", depth=5), "at least 0.01 mm apart"),
            (lambda: panel.slot(8, a, a, depth=5), "less than 0.01 mm"),
            (lambda: panel.slot(8, a, top.front(40).left(-10), depth=5), "its end centre is off the board"),
            (lambda: panel.slot(8, a, b, depth=20), "reaches past the opposite face"),
            (lambda: panel.slot(8, a, b, depth=5, chamfer=-1), "must not be negative"),
            (lambda: panel.slot(8, top.front(40).left(0), top.front(40).right(0), depth=through, name="split"),
             "the slot 'split' goes through the board and splits it"),
        ]
        for make, message in cases:
            with pytest.raises(LangError, match=message):
                make()
        assert panel.ops == []
        panel.cut(rect(depth=60, width=80), at=top.front.left, name="notch")
        with pytest.raises(LangError, match="its start centre is off the board"):
            panel.slot(8, top.front(30).left(40), top.front(30).left(200), depth=5)
    assert len(panel.ops) == 1 and isinstance(panel.ops[0], Cut) and panel.ops[0].name == "notch"


# -- names the board keeps ---------------------------------------------------------------------------

def test_operation_names_that_are_the_boards_own_are_refused():
    """`panel.slot` is the method, so an operation named "slot" could never
    be reached as `panel.slot`: such names are refused, for every kind of
    operation, and the refused operation is not kept."""
    m, panel = _panel()
    with m:
        top = panel.top
        for name in ("slot", "hole", "front", "outline", "inner", "name", "ops", "cutout", "dogbones"):
            with pytest.raises(LangError, match=f"operation name '{name}' is taken by the board itself "
                                                f"\\(panel\\.{name}\\)"):
                panel.pocket(rect(depth=20, width=20), at=top.center, depth=5, name=name)
        with pytest.raises(LangError, match="taken by the board itself"):
            panel.slot(8, top.front(40).left(100), top.front(40).left(300), depth=5, name="slot")
        with pytest.raises(LangError, match="taken by the board itself"):
            panel.hole(d=8, at=top.center, depth=5, name="top")
        with pytest.raises(LangError, match="taken by the board itself"):
            panel.cut(rect(depth=20, width=20), at=top.front.left, name="cut")
        assert panel.ops == [] and panel.outline.area == pytest.approx(300 * 400)
        assert panel.unique_op_name("slot") == "slot_2" and panel.unique_op_name("vent") == "vent"


def test_the_languages_own_default_names_are_not_the_boards():
    """A cutout without a name is "openings"; the reliefs of the outline's
    own corners (and of unnamed operations') are "outline_dogbones"."""
    m, panel = _panel()
    with m:
        panel.cut(rect(depth=60, width=80), at=panel.top.front.left)
        panel.dogbones()
        panel.cutout(border=100, depth=5)
    names = [op.name for op in panel.ops if isinstance(op, (Cut, Pocket)) and op.name]
    assert names[:2] == ["outline_dogbones", "openings"]
    assert panel.openings.floor == Pos("z", 5)          # from the bottom, the face not shown


# -- the layout ----------------------------------------------------------------------------------------

def test_the_layout_carries_a_slots_centre_line():
    m, panel = _panel()
    with m:
        top = panel.top
        panel.slot(8, top.front(40).left(100), top.front(40).left(300), depth=5, name="vent")
        panel.pocket(rect(depth=20, width=20), at=top.center, depth=5, name="square")
        panel.pocket(rect(depth=40, height=6), at=panel.right.center, depth=10, name="edge")
    layout = build_layout()
    assert layout["version"] >= 4          # slots came with version 4
    vent, square, edge = layout["modules"][0]["parts"][0]["ops"]
    assert vent["kind"] == "pocket" and vent["slot"] == {"start": [40.0, 100.0], "end": [40.0, 300.0], "width": 8.0}
    assert square["kind"] == "pocket" and square["slot"] is None
    assert edge["kind"] == "edge" and edge["op"]["kind"] == "pocket" and edge["op"]["slot"] is None
