"""Ball catches for inspection hatches (`lang.hardware.ball_catches`), drilled
as the ball_catch add-in drills them.

The standard case: a 15 mm floor panel on the module's bottom (z 0 to 15),
showing its top, so the catches go on its underside (z = 0). The opening is
`rect(width=400, depth=300).rounded(20)` in the middle of the 800 x 1000
module: x 350 to 650 (depth), y 200 to 600 (width; left is -y in the van's
terms). The straight part of its left and right edges runs from x 370 to
630 (260 long), that of its front and back edges from y 220 to 580 (360).

The expected positions are worked out by hand from the add-in's code
(addins-src/ball_catch/main.py, `_spaced_sides`, `_catch`): the selected
edge takes (n + 1) // 2 catches, the opposite edge n // 2; one catch on an
edge sits at length / 2, more at End Offset + k * (length - 2 * End
Offset) / (count - 1); the holder hole 8.4 mm outward into the frame, the
ball hole 9.4 mm inward. With the defaults (4 catches, End Offset 40) the
left edge gets catches 40 and 220 from x 370, at x 410 and 590.
"""
import math
from pathlib import Path
from typing import Any, get_args

import pytest
from shapely.geometry.polygon import orient

from lang import *
from lang.build import run_build
from lang.core.layout import build_layout
from lang.core.layout_types import HardwareLayout
from lang.core.ops import Hole
from lang.core.scope import registry
from lang.emit.arcs import Arc2, Line2, fit
from lang.emit.plan import Arc, FaceRef, HoleStep, plan_layout
from lang.hardware.ball_catches import CATCH_SHAPES, BallCatch, CatchModel
from lib import ball_catches as data
from helpers import ply12, ply15

BOX = Box.from_size(width=800, depth=1000, height=100)
#: The placeholder boxes; the expectations below follow them, so measured
#: numbers only change this table.
SHAPE = CATCH_SHAPES["GN 450"]
HOLDER, WEBS, JAW, BALL = SHAPE.holder, SHAPE.webs, SHAPE.jaw, SHAPE.ball


def _floor(catch: BallCatch | None = None, edge: str | None = "left", front: bool = False,
           shape: Shape | None = None) -> tuple[Scope, Board, Board]:
    """The standard panel, its opening and a hatch from `catch.hatch()`,
    with the catches mounted on the opening's `edge` (none when None), in a
    module in the van's terms or in a cabinet opening the same way
    (front=box.front), whose left is the van's right."""
    catch = catch or BallCatch()
    with (module("floor", BOX, front=BOX.front) if front else module("floor", BOX)) as f:
        panel = board("panel", ply15).on(f.bottom).show(f.top)
        panel.cut(shape or rect(width=400, depth=300).rounded(20), at=panel.top.center, name="opening")
        hatch = catch.hatch("hatch", panel.opening)
        if catch.at is not None:
            f.mount(catch, opening=panel.opening, hatch=hatch)
        elif edge is not None:
            f.mount(catch, opening=panel.opening, edge=panel.opening.side(edge), hatch=hatch)
    return f, panel, hatch


def _holes(part: Board) -> dict[str | None, tuple[float, float]]:
    return {op.name: (op.u, op.v) for op in part.ops if isinstance(op, Hole)}


def test_four_catches_by_default_two_on_each_edge():
    _, panel, hatch = _floor()
    # holders 8.4 outside the contour (left edge y = 200, right edge y = 600)
    assert _holes(panel) == {"catch_hatch_1": (410, 191.6), "catch_hatch_2": (590, 191.6),
                             "catch_hatch_3": (410, 608.4), "catch_hatch_4": (590, 608.4)}
    # balls 9.4 inside it, in the hatch
    assert _holes(hatch) == {"catch_panel_1": (410, 209.4), "catch_panel_2": (590, 209.4),
                             "catch_panel_3": (410, 590.6), "catch_panel_4": (590, 590.6)}
    # Ø2 x 4 pilot holes from the underside, the faces that are not shown
    for part in (panel, hatch):
        holes = [op for op in part.ops if isinstance(op, Hole)]
        assert all(h.face == "bottom" and h.d == 2 and h.depth == 4 and not h.through for h in holes)


@pytest.mark.parametrize("count, left, right", [
    (1, [500], []),                          # one catch, centred on the edge named
    (2, [500], [500]),                       # one on each edge, centred
    (3, [410, 590], [500]),                  # the edge named gets the extra one
    (5, [410, 500, 590], [410, 590]),        # 40, 130, 220 from x 370
])
def test_an_odd_count_gives_the_edge_named_one_more(count: int, left: list[float], right: list[float]):
    _, panel, _ = _floor(BallCatch(count=count))
    holes = _holes(panel).values()
    assert sorted(u for u, v in holes if v == 191.6) == left
    assert sorted(u for u, v in holes if v == 608.4) == right
    assert len(holes) == count


def test_end_offset_and_the_other_pair_of_edges():
    _, panel, _ = _floor(BallCatch(end=60))
    assert sorted({u for u, _ in _holes(panel).values()}) == [430, 570]       # 60 and 200 from x 370
    registry.reset()
    # on the front edge (x = 350, straight from y 220 to 580) and the back edge
    _, panel, hatch = _floor(edge="front")
    assert _holes(panel) == {"catch_hatch_1": (341.6, 260), "catch_hatch_2": (341.6, 540),
                             "catch_hatch_3": (658.4, 260), "catch_hatch_4": (658.4, 540)}
    assert _holes(hatch) == {"catch_panel_1": (359.4, 260), "catch_panel_2": (359.4, 540),
                             "catch_panel_3": (640.6, 260), "catch_panel_4": (640.6, 540)}


def test_the_hatch_fills_the_opening_with_the_slot_the_catch_takes():
    catch = BallCatch()
    assert catch.gap == 3.0 == (data.GN_450.min_gap + data.GN_450.max_gap) / 2
    _, panel, hatch = _floor(catch, edge=None)
    b = hatch.box()
    # the opening shrunk by 3 all round, flush with the panel on both faces
    assert (b.lo["x"], b.hi["x"], b.lo["y"], b.hi["y"], b.lo["z"], b.hi["z"]) == (353, 647, 203, 597, 0, 15)
    assert hatch.material is panel.material
    assert hatch.show_face.world_name == panel.show_face.world_name == "top"
    # its corners are true arcs, rounded with 20 - 3, between straight edges
    ring = list(orient(hatch.outline.polygons()[0], 1.0).exterior.coords)[:-1]
    curves = fit(ring)
    assert [type(c) for c in curves].count(Arc2) == 4
    assert all(abs(c.radius - 17) < 1e-9 for c in curves if isinstance(c, Arc2))
    lines = [c for c in curves if isinstance(c, Line2)]
    assert {round(c.a[1], 9) for c in lines if c.a[1] == c.b[1]} == {203, 597}
    # a thinner hatch is flush with the catch face; face= names another one
    with module("m", BOX) as m:
        panel = board("panel", ply15).on(m.bottom).show(m.top)
        panel.cut(rect(width=400, depth=300).rounded(20), at=panel.top.center, name="opening")
        thin = BallCatch(gap=2.5).hatch("thin", panel.opening, material=ply12)
        top = BallCatch().hatch("top", panel.opening, material=ply12, face=panel.top)
    assert (thin.box().lo["z"], thin.box().hi["z"], thin.box().lo["x"]) == (0, 12, 352.5)
    assert (top.box().lo["z"], top.box().hi["z"]) == (3, 15)


def test_points_go_square_onto_the_nearest_straight_edge():
    """`at=` takes points on a big face of the panel or the hatch; each
    catch is numbered by its point and goes onto the nearest straight
    edge, square to it, as the add-in's Custom Points do."""
    with module("floor", BOX) as f:
        panel = board("panel", ply15).on(f.bottom).show(f.top)
        panel.cut(rect(width=400, depth=300).rounded(20), at=panel.top.center, name="opening")
        opening = panel.opening
        catch = BallCatch(at=[
            panel.bottom.left(opening.left).front(450),         # on the left edge, x 450
            panel.top.left(opening.left - 5).front(500),         # 5 mm into the panel, on its top face
        ])
        hatch = catch.hatch("hatch", opening)
        points = BallCatch(at=[hatch.bottom.front(100)])        # the hatch's middle, 103 from the front edge
        f.mount(catch, opening=opening, hatch=hatch)
        f.mount(points, opening=opening, hatch=hatch)
    assert _holes(panel) == {"catch_hatch_1": (450, 191.6), "catch_hatch_2": (500, 191.6),
                             "catch_hatch_3": (341.6, 400)}
    assert _holes(hatch) == {"catch_panel_1": (450, 209.4), "catch_panel_2": (500, 209.4),
                             "catch_panel_3": (359.4, 400)}
    # a second mount on the same hatch numbers on, in an item of its own
    assert [(item["name"], [b["name"] for b in item["bodies"]]) for item in f.hardware] == [
        ("hatch_catches", ["catch_1", "catch_2"]), ("hatch_catches_2", ["catch_3"])]


def _mount_error(catch: BallCatch, **options: Any) -> str:
    with pytest.raises(LangError) as error:
        with module("floor", BOX) as f:
            panel = board("panel", ply15).on(f.bottom).show(f.top)
            panel.cut(rect(width=400, depth=300).rounded(20), at=panel.top.center, name="opening")
            hatch = BallCatch().hatch("hatch", panel.opening)
            if "edge" not in options and catch.at is None:
                options["edge"] = panel.opening.left
            f.mount(catch, opening=panel.opening, hatch=hatch, **options)
    return str(error.value)


def test_validation_of_spacing():
    # End Offset below half the holder's width, refused where the catch is made when an edge gets two
    with pytest.raises(LangError, match="end must be at least 14 mm"):
        BallCatch(end=10)
    BallCatch(count=2, end=10)                                            # one per edge: centred, end unused
    # 8 catches 40 from the ends of a 260 mm edge need 80 + 7 * 28 = 276
    assert ("the opening's left edge is 260 mm long; 8 catches 40 mm from its ends need 276 mm"
            in _mount_error(BallCatch(count=16)))
    assert len(_floor(BallCatch(count=14))[1].ops) == 1 + 14             # 7 per edge, 30 apart: fits
    # a single catch on an edge whose straight part is shorter than the holder
    registry.reset()
    with pytest.raises(LangError, match="the opening's front edge is 20 mm long, shorter than the 28 mm wide holder"):
        _floor(BallCatch(count=2), edge="front", shape=rect(width=60, depth=300).rounded(20))


def test_validation_of_points():
    with module("floor", BOX) as f:
        panel = board("panel", ply15).on(f.bottom).show(f.top)
        panel.cut(rect(width=400, depth=300).rounded(20), at=panel.top.center, name="opening")
        hatch = BallCatch().hatch("hatch", panel.opening)
        other = board("other", ply15).on(f.top)
        left = panel.opening.left
        cases = [
            # 10 from the straight part's start at x 370: the holder needs 14
            ([panel.bottom.left(left).front(380)], "point 1 of at= is too close to the end of the straight part "
                                                   "of the opening's left edge"),
            ([panel.bottom.left(left).front(450), panel.bottom.left(left).front(470)],
             "points 1 and 2 of at= are 20 mm apart; the holders are 28 mm wide"),
            ([other.bottom.center], "point 1 of at= lies on floor.other"),
        ]
        for points, message in cases:
            with pytest.raises(LangError) as error:
                f.mount(BallCatch(at=points), opening=panel.opening, hatch=hatch)
            assert message in str(error.value)
    assert _holes(panel) == {} and _holes(hatch) == {}                    # a failed mount drills nothing


def test_validation_of_the_hatch_and_the_slot():
    with module("floor", BOX) as f:
        panel = board("panel", ply15).on(f.bottom).show(f.top)
        panel.cut(rect(width=400, depth=300).rounded(20), at=panel.top.center, name="opening")
        x, y = Pos("x", 0), Pos("y", 0)
        # 4 mm all round: too wide a slot (with 10 the balls, 9.4 in, would miss the hatch)
        wide = board("wide", ply15).on(f.bottom).between(x + 354, x + 646, y + 204, y + 596)
        # a small board in the middle: nothing under the balls
        small = board("small", ply15).on(f.bottom).between(x + 450, x + 550, y + 300, y + 500)
        # in the opening, but 5 mm higher
        high = board("high", ply15).on(Pos("z", 5), toward=f.top).between(x + 353, x + 647, y + 203, y + 597)
        thin = BallCatch().hatch("thin", panel.opening, material=material("birch", t=4))
        catch = BallCatch()
        for hatch, message in [
            (wide, "the slot between floor.panel and floor.wide is 4 mm wide at the opening's left edge; the GN 450 "
                   "needs 2.5 mm to 3.5 mm"),
            (small, "there is no hatch under the ball of catch 1"),
            (high, "floor.high is not flush with floor.panel on the bottom face"),
            (thin, "the pilot depth (4 mm) must be less than floor.thin's thickness (4 mm)"),
            (panel, "the hatch must be a board of its own"),
        ]:
            with pytest.raises(LangError) as error:
                f.mount(catch, opening=panel.opening, edge=panel.opening.left, hatch=hatch)
            assert message in str(error.value)
        hatch = catch.hatch("hatch", panel.opening)
        with pytest.raises(LangError, match=r"the pilot depth \(15 mm\) must be less than floor.panel's thickness"):
            f.mount(BallCatch(pilot=(2, 15)), opening=panel.opening, edge=panel.opening.left, hatch=hatch)
        # a through hole under the rim of ball 1's base (10 across, at x 410)
        hatch.hole(d=4, depth=through, at=hatch.top.left(Pos("y", 209.4)).front(Pos("x", 415)))
        with pytest.raises(LangError, match="the ball of catch 1 does not fit on the hatch"):
            f.mount(catch, opening=panel.opening, edge=panel.opening.left, hatch=hatch)


def test_validation_of_the_opening():
    with module("floor", BOX) as f:
        panel = board("panel", ply15).on(f.bottom).show(f.top)
        # 10 mm from the panel's left edge: no room for the holders' 15 mm
        panel.cut(rect(width=400, depth=300).rounded(20), at=panel.top.left(10), name="opening")
        hatch = BallCatch().hatch("hatch", panel.opening)
        with pytest.raises(LangError, match="the holder of catch 1 does not fit on floor.panel; it needs 28 mm x "
                                            "15 mm beside the opening"):
            f.mount(BallCatch(), opening=panel.opening, edge=panel.opening.left, hatch=hatch)
        # the opening's right edge is fine, and the left holders are then the opposite ones
        with pytest.raises(LangError, match="the holder of catch 3 does not fit"):
            f.mount(BallCatch(), opening=panel.opening, edge=panel.opening.right, hatch=hatch)
        panel.cut(rect(width=100, depth=100), at=panel.top.front, name="notch")
        panel.pocket(rect(width=100, depth=100), at=panel.top.back(100), depth=5, name="dado")
        panel.cut(circle(100), at=panel.top.right(100), name="port")
        for name, message in [
            ("notch", "the opening 'notch' reaches the edge of floor.panel"),
            ("dado", "'dado' is not a through cut"),
            ("port", "the opening 'port' has no straight edges"),
        ]:
            with pytest.raises(LangError) as error:
                f.mount(BallCatch(), opening=panel.op(name), edge=panel.opening.left, hatch=hatch)
            assert message in str(error.value)
        with pytest.raises(LangError, match="no straight edge lies at y=15 on the opening 'opening'"):
            f.mount(BallCatch(), opening=panel.opening, edge=panel.opening.left + 5, hatch=hatch)


def test_an_edge_without_one_opposite():
    """A triangle's legs have no parallel edge across the opening."""
    with pytest.raises(LangError, match="the opening has no straight edge opposite the opening's left edge"):
        _floor(shape=polygon([(0, 0), (300, 0), (0, 300)]).rounded(10))
    registry.reset()
    _, panel, _ = _floor(BallCatch(count=1), shape=polygon([(0, 0), (300, 0), (0, 300)]).rounded(10))
    assert len(_holes(panel)) == 1


def test_mount_and_constructor_options():
    catch = BallCatch()
    with pytest.raises(LangError, match=r"mount\(\) needs edge="):
        with module("floor", BOX) as f:
            panel = board("panel", ply15).on(f.bottom)
            panel.cut(rect(width=400, depth=300).rounded(20), at=panel.top.center, name="opening")
            hatch = catch.hatch("hatch", panel.opening)
            f.mount(catch, opening=panel.opening, hatch=hatch)
    with pytest.raises(TypeError, match="side"):          # mount's own keywords, typed
        f.mount(catch, opening=panel.opening, hatch=hatch, edge=panel.opening.left, side=1)  # type: ignore[call-arg]
    registry.reset()
    with module("floor", BOX) as f:
        panel = board("panel", ply15).on(f.bottom)
        panel.cut(rect(width=400, depth=300).rounded(20), at=panel.top.center, name="opening")
        with pytest.raises(LangError, match="leave out edge="):
            f.mount(BallCatch(at=[panel.bottom.center]), opening=panel.opening, hatch=panel, edge=panel.opening.left)
    for make, message in [
        (lambda: BallCatch(gap=4), "the slot must be 2.5 to 3.5 mm wide, not 4"),
        (lambda: BallCatch(count=0), "count must be at least 1"),
        (lambda: BallCatch(end=-1), "end must not be negative"),
        (lambda: BallCatch(pilot=(0, 4)), "pilot= needs a diameter and a depth greater than zero, not 0 x 4"),
        (lambda: BallCatch(pilot=(2, 0)), "pilot= needs a diameter and a depth greater than zero, not 2 x 0"),
        (lambda: BallCatch(count=2, at=[]), "give count= or at=, not both"),
        (lambda: BallCatch(at=[]), "at= is empty"),
        (lambda: BallCatch("GN 451"), "BallCatch(): expected 'GN 450', not 'GN 451'"),     # type: ignore[arg-type]
    ]:
        with pytest.raises(LangError) as error:
            make()
        assert message in str(error.value)


def test_the_catch_model_names_are_the_catalogs():
    assert get_args(CatchModel) == tuple(data.CATCHES)
    data._self_check()   # type: ignore[reportPrivateUsage]


def test_a_cabinet_and_a_module_in_the_vans_terms_give_the_same_catches():
    """Seen from its front, a cabinet's left is the van's right: the same
    edge is the opening's left in the one and its right in the other, and
    the holes, their names and the catches' boxes come out the same."""
    _, panel, hatch = _floor(edge="left")
    van = (panel.to_layout()["ops"], hatch.to_layout()["ops"], build_layout()["modules"][0]["hardware"])
    registry.reset()
    _, panel, hatch = _floor(edge="right", front=True)
    cabinet = (panel.to_layout()["ops"], hatch.to_layout()["ops"], build_layout()["modules"][0]["hardware"])
    assert van == cabinet
    assert _holes(panel)["catch_hatch_1"] == (410, 191.6)          # the edge at y = 200 first


def test_a_hatch_in_an_upright_panel():
    """The back of a cabinet opening toward the van's right (+y): the back
    lies at y 0 to 15, its inner face (+y) is the hidden one, so the
    catches go there and stand into the cabinet."""
    box = Box.from_size(width=500, depth=600, height=700)
    with module("cab", box, front=box.right) as cab:
        back = board("back", ply15).on(cab.back)
        back.cut(rect(width=300, height=400).rounded(15), at=back.outer.center, name="opening")
        catch = BallCatch()
        hatch = catch.hatch("hatch", back.opening)
        cab.mount(catch, opening=back.opening, edge=back.opening.bottom, hatch=hatch)
    b = back.box()
    assert b.lo["y"] == 0 and b.hi["y"] == 15
    # the opening: x 150 to 450 (width), z 150 to 550 (height); the bottom
    # edge's straight part runs from x 165 to 435 (270)
    assert _holes(back) == {"catch_hatch_1": (205, 141.6), "catch_hatch_2": (395, 141.6),
                            "catch_hatch_3": (205, 558.4), "catch_hatch_4": (395, 558.4)}
    assert {op.face for op in back.ops if isinstance(op, Hole)} == {"right"}
    assert hatch.box().lo["y"] == 0 and hatch.box().hi["y"] == 15
    (item,) = cab.hardware
    for body in item["bodies"]:
        assert [b["min"][1] for b in body["boxes"]] == [15 + part.rise[0] for part in SHAPE.parts()]
        assert [b["max"][1] for b in body["boxes"]] == [15 + part.rise[1] for part in SHAPE.parts()]


def test_the_catches_are_placed_as_boxes():
    """Each catch is a body of boxes from the catch face (z = 0, out of it
    down), measured from the opening's contour: the holder on the panel
    outward, its webs up into the 3 mm slot, its jaw over the slot and the
    hatch's edge, the ball part on the hatch inward, each centred on the
    catch along the edge."""
    f, panel, hatch = _floor()
    (item,) = f.hardware
    assert item["path"] == "floor.hatch_catches" and item["kind"] == "hardware"
    bodies = {b["name"]: b["boxes"] for b in item["bodies"]}
    assert list(bodies) == ["catch_1", "catch_2", "catch_3", "catch_4"]

    def expected(x: float, contour: float, outward: int) -> list[dict[str, list[float]]]:
        out: list[dict[str, list[float]]] = []
        for part in SHAPE.parts():
            y0, y1 = sorted(contour + outward * a for a in part.across)
            out.append({"min": [x - part.width / 2, y0, -part.rise[1]], "max": [x + part.width / 2, y1, -part.rise[0]]})
        return out
    # catch 1 at x 410 on the left edge (y = 200, the panel at y < 200),
    # catch 4 at x 590 on the right edge (y = 600, the panel at y > 600)
    assert bodies["catch_1"] == expected(410, 200, -1)
    assert bodies["catch_4"] == expected(590, 600, 1)
    # under the boards or in the slot, never in their material; the holder
    # and the ball part apart, the jaw over the ball, the webs and the jaw
    # against the holder, so each body is one piece
    for boxes in bodies.values():
        holder, webs, jaw, ball = (Box(dict(zip("xyz", b["min"])), dict(zip("xyz", b["max"]))) for b in boxes)  # type: ignore[arg-type]
        for box in (holder, jaw, ball):
            assert not any(box.overlaps(p.box()) for p in (panel, hatch))
        assert webs.overlaps(panel.box())                                   # in the slot, inside the panel's box
        assert jaw.overlaps(ball) and not holder.overlaps(ball)
        assert holder.hi["y"] == jaw.lo["y"] or holder.lo["y"] == jaw.hi["y"]
    assert no_interference(f) == []
    assert build_layout()["modules"][0]["hardware"] == [item]


def test_layout_and_emit_plan():
    _floor()
    layout = build_layout()
    plan = plan_layout(layout)
    steps = {p.path: p.steps for p in plan.parts}
    (holders,) = [s for s in steps["floor.panel"] if isinstance(s, HoleStep)]
    (balls,) = [s for s in steps["floor.hatch"] if isinstance(s, HoleStep)]
    for step in (holders, balls):
        assert step.face == FaceRef("z", -1, 0.0) and step.d == 2 and step.depth == 4
    assert holders.points == [(410, 191.6, 0), (590, 191.6, 0), (410, 608.4, 0), (590, 608.4, 0)]
    assert balls.points == [(410, 209.4, 0), (590, 209.4, 0), (410, 590.6, 0), (590, 590.6, 0)]
    (item,) = plan.hardware
    assert (item.path, item.component, item.name) == ("floor.hatch_catches", ("floor",), "hatch_catches")
    assert [b.name for b in item.bodies] == ["catch_1", "catch_2", "catch_3", "catch_4"]
    assert item.bodies[0].boxes[0] == ((410 - HOLDER.width / 2, 200 - HOLDER.across[1], -HOLDER.rise[1]),
                                       (410 + HOLDER.width / 2, 200 - HOLDER.across[0], -HOLDER.rise[0]))
    assert plan.problems == []
    # the emitter draws the hatch's corners as arcs of 17, like the opening's of 20
    hatch = next(p for p in plan.parts if p.path == "floor.hatch")
    arcs = [c for loop in hatch.body.loops for c in loop if isinstance(c, Arc)]
    assert len(arcs) == 4 and all(abs(c.radius - 17) < 1e-6 for c in arcs)


def test_preview_draws_the_catches():
    from lang.preview.mesh import build_scene
    _floor()
    scene = build_scene(build_layout())
    meshes = {}
    for node in scene.graph.nodes_geometry:
        if "hatch_catches" in node:
            transform, geometry = scene.graph[node]
            mesh = scene.geometry[geometry].copy()
            mesh.apply_transform(transform)
            meshes[node.rsplit(".", 1)[1]] = mesh
    assert set(meshes) == {"catch_1", "catch_2", "catch_3", "catch_4"}
    mesh = meshes["catch_1"]
    assert mesh.is_volume
    (item,) = build_layout()["modules"][0]["hardware"]
    boxes = item["bodies"][0]["boxes"]
    assert mesh.bounds.round(4).tolist() == [[min(b["min"][i] for b in boxes) for i in range(3)],
                                             [max(b["max"][i] for b in boxes) for i in range(3)]]
    # the union of its boxes: the webs overlap the holder, the jaw the ball part
    def volume(part: Any) -> float:
        return part.width * (part.across[1] - part.across[0]) * (part.rise[1] - part.rise[0])

    def shared(a: Any, b: Any) -> float:
        spans = [(min(a.width, b.width), 0.0)] + [
            (min(x[1], y[1]) - max(x[0], y[0]), 0.0) for x, y in ((a.across, b.across), (a.rise, b.rise))]
        return math.prod(max(0.0, d) for d, _ in spans)
    union = sum(volume(p) for p in SHAPE.parts()) - shared(HOLDER, WEBS) - shared(JAW, BALL)
    assert math.isclose(mesh.volume, union, rel_tol=1e-6)
    assert "floor.hatch" in scene.geometry and "floor.panel" in scene.geometry


def test_the_example_builds(tmp_path: Path):
    layout = run_build(Path(__file__).parent.parent / "examples" / "inspection_hatch.py", tmp_path)
    (module_,) = layout["modules"]
    assert len(module_["parts"]) == 6 and layout["problems"] == [] and module_["problems"] == []
    (item,) = module_["hardware"]
    assert len(item["bodies"]) == 4
    hardware: HardwareLayout = item
    # the catches hang under the floor panel (z 45 to 60), the holder's
    # webs reaching 11 up into the slot
    for body in hardware["bodies"]:
        holder, webs, jaw, ball = body["boxes"]
        assert all(box["max"][2] == 45 and box["min"][2] < 45 for box in (holder, ball))
        assert jaw["max"][2] == 44 and (webs["min"][2], webs["max"][2]) == (45, 56)


# -- the review's fixes (findings 25, 31) --------------------------------------------------------------------

def test_a_holder_pilot_over_a_hole_made_before_is_refused():
    """`Board.hole_fits` for the pilot holes: a 4 mm hole in the panel's
    underside overlapping where the holder of catch 2 is screwed, its
    centre 2.5 mm off along the edge, refused before anything is drilled."""
    with module("floor", BOX) as f:
        panel = board("panel", ply15).on(f.bottom).show(f.top)
        panel.cut(rect(width=400, depth=300).rounded(20), at=panel.top.center, name="opening")
        catch = BallCatch()
        hatch = catch.hatch("hatch", panel.opening)
        panel.hole(d=4, depth=5, at=panel.bottom.front(Pos("x", 592.5)).left(Pos("y", 191.6)))
        with pytest.raises(LangError, match="the holder of catch 2 does not fit"):
            f.mount(catch, opening=panel.opening, edge=panel.opening.left, hatch=hatch)
    assert len(_holes(panel)) == 1 and _holes(hatch) == {} and f.hardware == []


def test_the_exact_inset_lives_with_the_cutouts():
    """The hatch's outline is `lang.core.cutouts.inset` of the opening:
    lines moved square to themselves, arcs about their centres, a circle a
    circle; it was ball_catches' own."""
    from lang.core.cutouts import inset
    from shapely.geometry import Polygon
    opening = rect(width=400, depth=300).rounded(20).polygons()[0]
    hatch = inset(opening, 3)
    assert isinstance(hatch, Polygon)
    curves = fit(list(orient(hatch, 1.0).exterior.coords)[:-1])
    assert sorted(round(c.radius, 9) for c in curves if isinstance(c, Arc2)) == [17] * 4
    assert hatch.bounds == pytest.approx((3, 3, 297, 397))                     # the shape from 0 to 300 x 400
    ring = circle(100).polygons()[0]
    assert inset(ring, 10).area == pytest.approx(math.pi * 40 ** 2, rel=1e-3)
    assert inset(ring, 60).is_empty
    square = rect(width=100, depth=100).polygons()[0]
    assert inset(square, 10).bounds == pytest.approx((10, 10, 90, 90))            # sharp corners stay sharp
    assert inset(square, 10).area == pytest.approx(80 * 80)
