"""Contacts between boards that meet edge-on, and the connectors joining them."""
from typing import get_args

import pytest

from lang import *
from lang.core.contact import contacts
from lang.core.layout import build_layout
from lang.core.ops import Hole, Pocket, VGroove
from lang.preview.mesh import mesh_part
from lang.joints.common import ContactJoint
from lang.joints.connectors import CabineoInsert, CabineoModel, ClamexModel, DominoSize
from lib import connector_data
from helpers import carcass, ply9, ply15, state



def _ops(part: Board, prefix: str) -> list[Pocket | Hole]:
    return [op for op in part.ops if isinstance(op, (Pocket, Hole)) and (op.name or "").startswith(prefix)]


def _pockets(part: Board, prefix: str) -> list[Pocket]:
    return [op for op in _ops(part, prefix) if isinstance(op, Pocket)]


def _holes(part: Board, prefix: str) -> list[Hole]:
    return [op for op in _ops(part, prefix) if isinstance(op, Hole)]


# -- contacts ---------------------------------------------------------------------------------

def test_a_board_between_two_others_meets_both_edge_on():
    _, p = carcass()
    (c,) = contacts(p["bottom"], p["left"])
    assert (c.axis, c.lo, c.hi, c.across, c.across_lo, c.across_hi) == ("x", 0, 500, "z", 0, 15)
    assert c.face.name == "right" and c.end.name == "left" and c.plane == 15
    assert contacts(p["left"], p["bottom"]) == []           # the side meets the bottom with its face
    assert contacts(p["left"], p["right"]) == []            # parallel
    # the back stands on the bottom and meets all four around it
    (b,) = contacts(p["back"], p["bottom"])
    assert (b.axis, b.lo, b.hi, b.across_lo, b.across_hi) == ("y", 15, 585, 491, 500)
    assert all(contacts(p["back"], p[n]) for n in ("left", "right", "top"))


def test_a_contact_covers_only_where_both_boards_have_material():
    _, p = carcass(toekick=True)
    (c,) = contacts(p["bottom"], p["left"])                  # the toe kick notch takes the front 60
    assert (c.lo, c.hi) == (60, 500)


def test_a_notched_end_meets_in_two_places():
    cab, p = carcass()
    with cab:
        divider = board("divider", ply15).center(Pos("y", 300)).between(p["bottom"], p["top"])
        divider.cut(rect(depth=100, height=50), at=divider.left.bottom)
    found = contacts(divider, p["bottom"])
    assert [(c.lo, c.hi) for c in found] == [(0, 200), (300, 500)]


def _divider() -> tuple[Scope, dict[str, Board]]:
    """The carcass with a divider between the bottom and the top, its lower
    end notched 100 deep in the middle: it meets the bottom twice, x 0..200
    and 300..500."""
    cab, p = carcass()
    with cab:
        divider = board("divider", ply15).center(Pos("y", 300)).between(p["bottom"], p["top"])
        divider.cut(rect(depth=100, height=50), at=divider.left.bottom)
    return cab, {**p, "divider": divider}


def _names(part: Board) -> list[str]:
    return [name for op in part.ops if (name := getattr(op, "name", None))]


def test_stations_are_numbered_across_the_contacts_of_a_pair():
    cab, p = _divider()
    with cab:
        p["divider"].join(p["bottom"], using=domino("4x20", count=2))
        p["divider"].join(p["top"], using=cabineo(count=2))
    # two per contact, numbered on from the first contact to the second
    assert _names(p["bottom"]) == [f"domino_divider_{i}" for i in (1, 2, 3, 4)]
    assert [round((op.shape.bounds[0] + op.shape.bounds[2]) / 2, 6) for op in _pockets(p["bottom"], "domino")] == [
        37, 163, 337, 463]
    assert _names(p["divider"])[:4] == [f"domino_bottom_{i}_mark" for i in (1, 2, 3, 4)]
    # the top meets the whole end: one contact, numbered as before
    assert _names(p["top"]) == ["cabineo_divider_1", "cabineo_divider_2"]
    assert _names(p["divider"])[4:] == [f"cabineo_top_{i}{x}" for i in (1, 2) for x in "abc"]


def test_screws_and_cabineos_are_numbered_across_the_contacts_too():
    cab, p = _divider()
    with cab:
        p["divider"].join(p["bottom"], using=cabineo(count=1))
        p["bottom"].join(p["divider"], using=screws(count=1))
    assert _names(p["divider"]) == ["cabineo_bottom_1a", "cabineo_bottom_1b", "cabineo_bottom_1c",
                                    "cabineo_bottom_2a", "cabineo_bottom_2b", "cabineo_bottom_2c"]
    assert _names(p["bottom"]) == ["cabineo_divider_1", "cabineo_divider_2", "screw_divider_1", "screw_divider_2"]


def test_a_pair_joined_twice_with_the_same_kind_of_joint_is_an_error():
    cab, p = _divider()
    bottom, divider = p["bottom"], p["divider"]
    with cab:
        divider.join(bottom, using=domino("4x20", count=2))
        before = state(bottom, divider)
        with pytest.raises(LangError, match=r"^cab\.bottom: domino with cab\.divider: cab\.bottom and cab\.divider are "
                                            r"joined with domino already \(cab\.bottom has domino_divider_1\); join a "
                                            r"pair once with each kind of joint\.$"):
            bottom.join(divider, using=domino("5x30", count=1, remaining=5))
        assert state(bottom, divider) == before
        bottom.join(divider, using=screws(count=1))              # another kind of joint: fine


def test_boards_of_the_same_name_in_other_scopes_are_no_second_join():
    """Two sides named left, in two modules: the shelf between them names
    its marks for the second one with a suffix, as before."""
    with module("unit", Box.from_size(width=600, depth=300, height=800)) as u:
        with module("a", Box.from_size(width=300, depth=300, height=800)) as a:
            first = board("left", ply15).on(a.left)
        with module("b", Box.from_size(width=300, depth=300, height=800, origin=(0, 300, 0))) as b:
            second = board("left", ply15).on(b.right)
        shelf = board("shelf", ply15).on(Pos("z", 400), toward=u.top).between(first, second)
        shelf.join(first, second, using=domino("4x20", count=2))
    assert _names(shelf) == ["domino_left_1_mark", "domino_left_2_mark", "domino_left_1_mark_2", "domino_left_2_mark_2"]
    assert _names(first) == _names(second) == ["domino_shelf_1", "domino_shelf_2"]


# -- Domino -------------------------------------------------------------------------------------

def test_dominos_are_slots_in_the_face_and_marks_on_the_edge_on_board():
    cab, p = carcass()
    with cab:
        p["bottom"].join(p["left"], p["right"], using=domino("4x20", count=3))
    slots = _pockets(p["left"], "domino_bottom_")
    assert [s.name for s in slots] == ["domino_bottom_1", "domino_bottom_2", "domino_bottom_3"]
    first = slots[0]
    assert first.face == "right" and first.depth == 10.5
    x0, z0, x1, z1 = first.shape.bounds                     # the side's frame is (x, z)
    assert (round(x0, 3), round(x1, 3)) == (37 - 8.3, 37 + 8.3)   # 16.6 long, 37 from the front
    assert (round(z0, 3), round(z1, 3)) == (5.5, 9.5)            # 4 high, centred on the bottom
    assert [round((s.shape.bounds[0] + s.shape.bounds[2]) / 2, 6) for s in slots] == [37, 250, 463]
    assert len(_ops(p["right"], "domino_bottom_")) == 3
    # nothing but marks on the bottom: its mortises are cut with the machine
    marks = [op for op in p["bottom"].ops if isinstance(op, VGroove)]
    assert len(marks) == len(p["bottom"].ops) == 6
    mark = marks[0]                                         # the bottom's frame is (x, y)
    assert mark.name == "domino_left_1_mark" and mark.face == "bottom"     # its show face
    assert (mark.u0, mark.v0, mark.u1, mark.v1, mark.depth) == (37, 15 - 1, 37, 15 + 4, 0.3)
    assert build_layout()["problems"] == []


def test_domino_marks_can_skip_the_outer_ones_or_be_left_out():
    cab, p = carcass()
    with cab:
        p["bottom"].join(p["left"], using=domino("4x20", count=3, marks="middle", face=cab.top))
        p["top"].join(p["left"], using=domino("4x20", count=3, marks=None))
    marks = [op for op in p["bottom"].ops if isinstance(op, VGroove)]
    assert [(m.name, m.face) for m in marks] == [("domino_left_2_mark", "top")]
    assert p["top"].ops == []
    layout = next(op for part in build_layout()["modules"][0]["parts"] if part["path"] == "cab.bottom"
                  for op in part["ops"])
    assert layout == {"kind": "vgroove", "name": "domino_left_2_mark", "face": "top", "start": [250, 14],
                      "end": [250, 19], "depth": 0.3}


def test_domino_depth_fence_and_loose_slots():
    cab, p = carcass()
    with cab:
        with pytest.raises(LangError, match="5x30 needs a 15.5 mm deep slot.*remaining="):
            p["bottom"].join(p["left"], using=domino("5x30", count=2))
        p["bottom"].join(p["left"], using=domino("5x30", count=2, end=20, remaining=3, fence=5,
                                                face=cab.bottom, loose=6))
    a, b = _pockets(p["left"], "domino_bottom_")
    assert a.depth == 12 and a.depth_spec == "to(left, -3)"
    assert (round(a.shape.bounds[1], 6), round(a.shape.bounds[3], 6)) == (2.5, 7.5)   # 5 above the underside
    assert round(a.shape.width, 6) == 18.8 and round(b.shape.width, 6) == 24.8         # the first one is exact
    assert round(a.shape.bounds[0], 6) == 20 - 9.4
    assert _ops(p["right"], "domino") == []


def test_dominos_around_a_back_panel():
    cab, p = carcass()
    with cab:
        p["back"].join(p["left"], p["right"], p["bottom"], p["top"], using=domino("4x20", count=2))
    for name in ("left", "right", "bottom", "top"):
        assert len(_ops(p[name], "domino_back_")) == 2
    (slot, _) = _ops(p["bottom"], "domino_back_")
    assert isinstance(slot, Pocket) and slot.face == "top"
    assert round(slot.shape.bounds[0] + slot.shape.bounds[2], 6) == 2 * 495.5   # centred on the back (x)


def test_domino_sizes_match_the_data():
    assert list(get_args(DominoSize)) == [s.key for s in connector_data.DOMINO_SIZES]


def test_clamex_and_cabineo_models_match_the_data():
    """The names a build file may give are the data's keys: a model added
    to lib/connector_data.py must be added to the type too."""
    assert set(get_args(ClamexModel)) == set(connector_data.CLAMEX_MODELS)
    # every model, and the 8 M6 with every insert, reaches one of the screw
    # holes in the data, and together they reach all of them
    reached = {cabineo(m, count=2).guide for m in get_args(CabineoModel) if m != "8 M6"}
    reached |= {cabineo("8 M6", count=2, insert=i).guide for i in get_args(CabineoInsert)}
    assert reached == set(connector_data.CABINEO_GUIDE_HOLES.values())


# -- Cabineo ------------------------------------------------------------------------------------

def test_cabineo_pockets_the_edge_on_board_and_drills_the_other():
    cab, p = carcass()
    with cab:
        p["bottom"].join(p["left"], using=cabineo(count=2, face=cab.bottom))
    access = _ops(p["bottom"], "cabineo_left_")
    assert [op.name for op in access] == ["cabineo_left_1a", "cabineo_left_1b", "cabineo_left_1c",
                                          "cabineo_left_2a", "cabineo_left_2b", "cabineo_left_2c"]
    assert all(isinstance(op, Hole) and op.face == "bottom" and op.d == 15 and op.depth == 10.5 for op in access)
    # bottom's frame is (x, y); the holes run in from the left side's face at y = 15
    assert [(op.u, round(op.v, 6)) for op in access if isinstance(op, Hole)][:3] == [
        (60, 18.6), (60, 29.8), (60, 41)]
    (screw_1, screw_2) = _holes(p["left"], "cabineo_bottom_")
    assert screw_1.face == "right" and (screw_1.d, screw_1.depth) == (5, 8)
    assert (screw_1.u, screw_1.v, screw_2.u) == (60, 5, 440)    # 5 above the access face (the underside)
    assert p["bottom"].machine_face.name == "bottom"


def test_a_connector_join_reads_the_same_from_either_board():
    cab, p = carcass()
    with cab:
        p["left"].join(p["bottom"], p["top"], using=cabineo(count=2))
    assert len(_holes(p["bottom"], "cabineo_left_")) == 6 and len(_holes(p["top"], "cabineo_left_")) == 6
    assert len(_holes(p["left"], "cabineo_bottom_")) == 2 and len(_holes(p["left"], "cabineo_top_")) == 2
    assert _ops(p["right"], "cabineo") == []                # only the boards named


def test_cabineo_defaults_to_the_hidden_face_and_its_variants():
    cab, p = carcass()
    with cab:
        p["top"].show(cab.top)
        p["top"].join(p["right"], using=cabineo("8 M6", count=1, surface="flush"))
        with pytest.raises(LangError, match="insert= is for the Cabineo 8 M6"):
            cabineo("12", count=1, insert="M6 x 12.3")
    holes = _ops(p["top"], "cabineo_right_1")
    assert {op.face for op in holes} == {"bottom"}          # the top shows its top face
    relief = next(op for op in holes if op.name == "cabineo_right_1_relief")
    assert isinstance(relief, Pocket) and relief.depth == 0.8
    assert all(op.depth == 11 for op in holes if isinstance(op, Hole))
    screw, collar = _ops(p["right"], "cabineo_top_1")
    assert isinstance(screw, Hole) and (screw.d, screw.depth) == (7.9, 13.5)
    assert screw.v == 705 + 5.8                             # 5.8 above the top's underside
    assert isinstance(collar, Pocket) and collar.depth == 0.8 and round(collar.shape.width, 1) == 12.7


def test_cabineo_needs_a_board_thicker_than_its_pocket():
    cab, p = carcass()
    with cab:
        with pytest.raises(LangError, match=r"10\.5 mm deep pocket goes through cab\.back \(9 thick\)"):
            p["back"].join(p["left"], using=cabineo(count=2))


# -- Clamex ---------------------------------------------------------------------------------------

def test_clamex_p10_slot_and_guide_holes():
    cab, p = carcass()
    with cab:
        p["bottom"].join(p["right"], using=clamex(count=1))
    (slot,) = _ops(p["bottom"], "clamex_right_1")
    assert isinstance(slot, Pocket) and slot.face == "top" and slot.depth == 7.5
    x0, y0, x1, y1 = slot.shape.bounds
    assert (round(x0, 6), round(x1, 6)) == (247, 253)                   # 6 wide at the centre
    assert (round(y0, 6), round(y1, 6)) == (585 - 10.5, 585 - 2)        # from 2 to 10.5 in from the right
    a, b = _ops(p["right"], "clamex_bottom_1")
    assert isinstance(a, Hole) and isinstance(b, Hole)
    assert (a.u, b.u, a.v, a.d, a.depth) == (250 - 50.5, 250 + 50.5, 7.5, 7.7, 8)


def test_clamex_p14_is_a_hole():
    cab, p = carcass()
    with cab:
        p["top"].join(p["left"], using=clamex("P-14", at=[Pos("x", 100)], through=True))
    (access,) = _ops(p["top"], "clamex_left_1")
    assert isinstance(access, Hole) and (access.u, access.v, access.d) == (100, 15 + 7.5, 6)
    guide = _ops(p["left"], "clamex_top_1")
    assert all(isinstance(g, Hole) and g.through for g in guide)


# -- spacing and errors -----------------------------------------------------------------------------

def test_spacing_and_join_errors():
    cab, p = carcass()
    left, right, bottom = p["left"], p["right"], p["bottom"]
    before = state(*p.values())
    with cab:
        with pytest.raises(LangError, match=r"^cab\.left: domino with cab\.right: the two do not touch"):
            left.join(right, using=domino("4x20", count=2))
        with pytest.raises(LangError, match="cabineo with cab.right: the two do not touch"):   # bottom is fine
            left.join(bottom, right, using=cabineo(count=2))
        with pytest.raises(LangError, match="not on the axis the contact"):
            bottom.join(left, using=cabineo(at=[Pos("y", 100)]))
        with pytest.raises(LangError, match="outside the contact"):
            bottom.join(left, using=cabineo(at=[Pos("x", 600)]))
        with pytest.raises(LangError, match="end=260 leaves no room"):
            bottom.join(left, using=cabineo(count=2, end=260))
        with pytest.raises(LangError, match=r"at x=5, the slot would reach past the contact \(x 0 to 500\)"):
            bottom.join(left, using=domino("4x20", count=2, end=5))
        with pytest.raises(LangError, match="face=front is not a big face"):
            bottom.join(left, using=cabineo(count=2, face=cab.front))
        with pytest.raises(LangError, match="name the boards"):
            bottom.join(using=cabineo(count=2))
    with pytest.raises(LangError, match="give count= or at="):
        cabineo()
    # a failed join leaves every board untouched
    assert state(*p.values()) == before


def test_errors_are_reported_on_the_board_whose_join_was_called():
    """One rule for every joint: the error's path is the receiver, its
    message names the joint and the other board, whichever of the two
    meets the other edge-on."""
    cab, p = carcass()
    with cab:
        with pytest.raises(LangError) as from_back:
            p["back"].join(p["left"], using=cabineo(count=2))
        with pytest.raises(LangError) as from_side:
            p["left"].join(p["back"], using=cabineo(count=2))
    assert (from_back.value.path, from_side.value.path) == ("cab.back", "cab.left")
    message = "the 10.5 mm deep pocket goes through cab.back (9 thick)."
    assert str(from_back.value) == f"cab.back: cabineo with cab.left: {message}"
    assert str(from_side.value) == f"cab.left: cabineo with cab.back: {message}"


@pytest.mark.parametrize("joint, message", [
    # the guide holes 50.5 either side, 7.7 wide
    (clamex(at=[Pos("x", 10)]), "at x=10, the guide holes would reach past the contact"),
    (clamex(count=2, end=54), "at x=54, the guide holes"),
    # the 15 mm access holes, 0.6 wider with an anti-break relief, 16.7 flush
    (cabineo(at=[Pos("x", 7)]), "at x=7, the Cabineo would reach past the contact"),
    (cabineo(at=[Pos("x", 7.8)], surface="anti-break"), "at x=7.8, the Cabineo"),
    (cabineo(at=[Pos("x", 8)], surface="flush"), "at x=8, the Cabineo"),
    # the last of two Dominos, 6 longer than the first, which is exact
    (domino("4x20", count=2, end=10, loose=6), "at x=490, the slot would reach past the contact"),
    (screws(at=[Pos("x", 1)]), "at x=1, the screw would reach past the contact"),
])
def test_connectors_must_stay_within_the_contact(joint: ContactJoint, message: str):
    cab, p = carcass()
    before = state(p["bottom"], p["left"])
    with cab, pytest.raises(LangError, match=f"^cab.bottom: {joint.label} with cab.left: {message}"):
        p["bottom"].join(p["left"], using=joint)
    assert state(p["bottom"], p["left"]) == before


def test_connectors_near_the_contacts_ends_that_fit():
    cab, p = carcass()
    with cab:
        p["bottom"].join(p["left"], using=clamex(at=[Pos("x", 54.35)]))
        p["bottom"].join(p["right"], using=cabineo(at=[Pos("x", 8.1)], surface="anti-break"))
        p["top"].join(p["left"], using=domino("4x20", count=2, end=10, loose=3.4))     # 20 long: to the end
        p["top"].join(p["right"], using=screws(at=[Pos("x", 2)]))
    assert [h.u for h in _holes(p["left"], "clamex_bottom_1")] == pytest.approx([3.85, 104.85])   # 3.85 from the end
    slot = _pockets(p["left"], "domino_top_2")[0]
    assert slot.shape.bounds[2] == pytest.approx(500)


def test_a_connector_must_lie_where_the_face_on_board_covers_the_end():
    """The back (x 491..500) stands on a bottom that ends at x 495: the
    contact covers only 4 of the back's 9 mm. The connectors stay where the
    back's thickness puts them, so a Domino centred on it would reach past
    the bottom's edge, and so would screws; one fenced into the part the
    bottom covers fits."""
    with module("cab", Box.from_size(width=600, depth=500, height=720)) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        bottom = board("bottom", ply15).on(cab.bottom).between(left, right, cab.front, Pos("x", 495))
        back = board("back", ply9).on(cab.back).between(left, right, cab.bottom + 15, cab.top)
        (c,) = contacts(back, bottom)
        assert (c.across_lo, c.across_hi, back.show_face.value) == (491, 495, 500)
        before = state(back, bottom)
        with pytest.raises(LangError, match=r"^cab\.back: domino with cab\.bottom: the slot \(x 493\.5 to 497\.5\) "
                                            r"would reach past cab\.bottom, which covers the end of cab\.back only "
                                            r"from x=491 to 495\.$"):
            back.join(bottom, using=domino("4x20", count=2))
        with pytest.raises(LangError, match=r"^cab\.bottom: screws with cab\.back: the screw \(x 493\.5 to 497\.5\)"):
            bottom.join(back, using=screws(count=2))
        assert state(back, bottom) == before
        back.join(bottom, using=domino("4x20", count=2, fence=7))     # 7 in from the back's outer face
    (slot, _) = _pockets(bottom, "domino_back_")
    assert (round(slot.shape.bounds[0], 6), round(slot.shape.bounds[2], 6)) == (491, 495)


def test_the_preview_cuts_the_marks():
    cab, p = carcass()
    with cab:
        p["bottom"].join(p["left"], using=domino("4x20", count=3))
    layout = build_layout()
    part = next(part for part in layout["modules"][0]["parts"] if part["path"] == "cab.bottom")
    mesh = mesh_part(part, layout["frame"])
    groove = 0.3 * 0.3 * 4                                  # a 90 degree V: depth squared, 4 long in the board
    assert mesh.volume == pytest.approx(570 * 500 * 15 - 3 * groove, abs=1e-3)
