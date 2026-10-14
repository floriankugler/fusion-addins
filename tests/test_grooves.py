"""Grooves (`lang.joints.grooves`): a panel set into grooves in the boards
around it, as a drawer floor in its box.

The box: 12 mm sides `l` (y 0..12) and `r` (y 288..300) the full depth (x
0..200, z 0..100), a front `f` (x 0..12) and a back `k` (x 188..200)
between them, and a 9 mm floor at z 10..19 between all four (x 12..188, y
12..288). Grooved 5 deep into each, the floor's outline runs x 7..193, y
7..293; the sides' grooves stop inside them, 7 - 0.5 and 193 + 0.5 along x
with a clearance of 0.5, the front's and the back's run out of their ends
into the sides.
"""
import math
from pathlib import Path
from typing import Any

import pytest
from shapely.geometry import Point

from lang import *
from lang.core.layout import build_layout
from lang.core.ops import Cut, Pocket
from lang.core.scope import registry
from lang.emit.plan import PocketStep, plan_layout
from helpers import EXAMPLES, has_material, overlap, part_meshes, ply12, ply9, run_example, state

O = 6 / (2 * math.sqrt(2))          # a corner relief's centre, along each edge from the corner
R = 3.05                            # its radius: the 6 mm tool plus 0.1, halved


def _box(floor_to: str = "k") -> tuple[Scope, dict[str, Board]]:
    """The box above; `floor_to="back"` runs the floor to the box's back
    instead, under where a back standing on it would be, and leaves the
    back out."""
    with module("box", Box.from_size(width=300, depth=200, height=100)) as m:
        l = board("left", ply12).on(m.left)
        r = board("right", ply12).on(m.right)
        f = board("front", ply12).on(m.front).between(l, r)
        parts = {"l": l, "r": r, "f": f}
        if floor_to == "k":
            k = board("back", ply12).on(m.back).between(l, r)
            parts["k"] = k
            end: Board | Side = k
        else:
            end = m.back
        parts["floor"] = board("floor", ply9).on(Pos("z", 10), toward=m.top).between(l, r, f, end)
    return m, parts


def _groove(part: Board) -> Pocket:
    (op,) = [op for op in part.ops if isinstance(op, Pocket) and (op.name or "").startswith("groove_")]
    return op



def _problems() -> list[str]:
    """The layout's problems: the checks' and the notes parts left."""
    return build_layout()["problems"]


# -- the panel ---------------------------------------------------------------------------------

def test_the_floor_goes_into_all_four_with_its_corners_chamfered():
    m, p = _box()
    floor = p["floor"]
    with m:
        floor.join(p["l"], p["r"], p["f"], p["k"], using=groove(5, clearance=(0.5, 0.5)))
    assert floor.outline.bounds == pytest.approx((7, 7, 193, 293))
    assert floor.box().lo["x"] == 12 and floor.box().hi["y"] == 288       # the box stays where it was placed
    # 3 mm along both edges off each corner, inside the grooves
    assert floor.outline.area == pytest.approx(186 * 286 - 4 * 4.5)
    assert has_material(floor, (191.6, 291.6), (191.4, 291.4), (7.1, 9.8), (7.1, 10.0)) == [False, True, False, True]
    assert floor.ops == []                                                 # an outline, no operation


def test_chamfer_none_or_0_leaves_the_corners_square():
    for chamfer in (None, 0):
        registry.reset()
        m, p = _box()
        with m:
            p["floor"].join(p["l"], p["r"], p["f"], p["k"], using=groove(5, chamfer=chamfer))
        assert p["floor"].outline.area == pytest.approx(186 * 286)


def test_a_chamfer_may_reach_the_boards_faces_but_not_past_them():
    m, p = _box()
    with m:
        p["floor"].join(p["l"], p["r"], p["f"], p["k"], using=groove(4, chamfer=8))
    # the chamfer's line runs through the corner where the boards' faces meet
    assert has_material(p["floor"], (11.9, 12.0), (12.1, 12.1)) == [False, True]
    with pytest.raises(LangError, match="a 10.5 mm chamfer reaches out of a 5 mm groove .* at most twice the depth"):
        groove(5, chamfer=10.5)


# -- the grooves ---------------------------------------------------------------------------------

def test_side_grooves_stop_inside_and_front_grooves_run_out():
    m, p = _box()
    with m:
        p["floor"].join(p["l"], p["r"], p["f"], p["k"], using=groove(5, clearance=(0.5, 0.5), dogbones=None))
    l, f = p["l"], p["f"]
    # from the face the floor meets, 5 + 0.5 deep; past the floor's corners
    # by 0.5, and 0.25 below and above it: the floor stays where it was
    # placed, the height clearance split evenly (Florian, 2026-10-12)
    side = _groove(l)
    assert side.name == "groove_floor" and side.face == l.inner.world_name and side.depth == 5.5
    assert side.shape.bounds == pytest.approx((6.5, 9.75, 193.5, 19.25))  # l's (x, z): inside its 0..200
    front = _groove(f)
    assert front.face == f.inner.world_name and front.depth == 5.5
    assert front.shape.bounds == pytest.approx((6.5, 9.75, 293.5, 19.25))  # f's (y, z): past its 12..288
    assert p["floor"].box().lo["z"] == 10
    assert _problems() == []


def test_without_clearance_the_grooves_are_what_the_floor_takes():
    m, p = _box()
    with m:
        p["floor"].join(p["l"], p["r"], p["f"], p["k"], using=groove(5, dogbones=None))
    assert _groove(p["r"]).depth == 5 and _groove(p["r"]).shape.bounds == pytest.approx((7, 10, 193, 19))


def test_the_stopped_ends_get_hidden_dog_bones_as_part_of_the_groove():
    """The default (Florian, 2026-10-12): each relief centred on the
    groove's end, touching its edge, bulging past the end only."""
    m, p = _box()
    with m:
        p["floor"].join(p["l"], p["r"], p["f"], p["k"], using=groove(5, clearance=(0.5, 0.5)))
    shape = _groove(p["l"]).shape
    assert shape.bounds == pytest.approx((6.5 - R, 9.75, 193.5 + R, 19.25))
    assert shape.geometry.contains(Point(6.5 - R + 0.01, 9.75 + R))       # centred on the end, R from the edge
    # the front's runs out of it at both ends: no corners, no reliefs
    assert _groove(p["f"]).shape.area == pytest.approx(287 * 9.5)
    # board.dogbones() finds nothing more there: the reliefs are arcs
    for part in p.values():
        part.dogbones()
    build_layout()
    assert not [op for part in p.values() for op in part.ops if (getattr(op, "name", "") or "").endswith("dogbones")]


def test_corner_dog_bones_bulge_past_the_ends_and_edges():
    m, p = _box()
    with m:
        p["floor"].join(p["l"], p["r"], p["f"], p["k"], using=groove(5, clearance=(0.5, 0.5), dogbones="corner"))
    shape = _groove(p["l"]).shape
    # a relief in each of the four corners, on the bisector, reaching just
    # past the corner and a little past the groove's ends and edges
    bulge = R - O
    assert shape.bounds == pytest.approx((6.5 - bulge, 9.75 - bulge, 193.5 + bulge, 19.25 + bulge))
    assert shape.geometry.contains(Point(6.5 - 0.03, 9.75 - 0.03))        # past the corner, by relief / 2


def test_hidden_dog_bones_must_stay_inside_the_board():
    """9 deep and 0.5 beyond, the sides' grooves stop 2.5 short of their
    front ends: a hidden dog bone, 3.05 past the end, would break out."""
    m, p = _box()
    with m:
        with pytest.raises(LangError, match=r"hidden dog bones would break out of box\.(left|right) past the end"):
            p["floor"].join(p["l"], p["r"], p["f"], p["k"], using=groove(9, clearance=(0.5, 0)))
        p["floor"].join(p["l"], p["r"], p["f"], p["k"], using=groove(9, clearance=(0.5, 0), dogbones="corner"))


def test_board_dogbones_relieve_a_groove_joined_without_them():
    m, p = _box()
    with m:
        p["floor"].join(p["l"], p["r"], p["f"], p["k"], using=groove(5, dogbones=None))
    p["l"].dogbones()
    p["f"].dogbones()
    build_layout()
    names = [op.name for op in p["l"].ops if isinstance(op, Pocket)]
    assert names == ["groove_floor", "groove_floor_dogbones"]
    assert len(p["f"].ops) == 1 and _groove(p["f"]).shape.area == pytest.approx(286 * 9)   # it runs out: no corners


def test_a_standing_panel_gets_half_the_height_clearance_either_side():
    """A back set into grooves in the sides, the bottom and the top: its
    groove is centred on it, as every panel's is."""
    with module("box", Box.from_size(width=300, depth=200, height=400)) as m:
        l = board("left", ply12).on(m.left)
        r = board("right", ply12).on(m.right)
        bottom = board("bottom", ply12).on(m.bottom).between(l, r)
        top = board("top", ply12).on(m.top).between(l, r)
        back = board("back", ply9).on(Pos("x", 180), toward=m.front).between(l, r, bottom, top)
        back.join(l, r, bottom, top, using=groove(6, clearance=(0, 1)))
    # the back at x 171..180, in l's (x, z) frame; l goes on past both
    # ends, so they get (hidden) reliefs
    assert _groove(l).shape.bounds == pytest.approx((170.5, 6 - R, 180.5, 394 + R))
    x0, _, x1, _ = _groove(bottom).shape.bounds                 # the bottom's (x, y)
    assert (x0, x1) == pytest.approx((170.5, 180.5))
    assert back.outline.bounds == pytest.approx((6, 6, 294, 394))


# -- what shows -------------------------------------------------------------------------------------

def test_a_groove_running_out_where_no_board_covers_it_is_noted():
    """The floor runs on to the box's back, under where a back standing on
    it would be: the sides' grooves run out of their back ends."""
    m, p = _box(floor_to="back")
    with m:
        p["floor"].join(p["l"], p["r"], p["f"], using=groove(5, clearance=(0.5, 0.5)))
    problems = _problems()
    assert problems == [f"box.{side}: the groove for box.floor runs out of it at its back end, where it shows "
                        "unless something covers it." for side in ("left", "right")]
    # its corners at the front are chamfered, those at the back are not
    assert has_material(p["floor"], (7.1, 7.1), (199.9, 7.1)) == [False, True]


def test_dados_for_shelves_from_the_side():
    """Two shelves the full depth of a side, joined from the side: one
    groove each, running out at the side's front and back, where they
    show."""
    with module("unit", Box.from_size(width=300, depth=200, height=400)) as m:
        side = board("side", ply12).on(m.left)
        low = board("low", ply12).on(Pos("z", 100), toward=m.top).between(side, m.right)
        high = board("high", ply12).on(Pos("z", 200), toward=m.top).between(side, m.right)
        side.join(low, high, using=groove(4))
    assert len(side.ops) == 2
    assert [op.name for op in side.ops if isinstance(op, Pocket)] == ["groove_low", "groove_high"]
    assert [op.shape.bounds for op in side.ops if isinstance(op, Pocket)] == [(0, 100, 200, 112), (0, 200, 200, 212)]
    assert low.outline.bounds == pytest.approx((0, 8, 200, 300))           # 4 into the side, nothing chamfered
    assert len(_problems()) == 4 and _problems()[0] == (
        "unit.side: the groove for unit.low runs out of it at its front end, where it shows unless something "
        "covers it.")


def test_an_end_narrower_than_anything_meant_goes_into_no_groove():
    """Found by fuzzing: a shelf's end notched to 7 um short of its edge
    keeps a fin as wide there. The fin's end went 4 deep into the side with
    the rest of the shelf's, but its groove, as narrow, was cleaned away as
    what a boolean leaves, and the two shared the fin. Nothing that narrow
    is meant: it is no contact, and the fin stays where it is."""
    from shapely.geometry import box
    with module("unit", Box.from_size(width=300, depth=200, height=400)) as m:
        side = board("side", ply12).on(m.left)
        shelf = board("shelf", ply12).on(Pos("z", 100), toward=m.top).between(side, m.right)
        shelf.add_cut(Shape(box(0.007, 11, 50, 13)))         # (the shelf's outline: x 0..200, y 12..300)
        side.join(shelf, using=groove(4))
    assert shelf.outline.geometry.intersection(box(0, 8, 0.007, 12)).area == 0
    assert shelf.outline.geometry.intersection(box(50, 8, 200, 12)).area == pytest.approx(150 * 4)
    meshes = part_meshes()
    assert overlap(meshes["unit.side"], meshes["unit.shelf"]) < 1e-6

def test_a_groove_through_the_board_is_an_error():
    m, p = _box()
    with m, pytest.raises(LangError, match=r"^box\.floor: groove with box\.left: a groove 12 deep, 0 beyond the "
                                           r"panel's edge, would go through box\.left \(12 thick\) and show on its far "
                                           r"face"):
        p["floor"].join(p["l"], using=groove(12))
    assert p["l"].ops == [] and p["floor"].outline.area == pytest.approx(176 * 276)


# -- joining ----------------------------------------------------------------------------------------

def test_the_panel_may_be_joined_from_a_board():
    m, p = _box()
    with m:
        p["l"].join(p["floor"], using=groove(5))
        p["r"].join(p["floor"], using=groove(5))                 # the opposite edge: no corner in common
    assert p["floor"].outline.bounds == pytest.approx((12, 7, 188, 293))
    assert _groove(p["l"]).shape.bounds == pytest.approx((12 - R, 10, 188 + R, 19))


def test_errors_are_reported_on_the_board_whose_join_was_called():
    m, p = _box()
    with m:
        with pytest.raises(LangError, match=r"^box\.left: groove with box\.floor: a groove 12 deep, 0 beyond the "
                                            r"panel's edge, would go through box\.left"):
            p["l"].join(p["floor"], using=groove(12))
        with pytest.raises(LangError, match=r"^box\.left: groove with box\.floor: the groove for box\.floor is 9 wide, "
                                            r"narrower than the 10 mm tool"):
            p["l"].join(p["floor"], using=groove(5, tool=10))
    assert p["l"].ops == [] and p["floor"].outline.area == pytest.approx(176 * 276)


def test_boards_at_a_corner_go_into_one_join():
    m, p = _box()
    with m:
        p["floor"].join(p["l"], using=groove(5))
        with pytest.raises(LangError, match="reaches past box.floor's box .* name the boards at its corners in one "
                                            "join"):
            p["floor"].join(p["f"], using=groove(5))
    assert p["f"].ops == []


def test_a_join_that_fails_on_a_board_changes_none():
    """The left side has a cutout just under the floor; the groove, 0.5
    lower than the floor with the height clearance, would run into it. The
    floor has grown into all four boards by then, and some of them have
    their grooves: every one is restored."""
    m, p = _box()
    with m:
        p["l"].cutout(rect(depth=100, height=10), at=p["l"].inner.bottom, border=5, radius=0)
        boards = [p[n] for n in ("floor", "l", "r", "f", "k")]
        before = state(*boards)
        with pytest.raises(LangError, match=r"^box\.floor: groove with box\.left: box\.left: the pocket 'groove_floor' "
                                            r"lies in the cutout 'openings'"):
            p["floor"].join(p["l"], p["r"], p["f"], p["k"], using=groove(5, clearance=(0.5, 1)))
        assert state(*boards) == before


def test_a_board_the_panel_does_not_meet_is_an_error():
    m, p = _box()
    with m:
        shelf = board("shelf", ply12).on(Pos("z", 60), toward=m.top).between(p["l"], p["r"], p["f"], p["k"])
        with pytest.raises(LangError, match="groove with box.shelf: the two do not touch"):
            p["floor"].join(p["l"], shelf, using=groove(5))
    assert p["l"].ops == [] and p["floor"].outline.area == pytest.approx(176 * 276)


@pytest.mark.parametrize("make, message", [
    (lambda: groove(0), "depth must be positive"),
    (lambda: groove(5, clearance=(-0.1, 0)), "clearance must not be negative"),
    (lambda: groove(5, chamfer=-1), "chamfer must not be negative"),
    (lambda: groove(5, dogbones="round"), "expected 'corner' or 'hidden', not 'round'"),   # type: ignore[arg-type]
    (lambda: groove(5, tool=0), "tool must be positive"),
    (lambda: groove(5, relief=-0.1), "relief must not be negative"),
])
def test_settings_are_checked(make: Any, message: str):
    with pytest.raises(LangError, match=message):
        make()


def test_the_tool_must_fit_the_groove():
    m, p = _box()
    with m:
        with pytest.raises(LangError, match="the groove for box.floor is 9 wide, narrower than the 10 mm tool"):
            p["floor"].join(p["l"], using=groove(5, tool=10))
        with pytest.raises(LangError, match="hidden dog bones are 9.1 across, wider than the 9 mm groove"):
            p["floor"].join(p["l"], using=groove(5, tool=9, dogbones="hidden"))
        p["floor"].join(p["l"], using=groove(5, tool=10, dogbones=None))


def test_the_tool_is_checked_only_where_a_relief_goes():
    """A dado running out of the side at both ends has no corner to relieve:
    its tool, which cuts only the reliefs, may be wider than the groove."""
    with module("unit", Box.from_size(width=300, depth=200, height=400)) as m:
        side = board("side", ply12).on(m.left)
        shelf = board("shelf", ply12).on(Pos("z", 100), toward=m.top).between(side, m.right)
        side.join(shelf, using=groove(4, tool=20))
    assert _groove(side).shape.bounds == (0, 100, 200, 112)


# -- assembled ----------------------------------------------------------------------------------------

def test_the_floor_fills_its_grooves_and_overlaps_no_board():
    m, p = _box()
    with m:
        p["floor"].join(p["l"], p["r"], p["f"], p["k"], using=groove(5, clearance=(0.5, 0.5)))
    meshes = part_meshes()
    for name in ("left", "right", "front", "back"):
        assert overlap(meshes["box.floor"], meshes[f"box.{name}"]) < 1e-6, name
    assert meshes["box.floor"].volume == pytest.approx((186 * 286 - 4 * 4.5) * 9)
    plan = plan_layout(build_layout())
    assert plan.problems == []
    side = next(part for part in plan.parts if part.path == "box.left")
    (step,) = side.steps
    assert isinstance(step, PocketStep) and step.depth == 5.5


def test_without_the_grooves_the_floor_wouldoverlap():
    m, p = _box()
    with m:
        p["floor"].join(p["l"], p["r"], p["f"], p["k"], using=groove(5))
    for part in (p["l"], p["f"]):
        part.ops.clear()
    meshes = part_meshes()
    assert overlap(meshes["box.floor"], meshes["box.left"]) == pytest.approx((186 * 5 - 2 * 4.5) * 9, rel=1e-3)
    assert overlap(meshes["box.floor"], meshes["box.front"]) == pytest.approx(276 * 5 * 9, rel=1e-3)


def _cabinet(tmp_path: Path, fingers: int, dogbones: str | None = None) -> None:
    """The drawer cabinet example with `fingers` in its box joints and, if
    given, `dogbones=` for its floors' grooves."""
    source = (EXAMPLES / "drawer_cabinet.py").read_text()
    source = source.replace("box_joint(7, margin=2", f"box_joint({fingers}, margin=2")
    if dogbones is not None:
        source = source.replace("clearance=(0.5, 0.5))", f"clearance=(0.5, 0.5), dogbones={dogbones!r})")
    build = tmp_path / "cabinet.py"
    build.write_text(source)
    run_example(build)


@pytest.mark.parametrize("fingers, dogbones", [(7, None), (9, "corner"), (11, "corner")])
def test_in_the_drawer_cabinet_nothing_overlaps_and_nothing_shows(tmp_path: Path, fingers: int,
                                                                   dogbones: str | None):
    """The example's drawer boxes, box-jointed with 7 fingers and, so that
    the floor lies near and across the end of a finger, with 9 and 11: the
    grooves take the fillets the joint's cutter keeps at the fingers'
    roots, so the floor overlaps none of the four boards, and nothing runs
    out where it would show."""
    _cabinet(tmp_path, fingers, dogbones)
    assert _problems() == []
    meshes = part_meshes()
    for i in (1, 2, 3):
        base = f"drawercab.drawer{i}"
        for name in ("left", "right", "front", "back"):
            assert overlap(meshes[f"{base}.floor"], meshes[f"{base}.{name}"]) < 1e-6, (base, name)


def test_hidden_dog_bones_where_the_floor_lies_across_the_end_of_a_finger(tmp_path: Path):
    """With 9 fingers the second drawer's floor lies across the lower end
    of a front finger: the front's groove stops inside the finger, and a
    hidden dog bone at its upper corner would reach down past the finger's
    end into the joint's gap. The default refuses it; corner dog bones fit
    (see above)."""
    with pytest.raises(LangError, match=r"^drawercab\.drawer2\.floor: groove with drawercab\.drawer2\.front: hidden dog "
                                        r"bones would break out of drawercab\.drawer2\.front past the end of the groove"):
        _cabinet(tmp_path, 9)


def test_the_drawer_cabinets_grooves():
    run_example(EXAMPLES / "drawer_cabinet.py")
    parts = {p.path: p for p in registry.roots[0].all_parts()}
    l, f, k, floor = (parts[f"drawercab.drawer1.{n}"] for n in ("left", "front", "back", "floor"))
    # into all four, 5 deep: the sides' inner faces at x 36 and 564, the
    # front's and back's at y 473 and 57
    assert floor.outline.bounds == pytest.approx((31, 52, 569, 478))
    # the sides' grooves stop inside their lowest finger, short of their
    # ends at y 45 and 485, their hidden dog bones too; 0.25 below and above
    # the floor at z 143..152
    assert _groove(l).shape.bounds == pytest.approx((51.5 - R, 142.75, 478.5 + R, 152.25))
    # the front's runs past its ends into the joints' gaps, the corner of the
    # floor going into the sides there
    assert _groove(f).shape.bounds == pytest.approx((30.5, 142.75, 569.5, 152.25))
    assert f.box().lo["x"] == 36 and f.box().hi["x"] == 564
    # the slide's cut-outs reach up to the floor's underside, 0.25 above the
    # groove's lower wall
    cuts = {op.name: op.shape.bounds for op in (*f.ops, *k.ops) if isinstance(op, Cut) and op.name
            and op.name.startswith(("coupling", "hook"))}
    assert {b[3] for b in cuts.values()} == {143.0} and floor.bottom.value == 143
