"""Lipping and edge banding (`Board.lip`): the board cut back along a narrow
face and a slat of solid wood in its place, as wide as the board is thick;
butted corners, the edges a face has, and what may come before and after."""
from collections.abc import Callable

import pytest
from shapely.geometry import box as shapely_box

from lang import *
from lang.core.directions import AXES
from lang.core.layout import build_layout
from lang.core.ops import Cut, Hole
from helpers import ply15, part_meshes

#: The module's box: x (depth) 0 to 400 from the front, y (width) 0 to 600 from the left, z 0 to 700.
BOX = Box.from_size(width=600, depth=400, height=700)
oak = slat_material("oak")


def _extents(part: Board) -> dict[str, tuple[float, float]]:
    b = part.box()
    return {a: (round(b.lo[a], 6), round(b.hi[a], 6)) for a in AXES}


def _shelf() -> tuple[Scope, Board]:
    """A shelf lying on the module's bottom, 15 thick: x 0 to 400 (its
    front at 0), y 0 to 600."""
    with module("m", BOX) as m:
        shelf = board("shelf", ply15).on(m.bottom)
    return m, shelf


def _parts(m: Scope) -> list[str]:
    return sorted(m.parts)


# -- what a lip makes ------------------------------------------------------------------------------

def test_a_lip_cuts_the_board_back_and_puts_a_strip_in_its_place():
    m, shelf = _shelf()
    with m:
        shelf.lip(shelf.front, 10, oak)
    strip = m.shelf_lip_front
    assert isinstance(strip, Slat) and strip.material is oak
    assert _extents(shelf) == {"x": (0, 400), "y": (0, 600), "z": (0, 15)}          # the box stays
    assert shelf.outline.geometry.equals(shapely_box(10, 0, 400, 600))
    assert _extents(strip) == {"x": (0, 10), "y": (0, 600), "z": (0, 15)}
    assert strip.section == (10, 15) and strip.t_axis == "x"
    assert isinstance(shelf.lip_front.op, Cut)                                       # the cut, named
    assert shelf.front.value == 0                                                    # still the finished face


def test_banding_is_a_thin_lip():
    m, shelf = _shelf()
    with m:
        shelf.lip(shelf.front, 0.5, oak)
    assert _extents(m.shelf_lip_front) == {"x": (0, 0.5), "y": (0, 600), "z": (0, 15)}
    assert shelf.outline.area == pytest.approx(399.5 * 600)


def test_a_lip_deeper_than_the_board_is_thick_lies_the_other_way():
    m, shelf = _shelf()
    with m:
        shelf.lip(shelf.front, 25, oak)
    strip = m.shelf_lip_front
    assert _extents(strip) == {"x": (0, 25), "y": (0, 600), "z": (0, 15)}
    assert strip.section == (15, 25) and strip.t_axis == "z"


def test_the_face_named_first_runs_through_a_butted_corner():
    """At each corner the strip lipped first runs through: the front past
    both, the left past the back, the back past the right."""
    m, shelf = _shelf()
    with m:
        shelf.lip([shelf.front, shelf.left, shelf.back, shelf.right], 10, oak)
    assert _extents(m.shelf_lip_front) == {"x": (0, 10), "y": (0, 600), "z": (0, 15)}
    assert _extents(m.shelf_lip_left) == {"x": (10, 400), "y": (0, 10), "z": (0, 15)}
    assert _extents(m.shelf_lip_back) == {"x": (390, 400), "y": (10, 600), "z": (0, 15)}
    assert _extents(m.shelf_lip_right) == {"x": (10, 390), "y": (590, 600), "z": (0, 15)}
    assert shelf.outline.geometry.equals(shapely_box(10, 10, 390, 590))
    with m:
        check(no_interference)
    assert m.run_checks() == []


def test_an_earlier_lip_runs_through_a_later_one():
    m, shelf = _shelf()
    with m:
        shelf.lip(shelf.left, 10, oak)
        shelf.lip(shelf.front, 5, oak)
    assert _extents(m.shelf_lip_left) == {"x": (0, 400), "y": (0, 10), "z": (0, 15)}
    assert _extents(m.shelf_lip_front) == {"x": (0, 5), "y": (10, 600), "z": (0, 15)}


def test_the_board_and_its_strips_are_the_board_as_it_was():
    m, shelf = _shelf()
    with m:
        shelf.lip([shelf.front, shelf.right], 12, oak)
    meshes = part_meshes()
    total = sum(meshes[p].volume for p in ("m.shelf", "m.shelf_lip_front", "m.shelf_lip_right"))
    assert total == pytest.approx(400 * 600 * 15)


def test_a_strip_goes_along_each_straight_edge_in_the_face():
    """A side with a toe kick: only the front edge above it. A notch in the
    middle of the edge: a strip on either side of it."""
    with module("m", BOX) as m:
        side = board("side", ply15).on(m.left)
        side.cut(rect(depth=60, height=100), at=side.outer.bottom.front, name="toekick")
        side.lip(side.front, 10, oak)
        shelf = board("shelf", ply15).on(m.bottom).between(side, m.right)
        shelf.cut(rect(depth=30, width=100), at=shelf.top.front(0).left(300), name="notch")
        shelf.lip(shelf.front, 10, oak)
    assert _extents(m.side_lip_front) == {"x": (0, 10), "y": (0, 15), "z": (100, 700)}
    # the notch: 100 wide from 300 past the shelf's left face (y 15)
    assert _extents(m.shelf_lip_front_1)["y"] == (15, 315) and _extents(m.shelf_lip_front_2)["y"] == (415, 600)
    assert "shelf_lip_front" not in m.parts


def test_strips_go_into_the_boards_scope_wherever_lip_is_called():
    with module("m", BOX) as m:
        shelf = board("shelf", ply15).on(m.bottom)
    shelf.lip(shelf.front, 10, oak)                      # outside the with block
    assert "shelf_lip_front" in m.parts and m.shelf_lip_front.path == "m.shelf_lip_front"


def test_strips_are_named_in_a_cabinets_own_terms():
    box = Box.from_size(width=600, depth=400, height=700)
    with cabinet("cab", box, front=box.right) as cab:
        door = board("door", ply15).on(cab.front)
        door.lip([door.left, door.top], 8, oak)
    assert {"door_lip_left", "door_lip_top"} <= set(cab.parts)
    lb = cab.door_lip_left.box()
    left = door.left                                     # the cabinet's left, wherever the world has it
    assert (lb.lo[left.axis] if left.direction.sign < 0 else lb.hi[left.axis]) == pytest.approx(left.value)


def test_the_layout_has_the_strips_as_slats():
    m, shelf = _shelf()
    with m:
        shelf.lip(shelf.front, 10, oak)
    parts = {p["path"]: p for p in build_layout()["modules"][0]["parts"]}
    strip = parts["m.shelf_lip_front"]
    assert (strip["kind"], strip["section"], strip["material"], strip["grain"]) == ("slat", [10.0, 15.0], "oak", "y")
    assert [op["kind"] for op in parts["m.shelf"]["ops"]] == ["cut"]


# -- refusals when lipping ---------------------------------------------------------------------------

_BAD: list[tuple[Callable[[Board], object], str]] = [
    (lambda s: s.lip(s.top, 10, oak), "big face"),
    (lambda s: s.lip([s.front, s.front], 10, oak), "named twice"),
    (lambda s: s.lip(s.front, 10, ply15), "solid wood"),  # type: ignore[arg-type]
    (lambda s: s.lip(s.front, 0.001, oak), "at least"),
    (lambda s: s.lip(s.front, 400, oak), "takes all of the board"),
    (lambda s: s.lip([], 10, oak), "name the faces"),
]


@pytest.mark.parametrize("call, message", _BAD)
def test_bad_lips_are_errors(call: Callable[[Board], object], message: str) -> None:
    m, shelf = _shelf()
    with m:
        with pytest.raises(LangError, match=message):
            call(shelf)
    assert shelf.ops == [] and _parts(m) == ["shelf"]


def test_a_face_is_lipped_once():
    m, shelf = _shelf()
    with m:
        shelf.lip(shelf.front, 10, oak)
        with pytest.raises(LangError, match="lipped already"):
            shelf.lip(shelf.front, 5, oak)


def test_a_refused_lip_changes_nothing():
    """The second face fails (a hole by its edge), so the first is not
    lipped either and its strip is gone again."""
    m, shelf = _shelf()
    with m:
        shelf.hole(5, shelf.top.right(4).front(200), depth=5)
        before = (shelf.outline.geometry.wkt, list(shelf.ops))
        with pytest.raises(LangError, match="lies where the lip on the right face goes"):
            shelf.lip([shelf.front, shelf.right], 10, oak)
    assert (shelf.outline.geometry.wkt, shelf.ops) == before and _parts(m) == ["shelf"]
    with m:
        shelf.lip(shelf.front, 10, oak)                  # and it can be lipped afterwards
    assert _parts(m) == ["shelf", "shelf_lip_front"]


def test_what_was_made_before_where_the_strip_goes_is_an_error():
    m, shelf = _shelf()
    with m:
        shelf.pocket(rect(depth=20, width=20), at=shelf.top.front(5).left(100), depth=5)
        with pytest.raises(LangError, match="lies where the lip on the front face goes"):
            shelf.lip(shelf.front, 10, oak)
        shelf.hole(5, shelf.left.center, depth=10)              # into the left edge
        with pytest.raises(LangError, match="lies where the lip on the left face goes"):
            shelf.lip(shelf.left, 10, oak)
        shelf.cut(circle(6), at=shelf.top.back(5).left(300))   # an opening by the back edge
        with pytest.raises(LangError, match="a cut or opening made before"):
            shelf.lip(shelf.back, 10, oak)


def test_chamfers_where_the_lip_goes_are_errors():
    m, shelf = _shelf()
    with m:
        shelf.chamfer(shelf.front.top, 1)
        with pytest.raises(LangError, match="an edge of the front face is chamfered"):
            shelf.lip(shelf.front, 10, oak)
        shelf.chamfer(shelf.top.outline, 1)
        with pytest.raises(LangError, match="the outline is chamfered"):
            shelf.lip(shelf.back, 10, oak)


def test_a_lip_goes_on_a_straight_edge_between_corners():
    m, shelf = _shelf()
    with m:
        shelf.fillet(shelf.front.left, 30)
        with pytest.raises(LangError, match="runs into a curve"):
            shelf.lip(shelf.front, 10, oak)
        shelf.lip(shelf.back, 10, oak)                          # the back's corners are square


def test_a_face_a_joint_reaches_past_is_not_lipped():
    with module("m", BOX) as m:
        side = board("side", ply15).on(m.left)
        shelf = board("shelf", ply15).on(Pos("z", 300), toward=m.top).between(side, m.right)
        shelf.join(side, using=tenons(count=2, even=True))
        with pytest.raises(LangError, match="past the left face"):
            shelf.lip(shelf.left, 5, oak)


def test_no_straight_edge_left_is_an_error():
    m, shelf = _shelf()
    with m:
        shelf.cut(rect(depth=400, width=50), at=shelf.top.front.left)    # the left edge cut away
        with pytest.raises(LangError, match="no straight edge left"):
            shelf.lip(shelf.left, 10, oak)


# -- nothing reaches the strip after -------------------------------------------------------------------

def test_nothing_reaches_the_strip_after():
    m, shelf = _shelf()
    with m:
        shelf.lip(shelf.front, 10, oak)
        before = (shelf.outline.geometry.wkt, list(shelf.ops))
        attempts = [
            (lambda: shelf.cut(rect(depth=40, width=40), at=shelf.top.front.left), "the cut"),
            (lambda: shelf.hole(35, shelf.top.front(12).left(100), depth=12), "a hole"),
            (lambda: shelf.pocket(rect(depth=20, width=20), at=shelf.top.front(5).left(200), depth=5), "a pocket"),
            (lambda: shelf.hole(5, shelf.front.center, depth=10), "a hole"),
            (lambda: shelf.chamfer(shelf.front.top, 1), "the lip's"),
            (lambda: shelf.chamfer(shelf.top.outline, 1), "glue lines"),
            (lambda: shelf.chamfer(shelf.lip_front, 1), "where a lip is glued on"),
            (lambda: shelf.fillet(shelf.top.outline, 5), "fillet"),
        ]
        for attempt, what in attempts:
            with pytest.raises(LangError) as error:
                attempt()
            assert what in str(error.value) and ("lip" in str(error.value) or "corner" in str(error.value))
    assert (shelf.outline.geometry.wkt, shelf.ops) == before


def test_operations_clear_of_the_strip_are_fine():
    m, shelf = _shelf()
    with m:
        shelf.lip(shelf.front, 10, oak)
        shelf.hole(5, shelf.top.front(20).left(100), depth=5)
        shelf.cut(rect(depth=50, width=50), at=shelf.top.back.left, name="notch")
        shelf.chamfer(shelf.back.top, 1)
        shelf.fillet(shelf.back.right, 10)                     # changes the outline, adds no operation
    assert [op.kind for op in shelf.ops] == ["cut", "hole", "cut", "chamfer"]


def test_a_lipped_board_still_joins_on_its_big_faces():
    """A side lipped at its front takes a shelf on its inner face; the
    connectors keep to the side's material, behind the lip."""
    with module("m", BOX) as m:
        side = board("side", ply15).on(m.left)
        side.lip(side.front, 10, oak)
        shelf = board("shelf", ply15).on(Pos("z", 300), toward=m.top).between(side, m.right)
        shelf.join(side, using=cabineo(count=2))
        check(no_interference)
    assert m.run_checks() == []
    assert all(op.u >= 10 for op in side.ops if isinstance(op, Hole))        # the side's holes behind the lip


def test_a_slat_is_not_lipped():
    with module("m", BOX) as m:
        s = slat("s", oak, section=(20, 40)).on(m.bottom).edge_on(m.left)
        with pytest.raises(LangError, match="takes no operations"):
            s.lip(s.front, 2, oak)


def test_a_lip_too_thin_to_cut_back_is_refused():
    """[Found by fuzzing, 2026-10-14] A lip 0.01 thick: its cut-back is as
    narrow as cleaning removes, so the board stayed as it was beside its
    strip."""
    m, shelf = _shelf()
    with m:
        with pytest.raises(LangError, match="too thin to cut"):
            shelf.lip(shelf.front, 0.01, oak)
    assert shelf.ops == [] and _parts(m) == ["shelf"]


def test_an_edge_meeting_another_at_a_shallow_angle_is_lipped():
    """A straight edge turning by a few degrees at the end of the face's
    edge is a corner, not a curve."""
    with module("m", BOX) as m:
        # the front edge from y 0 to 500, then on 11.3 degrees off its line
        shelf = board("shelf", ply15, polygon([(0, 0), (400, 0), (400, 600), (20, 600), (0, 500)])).on(m.bottom)
        shelf.lip(shelf.front, 10, oak)
    assert _extents(m.shelf_lip_front)["y"] == (0, 500)
