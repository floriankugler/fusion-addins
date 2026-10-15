"""Slats (`slat()`): solid wood by section and length, placed by naming what
their faces do (`on()` a wide face, `edge_on()` a narrow face, `center()`
the middle, `between()` the ends), cosmetic for now: no operations, joins
or hardware."""
from collections.abc import Callable
from pathlib import Path

import pytest

from lang import *
from lang.core.directions import AXES
from lang.build import run_build
from lang.core.layout import build_layout
from lang.emit.plan import plan_layout
from helpers import ply15, part_meshes

#: The module's box: x (depth) 0 to 400 from the front, y (width) 0 to 600 from the left, z 0 to 700.
BOX = Box.from_size(width=600, depth=400, height=700)
oak = slat_material("oak")


def _extents(part: Board) -> dict[str, tuple[float, float]]:
    b = part.box()
    return {a: (round(b.lo[a], 6), round(b.hi[a], 6)) for a in AXES}


def _carcass() -> tuple[Scope, Board, Board, Board]:
    """Sides at the left (y 0 to 15) and right (585 to 600) and a shelf
    between them, 15 thick from z 300."""
    with module("m", BOX) as m:
        left = board("left", ply15).on(m.left)
        right = board("right", ply15).on(m.right)
        shelf = board("shelf", ply15).on(Pos("z", 300), toward=m.top).between(left, right)
    return m, left, right, shelf


# -- placement ------------------------------------------------------------------------------------

def test_on_puts_a_wide_face_and_edge_on_a_narrow_face_on_their_references():
    m, left, _, shelf = _carcass()
    with m:
        cleat = slat("cleat", oak, section=(20, 40)).on(left.inner).edge_on(shelf.bottom).between(m.front, m.back)
    # 20 off the side, 40 down from the shelf, front to back
    assert _extents(cleat) == {"x": (0, 400), "y": (15, 35), "z": (260, 300)}
    assert (cleat.thickness, cleat.width, cleat.section) == (20, 40, (20, 40))
    assert cleat.t_axis == "y" and cleat.left.is_big and not cleat.top.is_big


def test_the_same_slat_turned_swaps_its_references():
    m, left, _, shelf = _carcass()
    with m:
        cleat = slat("cleat", oak, section=(20, 40)).on(shelf.bottom).edge_on(left.inner).between(m.front, m.back)
    # 20 under the shelf, 40 off the side
    assert _extents(cleat) == {"x": (0, 400), "y": (15, 55), "z": (280, 300)}
    assert cleat.t_axis == "z"


def test_the_sizes_of_a_section_come_in_either_order():
    m, left, _, shelf = _carcass()
    with m:
        a = slat("a", oak, section=(20, 40)).on(left.inner).edge_on(shelf.bottom).between(m.front, m.back)
        b = slat("b", oak, section=(40, 20)).on(left.inner).edge_on(shelf.bottom).between(m.front, m.back)
    assert _extents(a) == _extents(b) and a.section == b.section == (20, 40)


def test_center_places_the_middle_of_the_slat():
    with module("m", BOX) as m:
        # a batten standing on edge on the bottom, centred on y 100
        batten = slat("batten", oak, section=(20, 60)).edge_on(m.bottom).center(Pos("y", 100)).between(m.front, m.back)
        # a slat lying flat on the bottom, its width centred on x 200
        flat = slat("flat", oak, section=(20, 60)).on(m.bottom).center(Pos("x", 200)).between(m.left, m.right)
    assert _extents(batten) == {"x": (0, 400), "y": (90, 110), "z": (0, 60)}
    assert _extents(flat) == {"x": (170, 230), "y": (0, 600), "z": (0, 20)}


def test_a_bare_position_needs_toward():
    with module("m", BOX) as m:
        s = slat("s", oak, section=(20, 40)).on(Pos("z", 100), toward=m.bottom).edge_on(Pos("y", 50), toward=m.right)
        s.between(m.front, m.back)
        assert _extents(s) == {"x": (0, 400), "y": (50, 90), "z": (80, 100)}
        with pytest.raises(LangError, match="toward="):
            slat("t", oak, section=(20, 40)).edge_on(Pos("y", 50))


def test_missing_ends_come_from_the_scope_box():
    m, left, _, shelf = _carcass()
    with m:
        whole = slat("whole", oak, section=(20, 40)).on(left.inner).edge_on(shelf.bottom)
        half = slat("half", oak, section=(20, 40)).on(left.inner).edge_on(shelf.top).between(Pos("x", 150))
    assert _extents(whole)["x"] == (0, 400)
    assert _extents(half)["x"] == (150, 400)        # the far side of the room from its one end


def test_the_length_runs_along_the_axis_the_section_leaves():
    with module("m", BOX) as m:
        post = slat("post", oak, section=(40, 40)).on(m.front).edge_on(m.left).between(Pos("z", 100), Pos("z", 500))
    assert _extents(post) == {"x": (0, 40), "y": (0, 40), "z": (100, 500)}


def test_a_slat_limits_a_board_on_both_of_its_cross_axes():
    """A board between two slats meets either their narrow or their wide
    faces: a slat is a limit on both of its cross axes."""
    with module("m", BOX) as m:
        a = slat("a", oak, section=(20, 40)).on(m.bottom).edge_on(m.left).between(m.front, m.back)
        b = slat("b", oak, section=(20, 40)).on(m.bottom).edge_on(m.right).between(m.front, m.back)
        top = board("top", ply15).on(a.top).between(a, b)              # on their wide faces, between their narrow ones
        c = slat("c", oak, section=(20, 40)).edge_on(m.bottom).on(m.left).between(m.front, m.back)
        d = slat("d", oak, section=(20, 40)).edge_on(m.bottom).on(m.right).between(m.front, m.back)
        panel = board("panel", ply15).on(c.top).between(c, d)          # between their wide faces
    assert _extents(top)["y"] == (40, 560) and _extents(top)["z"] == (20, 35)
    assert _extents(panel)["y"] == (20, 580) and _extents(panel)["z"] == (40, 55)


def test_slats_end_against_parts():
    m, left, right, shelf = _carcass()
    with m:
        rail = slat("rail", oak, section=(20, 40)).on(m.front).edge_on(shelf.top).between(left, right)
    assert _extents(rail) == {"x": (0, 20), "y": (15, 585), "z": (315, 355)}


def test_slats_in_a_cabinet_read_its_own_terms():
    """A cabinet opening toward the module's right: the cleat on its left
    side, 20 off it, under the shelf, from its front to its back, whatever
    the world calls those."""
    box = Box.from_size(width=600, depth=400, height=700)
    with cabinet("cab", box, front=box.right) as cab:
        left = board("left", ply15).on(cab.left)
        shelf = board("shelf", ply15).on(Pos("z", 300), toward=cab.top).between(left, cab.right)
        cleat = slat("cleat", oak, section=(20, 40)).on(left.inner).edge_on(shelf.bottom).between(cab.front, cab.back)
    lb, cb = left.box(), cleat.box()
    assert cleat.t_axis == left.t_axis
    t = left.t_axis
    assert min(abs(cb.lo[t] - lb.hi[t]), abs(cb.hi[t] - lb.lo[t])) < 1e-9 and cb.hi[t] - cb.lo[t] == 20
    assert (cb.lo["z"], cb.hi["z"]) == (260, 300)
    assert cleat.front.name == "front" and cleat.inner.direction == left.inner.direction


# -- refusals --------------------------------------------------------------------------------------

_AMBIGUOUS: list[tuple[Callable[[Slat, Scope], object], str]] = [
    (lambda s, m: s.on(m.bottom), "only on"),
    (lambda s, m: s.between(m.front, m.back), "none is given"),
    (lambda s, m: s.on(m.bottom).edge_on(m.left).center(Pos("x", 100)), "all three"),
    (lambda s, m: s.on(m.bottom).edge_on(m.top), "both place the slat on z"),
    (lambda s, m: s.on(m.bottom).center(Pos("z", 100)), "both place the slat on z"),
    (lambda s, m: s.on(m.bottom).edge_on(m.left).between(m.front, m.right), "does not limit the slat's length"),
]


@pytest.mark.parametrize("place, message", _AMBIGUOUS)
def test_a_slat_placed_ambiguously_is_an_error(place: Callable[[Slat, Scope], object], message: str) -> None:
    with module("m", BOX) as m:
        s = slat("s", oak, section=(20, 40))
        place(s, m)
        with pytest.raises(LangError, match=message):
            s.box()


def test_inset_and_grain_are_refused():
    with module("m", BOX):
        s = slat("s", oak, section=(20, 40))
        with pytest.raises(LangError, match="section is its own"):
            s.inset(2)
        with pytest.raises(LangError, match="runs along its length"):
            s.grain("depth")


@pytest.mark.parametrize("section, message", [((0, 40), "at least"), ((20,), "two sizes"), ((20, 40, 60), "two sizes"),
                                              (("a", 3), "two sizes")])
def test_a_section_is_two_sizes(section: tuple[float, float], message: str) -> None:
    with module("m", BOX):
        with pytest.raises(LangError, match=message):
            slat("s", oak, section=section)


def test_materials_go_with_their_parts():
    with module("m", BOX):
        with pytest.raises(LangError, match="slat material.*slat\\('b', oak"):
            board("b", oak)  # type: ignore[arg-type]
        with pytest.raises(LangError, match="not a slat material"):
            slat("s", ply15, section=(20, 40))  # type: ignore[arg-type]


def test_a_slat_takes_no_operations():
    m, left, _, shelf = _carcass()
    with m:
        s = slat("s", oak, section=(20, 40)).on(left.inner).edge_on(shelf.bottom).between(m.front, m.back)
        attempts = [
            lambda: s.cut(rect(depth=10, height=10), at=s.left.center),
            lambda: s.hole(5, s.left.center, depth=5),
            lambda: s.pocket(rect(depth=10, height=10), at=s.left.center, depth=5),
            lambda: s.slot(5, at=s.left.center, centres=20, along="depth", depth=5),
            lambda: s.chamfer(s.left.top, 1),
            lambda: s.fillet(s.front.top, 2),
            lambda: s.dogbones(),
            lambda: s.cutout(),
            lambda: s.lip(s.front, 2, oak),
            lambda: s.join(shelf, using=screws(count=2)),
            lambda: shelf.join(s, using=screws(count=2)),
        ]
        for attempt in attempts:
            with pytest.raises(LangError, match="takes no operations"):
                attempt()
    assert s.ops == [] and shelf.ops == []


def test_hardware_goes_on_boards_not_slats():
    box = Box.from_size(width=600, depth=400, height=700)
    with cabinet("cab", box, front=box.front) as cab:
        left = board("left", ply15).on(cab.left)
        door = slat("door", oak, section=(20, 400)).on(cab.front).edge_on(left.inner).between(cab.bottom, cab.top)
        with pytest.raises(LangError, match="is a slat; hardware goes on boards"):
            cab.mount(ConcealedHinge(), door=door, carcass=left)
    assert door.ops == [] and left.ops == []


# -- layout, preview, emitter, checks ---------------------------------------------------------------

def test_the_layout_names_slats_and_their_sections():
    m, left, _, shelf = _carcass()
    with m:
        slat("cleat", oak, section=(40, 20)).on(left.inner).edge_on(shelf.bottom).between(m.front, m.back)
    layout = build_layout()
    parts = {p["path"]: p for p in layout["modules"][0]["parts"]}
    cleat, side = parts["m.cleat"], parts["m.left"]
    assert (cleat["kind"], cleat["section"], cleat["material"], cleat["thickness"]) == ("slat", [20.0, 40.0], "oak", 20)
    assert cleat["grain"] == "x" and cleat["grained"] and cleat["ops"] == []
    assert (side["kind"], side["section"]) == ("board", None)
    plans = {p.path: p for p in plan_layout(layout).parts}
    facts = plans["m.cleat"].facts
    assert facts is not None and facts.kind == "slat" and facts.material == "oak"


def test_the_preview_meshes_a_slat_as_its_section_by_its_length():
    m, left, _, shelf = _carcass()
    with m:
        slat("cleat", oak, section=(20, 40)).on(left.inner).edge_on(shelf.bottom).between(m.front, m.back)
    mesh = part_meshes()["m.cleat"]
    assert mesh.volume == pytest.approx(20 * 40 * 400)


def test_checks_see_slats():
    m, left, _, _ = _carcass()
    with m:
        slat("in_shelf", oak, section=(20, 40)).on(left.inner).edge_on(Pos("z", 310), toward=m.bottom)
        board("long", sheet_material("birch", t=15, size=(100, 100))).on(m.bottom).between(left, Pos("x", 50))
        check(no_interference, fits_sheet)
    problems = m.run_checks()
    assert "m.shelf overlaps m.in_shelf" in problems or "m.in_shelf overlaps m.shelf" in problems
    assert any(p.startswith("m.long ") and "sheet" in p for p in problems)
    assert not any("in_shelf" in p and "sheet" in p for p in problems)      # a slat is on no sheet


def test_the_example_builds(tmp_path: Path) -> None:
    """`examples/slats.py`: the lipped shelf unit and the slatted bed base,
    without problems; the top's front strip runs through its corners."""
    layout = run_build(Path(__file__).parent.parent / "examples" / "slats.py", tmp_path)
    assert layout["problems"] == []
    unit, bed = layout["modules"]
    kinds = {p["path"]: p["kind"] for p in unit["parts"] + bed["parts"]}
    assert sum(k == "slat" for k in kinds.values()) == 27 and sum(k == "board" for k in kinds.values()) == 6
    parts = {p["path"]: p for p in unit["parts"]}
    front, side = parts["unit.top_lip_front"]["box"], parts["unit.top_lip_left"]["box"]
    assert front["max"][1] - front["min"][1] == 620 and side["max"][0] - side["min"][0] == 310
    assert parts["unit.shelf_lip_front"]["section"] == [0.5, 18.0]
