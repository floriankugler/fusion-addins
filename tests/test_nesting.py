"""Nesting (`lang.nesting`): a nest's values resolved from the build's
settings, the inventory, the parts as the nest sees them (from the
machining face, their turns and openings, their own spacing, a
`nest(False)` board's own blank), the solvers' results as `verify` checks
them, the saw plans, refill, the nest file and its drawing, the command
line, and the Fusion emitter's reading of a nest.

The solvers get short times here; what is checked is what every nest must
be (the verifier, placements, the stock used), not how good it is."""
from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path

import numpy as np
import pytest
from shapely import Point, Polygon

from lang import (Board, Box, LangError, Shape, SheetMaterial, board, circle, module, nesting, rect, sheet_material,
                  slat, slat_material, through, use)
from lang.core.layout import build_layout, layout_hash
from lang.core.layout_types import Layout
from lang.emit.nested import NEST_VERSION as EMIT_NEST_VERSION, apply, plan_nest
from lang.nesting import sawing
from lang.nesting.__main__ import main as nest_main
from lang.nesting.draw import draw_nest
from lang.nesting.fingerprint import fingerprints
from lang.nesting.inventory import inventory_from, read_inventory
from lang.nesting.items import OUTSIDE, Item, Parts, check_sizes, parts_of_layout, turned
from lang.nesting.nest import Options, nest_layout, nest_parts
from lang.nesting.nest_types import NEST_VERSION, NestFile
from lang.nesting.packing import KNAPSACK, VARIABLE, Bin, pack
from lang.nesting.refilling import SheetState, refill
from lang.nesting.resolve import nest_of, resolve, workshop_of
from lang.nesting.sawing import Node, PartOn, cut_list, cuts, leaves, simplify
from lang.nesting.verify import verify
from lang.nesting.workshop import OnHand, Sheet, Workshop

from helpers import EXAMPLES, merged_layouts, ply12, ply15

FAST = Options(seconds=0.5, saw_seconds=0.1, refill_seconds=0.3)
oak = sheet_material("oak", t=20)
mdf = sheet_material("mdf", t=16, grain=False)
#: Sheets of 2470 x 1240 for every material the tests use.
SHEETS = tuple(Sheet(label, 2470.0, 1240.0) for label in ("birch 9", "birch 12", "birch 15", "birch 18", "oak 20",
                                                         "mdf 16"))
WORKSHOP = Workshop(bed=(2000.0, 1000.0), sheets=SHEETS)


def panel(name: str, length: float, width: float, mat: SheetMaterial = ply15) -> Board:
    """A board of length x width lying flat, in a module of its own."""
    with module(name, Box.from_size(depth=length, width=width, height=mat.thickness)) as m:
        b = board("panel", mat).on(m.bottom)
    return b


def nested(workshop: Workshop = WORKSHOP, options: Options = FAST, **kw: object) -> tuple[Layout, NestFile, Parts]:
    """Every nested part of the build, nested with `workshop`'s values."""
    layout = build_layout()
    nest, parts = nest_parts(layout, None, workshop, options=options, **kw)  # pyright: ignore[reportArgumentType]
    return layout, nest, parts


def placements(nest: NestFile) -> dict[str, list[tuple[str, str]]]:
    """Each part's (sheet, blank) by path."""
    out: dict[str, list[tuple[str, str]]] = {}
    for m in nest["materials"]:
        for s in m["sheets"]:
            for b in s["blanks"]:
                for p in b["parts"]:
                    out.setdefault(p["path"], []).append((s["name"], b["name"]))
    return out


# -- the inventory ---------------------------------------------------------------------------

def test_the_inventory_lists_stock_on_hand_one_kind_of_entry(tmp_path: Path):
    path = tmp_path / "inventory.toml"
    path.write_text('[[stock]]\nmaterial = "birch 15"\nsize = [2500, 1250]\ncount = 2\n'
                    '[[stock]]\nmaterial = " birch 9 "\nsize = [1250.5, 600]\n')
    assert read_inventory(path) == [OnHand("birch 15", 2500, 1250, 2), OnHand("birch 9", 1250.5, 600, 1)]
    assert inventory_from({}) == []
    assert OnHand("birch 15", 1250, 600, 2).spelled() == "birch 15:1250x600*2"


@pytest.mark.parametrize("text, message", [
    ("[[sheet]]\nsize = [2470, 1240]", "unknown key sheet"),
    ("[[stock]]\nsize = [2470, 1240]", "give its material and size"),
    ("[[stock]]\nmaterial = 'birch 15'", "give its material and size"),
    ("[[stock]]\nmaterial = ''\nsize = [2470, 1240]", "material is a material's name"),
    ("[[stock]]\nmaterial = 'birch 15'\nsize = [2470]", "two numbers"),
    ("[[stock]]\nmaterial = 'birch 15'\nsize = [2470, -1]", "not a size"),
    ("[[stock]]\nmaterial = 'birch 15'\nsize = [2470, 1240]\ncount = 0", "1 or more"),
    ("[[stock]]\nmaterial = 'birch 15'\nsize = [2470, 1240]\ncount = 1.5", "whole number"),
    ("[[stock]]\nmaterial = 'birch 15'\nsize = [2470, 1240]\nwidth = 3", "unknown key width"),
    ("stock = 3", "as a \\[\\[stock\\]\\] table"),
    ("[[stock]\n", "inventory.toml"),
])
def test_the_inventory_refuses_what_it_cannot_read(tmp_path: Path, text: str, message: str):
    path = tmp_path / "inventory.toml"
    path.write_text(text)
    with pytest.raises(LangError, match=message):
        read_inventory(path)


def test_the_nest_takes_its_time_by_the_parts_within_its_settings():
    w = Workshop()
    assert [w.nest_seconds(n) for n in (4, 20, 62, 500)] == pytest.approx([5, 12, 37.2, 40])
    assert Workshop(seconds=3).nest_seconds(4) == 3
    assert Workshop(rate=1, least_seconds=2).nest_seconds(1) == 2


def test_a_nest_without_a_bed_or_stock_is_refused():
    panel("a", 500, 300)
    with pytest.raises(LangError, match="No bed"):
        nested(Workshop(sheets=SHEETS))
    with pytest.raises(LangError, match="No stock for birch 15: no sheet size to buy"):
        nested(Workshop(bed=(2000, 1000), sheets=(Sheet("birch 9", 2470, 1240),)))


# -- a nest's values ------------------------------------------------------------------------------

def _two_modules() -> tuple[Board, Board]:
    with module("a", Box.from_size(depth=600, width=400, height=15)) as m:
        left = board("panel", ply15).on(m.bottom)
    with module("b", Box.from_size(depth=600, width=400, height=15, origin=(0, 1000, 0))) as m:
        right = board("panel", ply15).on(m.bottom)
    return left, right


def test_a_nest_s_own_value_comes_first_then_its_parts_then_the_default():
    use(nesting.bed((2000, 1000)), nesting.margin(12))
    with module("m", Box.from_size(depth=600, width=400, height=300)) as m:
        use(nesting.kerf(3.2))
        a = board("a", ply15).on(m.bottom)
        board("b", ply15).on(m.top).use(nesting.spacing(20))
        m.nest("both", [a, m["b"]]).use(nesting.margin(15))
    layout = build_layout()
    r = resolve(layout, nest_of(layout, "m.both"))
    assert r.values["nesting.bed"] == [2000, 1000] and r.sources["nesting.bed"] == "root"
    assert r.values["nesting.margin"] == 15 and r.sources["nesting.margin"] == "m.both"
    assert r.values["nesting.kerf"] == 3.2 and r.sources["nesting.kerf"] == "m"
    assert r.values["nesting.max_cuts"] == 5 and r.sources["nesting.max_cuts"] == "default"
    # Between two parts the larger spacing holds: each keeps its own, the nest the least.
    assert r.spacing == {"m.a": 10, "m.b": 20} and r.values["nesting.spacing"] == 10
    assert r.sources["nesting.spacing"] == "default, m.b"
    w = workshop_of(layout, nest_of(layout, "m.both"), r, [OnHand("birch 15", 2470, 1240)])
    assert (w.bed, w.margin, w.kerf, w.spacing, w.max_cuts, w.refill) == ((2000, 1000), 15, 3.2, 10, 5, True)


def test_parts_that_give_two_values_of_a_key_the_nest_needs_one_of_refuse_it():
    use(nesting.bed((2000, 1000)))
    left, right = _two_modules()
    left.use(nesting.margin(12))
    with module("van", Box.from_size(depth=10, width=10, height=10, origin=(5000, 0, 0))):
        pass
    layout = build_layout()
    from lang.core.layout_types import NestLayout
    both: NestLayout = {"path": "x.both", "module": "x", "by": "parts", "material": None,
                        "parts": [left.path, right.path], "left_out": [], "settings": {}}
    with pytest.raises(LangError, match=r"x.both: its parts give two values of nesting.margin: a.panel 12 \(a.panel\), "
                                        r"b.panel 10 \(default\); a nest takes one"):
        resolve(layout, both)
    resolve(layout, {**both, "settings": {"nesting.margin": {"value": 10.0, "source": "x.both"}}})


def test_a_nest_with_no_bed_anywhere_is_refused():
    panel("a", 500, 300)
    layout = build_layout()
    with pytest.raises(LangError, match=r"a.birch_15: no nesting.bed is used for it or its parts; "
                                        r"use\(nesting.bed\(\(2000, 1000\)\)\) at the root"):
        resolve(layout, nest_of(layout, "a.birch_15"))
    with pytest.raises(LangError, match="No nest 'a.oak' in the build \\(its nests: a.birch_15\\)"):
        nest_of(layout, "a.oak")


def test_a_part_on_a_bed_of_its_own_parts_disagree_unless_the_nest_says():
    use(nesting.bed((2000, 1000)))
    left, right = _two_modules()
    right.use(nesting.bed((2500, 1250)))
    with module("van", Box.from_size(depth=10, width=10, height=10, origin=(5000, 0, 0))) as van:
        pass
    layout = build_layout()
    from lang.core.layout_types import NestLayout
    both: NestLayout = {"path": "van.both", "module": "van", "by": "parts", "material": None,
                        "parts": [left.path, right.path], "left_out": [], "settings": {}}
    with pytest.raises(LangError, match=r"two values of nesting.bed: a.panel 2000 x 1000 \(root\), b.panel 2500 x "
                                        r"1250 \(b.panel\)"):
        resolve(layout, both)
    assert van.path == "van"


def test_the_sheets_bought_are_the_material_s_size_and_one_without_is_refused_unless_on_hand():
    use(nesting.bed((2000, 1000)))
    sized = sheet_material("birch", t=18, size=(2500, 1250))
    with module("m", Box.from_size(depth=600, width=400, height=300)) as m:
        board("a", sized).on(m.bottom)
        board("b", ply15).on(m.top)
    layout = build_layout()
    w = workshop_of(layout, nest_of(layout, "m.birch_18"), resolve(layout, nest_of(layout, "m.birch_18")))
    assert w.sheets == (Sheet("birch 18", 2500, 1250),) and w.on_hand == ()
    unsized = nest_of(layout, "m.birch_15")
    with pytest.raises(LangError, match=r"m.birch_15: birch 15 has no sheet size to buy .* and none on hand"):
        workshop_of(layout, unsized, resolve(layout, unsized))
    on_hand = [OnHand("birch 15", 1200, 800), OnHand("birch 9", 2500, 1250)]
    w = workshop_of(layout, unsized, resolve(layout, unsized), on_hand)
    assert w.sheets == () and w.on_hand == (OnHand("birch 15", 1200, 800),)


# -- nest() ---------------------------------------------------------------------------------------

def test_nest_false_leaves_a_part_out_and_a_manual_part_or_a_slat_is_never_nested():
    a = panel("a", 500, 300).nest(False)
    with module("m", Box.from_size(depth=400, width=300, height=15)) as m:
        board("hand", ply15).on(m.bottom).manual()
        slat("rail", slat_material("oak"), section=(20, 40)).on(m.bottom).edge_on(m.left).between(m.front, m.back)
    layout = build_layout()
    parts = {p["path"]: p for mod in layout["modules"] for p in mod["parts"]}
    assert parts["a.panel"]["nest"] is False and parts["m.hand"]["nest"] is False
    assert not a.nested
    out = parts_of_layout(layout, 10)
    assert out.by_material == {}
    assert [(p.path, p.why) for p in out.left_out] == [("a.panel", "nest(False)"), ("m.hand", "manual"),
                                                       ("m.rail", "slat")]


# -- the parts as the nest sees them -------------------------------------------------------------

#: Per side a board lies on: the notch's shape in that plane, and the
#: corner of its big face the notch is cut at.
_NOTCH = {
    "bottom": (rect(depth=60, width=40), ("front", "left")), "top": (rect(depth=60, width=40), ("front", "left")),
    "left": (rect(depth=60, height=40), ("front", "bottom")), "right": (rect(depth=60, height=40), ("front", "bottom")),
    "front": (rect(width=60, height=40), ("left", "bottom")), "back": (rect(width=60, height=40), ("left", "bottom")),
}


def _orientation(on: str, machined: str, given: bool = False) -> Board:
    """A board on the module's `on` side with a notch at one corner (so
    its outline has a handedness) and a blind pocket on its `machined` big
    face (so that face is the one machined); `given`: the pocket on the
    other face, and `machine()` names the `machined` one."""
    with module("m", Box.from_size(depth=600, width=500, height=400)) as m:
        b = board("b", ply15).on(getattr(m, on))
        face = getattr(b, machined)
        shape, (edge, corner) = _NOTCH[on]
        b.cut(shape, at=getattr(getattr(face, edge), corner))
        b.pocket(circle(20), at=(getattr(b, "outer" if machined == "inner" else "inner") if given else face).center,
                 depth=4)
        if given:
            b.machine(face)
    return b


@pytest.mark.parametrize("on", ["bottom", "top", "left", "right", "front", "back"])
@pytest.mark.parametrize("machined", ["inner", "outer"])
@pytest.mark.parametrize("given", [False, True])
def test_a_part_is_seen_from_its_machining_face_and_maps_onto_it(on: str, machined: str, given: bool):
    b = _orientation(on, machined, given)
    layout = build_layout()
    part = layout["modules"][0]["parts"][0]
    item = parts_of_layout(layout, 10).by_material["birch 15"][0]
    frame = layout["frame"]
    axis, sign = frame[part["machine"]][1], 1 if frame[part["machine"]][0] == "+" else -1
    assert part["machine"] == getattr(b, machined).world_name
    assert item.up == part["machine"]
    m = np.array(item.frame.matrix())
    rotation = m[:, :3]
    assert np.allclose(rotation @ rotation.T, np.eye(3)) and np.isclose(np.linalg.det(rotation), 1.0)
    normal = np.zeros(3)
    normal["xyz".index(axis)] = sign
    assert np.allclose(rotation @ normal, [0, 0, 1])                      # the machining face looks up
    t_axis, u, v = part["axes"]["t"], part["axes"]["u"], part["axes"]["v"]
    lo, hi = part["box"]["min"]["xyz".index(t_axis)], part["box"]["max"]["xyz".index(t_axis)]
    face_t = hi if sign > 0 else lo
    ring = part["outline"][0]
    points = []
    for pu, pv in ring:
        p = [0.0, 0.0, 0.0]
        p["xyz".index(u)], p["xyz".index(v)], p["xyz".index(t_axis)] = pu, pv, face_t
        x, y, z = apply(item.frame.matrix(), (p[0], p[1], p[2]))
        assert math.isclose(z, ply15.thickness, abs_tol=1e-9)
        points.append((x, y))
    assert Polygon(points).symmetric_difference(item.shape).area < 1e-6


def test_turns_follow_the_grain_and_free_parts_turn_in_quarters():
    with module("m", Box.from_size(depth=600, width=400, height=100)) as m:
        board("along", ply15).on(m.bottom).grain("depth")
        board("across", ply12).on(m.bottom).grain("width")
        board("unset", oak).on(m.bottom)
        board("free", mdf).on(m.bottom)
    by_path = {i.path: i for items in parts_of_layout(build_layout(), 10).by_material.values() for i in items}
    assert by_path["m.along"].turns == (0.0, 180.0) and by_path["m.along"].grained
    assert by_path["m.across"].turns == (90.0, 270.0) and by_path["m.across"].grained
    # A grained part without grain() turns freely [Florian, 2026-10-14].
    assert by_path["m.unset"].turns == (0.0, 90.0, 180.0, 270.0) and not by_path["m.unset"].grained
    assert by_path["m.free"].turns == (0.0, 90.0, 180.0, 270.0)


def test_openings_stay_open_where_a_part_fits_and_the_solver_outline_contains_the_part():
    frame = panel("frame", 1200, 800)
    frame.cut(rect(depth=1000, width=600), at=frame.top.center)            # the opening
    frame.hole(d=40, at=frame.top.front(50).left(50), depth=through)       # too small for any part
    frame.pocket(rect(depth=50, width=50), at=frame.top.front(50), depth=5)     # blind
    panel("small", 300, 200)
    items = {i.path: i for i in parts_of_layout(build_layout(), 10).by_material["birch 15"]}
    item = items["frame.panel"]
    assert len(item.shape.interiors) == 2                    # the opening and the hole
    assert len(item.solver.interiors) == 1                   # the hole is filled
    assert item.solver.buffer(1e-6).contains(item.shape)
    assert item.solver.hausdorff_distance(Polygon(item.solver.exterior)) > 0
    assert Polygon(item.solver.exterior).hausdorff_distance(Polygon(item.shape.exterior)) <= 0.61
    assert item.solver.bounds[:2] == (0.0, 0.0)


def test_a_needle_of_material_does_not_grow_a_spike_on_the_solver_outline():
    """A through hole tangent to the board's end leaves a needle of material
    at the corner; mitred without a limit its growth reached 3.75 mm out
    [found by fuzzing, 2026-10-14]."""
    b = panel("a", 40, 40)
    b.add_hole(b.big_faces()[0], (0.0, 1.0), 2.0, through)
    (item,) = parts_of_layout(build_layout(), 10).by_material["birch 15"]
    outside = max(Polygon(item.shape.exterior).distance(Point(p)) for p in item.solver.exterior.coords)
    assert outside <= OUTSIDE + 1e-9
    assert item.solver.buffer(1e-6).contains(item.shape)


def test_a_notch_whose_mouth_the_growth_closes_is_no_opening():
    """Grown, a notch with a narrow mouth became a hole in the solver's
    outline that no part could go in [found by fuzzing, 2026-10-14]."""
    b = panel("a", 200, 200)
    b.add_cut(Shape(Polygon([(0, 99.7), (60, 99.7), (60, 60), (100, 60), (100, 140), (60, 140), (60, 100.3),
                             (0, 100.3)])), "keyhole")            # a room 40 x 80 behind a slit 0.6 wide
    (item,) = parts_of_layout(build_layout(), 10).by_material["birch 15"]
    assert len(item.shape.interiors) == 0 and len(item.solver.interiors) == 0


def test_a_part_too_large_for_the_bed_or_the_stock_is_refused_by_name():
    panel("long", 2400, 100)
    panel("ok", 500, 300)
    layout = build_layout()
    with pytest.raises(LangError, match=r"long.panel \(2400 x 100\) does not fit the bed 2000 x 1000.*nest\(False\)"):
        check_sizes(parts_of_layout(layout, 10), WORKSHOP)
    small = Workshop(bed=(3000, 2000), sheets=(Sheet("birch 15", 1200, 600),))
    with pytest.raises(LangError, match="long.panel .* fits no stock for birch 15"):
        check_sizes(parts_of_layout(layout, 10), small)


def test_a_grained_part_needs_stock_along_its_grain():
    with module("m", Box.from_size(depth=300, width=1100, height=15)) as m:
        board("b", ply15).on(m.bottom).grain("width")      # 1100 along the grain
    # The sheet is long enough across its grain only.
    narrow = Workshop(bed=(2000, 2000), sheets=(Sheet("birch 15", 800, 1500),))
    with pytest.raises(LangError, match="with its grain along the stock's"):
        check_sizes(parts_of_layout(build_layout(), 10), narrow)


# -- packing -------------------------------------------------------------------------------------------

def _rect_item(i: int, w: float, h: float, turns: tuple[float, ...] = (0.0, 90.0, 180.0, 270.0)) -> Item:
    from lang.nesting.items import PartFrame
    shape = Polygon([(0, 0), (w, 0), (w, h), (0, h)])
    return Item(f"p{i}", "birch 15", 15.0, shape, shape, turns, False,
                PartFrame("z", "x", "y", False, 1, 0.0, 15.0, 0.0, 0.0), "top")


def test_pack_keeps_the_margin_the_spacing_and_clear_of_defects():
    items = [_rect_item(i, 300, 200) for i in range(6)]
    defect = Polygon([(0, 0), (500, 0), (500, 500), (0, 500)])
    result = pack(items, list(range(6)), [Bin(1000, 800, 1, 1.0, [defect])], 10, 10, VARIABLE, 0.5)
    assert not result.unplaced and len(result.packed) == 1
    shapes = [items[p.item].placed(p.turn, p.at) for p in result.packed[0].placements]
    for k, s in enumerate(shapes):
        assert Polygon([(10, 10), (990, 10), (990, 790), (10, 790)]).buffer(1e-6).contains(s)
        assert s.distance(defect) >= 10 - 1e-6
        assert all(s.distance(o) >= 10 - 1e-6 for o in shapes[k + 1:])


def test_knapsack_places_what_fits_when_the_bins_are_short():
    items = [_rect_item(i, 400, 300) for i in range(5)]
    assert pack(items, list(range(5)), [Bin(900, 700, 1, 1.0)], 10, 10, VARIABLE, 0.3).unplaced
    result = pack(items, list(range(5)), [Bin(900, 700, 1, 1.0)], 10, 10, KNAPSACK, 0.3)
    assert len(result.unplaced) == 1 and len(result.packed[0].placements) == 4


def test_a_part_turns_exactly_by_quarters():
    shape = Polygon([(0, 0), (30, 0), (30, 10), (0, 10)])
    assert list(turned(shape, 90).exterior.coords)[:4] == [(0.0, 0.0), (0.0, 30.0), (-10.0, 30.0), (-10.0, 0.0)]


# -- sawing --------------------------------------------------------------------------------------------

def _fits(w: float, h: float) -> bool:
    return (w <= 2000 and h <= 1000) or (w <= 1000 and h <= 2000)


def _keeps(w: float, h: float) -> bool:
    return min(w, h) >= 300 and w * h >= 0.25e6


def test_simplify_joins_blanks_the_bed_takes_together():
    # Two blanks side by side (600 and 700 long, 900 high), a waste strip
    # above them, and a rest beyond.
    sheet = Node([0, 0, 2470, 1240], children=[
        Node([0, 0, 1304, 1240], children=[
            Node([0, 0, 1304, 900], children=[Node([0, 0, 600, 900], [0]), Node([604, 0, 700, 900], [1])]),
            Node([0, 904, 1304, 336])]),
        Node([1308, 0, 1162, 1240])])
    plan = simplify(sheet, _fits, _keeps)
    used = [leaf for leaf in leaves(plan) if leaf.used]
    # Joined: 1304 x 900 fits the bed; the 336 strip above is worth keeping.
    assert len(used) == 1 and used[0].blanks == [0, 1] and used[0].rect == [0, 0, 1304, 900]
    assert cuts(plan) == 2


def test_blanks_are_joined_only_where_their_margins_and_the_kerf_make_the_spacing():
    """Two blanks joined are machined as one piece: their parts are only
    two margins and the kerf apart [found by fuzzing, 2026-10-14: with
    margin and kerf 0, 1.4 mm for a spacing of 10]."""
    sheet = Node([0, 0, 2470, 1240], children=[Node([0, 0, 600, 900], [0]), Node([600, 0, 700, 900], [1]),
                                               Node([1300, 0, 1170, 1240])])
    joined = simplify(sheet, _fits, _keeps, join=True)
    apart = simplify(sheet, _fits, _keeps, join=False)
    assert [leaf.blanks for leaf in leaves(joined) if leaf.used] == [[0, 1]]
    assert [leaf.blanks for leaf in leaves(apart) if leaf.used] == [[0], [1]]


def test_two_rests_side_by_side_are_one():
    sheet = Node([0, 0, 2470, 1240], children=[
        Node([0, 0, 1000, 1240], [0]), Node([1004, 0, 700, 1240]), Node([1708, 0, 762, 1240])])
    plan = simplify(sheet, _fits, _keeps)
    assert [leaf.rect for leaf in leaves(plan)] == [[0, 0, 1000, 1240], [1004, 0, 1466, 1240]]


def test_a_thin_waste_strip_goes_along_with_the_pieces_beside_it():
    # A strip 136 high along the top of a sheet whose lower part is cut into
    # a blank and a rest: the pieces under it take it along.
    sheet = Node([0, 0, 2470, 1240], children=[
        Node([0, 0, 2470, 1100], children=[Node([0, 0, 900, 1100], [0]), Node([904, 0, 1566, 1100])]),
        Node([0, 1104, 2470, 136])])
    plan = simplify(sheet, _fits, _keeps)
    assert [leaf.rect for leaf in leaves(plan)] == [[0, 0, 900, 1240], [904, 0, 1566, 1240]]
    assert cuts(plan) == 1


def test_a_sliver_narrower_than_the_kerf_is_trimmed_off():
    """A 2.5 mm strip beside a blank at the sheet's edge, narrower than the
    kerf, left the piece over the bed [found by fuzzing, 2026-10-15]."""
    def bed(w: float, h: float) -> bool:
        return (w <= 781 and h <= 1166) or (w <= 1166 and h <= 781)
    leaf = Node([676, 0, 130, 1168.5], [0])
    out = sawing.trim_to_bed(leaf, [(130, 1166)], {0: (676.0, 0.0)}, 4, bed)
    (used,) = leaves(out)
    assert used.rect == [676, 0, 130, 1166] and used.blanks == [0] and cuts(out) == 1
    (cut,) = cut_list(out, 4)
    assert cut.line == (676, 1168, 806, 1168) and cut.piece == (676, 0, 130, 1168.5)


def test_cuts_come_in_order_through_their_pieces():
    tree = Node([0, 0, 2000, 1000], children=[
        Node([0, 0, 1000, 1000], children=[Node([0, 0, 1000, 500], [0]), Node([0, 504, 1000, 496], [1])]),
        Node([1004, 0, 996, 1000], [2])])
    out = cut_list(tree, 4)
    assert [c.line for c in out] == [(1002, 0, 1002, 1000), (0, 502, 1000, 502)]
    assert out[1].piece == (0, 0, 1000, 1000)


def test_a_piece_larger_than_the_bed_is_cut_down_to_its_blank():
    leaf = Node([0, 0, 2470, 900], [0])
    out = sawing.trim_to_bed(leaf, [(1900, 900)], {0: (0.0, 0.0)}, 4, _fits)
    assert [lf.rect for lf in leaves(out)] == [[0, 0, 1900, 900], [1904, 0, 566, 900]]
    assert leaves(out)[0].blanks == [0] and leaves(out)[1].rest


def test_each_blank_lies_where_the_saw_plan_puts_it():
    """The guillotine solver gives its tree's root the item id 0: blank 0
    was taken to lie at the sheet's corner, and its parts ended up outside
    their blank [found comparing blank prices, 2026-10-14]."""
    stock = [sawing.Stock(2470, 1240, -1, 2470 * 1240, "bought", 0)]
    sizes = [(591, 1219), (591, 1219), (591, 1234), (591, 1240)]
    for setting in sawing.SETTINGS:
        trees, origins = sawing._solve(sizes, stock, 4, 0.1, knapsack=False, **setting)  # pyright: ignore[reportPrivateUsage]
        assert sorted(origins) == [0, 1, 2, 3]
        for tree, _k in trees:
            for leaf in leaves(tree):
                for bi in leaf.blanks:
                    (bx, by), (bw, bh) = origins[bi], sizes[bi]
                    x, y, w, h = leaf.rect
                    assert x <= bx and y <= by and bx + bw <= x + w and by + bh <= y + h


def test_a_sheet_of_a_fraction_of_a_millimetre_is_sawn_whole():
    """The guillotine solver takes whole millimetres; the pieces must still
    cover the sheet [found by fuzzing, 2026-10-14]."""
    stock = [sawing.Stock(500, 400.5, -1, 500 * 400.5, "bought", 0)]
    plan = sawing.best_plan([(60, 60)], stock, 0, 1, _fits, _keeps, 0.05)
    (sheet,) = plan.sheets
    assert sheet.tree.rect == [0, 0, 500, 400.5]
    assert sum(leaf.rect[2] * leaf.rect[3] for leaf in leaves(sheet.tree)) == pytest.approx(500 * 400.5)


def test_a_kerf_in_tenths_of_a_millimetre_is_sawn_as_it_is():
    """In whole millimetres a kerf of 3.2 was sawn as 4: two blanks that
    fill a sheet but for one kerf found no room, and elsewhere the pieces
    between the cuts grew by the difference, past the bed [found by
    fuzzing, 2026-10-14]."""
    stock = [sawing.Stock(1203.2, 500, 1, 1203.2 * 500, "on_hand", 0)]
    def small_bed(w: float, h: float) -> bool:                # takes one blank, not both
        return w <= 1000 and h <= 1000
    plan = sawing.best_plan([(600, 500), (600, 500)], stock, 3.2, 5, small_bed, _keeps, 0.05)
    assert not plan.unsawn
    (sheet,) = plan.sheets
    assert [leaf.rect for leaf in leaves(sheet.tree)] == [[0, 0, 600, 500], [603.2, 0, 600, 500]]
    assert Workshop(kerf=3.25).saw_kerf == 3.3 and Workshop(kerf=3.2).saw_kerf == 3.2


def test_best_plan_saws_every_blank_or_says_which_it_could_not():
    stock = [sawing.Stock(2470, 1240, 1, 2470 * 1240, "on_hand", 0)]
    plan = sawing.best_plan([(1000, 600), (1000, 600), (1200, 500)], stock, 4, 5, _fits, _keeps, 0.1)
    assert not plan.unsawn and len(plan.sheets) == 1 and plan.over == 0
    short = sawing.best_plan([(2000, 1000), (2000, 1000)], stock, 4, 5, _fits, _keeps, 0.1)
    assert len(short.unsawn) == 1 and len(short.sheets) == 1


# -- whole nests --------------------------------------------------------------------------------------

def test_a_nest_places_every_part_once_and_checks_clean():
    for k, (w, h) in enumerate([(600, 400), (800, 300), (500, 500), (1200, 350), (300, 200)] * 2):
        panel(f"p{k}", w, h)
    panel("q", 700, 400, ply12)
    layout, nest, parts = nested()
    assert nest["version"] == NEST_VERSION and nest["layout_hash"] == layout_hash(layout)
    assert nest["problems"] == []
    assert {k: len(v) for k, v in placements(nest).items()} == {
        i.path: 1 for items in parts.by_material.values() for i in items}
    assert [m["material"] for m in nest["materials"]] == ["birch 12", "birch 15"]
    for m in nest["materials"]:
        assert sum(m["bought"].values()) == len(m["sheets"])
        assert math.isclose(m["parts_area"], sum(i.area for i in parts.by_material[m["material"]]) / 1e6)
        assert math.isclose(m["used_area"], m["stock_area"] - m["kept_area"])
        assert m["kept_area"] == pytest.approx(sum(r["rect"][2] * r["rect"][3] for s in m["sheets"]
                                                   for r in s["rests"] if r["keep"]) / 1e6)


def test_a_piece_on_hand_the_bed_takes_is_used_as_it_is_and_first():
    panel("a", 500, 300)
    panel("b", 400, 250)
    workshop = Workshop(bed=(2000, 1000), sheets=SHEETS, on_hand=(OnHand("birch 15", 1000, 700),))
    _layout, nest, _parts = nested(workshop)
    (m,) = nest["materials"]
    assert m["bought"] == {} and m["on_hand_used"] == ["1000x700"]
    (sheet,) = m["sheets"]
    assert sheet["stock"] == "offcut" and not sheet["bought"] and sheet["cuts"] == []
    assert sheet["blanks"][0]["rect"] == [0, 0, 1000, 700]
    assert nest["problems"] == []


def test_a_piece_on_hand_larger_than_the_bed_is_sawn_like_a_sheet():
    for k in range(2):
        panel(f"p{k}", 900, 500)
    workshop = Workshop(bed=(2000, 1000), sheets=SHEETS, on_hand=(OnHand("birch 15", 2470, 600),))
    _layout, nest, _parts = nested(workshop)
    (m,) = nest["materials"]
    assert m["on_hand_used"] == ["2470x600"] and nest["problems"] == []
    offcut = next(s for s in m["sheets"] if s["stock"] == "offcut")
    assert not offcut["bought"]
    assert offcut["cuts"] and all(_fits(b["rect"][2], b["rect"][3]) for b in offcut["blanks"])


def test_a_blank_as_long_as_a_bed_of_fractions_is_sawn_within_it():
    """A blank as wide as a bed 846.352 wide was sawn 846.4, the saw's
    tenths rounded up, and did not fit the bed [found by fuzzing,
    2026-10-15]."""
    panel("a", 1100, 820)
    workshop = Workshop(bed=(2250.12, 846.352), margin=12.3, kerf=6, sheets=(Sheet("birch 15", 2602.8, 996.98),))
    _layout, nest, _parts = nested(workshop)
    assert nest["problems"] == []
    from lang.nesting.nest import _blank_types, _stock_of  # pyright: ignore[reportPrivateUsage]
    bins, _kinds = _blank_types(_stock_of("birch 15", workshop), workshop)
    assert all(b.width * 10 == round(b.width * 10) and b.height * 10 == round(b.height * 10) for b in bins)
    assert max(b.height for b in bins if b.width > 1000) == 846.3      # as wide as the bed, in tenths


def test_short_stock_leaves_parts_over_and_says_so():
    for k in range(4):
        panel(f"p{k}", 1900, 900)
    workshop = Workshop(bed=(2000, 1000), on_hand=(OnHand("birch 15", 2470, 1240, 2),))
    _layout, nest, _parts = nested(workshop)
    (m,) = nest["materials"]
    assert m["bought"] == {} and m["on_hand_used"] == ["2470x1240"] * 2 and len(m["unplaced"]) == 2
    assert all(s["stock"] == "offcut" and not s["bought"] for s in m["sheets"])
    assert any("left over" in p for p in nest["problems"])
    assert not [p for p in nest["problems"] if "left over" not in p]


def test_parts_go_into_the_opening_of_a_frame():
    frame = panel("frame", 1300, 900)
    frame.cut(rect(depth=1100, width=700), at=frame.top.center)
    for k in range(4):
        panel(f"small{k}", 400, 250)
    workshop = Workshop(bed=(1400, 1000), on_hand=(OnHand("birch 15", 1400, 1000),))
    _layout, nest, parts = nested(workshop)
    assert nest["problems"] == []
    (m,) = nest["materials"]
    (sheet,) = m["sheets"]
    (blank,) = sheet["blanks"]
    items = {i.path: i for i in parts.by_material["birch 15"]}
    shapes = {p["path"]: items[p["path"]].placed(p["turn"], (p["at"][0], p["at"][1])) for p in blank["parts"]}
    opening = Polygon(shapes["frame.panel"].interiors[0])
    assert all(opening.contains(shapes[f"small{k}.panel"]) for k in range(4))


def test_refill_empties_a_sheet_into_the_room_on_another():
    items = [_rect_item(0, 1000, 600), _rect_item(1, 400, 300)]
    ws = Workshop(bed=(2000, 1000), sheets=SHEETS)
    # Sheet one: the big part on a blank, a big rest beside it; sheet two: the small part.
    one = Node([0, 0, 2470, 1240], children=[Node([0, 0, 1020, 1240], parts=[PartOn(0, 0.0, (10.0, 10.0))]),
                                             Node([1024, 0, 1446, 1240])])
    two = Node([0, 0, 2470, 1240], children=[Node([0, 0, 420, 1240], parts=[PartOn(1, 0.0, (10.0, 10.0))]),
                                             Node([424, 0, 2046, 1240])])
    sheets = refill(items, [SheetState(one, (2470, 1240), "bought", "2470x1240"),
                            SheetState(two, (2470, 1240), "bought", "2470x1240")], ws, 0.3, "anytime", lambda _: None)
    assert len(sheets) == 1
    on = [p.item for leaf in leaves(sheets[0].tree) for p in leaf.parts]
    assert sorted(on) == [0, 1]
    assert cuts(sheets[0].tree) <= ws.max_cuts


def test_verify_finds_what_is_wrong():
    panel("a", 600, 400)
    panel("b", 500, 300)
    _layout, nest, parts = nested()
    items = parts.by_material["birch 15"]
    (m,) = nest["materials"]
    blank = m["sheets"][0]["blanks"][0]
    p0 = blank["parts"][0]
    p0["at"] = [0.0, 0.0]                                  # into the margin
    blank["parts"].append(p0.copy())                       # and twice
    m["sheets"][0]["cuts"].append({"line": [5, 5, 6, 6], "piece": [0, 0, 1, 1]})
    m["sheets"][0]["rests"].append({"rect": [-10, 0, 5, 5], "keep": True})
    problems = verify(m, items, WORKSHOP)
    text = "\n".join(problems)
    assert "not the margin 10 inside" in text and "placed 2 times" in text and "overlap" in text
    assert "not straight" in text and "off the sheet" in text and "marked kept" in text


def test_a_nest_file_draws_and_reads_back():
    a = panel("a", 600, 400)
    a.cut(rect(depth=200, width=100), at=a.top.center)
    panel("b", 500, 300).grain("depth")
    _layout, nest, parts = nested()
    again = json.loads(json.dumps(nest))
    assert again == nest
    items = {i.path: i for items in parts.by_material.values() for i in items}
    svg = draw_nest(nest, items)
    assert svg.startswith("<svg") and 'data-path="a.panel"' in svg and 'data-path="b.panel"' in svg
    assert 'class="grain"' in svg


def test_each_part_s_transform_puts_it_flat_on_its_blank():
    a = panel("a", 600, 400)
    a.pocket(rect(depth=100, width=100), at=a.bottom.center, depth=5)       # machined from below
    with module("s", Box.from_size(depth=500, width=300, height=700)) as m:
        board("side", ply15).on(m.left)
    layout, nest, parts = nested()
    items = {i.path: i for items in parts.by_material.values() for i in items}
    by_path = {p["path"]: p for mod in layout["modules"] for p in mod["parts"]}
    for s in nest["materials"][0]["sheets"]:
        for b in s["blanks"]:
            for p in b["parts"]:
                part, item = by_path[p["path"]], items[p["path"]]
                lo, hi = part["box"]["min"], part["box"]["max"]
                corners = [(x, y, z) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
                mapped = [apply(p["transform"], c) for c in corners]
                assert min(c[2] for c in mapped) == pytest.approx(0) and max(c[2] for c in mapped) == pytest.approx(15)
                xs, ys = [c[0] for c in mapped], [c[1] for c in mapped]
                x0, y0, x1, y1 = item.placed(p["turn"], (p["at"][0], p["at"][1])).bounds
                assert (min(xs), min(ys), max(xs), max(ys)) == pytest.approx((x0, y0, x1, y1), abs=1e-6)
                assert 0 <= min(xs) and max(xs) <= b["rect"][2] and 0 <= min(ys) and max(ys) <= b["rect"][3]


# -- the emitter's reading -------------------------------------------------------------------------------

def test_moved_facts_put_the_machining_face_up():
    from lang.emit.nested import moved_facts
    from lang.emit.plan import PartFacts
    quarter = [[0.0, -1.0, 0.0, 5.0], [0.0, 0.0, 1.0, 0.0], [-1.0, 0.0, 0.0, 15.0]]    # y up, x along -y
    facts = moved_facts(PartFacts("birch 15", 15, "board", True, (0.0, 1.0, 0.0), (-1.0, 0.0, 0.0)), quarter)
    assert facts.up == (0.0, 0.0, 1.0) and facts.grain == (-1.0, 0.0, 0.0)


def test_the_emitter_reads_the_nest_version_the_nest_writes():
    assert EMIT_NEST_VERSION == NEST_VERSION


def test_the_emitter_plans_a_document_per_material_with_blanks_where_the_nest_put_them():
    panel("a", 600, 400)
    panel("b", 700, 300, ply12)
    layout, nest, _parts = nested()
    docs = plan_nest(nest, layout)
    assert [d.material for d in docs] == ["birch 12", "birch 15"]
    for doc, m in zip(docs, nest["materials"]):
        assert [s.name for s in doc.sheets] == [s["name"] for s in m["sheets"]]
        for sheet, s in zip(doc.sheets, m["sheets"]):
            for blank, b in zip(sheet.blanks, s["blanks"]):
                assert blank.size == (b["rect"][2], b["rect"][3], m["thickness"])
                assert blank.origin[:2] == (b["rect"][0], sheet.origin[1] + b["rect"][1])
                assert [p.path for p in blank.parts] == [p["path"] for p in b["parts"]]
                for placed, p in zip(blank.parts, b["parts"]):     # the blank's transform, moved to the blank
                    point = (12.5, -3.0, 7.0)
                    on_blank, in_doc = apply(p["transform"], point), apply(placed.transform, point)
                    assert in_doc == pytest.approx((on_blank[0] + blank.origin[0], on_blank[1] + blank.origin[1],
                                                    on_blank[2]))
    assert [d.material for d in plan_nest(nest, layout, "birch 12")] == ["birch 12"]
    with pytest.raises(ValueError, match="no material"):
        plan_nest(nest, layout, "oak 20")
    with pytest.raises(ValueError, match="nest version 0"):
        plan_nest({**nest, "version": 0}, layout)


# -- a nest of the build -----------------------------------------------------------------------------

def test_a_nest_of_the_build_is_nested_with_its_settings_and_named_and_dated():
    use(nesting.bed((2000, 1000)), nesting.seconds(0.5), nesting.refill(False))
    sized = sheet_material("birch", t=15, size=(2500, 1250))
    with module("m", Box.from_size(depth=600, width=400, height=300)) as m:
        board("bottom", sized).on(m.bottom)
        board("top", sized).on(m.top)
        m.nest("carcass", material=sized).use(nesting.margin(12))
    layout = build_layout()
    when = datetime(2026, 10, 16, 9, 30)
    nest, _parts = nest_layout(layout, "m.carcass", options=Options(saw_seconds=0.1), written=when)
    assert nest["version"] == NEST_VERSION == 3 and nest["name"] == "m.carcass"
    assert nest["written"].startswith("2026-10-16T09:30:00") and nest["follows"] == "" and nest["reasons"] == {}
    prints = fingerprints(layout)
    placed = [p for s in nest["materials"][0]["sheets"] for b in s["blanks"] for p in b["parts"]]
    assert sorted(p["path"] for p in placed) == ["m.bottom", "m.top"]
    assert all(p["fingerprint"] == prints[p["path"]] for p in placed)
    settings = nest["settings"]
    assert settings["margin"] == 12 and settings["seconds"] == 0.5 and settings["refill"] is False
    assert settings["sources"]["nesting.margin"] == "m.carcass" and settings["sources"]["nesting.bed"] == "root"
    assert settings["buy"] == {"birch 15": "2500x1250"} and settings["on_hand"] == []
    (material,) = nest["materials"]
    assert material["bought"] == {"2500x1250": 1} and material["sheets"][0]["stock"] == "sheet"
    assert material["notes"][0] == "time: 0.5 s for 2 parts" and nest["problems"] == []


def test_bought_counts_only_the_sheets_bought_and_the_settings_the_time_limit():
    """Version 1 counted the sheets on hand as bought, and recorded the time
    of the last material as `seconds` (the nesting review's bugs, 2026-10-16)."""
    for k in range(3):
        panel(f"p{k}", 1900, 900)
    workshop = Workshop(bed=(2000, 1000), seconds=7, sheets=(Sheet("birch 15", 2470, 1240),),
                        on_hand=(OnHand("birch 15", 2470, 1240),))
    _layout, nest, _parts = nested(workshop, Options(seconds=None, saw_seconds=0.1, refill_seconds=0))
    (m,) = nest["materials"]
    assert m["on_hand_used"] == ["2470x1240"] and m["bought"] == {"2470x1240": 2}
    assert [s["bought"] for s in m["sheets"]] == [False, True, True]
    assert [s["stock"] for s in m["sheets"]] == ["sheet"] * 3            # a whole sheet on hand is a sheet
    assert nest["settings"]["seconds"] == 7 and m["notes"][0] == "time: 5 s for 3 parts"


def test_between_two_parts_the_larger_spacing_holds():
    use(nesting.bed((1000, 600)))
    with module("m", Box.from_size(depth=400, width=300, height=300)) as m:
        board("wide", ply15).on(m.bottom).use(nesting.spacing(40))
    for k in range(3):
        with module(f"s{k}", Box.from_size(depth=300, width=200, height=15, origin=(0, 500 + 300 * k, 0))) as s:
            board("small", ply15).on(s.bottom)
    layout = build_layout()
    paths = [p["path"] for mod in layout["modules"] for p in mod["parts"]]
    r_spacing = {"m.wide": 40.0} | {p: 10.0 for p in paths if p != "m.wide"}
    workshop = Workshop(bed=(1000, 600), sheets=(Sheet("birch 15", 1000, 600),))
    nest, parts = nest_parts(layout, None, workshop, spacing_of=r_spacing, options=FAST)
    assert nest["problems"] == [] and nest["settings"]["part_spacing"] == {"m.wide": 40.0}
    items = {i.path: i for i in parts.by_material["birch 15"]}
    assert items["m.wide"].spacing == 40 and items["s0.small"].spacing == 10
    # Grown by the difference: 30 mm more than the least all round.
    assert items["m.wide"].solver.bounds[2] == pytest.approx(400 + 2 * 30.375, abs=0.3)
    for m_ in nest["materials"]:
        for sheet in m_["sheets"]:
            for blank in sheet["blanks"]:
                shapes = {p["path"]: items[p["path"]].placed(p["turn"], (p["at"][0], p["at"][1]))
                          for p in blank["parts"]}
                if "m.wide" in shapes:
                    assert all(shapes["m.wide"].distance(o) >= 40 - 1e-4 for p, o in shapes.items() if p != "m.wide")


def test_verify_holds_each_pair_to_the_larger_of_their_spacings():
    a, b = _rect_item(0, 300, 200), _rect_item(1, 300, 200)
    a.spacing = 30
    from lang.nesting.verify import _check_spacing  # pyright: ignore[reportPrivateUsage]
    near = [a.placed(0, (0, 0)), b.placed(0, (320, 0))]
    assert _check_spacing(near, [a, b]) == ["p0 and p1: 20.0000 apart, less than 30"]
    assert _check_spacing([a.placed(0, (0, 0)), b.placed(0, (330, 0))], [a, b]) == []


# -- a nest(False) board named in a nest ---------------------------------------------------------------

def test_a_nest_false_board_named_in_a_nest_is_its_own_blank_sawn_to_size():
    use(nesting.bed((1200, 800)))
    sized = sheet_material("birch", t=15, size=(2500, 1250))
    with module("m", Box.from_size(depth=2200, width=300, height=300)) as m:
        long = board("long", sized).on(m.bottom).nest(False)              # 2200 x 300, longer than the bed
        long.cut(rect(depth=100, width=50), at=long.top.front.left)       # a notch: its outline cut by hand
        top = board("top", sized).on(m.top).between(m.front, m.front.into(500))
        m.nest("all", [long, top])
    layout = build_layout()
    nest, parts = nest_layout(layout, "m.all", options=FAST)
    assert nest["problems"] == []
    (material,) = nest["materials"]
    (sheet,) = material["sheets"]
    own = [b for b in sheet["blanks"] if b["own_blank"]]
    (blank,) = own
    assert blank["rect"][2:] == pytest.approx([2200, 300]) and [p["path"] for p in blank["parts"]] == ["m.long"]
    assert not any(b["own_blank"] for b in sheet["blanks"] if b is not blank)
    assert any(r["keep"] for r in sheet["rests"])                       # the rest beside it is kept
    item = next(i for i in parts.by_material["birch 15"] if i.path == "m.long")
    assert item.own and item.shape.area < 2200 * 300                      # its outline whole, the notch in it
    (p,) = blank["parts"]
    assert item.placed(p["turn"], (p["at"][0], p["at"][1])).bounds == pytest.approx((0, 0, 2200, 300))
    svg = draw_nest(nest, {i.path: i for i in parts.by_material["birch 15"]})
    assert 'class="blank own"' in svg and "sawn to size" in svg


def test_an_own_blank_keeps_its_grain_along_the_sheet_and_must_fit_the_stock():
    use(nesting.bed((1000, 600)))
    with module("m", Box.from_size(depth=300, width=1200, height=300)) as m:
        across = board("across", ply15).on(m.bottom).grain("depth").nest(False)     # 300 along its grain
        m.nest("own", [across])
    layout = build_layout()
    workshop = Workshop(bed=(1000, 600), sheets=(Sheet("birch 15", 2470, 1240),))
    nest, _parts = nest_parts(layout, ["m.across"], workshop, options=FAST)
    (blank,) = [b for s in nest["materials"][0]["sheets"] for b in s["blanks"]]
    assert blank["own_blank"] and blank["rect"][2:] == pytest.approx([300, 1200])
    short = Workshop(bed=(1000, 600), sheets=(Sheet("birch 15", 2470, 1000),))
    with pytest.raises(LangError, match=r"m.across \(300 x 1200\), its own blank, fits no stock for birch 15 with "
                                        "its grain along the stock's"):
        nest_parts(layout, ["m.across"], short, options=FAST)


def test_an_own_blank_is_never_joined_and_nothing_is_nested_onto_it():
    leaf = Node([0, 0, 1000, 800], children=[Node([0, 0, 400, 800], [0]), Node([404, 0, 40, 800])])
    joined = simplify(leaf, _fits, _keeps)
    assert [lf.rect for lf in leaves(joined)] == [[0, 0, 1000, 800]]                # a waste strip goes along
    own = simplify(leaf, _fits, _keeps, own={0})
    assert [lf.rect for lf in leaves(own)] == [[0, 0, 400, 800], [404, 0, 40, 800]]
    big = Node([0, 0, 2470, 400], [0])
    out = sawing.trim_to_bed(big, [(2200, 300)], {0: (0.0, 0.0)}, 4, _fits, own={0})
    # Cut down to its blank though the bed would take less, longer than the bed.
    assert [lf.rect for lf in leaves(out)] == [[0, 0, 2200, 300], [0, 304, 2200, 96], [2204, 0, 266, 400]]
    assert leaves(out)[0].blanks == [0] and cuts(out) == 2


# -- the command line ----------------------------------------------------------------------------------

_SHOP = """from lang import *
ply = sheet_material('birch', t=15, size=(2470, 1240))
thin = sheet_material('birch', t=9, size=(2470, 1240))
use(nesting.bed((2000, 1000)), nesting.seconds(0.5))
with module('m', Box.from_size(depth=600, width=400, height=300)) as m:
    board('bottom', ply).on(m.bottom)
    board('back', thin).on(m.back)
    board('strip', ply).on(m.left).nest(False)
with module('n', Box.from_size(depth=600, width=400, height=300, origin=(0, 1000, 0))) as n:
    board('bottom', ply).on(n.bottom)
"""


def test_the_command_line_nests_a_build_s_nests_each_into_its_folder(tmp_path: Path,
                                                                    capsys: pytest.CaptureFixture[str]):
    (tmp_path / "shop.py").write_text(_SHOP)
    out = tmp_path / "out"
    assert nest_main([str(tmp_path / "shop.py"), "--out", str(out), "--no-refill"]) == 0
    printed = capsys.readouterr().out
    assert "m.birch_15: birch 15: bought 1 x 2470x1240" in printed and "not nested: m.strip (nest(False))" in printed
    assert sorted(str(p.relative_to(out)) for p in out.rglob("nest.json")) == [
        "m/birch_15/nest.json", "m/birch_9/nest.json", "n/birch_15/nest.json"]
    nest = json.loads((out / "m" / "birch_15" / "nest.json").read_text())
    layout: Layout = json.loads((out / "m" / "birch_15" / "nest.layout.json").read_text())
    assert nest["name"] == "m.birch_15" and nest["layout_hash"] == layout_hash(layout) and nest["problems"] == []
    assert [p["path"] for p in nest["left_out"]] == ["m.strip"]
    assert (out / "m" / "birch_15" / "nest.svg").read_text().startswith("<svg")


def test_the_command_line_nests_the_nests_named_and_refuses_others(tmp_path: Path,
                                                                  capsys: pytest.CaptureFixture[str]):
    (tmp_path / "shop.py").write_text(_SHOP)
    out = tmp_path / "out"
    assert nest_main([str(tmp_path / "shop.py"), "n.birch_15", "--out", str(out), "--no-refill"]) == 0
    assert [str(p.relative_to(out)) for p in out.rglob("nest.json")] == ["n/birch_15/nest.json"]
    assert nest_main([str(tmp_path / "shop.py"), "n.oak", "--out", str(out)]) == 1
    err = capsys.readouterr().err
    assert "No nest n.oak in" in err and "(its nests: m.birch_15, m.birch_9, n.birch_15)" in err


def test_the_command_line_reads_the_inventory_and_its_nests_share_it(tmp_path: Path):
    (tmp_path / "shop.py").write_text(_SHOP)
    (tmp_path / "inventory.toml").write_text('[[stock]]\nmaterial = "birch 15"\nsize = [1000, 700]\n')
    out = tmp_path / "out"
    assert nest_main([str(tmp_path / "shop.py"), "m.birch_15", "n.birch_15", "--out", str(out), "--no-refill"]) == 0
    m = json.loads((out / "m" / "birch_15" / "nest.json").read_text())
    n = json.loads((out / "n" / "birch_15" / "nest.json").read_text())
    assert m["materials"][0]["on_hand_used"] == ["1000x700"] and m["materials"][0]["bought"] == {}
    assert n["materials"][0]["on_hand_used"] == [] and n["materials"][0]["bought"] == {"2470x1240": 1}
    assert m["settings"]["on_hand"] == ["birch 15:1000x700"] and n["settings"]["on_hand"] == []
    other = tmp_path / "other.toml"
    other.write_text('[[stock]]\nmaterial = "birch 15"\nsize = [900, 650]\ncount = 2\n')
    assert nest_main([str(tmp_path / "shop.py"), "n.birch_15", "--inventory", str(other), "--out", str(out),
                      "--no-refill"]) == 0
    n = json.loads((out / "n" / "birch_15" / "nest.json").read_text())
    assert n["materials"][0]["on_hand_used"] == ["900x650"]


def test_the_command_line_goes_on_past_a_nest_it_cannot_nest(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    wide = "    n.nest('wide', [board('wide', thin).on(n.top)]).use(nesting.bed((300, 300)))\n"
    (tmp_path / "shop.py").write_text(_SHOP + wide)
    out = tmp_path / "out"
    assert nest_main([str(tmp_path / "shop.py"), "--out", str(out), "--no-refill"]) == 1
    err = capsys.readouterr().err
    assert "n.wide: error: These parts cannot be nested" in err
    assert (out / "n" / "birch_15" / "nest.json").exists() and not (out / "n" / "wide").exists()


def test_the_command_line_takes_a_layout_file(tmp_path: Path):
    from lang.build import run_build
    run_build(EXAMPLES / "shelf.py", tmp_path / "shelf", scene=False)
    out = tmp_path / "nest"
    assert nest_main([str(tmp_path / "shelf" / "layout.json"), "shelf.birch_18", "--out", str(out),
                      "--no-refill"]) == 0
    nest = json.loads((out / "shelf" / "birch_18" / "nest.json").read_text())
    assert nest["name"] == "shelf.birch_18" and nest["problems"] == []
    assert nest["materials"][0]["bought"] == {"2500x1250": 1}


def test_the_examples_parts_nest_together_through_a_merged_layout():
    """One source per nest: nesting several build files together is a test
    helper's work, `merged_layouts` (the measurements over the examples)."""
    layout = merged_layouts([EXAMPLES / "shelf.py", EXAMPLES / "hatch.py"])
    workshop = Workshop(bed=(2000, 1000), sheets=(Sheet("birch 18", 2500, 1250),))
    nest, _parts = nest_parts(layout, None, workshop, material="birch 18", options=FAST)
    paths = set(placements(nest))
    assert any(p.startswith("shelf:") for p in paths) and any(p.startswith("hatch:") for p in paths)
    assert [m["material"] for m in nest["materials"]] == ["birch 18"] and nest["problems"] == []
