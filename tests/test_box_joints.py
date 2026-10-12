"""Box joints (`lang.joints.box_joints`), as the box_joint add-in makes them.

The corner: board `a` (15 thick, y 0..15, x 0..200, z 0..150) is met by
board `b` (12 thick, x 0..12, y 15..200), whose end lies on a's inner face
at y 15; a's end at x 0 is flush with b's outer face. b grows the fingers
through a, a gets the notches. With 5 fingers and a margin of 5 on the
150 mm joint every finger is 28 wide: a's at z 5..33 (with the margin
0..33), 61..89, 117..145 (..150), b's at 33..61 and 89..117.
"""
import math
from collections import Counter
from typing import Any

import pytest
from shapely.geometry import Point

from lang import *
from lang.core.layout import build_layout
from lang.core.ops import Cut, EdgeOp, Pocket
from lang.core.scope import registry
from lang.emit.plan import Arc, Circle, FaceRef, PocketStep, plan_layout
from helpers import has_material, overlap, part_meshes, ply12, ply15, state

#: What a 3 mm radius leaves in a right-angled corner; the polygons, inscribed
#: in the arcs, leave 0.01 more.
SPANDREL = 9 * (1 - math.pi / 4)


def _pair(a_from: float = 0.0, a_height: float = 150.0, b_at: float = 0.0) -> tuple[Scope, Board, Board]:
    """The corner above; `a_from` moves a's end along x, `a_height` makes a
    lower than b, `b_at` moves b along x."""
    with module("pair", Box.from_size(width=200, depth=200, height=150)) as m:
        a = board("a", ply15).on(m.left).between(Pos("x", a_from), m.back, m.bottom, Pos("z", a_height))
        b = board("b", ply12).on(Pos("x", b_at), toward=m.back).between(a, m.right)
    return m, a, b


def _names(part: Board) -> list[str | None]:
    return [op.op.name if isinstance(op, EdgeOp) else getattr(op, "name", None) for op in part.ops]



def test_a_square_joint():
    m, a, b = _pair()
    with m:
        b.join(a, using=box_joint(5, margin=5, tool=0))
    # a: notches 12 deep (b's thickness) through it, where b's fingers go
    assert has_material(a, (6, 20), (6, 47), (6, 75), (6, 103), (6, 130), (12.01, 47)) == [True, False, True, False, True, True]
    assert a.outline.area == pytest.approx(200 * 150 - 2 * 12 * 28)
    # b: fingers through a's 15, flush with its outer face, and the gaps between
    assert has_material(b, (0.01, 47), (7.5, 103), (7.5, 20), (7.5, 75), (7.5, 2), (-0.01, 47)) == [
        True, True, False, False, False, False]
    assert b.outline.area == pytest.approx(185 * 150 + 2 * 15 * 28)
    assert b.box().lo["y"] == 15                         # the box stays where b was placed
    assert _names(a) == ["notch_b_1", "notch_b_2"] and _names(b) == ["gap_a_1", "gap_a_2", "gap_a_3"]
    # assembled, the two fill the corner without overlapping
    meshes = part_meshes()
    assert overlap(meshes["pair.a"], meshes["pair.b"]) < 1e-6
    assert meshes["pair.a"].volume + meshes["pair.b"].volume == pytest.approx(
        (200 * 150 * 15) + (185 * 150 * 12), rel=1e-9)


def test_clearances_and_the_fillets_the_cutter_keeps():
    m, a, b = _pair()
    with m:
        b.join(a, using=box_joint(5, margin=5, tool=6, clearance=(0.2, 0.5)))
    # the notches are 0.2 wider (0.1 per side) and 0.5 deeper than b is thick
    notch = a.op("notch_b_1").op
    assert isinstance(notch, Cut) and notch.shape.bounds == pytest.approx((-1.0, 32.9, 12.5, 61.1))
    assert notch.shape.area == pytest.approx(13.5 * 28.2 - 2 * SPANDREL, abs=0.05)
    assert has_material(a, (6, 32.89), (6, 32.91), (12.45, 47), (12.55, 47)) == [True, False, False, True]
    # its bottom corners keep the cutter's radius, centred 3 inside them
    assert has_material(a, (12.4, 33.0), (11.0, 34.0), (12.4, 61.0), (11.0, 60.0)) == [True, False, True, False]
    # b's fingers are 0.2 narrower, the gaps' bottoms (b's seats) 0.5 deeper
    # than a is thick, with their own fillets kept
    assert has_material(b, (7.5, 33.05), (7.5, 33.15), (15.45, 75), (15.55, 75)) == [False, True, False, True]
    assert has_material(b, (15.4, 61.0), (14.0, 62.0)) == [True, False]
    # the stock grows from one radius before the first notch wall: the outer
    # gaps carve it back but keep the outer fingers' root fillets whole
    assert has_material(b, (15.4, 33.0), (10, 30.0)) == [True, False]


def test_fingers_are_rounded_over_by_grooves_from_their_tips():
    m, a, b = _pair()
    with m:
        b.join(a, using=box_joint(5, margin=5, tool=6, clearance=(0.2, 0.5)))
    grooves = b.op("finger_a_grooves")
    op = grooves.op
    assert isinstance(op, EdgeOp) and isinstance(op.op, Pocket)
    # from b's end, which faces a (-y), starting at the fingers' tips 15 in
    # front of it, to one radius short of the seats
    assert (op.face, op.offset, op.op.depth) == ("left", 15.0, 12.5)
    assert grooves.extents()["y"] == pytest.approx((0.0, 12.5))
    # a lens at each side of both fingers, at b's inner face (x 12): two
    # quarter arcs meeting 3 below it, in the face's (z, x) frame
    pieces = op.op.shape.polygons()
    assert len(pieces) == 4
    assert sorted(p.bounds for p in pieces)[0] == pytest.approx((30.1, 9.0, 36.1, 12.0))
    assert all(p.area == pytest.approx(2 * SPANDREL, abs=0.05) for p in pieces)


def test_notch_walls_are_grooved_from_the_end():
    m, a, b = _pair()
    with m:
        b.join(a, using=box_joint(5, margin=5, tool=6, clearance=(0.2, 0.5)))
    op = a.op("notch_b_grooves").op
    assert isinstance(op, EdgeOp) and isinstance(op.op, Pocket)
    # from a's end (-x) as deep as the notches
    assert (op.face, op.offset, op.op.depth) == ("front", 0.0, 12.5)
    # at each notch wall, by a's inner face (y 12..15): the finger's side a
    # spandrel, the notch's side opened square to clear its fillet
    pieces = sorted(op.op.shape.polygons(), key=lambda p: p.bounds[0])
    assert [p.bounds for p in pieces] == pytest.approx([
        (29.9, 12.0, 35.9, 15.0), (58.1, 12.0, 64.1, 15.0), (85.9, 12.0, 91.9, 15.0), (114.1, 12.0, 120.1, 15.0)])
    assert all(p.area == pytest.approx(SPANDREL + 9, abs=0.05) for p in pieces)
    assert pieces[0].contains(Point(33.5, 12.5)) and not pieces[0].contains(Point(30.5, 12.5))
    assert pieces[1].contains(Point(58.5, 12.5)) and not pieces[1].contains(Point(61.5, 12.5))


def test_hidden_dog_bones_in_both_inner_faces():
    m, a, b = _pair()
    with m:
        b.join(a, using=box_joint(5, margin=5, tool=6, clearance=(0.2, 0.5)))
    reliefs = a.op("notch_b_reliefs").op
    assert isinstance(reliefs, Pocket) and (reliefs.face, reliefs.depth) == ("right", 3.0)   # a's inner face
    # on the notch walls, touching the notch bottoms (x 12.5)
    centres = sorted((round((p.bounds[0] + p.bounds[2]) / 2, 6), round((p.bounds[1] + p.bounds[3]) / 2, 6))
                     for p in reliefs.shape.polygons())
    assert centres == [(9.5, 32.9), (9.5, 61.1), (9.5, 88.9), (9.5, 117.1)]
    reliefs = b.op("finger_a_reliefs").op
    assert isinstance(reliefs, Pocket) and (reliefs.face, reliefs.depth) == ("back", 3.0)    # b's inner face
    # on the fingers' sides, touching the seats (y 15.5)
    centres = sorted((round((p.bounds[0] + p.bounds[2]) / 2, 6), round((p.bounds[1] + p.bounds[3]) / 2, 6))
                     for p in reliefs.shape.polygons())
    assert centres == [(12.5, 33.1), (12.5, 60.9), (12.5, 89.1), (12.5, 116.9)]
    assert all(p.bounds[2] - p.bounds[0] == pytest.approx(6.0) for p in reliefs.shape.polygons())


@pytest.mark.parametrize("joint", [
    box_joint(),
    box_joint(5, margin=5, tool=6),
    box_joint(7, margin=2, tool=6, clearance=(0.1, 0.1)),
    box_joint(3, margin=5, tool=6, clearance=(0.2, 0.5)),
    box_joint(9, margin=0, tool=6, clearance=(0.3, 0.0)),
])
def test_the_assembled_joint_does_notoverlap(joint: Any):
    m, a, b = _pair()
    with m:
        b.join(a, using=joint)
    meshes = part_meshes()
    assert overlap(meshes["pair.a"], meshes["pair.b"]) < 1e-3
    assert all(mesh.is_volume for mesh in meshes.values())


@pytest.mark.parametrize("tool", [0.0, 6.0])
def test_all_four_corners_of_a_drawer_box(tool: float):
    """Each corner faces another way; all come out alike and fit."""
    with module("box", Box.from_size(width=400, depth=300, height=150)) as m:
        l = board("left", ply12).on(m.left)
        r = board("right", ply12).on(m.right)
        f = board("front", ply12).on(m.front).between(l, r)
        k = board("back", ply12).on(m.back).between(l, r)
        f.join(l, r, using=box_joint(5, tool=tool))
        l.join(k, using=box_joint(5, tool=tool))
        k.join(r, using=box_joint(5, tool=tool))
    meshes = part_meshes()
    sides, ends = [meshes["box.left"], meshes["box.right"]], [meshes["box.front"], meshes["box.back"]]
    assert sides[0].volume == pytest.approx(sides[1].volume) and ends[0].volume == pytest.approx(ends[1].volume)
    if tool == 0:
        # two 12 x 30 x 12 notches per corner in the sides, as many fingers on the ends
        assert sides[0].volume == pytest.approx(300 * 150 * 12 - 4 * 12 * 30 * 12)
        assert ends[0].volume == pytest.approx(376 * 150 * 12 + 4 * 12 * 30 * 12)
    assert all(overlap(s, e) < 1e-3 for s in sides for e in ends)


def test_three_fingers_make_one_notch():
    m, a, b = _pair()
    with m:
        b.join(a, using=box_joint(3, tool=0))
    # 150 / 3 = 50: a's fingers at 0..50 and 100..150, b's between
    assert _names(a) == ["notch_b_1"] and _names(b) == ["gap_a_1", "gap_a_2"]
    assert has_material(b, (7.5, 75), (7.5, 49), (7.5, 101)) == [True, False, False]


def test_with_no_margin_the_end_gaps_reach_past_the_ends():
    """The add-in fails here: its end gaps, widened by half the clearance,
    would start outside the board. Here they are cut past its ends."""
    m, a, b = _pair()
    with m:
        b.join(a, using=box_joint(5, tool=6, clearance=(0.2, 0.5)))
    gap = b.op("gap_a_1").op
    assert isinstance(gap, Cut) and gap.shape.bounds[1] == pytest.approx(-0.1)
    assert len(b.outline.polygons()) == 1 and has_material(b, (7.5, 0.5), (15.6, 0.5)) == [False, True]
    meshes = part_meshes()
    assert overlap(meshes["pair.a"], meshes["pair.b"]) < 1e-3


def test_either_board_can_make_the_call():
    m, a, b = _pair()
    with m:
        a.join(b, using=box_joint(5, margin=5))
    assert _names(a) == ["notch_b_1", "notch_b_2", "notch_b_grooves", "notch_b_reliefs"]
    assert _names(b) == ["gap_a_1", "gap_a_2", "gap_a_3", "finger_a_grooves", "finger_a_reliefs"]


def test_the_emitter_cuts_the_grooves_from_where_they_start():
    m, a, b = _pair()
    with m:
        b.join(a, using=box_joint(5, margin=5, tool=6, clearance=(0.2, 0.5)))
    plan = {p.path: p for p in plan_layout(build_layout()).parts}

    def kinds(loops: Any) -> Counter[str]:
        return Counter(type(c).__name__ for loop in loops for c in loop)

    grooves, reliefs = plan["pair.b"].steps
    assert isinstance(grooves, PocketStep) and isinstance(reliefs, PocketStep)
    assert grooves.face == FaceRef("y", -1, 0.0) and grooves.depth == 12.5     # at the fingers' tips
    assert [kinds(s) for s in grooves.shapes] == [Counter(Line=1, Arc=2)] * 4
    assert reliefs.face == FaceRef("x", 1, 12.0) and reliefs.depth == 3.0
    assert all(isinstance(s[0][0], Circle) and s[0][0].radius == pytest.approx(3) for s in reliefs.shapes)
    # every fillet in b's outline is an arc, the pieces the board's end
    # leaves of the outer gaps' outer ones too
    assert kinds(plan["pair.b"].body.loops) == Counter(Line=14, Arc=6)
    arcs = [c for c in plan["pair.b"].body.loops[0] if isinstance(c, Arc)]
    assert all(c.radius == pytest.approx(3) for c in arcs)
    grooves, reliefs = plan["pair.a"].steps
    assert isinstance(grooves, PocketStep) and isinstance(reliefs, PocketStep)
    assert grooves.face == FaceRef("x", -1, 0.0) and grooves.depth == 12.5
    assert [kinds(s) for s in grooves.shapes] == [Counter(Line=3, Arc=1)] * 4
    assert kinds(plan["pair.a"].body.loops) == Counter(Line=12, Arc=4)


def test_the_preview_meshes_pockets_in_narrow_faces():
    with module("m", Box.from_size(width=200, depth=200, height=150)) as m:
        p = board("p", ply15).on(m.bottom)
        p.pocket(rect(depth=40, height=6), at=p.right.center, depth=10)
        p.hole(d=8, depth=30, at=p.front.right(50))
        # 5 in front of the left face (y 0), 15 deep: 10 of it in the board
        p.add_edge_pocket(p.left, Shape(Point(100, 7.5).buffer(3, quad_segs=16)), 15, offset=5)
    mesh = part_meshes()["m.p"]
    removed = 200 * 200 * 15 - mesh.volume
    hole = 24 / 2 * 4 ** 2 * math.sin(2 * math.pi / 24)                   # the mesher's 24-sided cylinder
    disc = Point(0, 0).buffer(3, quad_segs=16).area
    # each tool reaches 0.005 past its depth
    assert removed == pytest.approx(40 * 6 * 10.005 + 30.005 * hole + 10.005 * disc, rel=1e-6)


def test_box_joint_errors():
    for message, make in (("must be odd", lambda: box_joint(4)),
                          ("at least 3 fingers", lambda: box_joint(1)),
                          ("must not be negative", lambda: box_joint(margin=-1)),
                          ("must not be negative", lambda: box_joint(clearance=(0, -0.1)))):
        with pytest.raises(LangError, match=message):
            make()
    m, a, b = _pair()
    before = state(a, b)
    with m:
        with pytest.raises(LangError, match="too narrow for the corner reliefs"):
            b.join(a, using=box_joint(25))                          # 6 wide: not wider than the tool
        with pytest.raises(LangError, match="leaves no room"):
            b.join(a, using=box_joint(margin=75))
        with pytest.raises(LangError, match="leaves nothing of the 6 mm fingers"):
            b.join(a, using=box_joint(25, tool=0, clearance=(6, 0)))
        with pytest.raises(LangError, match=r"^pair\.b: box_joint with pair\.c: the two do not touch"):
            b.join(board("c", ply15).on(Pos("x", 100), toward=m.back), using=box_joint())
    assert state(a, b) == before
    with pytest.raises(LangError, match="pair.a is 2.5 thick, not thicker than the tool's radius"):
        registry.reset()
        with module("pair", Box.from_size(width=200, depth=200, height=150)) as m:
            a = board("a", material("veneer", t=2.5)).on(m.left)
            b = board("b", ply12).on(m.front).between(a, m.right)
            b.join(a, using=box_joint())


@pytest.mark.parametrize("make, message", [
    (lambda: _pair(a_from=-20), "not flush: the end of pair.a must lie in the plane"),     # a reaches past b
    (lambda: _pair(a_from=-20, b_at=50), "not reach past both"),                           # a T, not a corner
    (lambda: _pair(a_from=5), "pair.a does not cover the end of pair.b"),                  # a ends inside b
    (lambda: _pair(a_height=100), "not across its whole width"),                           # b is wider than a
])
def test_the_corner_must_be_a_flush_corner(make: Any, message: str):
    m, a, b = make()
    before = state(a, b)
    with m:
        with pytest.raises(LangError, match=message):
            b.join(a, using=box_joint())
    assert state(a, b) == before


def test_a_joint_that_fails_on_the_notched_board_changes_neither():
    """A slot in a just past the notches' bottoms (x 12.2 to 20): the
    second notch cuts a's finger between the two loose. b has grown its
    fingers and lost its gaps by then; both are restored."""
    m, a, b = _pair()
    with m:
        a.cut(rect(depth=7.8, height=140), at=a.right.front(12.2), name="slot")
        before = state(a, b)
        with pytest.raises(LangError, match=r"^pair\.b: box_joint with pair\.a: pair\.a: the cut notch_b_2 splits the "
                                            r"board in pieces"):
            b.join(a, using=box_joint(5, margin=5, tool=0, clearance=(0, 0.5)))
    assert state(a, b) == before


def test_errors_are_reported_on_the_board_whose_join_was_called():
    m, a, b = _pair(a_from=5)
    with m:
        with pytest.raises(LangError, match=r"^pair\.a: box_joint with pair\.b: pair\.a does not cover the end of "
                                            r"pair\.b"):
            a.join(b, using=box_joint())


def test_cut_outs_at_the_joint_go_after_it():
    m, a, b = _pair()
    with m:
        b.cut(rect(width=40, height=10), at=b.back.left.bottom)          # at b's end, as a slide's coupling
        with pytest.raises(LangError, match="Cut-outs at the joint go after the join"):
            b.join(a, using=box_joint())
