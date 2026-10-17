"""The CAM plan (`lang.cam`): Florian's templates read outside Fusion, the
rules Auto Setup's were lifted from, the opening test, holding and tabs,
and whole nests planned and checked."""
import json
import math
from pathlib import Path

import pytest
from shapely.geometry import LineString, Point, Polygon
from shapely.geometry import box as shapely_box

from lang import *
from lang import cam
from lang.cam import holding, rules, tabbing
from lang.cam.__main__ import main as cam_main
from lang.cam.plan import plan_nest
from lang.cam.plan_types import CAM_VERSION, CamFile, OperationOut, SetupOut
from lang.cam.regions import gets_in, hold, sharp_corners, unreached
from lang.cam.resolve import REPO
from lang.cam.tooling import Registry, evaluate, parse_stem, scan
from lang.cam.verify import verify
from lang.core.dogbones import corner_bone
from lang.core.layout import build_layout
from lang.core.layout_types import Layout
from lang.core.scope import registry
from lang.core.shapes import slot_shape
from lang.nesting.nest import Options, nest_parts
from lang.nesting.nest_types import NestFile
from lang.nesting.workshop import Sheet, Workshop
from helpers import EXAMPLES, carcass, ply9, ply15

TEMPLATES = REPO / "addins-src" / "auto_setup" / "templates"
REGISTRY = scan(TEMPLATES)
FAST = Options(seconds=0.3, saw_seconds=0.05, refill_seconds=0.0)


# -- the templates ----------------------------------------------------------------------------------

def test_every_template_is_read_with_its_tools():
    assert REGISTRY.skipped == ()
    assert sum(len(ts) for ts in REGISTRY.by_kind.values()) == 29
    kontur = {t.stem: t for t in REGISTRY.by_kind["contour"]}
    assert kontur["contour.dc_Kontur 6mm"].tool.diameter == 6 and kontur["contour.dc_Kontur 6mm"].flute == 24
    assert kontur["contour.udc_Kontur 6mm"].flute == 17                    # dc and udc reach differently
    assert kontur["contour.dc_Kontur 6mm"].stepdown == pytest.approx(6.4)
    assert kontur["contour.dc_Kontur 6mm"].number("tabWidth") == 5 and \
        kontur["contour.dc_Kontur 6mm"].number("tabHeight") == 2
    assert kontur["contour.dc_Kontur 6mm"].number("bottomHeight_offset") == pytest.approx(-0.2)
    adaptive = {t.stem: t for t in REGISTRY.by_kind["pocket"]}["pocket.dc.finish_Tasche adaptiv 8mm"]
    assert (adaptive.diameter, adaptive.narrowest, adaptive.adaptive) == (8, 6, True)   # the 6 mm clean-up
    chamfer = REGISTRY.by_kind["chamfer"][0]
    assert chamfer.tool.taper == 45 and chamfer.reach == pytest.approx(3.0)
    assert chamfer.number("chamferTipOffset") == pytest.approx(0.3)
    assert REGISTRY.by_kind["groove"][0].stepdown == pytest.approx(2.0)


def test_a_templates_name_is_its_kind_tags_and_label():
    assert parse_stem("contour.dc.finish_Kontur 6mm") == ("contour", ("dc", "finish"), "Kontur 6mm")
    assert parse_stem("bore_Bohrung 2mm") == ("bore", (), "Bohrung 2mm")
    assert parse_stem("tool_X") is None and parse_stem("contour.xx_X") is None and parse_stem("contour") is None


def test_expressions_are_evaluated_where_plain():
    assert evaluate("6.4mm") == pytest.approx(6.4)
    assert evaluate("(-0.2) * 1mm") == pytest.approx(-0.2)
    assert evaluate("0.125in") == pytest.approx(3.175)
    assert evaluate("'from stock top'") == "from stock top" and evaluate("true") is True
    from lang.cam.tooling import Tool
    tool = Tool("flat end mill", 6.0, 24.0, None, 0.0)
    assert evaluate("Math.min(tool_fluteLength * 0.75; tool_diameter)", tool) == 6.0
    assert evaluate("tool_diameter ", tool) == 6.0
    assert evaluate("holeMode == 'selection-points' ? 'from hole top' : 'from hole bottom'") is None
    assert evaluate("tool_stepdown", tool) is None


def test_a_label_resolves_for_the_cutter_and_the_finishing_pass():
    chosen, notes = REGISTRY.resolve("contour", "Kontur 6mm", False, "udc")
    assert chosen is not None and chosen.stem == "contour.udc_Kontur 6mm" and notes == []
    chosen, notes = REGISTRY.resolve("pocket", "Tasche adaptiv 8mm", False, "dc")
    assert chosen is not None and chosen.stem == "pocket_Tasche adaptiv 8mm"          # untagged: either cutter
    chosen, notes = REGISTRY.resolve("contour", "Kontur 2mm", True, "dc")
    assert chosen is not None and chosen.stem == "contour.finish_Kontur 2mm"
    chosen, notes = REGISTRY.resolve("bore", "Bohrung 6mm", True, "dc")              # no bore with a finish
    assert chosen is not None and chosen.stem == "bore.dc_Bohrung 6mm" and "finishing" in notes[0]


# -- holes (Florian's rules, rules.py) ------------------------------------------------------------------

def _hole(d: float, depth: float, through: bool = False) -> tuple[str, float | None] | None:
    bores = rules.by_diameter(REGISTRY.of("bore", "dc"))
    drills = rules.by_diameter(REGISTRY.of("drill", "dc"))
    choice = rules.hole_choice(d, depth, through, 0.2, bores, drills)
    return None if choice is None else (choice.template.stem, choice.depth_limit)


def test_a_hole_is_bored_with_the_widest_cutter_a_millimetre_smaller():
    assert _hole(10, 5) == ("bore.dc_Bohrung 6mm", None)
    assert _hole(20, 15, through=True) == ("bore.dc_Bohrung 6mm", None)
    assert _hole(5, 10) == ("bore_Bohrung 3.175mm", None)
    assert _hole(3.175, 3) == ("bore_Bohrung 2mm", None)
    assert _hole(4, 15, through=True) == ("bore_Bohrung 2mm", None)          # 3.175 has not a millimetre
    assert _hole(6.5, 15, through=True) == ("bore_Bohrung 3.175mm", None)


def test_a_blind_hole_leaves_no_core_and_a_tight_one_goes_four_deep():
    # 6.5 blind: 3.175 leaves a core (6.5 > 2 x 3.175), so the 6 mm fits without its millimetre, 4 deep
    assert _hole(6.5, 10) == ("bore.dc_Bohrung 6mm", rules.TIGHT_CUT_DEPTH)
    assert _hole(2.5, 8) == ("bore_Bohrung 2mm", rules.TIGHT_CUT_DEPTH)
    assert _hole(2.5, 3) == ("bore_Bohrung 2mm", None)                       # no deeper than 4 anyway


def test_a_hole_no_cutter_fits_is_drilled_four_deep_at_most():
    assert _hole(2, 8) == ("drill_Bohrung exakt 2mm [Deep drilling]", rules.TIGHT_CUT_DEPTH)
    assert _hole(2, 4) == ("drill_Bohrung exakt 2mm [Deep drilling]", None)
    assert _hole(1.5, 4) is None


# -- the opening test ---------------------------------------------------------------------------------

def test_a_cutter_reaches_a_region_but_its_corners_fillets():
    square = shapely_box(0, 0, 50, 50)
    assert unreached(square, 4) == []
    assert [c for c, _a in sharp_corners(square)] == [(50.0, 0.0), (50.0, 50.0), (0.0, 50.0), (0.0, 0.0)]
    triangle = Polygon([(0, 0), (60, 0), (30, 52)])                         # acute corners: fillets too
    assert unreached(triangle, 4) == []


def test_a_passage_narrower_than_the_cutter_is_not_reached():
    channel = shapely_box(0, 0, 50, 50).union(shapely_box(50, 20, 90, 25))   # 5 wide
    (piece,) = unreached(channel, 4)
    assert piece.area == pytest.approx(197, abs=2)
    assert unreached(channel, 1.5875) == []
    assert unreached(shapely_box(0, 0, 4, 30), 4) == [shapely_box(0, 0, 4, 30)] or \
        len(unreached(shapely_box(0, 0, 4, 30), 4)) == 1


def test_a_slot_made_a_tenth_wider_takes_its_cutter():
    assert unreached(slot_shape((0, 0), (30, 0), 6.1).geometry, 3) == []
    assert unreached(slot_shape((0, 0), (30, 0), 6.0).geometry, 3) != []
    assert unreached(slot_shape((0, 0), (30, 0), 4.0).geometry, 1.5875) == []


def test_a_rounded_corner_tighter_than_the_pockets_cutter_is_not_reached_but_a_contour_follows_its_own():
    rounded = rect(depth=40, width=40).rounded(3).geometry
    assert len(unreached(rounded, 3)) == 4 and unreached(rounded, 1.5875) == []
    assert unreached(rounded, 3, clearance=0.0) == []                        # a box joint's fillet
    assert not gets_in(shapely_box(0, 0, 6.05, 40), 3) and gets_in(shapely_box(0, 0, 6.15, 40), 3)


def test_dog_bones_are_excused():
    bone = corner_bone((0.0, 0.0), (1.0, 0.0), (0.0, 1.0), 6.0, 0.1)
    region = shapely_box(0, 0, 50, 50).union(bone.shape.geometry)
    assert len(unreached(region, 4)) == 1
    assert unreached(region, 4, bone.shape.geometry.buffer(0.01)) == []


# -- pockets, contours, dog bones, the V-bit ---------------------------------------------------------------

def _pocket(region: object, depth: float = 5.0, label: str = "Tasche adaptiv 8mm", finish: bool = False,
            excused: object = None) -> rules.PocketPlan:
    tried, _notes = rules.candidates(REGISTRY, "pocket", label, finish, "dc")
    return rules.pocket_cutters(region, depth, tried, excused)  # pyright: ignore[reportArgumentType]


def test_a_pocket_takes_the_widest_cutter_that_reaches_all_of_it():
    big = _pocket(shapely_box(0, 0, 200, 100))
    assert big.main is not None and big.main.stem == "pocket_Tasche adaptiv 8mm" and not big.rests
    small = _pocket(shapely_box(0, 0, 40, 40))                              # too small for adaptive clearing
    assert small.main is not None and small.main.stem == "pocket.dc_Tasche 6mm"
    # the 8 mm adaptive rougher takes larger pockets only, never a groove or a slot [Florian, 2026-10-17]
    groove = _pocket(shapely_box(0, 0, 9.4, 400))
    assert groove.main is not None and groove.main.stem == "pocket.dc_Tasche 6mm"
    narrow = _pocket(shapely_box(0, 0, 15.9, 400))
    assert narrow.main is not None and narrow.main.stem == "pocket.dc_Tasche 6mm"
    wide = _pocket(shapely_box(0, 0, 16.5, 400))
    assert wide.main is not None and wide.main.stem == "pocket_Tasche adaptiv 8mm"
    domino = _pocket(slot_shape((0, 0), (20, 0), 4.0).geometry, 10.5)
    assert domino.main is not None and domino.main.stem == "pocket_Tasche 3.175mm"
    rounded = _pocket(rect(depth=40, width=40).rounded(3).geometry)        # too small for adaptive clearing
    assert rounded.main is not None and rounded.main.diameter == 6         # its corners need a 3.05 radius
    assert [t.diameter for t, _p in rounded.rests] == [3.175] * 4


def test_what_no_template_reaches_whole_goes_to_a_narrower_one_as_a_rest():
    region = shapely_box(0, 0, 200, 100).union(shapely_box(200, 40, 260, 42.5))    # a 2.5 mm channel
    plan = _pocket(region)
    assert plan.main is not None and plan.main.stem == "pocket_Tasche adaptiv 8mm"
    assert [t.diameter for t, _p in plan.rests] == [2.0] and not plan.unreached
    region = shapely_box(0, 0, 200, 100).union(shapely_box(200, 40, 260, 44))       # 4 wide: the 3.175 rest
    plan = _pocket(region)
    assert plan.main is not None and plan.main.diameter == 8
    assert [t.diameter for t, _p in plan.rests] == [3.175] and not plan.unreached
    region = shapely_box(0, 0, 200, 100).union(shapely_box(200, 40, 260, 42))       # 2 wide: no cutter
    plan = _pocket(region)
    assert plan.main is not None and not plan.rests and len(plan.unreached) == 1
    rounded = _pocket(rect(depth=200, width=200).rounded(3).geometry)               # rests in the corners
    assert rounded.main is not None and rounded.main.diameter == 8
    assert [t.diameter for t, _p in rounded.rests] == [3.175] * 4


def test_an_adaptive_pocket_needs_its_flute_and_its_area():
    deep = _pocket(shapely_box(0, 0, 200, 100), depth=23)
    assert deep.main is not None and deep.main.stem == "pocket.dc_Tasche 6mm"      # 8 mm flute is 22


def test_a_contour_takes_the_cutter_that_reaches_it_and_cuts_through():
    tried, _ = rules.candidates(REGISTRY, "contour", "Kontur 6mm", False, "dc")
    waste = shapely_box(-30, -30, 130, 130).difference(shapely_box(0, 0, 100, 100).difference(
        shapely_box(40, 90, 44, 100)))                                       # a 4 wide notch in the part
    t, notes = rules.contour_cutter(waste, 15.2, tried)
    assert t is not None and t.diameter == 3.175 and notes == []
    t, notes = rules.contour_cutter(shapely_box(-30, -30, 130, 130).difference(shapely_box(0, 0, 100, 100)), 15.2,
                                    tried)
    assert t is not None and t.stem == "contour.dc_Kontur 6mm"
    tried, _ = rules.candidates(REGISTRY, "contour", "Kontur 6mm", False, "udc")
    t, notes = rules.contour_cutter(shapely_box(-30, -30, 130, 130).difference(shapely_box(0, 0, 100, 100)), 18.2,
                                    tried)
    assert t is not None and t.flute == 17 and "flute" in notes[0]          # an 18 mm board: the udc is short


def test_a_dog_bone_goes_to_its_own_cutter_else_a_drill_or_a_dog_bone_cutter():
    drills = rules.by_diameter(REGISTRY.of("drill", "dc"))
    dogbones = REGISTRY.of("dogbone", "dc")
    assert rules.self_cut(6.1, 6.0) and rules.self_cut(6.0, 6.0) and not rules.self_cut(6.1, 8.0)
    picked = rules.dogbone_route(6.1, drills, dogbones)
    assert picked is not None and picked.stem == "dogbone_Dogbone 3.175mm"
    picked = rules.dogbone_route(3.175, drills, dogbones)
    assert picked is not None and picked.kind == "drill" and picked.diameter == 3.175
    picked = rules.dogbone_route(3.0, drills, dogbones)
    assert picked is not None and picked.stem == "dogbone_Dogbone 2mm"
    assert rules.dogbone_route(1.9, drills, dogbones) is None


def test_the_v_bit_cuts_chamfers_that_fit_and_grooves_in_passes():
    chamfer, notes = rules.v_bit(REGISTRY, "chamfer", "dc", None)
    assert chamfer is not None and notes == []
    assert rules.chamfer_fits(1.0, None, chamfer) == (True, [])
    assert rules.chamfer_fits(2.2, 2.0, chamfer)[0]                          # a 4 mm hole's rim: room for the tip
    assert not rules.chamfer_fits(1.0, 0.35, chamfer)[0]
    assert "flank" in rules.chamfer_fits(2.9, None, chamfer)[1][0]
    groove, _ = rules.v_bit(REGISTRY, "groove", "dc", None)
    assert groove is not None
    assert [rules.groove_passes(d, groove) for d in (1.0, 2.0, 2.5, 4.0)] == [1, 1, 2, 2]


# -- holding --------------------------------------------------------------------------------------------

def test_a_part_needs_tabs_where_its_footprint_shrunk_by_the_margin_holds_too_little():
    # Florian's held cases keep more than 10 cm2 at 6 mm, the smaller ones less (proposals/cam.md)
    assert hold(shapely_box(0, 0, 300, 20), 6) == pytest.approx(23.04)
    assert hold(Point(0, 0).buffer(30, quad_segs=90), 6) == pytest.approx(18.1, abs=0.1)
    assert not holding.needs_tabs(shapely_box(0, 0, 300, 20), 6, 10)
    assert not holding.needs_tabs(Point(0, 0).buffer(30, quad_segs=90), 6, 10)
    assert holding.needs_tabs(shapely_box(0, 0, 300, 15), 6, 10)
    assert holding.needs_tabs(Point(0, 0).buffer(22, quad_segs=90), 6, 10)
    assert holding.needs_tabs(shapely_box(0, 0, 900, 11), 6, 10)          # narrower than twice the margin


def test_the_release_order_is_smallest_hold_first_ties_by_travel():
    order = holding.release_order([("big", 900.0, (10.0, 10.0)), ("b", 5.0, (500.0, 0.0)), ("a", 5.0, (100.0, 0.0)),
                                   ("c", 20.0, (0.0, 0.0))])
    assert order == ["a", "b", "c", "big"]


def test_tabs_go_on_straight_stretches_spread_and_off_what_is_excluded():
    ring = [[0.0, 0.0], [300.0, 0.0], [300.0, 15.0], [0.0, 15.0]]
    positions, want = tabbing.place(ring, 5.0, 3, (150.0, 7.5), lambda p: 1.0)
    assert want == tabbing.tab_count(630, 3) and len(positions) == want
    line = LineString(ring + ring[:1])
    assert all(line.distance(Point(p)) < 1e-9 for p in positions)
    assert all(min(math.dist(p, c) for c in [(0, 0), (300, 0), (300, 15), (0, 15)]) >= 5 - 1e-9 for p in positions)
    xs = sorted(p[0] for p in positions)
    assert xs[0] < 60 and xs[-1] > 240                                    # spread along the strip
    # only the top edge allowed: all there
    positions, _ = tabbing.place(ring, 5.0, 3, (150.0, 7.5), lambda p: 1.0 if p[1] > 14 else 0.0)
    assert positions and all(p[1] == pytest.approx(15) for p in positions)
    # a concave corner keeps three tab widths
    ell = [[0.0, 0.0], [100.0, 0.0], [100.0, 40.0], [40.0, 40.0], [40.0, 100.0], [0.0, 100.0]]
    sites = tabbing.Contour(ell).sites(5.0)
    assert all(math.dist(p, (40.0, 40.0)) >= 15 - 1e-9 for _s, p in sites)


# -- whole nests ---------------------------------------------------------------------------------------------

def _nested(workshop: Workshop | None = None) -> tuple[NestFile, Layout]:
    layout = build_layout()
    workshop = workshop or Workshop(bed=(2000.0, 1000.0), sheets=(Sheet("birch 15", 2500, 1250),
                                                                    Sheet("birch 9", 2500, 1250)))
    nest, _parts = nest_parts(layout, None, workshop, name="m.birch_15", options=FAST)
    return nest, layout


def _plan(nest: NestFile, layout: Layout) -> CamFile:
    plan = plan_nest(nest, layout, registry=REGISTRY)
    assert verify(plan, nest, layout, REGISTRY) == []
    assert json.loads(json.dumps(plan)) == plan
    return plan


def _ops(setup: SetupOut, kind: str) -> list[OperationOut]:
    return [op for op in setup["operations"] if op["kind"] == kind]


def _panel() -> Board:
    """A 600 by 400 panel with an operation of every kind on its top."""
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        with board("panel", ply15).on(m.bottom).show(m.top) as p:
            top = p.top
            p.hole(d=10, at=top.front(50).left(50), depth=5, name="blind")
            p.hole(d=20, at=top.front(50).left(150), depth=through, name="bolt", chamfer=1)
            p.hole(d=2, at=top.front(50).left(250), depth=8, name="pilot")
            p.hole(d=40, at=top.back(100).left(100), depth=through, name="big")
            p.pocket(rect(depth=120, width=20), at=top.front(150).left(300), depth=5, name="dado")
            p.slot(4, at=top.front(150).left(450), centers=20, along="depth", depth=10, name="domino")
            p.cut(rect(depth=150, width=150), at=top.back(60).right(60), name="window")
            p.cut(rect(depth=60, width=10), at=top.back(150).left(250), name="slit")
            p.add_vgroove(top, (300.0, 100.0), (300.0, 300.0), 1.0, name="mark")
            p.chamfer(top.outline, 1)
            p.hole(d=5, depth=8, at=p.bottom.front(200).left(50), name="under")
            p.hole(d=8, depth=20, at=p.front.left(300), name="edge")
            p.dogbones(at=p.window)
    return p


def test_a_panel_is_planned_with_every_operation_or_why_not():
    panel = _panel()
    nest, layout = _nested()
    plan = _plan(nest, layout)
    assert plan["version"] == CAM_VERSION and plan["nest"] == nest["name"]
    assert plan["layout_hash"] == nest["layout_hash"] and plan["nest_written"] == nest["written"]
    (setup,) = plan["setups"]
    blank = nest["materials"][0]["sheets"][0]["blanks"][0]
    assert setup["name"] == f"m.birch_15 birch 15 {blank['name']}"
    names = [op["name"] for op in setup["operations"]]
    kinds = [op["kind"] for op in setup["operations"]]
    # by tool widest first, the V-bit, then the release last
    assert kinds[-1] == "release" and "chamfer" in kinds and kinds.index("chamfer") < kinds.index("release")
    assert kinds.index("groove") > kinds.index("chamfer")
    bores = _ops(setup, "bore")
    assert {(op["template"], f["d"], f["depth"]) for op in bores for f in op["features"] if f["what"] == "hole"} == {
        ("bore.dc_Bohrung 6mm", 10.0, 5.0), ("bore.dc_Bohrung 6mm", 20.0, None)}
    (drill,) = _ops(setup, "drill")
    assert drill["params"]["bottom"] == {"mode": "from stock top", "offset": -4.0}
    # holes count from the stock's top, a chamfered one too; its chamfer is the V-bit's
    assert all(op["params"]["top"] == {"mode": "from stock top", "offset": 0.0} for op in bores)
    (chamfers,) = _ops(setup, "chamfer")
    assert sorted(f["ops"][0]["name"] or f["ops"][0]["kind"] for f in chamfers["features"]) == ["bolt", "chamfer"]
    # the domino slot is a pocket with a cutter narrower than it, never a dog bone
    pockets = {r["name"]: op["template"] for op in _ops(setup, "pocket") for f in op["features"] for r in f["ops"]
               if r["name"]}
    assert pockets["domino"] == "pocket_Tasche 3.175mm" and pockets["dado"] == "pocket.dc_Tasche 6mm"
    # the 40 mm hole's waste and the slit are taken out whole, the window is released
    assert pockets["big"] and pockets["slit"]
    (rough,) = _ops(setup, "contour")
    assert sorted((f["what"], sorted({r["name"] for r in f["ops"] if r["name"]})) for f in rough["features"]) == [
        ("inner", ["window", "window_dogbones"]), ("outer", [])]
    inner = next(f for f in rough["features"] if f["what"] == "inner")
    assert sorted(r["aspect"] for r in inner["ops"] if r["name"] == "window_dogbones") == [
        "op", "relief 0", "relief 1", "relief 2", "relief 3"]
    assert rough["params"]["bottom"] == {"mode": "from stock bottom", "offset": 0.2}
    (release,) = _ops(setup, "release")
    assert release["params"]["top"] == {"mode": "from stock bottom", "offset": 0.2}
    assert release["params"]["bottom"] == {"mode": "from stock bottom", "offset": -0.2}
    assert release["params"]["preserve_order"] and release["params"]["multiple_depths"] is False
    assert [r["what"] for r in setup["release_order"]] == ["inner", "outer"]
    # the dog bones the window has are the contour's own (6.1 across, a 6 mm cutter)
    assert not _ops(setup, "dogbone")
    left = {(lo["op"]["name"], lo["why"]) for lo in setup["left_out"]}
    assert left == {("under", "other face"), ("edge", "narrow face")}
    assert names == [op["name"] for op in setup["operations"]]
    assert panel.path == "m.panel"


def test_a_small_part_gets_tabs_on_both_its_operations_unless_it_says_none():
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        board("strip", ply15).on(m.bottom).between(m.front, Pos("x", 15), m.left, Pos("y", 300))
        board("big", ply15).on(m.bottom).between(Pos("x", 100), m.back, m.left, m.right)
    nest, layout = _nested()
    (setup,) = _plan(nest, layout)["setups"]
    parts = {p["path"]: p for p in setup["parts"]}
    assert parts["m.strip"]["tabs"] >= 3 and parts["m.big"]["tabs"] == 0
    assert parts["m.strip"]["hold"] < 10 < parts["m.big"]["hold"]
    tabbed = [op for op in setup["operations"] if op["params"]["tabs"] is not None]
    assert sorted(op["kind"] for op in tabbed) == ["contour", "release"]
    assert all(len(op["params"]["tabs"]["positions"]) == parts["m.strip"]["tabs"] for op in tabbed)   # pyright: ignore[reportOptionalSubscript]
    assert [r["part"] for r in setup["release_order"]] == ["m.strip", "m.big"]   # smallest hold first
    # the tabbed release runs first, in an operation of its own
    releases = _ops(setup, "release")
    assert [op["params"]["tabs"] is not None for op in releases] == [True, False]

    registry.reset()
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        board("strip", ply15).on(m.bottom).between(m.front, Pos("x", 15), m.left, Pos("y", 300)).use(cam.tabs("none"))
        board("big", ply15).on(m.bottom).between(Pos("x", 100), m.back, m.left, m.right).use(cam.tabs("forced"))
    nest, layout = _nested()
    (setup,) = _plan(nest, layout)["setups"]
    parts = {p["path"]: p for p in setup["parts"]}
    assert parts["m.strip"]["tabs"] == 0 and parts["m.big"]["tabs"] >= 3


def test_no_tab_under_a_chamfer():
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        strip = board("strip", ply15).on(m.bottom).between(m.front, Pos("x", 15), m.left, Pos("y", 300))
        strip.chamfer(strip.top.outline, 1)
    nest, layout = _nested()
    (setup,) = _plan(nest, layout)["setups"]
    assert setup["parts"][0]["tabs"] == 0 and any("tab(s) of the 3" in p for p in setup["problems"])


def test_the_settings_are_read_per_part_and_for_the_nest():
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        use(cam.cutter("udc"), cam.breakthrough(0.3))
        a = board("a", ply15).on(m.bottom).between(m.front, Pos("x", 150), m.left, m.right)
        b = board("b", ply15).on(m.bottom).between(Pos("x", 200), m.back, m.left, m.right)
        b.use(cam.contour_template("Kontur 3.175mm"))
        a.hole(d=10, at=a.top.center, depth=through, name="h")
        a.op_settings("h").use(cam.bore_template("Bohrung 3.175mm"))
    nest, layout = _nested()
    plan = _plan(nest, layout)
    (setup,) = plan["setups"]
    assert plan["settings"]["values"]["cam.cutter"] == "udc" and plan["settings"]["sources"]["cam.cutter"] == "m"
    assert plan["settings"]["values"]["cam.breakthrough"] == 0.3
    assert plan["settings"]["parts"]["m.b"]["cam.contour_template"]["value"] == "Kontur 3.175mm"
    contours = {f["part"]: op["template"] for op in _ops(setup, "contour") for f in op["features"]}
    assert contours == {"m.a": "contour.udc_Kontur 6mm", "m.b": "contour_Kontur 3.175mm"}
    (bore,) = _ops(setup, "bore")
    assert bore["template"] == "bore_Bohrung 3.175mm"                       # the hole's own setting
    assert all(op["params"]["bottom"]["offset"] == -0.3 for op in _ops(setup, "release"))


def test_parts_that_disagree_on_a_key_the_nest_takes_one_of_are_refused():
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        board("a", ply15).on(m.bottom).between(m.front, Pos("x", 150), m.left, m.right).use(cam.skin(0.3))
        board("b", ply15).on(m.bottom).between(Pos("x", 200), m.back, m.left, m.right)
    nest, layout = _nested()
    with pytest.raises(LangError, match="two values of cam.skin"):
        plan_nest(nest, layout, registry=REGISTRY)


def test_an_own_blank_has_its_operations_planned_and_its_outline_left_to_hand_work():
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        floor = board("floor", ply15).on(m.bottom).nest(False)
        floor.hole(d=10, at=floor.top.center, depth=5, name="h")
        floor.cut(rect(depth=60, width=60), at=floor.top.front.left, name="notch")
        m.nest("floor", [floor])
    layout = build_layout()
    workshop = Workshop(bed=(2000.0, 1000.0), sheets=(Sheet("birch 15", 2500, 1250),))
    nest, _ = nest_parts(layout, ["m.floor"], workshop, name="m.floor", options=FAST)
    (setup,) = _plan(nest, layout)["setups"]
    assert setup["stock"]["own_blank"]
    assert [op["kind"] for op in setup["operations"]] == ["bore"]
    assert {(lo["op"]["kind"], lo["why"]) for lo in setup["left_out"]} == {("outline", "hand work"),
                                                                            ("cut", "hand work")}


def test_a_plan_of_a_layout_written_before_the_dog_bones_were_marked_is_refused():
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        board("a", ply15).on(m.bottom)
    nest, layout = _nested()
    old = dict(layout)
    old["version"] = 8
    with pytest.raises(ValueError, match="version 8"):
        plan_nest(nest, old, registry=REGISTRY)  # pyright: ignore[reportArgumentType]


# -- the command ---------------------------------------------------------------------------------------------

def test_the_command_plans_the_nests_of_a_build(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    from lang.nesting.__main__ import main as nest_main
    out = tmp_path / "out"
    assert nest_main([str(EXAMPLES / "operations.py"), "--out", str(out)]) == 0
    capsys.readouterr()
    assert cam_main([str(EXAMPLES / "operations.py"), "--out", str(out)]) == 0
    printed = capsys.readouterr().out
    (file,) = list(out.rglob("cam.json"))
    plan = json.loads(file.read_text())
    assert plan["version"] == CAM_VERSION and plan["settings"]["read_from"] == "build"
    assert "planned ->" in printed and "release" in printed
    assert not [p for p in plan["problems"] if p.startswith("check:")]
    assert cam_main([str(EXAMPLES / "operations.py"), "--out", str(out), "nothing.here"]) == 1


def test_the_examples_nests_are_planned_and_check_clean():
    from lang.build import layout_of
    from lang.nesting.nest import nest_layout
    from lang.nesting.resolve import nests_of
    checked = 0
    for name in ("drawer_cabinet", "dogbones", "cutouts", "hatch", "door_latch"):
        layout = layout_of(EXAMPLES / f"{name}.py")
        for n in nests_of(layout):
            if not n["parts"]:
                continue
            nest, _ = nest_layout(layout, n["path"], options=FAST)
            plan = plan_nest(nest, layout, registry=REGISTRY)
            assert verify(plan, nest, layout, REGISTRY) == [], n["path"]
            checked += len(plan["setups"])
    assert checked >= 10


def test_ply9_floors_get_their_v_grooves_in_one_pass():
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        floor = board("floor", ply9).on(m.bottom)
        floor.add_vgroove(floor.top, (100.0, 50.0), (100.0, 350.0), 1.5)
        floor.add_vgroove(floor.top, (200.0, 50.0), (200.0, 350.0), 3.0)
    nest, layout = _nested(Workshop(bed=(2000.0, 1000.0), sheets=(Sheet("birch 9", 2500, 1250),)))
    (setup,) = _plan(nest, layout)["setups"]
    grooves = _ops(setup, "groove")
    assert [(op["params"]["stepdowns"], len(op["features"])) for op in grooves] == [(0, 1), (1, 1)]
    assert Registry is not None


def test_the_cam_keys_are_not_shadowed_by_the_package_s_modules():
    """Importing a submodule of `lang.cam` sets an attribute of the package:
    a module named like a key would replace it (`templates`, `tabs`)."""
    import importlib
    import pkgutil

    import lang.cam as package
    from lang.cam.keys import KEYS
    for info in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"lang.cam.{info.name}")
    for key in KEYS:
        assert getattr(package, key.name.split(".", 1)[1]) is key
    import lang
    assert lang.cam is package and "cam" in lang.__all__


# -- found by fuzzing (tests/fuzz/machining.py) ------------------------------------------------------

def test_tabs_on_an_arc_lie_on_the_rings_polygon():
    """A tab site on an arc lay on the true circle, a hair off the ring's
    polygon the emitter draws the arc through [found by fuzzing, 2026-10-17]."""
    from lang.core.cutouts import circle_geometry
    ring = [[float(x), float(y)] for x, y in list(circle_geometry((0.0, 0.0), 30.0).exterior.coords)[:-1]]
    positions, _ = tabbing.place(ring, 5.0, 3, (0.0, 0.0), lambda p: 1.0)
    line = LineString(ring + ring[:1])
    assert len(positions) >= 3 and all(line.distance(Point(p)) < 1e-9 for p in positions)


def test_a_piece_of_a_pocket_no_cutter_gets_into_is_left_out_alone():
    """A pocket of two pieces, one too narrow for every cutter, was both
    planned and left out [found by fuzzing, 2026-10-17]."""
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        p = board("panel", ply15).on(m.bottom)
        u0, v0, _u1, _v1 = p.outline.bounds
        two = shapely_box(u0 + 50, v0 + 50, u0 + 90, v0 + 90).union(shapely_box(u0 + 150, v0 + 50, u0 + 151.8, v0 + 90))
        p.add_pocket(p.top, Shape(two), 5, "two")
    nest, layout = _nested()
    (setup,) = _plan(nest, layout)["setups"]
    assert [(lo["op"]["aspect"], lo["why"]) for lo in setup["left_out"] if lo["op"]["name"] == "two"] == [
        ("piece 1", "nothing fits")]
    assert any(r["name"] == "two" for op in _ops(setup, "pocket") for f in op["features"] for r in f["ops"])


def test_a_wide_blind_hole_over_the_edge_is_pocketed_where_the_part_is():
    """A blind hole wider than twice the widest bore cutter, over the
    board's edge, was pocketed as the whole circle, off the part
    [found by fuzzing, 2026-10-17]."""
    from lang.cam.regions import Placed, polygons
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        p = board("panel", ply15).on(m.bottom)
        u0, v0, _u1, _v1 = p.outline.bounds
        p.add_hole(p.top, (u0 + 100, v0), 40, 5, "edge")
    nest, layout = _nested()
    (setup,) = _plan(nest, layout)["setups"]
    (feature,) = [f for op in _ops(setup, "pocket") for f in op["features"] if f["what"] == "pocket"]
    placed = nest["materials"][0]["sheets"][0]["blanks"][0]["parts"][0]
    part = layout["modules"][0]["parts"][0]
    outline = Placed.of(part, placed["transform"], layout["frame"]).footprint()
    region = polygons(feature["rings"])[0]
    assert region.difference(outline.buffer(1e-6)).area < 1e-6 and region.area < math.pi * 20 ** 2 / 2 + 1


def test_an_own_blanks_opening_is_taken_out_whole():
    """A `nest(False)` board's opening whose waste survives the cut was
    handed to the release, which an own blank has not, and was lost
    [found by fuzzing, 2026-10-17]."""
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        floor = board("floor", ply15).on(m.bottom).nest(False)
        floor.pocket(rect(depth=120, width=120), at=floor.top.center, depth=through, name="hatch")
        m.nest("floor", [floor])
    layout = build_layout()
    workshop = Workshop(bed=(2000.0, 1000.0), sheets=(Sheet("birch 15", 2500, 1250),))
    nest, _ = nest_parts(layout, ["m.floor"], workshop, name="m.floor", options=FAST)
    (setup,) = _plan(nest, layout)["setups"]
    (pocket,) = _ops(setup, "pocket")
    assert pocket["params"]["bottom"]["mode"] == "from stock bottom" and not _ops(setup, "release")
    assert any(r["name"] == "hatch" for f in pocket["features"] for r in f["ops"])


def test_a_chamfer_along_the_outline_follows_the_faces_outer_loop():
    """A chamfer along the outline followed the layout's outline where a
    through pocket crosses the edge, off the board; the face's outer loop
    is the outline less its openings [found by fuzzing, 2026-10-17]."""
    from lang.cam.regions import Placed
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        p = board("panel", ply15).on(m.bottom)
        p.pocket(rect(depth=80, width=60), at=p.top.front.left(100), depth=through, name="bite")
        p.chamfer(p.top.outline, 1)
    nest, layout = _nested()
    (setup,) = _plan(nest, layout)["setups"]
    (chamfers,) = _ops(setup, "chamfer")
    (feature,) = [f for f in chamfers["features"] if f["what"] == "chamfer" and f["ops"][0]["kind"] == "chamfer"]
    placed = nest["materials"][0]["sheets"][0]["blanks"][0]["parts"][0]
    loop = Placed.of(layout["modules"][0]["parts"][0], placed["transform"], layout["frame"]).machine_outline(30.0)
    rim = loop.exterior.buffer(1e-6)
    assert all(LineString(path["points"]).difference(rim).length < 1e-6 for path in feature["paths"])


def test_two_tabbed_parts_keep_their_own_tabs_on_both_operations():
    """Two tabbed parts in one roughing operation shared one list of
    positions, so the release got each part's tabs twice [found by the
    plan's check on the van, 2026-10-17]."""
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        board("a", ply15).on(m.bottom).between(m.front, Pos("x", 15), m.left, Pos("y", 300))
        board("b", ply15).on(m.bottom).between(Pos("x", 100), Pos("x", 115), m.left, Pos("y", 300))
    nest, layout = _nested()
    (setup,) = _plan(nest, layout)["setups"]
    tabs = sum(p["tabs"] for p in setup["parts"])
    assert tabs >= 6
    for kind in ("contour", "release"):
        (op,) = [op for op in _ops(setup, kind) if op["params"]["tabs"] is not None]
        assert len(op["params"]["tabs"]["positions"]) == tabs           # pyright: ignore[reportOptionalSubscript]


def test_a_corner_of_next_to_no_angle_is_judged_without_failing():
    """A corner of next to no angle reached infinitely far: shapely refused
    the buffer [found by fuzzing, 2026-10-17]; a fillet's reach is now
    where the cutter touches the sides."""
    needle = Polygon([(0, 0), (100, 0), (100, 1e-6)])
    assert unreached(shapely_box(0, -50, 50, 50).union(needle.buffer(0)), 3.0) == []


def test_a_fillet_between_a_line_and_an_arc_is_no_rest():
    """A Cabineo's access hole over the board's edge, a round pocket the
    edge cuts, met it at a corner between a line and an arc; the fillet the
    6 mm cutter leaves there reaches 3.06 from it, beyond the tangent points
    of two lines (1.81), and was sent to the 2 mm cutter as a rest
    [found by the coordinating session's review, 2026-10-17]."""
    cab, p = carcass(back=False)
    with cab:
        p["top"].join(p["left"], p["right"], using=cabineo(count=2))
    nest, layout = _nested()
    plan = _plan(nest, layout)
    rests = [f for s in plan["setups"] for op in s["operations"] for f in op["features"] if f["what"] == "rest"]
    holes = [f for s in plan["setups"] for op in _ops(s, "pocket") for f in op["features"]
             if any((r["name"] or "").startswith("cabineo") for r in f["ops"])]
    assert holes and rests == []
    assert all(op["template"] == "pocket.dc_Tasche 6mm" for s in plan["setups"] for op in _ops(s, "pocket"))
    # its three overlapping access holes are one pocket, as their floor is one face
    assert len(holes) == 4 and all(sorted((r["name"] or "")[-1] for r in f["ops"]) == ["a", "b", "c"] for f in holes)


def test_what_any_cutter_leaves_in_a_corner_is_excused_but_a_passage_is_not():
    from lang.core.dogbones import corner_bone
    line_arc = Point(0, 3.6).buffer(7.5, quad_segs=90).intersection(shapely_box(-10, 0, 10, 20))   # a Cabineo hole
    assert unreached(line_arc, 3.0) == []
    chamfered = Polygon([(1, 0), (50, 0), (50, 50), (0, 50), (0, 1)])                            # a corner cut off
    assert unreached(chamfered, 4) == []
    channel = shapely_box(0, 0, 50, 50).union(shapely_box(50, 20, 90, 25))
    notch = shapely_box(0, 0, 50, 50).union(shapely_box(50, 20, 54, 25))
    assert len(unreached(channel, 4)) == 1 and len(unreached(notch, 4)) == 1
    assert len(unreached(rect(depth=40, width=40).rounded(3).geometry, 3)) == 4                   # tighter than it
    relieved = shapely_box(0, 0, 50, 50).union(corner_bone((0.0, 0.0), (1.0, 0.0), (0.0, 1.0), 6.0, 0.1).shape.geometry)
    assert len(unreached(relieved, 4)) == 1                                                        # a dog bone's own


def test_a_dog_bone_over_a_corner_leaves_its_fillet_a_fillet():
    """A dog bone excused before the fillets were judged cut a corner's
    fillet into pieces that were no fillet each [found by fuzzing,
    2026-10-17]."""
    square = shapely_box(0, 0, 50, 50)
    bone = Point(0.3, 0.3).buffer(0.6, quad_segs=32)             # over the corner: the fillet's horns are left
    assert unreached(square, 4, bone) == []


def test_the_plan_says_the_smallest_cutter():
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        board("a", ply15).on(m.bottom)
    nest, layout = _nested()
    assert _plan(nest, layout)["settings"]["smallest_cutter"] == 2.0
    registry.reset()
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        use(cam.smallest_cutter(3.175))
        board("a", ply15).on(m.bottom)
    nest, layout = _nested()
    assert _plan(nest, layout)["settings"]["smallest_cutter"] == 3.175


def test_a_counterbore_over_a_through_slot_is_one_pocket():
    """A counterbore was clipped by the through slot under it, still
    material when the blind pockets are cut, and the narrow ring left took
    the 2 mm cutter (the examples' operations panel, 2026-10-17)."""
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        p = board("panel", ply15).on(m.bottom)
        p.slot(12, at=p.top.center, centers=40, along="depth", depth=4, name="head")
        p.slot(6, at=p.top.center, centers=40, along="depth", depth=through, name="mount")
    nest, layout = _nested()
    (setup,) = _plan(nest, layout)["setups"]
    templates = {r["name"]: op["template"] for op in _ops(setup, "pocket") for f in op["features"] for r in f["ops"]
                 if r["name"]}
    assert templates["head"] == "pocket.dc_Tasche 6mm"


def test_the_opening_test_answers_alike_however_a_ring_is_written():
    """One pocket's region, a round pocket clipped by the board's edge and a
    hole, written clockwise and counter-clockwise, left 5.3 and 13.5 mm²
    of it to the 6 mm cutter, so the plan and its check disagreed: the
    region is normalized first [found by fuzzing, 2026-10-17]."""
    from shapely.geometry.polygon import orient
    ring = json.loads((Path(__file__).parent / "data" / "cam_pocket_ring.json").read_text())
    region = Polygon(ring)
    left = [round(p.area, 3) for p in unreached(region, 3.0)]
    assert left == [round(p.area, 3) for p in unreached(orient(region, 1.0), 3.0)] == \
        [round(p.area, 3) for p in unreached(orient(region, -1.0), 3.0)]
    turned = ring[50:] + ring[:50]
    assert [round(p.area, 3) for p in unreached(Polygon(turned), 3.0)] == left


def test_a_pocket_over_an_opening_at_the_edge_stays_within_the_parts_outer_loop():
    """Clipped by the outline alone, a pocket over a through pocket that
    opens the board's edge reached where the nest may have put another part,
    off the blank [found by fuzzing, 2026-10-17]."""
    from lang.cam.regions import Placed, polygons
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        p = board("panel", ply15).on(m.bottom)
        p.pocket(rect(depth=80, width=60), at=p.top.front.left(100), depth=through, name="bite")
        p.pocket(rect(depth=40, width=140), at=p.top.front(60).left(60), depth=5, name="over")
    nest, layout = _nested()
    (setup,) = _plan(nest, layout)["setups"]
    (feature,) = [f for op in _ops(setup, "pocket") for f in op["features"]
                  if f["what"] == "pocket" and f["ops"][0]["name"] == "over"]
    placed = nest["materials"][0]["sheets"][0]["blanks"][0]["parts"][0]
    loop = Placed.of(layout["modules"][0]["parts"][0], placed["transform"], layout["frame"]).machine_outline(30.0)
    assert polygons(feature["rings"])[0].difference(Polygon(loop.exterior).buffer(1e-6)).area < 1e-6
