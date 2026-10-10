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
        board("x", ply15).on(Pos("z", 1) + Pos("z", 2), side="top")


def test_mixing_axes_is_an_error():
    with pytest.raises(LangError):
        _ = Pos("x", 1) - Pos("z", 1)


def test_spread():
    assert spread(Pos("z", 0), Pos("z", 100), count=3) == [Pos("z", 0), Pos("z", 50), Pos("z", 100)]
    assert [p.value for p in spread(Pos("z", 0), Pos("z", 100), pitch=32)] == pytest.approx([2, 34, 66, 98])


# -- boxes --------------------------------------------------------------------

def test_box_sides_and_extents():
    b = Box.from_size(width=600, depth=500, height=720)
    assert b.left.axis == "y" and b.left.value == 600 and b.left.inward.name == "right"
    assert b.bottom.value == 0 and b.top.value == 720
    assert b.height == 720 and b.width == 600 and b.depth == 500
    bays = b.split("z", 3)
    assert [bay.bottom.value for bay in bays] == [0, 240, 480]


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
    assert left.box().hi["y"] == 600 and left.box().lo["y"] == 585
    assert left.inner.value == 585 and left.outer.value == 600
    assert left.right.value == 585  # global direction names work everywhere
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
    assert inner.left.value == 585 and inner.right.value == 15
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
        shelf = board("shelf", ply15).center(m.center("z"))
        with pytest.raises(LangError):
            shelf.inner
        assert shelf.top.value == 367.5


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
    left.cut(rect(60, 100), at="bottom.front", name="toekick")
    assert left.outline.area == pytest.approx(area_before - 60 * 100)
    toekick = left.op("toekick")
    assert isinstance(toekick, Cut)
    assert toekick.shape.bounds == pytest.approx((0, 0, 60, 100))
    assert left.toekick is toekick


def test_hole_anchor_offsets_and_positions():
    cab = carcass()
    left = cab["left"]
    left.hole(d=5, depth=10, face="inner", at=("front", 37, Pos("z", 300)))
    hole = left.ops[-1]
    assert isinstance(hole, Hole)
    assert (hole.u, hole.v) == pytest.approx((37, 300))
    assert hole.face == "right" and hole.depth == 10
    left.hole(d=5, depth=through, face="inner", at=("back.top", 20, 30))
    hole = left.ops[-1]
    assert isinstance(hole, Hole)
    assert (hole.u, hole.v) == pytest.approx((480, 690))
    assert hole.through and hole.depth == 15


def test_pocket_depth_to_face():
    cab = carcass()
    left = cab["left"]
    left.pocket(rect(200, 12), face="inner", at="center", depth=to("outer", -3))
    pocket = left.ops[-1]
    assert isinstance(pocket, Pocket)
    assert pocket.depth == pytest.approx(12)
    with pytest.raises(LangError):
        left.pocket(rect(10, 10), face="inner", depth=to("front"))


def test_edge_face_hole():
    cab = carcass()
    bottom = cab["bottom"]
    bottom.hole(d=8, depth=20, face="front", at=("left", 50))        # centred in the thickness
    op = bottom.ops[-1]
    assert isinstance(op, EdgeOp) and op.face == "front"
    assert (op.s, op.t) == pytest.approx((535, 7.5))
    bottom.hole(d=8, depth=20, face="front", at=("left.bottom", 50, 5))
    op = bottom.ops[-1]
    assert isinstance(op, EdgeOp)
    assert (op.s, op.t) == pytest.approx((535, 5))


def test_chamfer_targets():
    cab = carcass()
    left = cab["left"]
    left.chamfer("outline", 1).chamfer(left.front.inner, 1).chamfer("front.top", 0.5)
    assert [op.what for op in left.ops if isinstance(op, Chamfer)] == ["outline", "front.right", "front.top"]
    with pytest.raises(LangError):
        left.chamfer("nonsense", 1)


# -- layout --------------------------------------------------------------------

def test_layout_json_roundtrip(tmp_path: Path) -> None:
    from lang.core.layout import write_layout
    cab = carcass()
    cab["left"].cut(rect(60, 100), at="bottom.front", name="toekick")
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
