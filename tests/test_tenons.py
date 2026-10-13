"""Integral tenons and their mortises (`lang.joints.tenons`)."""
import math

import pytest
from shapely.geometry import box

from lang import *
from lang.core.cutouts import circle_geometry
from lang.core.layout import build_layout
from lang.core.ops import Cut, Hole, Pocket
from helpers import has_material, ply15, ply18, state

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
    lobe = circle_geometry((O, O), R).difference(box(0, 0, 100, 100)).area    # outside one corner
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


def test_hidden_dog_bones_need_their_whole_width():
    """A hidden relief is the tool plus the relief across (6.1): a 5 mm
    shelf's mortise, 5.1 across the joint, would show it bulging 1 mm past
    both long sides, outside the shoulder; the check compared the mortise
    with the radius before. With 1.1 of play across the reliefs fit."""
    with module("unit", Box.from_size(width=600, depth=300, height=800)) as u:
        left = board("left", ply15).on(u.left)
        thin = board("thin", material("birch", t=5)).on(Pos("z", 100), toward=u.top).between(left, u.right)
        before = state(thin, left)
        with pytest.raises(LangError, match=r"^unit\.thin: tenons with unit\.left: hidden dog bones are 6\.1 across, "
                                            r"wider than the mortises across the joint \(5\.1\)"):
            thin.join(left, using=tenons(count=1, width=50, dogbones="hidden"))
        assert state(thin, left) == before
        thin.join(left, using=tenons(count=1, width=50, dogbones="hidden", clearance=(0.1, 1.1)))
    mortise = left.op("mortise_thin_1").op
    assert isinstance(mortise, Cut)
    assert (mortise.shape.bounds[1], mortise.shape.bounds[3]) == pytest.approx((99.45, 105.55))   # 0.55 per side


def test_hidden_dog_bones_must_not_reach_past_the_tenons_end():
    """They reach 6.1 along the tenon from the shoulder: with remaining=9.5
    the tenon into the 15 mm side is 5.5 long."""
    u, left, _, shelf = _unit()
    with u:
        with pytest.raises(LangError, match="hidden dog bones reach 6.1 along the tenons from the shoulder, past the "
                                            "end of the 5.5 mm tenons"):
            shelf.join(left, using=tenons(count=1, width=50, remaining=9.5, dogbones="hidden"))
        shelf.join(left, using=tenons(count=1, width=50, remaining=8.9, dogbones="hidden"))    # 6.1 long: fits



def test_the_tool_must_fit_between_the_tenons_and_leave_them_standing():
    """Found by fuzzing: five tenons 1.1 wide and 1.1 apart, with 8 mm
    corner dog bones, each biting 1.2 into a tenon's side at its root: they
    ate the tenons, and the shelf was left with islands. With dog bones,
    the gaps between the tenons must be at least the tool, which cuts them,
    and the two corner dog bones at a tenon's root must leave it standing."""
    u, left, _, shelf = _unit()
    with u:
        before = state(left, shelf)
        with pytest.raises(LangError, match=r"^unit\.shelf: tenons with unit\.left: the 5 mm gaps between the tenons "
                                            r"are narrower than the 6 mm tool that cuts them"):
            shelf.join(left, using=tenons(width=20, at=[Pos("x", 100), Pos("x", 125)]))
        with pytest.raises(LangError, match=r"corner dog bones cut 0\.929 into each side of a tenon at its root; the "
                                            r"tenons must be wider than 1\.86"):
            shelf.join(left, using=tenons(width=1.5, at=[Pos("x", 100)]))
        assert state(left, shelf) == before
        shelf.join(left, using=tenons(width=20, at=[Pos("x", 100), Pos("x", 126)]))      # a 6 mm gap: it fits


def test_tenons_without_dog_bones_leave_square_corners():
    """dogbones=None, as half laps and grooves take it: square roots and
    mortises, for board.dogbones() or another way of relieving them."""
    u, left, _, shelf = _unit()
    with u:
        shelf.join(left, using=tenons(count=2, width=50, margin=10, dogbones=None))
    assert _named(shelf, "tenon_") == [] and _named(left, "mortise_") == ["mortise_shelf_1", "mortise_shelf_2"]
    mortise = left.op("mortise_shelf_1").op
    assert isinstance(mortise, Cut) and mortise.shape.area == pytest.approx(50.1 * 18.1)
    assert mortise.shape.bounds == pytest.approx((9.95, 399.95, 60.05, 418.05))     # the margin of 10 counts
    left.dogbones()
    shelf.dogbones()
    build_layout()
    assert [op.name for op in left.ops if isinstance(op, Cut)] == [
        "mortise_shelf_1", "mortise_shelf_2", "mortise_shelf_1_dogbones", "mortise_shelf_2_dogbones"]


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


def test_a_join_that_fails_on_its_second_board_changes_nothing():
    """The left side takes its tenons; the right one is a rail as high as
    the shelf, which its mortise would cut in two. The shelf has grown its
    first tenons by then: every board is restored, and the tenons record
    nothing, so no joint can sit in gaps they never made."""
    with module("unit", Box.from_size(width=600, depth=300, height=800)) as u:
        left = board("left", ply15).on(u.left)
        rail = board("rail", ply15).on(u.right).between(Pos("z", 400), Pos("z", 418))
        shelf = board("shelf", ply18).on(Pos("z", 400), toward=u.top).between(left, rail)
        t = tenons(count=2, width=50)
        before = state(shelf, left, rail)
        with pytest.raises(LangError, match=r"^unit\.shelf: tenons with unit\.rail: unit\.rail: the cut "
                                            r"mortise_shelf_1 splits the board in pieces"):
            shelf.join(left, rail, using=t)
        assert state(shelf, left, rail) == before
        assert t.made == []
        with pytest.raises(LangError, match="not joined with the tenons given"):
            shelf.join(left, using=screws(gaps=t))
        shelf.join(left, using=t)                                       # the pair that fits still joins
    assert [p.contact.face_on for p in t.made] == [left]


def test_one_tenon_joint_for_two_pairs():
    """One tenons object joins two shelves; the screws in its gaps find
    each shelf's own tenons."""
    u, left, right, shelf = _unit()
    with u:
        low = board("low", ply18).on(Pos("z", 100), toward=u.top).between(left, right)
        t = tenons(count=2, width=50, margin=50)                      # tenons 50..100 and 200..250
        shelf.join(left, using=t)
        low.join(right, using=t)
        shelf.join(left, using=screws(gaps=t))
        low.join(right, using=screws(gaps=t, offset=12))
    assert len(t.made) == 2
    assert [h.u for h in left.ops if isinstance(h, Hole) and (h.name or "").startswith("screw_")] == [25, 150, 275]
    assert [(h.u, h.v) for h in right.ops if isinstance(h, Hole) and (h.name or "").startswith("screw_")] == [
        (38, 109), (112, 109), (188, 109), (262, 109)]


def test_tenons_are_numbered_across_the_contacts_of_a_pair():
    """The shelf's end notched in the middle meets the side twice, x 0..100
    and 200..300: one tenon each, numbered on."""
    u, left, _, shelf = _unit()
    with u:
        shelf.cut(rect(depth=100, width=20), at=shelf.top.left, name="notch")
        shelf.join(left, using=tenons(count=1, width=50))
    assert _named(shelf, "tenon_") == ["tenon_left_1_relief", "tenon_left_2_relief"]
    assert _named(left, "mortise_") == ["mortise_shelf_1", "mortise_shelf_2"]
    assert has_material(shelf, (50, 1), (250, 1), (150, 1)) == [True, True, False]
    before = state(shelf, left)
    with u, pytest.raises(LangError, match="unit.shelf and unit.left are joined with tenons already"):
        shelf.join(left, using=tenons(count=1, width=10))         # on the shoulders the first join left
    assert state(shelf, left) == before


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
        with pytest.raises(LangError, match=r"^unit\.left: tenons with unit\.right: the two do not touch"):
            left.join(right, using=tenons(count=1, width=50))
        # an error core raises about the other board keeps its path in the message
        with pytest.raises(LangError, match=r"^unit\.shelf: tenons with unit\.left: unit\.left: the cut "
                                            r"mortise_shelf_1 splits the board in pieces"):
            shelf.join(left, using=tenons(width=300, at=[Pos("x", 150)]))
        # on the board whose join() was called, naming the other
        with pytest.raises(LangError, match=r"^unit\.left: tenons with unit\.shelf: remaining=15 leaves no tenon in "
                                            r"unit\.left \(15 thick\)\.$"):
            left.join(shelf, using=tenons(count=1, width=50, remaining=15))
    assert state(left, right, shelf) == [(box(0, 0, 300, 800).wkt, []), (box(0, 0, 300, 800).wkt, []),
                                         (box(0, 15, 300, 585).wkt, [])]
    for message, make in (("margin= spaces two tenons or more .* with at= it has nothing to do",
                           lambda: tenons(width=50, at=[Pos("x", 50)], margin=10)),
                          ("with count=1, which centres the one, it has nothing to do",
                           lambda: tenons(count=1, width=50, margin=10)),
                          ("at= takes a list of positions", lambda: tenons(width=50, at=Pos("x", 50))),  # type: ignore
                          ("give width=, or even=True", lambda: tenons(count=2)),
                          ("works the width out", lambda: tenons(count=2, width=50, even=True)),
                          ("two tenons or more", lambda: tenons(count=1, even=True)),
                          ("need a width", lambda: tenons(at=[Pos("x", 1)])),
                          ("give count= or at=", lambda: tenons(width=50))):
        with pytest.raises(LangError, match=message):
            make()
