from pathlib import Path

import pytest

from lang import *
from lang.core.ops import Chamfer, Cut, EdgeOp, Hole, Pocket
from lang.core.refs import Affine
from lang.core.scope import registry


@pytest.fixture(autouse=True)
def fresh_registry():
    registry.reset()
    yield
    registry.reset()


ply15 = material("birch", t=15)
ply9 = material("birch", t=9)


# -- position algebra ---------------------------------------------------------

def test_position_plus_length_is_position():
    p = Pos("z", 100) + 20
    assert p == Pos("z", 120)
    assert (Pos("z", 100) - 20) == Pos("z", 80)


def test_position_minus_position_is_length():
    assert Pos("z", 120) - Pos("z", 100) == 20


def test_mix_of_positions_needs_weights_summing_to_one():
    mid = (Pos("z", 100) + Pos("z", 200)) / 2
    assert mid == Pos("z", 150)
    assert isinstance(Pos("z", 100) + Pos("z", 200), Affine)
    with pytest.raises(LangError):
        # a bare sum of positions is not a position
        board("x", ply15).on(Pos("z", 1) + Pos("z", 2), toward=frame.direction("top"))


def test_mixing_axes_is_an_error():
    with pytest.raises(LangError):
        _ = Pos("x", 1) - Pos("z", 1)


def test_spread():
    assert spread(Pos("z", 0), Pos("z", 100), count=3) == [Pos("z", 0), Pos("z", 50), Pos("z", 100)]
    assert [p.value for p in spread(Pos("z", 0), Pos("z", 100), pitch=32)] == pytest.approx([2, 34, 66, 98])


# -- boxes --------------------------------------------------------------------

def test_box_sides_and_extents():
    b = Box.from_size(width=600, depth=500, height=720)
    assert b.left.axis == "y" and b.left.value == 0 and b.left.inward.name == "right"
    assert b.right.value == 600 and b.front.value == 0 and b.back.value == 500
    assert b.bottom.value == 0 and b.top.value == 720
    assert b.height == 720 and b.width == 600 and b.depth == 500
    bays = b.split("height", 3)
    assert [bay.bottom.value for bay in bays] == [0, 240, 480]
    first, rest = b.split("height", [230])
    assert (first.bottom.value, first.top.value) == (0, 230) and (rest.bottom.value, rest.top.value) == (230, 720)
    assert [(bay.bottom.value, bay.top.value) for bay in rest.split("height", 2)] == [(230, 475), (475, 720)]
    one, two, remainder = b.split("height", [230, 200])
    assert one.height == 230
    assert (two.bottom.value, two.top.value) == (230, 430) and remainder.bottom.value == 430
    gapped = b.split("width", [100], gap=20)
    assert [(bay.left.value, bay.right.value) for bay in gapped] == [(0, 100), (120, 600)]
    assert len(b.split("height", [360, 360])) == 2    # an exact fit has no remainder
    with pytest.raises(LangError):
        b.split("height", [500, 300])          # more than the box has
    moved = b.with_sides(front=Pos("x", 100), top=b.bottom + 50)
    assert moved.front.value == 100 and moved.top.value == 50
    with pytest.raises(TypeError):
        b.shrunk(lefft=5)  # type: ignore[call-arg]  -- a misspelt side is a type error


def test_split_runs_from_the_frames_own_side():
    box = Box.from_size(width=500, depth=600, height=720)
    with module("cab", box, front=box.right) as cab:
        first, rest = cab.interior.split("width", [100])
        assert first.left.value == cab.left.value and first.width == 100
        assert rest.right.value == cab.right.value


# -- placement ----------------------------------------------------------------

def carcass():
    with module("cab", Box.from_size(width=600, depth=500, height=720)) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        bottom = board("bottom", ply15).on(cab.bottom).between(left, right)
        board("back", ply9).on(cab.back).between(left, right, bottom, cab.top)
    return cab


def test_on_puts_thickness_inward():
    cab = carcass()
    left = cab["left"]
    assert left.t_axis == "y"
    assert left.box().lo["y"] == 0 and left.box().hi["y"] == 15
    assert left.inner.value == 15 and left.outer.value == 0
    assert left.right.value == 15  # direction names work on every part
    assert left.show_face.name == "left"


def test_between_parts_uses_nearest_faces_and_box_defaults():
    cab = carcass()
    bottom = cab["bottom"]
    assert bottom.box().lo["y"] == 15 and bottom.box().hi["y"] == 585
    assert bottom.box().lo["x"] == 0 and bottom.box().hi["x"] == 500  # defaults from the box
    back = cab["back"]
    assert back.box().lo["z"] == 15 and back.box().hi["z"] == 720
    assert back.t_axis == "x" and back.box().hi["x"] == 500 and back.box().lo["x"] == 491


def test_interior_is_inside_the_carcass():
    cab = carcass()
    inner = cab.interior
    assert inner.left.value == 15 and inner.right.value == 585
    assert inner.bottom.value == 15 and inner.top.value == 720
    assert inner.back.value == 491 and inner.front.value == 0


def test_placement_is_settable_once_and_frozen_after_use():
    with module("m", Box.from_size(100, 100, 100)) as m:
        b = board("a", ply15).on(m.left)
        with pytest.raises(LangError):
            b.on(m.right)
        b.box()
        with pytest.raises(LangError):
            b.inset(2)


def test_missing_placement_errors_with_path():
    with module("m", Box.from_size(100, 100, 100)):
        b = board("a", ply15)
        with pytest.raises(LangError) as info:
            b.box()
        assert info.value.path == "m.a"


def test_inner_outer_ambiguous_for_a_shelf_at_mid_height():
    with module("m", Box.from_size(600, 500, 720)) as m:
        shelf = board("shelf", ply15).center(m.center("height"))
        with pytest.raises(LangError):
            shelf.inner
        assert shelf.top.value == 367.5


def test_show_and_grain_take_objects():
    with module("m", Box.from_size(width=600, depth=500, height=720)) as m:
        a = board("a", ply15).on(m.left).show(m.right).grain("height")
        b = board("b", ply15).on(m.left).show("inner").grain(m.top)
        c = board("c", ply15).on(m.bottom)
        c.show(c.top).grain(c.front)
        d = board("d", ply15).on(m.bottom).show(m.front.outward)
    assert a.show_face.name == "right" and b.show_face.name == "right"
    assert a.to_layout()["grain"] == "z" and b.to_layout()["grain"] == "z"
    assert c.show_face.name == "top" and c.to_layout()["grain"] == "x"
    assert d.show_face.name == "front"
    with pytest.raises(LangError):
        c.show(a.top)   # another board's face


def test_scope_registration_and_paths():
    with module("cab", Box.from_size(600, 500, 720)) as cab:
        with scope("drawer1") as d:
            board("face", ply15).on(cab.front)
    assert cab.drawer1.face.path == "cab.drawer1.face"
    assert cab.drawer1.face is d.face


# -- operations ------------------------------------------------------------------

def test_cut_changes_outline_and_names_the_op():
    cab = carcass()
    left = cab["left"]
    area_before = left.outline.area
    left.cut(rect(depth=60, height=100), at=left.outer.bottom.front, name="toekick")
    assert left.outline.area == pytest.approx(area_before - 60 * 100)
    toekick = left.op("toekick")
    assert isinstance(toekick.op, Cut)
    assert toekick.op.shape.bounds == pytest.approx((0, 0, 60, 100))
    assert left.toekick.op is toekick.op


def test_named_operations_expose_their_edges():
    cab = carcass()
    left = cab["left"]
    left.cut(rect(depth=60, height=100), at=left.outer.bottom.front, name="toekick")
    assert left.toekick.top == Pos("z", 100) and left.toekick.bottom == Pos("z", 0)
    assert left.toekick.front == Pos("x", 0) and left.toekick.back == Pos("x", 60)
    with pytest.raises(LangError):
        left.toekick.left                     # a through cut has no extent in the thickness
    with pytest.raises(LangError):
        left.toekick.floor
    left.pocket(rect(depth=300, height=9.5), at=left.inner.bottom(20).front(12), depth=5, name="groove")
    assert left.groove.floor == Pos("y", 15 - 5) and left.groove.right == Pos("y", 15)
    assert left.groove.left == left.groove.floor
    assert left.groove.bottom == Pos("z", 20) and left.groove.top == Pos("z", 29.5)
    left.hole(d=8, depth=30, at=left.front.bottom(50), name="dowel")   # into the front narrow face
    assert left.dowel.floor == Pos("x", 30) and left.dowel.top == Pos("z", 54)
    # a board placed on a cut's edge, and bays above it
    with cab:
        bottom = board("bottom2", ply15).on(left.toekick.top, toward=cab.top).between(cab["left"], cab["right"])
    assert bottom.box().lo["z"] == 100 and bottom.box().hi["z"] == 115
    bays = cab.interior.with_sides(bottom=bottom.top).split("height", 2)
    assert bays[0].bottom.value == 115


def test_hole_anchor_offsets_and_positions():
    cab = carcass()
    left = cab["left"]
    left.hole(d=5, depth=10, at=left.inner.front(37).bottom(Pos("z", 300)))
    hole = left.ops[-1]
    assert isinstance(hole, Hole)
    assert (hole.u, hole.v) == pytest.approx((37, 300))
    assert hole.face == "right" and hole.depth == 10
    left.hole(d=5, depth=through, at=left.inner.back(20).top(30))
    hole = left.ops[-1]
    assert isinstance(hole, Hole)
    assert (hole.u, hole.v) == pytest.approx((480, 690))
    assert hole.through and hole.depth == 15
    left.hole(d=5, depth=10)   # the centre of the show face by default
    hole = left.ops[-1]
    assert isinstance(hole, Hole)
    assert (hole.u, hole.v, hole.face) == (250, 360, "left")


def test_anchor_errors_name_the_problem():
    cab = carcass()
    left, right = cab["left"], cab["right"]
    with pytest.raises(LangError):
        left.inner.left                     # the face's own axis is not an edge of it
    with pytest.raises(LangError):
        left.inner.front.back               # two edges on one axis
    with pytest.raises(LangError):
        left.inner.front(37)(5)             # a value given twice
    with pytest.raises(LangError):
        left.inner.center(5)                # nothing to measure from
    with pytest.raises(LangError):
        left.inner.front(Pos("z", 5))       # a position on the wrong axis
    with pytest.raises(LangError):
        left.hole(d=5, depth=5, at=right.inner.center)   # another board's face


def test_pocket_depth_to_face():
    cab = carcass()
    left = cab["left"]
    left.pocket(rect(depth=200, height=12), at=left.inner.center, depth=to(left.outer, -3))
    pocket = left.ops[-1]
    assert isinstance(pocket, Pocket)
    assert pocket.depth == pytest.approx(12)
    with pytest.raises(LangError):
        left.pocket(rect(depth=10, height=10), at=left.inner.center, depth=to(left.front))


def test_shapes_name_their_plane():
    cab = carcass()
    left, bottom = cab["left"], cab["bottom"]
    # a rect in the wrong plane for the face
    with pytest.raises(LangError):
        left.pocket(rect(width=10, height=10), at=left.inner.center, depth=3)
    # the same rect reads the same whichever way its extents were given
    bottom.pocket(rect(width=20, depth=100), at=bottom.top.front.left, depth=3)
    bottom.pocket(rect(depth=100, width=20), at=bottom.top.front.left, depth=3)
    a, b = bottom.ops[-2:]
    assert isinstance(a, Pocket) and isinstance(b, Pocket)
    assert a.shape.bounds == b.shape.bounds == (0.0, 15.0, 100.0, 35.0)
    with pytest.raises(LangError):
        rect(width=10)


def test_edge_face_hole():
    cab = carcass()
    bottom = cab["bottom"]
    bottom.hole(d=8, depth=20, at=bottom.front.left(50))        # centred in the thickness
    op = bottom.ops[-1]
    assert isinstance(op, EdgeOp) and op.face == "front"
    assert (op.s, op.t) == pytest.approx((65, 7.5))
    bottom.hole(d=8, depth=20, at=bottom.front.left(50).bottom(5))
    op = bottom.ops[-1]
    assert isinstance(op, EdgeOp)
    assert (op.s, op.t) == pytest.approx((65, 5))


def test_chamfer_targets():
    cab = carcass()
    left, right = cab["left"], cab["right"]
    left.cut(rect(depth=60, height=100), at=left.outer.bottom.front, name="toekick")
    left.hole(d=5, depth=5, at=left.inner.center)
    left.chamfer(left.outer.outline, 1).chamfer(left.front.inner, 1).chamfer(left.front.top, 0.5)
    left.chamfer(left.toekick, 1)
    chamfers = [op for op in left.ops if isinstance(op, Chamfer)]
    assert [op.what for op in chamfers] == ["outline", "front.right", "front.top", "toekick"]
    assert [op.face for op in chamfers] == ["left", "front", "front", "left"]
    with pytest.raises(LangError):
        left.chamfer(left.ops[1], 1)          # the unnamed hole
    with pytest.raises(LangError):
        left.chamfer(right.front.inner, 1)    # another board's edge


# -- layout --------------------------------------------------------------------

def test_layout_json_roundtrip(tmp_path: Path) -> None:
    from lang.core.layout import write_layout
    cab = carcass()
    cab["left"].cut(rect(depth=60, height=100), at=cab["left"].outer.bottom.front, name="toekick")
    cab.export("top", cab.top)
    cab.check(no_interference)
    layout = write_layout(tmp_path / "layout.json")
    assert layout["version"] == 1
    module_layout = layout["modules"][0]
    assert [p["path"] for p in module_layout["parts"]] == ["cab.left", "cab.right", "cab.bottom", "cab.back"]
    left = module_layout["parts"][0]
    assert left["axes"] == {"t": "y", "u": "x", "v": "z"}
    assert left["ops"][0]["kind"] == "cut"
    assert layout["problems"] == []


def test_box_grown_mirrors_shrunk():
    b = Box.from_size(width=100, depth=100, height=100)
    g = b.grown(top=0.5, left=1)
    assert g.hi["z"] == 100.5 and g.lo["y"] == -1 and g.hi["y"] == 100


def test_part_limits_into_and_gap():
    with module("box", Box.from_size(width=400, depth=300, height=100)) as m:
        left = board("left", ply15).on(m.left)
        right = board("right", ply15).on(m.right)
        floor = board("floor", ply9).on(m.bottom).between(left.into(5), right.gap(2))
    fb = floor.box()
    assert fb.lo["y"] == 15 - 5 and fb.hi["y"] == 385 - 2


def test_cut_with_a_perpendicular_part_is_a_pocket_from_the_entered_face():
    with module("box", Box.from_size(width=400, depth=300, height=100)) as m:
        side = board("side", ply15).on(m.left)
        floor = board("floor", ply9).on(m.bottom + 10).between(side.into(5), m.right, m.front + 12, m.back)
        side.cut(floor, name="groove")
        side.cut(floor.box().grown(top=0.5, left=0.5), name="roomy")
    groove, roomy = side.ops
    assert isinstance(groove, Pocket) and groove.face == "right" and groove.depth == 5
    assert groove.shape.bounds == (12.0, 10.0, 300.0, 19.0)
    assert groove.depth_spec == "cut(box.floor)"
    assert isinstance(roomy, Pocket) and roomy.depth == 5.5
    assert roomy.shape.bounds == (12.0, 10.0, 300.0, 19.5)


def test_cut_with_a_parallel_part_through_the_thickness_changes_the_outline():
    with module("box", Box.from_size(width=400, depth=300, height=100)) as m:
        shelf = board("shelf", ply15).on(m.bottom)
        block = board("block", ply15).on(m.bottom).between(m.left, m.left.into(50), m.front, m.front.into(15))
        shelf.cut(block, name="notch")
    notch = shelf.ops[0]
    assert isinstance(notch, Cut)
    assert shelf.outline.bounds == (0.0, 0.0, 300.0, 400.0)
    assert shelf.outline.area == 300 * 400 - 15 * 50


def test_cut_with_a_part_that_misses_or_floats_is_an_error():
    with module("box", Box.from_size(width=400, depth=300, height=100)) as m:
        side = board("side", ply15).on(m.left)
        away = board("away", ply9).on(m.bottom).between(m.right, m.right + 100)
        with pytest.raises(LangError):
            side.cut(away)
        with pytest.raises(LangError):
            side.cut(Box.from_size(width=5, depth=100, height=9, origin=(0, 390, 20)))
        with pytest.raises(LangError):
            side.cut(away, at=side.inner.center)   # at= belongs to shapes only


def test_module_frame_follows_placement():
    # a cabinet against the driver's wall (left, -y) that opens toward the aisle
    box = Box.from_size(width=500, depth=600, height=720)
    with module("cab", box, front=box.right) as cab:
        assert cab.front.value == 500 and cab.front.axis == "y"
        assert cab.back.value == 0
        # a cabinetmaker's left, standing in front of it: toward the vehicle's rear (+x)
        assert cab.left.axis == "x" and cab.left.value == 600 and cab.right.value == 0
        assert cab.top.value == 720
        assert cab.width == 600 and cab.depth == 500 and cab.height == 720
        back = board("back", ply9).on(cab.back)
        assert back.t_axis == "y" and back.box().hi["y"] == 9
        assert back.inner.name == "front" and back.inner.world_name == "right"
        back.hole(d=5, depth=5, at=back.inner.center)
        with scope("drawer1") as d:
            assert d.left.value == 600     # a child scope inherits the frame
            front = board("front", ply9).on(cab.front).between(cab.left.into(100), cab.right)
            assert front.box().lo["x"] == 0 and front.box().hi["x"] == 500
        assert rect(width=100, depth=50).axes == ("x", "y")
    layout_back = back.to_layout()
    assert layout_back["show"] == "left"
    op = layout_back["ops"][0]
    assert op["kind"] == "hole" and op["face"] == "right"   # world names in the layout
    assert not cab.frame.is_mirrored


def test_module_frame_mirrored_and_default():
    box = Box.from_size(width=500, depth=600, height=720)
    with module("cab", box, front=box.right, mirrored=True) as cab:
        assert cab.left.value == 0 and cab.right.value == 600 and cab.front.value == 500
        assert cab.frame.is_mirrored
    with module("plain", box) as plain:
        assert plain.left.value == 0 and plain.left.axis == "y"   # the world frame
    with pytest.raises(ValueError):
        module("up", box, front=box.top)


def test_interference_ignores_overlap_inside_a_pocket():
    with module("box", Box.from_size(width=400, depth=300, height=100)) as m:
        side = board("side", ply15).on(m.left)
        floor = board("floor", ply9).on(m.bottom + 10).between(side.inner.into(5), m.right)
        side.pocket(rect(depth=300, height=9.5), at=side.inner.bottom(floor.bottom).front,
                    depth=5, name="groove")
    assert no_interference(m) == []
    # a floor reaching deeper than the groove hits material
    with module("box2", Box.from_size(width=400, depth=300, height=100)) as m2:
        side = board("side", ply15).on(m2.left)
        floor = board("floor", ply9).on(m2.bottom + 10).between(side.inner.into(6), m2.right)
        side.pocket(rect(depth=300, height=9.5), at=side.inner.bottom(floor.bottom).front,
                    depth=5, name="groove")
    assert no_interference(m2) == ["box2.side overlaps box2.floor"]


# -- the face to machine from ------------------------------------------------------

def test_the_machine_face_is_the_one_with_the_operations():
    with module("cab", Box.from_size(width=600, depth=500, height=720)) as cab:
        plain = board("plain", ply15).on(cab.left)
        drilled = board("drilled", ply15).on(cab.right)
        drilled.hole(d=5, depth=10, at=drilled.inner.front(37).bottom(100))
        drilled.hole(d=5, depth=10, at=drilled.inner.front(37).bottom(132))
        drilled.chamfer(drilled.outer.outline, 1)          # one chamfer on the show face
    assert plain.machine_face.direction == plain.show_face.direction == plain.outer.direction
    assert drilled.machine_face.direction == drilled.inner.direction   # two holes beat one chamfer
    layout = drilled.to_layout()
    assert layout["machine"] == drilled.inner.world_name and layout["show"] == drilled.outer.world_name
    assert layout["grained"] is True


def test_a_tie_keeps_the_show_face_up():
    with module("cab", Box.from_size(width=600, depth=500, height=720)) as cab:
        side = board("side", ply15).on(cab.left)
        side.hole(d=5, depth=10, at=side.inner.center)
        side.hole(d=5, depth=10, at=side.outer.center)
    assert side.machine_face.direction == side.show_face.direction
