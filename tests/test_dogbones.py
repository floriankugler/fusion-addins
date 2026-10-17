"""Dog bones (`lang.core.dogbones`): the add-in's relief geometry, finding
inside corners, `board.dogbones()` and the half lap's dog bones."""
import json
import math
from pathlib import Path

import pytest
from shapely.geometry import Point, Polygon
from shapely.geometry import box as shapely_box

from lang import *
from lang.build import run_build
from lang.core.dogbones import corner_relief, corners, hidden_relief
from lang.core.layout import build_layout
from lang.core.layout_types import DogBoneLayout
from lang.core.ops import Cut, Pocket
from lang.core.part import DogBoneTarget
from lang.core.scope import registry
from lang.emit.plan import Arc, plan_layout
from helpers import EXAMPLES, has_material, ply15, run_example

R = 3.05                            # a square corner's relief: the 6 mm tool plus 0.1, halved
O = 3 / math.sqrt(2)                # its centre, along each edge from the corner


def _panel() -> tuple[Scope, Board]:
    """A 15 mm panel, 400 deep (x) and 600 wide (y), on the bottom of its box."""
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom).show(m.top)
    return m, panel


def _dogbones(part: Board) -> list[Cut | Pocket]:
    return [op for op in part.ops if isinstance(op, (Cut, Pocket)) and (op.name or "").endswith("dogbones")]


def _centre_radius(shape: Shape) -> tuple[tuple[float, float], float]:
    """A relief's centre and radius: its polygon's vertices lie on the circle."""
    (poly,) = shape.polygons()
    c = (float(poly.centroid.x), float(poly.centroid.y))
    return c, max(math.dist(c, (float(p[0]), float(p[1]))) for p in poly.exterior.coords)


def _single() -> float:
    """The area of one square corner's relief."""
    return corner_relief((0.0, 0.0), (1.0, 0.0), (0.0, 1.0), 6.0, 0.1).area


# -- the geometry ------------------------------------------------------------------------------

def test_a_square_corner_gets_the_add_ins_relief():
    disc = corner_relief((10.0, 20.0), (-1.0, 0.0), (0.0, 1.0), 6.0, 0.1)
    (cx, cy), r = _centre_radius(disc)
    assert (cx, cy) == pytest.approx((10 - O, 20 + O)) and r == pytest.approx(R)
    assert disc.geometry.contains(Point(10 + 0.035, 20 - 0.035))       # 0.05 past the corner on the diagonal
    assert not disc.geometry.contains(Point(10 + 0.04, 20 - 0.04))


@pytest.mark.parametrize("degrees", [30, 60, 120, 150])
def test_other_angles_move_out_by_one_over_the_sine(degrees: int):
    a = math.radians(degrees)
    disc = corner_relief((0.0, 0.0), (1.0, 0.0), (math.cos(a), math.sin(a)), 6.0, 0.1)
    reach = 3 / math.sin(a)
    (cx, cy), r = _centre_radius(disc)
    assert math.hypot(cx, cy) == pytest.approx(reach) and math.atan2(cy, cx) == pytest.approx(a / 2)
    assert r == pytest.approx(reach + 0.05, rel=1e-6)


def test_a_hidden_relief_runs_along_one_edge():
    disc = hidden_relief((0.0, 0.0), (1.0, 0.0), 6.0, 0.1)
    (cx, cy), r = _centre_radius(disc)
    assert (cx, cy) == pytest.approx((R, 0.0)) and r == pytest.approx(R)


# -- finding corners ----------------------------------------------------------------------------

def test_corners_of_the_outline_and_of_cuts_at_any_angle():
    m, panel = _panel()
    with m:
        top = panel.top
        panel.cut(rect(depth=60, width=80), at=top.front.left, name="notch")
        panel.cut(polygon([(60, 0), (0, 20), (60, 40)]), at=top.back.left(150), name="vee")
        panel.cut(rect(depth=80, width=60).clip(back=20, right=20), at=top.center, name="window")
    found = {(round(c.point[0], 6), round(c.point[1], 6)): c for c in corners(panel)}
    assert set(found) == {(60, 80), (340, 170), (160, 270), (240, 270), (160, 330), (220, 330), (240, 310)}
    assert math.degrees(found[(340, 170)].angle) == pytest.approx(2 * math.degrees(math.atan(20 / 60)))
    assert math.degrees(found[(220, 330)].angle) == pytest.approx(135)
    assert all(c.bottom is None and c.outline_cut and set(c.faces) == {"top", "bottom"} for c in found.values())
    assert found[(60, 80)].ops == ("notch",) and found[(60, 80)].on_outline
    assert found[(160, 270)].ops == ("window",) and not found[(160, 270)].on_outline


def test_round_shapes_have_no_corners():
    m, panel = _panel()
    with m:
        top = panel.top
        panel.cut(circle(30), at=top.center)
        panel.cut(rect(depth=60, width=60).rounded(10), at=top.front(20).left(20))
        panel.cut(rect(depth=68, width=12).union(circle(12, (0, 6))).union(circle(12, (68, 6))),
                  at=top.back(20).right(20))
        panel.pocket(rect(depth=40, width=40).rounded(6), at=top.back(20).left(20), depth=5)
        panel.hole(d=10, at=top.front(100).right(100), depth=8)
        # a coarse polygon standing for nothing round: its corners are corners
        panel.cut(polygon([(10, 0), (0, 10), (-10, 0), (0, -10)]), at=top.front(150).left(150))
    found = corners(panel)
    assert len(found) == 4 and all(math.degrees(c.angle) == pytest.approx(90) for c in found)


def test_pockets_are_relieved_as_deep_as_they_are_from_their_face():
    m, panel = _panel()
    with m:
        top, bottom = panel.top, panel.bottom
        panel.pocket(rect(depth=100, width=100), at=top.front(40).left(40), depth=4, name="recess")
        panel.pocket(rect(depth=40, width=40), at=top.front(70).left(70), depth=10, name="well")
        panel.pocket(rect(depth=60, width=40), at=bottom.back(40).right(40), depth=6, name="below")
        panel.pocket(rect(depth=40, width=40), at=top.back(40).left(40), depth=through, name="window")
    by_op = {c.ops[-1]: c for c in corners(panel)}
    assert (by_op["recess"].face, by_op["recess"].top, by_op["recess"].bottom) == ("top", 0, 4)
    assert (by_op["well"].face, by_op["well"].top, by_op["well"].bottom) == ("top", 4, 10)
    assert (by_op["below"].face, by_op["below"].bottom) == ("bottom", 6)
    assert by_op["window"].bottom is None and not by_op["window"].outline_cut
    panel.dogbones()
    build_layout()
    reliefs = {op.name: (op.face, op.depth, op.depth_spec) for op in _dogbones(panel) if isinstance(op, Pocket)}
    assert reliefs == {"recess_dogbones": ("top", 4, "4"), "well_dogbones": ("top", 10, "10"),
                       "below_dogbones": ("bottom", 6, "6"), "window_dogbones": ("top", 15, "through")}
    # four whole circles each: none reaches material that is not its corner's
    assert all(op.shape.area == pytest.approx(4 * _single()) for op in _dogbones(panel))
    assert panel.outline.geometry.area == 400 * 600         # the through pocket and its reliefs are no cuts


def test_a_hole_over_a_corner_leaves_it_alone():
    m, panel = _panel()
    with m:
        top = panel.top
        panel.pocket(rect(depth=120, width=20), at=top.back(60).right(150), depth=5, name="dado")
        panel.hole(d=20, at=top.back(180).right(170), depth=through)
    assert len(corners(panel)) == 3


def test_an_islands_corners_are_not_inside_corners():
    m, panel = _panel()
    with m:
        top = panel.top
        ring = rect(depth=100, width=100).difference(rect(depth=40, width=40).moved(30, 30))
        panel.pocket(ring, at=top.center, depth=5, name="moat")
    # the moat's outer corners only: the island's stick out of its floor
    assert sorted(c.point for c in corners(panel)) == [(150, 250), (150, 350), (250, 250), (250, 350)]


# -- board.dogbones() ----------------------------------------------------------------------------

def test_dogbones_go_into_the_corners_the_board_has_at_the_call():
    """Florian 2026-10-12: dogbones() acts where it is written, like every
    operation: the notch cut before it is relieved at once, the one cut
    after it is not."""
    m, panel = _panel()
    with m:
        panel.cut(rect(depth=60, width=80), at=panel.top.front.left, name="notch")
        panel.dogbones()
        assert [op.name for op in _dogbones(panel)] == ["notch_dogbones"]        # at once
        panel.cut(rect(depth=60, width=80), at=panel.top.back.left, name="later")
        layout = build_layout()
    assert [op.name for op in _dogbones(panel)] == ["notch_dogbones"]
    # through the corner at (60, 80): the relief's centre lies on the diagonal into the notch
    assert has_material(panel, (60.03, 80.03), (60 - O, 80 - O), (61, 82)) == [False, False, True]
    assert has_material(panel, (340 - 0.03, 80 + 0.03)) == [True]               # the later notch's corner stays
    ops = layout["modules"][0]["parts"][0]["ops"]
    assert [op.get("name") for op in ops] == ["notch", "notch_dogbones", "later"]
    build_layout()                                      # the layout adds nothing
    assert len(_dogbones(panel)) == 1
    plan = plan_layout(build_layout())
    assert [round(c.radius, 6) for loop in plan.parts[0].body.loops for c in loop if isinstance(c, Arc)] == [R]


def test_dogbones_relieve_a_joint_made_before_the_call_only():
    with module("grid", Box.from_size(width=600, depth=1000, height=30)) as g:
        cross = board("cross", ply15).center(Pos("x", 200))
        long = board("long", ply15).center(Pos("y", 300))
        long.dogbones()                                 # no corners yet
        assert _dogbones(long) == []
        long.join(cross, using=half_lap(toward=g.top, dogbones=None))
        long.dogbones()
    build_layout()
    assert [op.name for op in _dogbones(long)] == ["lap_cross_dogbones"]
    assert _dogbones(cross) == []
    assert has_material(long, (192.5 - 0.03, 15 - 0.03), (192.5 + O, 15 + O)) == [False, False]


def test_at_names_operations_faces_or_the_outline():
    def build(*at: str) -> list[str]:
        registry.reset()
        m, panel = _panel()
        with m:
            top = panel.top
            panel.cut(rect(depth=60, width=80), at=top.front.left, name="notch")
            panel.cut(rect(depth=40, width=40), at=top.center, name="window")
            panel.pocket(rect(depth=40, width=40), at=top.back(40).left(40), depth=5, name="dado")
            panel.pocket(rect(depth=40, width=40), at=panel.bottom.back(40).right(40), depth=5, name="below")
            named: dict[str, DogBoneTarget] = {"notch": panel.notch, "window": panel.window, "dado": panel.dado,
                                               "outline": panel.outer.outline, "bottom": panel.bottom}
            panel.dogbones(at=[named[a] for a in at])
        build_layout()
        return sorted(op.name or "" for op in _dogbones(panel))

    assert build("window") == ["window_dogbones"]
    assert build("notch", "dado") == ["dado_dogbones", "notch_dogbones"]
    assert build("outline") == ["notch_dogbones"]
    assert build("bottom") == ["below_dogbones", "notch_dogbones", "window_dogbones"]


def test_no_doubles_with_a_joints_own_dog_bones():
    with module("unit", Box.from_size(width=600, depth=300, height=800)) as u:
        left = board("left", ply15).on(u.left)
        right = board("right", ply15).on(u.right)
        low = board("low", ply15).on(Pos("z", 200), toward=u.top).between(left, right)
        high = board("high", ply15).on(Pos("z", 500), toward=u.top).between(left, right)
        low.join(left, right, using=tenons(count=2, width=50))
        high.join(left, right, using=tenons(count=2, width=50, dogbones="hidden"))
        for b in (left, right, low, high):
            b.dogbones()
        # two boards standing on edge, crossing in a half lap above the shelves
        across = board("across", ply15).center(Pos("x", 150)).between(Pos("z", 600), Pos("z", 640), left, right)
        along = board("along", ply15).center(Pos("y", 300)).between(Pos("z", 600), Pos("z", 640))
        across.join(along, using=half_lap(toward=u.top))
        across.dogbones()
        along.dogbones()
    build_layout()
    assert [getattr(op, "name") for op in across.ops] == ["lap_along"]
    assert [getattr(op, "name") for op in along.ops] == ["lap_across"]
    assert all(_dogbones(b) == [] for b in (left, right, low, high, across, along))


def test_a_relief_takes_only_its_own_corners_material():
    m, panel = _panel()
    with m:
        # a deep pocket, and a shallow one half a millimetre beside it,
        # within reach of the deep one's corner reliefs
        panel.pocket(rect(depth=40, width=40), at=panel.top.front(100).left(100), depth=10, name="deep")
        panel.pocket(rect(depth=20, width=50), at=panel.top.front(140.5).left(95), depth=3, name="shallow")
        panel.dogbones(at=panel.deep)
    build_layout()
    (relief,) = _dogbones(panel)
    shallow = shapely_box(140.5, 95, 160.5, 145)
    assert relief.shape.area < 4 * _single() - 0.1
    assert relief.shape.geometry.intersection(shallow).area < 1e-6         # the shallow pocket stays 3 deep
    assert relief.shape.geometry.contains(Point(140.3, 139.5))              # but the web at the corner goes


def test_a_sharp_cutout_gets_dog_bones_in_its_corners():
    m, panel = _panel()
    with m:
        panel.cutout(panel.top, radius=0)
        panel.dogbones()
    build_layout()
    (relief,) = _dogbones(panel)
    assert relief.name == "openings_dogbones" and isinstance(relief, Cut)
    # each relief without the part in the opening: the cutout's check for
    # operations in its opening passes
    lobe = corner_relief((0.0, 0.0), (1.0, 0.0), (0.0, 1.0), 6.0, 0.1).geometry.difference(
        shapely_box(0, 0, 100, 100)).area
    assert relief.shape.area == pytest.approx(4 * lobe)
    assert has_material(panel, (20 - 0.03, 20 - 0.03), (19, 19)) == [False, True]


def test_dogbones_errors():
    m, panel = _panel()
    with m:
        other = board("other", ply15).on(m.top)
        panel.cut(rect(depth=60, width=80), at=panel.top.front.left, name="notch")
        with pytest.raises(LangError, match="tool must be positive"):
            panel.dogbones(tool=0)
        with pytest.raises(LangError, match="relief must not be negative"):
            panel.dogbones(relief=-1)
        with pytest.raises(LangError, match="at= is empty"):
            panel.dogbones(at=[])
        with pytest.raises(LangError, match="narrow face"):
            panel.dogbones(at=panel.front)
        with pytest.raises(LangError, match="not a face of this board"):
            panel.dogbones(at=other.top)
        other.cut(rect(depth=60, width=80), at=other.top.front.left, name="notch")
        with pytest.raises(LangError, match="not an operation of this board"):
            panel.dogbones(at=other.notch)


def test_dogbones_at_takes_operations_not_their_names():
    """Florian 2026-10-12: at= takes the operation itself; a name, alone
    or in a list, is refused, saying what to write instead."""
    m, panel = _panel()
    with m:
        panel.cut(rect(depth=60, width=80), at=panel.top.front.left, name="notch")
        with pytest.raises(LangError, match=r"takes the operation itself, not its name 'notch': write panel\.notch"):
            panel.dogbones(at="notch")  # type: ignore[arg-type]
        with pytest.raises(LangError, match="not its name 'notch'"):
            panel.dogbones(at=[panel.outer.outline, "notch"])  # type: ignore[list-item]
        with pytest.raises(LangError, match="takes operations, big faces or an outline"):
            panel.dogbones(at=[42])  # type: ignore[list-item]
    assert _dogbones(panel) == []


def test_a_relief_that_would_split_the_board_is_an_error():
    m, panel = _panel()
    with m:
        top = panel.top
        # a notch that leaves a strip half a millimetre wide beside it
        panel.cut(rect(depth=60, width=599.5), at=top.front.left, name="notch")
        before = (list(panel.ops), panel.outline.area)
        with pytest.raises(LangError, match="splits the board"):
            panel.dogbones(at=panel.notch)
    assert (panel.ops, panel.outline.area) == before        # none of its reliefs stays


# -- half laps ------------------------------------------------------------------------------------

def _grid() -> tuple[Scope, Board, Board]:
    with module("grid", Box.from_size(width=600, depth=1000, height=30)) as g:
        cross = board("cross", ply15).center(Pos("x", 200))
        long = board("long", ply15).center(Pos("y", 300))
    return g, cross, long


def test_a_half_lap_has_corner_dog_bones_by_default():
    g, cross, long = _grid()
    with g:
        long.join(cross, using=half_lap(toward=g.top))
    # long is notched from the top, 192.5 to 207.5 above z = 15; cross from below, 292.5 to 307.5 under it
    assert has_material(long, (192.5 + O, 15 + O), (192.5 - 0.6, 15 - 0.6), (200, 14)) == [False, True, True]
    assert has_material(long, (207.5 - O, 15 + O), (192.4, 20)) == [False, True]
    assert has_material(cross, (292.5 + O, 15 - O), (307.5 - O, 15 - O), (300, 16)) == [False, False, True]
    notch = long.op("lap_cross").op
    assert isinstance(notch, Cut)
    lobe = corner_relief((0.0, 0.0), (1.0, 0.0), (0.0, 1.0), 6.0, 0.1).geometry.difference(
        shapely_box(0, 0, 100, 100)).area                  # the part outside the notch, at one corner
    assert notch.shape.area == pytest.approx(15 * 16 + 2 * lobe)


def test_hidden_dog_bones_bulge_past_the_floor_and_none_leave_it_square():
    g, cross, long = _grid()
    with g:
        long.join(cross, using=half_lap(toward=g.top, dogbones="hidden"))
    # tangent to the notch's sides, centred on its floor, reaching R below it
    assert has_material(long, (192.5 + R, 15 - R + 0.05), (192.5 + R, 15 - R - 0.05), (192.4, 15.5)) == [False, True, True]
    assert has_material(long, (200, 14.9)) == [True]               # between the two
    registry.reset()
    g, cross, long = _grid()
    with g:
        long.join(cross, using=half_lap(toward=g.top, dogbones=None))
    assert has_material(long, (192.6, 15.1), (192.4, 15.1), (192.6, 14.9)) == [False, True, True]


def test_half_lap_dog_bone_errors():
    g, cross, long = _grid()
    with g:
        with pytest.raises(LangError, match="wider than the notch"):
            long.join(cross, using=half_lap(toward=g.top, dogbones="hidden", tool=16))
        with pytest.raises(LangError, match="would break out of grid.long below its notch"):
            long.join(cross, using=half_lap(toward=g.top, split=g.bottom.into(2), dogbones="hidden"))
    assert long.ops == [] and cross.ops == []
    with g:
        long.join(cross, using=half_lap(toward=g.top, dogbones="hidden", tool=14.9))     # 15 across: just fits
    notch = long.op("lap_cross").op
    assert isinstance(notch, Cut) and notch.shape.bounds[0] == pytest.approx(192.5)       # nothing past the sides
    with pytest.raises(LangError, match="dogbones"):
        half_lap(toward=world_frame().direction("top"), dogbones="square")  # type: ignore[arg-type]
    with pytest.raises(LangError, match="tool must be positive"):
        half_lap(toward=world_frame().direction("top"), tool=0)


# -- the example --------------------------------------------------------------------------------------

def test_the_example_builds_with_every_kind_of_corner(tmp_path: Path):
    layout = run_build(EXAMPLES / "dogbones.py", tmp_path, scene=False)
    assert layout["problems"] == []
    parts = {p["path"]: p for m in layout["modules"] for p in m["parts"]}
    names = [name for op in parts["panels.panel"]["ops"] if (name := op.get("name") or "").endswith("dogbones")]
    assert sorted(names) == sorted(["vee_dogbones", "notch_dogbones", "window_dogbones", "through_dogbones",
                                    "dado_dogbones", "recess_dogbones", "well_dogbones", "below_dogbones"])
    assert [op.get("name") for op in parts["panels.shelf"]["ops"]] == ["cable", "window", "cable_dogbones"]
    json.dumps(layout)


# -- box joints ---------------------------------------------------------------------------------------

def _box_jointed(joint: object) -> tuple[Board, Board]:
    """test_box_joints' corner: a (15 thick, y 0..15) met by b (12 thick,
    x 0..12), b growing the fingers, both asking for dog bones after."""
    with module("pair", Box.from_size(width=200, depth=200, height=150)) as m:
        a = board("a", ply15).on(m.left).between(Pos("x", 0), m.back, m.bottom, m.top)
        b = board("b", sheet_material("birch", t=12)).on(Pos("x", 0), toward=m.back).between(a, m.right)
        b.join(a, using=joint)  # type: ignore[arg-type]
        a.dogbones()
        b.dogbones()
    build_layout()
    return a, b


def test_a_box_joint_keeps_its_fillets_and_gets_no_dog_bones():
    for clearance in ((0.0, 0.0), (0.2, 0.5)):
        registry.reset()
        a, b = _box_jointed(box_joint(5, margin=5, tool=6, clearance=clearance))
        assert _dogbones(a) == [] and _dogbones(b) == []


def test_a_square_box_joint_gets_them():
    a, b = _box_jointed(box_joint(5, margin=5, tool=0))
    # two notches in a and three gaps in b (the outer two open at the board's
    # sides, with one inside corner each), each corner one relief
    assert sorted(op.name or "" for op in _dogbones(a)) == ["notch_b_1_dogbones", "notch_b_2_dogbones"]
    assert sorted(op.name or "" for op in _dogbones(b)) == ["gap_a_1_dogbones", "gap_a_2_dogbones", "gap_a_3_dogbones"]
    assert sum(op.shape.area for op in _dogbones(a)) == pytest.approx(4 * _single())
    assert sum(op.shape.area for op in _dogbones(b)) == pytest.approx(4 * _single())


def test_the_drawer_boxes_relieve_only_their_cut_outs():
    """The floor's grooves come relieved from the groove joint where they
    stop (in the sides) and run out of the front and back, so dog bones
    are left for the slide's cut-outs only."""
    run_example(EXAMPLES / "drawer_cabinet.py")
    boxes = [p for root in registry.roots for p in root.all_parts()
             if ".drawer" in p.path and p.name in ("left", "right", "front", "back")]
    for p in boxes:
        p.dogbones()
    assert build_layout()["problems"] == []
    made = {p.path.split(".")[-1]: sorted(op.name or "" for op in _dogbones(p)) for p in boxes}
    assert made == {"left": [], "right": [],
                    "front": ["coupling_left_dogbones", "coupling_right_dogbones"],
                    "back": ["hook_left_dogbones", "hook_right_dogbones"]}


# -- found by fuzzing ----------------------------------------------------------------------------

def _fuzzed(name: str, size: tuple[float, float], t: float, place: str, origin: tuple[float, float, float],
            features: list[tuple[str, int, float, float, float, float, float, float | None]],
            outline: Shape | None = None) -> tuple[Scope, Board]:
    """A board as the fuzz tests build one (`tests/fuzz/boards.py`): its
    outline `size` from its low corner, then pockets ("pocket", face, u, v,
    a, b, angle, depth fraction or None for through) and cuts ("cut", ...),
    a rectangle a by b turned by angle about (u, v), a circle a across when
    b is 0, named by kind and index; one the language refuses is left out."""
    from shapely import affinity
    u, v = size
    box = {"bottom": Box.from_size(width=v, depth=u, height=100, origin=origin),
           "left": Box.from_size(width=100, depth=u, height=v, origin=origin),
           "back": Box.from_size(width=u, depth=100, height=v, origin=origin)}[place]
    with module(name, box) as m:
        b = board("panel", sheet_material("birch", t=t), outline).on(getattr(m, place))
        u0, v0, _, _ = b.outline.bounds
        for i, (kind, face, fu, fv, a, bb, angle, depth) in enumerate(features):
            p = (u0 + fu, v0 + fv)
            g = Point(p).buffer(a / 2, quad_segs=32) if bb <= 0 else \
                affinity.rotate(shapely_box(p[0] - a / 2, p[1] - bb / 2, p[0] + a / 2, p[1] + bb / 2), angle, origin=p)
            try:
                if kind == "pocket":
                    b.add_pocket(b.big_faces()[face], Shape(g), through if depth is None else max(0.1, depth * t),
                                 f"pocket_{i}")
                else:
                    b.add_cut(Shape(g), f"cut_{i}")
            except LangError:
                pass
    return m, b


def test_dog_bones_with_no_relief_relieve_every_corner():
    """Found by fuzzing: with relief=0 a dog bone's circle runs through its
    corner, and its polygon, drawn on the whole degrees, a hair inside it
    where the corner falls between two of them. The circle's part at the
    corner then touched nothing of the corner's own material, and the
    relief was left out as another's; where it was cut, the corner's tip it
    left, edges under 0.01 mm, counted as a corner again. Every corner is
    relieved, once."""
    m, b = _fuzzed("m", (570, 293), 6, "back", (0, 0, 0), [
        ("cut", 1, 34.16370084795572, 14.0, 35.0, 20.0, 77.0, 0.5),
        ("pocket", 0, 28.0, 250.0, 51.0, 14.973648255725742, 128.63460686845886, None)])
    with m:
        b.dogbones(tool=10.5, relief=0)
    assert corners(b) == []
    assert sorted(op.name or "" for op in _dogbones(b)) == ["cut_0_dogbones", "pocket_1_dogbones"]


def _taper(size: tuple[float, float], r: float) -> Shape:
    u, v = size
    return Shape(Polygon([(0, 0), (u, 0), (u, r), (0, v)]))


def test_dog_bones_come_in_the_order_of_the_operations_wherever_the_board_lies():
    """Found by fuzzing: the reliefs came in the order their corners were
    found, which follows where each ring starts, and that follows the
    board's place in the world: the same board lying elsewhere had them
    in another order. They come in the order of the operations they
    belong to."""
    features: list[tuple[str, int, float, float, float, float, float, float | None]] = [
        ("pocket", 0, 1550.0, 537.3755351993901, 102.89750496278405, 112.66173214154878, 0.0, 0.5),
        ("pocket", 1, 1341.3208821543392, 30.048688607178907, 110.0, 47.0, 45.0, 0.6945524194107097),
        ("cut", 0, 0.0, 58.0, 85.46812652873423, 119.0, 45.0, None),
        ("cut", 1, 14.0, 115.86812070661084, 110.0, 120.0, 0.0, None),
        ("pocket", 0, 1566.9690742404343, 518.0755351993902, 80.49557002503873, 71.0, 0.0, 0.613673301962901)]
    size = (1600.0, 572.5755351993902)
    for place, origin in (("left", (0.0, 0.0, 0.0)), ("back", (-420.0, 13.5, 4000.0))):
        registry.reset()
        m, b = _fuzzed("m", size, 6, place, origin, features, _taper(size, 137.67758347807668))
        with m:
            b.dogbones(tool=6, relief=0)
        assert [op.name for op in _dogbones(b)] == ["pocket_1_dogbones", "cut_2_dogbones", "cut_3_dogbones"], place


def test_a_relief_takes_no_material_held_on_to_its_corner_at_a_point():
    """Found by fuzzing: two pockets from either face of a 6 mm board,
    3 deep, crossing at 45 degrees, go through where they meet; the
    reliefs of that make corners of their own, and the relief of one of
    those met a piece of 7.4 mm2 that touches the corner's material at a
    point only. With the board at the origin shapely made them two pieces;
    1 mm along, one, and the relief took that piece too. A piece held on
    at a point is apart."""
    features: list[tuple[str, int, float, float, float, float, float, float | None]] = [
        ("pocket", 0, 0.0, 0.0, 59.0, 2.0, 45.0, 0.5), ("pocket", 1, 0.0, 40.0, 2.0, 57.0, 45.0, 0.5)]
    areas: list[float] = []
    for origin in ((0.0, 0.0, 0.0), (0.0, 1.0, 0.0)):
        registry.reset()
        m, b = _fuzzed("m", (40.0, 40.0), 6, "bottom", origin, features)
        with m:
            b.dogbones(tool=6, relief=0.1)
            b.dogbones(tool=6, relief=0.1)                 # the corners the first one's reliefs made
        (second,) = [op for op in _dogbones(b) if op.name == "outline_dogbones_dogbones"]
        areas.append(second.shape.geometry.area)
    assert areas[0] == pytest.approx(areas[1], abs=1e-6) and areas[0] == pytest.approx(39.8996, abs=1e-3)


def test_a_wall_of_no_width_where_pockets_from_either_face_meet_is_no_corner():
    """Found by fuzzing: a pocket into the top of a 6 mm board's corner and
    one turned 45 degrees into its bottom, 3 deep each, meet along the
    turned one's edge. The floor of the bottom one, less where they go
    through together, ran along itself there, a wall of no width, which
    the rounding kept at the origin, two 135 degree corners at its ends
    and two more reliefs, and parted 1 mm along. The regions corners are
    found in are opened now, so the wall parts wherever the board lies."""
    features: list[tuple[str, int, float, float, float, float, float, float | None]] = [
        ("pocket", 0, 0.0, 0.0, 2.0, 2.5, 0.0, 0.5), ("pocket", 1, 0.0, 0.0, 3.0, 4.0, 45.0, 0.5)]
    for origin in ((0.0, 0.0, 0.0), (0.0, 1.0, 0.0)):
        registry.reset()
        m, b = _fuzzed("m", (40.0, 40.0), 6, "bottom", origin, features)
        with m:
            b.dogbones(tool=6, relief=0.1)
        assert [op.name for op in _dogbones(b)] == ["pocket_0_dogbones"], origin


def test_a_hairline_spike_two_drawings_of_a_circle_leave_is_no_corner():
    """Found by fuzzing: where a circle pocket overlaps pockets from the
    other face, the regions the corners are found in, made by booleans of
    the circle's two drawings, kept a spike, a ring turning back along
    itself. It counted as a corner, and a dog bone needs a corner, not two
    edges in one line: the second dogbones() was refused. The regions are
    cleaned first, as every shape is."""
    size = (58.0, 80.0)
    features: list[tuple[str, int, float, float, float, float, float, float | None]] = [
        ("pocket", 0, 36.0, 3.0, 55.012957425635086, 65.74747336688866, 45.0, 0.5),
        ("pocket", 1, 20.171108416351803, 70.75689498186713, 116.0, 0.0, 45.0, 0.5),
        ("pocket", 0, 37.5, 79.0, 32.5, 88.5, 0.0, 0.8648160999719844),
        ("pocket", 1, 53.0, 50.0, 6.0, 58.0, 45.0, 0.4007865005434067)]
    for origin in ((0.0, 0.0, 0.0), (-2.0, -2921.771679118425, -2115.0)):
        registry.reset()
        m, b = _fuzzed("m", size, 9, "left", origin, features, _taper(size, 17.60097056214606))
        with m:
            b.dogbones(tool=5, relief=0.1, at=b.pocket_1)
            b.dogbones(tool=5, relief=0.1, at=b.pocket_1)


# -- dog bones marked in the layout, for the CAM plan ------------------------------------------------

def _on_its_shape(rings: list[list[list[float]]], bone: DogBoneLayout) -> float:
    """How much of a shape's boundary runs on the bone's circle (mm)."""
    boundary = Polygon(rings[0]).boundary
    for ring in rings[1:]:
        boundary = boundary.union(Polygon(ring).boundary)
    circle_line = Point(*bone["center"]).buffer(bone["d"] / 2, quad_segs=90).exterior
    return boundary.intersection(circle_line.buffer(1e-3)).length


def test_every_dog_bone_is_marked_with_its_circle_and_tool(tmp_path: Path):
    layout = run_build(EXAMPLES / "dogbones.py", tmp_path, scene=False)
    parts = {p["path"]: p for m in layout["modules"] for p in m["parts"]}
    for path, part in parts.items():
        for op in part["ops"]:
            if op["kind"] != "cut" and op["kind"] != "pocket":
                continue
            name = op["name"] or ""
            bones = op["dogbones"]
            if name.endswith("dogbones"):
                # a dogbones() relief: its shape is its circles, each the add-in's for a 6 mm tool
                assert bones, f"{path}.{name}"
                discs = Polygon()
                for bone in bones:
                    assert bone["tool"] == 6.0 and bone["d"] >= 6.1 - 1e-9
                    discs = discs.union(Point(*bone["center"]).buffer(bone["d"] / 2 + 1e-3, quad_segs=90))
                shape = Polygon(op["shape"][0], op["shape"][1:])
                assert shape.difference(discs).area < 1e-6, f"{path}.{name}"
            elif name.startswith("lap_"):
                assert len(bones) == 2, f"{path}.{name}"           # the notch's two corners at its floor
            else:
                assert bones == [], f"{path}.{name}"
            for bone in bones:
                assert _on_its_shape(op["shape"], bone) > 1.0, f"{path}.{name}: {bone}"     # an arc of its wall


def test_a_square_corners_mark_is_a_tool_and_the_relief_across():
    _, panel = _panel()
    panel.cut(rect(depth=60, width=80), at=panel.top.front.left, name="notch")
    panel.dogbones()
    (relief,) = _dogbones(panel)
    (bone,) = relief.dogbones
    assert bone.d == pytest.approx(6.1) and bone.tool == 6.0
    c, r = _centre_radius(relief.shape)
    assert bone.center == pytest.approx(c, abs=1e-6) and bone.d / 2 == pytest.approx(r)


def test_joints_mark_the_dog_bones_in_their_cuts():
    # tenons: the mortise's four corners, the tenon's two roots
    with module("m", Box.from_size(width=600, depth=300, height=400)) as m:
        side = board("side", ply15).on(m.left)
        shelf = board("shelf", ply15).on(Pos("z", 200), toward=m.top).between(side, m.right)
        shelf.join(side, using=tenons(count=1, width=60))
    build_layout()
    mortise = next(op for op in side.ops if isinstance(op, (Cut, Pocket)) and (op.name or "").startswith("mortise"))
    root = next(op for op in shelf.ops if isinstance(op, Cut) and (op.name or "").endswith("relief"))
    assert len(mortise.dogbones) == 4 and len(root.dogbones) == 2
    assert all(b.tool == 6.0 for b in mortise.dogbones + root.dogbones)
    # box joints: the circles of the reliefs' pockets, a tool across
    registry.reset()
    a, b = _box_jointed(box_joint(5, margin=5, tool=6))
    pockets = [op for op in a.ops + b.ops if isinstance(op, Pocket) and (op.name or "").endswith("_reliefs")]
    assert len(pockets) == 2 and all(len(p.dogbones) == 4 for p in pockets)
    assert all(bone.d == 6.0 and bone.tool == 6.0 for p in pockets for bone in p.dogbones)
