"""The CAM emitter's Fusion-free half (`lang.emit.cam_plan`): a plan's
setups mapped into the nested document, the plans it refuses, the
parameters it writes, and the tests it binds the model's faces and edges by."""
import json
import math
import re
from pathlib import Path
from typing import Any

import pytest

from lang import *
from lang.cam.plan import plan_nest as plan_cam_nest
from lang.cam.plan_types import CAM_VERSION as PLAN_CAM_VERSION
from lang.cam.plan_types import CamFile
from lang.cam.resolve import REPO
from lang.core.layout import build_layout
from lang.emit import cam_plan
from lang.emit.cam_plan import (Cylinder, EdgeLine, EdgePath, EdgeSample, FaceLoop, Floor, Height, OperationPlan,
                                Params, Region, Silhouette, Tabs, WallArc, bore_feed, chamfer_reverted, check_plan,
                                edge_on_line, edge_on_path, inside, is_plan, loop_follows, on_circle, param_writes,
                                plan_cam, read_plan, region_samples, runs, template_path)
from lang.emit.nested import GAP, plan_nest
from lang.nesting.nest import nest_parts
from lang.nesting.workshop import Sheet, Workshop
from helpers import ply9, ply15
from test_cam import FAST, REGISTRY, _panel  # pyright: ignore[reportPrivateUsage]


def _planned(workshop: Workshop | None = None) -> tuple[CamFile, Any, Any]:
    layout = build_layout()
    workshop = workshop or Workshop(bed=(2000.0, 1000.0), sheets=(Sheet("birch 15", 2500, 1250),
                                                                    Sheet("birch 9", 2500, 1250)))
    nest, _parts = nest_parts(layout, None, workshop, name="m.birch_15", options=FAST)
    return plan_cam_nest(nest, layout, registry=REGISTRY), nest, layout


def _bindings(setup: cam_plan.SetupPlan, kind: str | None = None) -> list[Any]:
    return [b for op in setup.operations if kind is None or op.kind == kind for f in op.features for b in f.bindings]


# -- the versions --------------------------------------------------------------------------------------------

def test_the_emitter_reads_the_plans_version_and_caps_a_bores_feed_as_auto_setup():
    assert cam_plan.CAM_VERSION == PLAN_CAM_VERSION
    rules = (REPO / "lib" / "auto_setup" / "rules.py").read_text()
    found = re.search(r"^MAX_BORE_FEED = ([0-9.]+)", rules, re.M)
    assert found is not None and float(found.group(1)) == cam_plan.MAX_BORE_FEED


# -- the mapping -----------------------------------------------------------------------------------------------

def test_a_setup_lies_where_the_nested_document_draws_its_blank():
    _panel()
    with module("n", Box.from_size(width=600, depth=400, height=100)) as n:
        board("thin", ply9).on(n.bottom).between(n.front, Pos("x", 200), n.left, n.right)
    plan, nest, layout = _planned()
    docs = plan_cam(plan, nest)
    drawn = {(d.material, b.name): b for d in plan_nest(nest, layout) for s in d.sheets for b in s.blanks}
    assert [d.material for d in docs] == [m["material"] for m in nest["materials"]]
    assert sum(len(d.setups) for d in docs) == len(plan["setups"]) == len(drawn)
    for doc in docs:
        for setup in doc.setups:
            blank = drawn[(doc.material, setup.blank)]
            assert setup.corner == blank.origin and setup.size == blank.size
            assert setup.top == blank.size[2] and setup.parts == [p.path for p in blank.parts]
    assert plan_cam(plan, nest, "birch 9")[0].material == "birch 9"
    with pytest.raises(ValueError, match="no material"):
        plan_cam(plan, nest, "oak 20")


def test_a_second_sheet_lies_above_the_first_one_gap_apart():
    nest: Any = {"version": 3, "name": "n", "written": "w", "layout_hash": "h", "materials": [
        {"material": "birch 15", "thickness": 15.0, "sheets": [
            {"name": "1", "size": [2500.0, 1250.0], "blanks": [{"name": "1.1", "rect": [0.0, 0.0, 10.0, 10.0],
                                                                 "parts": []}]},
            {"name": "2", "size": [1200.0, 600.0], "blanks": [{"name": "2.1", "rect": [5.0, 7.0, 10.0, 10.0],
                                                                "parts": []}]}]}]}
    plan: Any = {"version": cam_plan.CAM_VERSION, "nest": "n", "nest_written": "w", "layout_hash": "h", "setups": [
        _setup("n birch 15 2.1", "birch 15", "2.1", [5.0, 7.0, 10.0, 10.0])]}
    (setup,) = plan_cam(plan, nest)[0].setups
    assert setup.corner == (5.0, 1250.0 + GAP + 7.0, 0.0) and setup.sheet == "2"


def _setup(name: str, material: str, blank: str, rect: list[float], operations: list[Any] | None = None) -> Any:
    return {"name": name, "stock": {"material": material, "sheet": blank.split(".")[0], "blank": blank, "rect": rect,
                                    "thickness": 15.0, "own_blank": False},
            "parts": [], "operations": operations or [], "release_order": [], "left_out": [], "problems": []}


def test_every_feature_is_bound_by_what_its_kind_needs():
    _panel()
    plan, nest, _layout = _planned()
    (doc,) = [d for d in plan_cam(plan, nest) if d.material == "birch 15"]
    (setup,) = doc.setups
    planned: Any = plan["setups"][0]
    x0, y0, _z = setup.corner
    top = setup.top
    for op, out in zip(planned["operations"], setup.operations):
        assert (out.name, out.kind, out.template, out.selection) == (op["name"], op["kind"], op["template"],
                                                                       cam_plan.SELECTION[op["kind"]])
        for f, got in zip(op["features"], out.features):
            assert got.part == f["part"] and got.what == f["what"]
            if f["what"] == "outer":
                (b,) = got.bindings
                assert isinstance(b, Silhouette) and b.ring == [(x0 + p[0], y0 + p[1]) for p in f["ring"]]
            elif f["what"] == "inner":
                (b,) = got.bindings
                assert isinstance(b, FaceLoop) and b.levels == (top, 0.0)
                assert b.ring[0] == (x0 + f["ring"][0][0], y0 + f["ring"][0][1])
            elif f["what"] == "pocket" and f["depth"] is None:
                assert [type(b) for b in got.bindings] == [FaceLoop] * len(f["rings"])
            elif f["what"] == "pocket":
                (b,) = got.bindings
                assert isinstance(b, Floor) and b.z == pytest.approx(top - f["depth"])
                assert len(b.rings) == len(f["rings"])
            elif f["what"] == "rest":
                (b,) = got.bindings
                assert isinstance(b, Region) and len(b.loops) == len(f["rings"])
            elif f["what"] == "hole":
                (b,) = got.bindings
                assert isinstance(b, Cylinder) and b.center == (x0 + f["center"][0], y0 + f["center"][1])
                assert b.d == f["d"]
            elif f["what"] == "dogbone":
                (b,) = got.bindings
                assert isinstance(b, Cylinder if op["kind"] == "drill" else WallArc)
            elif f["what"] == "chamfer":
                assert [type(b) for b in got.bindings] == [EdgePath] * len(f["paths"])
                assert all(isinstance(b, EdgePath) and b.z == pytest.approx(top - f["size"]) for b in got.bindings)
            else:
                (b,) = got.bindings
                assert isinstance(b, EdgeLine) and b.z == pytest.approx(top - f["depth"])
                assert b.start == (x0 + f["start"][0], y0 + f["start"][1])
    kinds = {type(b) for b in _bindings(setup)}
    assert {Silhouette, FaceLoop, Floor, Cylinder, EdgePath, EdgeLine} <= kinds


def test_a_small_parts_tabs_are_sketch_positions_at_the_stocks_top():
    with module("m", Box.from_size(width=600, depth=400, height=100)) as m:
        board("strip", ply15).on(m.bottom).between(m.front, Pos("x", 15), m.left, Pos("y", 300))
    plan, nest, _layout = _planned()
    (setup,) = plan_cam(plan, nest)[0].setups
    tabbed = [op for op in setup.operations if op.params.tabs is not None]
    assert sorted(op.kind for op in tabbed) == ["contour", "release"]
    positions = setup.tab_positions()
    assert len(positions) == len(tabbed[0].params.tabs.positions) >= 3  # pyright: ignore[reportOptionalMemberAccess]
    assert all(p[2] == setup.top for p in positions)
    (planned,) = plan["setups"]
    raw = next(op for op in planned["operations"] if op["params"]["tabs"])["params"]["tabs"]
    assert raw is not None
    assert positions[0] == (setup.corner[0] + raw["positions"][0][0], setup.corner[1] + raw["positions"][0][1], 15.0)


# -- refusals ----------------------------------------------------------------------------------------------------

def test_a_plan_of_another_version_or_nest_is_refused():
    _panel()
    plan, nest, _layout = _planned()
    check_plan(plan, nest)
    for key, value, words in (("version", 0, "version 0"), ("nest", "other", "another nest"),
                              ("nest_written", "2020-01-01T00:00:00+01:00", "another nest"),
                              ("layout_hash", "0", "another nest")):
        with pytest.raises(ValueError, match=words):
            plan_cam({**plan, key: value}, nest)  # pyright: ignore[reportArgumentType]
    with pytest.raises(ValueError, match="nest version"):
        plan_cam(plan, {**nest, "version": 0})
    moved = json.loads(json.dumps(plan))
    moved["setups"][0]["stock"]["rect"][0] += 1
    with pytest.raises(ValueError, match="lies at"):
        plan_cam(moved, nest)
    gone = json.loads(json.dumps(plan))
    gone["setups"][0]["stock"]["blank"] = "9.9"
    with pytest.raises(ValueError, match="no blank 9.9"):
        plan_cam(gone, nest)
    stranger = json.loads(json.dumps(plan))
    stranger["setups"][0]["operations"][0]["features"][0]["part"] = "m.nobody"
    with pytest.raises(ValueError, match="m.nobody, which is not on the blank"):
        plan_cam(stranger, nest)
    wrong = json.loads(json.dumps(plan))
    op = next(op for op in wrong["setups"][0]["operations"] if op["kind"] == "bore")
    op["kind"] = "groove"
    with pytest.raises(ValueError, match="cannot machine a 'hole' feature"):
        plan_cam(wrong, nest)


def test_a_plan_file_is_read_with_its_nest_and_layout(tmp_path: Path):
    _panel()
    plan, nest, layout = _planned()
    for name, data in (("cam.json", plan), ("nest.json", nest), ("nest.layout.json", layout)):
        (tmp_path / name).write_text(json.dumps(data))
    got, got_nest, got_layout = read_plan(str(tmp_path / "cam.json"))
    assert got == json.loads(json.dumps(plan)) and got_nest == nest and got_layout == layout
    assert is_plan(got) and not is_plan(nest) and not is_plan(layout)
    (tmp_path / "nest.json").write_text(json.dumps({**nest, "written": "later"}))
    with pytest.raises(ValueError, match="another nest"):
        read_plan(str(tmp_path / "cam.json"))


def test_a_template_is_found_where_the_plan_read_it_else_in_this_repository(tmp_path: Path):
    plan: Any = {"settings": {"templates": str(REPO / "addins-src" / "auto_setup" / "templates"),
                              "values": {"cam.templates": "addins-src/auto_setup/templates"}}}
    stem = "contour.dc_Kontur 6mm"
    assert template_path(plan, stem, str(tmp_path)) == str(REPO / "addins-src" / "auto_setup" / "templates" /
                                                           (stem + ".f3dhsm-template"))
    moved: Any = {"settings": {"templates": str(tmp_path / "gone"), "values": plan["settings"]["values"]}}
    assert template_path(moved, stem, str(REPO)) == str(REPO / "addins-src" / "auto_setup" / "templates" /
                                                        (stem + ".f3dhsm-template"))
    assert template_path(moved, stem, str(tmp_path)).startswith(str(tmp_path / "gone"))


# -- the parameters -----------------------------------------------------------------------------------------------

def _op(kind: str, top: Height, bottom: Height, *, multiple: bool | None = None, stepdowns: int | None = None,
        order: bool = False, scale: float | None = None, tabs: Tabs | None = None) -> OperationPlan:
    return OperationPlan("op", kind, "t", "l", 6.0, cam_plan.SELECTION[kind],
                         Params(top, bottom, multiple, stepdowns, order, scale, tabs), [])


def test_a_release_is_written_from_the_stocks_bottom_in_one_depth_in_order():
    writes = param_writes(_op("release", Height("from stock bottom", 0.2), Height("from stock bottom", -0.2),
                              multiple=False, order=True))
    assert writes == [("topHeight_mode", "'from stock bottom'"), ("topHeight_offset", "0.2 mm"),
                      ("bottomHeight_mode", "'from stock bottom'"), ("bottomHeight_offset", "-0.2 mm"),
                      ("doMultipleDepths", "false"), ("preserveOrder", "true"), ("group_tabs", "false")]


def test_tabs_are_written_after_their_group_and_count_none_per_contour():
    writes = dict(param_writes(_op("contour", Height("from stock top", 0.0), Height("from stock bottom", 0.2),
                                   tabs=Tabs(5.0, 2.0, [(1.0, 2.0, 15.0)]))))
    assert writes["group_tabs"] == "true" and writes["tabsPerContour"] == "0"
    assert writes["tabWidth"] == "5 mm" and writes["tabHeight"] == "2 mm" and writes["tabPositioning"] == "'tabCount'"
    names = [n for n, _e in param_writes(_op("contour", Height("from stock top", 0.0), Height("from stock top", 0.0),
                                             tabs=Tabs(5.0, 2.0, [])))]
    assert names.index("group_tabs") < names.index("tabWidth") < names.index("tabsPerContour")


def test_holes_take_only_their_own_and_a_groove_is_cut_with_the_tip():
    bore = dict(param_writes(_op("bore", Height("from stock top", 0.0), Height("from hole bottom", 0.0), scale=1.5)))
    assert bore["selectSameDiameter"] == "false" and bore["bottomHeight_mode"] == "'from hole bottom'"
    assert "preserveOrder" not in bore
    groove = param_writes(_op("groove", Height("from stock top", 0.0), Height("from contour", 0.0), multiple=True,
                              stepdowns=2))
    assert groove == [("doMultipleDepths", "true"), ("numberOfStepdowns", "2"), ("preserveOrder", "false"),
                      ("doChamfer", "false"), ("group_tabs", "false")]
    one = dict(param_writes(_op("groove", Height("from stock top", 0.0), Height("from contour", 0.0), multiple=False,
                                stepdowns=0)))
    assert one["doMultipleDepths"] == "false" and "numberOfStepdowns" not in one
    chamfer = dict(param_writes(_op("chamfer", Height("from stock top", 0.0), Height("from contour", 0.0))))
    assert chamfer["chamferWidth"] == "0 mm" and chamfer["chamferClearance"] == "0 mm"
    assert dict(param_writes(_op("pocket", Height("from stock top", 0.0), Height("from contour", -0.25))))[
        "bottomHeight_offset"] == "-0.25 mm"


def test_a_bores_feed_follows_its_hole_but_never_past_the_cap_or_below_the_template():
    assert bore_feed(400.0, None) is None
    assert bore_feed(400.0, 1.5) == 600.0
    assert bore_feed(400.0, 20.0) == cam_plan.MAX_BORE_FEED
    assert bore_feed(400.0, 0.9) is None and bore_feed(3500.0, 2.0) is None


# -- binding by position ---------------------------------------------------------------------------------------------

def _line(a: tuple[float, float], b: tuple[float, float], z: float = 15.0) -> EdgeSample:
    return EdgeSample((a[0], a[1], z), (b[0], b[1], z), ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, z), None,
                      math.dist(a, b))


def _arc(c: tuple[float, float], r: float, a0: float, a1: float, z: float = 15.0) -> EdgeSample:
    def at(t: float) -> tuple[float, float, float]:
        return (c[0] + r * math.cos(t), c[1] + r * math.sin(t), z)
    return EdgeSample(at(a0), at(a1), at((a0 + a1) / 2), r, r * abs(a1 - a0))


def _polygon_arc(c: tuple[float, float], r: float, a0: float, a1: float, n: int) -> list[tuple[float, float]]:
    return [(c[0] + r * math.cos(a0 + (a1 - a0) * k / n), c[1] + r * math.sin(a0 + (a1 - a0) * k / n))
            for k in range(n + 1)]


def test_an_edge_is_on_a_path_with_its_ends_and_middle_an_arcs_within_its_chords_sagitta():
    square = [(0.0, 0.0), (100.0, 0.0), (100.0, 50.0), (0.0, 50.0)]
    assert edge_on_path(_line((0, 0), (100, 0)), square, True, 15.0)
    assert edge_on_path(_line((0, 50), (0, 0)), square, True, 15.0)               # closing edge, either way
    assert not edge_on_path(_line((0, 50), (0, 0)), square, False, 15.0)          # an open path has no closing edge
    assert not edge_on_path(_line((0, 0), (100, 0), z=14.0), square, True, 15.0)  # another height
    assert not edge_on_path(_line((0, 0.1), (100, 0.1)), square, True, 15.0)      # beside it
    assert not edge_on_path(_line((0, 0), (100, 50)), square, True, 15.0)         # across it
    # a quarter circle of radius 50 as 8 chords: its middle lies off them by up to the sagitta
    arc = _polygon_arc((0.0, 0.0), 50.0, 0.0, math.pi / 2, 8)
    assert edge_on_path(_arc((0.0, 0.0), 50.0, 0.0, math.pi / 2), arc, False, 15.0)
    assert not edge_on_path(_arc((0.0, 0.0), 49.0, 0.0, math.pi / 2), arc, False, 15.0)


def test_a_loop_follows_a_ring_only_all_of_it():
    ring = [(0.0, 0.0), (100.0, 0.0), (100.0, 50.0), (0.0, 50.0)]
    loop = [_line(ring[k], ring[(k + 1) % 4]) for k in range(4)]
    assert loop_follows(loop, ring, 15.0)
    assert not loop_follows(loop[:3], ring, 15.0)                               # short of it
    assert not loop_follows(loop, ring, 0.0) and not loop_follows([], ring, 15.0)
    split = loop[1:] + [_line((0, 0), (40, 0)), _line((40, 0), (100, 0))]
    assert loop_follows(split, ring, 15.0)                                      # an edge in two is still it
    notch = [(0.0, 0.0), (40.0, 0.0), (40.0, 10.0), (60.0, 10.0), (60.0, 0.0), (100.0, 0.0), (100.0, 50.0), (0.0, 50.0)]
    assert not loop_follows([_line(notch[k], notch[(k + 1) % 8]) for k in range(8)], ring, 15.0)


def test_a_line_a_circle_and_a_region():
    assert edge_on_line(_line((0, 5), (3, 5), z=14.7), (-1.0, 5.0), (3.0, 5.0), 14.7)
    assert not edge_on_line(_line((0, 5), (3, 5), z=14.7), (-1.0, 5.1), (3.0, 5.1), 14.7)
    assert not edge_on_line(_arc((0, 0), 5, 0, 1, z=14.7), (-1.0, 5.0), (3.0, 5.0), 14.7)
    assert on_circle((10.0, 10.0), 5.0, (10.0, 10.01), 2.5) and not on_circle((10.0, 10.0), 5.0, (10.0, 10.0), 2.6)
    frame = [[(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)], [(4.0, 4.0), (4.0, 6.0), (6.0, 6.0), (6.0, 4.0)]]
    assert inside((1.0, 1.0), frame) and not inside((5.0, 5.0), frame) and not inside((11.0, 5.0), frame)


def test_a_regions_samples_lie_in_it_a_narrow_ones_too():
    slot = [[(0.0, 0.0), (200.0, 0.0), (200.0, 0.3), (0.0, 0.3)]]
    samples = region_samples(slot)
    assert samples and all(inside(p, slot) for p in samples)
    frame = [[(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)], [(1.0, 1.0), (1.0, 9.0), (9.0, 9.0), (9.0, 1.0)]]
    samples = region_samples(frame)
    assert samples and all(inside(p, frame) for p in samples) and len(samples) <= 48


def test_edges_make_runs_turned_as_they_go_and_closed_where_they_close():
    a, b, c = _line((0, 0), (10, 0)), _line((20, 0), (10, 0)), _line((20, 0), (30, 5))
    far = _line((50, 50), (60, 50))
    got = runs([c, far, a, b])
    assert sorted((sorted(r), closed) for r, closed in got) == [([0, 2, 3], False), ([1], False)]
    (chain, _closed) = next(r for r in got if len(r[0]) == 3)
    assert chain in ([2, 3, 0], [0, 3, 2])                                       # end to end
    square = [_line((0, 0), (10, 0)), _line((10, 10), (10, 0)), _line((10, 10), (0, 10)), _line((0, 10), (0, 0))]
    ((run, closed),) = runs(square)
    assert sorted(run) == [0, 1, 2, 3] and closed
    circle = EdgeSample((5.0, 0.0, 0.0), (5.0, 0.0, 0.0), (-5.0, 0.0, 0.0), 5.0, 10 * math.pi)
    assert runs([circle]) == [([0], True)]


def test_a_chamfers_chain_turns_so_the_tool_runs_on_its_open_side():
    # an edge running +x with the chamfer's face looking out to -y: the open side is on the right
    assert chamfer_reverted((1.0, 0.0, 0.0), (0.0, -0.7, 0.7))
    assert not chamfer_reverted((-1.0, 0.0, 0.0), (0.0, -0.7, 0.7))
    assert not chamfer_reverted((1.0, 0.0, 0.0), (0.0, 0.7, 0.7))
