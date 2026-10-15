import math
import re
from pathlib import Path
from typing import Any

import pytest
from shapely.geometry import Point
from shapely.geometry import box as shapely_box

from lang import *
from lang.core.cutouts import circle_geometry
from lang.core.directions import Axis, InnerOuter
from lang.core.faces import Face
from lang.core.layout import build_layout
from lang.core.ops import Chamfer, Cut, EdgeOp, Hole, Pocket
from lang.core.refs import Affine, as_pos
from lang.core.scope import registry
from lang.emit.plan import plan_layout
from lang.master import Plane
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


def test_a_sum_of_positions_less_a_position_is_a_position():
    """Decided by Florian, 2026-10-14: `a + b - c` of positions is a
    position where the weights add up to one (it was a TypeError), also
    as `a - (b + c) / 2 + ...` sums; a length taken from a sum of positions
    is an error saying so."""
    cab = carcass()
    bottom = cab["bottom"]
    # the box's top moved up by the bottom's thickness: 720 + 15 - 0
    assert cab.top + bottom.top - bottom.bottom == Pos("z", 735)
    assert cab.top + cab.bottom - cab.bottom == Pos("z", 720)
    assert as_pos(bottom.top - (cab.top + cab.bottom) + cab.top + cab.bottom) == Pos("z", 15)
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        shelf = board("shelf", ply15).on(m.bottom + m.top - m.top, toward=m.top)
    assert shelf.box().lo["z"] == 0
    with pytest.raises(LangError, match="weights of a sum of positions must add up to 1"):
        as_pos(Pos("z", 1) + Pos("z", 2) + Pos("z", 3) - Pos("z", 4))         # weights 2
    with pytest.raises(LangError, match="a length goes with one position"):
        _ = Pos("z", 1) + Pos("z", 2) - 20


def test_box_sides_mix_like_other_positions():
    """Found by fuzzing the placement: `0.5 * m.bottom + 0.5 * m.top` was a
    TypeError where the same mix of faces or positions is a position: a box
    side had no scaling (`*`, `/`). A number added from the left is refused
    as one added from the right is (syntax.md item 1)."""
    with module("m", Box.from_size(width=600, depth=400, height=700, origin=(0, 0, 100))) as m:
        assert 0.5 * m.bottom + 0.5 * m.top == Pos("z", 450)
        assert (m.bottom * 3 + m.top) / 4 == Pos("z", 275)
        assert m.bottom / 2 + m.top / 2 == Pos("z", 450)
        with pytest.raises(LangError, match=r"^60 \+ m.bottom: a side has a direction; write m.bottom.into\(60\) "):
            _ = 60 + m.bottom  # type: ignore[operator]
        shelf = board("shelf", ply15).center(0.25 * m.bottom + 0.75 * m.top)
    assert shelf.box().lo["z"] == 625 - 7.5


def test_a_side_or_a_face_plus_a_length_is_refused():
    """Decided by Florian, 2026-10-15 (syntax.md item 1): a side or a face
    plus or minus a number moved along the world axis, so in a cabinet it
    moved inward or outward depending on `front=`. It is an error naming
    the receiver and the fix, `into()` or `gap()`: for a box side, a side
    moved by `into()` or `gap()`, a face and a face moved by `gap()` or
    `into()`, the number on either side of the operator, in cabinets facing
    two ways."""
    van = Box.from_size(width=600, depth=500, height=700)
    for facing in ("front", "right"):
        with cabinet(f"cab_{facing}", van, front=van.side(facing)) as cab:
            left = board("left", ply15).on(cab.left)
            refused: dict[str, Any] = {
                f"cab_{facing}.front": cab.front,
                f"cab_{facing}.bottom.into(60)": cab.bottom.into(60),
                f"cab_{facing}.top.gap(5)": cab.top.gap(5),
                "left.right": left.inner,
                "left.right.gap(15)": left.inner.gap(15),
                "left.front.into(3)": left.front.into(3),
            }
        for label, ref in refused.items():
            noun = "a face" if isinstance(ref, Face) else "a side"
            for written, move in ((f"{label} + 40", lambda: ref + 40), (f"{label} - 40", lambda: ref - 40),
                                  (f"40 + {label}", lambda: 40 + ref)):
                fix = f"{written}: {noun} has a direction; write {label}.into(40) or {label}.gap(40)."
                with pytest.raises(LangError, match=re.escape(fix)):
                    move()
        with pytest.raises(LangError, match=re.escape(f"cab_{facing}.front - -2.5: a side has a direction; write "
                                                      f"cab_{facing}.front.into(2.5) or cab_{facing}.front.gap(2.5).")):
            _ = cab.front - -2.5  # type: ignore[operator]
    with pytest.raises(LangError, match=re.escape("box.top + 1: a side has a direction; write box.top.into(1)")):
        _ = van.top + 1  # type: ignore[operator]


def test_positions_keep_their_arithmetic_and_sides_and_faces_mix():
    """What stays (syntax.md item 1): a bare position takes a length (a
    `Pos`, a master's plane, an operation's side, `spread()`'s positions,
    `box.center()`, a side's or a face's `.position`); a side or a face
    plus a position is the weighted mix, minus one a length, and `*` and
    `/` scale it."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        left.cut(rect(depth=60, height=100), at=left.outer.bottom.front, name="toekick")
        bottom = board("bottom", ply15).on(left.toekick.top + 5, toward=m.top).between(left, m.right)
        top = board("top", ply15).on(m.top).between(left, m.right)
        rows = spread(bottom.top, top.bottom, count=3)
    assert left.toekick.top + 5 == Pos("z", 105) and bottom.bottom.value == 105
    assert Pos("z", 10) + 5 == Pos("z", 15) and 5 + Pos("z", 10) == Pos("z", 15) and Pos("z", 10) - 5 == Pos("z", 5)
    floor = Plane("floor", [0, 0, 100], [0, 0, 1])
    assert floor + 5 == Pos("z", 105) and floor - 5 == Pos("z", 95) and 5 + floor == Pos("z", 105)
    assert rows[1] + 10 == Pos("z", (120 + 685) / 2 + 10)
    assert m.center("height") - 50 == Pos("z", 300)
    assert m.bottom.position + 60 == Pos("z", 60) and bottom.top.position - 5 == Pos("z", 115)
    # sides and faces with positions
    assert (bottom.top + top.bottom) / 2 == Pos("z", 402.5) and top.bottom - bottom.top == 565
    assert m.top - m.bottom == 700 and m.top - floor == 600 and floor - m.bottom == 100
    assert 0.5 * m.bottom + 0.5 * top.bottom == Pos("z", 342.5) and m.top / 2 + bottom.top / 2 == Pos("z", 410)
    assert bottom.top + top.bottom - m.top == Pos("z", 120 + 685 - 700)
    assert as_pos(m.bottom.into(60) + m.top.gap(40) - left.toekick.top) == Pos("z", 700)


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
    moved = b.with_sides(front=Pos("x", 100), top=b.bottom.into(50))
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


def test_a_side_moved_into_or_out_of_its_box_is_a_side():
    """Decided by Florian, 2026-10-14: `side.into(n)` and `side.gap(n)` are
    the side moved, its inward direction kept, so a board lies on them with
    its thickness inward without toward= (`on(cab.bottom.into(60))`); they
    were bare positions."""
    van = Box.from_size(width=600, depth=500, height=700)
    with cabinet("cab", van, front=van.right) as cab:
        raised = board("raised", ply15).on(cab.bottom.into(60))
        partition = board("partition", ply15).on(cab.left.into(100))
        lid = board("lid", ply15).on(cab.top.gap(5))
    assert isinstance(cab.left.into(100), Side) and isinstance(cab.top.gap(5), Side)
    assert (raised.box().lo["z"], raised.box().hi["z"]) == (60, 75)
    assert cab.left.axis == "x" and cab.left.value == 500                       # the cabinet's left is +x
    assert (partition.box().lo["x"], partition.box().hi["x"]) == (385, 400)    # 100 in, thickness inward
    assert (lid.box().lo["z"], lid.box().hi["z"]) == (690, 705)                # 5 above, thickness down
    assert cab.left.into(100).position == Pos("x", 400) and cab.left.gap(5) - cab.left == 5


def _extents(part: Board) -> tuple[dict[Axis, float], dict[Axis, float]]:
    b = part.box()
    return dict(b.lo), dict(b.hi)


def test_a_face_moved_by_gap_or_into_keeps_its_side():
    """Decided by Florian, 2026-10-15: `face.gap(n)` and `face.into(n)` are
    the face's plane moved, keeping the face's side, so a board lies on them
    away from the face's part without toward= (`on(back.inner.gap(15))`),
    as on the face itself; they were bare positions, which needed toward=.
    The same from big and narrow faces, in a module and in cabinets facing
    each side of the van, measured in the scope's own terms."""
    van = Box.from_size(width=600, depth=500, height=700)
    for facing in (None, "front", "right", "back", "left"):
        name = f"cab_{facing}"
        with (module(name, van) if facing is None else cabinet(name, van, front=van.side(facing))) as cab:
            left = board("left", ply15).on(cab.left)
            bottom = board("bottom", ply15).on(cab.bottom).between(left, cab.right)
            back = board("back", ply9).on(cab.back).between(left, cab.right, bottom, cab.top)
            moved = {
                "panel": (back.inner.gap(15), cab.front),     # a big face, out of its part
                "inset": (back.inner.into(3), cab.front),     # a big face, into its part
                "apron": (bottom.front.gap(10), cab.front),   # a narrow face, out of its part
                "rail": (left.top.into(20), cab.top),         # a narrow face, into its part
            }
            placed = {k: board(k, ply15).on(ref) for k, (ref, _) in moved.items()}
            spelled = {k: board(f"{k}_toward", ply15).on(ref.position, toward=toward)
                       for k, (ref, toward) in moved.items()}
            # toward= still decides where it is given
            behind = board("behind", ply15).on(back.inner.gap(15), toward=cab.back)
        front = cab.frame.direction("front")
        f = front.sign
        assert back.inner.name == "front" and left.top.name == "top"
        assert all(isinstance(ref, Side) for ref, _ in moved.values())
        assert moved["panel"][0].inward == front and moved["rail"][0].inward == cab.frame.direction("top")
        for k in moved:
            assert _extents(placed[k]) == _extents(spelled[k]), (facing, k)
        panel, inset, apron, rail = (placed[k] for k in ("panel", "inset", "apron", "rail"))
        assert panel.t_axis == back.t_axis and apron.t_axis == front.axis and rail.t_axis == "z"
        # 15 in front of the back, its thickness on to the front
        assert (panel.back.value, panel.front.value) == (back.front.value + 15 * f, back.front.value + 30 * f)
        assert behind.front.value == back.front.value + 15 * f and behind.back.value == back.front.value
        # 3 into the back, its thickness to the front
        assert (inset.back.value, inset.front.value) == (back.front.value - 3 * f, back.front.value + 12 * f)
        # 10 in front of the bottom's front edge
        assert (apron.back.value, apron.front.value) == (bottom.front.value + 10 * f, bottom.front.value + 25 * f)
        # 20 below the side's top edge, its thickness up
        assert (rail.bottom.value, rail.top.value) == (680, 695)


def test_a_face_moved_again_keeps_the_face_s_in_and_out():
    """Decided by Florian, 2026-10-15: a side made from a face keeps the
    face's in and out when it is moved again, so `back.inner.gap(15).gap(5)`
    is 20 in front of the back and `back.inner.gap(15).into(5)` 10 (moved
    as a box side, they went the other way: `into()` away from the part).
    Its inward direction, which `on()` and the direction arguments read,
    stays the face's. From big and narrow faces, in a module and in
    cabinets facing each side of the van, measured in the scope's own
    terms."""
    van = Box.from_size(width=600, depth=500, height=700)
    for facing in (None, "front", "right", "back", "left"):
        name = f"cab_{facing}"
        with (module(name, van) if facing is None else cabinet(name, van, front=van.side(facing))) as cab:
            left = board("left", ply15).on(cab.left)
            bottom = board("bottom", ply15).on(cab.bottom).between(left, cab.right)
            back = board("back", ply9).on(cab.back).between(left, cab.right, bottom, cab.top)
            panel = board("panel", ply15).on(back.inner.gap(15).gap(5))
            inset = board("inset", ply15).on(back.inner.gap(15).into(18))
        front, right = cab.frame.direction("front"), cab.frame.direction("right")
        f, r = front.sign, right.sign
        inner = back.front.value
        # a big face: out and out again, out and back, in and in again, in and out
        assert back.inner.gap(15).gap(5).value == inner + 20 * f
        assert back.inner.gap(15).into(5).value == inner + 10 * f
        assert back.inner.into(3).into(2).value == inner - 5 * f
        assert back.inner.into(3).gap(5).value == inner + 2 * f
        assert left.inner.gap(100).into(30).value == left.right.value + 70 * r
        # narrow faces
        assert bottom.front.gap(10).gap(5).value == bottom.front.value + 15 * f
        assert bottom.front.gap(10).into(4).value == bottom.front.value + 6 * f
        assert left.front.into(30).into(10).value == left.front.value - 40 * f
        assert left.top.into(20).into(5).value == 675 and left.top.into(20).gap(25).value == 705
        # its direction stays the face's, away from the part
        moved = back.inner.gap(15).gap(5).into(1)
        assert moved.from_face and moved.inward == front and moved.outward == -front
        assert (panel.back.value, panel.front.value) == (inner + 20 * f, inner + 35 * f)
        assert (inset.back.value, inset.front.value) == (inner - 3 * f, inner + 12 * f)


def test_box_sides_moved_again_move_as_before():
    """A box side moved again moves into and out of its box as it did
    before sides made from faces kept the face's in and out [Florian,
    2026-10-15]: `cab.bottom.into(60).into(10)` is 70 inside."""
    van = Box.from_size(width=600, depth=500, height=700)
    for facing in (None, "right"):
        name = f"cab_{facing}"
        with (module(name, van) if facing is None else cabinet(name, van, front=van.side(facing))) as cab:
            raised = board("raised", ply15).on(cab.bottom.into(60).into(10))
            lid = board("lid", ply15).on(cab.top.gap(5).gap(5))
        r = cab.frame.direction("right").sign
        assert not cab.bottom.into(60).from_face
        assert cab.bottom.into(60).into(10) == cab.bottom.into(70) == Side("z", 70, cab.bottom.inward)
        assert cab.bottom.into(60).gap(10) == cab.bottom.into(50)
        assert cab.top.gap(5).gap(5).value == 710 and cab.top.gap(5).into(15).value == 690
        assert cab.left.into(100).into(20).value == cab.left.value + 120 * r
        assert (raised.box().lo["z"], raised.box().hi["z"]) == (70, 85)
        assert (lid.box().lo["z"], lid.box().hi["z"]) == (695, 710)


def test_a_slat_lies_on_and_edge_on_moved_faces_away_from_their_parts():
    """Decided by Florian, 2026-10-15 (`Face.gap()`, `Face.into()` keep the
    face's side): `edge_on()` takes a moved face as `on()` does."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        shelf = board("shelf", ply15).on(Pos("z", 300), toward=m.top).between(left, m.right)
        oak = slat_material("oak")
        cleat = slat("cleat", oak, section=(20, 40)).on(left.inner.gap(2)).edge_on(shelf.bottom.into(5))
        twin = (slat("twin", oak, section=(20, 40)).on(Pos("y", 17), toward=m.right)
                .edge_on(Pos("z", 305), toward=m.bottom))
    assert _extents(cleat) == _extents(twin)
    assert (cleat.box().lo["y"], cleat.box().hi["y"], cleat.box().lo["z"], cleat.box().hi["z"]) == (17, 37, 265, 305)


def test_a_moved_face_is_a_position_as_before_everywhere_else():
    """`face.gap(n)` and `face.into(n)` keep the face's side since
    2026-10-15 [Florian]; as limits, in `center()`, `spread()`, anchors,
    `with_sides()` and the position algebra they give what the bare
    positions they were gave."""
    box = Box.from_size(width=600, depth=500, height=700)
    with module("m", box) as m:
        left = board("left", ply15).on(m.left)
        right = board("right", ply15).on(m.right)
        bottom = board("bottom", ply15).on(m.bottom).between(left, right)
        back = board("back", ply9).on(m.back).between(left, right, bottom, m.top)
        a, b, c = left.inner.gap(2), right.inner.into(5), back.inner.gap(4)
        pa, pb, pc = a.position, b.position, c.position
        shelf = board("shelf", ply15).on(m.bottom.into(300), toward=m.top).between(a, b, c)
        shelf_p = board("shelf_p", ply15).on(m.bottom.into(300), toward=m.top).between(pa, pb, pc)
        lone = board("lone", ply15).on(m.bottom.into(400), toward=m.top).between(c)
        lone_p = board("lone_p", ply15).on(m.bottom.into(400), toward=m.top).between(pc)
        divider = board("divider", ply15).center(left.inner.gap(100)).between(bottom, m.top)
        divider_p = board("divider_p", ply15).center(left.inner.gap(100).position).between(bottom, m.top)
        at = back.inner.left(left.inner.gap(30)).bottom(bottom.top.gap(40))
        at_p = back.inner.left(left.inner.gap(30).position).bottom(bottom.top.gap(40).position)
        back.hole(d=8, at=at, depth=5)
    assert isinstance(a, Side) and isinstance(b, Side) and isinstance(c, Side)
    assert (pa, pb, pc) == (Pos("y", 17), Pos("y", 590), Pos("x", 487))
    assert _extents(shelf) == _extents(shelf_p) == ({"x": 0, "y": 17, "z": 300}, {"x": 487, "y": 590, "z": 315})
    assert _extents(lone) == _extents(lone_p)
    assert _extents(divider) == _extents(divider_p) and divider.box().lo["y"] == 107.5
    assert at.resolve() == at_p.resolve() and at.resolve()[0] == (45, 55)
    hole = back.ops[-1]
    assert isinstance(hole, Hole) and (hole.u, hole.v) == (45, 55)
    assert spread(a, b, count=3) == spread(pa, pb, count=3) == [Pos("y", 17), Pos("y", 303.5), Pos("y", 590)]
    assert spread(b, a, pitch=100) == spread(pb, pa, pitch=100)
    narrowed, narrowed_p = box.with_sides(left=a, back=c), box.with_sides(left=pa, back=pc)
    assert (narrowed.lo, narrowed.hi) == (narrowed_p.lo, narrowed_p.hi) == ({"x": 0, "y": 17, "z": 0},
                                                                            {"x": 487, "y": 600, "z": 700})
    # the algebra: lengths and mixes come out as they did; a length added is refused (syntax.md item 1)
    assert a - left.inner == 2 and b - a == pb - pa == 573 and a - pa == 0
    assert (a + b) / 2 == (pa + pb) / 2 == Pos("y", 303.5)
    assert 0.5 * a + 0.5 * b == Pos("y", 303.5) and a + b - a == pb
    assert a.position + 5 == pa + 5
    with pytest.raises(LangError, match=r"left.right.gap\(2\) \+ 5: a side has a direction"):
        _ = a + 5  # type: ignore[operator]


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


def test_a_board_across_its_scope_s_middle_shows_its_top_back_or_right_face():
    """Decided by Florian, 2026-10-14: a board across its scope's middle
    without show(), which has no outer face, shows the face toward the
    scope's top, else its back, else its right, named in the scope's own
    terms. (It showed the face toward the world axis' positive end, so a
    divider showed its left in a cabinet facing the van's right and its
    right in one facing its front.)"""
    van = Box.from_size(width=600, depth=600, height=700)
    for front in ("front", "right", "back", "left"):
        with cabinet(f"cab_{front}", van, front=van.side(front)) as cab:
            shelf = board("shelf", ply15).center(cab.center("height"))
            divider = board("divider", ply15).center(cab.center("width"))
            panel = board("panel", ply15).center(cab.center("depth"))
            side = board("side", ply15).on(cab.left)
        assert (shelf.show_face.name, divider.show_face.name, panel.show_face.name) == ("top", "right", "back")
        assert side.show_face.name == "left"                           # its outer face, as before
        assert divider.to_layout()["show"] == world_frame().name_of(cab.frame.direction("right"))


def test_the_inner_face_of_a_board_with_a_face_on_the_middle_faces_the_middle():
    """Found by fuzzing the placement: a board whose top face lay on its
    module's middle had its bottom face for its inner one (the one toward
    the middle), and one whose bottom face lay there its bottom face too,
    so a frame binding the axis the other way swapped them; at some places
    rounding put the face a hair across the middle, and both faces were
    refused as ambiguous."""
    for name, origin in (("at0", 0.0), ("far", 1234.1)):
        with module(name, Box.from_size(width=600, depth=400, height=30, origin=(0, 0, origin))) as m:
            low = board("low", ply15).on(m.bottom)
            high = board("high", ply15).on(m.top)
            mid = board("mid", ply15).on(m.bottom.into(7.5))             # 7.5 to 22.5, across the middle at 15
        assert low.inner.name == "top" and low.outer.name == "bottom"
        assert high.inner.name == "bottom" and high.outer.name == "top"
        with pytest.raises(LangError, match="ambiguous"):
            mid.inner
    with module("hair", Box.from_size(width=600, depth=400, height=30, origin=(0, 0, 12.3))) as m:
        low = board("low", ply15).on(m.bottom)            # its top at 27.3, the middle at 27.299999999999997
    assert low.inner.name == "top"


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


def test_an_anchor_centres_a_shape_on_a_position():
    """Decided by Florian, 2026-10-15 (syntax.md item 6): `anchor.center(pos)`
    puts a shape's middle on `pos` along the axis the anchor has not named:
    `b.outer.top.center(line)` puts a notch's top on the top edge and its
    middle on `line`, where `left(line - 7)` was written for a notch 14
    wide. It works wherever a shape is placed by at= (a cut, a pocket on a
    big face and on a narrow one; a cutout's region in test_cutouts) and
    gives a hole's and a slot's centre. The position may be a `Pos`, a box
    side, a part's face, a master's plane or an operation's edge."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)               # x 0..400, y 0..15, z 0..700
        shelf = board("shelf", ply15).on(Pos("z", 300), toward=m.top).between(left, m.right)
        line, cable = Pos("x", 120), Plane("cable", [250, 0, 0], [1, 0, 0])
        left.cut(rect(depth=14, height=12), at=left.outer.top.center(line), name="notch")
        left.pocket(rect(depth=30, height=10), at=left.inner.front(50).center(shelf.bottom), depth=5, name="dado")
        left.pocket(rect(width=6, height=20), at=left.front.inner(3).center(m.bottom.into(400)), depth=10,
                    name="edge")
        left.hole(d=8, at=left.inner.bottom(100).center(cable), depth=5, name="cable")
        left.hole(d=8, at=left.inner.bottom(140).center(left.notch.front), depth=5, name="under_notch")
        start, end = left.inner.top(50).center(m.front.into(150)), left.inner.top(50).center(Pos("x", 250))
        left.slot(6, start, end, depth=5, name="mount")
    def edges(name: str) -> tuple[float, ...]:
        return tuple(left.op(name).side(d).value for d in ("front", "back", "bottom", "top"))

    assert edges("notch") == (113, 127, 688, 700)
    assert edges("dado") == (50, 80, 295, 305)
    assert edges("edge") == (0, 10, 390, 410) and (left.edge.left.value, left.edge.right.value) == (6, 12)
    assert edges("cable") == (246, 254, 96, 104) and edges("under_notch") == (109, 117, 136, 144)
    assert edges("mount") == (147, 253, 647, 653)
    assert left.outer.top.center(line).resolve()[0] == (120, 700)
    assert left.inner.center.center(line).resolve()[0] == (120, 350)    # the other axis centred on the face


def test_anchor_center_takes_a_position_on_the_axis_left_unnamed():
    """syntax.md item 6: `center()` takes a position, never a number (that
    measures from an edge); its axis lies in the face's plane and is the
    one the anchor has not named; once it is given, that axis is no edge
    to name."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
    anchor = left.inner.top
    refused = [
        (lambda: anchor.center(5), re.escape("center() takes a position; a number measures from an edge, "  # type: ignore[arg-type]
                                             "name one: face.front(37).")),
        (lambda: anchor.center(m.right), r"center\(y=600\) is not in the plane of the right face"),
        (lambda: anchor.center(m.top), r"center\(z=700\) lies on the axis of top, which the anchor names"),
        (lambda: anchor.front.center(Pos("x", 5)), "both axes of the face are given already"),
        (lambda: anchor(30).back(20).center(Pos("x", 5)), "both axes of the face are given already"),
        (lambda: anchor.center(Pos("x", 5)).center(Pos("x", 6)), "both axes of the face are given already"),
        (lambda: left.inner.center.center(Pos("x", 5)).center(Pos("x", 6)), r"center\(x=6\) is given on x already"),
        (lambda: anchor.center(Pos("x", 5)).front, "front lies on the axis it is centred on"),
        (lambda: left.inner.center.center(Pos("z", 5)).top, "top lies on the axis it is centred on"),
    ]
    for make, message in refused:
        with pytest.raises(LangError, match=message):
            make()
    assert repr(anchor.center(Pos("x", 5))) == "Anchor(m.left.right.top.center(x=5))"


def test_pocket_depth_to_face():
    cab = carcass()
    left = cab["left"]
    left.pocket(rect(depth=200, height=12), at=left.inner.center, depth=to(left.outer, leave=3))
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
    ply20 = sheet_material("birch", t=20)
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


def test_a_hole_into_a_narrow_face_stays_there_when_a_cut_leaves_the_face_a_hair_askew():
    """Found by fuzzing the placement: a notch at a board's back right
    corner, placed by that corner, came 6e-14 mm short of the back face,
    so the cut left the back face's edge 6e-14 askew, and a hole made
    before into the back face's other end was then taken to be off the
    board ("its outline does not reach the back side there"); in another
    frame the same notch was made. The outline must run along the face
    within a micrometre. A notch that takes the face from under the hole is
    still refused."""
    with module("m", Box.from_size(width=600, depth=426.71380074360144, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom)
        panel.hole(d=8, at=panel.back.left(50), depth=20)
        panel.cut(rect(depth=77.69648890942747, width=100), at=panel.top.back.right, name="notch")
        other = board("other", ply15).on(m.bottom.into(20))
        other.hole(d=8, at=other.back.right(30), depth=20)
        with pytest.raises(LangError, match="does not reach the back side there"):
            other.cut(rect(depth=77.69648890942747, width=100), at=other.top.back.right, name="notch")
    assert panel.has_operation("notch") and not other.has_operation("notch")


def test_a_shaped_board_s_box_lies_where_its_shape_s_edges_do():
    """Found by fuzzing the placement: a board made of a rect between
    limits as far apart as the rect is wide had its far edge at 110.2
    where its box's side was at 110.19999999999999 (its low corner plus the
    width, against the limit as written), so at that place a hole into
    that narrow face was refused: the outline did not reach the face. Its
    box takes the outline's edges where they differ by rounding only."""
    for k, y in enumerate((0.0, 0.1)):
        with module(f"m{k}", Box.from_size(width=600, depth=400, height=100, origin=(0, y, 0))) as m:
            panel = board("panel", ply15, rect(width=100, depth=50)).on(m.bottom).between(
                m.left.into(10.1), m.left.into(110.1), m.front, m.front.into(50))
            panel.hole(d=8, at=panel.right.front(25), depth=20)
        assert panel.box().hi["y"] == panel.outline.bounds[3]
        assert panel.box().hi["y"] == pytest.approx(y + 110.1)


def _measured(cab: Scope, b: Board) -> list[tuple[float, float]]:
    """A board's box measured inward from its scope's front, left and
    bottom sides."""
    out: list[tuple[float, float]] = []
    for name in ("front", "left", "bottom"):
        s = cab.side(name)
        p, q = (s.inward.sign * (b.box().lo[s.axis] - s.value), s.inward.sign * (b.box().hi[s.axis] - s.value))
        out.append((min(p, q), max(p, q)))
    return out


@pytest.mark.parametrize("facing", ["front", "right"])
def test_a_shaped_board_fills_its_limits_or_sits_against_one_or_in_the_corner(facing: str):
    """Decided by Florian, 2026-10-14: a board made of a shape fills its two
    limits on an axis less its inset, or is refused; with one limit it sits
    against it, on the side the board would lie; with none, at the scope's
    front, left and bottom corner; and its box is its outline's. It sat at
    the limits' lowest corner in world terms, its box the limits', so in a
    cabinet facing elsewhere it lay elsewhere and its box missed it."""
    van = Box.from_size(width=600, depth=500, height=300)
    with cabinet("cab", van, front=van.side(facing)) as cab:
        shape = rect(width=100, depth=50)
        filled = board("filled", ply15, shape).on(cab.bottom).between(
            cab.left.into(10), cab.left.into(110), cab.front, cab.front.into(50))
        inset = board("inset", ply15, shape).on(cab.bottom.into(20)).between(
            cab.left.into(10), cab.left.into(120), cab.front, cab.front.into(60)).inset(5)
        against = board("against", ply15, shape).on(cab.bottom.into(40)).between(cab.right.into(20))
        side = board("side", ply15).on(cab.right)
        on_side = board("on_side", ply15, shape).on(cab.bottom.into(60)).between(side, cab.back.into(30))
        corner = board("corner", ply15, shape).on(cab.bottom.into(80)).inset(2)
        wrong = board("wrong", ply15, shape).on(cab.bottom.into(100)).between(cab.left.into(10), cab.left.into(120))
    assert _measured(cab, filled)[:2] == [(0, 50), (10, 110)]
    assert _measured(cab, inset)[:2] == [(5, 55), (15, 115)]
    width = cab.width
    assert _measured(cab, against)[:2] == [(0, 50), (width - 120, width - 20)]
    assert _measured(cab, on_side)[:2] == [(cab.depth - 80, cab.depth - 30), (width - 115, width - 15)]
    assert _measured(cab, corner)[:2] == [(2, 52), (2, 102)]
    for b in (filled, inset, against, on_side, corner):
        u0, v0, u1, v1 = b.outline.bounds
        assert (b.box().lo[b.u_axis], b.box().lo[b.v_axis], b.box().hi[b.u_axis], b.box().hi[b.v_axis]) == (u0, v0, u1, v1)
    with pytest.raises(LangError, match=r"the shape is 100 across on [xy], its limits less its inset leave 110"):
        wrong.box()


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
    assert [op.face for op in chamfers] == ["left", "right", "left"]
    assert left.outline.area == pytest.approx(area - 0.5 * 0.5 ** 2)
    with pytest.raises(LangError):
        left.chamfer(left.ops[1], 1)          # the unnamed hole
    with pytest.raises(LangError):
        left.chamfer(right.front.inner, 1)    # another board's edge


def test_an_edge_chamfer_is_on_its_big_face_whichever_face_names_it_first():
    """Found by fuzzing the placement: `side.front.inner` put the chamfer on
    the front face and `side.inner.front` on the inner one, so the face a
    board is machined from (the one more chamfers are made from) differed
    by how the edge was named."""
    cab = carcass()
    left, right = cab["left"], cab["right"]
    left.chamfer(left.front.inner, 1)
    right.chamfer(right.inner.front, 1)
    for side in (left, right):
        chamfer = side.ops[-1]
        assert isinstance(chamfer, Chamfer) and chamfer.face == side.inner.world_name
        assert side.machine_face.direction == side.inner.direction


# -- layout --------------------------------------------------------------------

def test_nest_is_given_once_takes_a_bool_and_reaches_the_layout() -> None:
    with module("m", Box.from_size(depth=500, width=300, height=15)) as m:
        a = board("a", ply15).on(m.bottom)
        b = board("b", ply15).on(m.bottom)
        c = board("c", ply15).on(m.bottom).manual()
        slat("d", slat_material("oak"), section=(20, 40)).on(m.bottom).edge_on(m.left).between(m.front, m.back)
    a.hole(d=8, at=a.top.center, depth=5)
    a.nest(False)                            # after the placement is used: it changes no shape
    with pytest.raises(LangError, match="nest\\(\\) given twice"):
        a.nest(True)
    with pytest.raises(LangError, match="True or False"):
        b.nest("no")  # pyright: ignore[reportArgumentType]
    parts = {p["path"]: p for p in build_layout()["modules"][0]["parts"]}
    assert (parts["m.a"]["nest"], parts["m.b"]["nest"], parts["m.c"]["nest"]) == (False, True, False)
    assert parts["m.d"]["kind"] == "slat" and parts["m.d"]["nest"] is False     # slats go on the cut list
    assert not a.nested and b.nested and c.nested       # a manual part is left out by the layout


def test_layout_json_roundtrip(tmp_path: Path) -> None:
    from lang.core.layout import write_layout
    cab = carcass()
    cab["left"].cut(rect(depth=60, height=100), at=cab["left"].outer.bottom.front, name="toekick")
    cab.export("worktop", cab.top)
    cab.check(no_interference)
    layout = write_layout(tmp_path / "layout.json")
    assert layout["version"] == 6
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


def test_shrunk_and_grown_take_one_amount_for_every_side():
    """Decided by Florian, 2026-10-15 (syntax.md item 5): a leading amount
    moves all six sides, a side's keyword overrides it for that side, and
    keywords alone move their sides only, as before."""
    b = Box.from_size(width=100, depth=200, height=300)       # x 0 to 200 (front low), y 0 to 100, z 0 to 300

    def spans(box: Box) -> list[tuple[float, float]]:
        return [(box.lo[a], box.hi[a]) for a in ("x", "y", "z")]

    assert spans(b.shrunk(5)) == [(5, 195), (5, 95), (5, 295)]
    assert spans(b.shrunk(5, front=0, top=-1)) == [(0, 195), (5, 95), (5, 301)]
    assert spans(b.shrunk(front=20)) == [(20, 200), (0, 100), (0, 300)]
    assert spans(b.grown(0.5)) == [(-0.5, 200.5), (-0.5, 100.5), (-0.5, 300.5)]
    assert spans(b.grown(0.5, front=0)) == [(0, 200.5), (-0.5, 100.5), (-0.5, 300.5)]
    assert spans(b.grown(top=0.5)) == [(0, 200), (0, 100), (0, 300.5)]
    assert spans(b.grown(2, left=1)) == spans(b.shrunk(-2, left=-1))


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
        floor = board("floor", ply9).on(m.bottom.into(10)).between(side.into(5), m.right, m.front.into(12), m.back)
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
        away = board("away", ply9).on(m.bottom).between(m.right, m.right.gap(100))
        with pytest.raises(LangError):
            side.cut(away)
        with pytest.raises(LangError):
            side.cut(Box.from_size(width=5, depth=100, height=9, origin=(0, 390, 20)))
        with pytest.raises(LangError):
            side.cut(away, at=side.inner.center)   # at= belongs to shapes only


def test_a_cut_by_a_board_or_its_box_reaching_under_a_hundredth_in_is_refused_alike():
    """Found by fuzzing the placement: a floor reaching 0.0036 mm into a
    side was refused as `side.cut(floor)`, which does not reach into the
    side (the section, narrower than 0.01 mm, is cleaned away), and made a
    pocket 0.0036 deep as `side.cut(floor.box())`."""
    with module("box", Box.from_size(width=400, depth=300, height=100)) as m:
        side = board("side", ply15).on(m.left)
        floor = board("floor", ply9).on(m.bottom.into(10)).between(side.into(0.0036), m.right)
        for region in (floor, floor.box()):
            with pytest.raises(LangError, match="does not reach into this board"):
                side.cut(region)
        deeper = board("deeper", ply9).on(m.bottom.into(30)).between(side.into(0.01), m.right)
        side.cut(deeper.box())
    assert len(side.ops) == 1


def test_a_cut_by_a_board_or_its_box_reaching_a_hundredth_in_makes_one_pocket():
    """Found by fuzzing the placement: a floor reaching 0.01 mm into a
    side, the least a cut by a board or a box must reach, made a pocket
    that deep as `side.cut(floor.box())` and was refused as
    `side.cut(floor)`: the floor's section across the side, as narrow, was
    cleaned away. The section is taken as it is."""
    with module("box", Box.from_size(width=400, depth=300, height=100)) as m:
        sides = [board(f"side{k}", ply15).on(m.left) for k in range(2)]
        floor = board("floor", ply9).on(m.bottom.into(10)).between(sides[0].into(0.01), m.right)
        sides[0].cut(floor)
        sides[1].cut(floor.box())
    a, c = sides[0].ops[0], sides[1].ops[0]
    assert isinstance(a, Pocket) and isinstance(c, Pocket)
    assert a.depth == pytest.approx(0.01) and c.depth == pytest.approx(0.01) and a.face == c.face
    assert a.shape.geometry.symmetric_difference(c.shape.geometry).area < 1e-9


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
        shelf = board("shelf", ply15).on(cab.bottom.into(355))    # straddles the middle at 360
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
        floor = board("floor", ply9).on(m.bottom.into(10)).between(side.inner.into(5), m.right)
        side.pocket(rect(depth=300, height=9.5), at=side.inner.bottom(floor.bottom).front,
                    depth=5, name="groove")
    assert no_interference(m) == []
    # a floor reaching deeper than the groove hits material
    with module("box2", Box.from_size(width=400, depth=300, height=100)) as m2:
        side = board("side", ply15).on(m2.left)
        floor = board("floor", ply9).on(m2.bottom.into(10)).between(side.inner.into(6), m2.right)
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


def test_machine_names_the_face_the_board_is_machined_from_however_it_is_named():
    """The holes would make the inner face the machined one; `machine()`
    wins, named as a face, inner or outer, a box side or a direction."""
    with module("cab", Box.from_size(width=1200, depth=500, height=720)) as cab:
        sides = [board(f"s{k}", ply15).on(cab.left + 100 * k, toward=cab.right) for k in range(5)]   # left of the middle
    namings: list[Face | Side | Direction | InnerOuter] = [sides[0].outer, "outer", cab.left, cab.left.outward,
                                                           sides[4].left]
    for side, name in zip(sides, namings):
        side.hole(d=5, depth=10, at=side.right.center)
        side.hole(d=5, depth=10, at=side.right.front(50).bottom(50))
        side.machine(name)
        assert side.machine_face.direction == side.left.direction
        assert side.to_layout()["machine"] == side.left.world_name
        assert side.show_face.direction == side.left.direction       # machine() leaves the show face alone


def test_machine_may_come_at_any_time_once():
    with module("cab", Box.from_size(width=600, depth=500, height=720)) as cab:
        early = board("early", ply15).machine(cab.right).on(cab.left)      # before the placement
        late = board("late", ply15).on(cab.right)
    late.hole(d=5, depth=10, at=late.inner.center)
    late.machine(late.outer)                                             # after the placement and its operations
    assert early.machine_face.direction == early.inner.direction
    assert late.machine_face.direction == late.outer.direction
    with pytest.raises(LangError, match="machine\\(\\) given twice"):
        late.machine(late.inner)
    assert late.machine_face.direction == late.outer.direction


def test_machine_takes_a_big_face_of_this_board_only():
    with module("cab", Box.from_size(width=600, depth=500, height=720)) as cab:
        side = board("side", ply15).on(cab.left)
        other = board("other", ply15).on(cab.right)
        unplaced = board("unplaced", ply15).machine(cab.front).on(cab.bottom)
        straddling = board("straddling", ply15).center(cab.left + 300).machine("inner")
        rail = slat("rail", slat_material("oak"), section=(20, 40)).on(cab.bottom).edge_on(cab.front) \
            .between(cab.left, cab.right)
    side.box()
    with pytest.raises(LangError, match="front is a narrow face.*(left or right|right or left)"):
        side.machine(side.front)                         # placed: refused at once
    with pytest.raises(LangError, match="not a face of this board"):
        side.machine(other.inner)
    with pytest.raises(LangError, match="expected 'inner' or 'outer', not 'sideways'"):
        side.machine("sideways")  # pyright: ignore[reportArgumentType]
    side.machine(side.inner)                             # the refusals changed nothing
    assert side.machine_face.direction == side.inner.direction
    with pytest.raises(LangError, match="front is a narrow face"):
        unplaced.machine_face                            # given before the placement: refused when read
    with pytest.raises(LangError, match="ambiguous"):
        straddling.machine_face
    with pytest.raises(LangError, match="a slat is not machined"):
        rail.machine(cab.bottom)


# -- review fixes 2026-10-12: limits ------------------------------------------------

def _partitions() -> tuple[Scope, Board, Board]:
    """Two partitions, both left of the middle of a 1000 wide box: y
    100..115 and 300..315."""
    with module("m", Box.from_size(width=1000, depth=400, height=700)) as m:
        p1 = board("p1", ply15).on(m.left.into(100), toward=m.right)
        p2 = board("p2", ply15).on(m.left.into(300), toward=m.right)
    return m, p1, p2


def test_between_two_parts_takes_the_faces_that_face_each_other():
    """The box's middle (y 500) lies right of both partitions; the shelf
    still runs from the first one's right face to the second one's left
    face, not through the second one."""
    m, p1, p2 = _partitions()
    with m:
        shelf = board("shelf", ply15).on(m.bottom.into(300), toward=m.top).between(p1, p2)
        check(no_interference)
    assert (shelf.box().lo["y"], shelf.box().hi["y"]) == (115, 300)
    assert build_layout()["problems"] == []


def test_between_a_part_and_a_position_takes_the_face_toward_the_position():
    m, p1, p2 = _partitions()
    with m:
        shelf = board("shelf", ply15).on(m.bottom.into(300), toward=m.top).between(m.left, p2.gap(1))
        reach = board("reach", ply15).on(m.bottom.into(400), toward=m.top).between(p1.into(5), m.right)
    assert (shelf.box().lo["y"], shelf.box().hi["y"]) == (0, 299)      # p2's left face, 1 away from it
    assert (reach.box().lo["y"], reach.box().hi["y"]) == (110, 1000)   # p1's right face, 5 into it


def test_a_board_between_one_board_keeps_to_its_side_of_it():
    """Found by fuzzing the placement: a back between a bottom lying across
    the box's middle ran through the bottom. Its face toward the middle is
    its top (46 to 61: the bottom, 40 to 55: the top, the middle at 50),
    but the back went the way that face lies from the middle, down to the
    box's bottom. It goes from the face away from the board."""
    for z, want in ((40, (55, 100)), (46, (0, 46))):
        with module(f"m{z}", Box.from_size(width=600, depth=400, height=100)) as m:
            bottom = board("bottom", ply15).on(m.bottom.into(z))
            back = board("back", ply9).on(m.back).between(bottom)
            check(no_interference)
        assert (back.box().lo["z"], back.box().hi["z"]) == want
    assert build_layout()["problems"] == []


@pytest.mark.parametrize("case, error", [
    ("twice", r"between\(\): m\.left is given twice on y"),
    ("overlapping", r"between\(\): m\.low and m\.high overlap on z, so nothing lies between them"),
    ("position inside", r"between\(\): the limit at y=590 lies inside m\.right on y"),
    ("gap inside", r"between\(\): m\.panel's face, moved by gap\(\), lies inside m\.door on x"),
    ("middle", r"between\(\): the only limit on y, at y=300, lies at the middle of its room"),
    ("centred board", r"between\(\): m\.divider is the only limit on y and lies across the middle of the box"),
])
def test_ambiguous_limits_are_refused(case: str, error: str):
    """Decided by Florian, 2026-10-14: limits that leave it open where a
    board lies are refused, each naming what is ambiguous: limits that
    overlap (two boards overlapping each other, the same board twice, a
    position or a face moved by `gap()` inside a board), a single limit at
    the middle of the box, a board as the only limit centred in the box.
    They put the board inside its limits, or on a side the world frame
    chose."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        right = board("right", ply15).on(m.right)
        door = board("door", ply15).on(m.front)                            # x 0 to 15
        panel = board("panel", ply15).on(door.back)                        # x 15 to 30, touching it
        low = board("low", ply15).on(m.bottom.into(100))                       # z 100 to 115
        high = board("high", ply15).on(m.bottom.into(110))                     # z 110 to 125
        divider = board("divider", ply15).center(m.center("width"))
        limits = {"twice": [left, left.into(5)], "overlapping": [low, high],
                  "position inside": [right, m.left.into(590)], "gap inside": [door, panel.gap(1.5)],
                  "middle": [m.left.into(300)], "centred board": [divider]}[case]
        # (standing across the width for the limits on x, against the back for the others)
        x = board("x", ply9).on(m.left.into(200)) if case == "gap inside" else board("x", ply9).on(m.back)
        x.between(*limits)
    with pytest.raises(LangError, match=error):
        x.box()


def test_limits_near_the_ambiguous_ones_are_kept():
    """Decided by Florian, 2026-10-14 (see above): a board's own face moved
    into it, a limit off the middle and a board off it are fine."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        a = board("a", ply9).on(m.back).between(left.into(5), m.right)
        b = board("b", ply9).on(m.back.into(20)).between(m.left.into(299))
        c = board("c", ply9).on(m.back.into(40)).between(board("off", ply15).center(m.center("width") + 1))
    assert (a.box().lo["y"], a.box().hi["y"]) == (10, 600)
    assert (b.box().lo["y"], b.box().hi["y"]) == (299, 600)
    assert (c.box().lo["y"], c.box().hi["y"]) == (0, 293.5)


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
        parallel = board("parallel", ply15).on(m.left.into(100), toward=m.right).between(left)
        thick = board("thick", ply15).on(m.bottom.into(100), toward=m.top).between(left, Pos("z", 50))
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


def test_show_takes_the_board_s_own_inner_face():
    """Found by fuzzing the placement: `side.show(side.inner)`, the form
    show()'s docstring gives, was always refused, since naming the inner
    face resolves the placement, which froze show(). It is frozen once the
    show face is used instead."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        side = board("side", ply15).on(m.left)
        side.show(side.inner)
        other = board("other", ply15).on(m.right)
        other.hole(d=5, depth=5)                  # at the show face's centre: it is used
    assert side.show_face.name == "right" and side.to_layout()["show"] == "right"
    with pytest.raises(LangError, match="show\\(\\) after the show face was used"):
        other.show(other.inner)


# -- review fixes: depths --------------------------------------------------------------

def test_a_depth_past_the_opposite_face_is_an_error():
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        with pytest.raises(LangError, match="depth 40 reaches past the opposite face, 15 from"):
            left.hole(d=5, at=left.inner.center, depth=40)
        with pytest.raises(LangError, match="reaches past the opposite face, 400 from the front face"):
            left.hole(d=5, at=left.front.center, depth=401)
        with pytest.raises(LangError, match=r"to\(left.left, leave=-1\): a negative leave= reaches past the face"):
            left.pocket(rect(depth=50, height=50), at=left.inner.center, depth=to(left.outer, leave=-1))
        left.hole(d=5, at=left.inner.center, depth=15)            # as deep as the board: fine
        left.hole(d=5, at=left.front.bottom(50), depth=400)
    assert len(left.ops) == 2


def test_a_depth_that_does_not_reach_into_the_board_is_an_error():
    """Found by fuzzing the placement: `to(left.outer, leave=20)` on a 15 mm
    board made a hole -5 deep, accepted where the number -5 is refused;
    and `to(left.outer, leave=15)` was 0 deep at some places and 2e-15 at
    others, refused or not. A depth under 0.01 mm reaches nothing either
    way."""
    for name, y in (("at0", 0.0), ("far", 0.1)):
        with module(name, Box.from_size(width=600, depth=400, height=700, origin=(0, y, 0))) as m:
            left = board("left", ply15).on(m.left)
            for depth in (to(left.outer, leave=20), to(left.outer, leave=15), to(left.outer, leave=14.995), -5, 0.005):
                with pytest.raises(LangError, match="does not reach into the board"):
                    left.hole(d=5, at=left.inner.center, depth=depth)
            left.hole(d=5, at=left.inner.center, depth=to(left.outer, leave=14.99))
        hole = left.ops[0]
        assert isinstance(hole, Hole) and hole.depth == pytest.approx(0.01)


def test_to_leaves_what_leave_says():
    """Decided by Florian, 2026-10-15 (syntax.md item 7): `to(face,
    leave=3)` leaves 3 mm at the face, `to(face)` reaches it; the signed
    offset, `to(face, -3)`, of which only zero or a negative was legal,
    goes. A number given by position is an error saying to write leave=,
    and so is a negative leave=. The layout records the depth as written."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        left.pocket(rect(depth=50, height=50), at=left.inner.front(40), depth=to(left.outer, leave=3))
        left.pocket(rect(depth=50, height=50), at=left.inner.back(40), depth=to("outer", leave=0.5))
        left.hole(d=5, at=left.inner.center, depth=to(left.outer))
        left.hole(d=5, at=left.front.center, depth=to(left.back, leave=100))
        for n in (-3, 3):
            with pytest.raises(LangError, match=re.escape(f"to(left.left, {n}): give what is left at the face as "
                                                          "leave=, to(left.left, leave=3).")):
                to(left.outer, n)  # type: ignore[arg-type]
        with pytest.raises(LangError, match=re.escape("to(outer, -2): give what is left at the face as leave=, "
                                                      "to(outer, leave=2).")):
            to("outer", -2)  # type: ignore[arg-type]
        with pytest.raises(LangError, match=re.escape("to(outer, leave=-0.5): a negative leave= reaches past")):
            to("outer", leave=-0.5)
        with pytest.raises(LangError, match=re.escape("depth to(left, leave=15) does not reach into the board: "
                                                      "that face is 15 from the right face.")):
            left.hole(d=5, at=left.inner.center, depth=to(left.outer, leave=15))
    pockets = [op for op in left.ops if isinstance(op, Pocket)]
    holes = [op.op if isinstance(op, EdgeOp) else op for op in left.ops if isinstance(op, (Hole, EdgeOp))]
    assert [(p.depth, p.depth_spec) for p in pockets] == [(12, "to(left, leave=3)"), (14.5, "to(outer, leave=0.5)")]
    assert [(h.depth, h.depth_spec, isinstance(h, Hole) and h.through) for h in holes] == [
        (15, "to(left)", True), (300, "to(back, leave=100)", False)]


def test_to_names_a_face_of_the_board_itself():
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        bottom = board("bottom", ply15).on(m.bottom).between(left, m.right)
        with pytest.raises(LangError, match=r"to\(m.left.right\) names a face of another part"):
            bottom.pocket(rect(depth=50, width=50), at=bottom.top.center, depth=to(left.inner, leave=3))
        bottom.pocket(rect(depth=50, width=50), at=bottom.top.center, depth=to(bottom.bottom, leave=3))
    assert isinstance(bottom.ops[0], Pocket) and bottom.ops[0].depth == 12


def test_through_a_narrow_face_reaches_across_the_board():
    """The left side is 400 deep (x): a hole through its front face is 400
    deep, in the layout as in the plan."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        left = board("left", ply15).on(m.left)
        left.hole(d=8, at=left.front.bottom(50), depth=through, name="pin")
        left.pocket(rect(width=5, height=20), at=left.back.center, depth=through, name="mortise")
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
        board("foot", ply15).on(cab.bottom).between(cab.left, cab.left.into(50), cab.front, cab.front.into(50))
        assert cab.interior.lo["z"] == 0
        board("bottom", ply15).on(cab.bottom).between(cab.left.into(100), cab.right)
        assert cab.interior.lo["z"] == 15


def test_problems_are_listed_once():
    """The module lists its own; the layout lists all of them once, and
    the emitter's plan reports each once."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        board("a", ply15).on(m.left)
        board("b", ply15).on(m.left.into(5), toward=m.right)
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


def test_spread_runs_from_its_start_and_fits_alike_anywhere():
    """Found by fuzzing the placement: spread() gave its positions from the
    lower coordinate whichever end came first, so a row in a cabinet facing
    another way ran the other way round; and a span of a whole number of
    pitches fitted one position fewer where rounding left it a hair short
    (from 0.1 to 64.1 is 63.99999999999999)."""
    assert spread(Pos("z", 100), Pos("z", 0), count=3) == [Pos("z", 100), Pos("z", 50), Pos("z", 0)]
    assert [p.value for p in spread(Pos("z", 100), Pos("z", 0), pitch=32)] == pytest.approx([98, 66, 34, 2])
    for start in (0.0, 0.1, 1234.1):
        assert len(spread(Pos("z", start), Pos("z", start + 64), pitch=32)) == 3
        assert len(spread(Pos("z", start + 64), Pos("z", start), pitch=32)) == 3


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


def test_a_hole_as_far_off_the_face_as_the_tolerance_is_on_it_wherever_the_board_lies():
    """Found by fuzzing the placement: a hole lined up with another board's
    face, 0.001 mm off this board's edge, as far as a point may lie off a
    face and still be on it (`ON_FACE_TOLERANCE`), was refused as off the
    face where the module lay at the origin (18.001 - 18 is a hair more
    than 0.001) and made where it lay elsewhere."""
    for k, x in enumerate((0.0, 817.7)):
        with module(f"m{k}", Box.from_size(width=600, depth=400, height=700, origin=(x, 0, 0))) as m:
            side = board("side", ply15).on(m.left).between(m.front.into(18.001))
            side.hole(d=8, at=side.inner.front(m.front.into(18)).bottom(100), depth=5)
        assert len(side.ops) == 1


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


@pytest.mark.parametrize("origin", [0.0, 0.1, 260.0, 1234.56, -5255.0, 3000.3, 17.25, 99.9])
def test_a_hole_through_the_board_that_leaves_a_corner_hanging_at_a_point_splits_it(origin: float):
    """Found by fuzzing the checks: a 118 mm hole through a 519 by 746
    board, tangent to its edge and over the next one, cuts the corner off
    but for the point where it touches the edge. It was refused at most
    places and kept where the rounding put the circle 1e-15 short of the
    edge (at 0.1). It is refused at every place now, as a through pocket
    of that circle is; one touching the edge further in, which cuts
    nothing off, is kept, as Fusion builds it."""
    with module("m", Box.from_size(width=746, depth=519, height=100, origin=(origin, origin, 0))) as m:
        panel = board("panel", sheet_material("birch", t=31)).on(m.bottom)
    corner = (origin + 482, origin + 59)
    with pytest.raises(LangError, match="the hole 'corner' goes through the board and splits it in pieces"):
        panel.add_hole(panel.top, corner, 118, through, name="corner")
    with pytest.raises(LangError, match="splits it in pieces"):
        panel.add_pocket(panel.top, Shape(circle_geometry(corner, 59)), through)
    panel.add_hole(panel.top, (origin + 200, origin + 59), 118, through)          # touches the edge only
    panel.add_pocket(panel.top, Shape(circle_geometry((origin + 200, origin + 687), 59)), through)
    assert [op.kind for op in panel.ops] == ["hole", "pocket"]


@pytest.mark.parametrize("origin", [0.0, 0.1, 260.0, 1234.56, -5255.0, 3000.3, 17.25, 99.9])
def test_a_cut_that_leaves_a_corner_hanging_at_a_point_splits_the_board(origin: float):
    """Found by fuzzing the checks: the 118 mm circle of the hole above,
    cut through the board, was refused at most places and kept at 0.1, as
    the hole was. It splits the board everywhere now; a circle cut that
    touches the edge further in, and cuts nothing off, is kept, as Fusion
    builds it [Florian, 2026-10-12]."""
    with module("m", Box.from_size(width=746, depth=519, height=100, origin=(origin, origin, 0))) as m:
        panel = board("panel", sheet_material("birch", t=31)).on(m.bottom)
        with pytest.raises(LangError, match="the cut splits the board in pieces"):
            panel.add_cut(Shape(circle_geometry((origin + 482, origin + 59), 59)))
        with pytest.raises(LangError, match="the cut corner splits the board in pieces"):
            panel.cut(circle(118), at=panel.top.front(423).left(0), name="corner")
        panel.cut(circle(118), at=panel.top.front(141).left(0), name="touching")
    assert [op.kind for op in panel.ops] == ["cut"] and len(panel.outline.polygons()) == 1


def test_material_held_by_less_than_a_hundredth_of_a_millimetre_is_cut_free():
    """Found by fuzzing the placement: a notch at a board's corner with its
    own corner clipped leaves that corner's triangle of the board, cut
    free, and was refused as splitting the board, but where the module lay
    4 m out the notch's edge came 5e-13 mm off the board's and held the
    triangle on by that hairline: one piece, accepted. A through pocket
    likewise. Nothing narrower than 0.01 mm holds material on."""
    far = -3999.9999999999995
    for name, origin in (("near", 0.0), ("far", far)):
        with module(name, Box.from_size(width=600, depth=400, height=100, origin=(origin, origin, 0))) as m:
            panel = board("panel", ply15).on(m.bottom)
            notch = rect(depth=196.47573931604643, width=20).clip(back=5, right=98.23786965802322)
            with pytest.raises(LangError, match="splits the board in pieces"):
                panel.cut(notch, at=panel.top.back.right, name="notch")
            with pytest.raises(LangError, match="splits it in pieces"):
                panel.pocket(notch, at=panel.top.back.right, depth=through)
        assert panel.ops == [] and len(panel.outline.polygons()) == 1


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


def test_pockets_from_either_face_through_together_may_not_leave_nothing_or_split_the_board():
    """Found by fuzzing dog bones: two circle pockets, from either face of a
    6 mm board and 3 deep each, covered all of it, so together they left
    nothing of the board, which the preview could not mesh. Where pockets
    or holes from opposite faces meet as deep as the board together, they
    go through there, and are held to what a pocket through it is."""
    with module("m", Box.from_size(width=40, depth=40, height=100)) as m:
        panel = board("panel", sheet_material("birch", t=6)).on(m.bottom)
        panel.add_pocket(panel.top, Shape(Point(0, 0).buffer(80.5, quad_segs=64)), 3, name="top_dish")
        with pytest.raises(LangError, match=r"^m\.panel: the pocket 'bottom_dish' goes through the board with the "
                                            r"pocket 'top_dish' from the other face and leaves nothing of it\.$"):
            panel.add_pocket(panel.bottom, Shape(Point(0, 0).buffer(81, quad_segs=64)), 3, name="bottom_dish")
    with module("n", Box.from_size(width=40, depth=40, height=100)) as n:
        strip = board("strip", sheet_material("birch", t=6)).on(n.bottom)
        strip.add_pocket(strip.top, Shape(shapely_box(-1, 15, 41, 25)), 3, name="top_band")
        with pytest.raises(LangError, match="goes through the board with the pocket 'top_band' from the other face "
                                            "and splits it in pieces"):
            strip.add_pocket(strip.bottom, Shape(shapely_box(-1, 10, 41, 30)), 4)          # along it, 7 deep in all
        strip.add_pocket(strip.bottom, Shape(shapely_box(-1, 10, 41, 30)), 2)              # 5 deep in all: no way through
        strip.add_pocket(strip.bottom, Shape(shapely_box(5, 18, 8, 22)), 4)                # through, but only a window
    assert [len(panel.ops), len(strip.ops)] == [1, 3]


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
