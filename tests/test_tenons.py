"""Integral tenons and their mortises (`lang.joints.tenons`)."""
import math

import pytest
from shapely.geometry import Point, box

from lang import *
from lang.core.layout import build_layout
from lang.core.ops import Cut, Pocket
from helpers import has_material, ply15, ply18

O = 6 / (2 * math.sqrt(2))          # a corner relief's centre, along each edge from the corner
R = 3.05                            # its radius: the 6 mm tool plus 0.1, halved


def _unit() -> tuple[Scope, Board, Board, Board]:
    """Two 15 mm sides (y) and an 18 mm shelf between them at z 400..418, in
    a 600 wide (y), 300 deep (x), 800 high box."""
    with module("unit", Box.from_size(width=600, depth=300, height=800)) as u:
        left = board("left", ply15).on(u.left)
        right = board("right", ply15).on(u.right)
        shelf = board("shelf", ply18).on(Pos("z", 400), toward=u.top).between(left, right)
        check(no_interference)
    return u, left, right, shelf


def _named(part: Board, prefix: str) -> list[str]:
    names = [getattr(op, "name", None) for op in part.ops]
    return [n for n in names if isinstance(n, str) and n.startswith(prefix)]


def test_the_shelf_grows_tenons_through_the_sides():
    u, left, right, shelf = _unit()
    with u:
        shelf.join(left, right, using=tenons(count=2, width=50))
    # the shelf's frame is (x, y); its end is at y = 15, the tenons reach y = 0
    assert has_material(shelf, (55, 1), (245, 1), (55, 599)) == [True, True, True]
    assert has_material(shelf, (150, 7), (10, 7)) == [False, False]          # between and beside them: the side
    # a corner relief at each root, cutting into the shoulder and the tenon's side
    assert has_material(shelf, (30 - O, 15.5), (30 - O, 16.0), (30.5, 13)) == [False, True, False]
    assert _named(shelf, "tenon_left") == ["tenon_left_1_relief", "tenon_left_2_relief"]
    assert build_layout()["problems"] == []


def test_the_sides_get_through_mortises_with_corner_reliefs():
    u, left, _, shelf = _unit()
    with u:
        shelf.join(left, using=tenons(count=2, width=50))
    # left's frame is (x, z): 0.1 mm play along and across, through the side
    assert has_material(left, (55, 409), (29.96, 409), (55, 399.96)) == [False, False, False]
    assert has_material(left, (29.9, 409), (55, 399.9), (55, 420)) == [True, True, True]
    # each corner's relief reaches 0.05 past it along the diagonal
    assert has_material(left, (80.08, 418.08), (80.1, 418.1)) == [False, True]
    mortise = left.op("mortise_shelf_1").op
    assert isinstance(mortise, Cut)
    lobe = Point(O, O).buffer(R, quad_segs=16).difference(box(0, 0, 100, 100)).area    # outside one corner
    assert mortise.shape.area == pytest.approx(50.1 * 18.1 + 4 * lobe, rel=1e-6)


def test_blind_mortises_are_pockets_half_a_millimetre_deeper():
    u, left, _, shelf = _unit()
    with u:
        shelf.join(left, using=tenons(count=1, width=60, remaining=6))
    assert has_material(shelf, (150, 6.5), (150, 5.5)) == [True, False]       # 15 - 6 = 9 long, from y = 15 to 6
    (pocket,) = [op for op in left.ops if isinstance(op, Pocket)]
    assert pocket.face == "right" and pocket.depth == pytest.approx(9.5) and pocket.depth_spec == "to(left, -5.5)"
    assert left.outline.geometry.area == 300 * 800                     # nothing through


def test_hidden_dog_bones_sit_under_the_shoulder():
    u, left, _, shelf = _unit()
    with u:
        shelf.join(left, using=tenons(count=1, width=60, dogbones="hidden"))
    # the root relief bites into the tenon only, tangent to the shoulder
    assert has_material(shelf, (120.5, 13), (119.5, 15.5), (122.0, 15 - R)) == [False, True, False]
    # the mortise reliefs reach past its ends along the joint, within the shelf's thickness
    assert has_material(left, (120 - 0.05 - R + 0.1, 400 - 0.05 + R)) == [False]
    assert has_material(left, (180.05 + 1, 399.9)) == [True]                   # not past the long side


def test_even_tenons_are_as_wide_as_the_gaps():
    u, left, _, shelf = _unit()
    with u:
        shelf.join(left, using=tenons(count=3, even=True))
    # (300 - 2 x 30) / 5 = 48: tenons at 30..78, 126..174, 222..270
    assert has_material(shelf, (30.5, 1), (77.5, 1), (78.5, 1), (125.5, 1), (126.5, 1)) == [True, True, False, False, True]


def test_a_tenon_flush_with_the_board_end_gets_no_relief_there():
    u, left, _, shelf = _unit()
    with u:
        shelf.join(left, using=tenons(width=50, at=[Pos("x", 25)]))
    relief = shelf.op("tenon_left_1_relief").op
    assert isinstance(relief, Cut) and relief.shape.bounds[0] > 49         # only at the tenon's inner side
    # the mortise runs out of the side's front edge there, with reliefs only inside
    mortise = left.op("mortise_shelf_1").op
    assert isinstance(mortise, Cut) and mortise.shape.bounds[0] == pytest.approx(-0.05)
    assert has_material(left, (0.1, 409)) == [False]


def test_either_board_can_make_the_call():
    u, left, _, shelf = _unit()
    with u:
        left.join(shelf, using=tenons(count=2, width=50))
    assert has_material(shelf, (55, 1)) == [True] and _named(left, "mortise_shelf") == ["mortise_shelf_1", "mortise_shelf_2"]


def test_tenon_errors():
    u, left, right, shelf = _unit()
    with u:
        with pytest.raises(LangError, match="overlap"):
            shelf.join(left, using=tenons(width=50, at=[Pos("x", 100), Pos("x", 140)]))
        with pytest.raises(LangError, match="reaches past the contact"):
            shelf.join(left, using=tenons(width=50, at=[Pos("x", 10)]))
        with pytest.raises(LangError, match="leaves no tenon"):
            shelf.join(left, using=tenons(count=1, width=50, remaining=15))
        with pytest.raises(LangError, match="must be wider than 6.1"):
            shelf.join(left, using=tenons(count=1, width=6, dogbones="hidden"))
        with pytest.raises(LangError, match="leaves no room"):
            shelf.join(left, using=tenons(count=2, width=250, margin=30))
        with pytest.raises(LangError, match="does not touch"):
            left.join(right, using=tenons(count=1, width=50))
        with pytest.raises(LangError, match="splits the board"):
            shelf.join(left, using=tenons(width=300, at=[Pos("x", 150)]))
    for message, make in (("give width=, or even=True", lambda: tenons(count=2)),
                          ("works the width out", lambda: tenons(count=2, width=50, even=True)),
                          ("two tenons or more", lambda: tenons(count=1, even=True)),
                          ("need a width", lambda: tenons(at=[Pos("x", 1)])),
                          ("give count= or at=", lambda: tenons(width=50))):
        with pytest.raises(LangError, match=message):
            make()
    assert all(p.ops == [] for p in (left, right)) and len(shelf.ops) == 0
