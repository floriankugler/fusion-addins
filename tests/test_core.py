import math
from pathlib import Path

import pytest
from shapely.geometry import Point

from lang import *
from lang.core.layout import build_layout
from lang.core.ops import Chamfer, Cut, EdgeOp, Hole, Pocket
from lang.core.refs import Affine
from lang.core.scope import registry
from lang.emit.plan import plan_layout
from helpers import ply15, ply9


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
        board("x", ply15).on(Pos("z", 1) + Pos("z", 2), toward=world_frame().direction("top"))


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
    with cabinet("cab", box, front=box.right) as cab:
        first, rest = cab.interior.split("width", [100])
        assert first.left.value == cab.left.value and first.width == 100
        assert rest.right.value == cab.right.value


# -- placement ----------------------------------------------------------------

def carcass(name: str = "cab"):
    with module(name, Box.from_size(width=600, depth=500, height=720)) as cab:
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
    left.hole(d=8, depth=30, at=left.front.bottom(150), name="dowel")  # into the front narrow face, above the toekick
    assert left.dowel.floor == Pos("x", 30) and left.dowel.top == Pos("z", 154)
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


def test_a_board_with_no_room_is_refused_wherever_the_module_lies():
    """Found by fuzzing the hardware: a top between two 20 mm sides in a
    40 mm box has no room, but with the box from 0.84 its extent came out
    20.84 to 20.840000000000003 and the board was built, 3.5e-15 mm wide.
    No board narrower than 0.01 mm is meant."""
    ply20 = material("birch", t=20)
    for name, y in (("at0", 0.0), ("at084", 0.84)):
        with module(name, Box.from_size(width=40, depth=300, height=400, origin=(0, y, 0))) as m:
            left = board("left", ply20).on(m.left)
            right = board("right", ply20).on(m.right)
            top = board("top", ply15).on(m.top).between(left, right)
        with pytest.raises(LangError, match=r"top: extent on y is not positive"):
            top.box()
    with module("narrow", Box.from_size(width=40.005, depth=300, height=400)) as m:
        left = board("left", ply20).on(m.left)
        right = board("right", ply20).on(m.right)
        top = board("top", ply15).on(m.top).between(left, right)
    with pytest.raises(LangError, match=r"top: extent on y is 0\.005 mm, less than 0\.01 \(20 to 20\.005\)\.$"):
        top.box()


def test_shapes_name_their_plane():
    cab = carcass()
    left, bottom = cab["left"], cab["bottom"]
    # a rect in the wrong plane for the face
    with pytest.raises(LangError):
        left.pocket(rect(width=10, height=10), at=left.inner.center, depth=3)
    # the same rect reads the same whichever way its extents were given
    other = carcass("other")["bottom"]
    bottom.pocket(rect(width=20, depth=100), at=bottom.top.front.left, depth=3)
    other.pocket(rect(depth=100, width=20), at=other.top.front.left, depth=3)
    a, b = bottom.ops[-1], other.ops[-1]
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
    bottom.hole(d=8, depth=20, at=bottom.front.left(150).bottom(5))
    op = bottom.ops[-1]
    assert isinstance(op, EdgeOp)
    assert (op.s, op.t) == pytest.approx((165, 5))


def test_chamfer_targets():
    cab = carcass()
    left, right = cab["left"], cab["right"]
    left.cut(rect(depth=60, height=100), at=left.outer.bottom.front, name="toekick")
    left.hole(d=5, depth=5, at=left.inner.center)
    area = left.outline.area
    left.chamfer(left.outer.outline, 1).chamfer(left.front.inner, 1).chamfer(left.front.top, 0.5)
    left.chamfer(left.toekick, 1)
    chamfers = [op for op in left.ops if isinstance(op, Chamfer)]
    # front.top runs through the board: a corner of the outline, cut off in it
    assert [op.what for op in chamfers] == ["outline", "front.right", "toekick"]
    assert [op.face for op in chamfers] == ["left", "front", "left"]
    assert left.outline.area == pytest.approx(area - 0.5 * 0.5 ** 2)
    with pytest.raises(LangError):
        left.chamfer(left.ops[1], 1)          # the unnamed hole
    with pytest.raises(LangError):
        left.chamfer(right.front.inner, 1)    # another board's edge


# -- layout --------------------------------------------------------------------

def test_layout_json_roundtrip(tmp_path: Path) -> None:
    from lang.core.layout import write_layout
    cab = carcass()
    cab["left"].cut(rect(depth=60, height=100), at=cab["left"].outer.bottom.front, name="toekick")
    cab.export("worktop", cab.top)
    cab.check(no_interference)
    layout = write_layout(tmp_path / "layout.json")
    assert layout["version"] == 3
    module_layout = layout["modules"][0]
    assert module_layout["exports"] == {"worktop": {"axis": "z", "value": 720.0}}
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
    with cabinet("cab", box, front=box.right) as cab:
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
    # the names the build file uses, by world name, for the preview's labels
    assert layout_back["faces"] == {"right": ["front", "inner"], "left": ["back", "outer"],
                                    "back": ["left"], "front": ["right"], "top": ["top"], "bottom": ["bottom"]}


def test_face_names_leave_out_inner_and_outer_when_ambiguous():
    with module("cab", Box.from_size(width=500, depth=600, height=720)) as cab:
        shelf = board("shelf", ply15).on(cab.bottom + 355)    # straddles the middle at 360
    assert shelf.to_layout()["faces"]["top"] == ["top"]
    assert all(len(names) == 1 for names in shelf.to_layout()["faces"].values())


def test_module_frame_mirrored_and_default():
    box = Box.from_size(width=500, depth=600, height=720)
    with cabinet("cab", box, front=box.right, mirrored=True) as cab:
        assert cab.left.value == 0 and cab.right.value == 600 and cab.front.value == 500
        assert cab.frame.is_mirrored
    with module("plain", box) as plain:
        assert plain.left.value == 0 and plain.left.axis == "y"   # the world frame
    with pytest.raises(LangError, match="front= must face sideways; top is up or down"):
        cabinet("up", box, front=box.top)


def test_a_module_that_opens_toward_a_side_is_a_cabinet():
    """Florian 2026-10-12: cabinet(name, box, front=) for anything that
    opens toward a side, module(name, box) for van-level parts in the
    enclosing frame; module(front=) points to cabinet()."""
    van = Box.from_size(width=2000, depth=1000, height=1000)
    with cabinet("cab", van, front=van.right) as cab:
        assert cab.is_module and cab.frame.direction("front").code == "+y"
        assert cab.frame.direction("left").code == "+x"          # a cabinetmaker's, facing it: front x up
    with module("floor", van) as floor:
        assert floor.frame.direction("left").code == "-y"        # the van's: the driver's side
    with pytest.raises(LangError, match=r"write cabinet\('kitchen', box, front=\.\.\.\)"):
        module("kitchen", van, front=van.right)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="front"):
        cabinet("cab2", van)  # type: ignore[call-arg]


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


def test_interference_of_parallel_parts_follows_their_outlines():
    """A hatch with rounded corners in a rounded opening, 3 mm clear all
    round: the boxes overlap in the corners, the material does not. A
    square hatch of the same size hits the panel in the corners."""
    for name, hatch_shape, expected in (("round", rect(width=394, depth=294).rounded(17), []),
                                        ("square", rect(width=394, depth=294), ["square.panel overlaps square.hatch"])):
        with module(name, Box.from_size(width=800, depth=600, height=15)) as m:
            panel = board("panel", ply15).on(m.bottom)
            panel.cut(rect(width=400, depth=300).rounded(20), at=panel.top.center, name="opening")
            limits: list[Pos] = []
            for a, b in ((panel.opening.front, panel.opening.back), (panel.opening.left, panel.opening.right)):
                lo, hi = sorted((a.value, b.value))
                limits += [Pos(a.axis, lo + 3), Pos(a.axis, hi - 3)]
            board("hatch", ply15, hatch_shape).on(m.bottom).between(*limits)
        assert no_interference(m) == expected


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


# -- review fixes 2026-10-12: limits ------------------------------------------------

def _partitions() -> tuple[Scope, Board, Board]:
    """Two partitions, both left of the middle of a 1000 wide box: y
    100..115 and 300..315."""
    with module("m", Box.from_size(width=1000, depth=400, height=700)) as m:
        p1 = board("p1", ply15).on(m.left + 100, toward=m.right)
        p2 = board("p2", ply15).on(m.left + 300, toward=m.right)
    return m, p1, p2


def test_between_two_parts_takes_the_faces_that_face_each_other():
    """The box's middle (y 500) lies right of both partitions; the shelf
    still runs from the first one's right face to the second one's left
    face, not through the second one."""
    m, p1, p2 = _partitions()
    with m:
        shelf = board("shelf", ply15).on(m.bottom + 300, toward=m.top).between(p1, p2)
        check(no_interference)
    assert (shelf.box().lo["y"], shelf.box().hi["y"]) == (115, 300)
    assert build_layout()["problems"] == []


def test_between_a_part_and_a_position_takes_the_face_toward_the_position():
    m, p1, p2 = _partitions()
    with m:
        shelf = board("shelf", ply15).on(m.bottom + 300, toward=m.top).between(m.left, p2.gap(1))
        reach = board("reach", ply15).on(m.bottom + 400, toward=m.top).between(p1.into(5), m.right)
    assert (shelf.box().lo["y"], shelf.box().hi["y"]) == (0, 299)      # p2's left face, 1 away from it
    assert (reach.box().lo["y"], reach.box().hi["y"]) == (110, 1000)   # p1's right face, 5 into it


def test_a_box_as_a_limit_gives_both_ends_on_each_in_plane_axis():
    drawer = Box.from_size(width=300, depth=400, height=150, origin=(20, 30, 40))
    with module("m", Box.from_size(width=600, depth=500, height=300)):
        side = board("side", ply15).on(drawer.left).between(drawer)
        long = board("long", ply15).on(drawer.left).between(drawer.front, drawer.back, drawer.bottom, drawer.top)
    assert side.box().as_dict() == long.box().as_dict()
    assert side.box().as_dict() == {"min": [20, 30, 40], "max": [420, 45, 190]}


def test_a_limit_that_limits_neither_in_plane_axis_is_an_error():
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        parallel = board("parallel", ply15).on(m.left + 100, toward=m.right).between(left)
        thick = board("thick", ply15).on(m.bottom + 100, toward=m.top).between(left, Pos("z", 50))
    with pytest.raises(LangError, match="m.left is parallel to this board"):
        parallel.box()
    with pytest.raises(LangError, match=r"lies on the board's thickness axis \(z\)"):
        thick.box()


# -- review fixes: faces in another frame ---------------------------------------------

def test_directions_are_equal_when_they_point_the_same_way():
    van = Box.from_size(width=2000, depth=1000, height=1000)
    with cabinet("cab", van, front=van.right) as cab:
        assert cab.frame.direction("front") == world_frame().direction("right")
        assert cab.frame.direction("front").name == "front"
        assert cab.frame.cross(cab.frame.direction("back"), cab.frame.direction("top")).name == "right"


def test_show_takes_a_side_of_an_enclosing_box_in_its_own_terms():
    """The van's right is this cabinet's front. A back shown toward it
    (`show(van.right)`) shows its front face; machined from the other one,
    which carries the holes, and cut out from it by default."""
    van = Box.from_size(width=2000, depth=1000, height=1000)
    with cabinet("cab", van, front=van.right) as cab:
        back = board("back", ply15).on(cab.back).show(van.right)
        rear = back.back
        back.hole(d=5, at=rear.top(20), depth=5).hole(d=5, at=rear.top(60), depth=5)
    assert back.show_face.name == "front" and back.show_face.world_name == "right"
    assert back.machine_face.name == "back"
    assert back.face(world_frame().direction("left")).name == "back"     # named in the cabinet's frame


# -- review fixes: depths --------------------------------------------------------------

def test_a_depth_past_the_opposite_face_is_an_error():
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        with pytest.raises(LangError, match="depth 40 reaches past the opposite face, 15 from"):
            left.hole(d=5, at=left.inner.center, depth=40)
        with pytest.raises(LangError, match="reaches past the opposite face, 400 from the front face"):
            left.hole(d=5, at=left.front.center, depth=401)
        with pytest.raises(LangError, match="reaches past that face"):
            left.pocket(rect(depth=50, height=50), at=left.inner.center, depth=to(left.outer, 1))
        left.hole(d=5, at=left.inner.center, depth=15)            # as deep as the board: fine
        left.hole(d=5, at=left.front.bottom(50), depth=400)
    assert len(left.ops) == 2


def test_to_names_a_face_of_the_board_itself():
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        bottom = board("bottom", ply15).on(m.bottom).between(left, m.right)
        with pytest.raises(LangError, match=r"to\(m.left.right\) names a face of another part"):
            bottom.pocket(rect(depth=50, width=50), at=bottom.top.center, depth=to(left.inner, -3))
        bottom.pocket(rect(depth=50, width=50), at=bottom.top.center, depth=to(bottom.bottom, -3))
    assert isinstance(bottom.ops[0], Pocket) and bottom.ops[0].depth == 12


def test_through_a_narrow_face_reaches_across_the_board():
    """The left side is 400 deep (x): a hole through its front face is 400
    deep, in the layout as in the plan."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        left.hole(d=8, at=left.front.bottom(50), depth=through, name="pin")
        left.pocket(rect(width=5, height=20), at=left.back.center, depth=through, name="slot")
    hole, slot = (op.op for op in left.ops if isinstance(op, EdgeOp))
    assert isinstance(hole, Hole) and isinstance(slot, Pocket)
    assert (hole.depth, hole.through, slot.depth) == (400, True, 400)
    edge = build_layout()["modules"][0]["parts"][0]["ops"][0]
    assert edge["kind"] == "edge" and edge["op"]["depth"] == 400


def test_pocket_and_hole_need_their_depth():
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        with pytest.raises(TypeError, match="depth"):
            left.pocket(rect(depth=50, height=50), left.inner.center)  # type: ignore[call-arg]
        with pytest.raises(TypeError, match="depth"):
            left.hole(5, left.inner.center)  # type: ignore[call-arg]


def test_fillet_takes_a_radius():
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom)
        panel.fillet(panel.front.left, radius=20)
    assert panel.outline.area == pytest.approx(400 * 300 - (1 - math.pi / 4) * 400)


# -- review fixes: scopes --------------------------------------------------------------

def test_an_export_must_not_be_hidden_by_the_scope():
    with module("cab", Box.from_size(width=600, depth=500, height=720)) as cab:
        top = board("top", ply15).on(cab.top)
        for taken in ("top", "up", "width", "interior", "mount", "parts", "_secret"):
            with pytest.raises(LangError, match=f"export '{taken}'"):
                cab.export(taken, top.top)
        cab.export("worktop", top.top)
    assert cab.worktop.position == top.top.position == Pos("z", 720)


def test_the_interior_counts_parts_that_cover_a_side_s_middle():
    """A foot in a corner of the bottom does not raise the interior; the
    bottom board does."""
    with module("cab", Box.from_size(width=600, depth=500, height=720)) as cab:
        board("foot", ply15).on(cab.bottom).between(cab.left, cab.left + 50, cab.front, cab.front + 50)
        assert cab.interior.lo["z"] == 0
        board("bottom", ply15).on(cab.bottom).between(cab.left + 100, cab.right)
        assert cab.interior.lo["z"] == 15


def test_problems_are_listed_once():
    """The module lists its own; the layout lists all of them once, and
    the emitter's plan reports each once."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        board("a", ply15).on(m.left)
        board("b", ply15).on(m.left + 5, toward=m.right)
        check(no_interference)
    layout = build_layout()
    assert layout["problems"] == ["m.a overlaps m.b"] == layout["modules"][0]["problems"]
    assert plan_layout(layout).problems == ["m.a overlaps m.b"]


# -- review fixes: the world frame, spread, boxes, joins -------------------------------------

def test_the_world_frame_is_read_through_a_function_and_reset_with_the_build():
    import lang
    assert not hasattr(lang, "frame") and "registry" not in lang.__all__
    set_frame(Frame(front="+y", left="+x", top="+z"))
    assert world_frame().direction("front").code == "+y"
    assert Box.from_size(width=10, depth=20, height=30).hi == {"x": 10, "y": 20, "z": 30}
    registry.reset()
    assert world_frame().direction("front").code == "-x"


def test_spread_takes_pitch_or_count():
    with pytest.raises(LangError, match="pitch= or count=, not both"):
        spread(Pos("z", 0), Pos("z", 100), pitch=32, count=3)


def test_positions_are_not_numbers():
    with pytest.raises(TypeError):
        float(Pos("z", 12.5))  # type: ignore[arg-type]


def test_boxes_without_a_common_region_have_no_intersection():
    a = Box({"x": 0, "y": 0, "z": 0}, {"x": 10, "y": 10, "z": 10})
    b = Box({"x": 20, "y": 0, "z": 0}, {"x": 30, "y": 10, "z": 10})
    with pytest.raises(LangError, match="no region in common"):
        a.intersection(b)
    assert a.intersection(Box({"x": 10, "y": 0, "z": 0}, {"x": 30, "y": 10, "z": 10})).lo["x"] == 10   # touching


def test_a_failed_join_changes_no_board():
    """The second tenon would split the side in two; the first one has
    grown the shelf's outline by then. Neither board keeps anything."""
    with module("unit", Box.from_size(width=600, depth=300, height=800)) as u:
        left = board("left", ply15).on(u.left)
        shelf = board("shelf", ply15).on(Pos("z", 400), toward=u.top).between(left, u.right)
        before = (shelf.outline.area, left.outline.area, list(shelf.ops), list(left.ops))
        with pytest.raises(LangError, match="splits the board"):
            shelf.join(left, using=tenons(width=300, at=[Pos("x", 150)]))
    assert (shelf.outline.area, left.outline.area, shelf.ops, left.ops) == before
    with u:
        shelf.join(left, using=tenons(count=1, width=50))     # and it can still be joined
    assert shelf.outline.area > before[0]


def test_parts_of_and_polygons_of():
    from shapely.geometry import GeometryCollection, LineString, Point as P, Polygon
    from lang.core.geometry import parts_of, polygons_of
    square = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    mixed = GeometryCollection([square, LineString([(0, 0), (2, 2)]), P(5, 5), Polygon()])
    assert polygons_of(mixed) == [square] and polygons_of(LineString([(0, 0), (1, 1)])) == []
    assert len(parts_of(mixed)) == 3 and parts_of(square) == [square] and parts_of(Polygon()) == []


def test_an_operation_that_misses_the_board_is_an_error():
    """Found compiling fuzz boards in Fusion: holes, pockets and V-grooves
    wholly where a rounded corner took the board away, holes whose centre
    lies off the board, and holes into a narrow face where the outline does
    not reach it, were accepted, and Fusion found nothing to cut. A hole
    partly on the board, its centre on it, is fine."""
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15, rect(depth=300, width=400).rounded(100)).on(m.bottom)
        with pytest.raises(LangError, match="lies off the board"):
            panel.hole(d=8, at=panel.top.front(5).left(5), depth=5)          # in the rounded-off corner
        with pytest.raises(LangError, match="centre off the top face"):
            panel.hole(d=60, at=panel.top.front(20).left(20), depth=5)      # partly on, its centre off
        panel.hole(d=60, at=panel.top.front(35).left(35), depth=5)          # partly on, its centre on
        with pytest.raises(LangError, match="front face where the board has none"):
            panel.hole(d=8, at=panel.front.left(20), depth=10)             # the front face starts 100 in
        panel.hole(d=8, at=panel.front.left(150), depth=10)
    assert [op.kind for op in panel.ops] == ["hole", "edge"]


def test_an_operation_whose_material_other_operations_took_is_an_error():
    """Found compiling fuzz boards in Fusion: a cut made after a hole took
    away all of the board around it, and a hole into a narrow face had its
    centre in a larger hole made there before; Fusion found nothing to cut
    for either. A cut taking part of a hole is fine."""
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom)
        panel.hole(d=8, at=panel.top.front(20).left(20), depth=5, name="pin")
        with pytest.raises(LangError, match="the cut takes the board away from the hole 'pin' made before, which "
                                            "then lies off the board"):
            panel.cut(rect(depth=50, width=50), at=panel.top.front(0).left(0))
        with pytest.raises(LangError, match="takes the board away from the hole 'pin' made before, which then has "
                                            "its centre off the top face"):
            panel.cut(rect(depth=22, width=50), at=panel.top.front(0).left(0))      # takes its centre
        panel.cut(rect(depth=18, width=50), at=panel.top.front(0).left(0))         # its centre stays
        panel.hole(d=18, depth=35, at=panel.back.left(200), name="dowel")
        with pytest.raises(LangError, match="has its centre in the hole 'dowel', made into the back face before"):
            panel.hole(d=9.5, depth=17, at=panel.back.left(202))
        panel.hole(d=8, depth=20, at=panel.back.left(220))                        # clear of it
    assert [op.kind for op in panel.ops] == ["hole", "cut", "edge", "edge"]


def test_a_pocket_through_the_board_may_not_split_it():
    """Found compiling fuzz boards in Fusion: a through pocket cut a board
    in two, which a through cut may not; Fusion made two bodies."""
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom)
        panel.pocket(rect(depth=10, width=380), at=panel.top.front(150).left(0), depth=through)   # leaves 20
        with pytest.raises(LangError, match="splits it in pieces"):
            panel.hole(d=30, at=panel.top.front(155).left(390), depth=through)   # takes the 20 left
        with pytest.raises(LangError, match="splits it in pieces"):
            panel.pocket(rect(depth=10, width=400), at=panel.top.front(250).left(0), depth=through)
    assert len(panel.ops) == 1


def test_a_pocket_through_the_board_may_not_leave_nothing_of_it():
    """Found by fuzzing dog bones: a circle pocket through a 53 mm square
    board, wider than the board, took all of it, which a cut may not, and
    the preview could not mesh what was left."""
    with module("m", Box.from_size(width=53, depth=53, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom)
        with pytest.raises(LangError, match=r"^m\.panel: a pocket goes through the board and leaves nothing of it\.$"):
            panel.pocket(circle(119), at=panel.top.center, depth=through)
        with pytest.raises(LangError, match="the hole 'big' goes through the board and leaves nothing of it"):
            panel.hole(d=80, at=panel.top.center, depth=through, name="big")
    assert panel.ops == []


def test_a_pocket_or_groove_with_nothing_left_to_cut_is_refused():
    """Found compiling fuzz boards in Fusion: the same V-groove made twice
    was accepted, and Fusion found nothing for the second one to cut. A
    pocket or V-groove wholly in what was cut from its face before, as deep,
    or in a pocket or hole through the board, has nothing to cut; one
    deeper, from the other face or partly beside it still cuts."""
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom)
        top, bottom = panel.top, panel.bottom
        panel.add_vgroove(top, (50, 50), (250, 50), 3, name="groove")
        with pytest.raises(LangError, match=r"^m\.panel: the vgroove 'again' lies wholly in what was cut from that "
                                            r"face before, as deep or through: it has nothing to cut\.$"):
            panel.add_vgroove(top, (50, 50), (250, 50), 3, name="again")
        panel.add_vgroove(top, (60, 50), (240, 50), 4)                      # deeper
        panel.add_pocket(top, Shape(Point(150, 200).buffer(50)), 6, name="dish")
        with pytest.raises(LangError, match="^m\\.panel: a pocket lies wholly in what was cut"):
            panel.add_pocket(top, Shape(Point(150, 200).buffer(20)), 6)
        panel.add_pocket(top, Shape(Point(150, 200).buffer(20)), 8)         # deeper
        panel.add_pocket(bottom, Shape(Point(150, 200).buffer(20)), 4)      # from the other face
        panel.add_pocket(top, Shape(Point(150, 140).buffer(20)), 4)         # partly beside the dish
        panel.add_hole(top, (250, 300), 30, through, name="bore")
        with pytest.raises(LangError, match="nothing to cut"):
            panel.add_pocket(bottom, Shape(Point(250, 300).buffer(10)), 2)  # in the hole through
    assert len(panel.ops) == 7


def test_a_cut_may_not_leave_only_what_through_pockets_take():
    """Found by fuzzing cutouts: with border 0 a cutout took all of a board
    but the corner a through pocket had already taken, which left a board
    of nothing."""
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom)
        panel.pocket(rect(depth=20, width=400), at=panel.top.front(0).left(0), depth=through)
        with pytest.raises(LangError, match="nothing of the board but what pockets and holes through it take"):
            panel.cut(rect(depth=280, width=400), at=panel.top.back(0).left(0))
    assert len(panel.ops) == 1 and panel.outline.area == pytest.approx(400 * 300)


def test_an_operation_refused_for_its_name_is_not_kept():
    """Found while ordering the checks: an operation whose name was taken
    was refused, but stayed among the board's operations."""
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom)
        panel.hole(d=5, at=panel.top.front(50), depth=5, name="a")
        with pytest.raises(LangError, match="used twice"):
            panel.hole(d=5, at=panel.top.front(100), depth=5, name="a")
    assert len(panel.ops) == 1


def test_a_chamfer_under_a_hundredth_of_a_millimetre_is_an_error():
    """Found compiling fuzz boards in Fusion: chamfers of 6e-5 and 2e-8 mm
    were accepted, and Fusion failed on them. Every way to make a chamfer
    refuses one under `MIN_CHAMFER`; 0 is none, and a refused cutout
    leaves nothing behind."""
    from lang.core.ops import MIN_CHAMFER
    tiny = MIN_CHAMFER / 2
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom)
        for make in (lambda: panel.hole(d=8, at=panel.top.front(50).left(50), depth=5, chamfer=tiny),
                     lambda: panel.pocket(rect(depth=20, width=20), at=panel.top.center, depth=5, chamfer=tiny),
                     lambda: panel.cut(rect(depth=20, width=20), at=panel.top.center, chamfer=tiny),
                     lambda: panel.hole(d=8, at=panel.front.left(100), depth=20, chamfer=tiny),
                     lambda: panel.chamfer(panel.top.outline, tiny),
                     lambda: panel.chamfer(panel.front.left, tiny),
                     lambda: panel.cutout(depth=5, chamfer=tiny)):
            with pytest.raises(LangError, match="too small to make"):
                make()
        assert panel.ops == [] and panel.outline.area == pytest.approx(400 * 300)
        panel.hole(d=8, at=panel.top.front(50).left(50), depth=5, chamfer=MIN_CHAMFER)
        panel.chamfer(panel.top.outline, 0.5)
    assert [op.kind for op in panel.ops] == ["hole", "chamfer"]
