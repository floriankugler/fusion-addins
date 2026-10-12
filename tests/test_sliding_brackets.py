"""Sliding brackets (lang/hardware/sliding_brackets.py): positions worked
out by hand from the Pacofix data (lib/sliding_brackets.py) for the bent
frame part PF-L-R (the default) and the straight PF-L, the gap read from
the model, both hole options, and what is refused. Most tests use the
PF-L, whose gap and System 32 line need the most checking; the PF-L-R
has its own section.

The test box is 400 deep (x 0..400, the front at -x), 600 wide (y
0..600) and 500 high, in the van's terms (no front=, left is -y). Its
sides are the frame boards, 18 thick: the left one at y 0..18, its inner
face at 18 pointing +y (world "right"), the right one at y 582..600. A 12
mm cover lies over the front (x 0..12), its back face at x 12; the sides
begin `gap` behind it."""
from pathlib import Path
from typing import Any, get_args

import pytest

from lang import *
from lang.build import run_build
from lang.core.checks import _box_hits  # type: ignore[reportPrivateUsage]
from lang.core.layout import build_layout
from lang.core.ops import Hole
from lang.core.scope import registry
from lang.emit.plan import HoleStep, plan_layout
from lang.hardware.sliding_brackets import BRACKET_SHAPES, BracketBox, BracketModel, SlidingBracket
from lib import sliding_brackets as data
from helpers import ply12, ply18


BOX = Box.from_size(width=600, depth=400, height=500)
PF_L: BracketModel = "Pacofix PF-L"
SPEC = data.PACOFIX_PF_L
SHAPE = BRACKET_SHAPES[SPEC.name]
BENT = data.PACOFIX_PF_L_R
BENT_SHAPE = BRACKET_SHAPES[BENT.name]


def _cover(bracket: SlidingBracket | None = None, *, gap: float = 0.0, cover: Material = ply12,
           frame: str = "both", front: bool = False) -> tuple[Scope, dict[str, Board]]:
    """The test box with its cover; `frame` names the frame boards the
    cover is mounted on: "left", "right" or "both"."""
    with (module("cab", BOX, front=BOX.front) if front else module("cab", BOX)) as cab:
        behind = cab.front.into(cover.t + gap)
        left = board("left", ply18).on(cab.left).between(behind)
        right = board("right", ply18).on(cab.right).between(behind)
        panel = board("cover", cover).on(cab.front)
        if bracket is not None:
            frames = {"left": [left], "right": [right], "both": [left, right]}[frame]
            cab.mount(bracket, panel=panel, frame=frames)
    return cab, {"left": left, "right": right, "cover": panel}


def _holes(part: Board) -> list[tuple[str, str, float, float, float, float]]:
    return [(op.name or "", op.face, round(op.u, 6), round(op.v, 6), op.d, op.depth)
            for op in part.ops if isinstance(op, Hole)]


def _world(box: BracketBox, out: tuple[int, float, int], back: tuple[int, float, int], along: float) -> dict[str, list[float]]:
    """A bracket box in world coordinates; `out` and `back` as (axis index,
    start, sign), the edge along z."""
    lo, hi = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
    for (axis, start, sign), (a, b) in zip((out, back), box[:2]):
        lo[axis], hi[axis] = sorted((start + sign * a, start + sign * b))
    lo[2], hi[2] = along + box[2][0], along + box[2][1]
    return {"min": lo, "max": hi}


# -- the data ---------------------------------------------------------------------------------------

def test_the_model_names_are_the_libs_and_the_bent_one_is_the_default():
    assert list(get_args(BracketModel)) == list(data.BRACKETS) == list(BRACKET_SHAPES)
    assert SlidingBracket().spec is BENT and SlidingBracket(PF_L).spec is SPEC


@pytest.mark.parametrize("model", list(get_args(BracketModel)))
def test_the_boxes_agree_with_the_drilling_data(model: BracketModel):
    """The plates' boxes cover the footprints the checks use (the PF-L-R's
    plate reaches past its flat underside, rounded), the holes lie on them,
    the panel part's boxes begin at the tongue's side, the hook lies over
    the tongue, and the boxes touch the boards' faces without reaching into
    them."""
    spec, shape = data.BRACKETS[model], BRACKET_SHAPES[model]
    (frame_plate, hook), (panel_plate, tongue) = shape.frame_part, shape.panel_part
    half = spec.plate_length / 2
    assert frame_plate[1][0] == spec.frame_plate_back[0] and frame_plate[1][1] >= spec.frame_plate_back[1]
    assert frame_plate[2] == (-half, half) == panel_plate[2] and frame_plate[0] == (0, 4)
    assert panel_plate[0] == spec.panel_plate_out
    assert frame_plate[1][0] < spec.frame_hole_back < frame_plate[1][1]
    assert panel_plate[0][0] < spec.panel_hole_out < panel_plate[0][1]
    assert spec.hole_pitch / 2 < half
    assert tongue[0][0] == panel_plate[0][0] and tongue[1] == (panel_plate[1][1], data.TONGUE_LENGTH)
    assert hook[0][0] == frame_plate[0][1] and hook[1][1] == frame_plate[1][1]
    assert hook[1][0] < tongue[1][1] and hook[2] == (-8, 8)
    assert min(b[0][0] for b in shape.boxes()) == 0 and min(b[1][0] for b in shape.boxes()) == 0


def test_the_straight_tongue_ends_at_the_plate_and_the_bent_one_lies_on_it():
    """PF-L: the tongue lies on the frame board and reaches the plate,
    which begins 29 behind the panel (37 - 8). PF-L-R: the tongue lies on
    the frame part's plate, 4 off the board, its tip at the end of the
    plate's flat underside (29), the hook's closed end; the plate begins
    at the panel's back face and may hang 3 over the frame board's edge."""
    (plate, _), (_, tongue) = SHAPE.frame_part, SHAPE.panel_part
    assert tongue[0][0] == 0 and tongue[1][1] == SPEC.max_gap == plate[1][0] == SPEC.frame_hole_back - 8
    (plate, hook), (_, tongue) = BENT_SHAPE.frame_part, BENT_SHAPE.panel_part
    assert tongue[0] == (plate[0][1], plate[0][1] + 10) == hook[0]
    assert tongue[1][1] == BENT.frame_plate_back[1] and plate[1][0] == BENT.frame_plate_back[0] == 0
    assert BENT.max_gap == data.MAX_PLATE_OVERHANG == 3 and SlidingBracket().max_gap == 3


# -- positions ----------------------------------------------------------------------------------------

def test_a_cover_on_the_frame_edges_gets_the_system_32_line():
    """The sides' front edges touch the cover's back face (x 12): the frame
    holes 37 behind it at x 49, the panel holes 15 out from each side's
    inner face (y 33 and 567); two brackets per side 50 from the ends of
    the 500 mm they share, numbered from the bottom, a pair 32 apart; Ø2 x
    6 pilot holes everywhere."""
    _, parts = _cover(SlidingBracket(PF_L))
    zs = [34.0, 66.0, 434.0, 466.0]
    names = ["1a", "1b", "2a", "2b"]
    assert _holes(parts["left"]) == [(f"bracket_cover_{n}", "right", 49.0, z, 2.0, 6.0) for n, z in zip(names, zs)]
    assert _holes(parts["right"]) == [(f"bracket_cover_{n}", "left", 49.0, z, 2.0, 6.0) for n, z in zip(names, zs)]
    assert _holes(parts["cover"]) == (
        [(f"bracket_left_{n}", "back", 33.0, z, 2.0, 6.0) for n, z in zip(names, zs)]
        + [(f"bracket_right_{n}", "back", 567.0, z, 2.0, 6.0) for n, z in zip(names, zs)])


@pytest.mark.parametrize("gap", [0.0, 5.0, 29.0])
def test_the_gap_is_read_from_the_model(gap: float):
    """The frame holes stay 37 behind the panel's back face, so they move
    toward the frame board's edge by the gap: 37 - gap from it."""
    _, parts = _cover(SlidingBracket(PF_L), gap=gap)
    left = parts["left"]
    assert {u for _, _, u, *_ in _holes(left)} == {12 + 37.0}
    assert left.box().lo["x"] == 12 + gap
    assert {u - left.box().lo["x"] for _, _, u, *_ in _holes(left)} == {37 - gap}


def test_a_panel_set_in_between_the_frame_boards():
    """A back panel between the sides, 1.5 clear of each, flush with their
    back edges (x 388..400): its back face is the one toward the sides'
    middle (x 388), the frame holes 37 in front of it (x 351), the panel
    holes 15 from the sides' faces (y 33 and 567); its plates hang 1.5 over
    its edges."""
    with module("cab", BOX) as cab:
        left = board("left", ply18).on(cab.left)
        right = board("right", ply18).on(cab.right)
        rear = board("rear", ply12).on(cab.back).between(left.gap(1.5), right.gap(1.5))
        cab.mount(SlidingBracket(PF_L), panel=rear, frame=[left, right])
    assert {(face, u) for _, face, u, *_ in _holes(left)} == {("right", 351.0)}
    assert {(face, u) for _, face, u, *_ in _holes(rear)} == {("front", 567.0), ("front", 33.0)}
    (item,) = cab.hardware
    for body in item["bodies"]:
        assert all(b["max"][0] <= 388 for b in body["boxes"])        # in front of the panel
    assert not [p for p in cab.all_parts() for body in item["bodies"] for b in body["boxes"]
                if _box_hits(p, Box(dict(zip("xyz", b["min"])), dict(zip("xyz", b["max"]))))]  # type: ignore[arg-type]


def test_count_end_and_at():
    """count=3 with end=100: z 100, 250, 400. at= positions go to every
    frame board named."""
    _, parts = _cover(SlidingBracket(PF_L, count=3, end=100), frame="left")
    assert [z for *_, z, _, _ in _holes(parts["left"])] == [84.0, 116.0, 234.0, 266.0, 384.0, 416.0]
    registry.reset()
    _, parts = _cover(SlidingBracket(PF_L, at=[Pos("z", 120), Pos("z", 380)]))
    for side in ("left", "right"):
        assert [z for *_, z, _, _ in _holes(parts[side])] == [104.0, 136.0, 364.0, 396.0]
    assert len(_holes(parts["cover"])) == 8


def test_one_bracket_is_centred():
    _, parts = _cover(SlidingBracket(PF_L, count=1), frame="right")
    assert [z for *_, z, _, _ in _holes(parts["right"])] == [234.0, 266.0]


def test_brackets_on_horizontal_rails_are_numbered_from_the_panels_left():
    """A cover hung on a rail under the top (z 482..500, its lower face the
    frame face): the edge runs along y. Standing in front (at -x) the
    panel's left is +y, so bracket 1 is the one near y 600 and its hole a
    the one nearer the left; the frame holes 37 behind the cover, the panel
    holes 15 below the rail. The same in a cabinet with front=."""
    for front in (False, True):
        registry.reset()
        with (module("cab", BOX, front=BOX.front) if front else module("cab", BOX)) as cab:
            rail = board("rail", ply18).on(cab.top).between(cab.front.into(12))
            cover = board("cover", ply12).on(cab.front)
            cab.mount(SlidingBracket(PF_L), panel=cover, frame=rail)
        ys = [566.0, 534.0, 66.0, 34.0]
        assert [(n, f, u, v) for n, f, u, v, *_ in _holes(rail)] == [
            (f"bracket_cover_{n}", "bottom", 49.0, y) for n, y in zip(["1a", "1b", "2a", "2b"], ys)]
        assert [(u, v) for _, _, u, v, *_ in _holes(cover)] == [(y, 482.0 - 15) for y in ys]
        assert [b["name"] for b in cab.hardware[0]["bodies"]] == ["rail_1", "rail_2"]


def test_frame_takes_a_face():
    """A partition in the middle (y 291..309): naming its left face (y 291,
    pointing -y) puts the frame parts on it, toward a panel over the left
    half."""
    with module("cab", BOX) as cab:
        wall = board("wall", ply18).center(cab.center("width")).between(cab.front.into(12))
        panel = board("cover", ply12).on(cab.front).between(Pos("y", 300), cab.left)
        cab.mount(SlidingBracket(PF_L), panel=panel, frame=wall.left)
    assert {(face, u) for _, face, u, *_ in _holes(wall)} == {("left", 49.0)}
    assert {u for _, _, u, *_ in _holes(panel)} == {291.0 - 15}


# -- holes ------------------------------------------------------------------------------------------

def test_euro_and_custom_holes():
    """Euro screws take Ø5 x 11 holes; a part's holes may be given as
    (diameter, depth)."""
    _, parts = _cover(SlidingBracket(PF_L, frame_hole="euro", panel_hole=(2.5, 8)))
    assert {(d, depth) for *_, d, depth in _holes(parts["left"])} == {(data.EURO_DIAMETER, data.EURO_DEPTH)}
    assert {(d, depth) for *_, d, depth in _holes(parts["cover"])} == {(2.5, 8.0)}
    registry.reset()
    _, parts = _cover(SlidingBracket(PF_L, panel_hole="euro"), cover=material("birch", t=15))
    assert {(d, depth) for *_, d, depth in _holes(parts["cover"])} == {(5.0, 11.0)}


@pytest.mark.parametrize("t, depth", [(18.0, 11.0), (13.0, 11.0), (12.0, 10.0), (9.0, 7.0)])
def test_euro_holes_stop_2_short_of_the_far_face(t: float, depth: float):
    """Florian 2026-10-12: Euro holes are 11 deep, but never deeper than
    the board less 2 (10 on a 12 mm board), in the frame boards and the
    panel alike; the 18 mm sides keep 11. Explicit sizes stay as given."""
    _, parts = _cover(SlidingBracket(PF_L, frame_hole="euro", panel_hole="euro"), cover=material("birch", t=t))
    assert {(d, dp) for *_, d, dp in _holes(parts["cover"])} == {(5.0, depth)}
    assert {(d, dp) for *_, d, dp in _holes(parts["left"])} == {(5.0, 11.0)}
    registry.reset()
    _, parts = _cover(SlidingBracket(PF_L, panel_hole=(5, 11)), cover=material("birch", t=12))
    assert {(d, dp) for *_, d, dp in _holes(parts["cover"])} == {(5.0, 11.0)}


def test_euro_holes_need_a_board_thicker_than_the_wall():
    with pytest.raises(LangError, match="too thin for Euro holes"):
        _cover(SlidingBracket(PF_L, panel_hole="euro"), cover=material("veneer", t=2))
    assert _holes(registry.roots[0].part("left")) == []


def test_bad_hole_settings_are_refused():
    with pytest.raises(LangError, match="expected 'pilot' or 'euro'"):
        SlidingBracket(frame_hole="m4")  # type: ignore[arg-type]
    with pytest.raises(LangError, match="greater than zero"):
        SlidingBracket(panel_hole=(2, 0))


def test_holes_as_deep_as_a_board_is_thick_are_refused_before_drilling():
    """Holes 11 deep, given as such, into a 9 mm cover: refused, and
    nothing drilled ("euro" would make them 7 deep there)."""
    with pytest.raises(LangError, match="panel_hole depth"):
        _cover(SlidingBracket(PF_L, panel_hole=(5, 11)), cover=material("birch", t=9))
    left = registry.roots[0].part("left")
    assert _holes(left) == [] and registry.roots[0].hardware == []


# -- refusals ---------------------------------------------------------------------------------------

def test_a_gap_over_29_is_refused():
    with pytest.raises(LangError, match="at most"):
        _cover(SlidingBracket(PF_L), gap=30)


def test_a_frame_board_that_ends_before_the_plate_does_is_refused():
    with module("cab", BOX) as cab:
        left = board("left", ply18).on(cab.left).between(cab.front.into(12), cab.front.into(50))
        cover = board("cover", ply12).on(cab.front)
        with pytest.raises(LangError, match="reaches 45 mm"):
            cab.mount(SlidingBracket(PF_L), panel=cover, frame=left)


def test_a_panel_short_of_the_frame_face_is_refused():
    """Set in between with 4 mm clearance: the tongue would not reach."""
    with module("cab", BOX) as cab:
        left = board("left", ply18).on(cab.left)
        rear = board("rear", ply12).on(cab.back).between(left.gap(4), cab.right)
        with pytest.raises(LangError, match="within 3 mm"):
            cab.mount(SlidingBracket(PF_L), panel=rear, frame=left)


def test_a_parallel_frame_board_is_refused():
    with module("cab", BOX) as cab:
        back = board("back", ply18).on(cab.back)
        cover = board("cover", ply12).on(cab.front)
        with pytest.raises(LangError, match="parallel"):
            cab.mount(SlidingBracket(PF_L), panel=cover, frame=back)


@pytest.mark.parametrize("kwargs, message", [
    ({"end": 20}, "at least 24"),
    ({"count": 2, "at": []}, "not both"),
    ({"count": 0}, "at least 1"),
    ({"at": []}, "empty"),
])
def test_bad_placement_settings_are_refused(kwargs: dict[str, Any], message: str):
    with pytest.raises(LangError, match=message):
        SlidingBracket(**kwargs)


@pytest.mark.parametrize("bracket, message", [
    (SlidingBracket(PF_L, at=[Pos("z", 100), Pos("z", 140)]), "would overlap"),
    (SlidingBracket(PF_L, at=[Pos("z", 510)]), "outside the stretch"),
    (SlidingBracket(PF_L, at=[Pos("x", 100)]), "not on the axis"),
    (SlidingBracket(PF_L, count=3, end=250), "too short"),
    # 20 from the bottom: the plates would hang 4 mm off both boards
    (SlidingBracket(PF_L, at=[Pos("z", 20)]), "does not fit"),
])
def test_brackets_too_close_or_off_the_stretch_are_refused(bracket: SlidingBracket, message: str):
    with pytest.raises(LangError, match=message):
        _cover(bracket)
    assert _holes(registry.roots[0].part("left")) == []


def test_a_plate_over_a_pocket_or_a_hole_in_a_hole_is_refused():
    with module("cab", BOX) as cab:
        left = board("left", ply18).on(cab.left).between(cab.front.into(12))
        cover = board("cover", ply12).on(cab.front)
        left.pocket(rect(depth=20, height=20), at=left.right.front(30).bottom(40), depth=5)
        with pytest.raises(LangError, match="frame part of bracket 1 does not fit"):
            cab.mount(SlidingBracket(PF_L), panel=cover, frame=left)
    registry.reset()
    with module("cab", BOX) as cab:
        left = board("left", ply18).on(cab.left).between(cab.front.into(12))
        cover = board("cover", ply12).on(cab.front)
        cover.hole(d=8, depth=5, at=cover.back.left(33).bottom(34))
        with pytest.raises(LangError, match="lands off"):
            cab.mount(SlidingBracket(PF_L), panel=cover, frame=left)
        assert _holes(left) == []


def test_mount_options_are_checked():
    with module("cab", BOX) as cab:
        left = board("left", ply18).on(cab.left).between(cab.front.into(12))
        cover = board("cover", ply12).on(cab.front)
        with pytest.raises(LangError, match="takes panel= and frame="):
            cab.mount(SlidingBracket(PF_L), panel=cover)
        with pytest.raises(LangError, match="named twice"):
            cab.mount(SlidingBracket(PF_L), panel=cover, frame=[left, left])
        with pytest.raises(LangError, match="cannot be one of its frame boards"):
            cab.mount(SlidingBracket(PF_L), panel=cover, frame=[cover])
        with pytest.raises(LangError, match="narrow face"):
            cab.mount(SlidingBracket(PF_L), panel=cover, frame=left.front)


# -- the makers' advice -------------------------------------------------------------------------------

def test_the_makers_advice_is_not_checked():
    """Florian 2026-10-12: Keku's largest spacing (600) and Häfele's "no
    hanging loads" are advice, not checks: two brackets 1300 apart on a
    1400 mm side, and a panel hanging under its frame boards, build
    without a note."""
    tall = Box.from_size(width=600, depth=400, height=1400)
    with module("cab", tall) as cab:
        left = board("left", ply18).on(cab.left).between(cab.front.into(12))
        cover = board("cover", ply12).on(cab.front)
        cab.mount(SlidingBracket(PF_L), panel=cover, frame=left)
    assert build_layout()["modules"][0]["problems"] == []
    registry.reset()
    with module("cab", BOX) as cab:
        battens = [board(f"batten{i}", ply18).on(side).between(cab.bottom.into(12))
                   for i, side in enumerate((cab.left, cab.right))]
        ceiling = board("ceiling", ply12).on(cab.bottom)
        cab.mount(SlidingBracket(PF_L), panel=ceiling, frame=battens)
    assert build_layout()["modules"][0]["problems"] == []


# -- the brackets as boxes --------------------------------------------------------------------------

def test_brackets_are_placed_as_one_body_each():
    """Per bracket a body of the frame part's and the panel part's boxes,
    measured out from the side's inner face (left y 18 toward +y, right y
    582 toward -y), back from the cover's back face (x 12, toward +x) and along z from its centre;
    they touch the boards without reaching into them, and no_interference
    finds nothing."""
    cab, parts = _cover(SlidingBracket(PF_L))
    (item,) = cab.hardware
    assert (item["path"], item["name"]) == ("cab.cover_brackets", "cover_brackets")
    assert [b["name"] for b in item["bodies"]] == ["left_1", "left_2", "right_1", "right_2"]
    for body, (out, z) in zip(item["bodies"], [((1, 18.0, 1), 50.0), ((1, 18.0, 1), 450.0),
                                               ((1, 582.0, -1), 50.0), ((1, 582.0, -1), 450.0)]):
        assert body["boxes"] == [_world(b, out, (0, 12.0, 1), z) for b in SHAPE.boxes()]
    assert not [p.path for p in parts.values() for body in item["bodies"] for b in body["boxes"]
                if _box_hits(p, Box(dict(zip("xyz", b["min"])), dict(zip("xyz", b["max"]))))]  # type: ignore[arg-type]
    assert no_interference(cab) == []


def test_a_part_in_the_brackets_space_is_reported():
    """The hardware check sees the boxes: a shelf through the hook's and
    the tongue's space is reported."""
    with module("cab", BOX) as cab:
        left = board("left", ply18).on(cab.left).between(cab.front.into(12))
        right = board("right", ply18).on(cab.right).between(cab.front.into(12))
        board("shelf", ply18).on(Pos("z", 40), toward=cab.top).between(left, right, cab.front.into(30))
        cover = board("cover", ply12).on(cab.front)
        cab.mount(SlidingBracket(PF_L), panel=cover, frame=[left, right])
    assert any("cover_brackets.left_1 overlaps cab.shelf" in p for p in no_interference(cab))


# -- the bent frame part, PF-L-R --------------------------------------------------------------------

def test_the_bent_frame_part_sits_at_the_frame_edge():
    """The default PF-L-R on the sides' front edges (x 12, the cover's back
    face): the frame holes 8 behind it at x 20, where the frame part's
    plate begins; the panel holes 19 out from the sides' faces (y 37 and
    563), the tongue lying on the 4 mm plate; Ø2 x 6 pilots, two per side
    50 from the ends, a pair 32 apart."""
    _, parts = _cover(SlidingBracket())
    zs = [34.0, 66.0, 434.0, 466.0]
    names = ["1a", "1b", "2a", "2b"]
    assert _holes(parts["left"]) == [(f"bracket_cover_{n}", "right", 20.0, z, 2.0, 6.0) for n, z in zip(names, zs)]
    assert _holes(parts["right"]) == [(f"bracket_cover_{n}", "left", 20.0, z, 2.0, 6.0) for n, z in zip(names, zs)]
    assert _holes(parts["cover"]) == (
        [(f"bracket_left_{n}", "back", 37.0, z, 2.0, 6.0) for n, z in zip(names, zs)]
        + [(f"bracket_right_{n}", "back", 563.0, z, 2.0, 6.0) for n, z in zip(names, zs)])


@pytest.mark.parametrize("gap", [0.0, 1.5, 3.0])
def test_the_bent_frame_part_takes_a_gap_up_to_3(gap: float):
    """Florian 2026-10-12: the cover may stand up to 3 mm in front of the
    sides' edges. The plate begins at the cover's back face, so it hangs
    over the edge by the gap; the frame holes stay 8 behind the cover (x
    20), 8 - gap from the edge, the panel holes 19 from the sides' faces.
    The boxes reach into no board."""
    cab, parts = _cover(SlidingBracket(), gap=gap)
    left = parts["left"]
    assert left.box().lo["x"] == 12 + gap
    assert {(u, u - left.box().lo["x"]) for _, _, u, *_ in _holes(left)} == {(20.0, 8 - gap)}
    assert {u for _, _, u, *_ in _holes(parts["cover"])} == {37.0, 563.0}
    assert no_interference(cab) == []


def test_the_bent_frame_part_refuses_a_gap_over_3():
    """3.5 mm would leave more of the plate in the air: refused, naming
    the gap and the limit, before anything is drilled."""
    with pytest.raises(LangError, match=r"lies 3\.5 mm behind .*may hang 3 mm over the frame board's edge, so the gap "
                                        r"may be at most 3 mm"):
        _cover(SlidingBracket(), gap=3.5)
    assert _holes(registry.roots[0].part("left")) == [] and _holes(registry.roots[0].part("cover")) == []


def test_the_bent_frame_part_behind_a_panel_set_in_between():
    """The rear panel 5 mm clear of the sides: the panel part's plate
    begins 4 from the sides' faces, so it hangs 1 mm over the panel's
    edge; the frame holes 8 in front of the panel (x 380), the panel holes
    19 from the sides' faces. 8 mm clear is refused: 7 is the most."""
    with module("cab", BOX) as cab:
        left = board("left", ply18).on(cab.left)
        right = board("right", ply18).on(cab.right)
        rear = board("rear", ply12).on(cab.back).between(left.gap(5), right.gap(5))
        cab.mount(SlidingBracket(), panel=rear, frame=[left, right])
    assert {(face, u) for _, face, u, *_ in _holes(left)} == {("right", 380.0)}
    assert {(face, u) for _, face, u, *_ in _holes(rear)} == {("front", 37.0), ("front", 563.0)}
    assert no_interference(cab) == []
    registry.reset()
    with module("cab", BOX) as cab:
        left = board("left", ply18).on(cab.left)
        rear = board("rear", ply12).on(cab.back).between(left.gap(8), cab.right)
        with pytest.raises(LangError, match="within 7 mm"):
            cab.mount(SlidingBracket(), panel=rear, frame=left)


def test_the_bent_frame_part_needs_29_of_frame_board():
    """Its plate bears on the frame board from the panel's back face to 29
    behind it (the rest is rounded underneath)."""
    for depth, fits in ((29.0, True), (25.0, False)):
        registry.reset()
        with module("cab", BOX) as cab:
            left = board("left", ply18).on(cab.left).between(cab.front.into(12), cab.front.into(12 + depth))
            cover = board("cover", ply12).on(cab.front)
            if fits:
                cab.mount(SlidingBracket(), panel=cover, frame=left)
            else:
                with pytest.raises(LangError, match="reaches 29 mm"):
                    cab.mount(SlidingBracket(), panel=cover, frame=left)


def test_bent_brackets_are_placed_as_one_body_each():
    """The PF-L-R's boxes, out from the sides' faces, back from the
    cover's back face (x 12), along z: they touch the boards, the tongue
    lying on the frame part's plate, and no_interference finds nothing."""
    cab, parts = _cover(SlidingBracket())
    (item,) = cab.hardware
    for body, (out, z) in zip(item["bodies"], [((1, 18.0, 1), 50.0), ((1, 18.0, 1), 450.0),
                                               ((1, 582.0, -1), 50.0), ((1, 582.0, -1), 450.0)]):
        assert body["boxes"] == [_world(b, out, (0, 12.0, 1), z) for b in BENT_SHAPE.boxes()]
    assert not [p.path for p in parts.values() for body in item["bodies"] for b in body["boxes"]
                if _box_hits(p, Box(dict(zip("xyz", b["min"])), dict(zip("xyz", b["max"]))))]  # type: ignore[arg-type]
    assert no_interference(cab) == []


# -- the example --------------------------------------------------------------------------------------

def test_the_example_builds_clean_and_plans_its_holes(tmp_path: Path):
    """examples/removable_panels.py: the cover on the sides' front edges
    on the bent frame part, its frame holes 8 behind its back face and its
    own 19 in from the sides; the rear panel set in between on the straight
    frame part, Euro holes on the System 32 line 37 in front of it."""
    example = Path(__file__).resolve().parents[1] / "examples" / "removable_panels.py"
    layout = run_build(example, tmp_path, scene=True)
    (module_,) = layout["modules"]
    assert layout["problems"] == [] and module_["problems"] == []
    assert [h["name"] for h in module_["hardware"]] == ["cover_brackets", "rear_brackets"]
    assert all(len(h["bodies"]) == 4 for h in module_["hardware"])
    parts = {p["path"]: p for p in module_["parts"]}
    cover, left, rear = parts["seatbase.cover"], parts["seatbase.left"], parts["seatbase.rear"]
    back_face = cover["box"]["min"][0]
    assert left["box"]["max"][0] == back_face
    holes = [op for op in left["ops"] if op["kind"] == "hole" and (op["name"] or "").startswith("bracket_cover")]
    assert {(op["u"], op["d"], op["depth"]) for op in holes} == {(back_face - 8, 2.0, 6.0)}
    holes = [op for op in cover["ops"] if op["kind"] == "hole" and (op["name"] or "").startswith("bracket_left")]
    assert {op["u"] for op in holes} == {left["box"]["max"][1] + 19}
    holes = [op for op in left["ops"] if op["kind"] == "hole" and (op["name"] or "").startswith("bracket_rear")]
    assert {(op["u"], op["d"], op["depth"]) for op in holes} == {(rear["box"]["max"][0] + 37, 5.0, 11.0)}
    plan = plan_layout(layout)
    assert plan.problems == []
    side = next(p for p in plan.parts if p.path == "seatbase.left")
    euro = [s for s in side.steps if isinstance(s, HoleStep) and (s.d, s.depth) == (5.0, 11.0)]
    assert sum(len(s.points) for s in euro) == 4
    assert {b.name for h in plan.hardware for b in h.bodies} == {"left_1", "left_2", "right_1", "right_2"}
    assert (tmp_path / "scene.glb").exists()
