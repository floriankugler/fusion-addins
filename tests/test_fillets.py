"""Corners of a board's outline: rounded with `fillet()`, cut off with
`chamfer()` on an edge through the board (`lang.core.corners`)."""
import math

import pytest
from shapely.geometry import Point

from lang import *
from lang.core.contact import contacts
from lang.core.layout import build_layout
from lang.core.ops import Chamfer, Cut
from lang.core.scope import registry
from lang.emit.arcs import Arc2, Line2, fit
from lang.emit.plan import Arc, Line, plan_layout
from lang.preview.mesh import mesh_part
from helpers import carcass, ply15

#: What a quarter circle of radius 1 leaves of its square.
CORNER = 1 - math.pi / 4
#: The module's box: x (depth) 0 to 300 from the front, y (width) 0 to 400 from the left, z 0 to 200.
BOX = Box.from_size(width=400, depth=300, height=200)


def _panel(box: Box = BOX) -> tuple[Scope, Board]:
    """A board lying on the module's bottom, 300 deep (x) and 400 wide (y)."""
    with module("m", box) as m:
        panel = board("panel", ply15).on(m.bottom).show(m.top)
    return m, panel


def _side() -> tuple[Scope, Board]:
    """A board standing on the module's left, 300 deep (x) and 200 high (z)."""
    with module("m", BOX) as m:
        side = board("side", ply15).on(m.left).show("inner")
    return m, side


def _curves(shape: Shape) -> list[list[str]]:
    """Each ring's lines and arcs, an arc as `arc r=<radius> <sweep in
    degrees>`, starting with the first arc."""
    rings: list[list[str]] = []
    for ring in shape.rings():
        out: list[str] = []
        for c in fit(ring):
            if isinstance(c, Arc2):
                out.append(f"arc r={c.radius:.6g} {math.degrees(_sweep(c)):.4g}")
            else:
                assert isinstance(c, Line2)
                out.append("line")
        first = next((i for i, c in enumerate(out) if c.startswith("arc")), 0)
        rings.append(out[first:] + out[:first])
    return rings


def _sweep(c: Arc2) -> float:
    def angle(p: tuple[float, float]) -> float:
        return math.atan2(p[1] - c.center[1], p[0] - c.center[0])
    return abs(math.remainder(angle(c.b) - angle(c.mid), 2 * math.pi)) + abs(
        math.remainder(angle(c.mid) - angle(c.a), 2 * math.pi))


def _arcs(shape: Shape) -> list[Arc2]:
    return [c for ring in shape.rings() for c in fit(ring) if isinstance(c, Arc2)]


# -- rounding ------------------------------------------------------------------------------------

def test_a_fillet_rounds_one_corner_of_a_board_lying_flat():
    m, panel = _panel()
    with m:
        panel.fillet(panel.front.left, 20)
    assert panel.outline.area == pytest.approx(300 * 400 - CORNER * 400, abs=0.05)
    assert _curves(panel.outline) == [["arc r=20 90", "line", "line", "line", "line"]]
    (arc,) = _arcs(panel.outline)
    # front is x = 0, left y = 0: the arc touches both edges 20 from the corner
    assert arc.center == pytest.approx((20, 20))
    assert {tuple(round(c, 9) for c in p) for p in (arc.a, arc.b)} == {(0, 20), (20, 0)}
    assert not panel.outline.geometry.contains(Point(1, 1))
    assert panel.box().lo["x"] == 0 and panel.box().lo["y"] == 0      # the box stays
    assert panel.ops == []                                             # nothing to emit but the outline


def test_several_corners_of_a_standing_board_at_once():
    m, side = _side()
    with m:
        side.fillet([side.front.bottom, side.back.top], 25)
    arcs = sorted(_arcs(side.outline), key=lambda a: a.center)
    # the outline lies in (x, z): front x = 0, back 300, bottom z = 0, top 200
    assert [a.center for a in arcs] == [pytest.approx((25, 25)), pytest.approx((275, 175))]
    assert [a.radius for a in arcs] == pytest.approx([25, 25])
    assert side.outline.area == pytest.approx(300 * 200 - 2 * CORNER * 625, abs=0.05)


def test_half_the_width_rounds_an_end_fully():
    m, panel = _panel()
    with m:
        panel.fillet([panel.front.left, panel.back.left], 150)
    # one half circle across the left end, not two quarters
    assert _curves(panel.outline) == [["arc r=150 180", "line", "line", "line"]]


def test_the_corners_a_cut_made_concave_ones_gain_material():
    m, side = _side()
    with m:
        side.cut(rect(depth=60, height=40), at=side.outer.bottom.front, name="toekick")
        before = side.outline.area
        side.fillet(side.toekick, 8)
    # two convex corners lose a little, the concave one gains as much
    assert side.outline.area == pytest.approx(before - CORNER * 64, abs=0.02)
    assert _curves(side.outline) == [["arc r=8 90", "line", "arc r=8 90", "line", "arc r=8 90", "line", "line",
                                      "line", "line"]]
    assert side.outline.geometry.contains(Point(60.5, 40.5))         # the inside corner filled
    assert [op.kind for op in side.ops] == ["cut"]


def test_a_rounded_inside_corner_gets_no_dog_bone():
    m, side = _side()
    with m:
        side.cut(rect(depth=60, height=40), at=side.outer.bottom.front, name="toekick")
        side.fillet(side.toekick, 8).dogbones()
    build_layout()
    assert [op.kind for op in side.ops] == ["cut"]


def test_every_corner_of_the_outline_but_not_its_holes():
    ell = polygon([(0, 0), (300, 0), (300, 100), (100, 100), (100, 400), (0, 400)])
    with module("m", BOX) as m:
        panel = board("panel", ply15, ell).on(m.bottom)
        panel.cut(rect(depth=40, width=40), at=panel.top.front(20).left(20), name="window")
        before = panel.outline.area
        panel.fillet(panel.bottom.outline, 10)               # either big face: the same corners
    # five convex corners lose, the concave one gains
    assert panel.outline.area == pytest.approx(before - 4 * CORNER * 100, abs=0.05)
    outer, window = _curves(panel.outline)
    assert outer == ["arc r=10 90", "line"] * 6
    assert window == ["line"] * 4


def test_corners_named_twice_are_rounded_once():
    m, panel = _panel()
    with m:
        panel.fillet([panel.front.left, panel.top.outline], 10)
    assert len(_arcs(panel.outline)) == 4


# -- corner chamfers -----------------------------------------------------------------------------

def test_a_chamfer_on_an_edge_through_the_board_cuts_the_corner_off_the_outline():
    m, panel = _panel()
    with m:
        panel.chamfer(panel.front.right, 10)
        panel.chamfer([panel.back.left, panel.top.outline], 2)
    assert panel.outline.area == pytest.approx(300 * 400 - 50 - 2)
    assert panel.outline.geometry.boundary.distance(Point(0, 390)) < 1e-9
    assert panel.outline.geometry.boundary.distance(Point(10, 400)) < 1e-9
    assert not panel.outline.geometry.contains(Point(4, 396))
    # only the outline chamfer along the top face is an operation
    assert [(op.what, op.face) for op in panel.ops if isinstance(op, Chamfer)] == [("outline", "top")]


def test_a_chamfer_on_a_corner_a_cut_made():
    m, side = _side()
    with m:
        side.cut(rect(depth=60, height=40), at=side.outer.bottom.front, name="toekick")
        side.chamfer(side.back.bottom, 30)
    assert side.outline.area == pytest.approx(300 * 200 - 60 * 40 - 450)


# -- what else sees the new outline ----------------------------------------------------------------


def test_contacts_and_joints_made_after_meet_the_rounded_corner():
    cab, p = carcass(back=False)
    with cab:
        p["top"].fillet([p["top"].front.left, p["top"].front.right], 30)
        p["top"].join(p["left"], p["right"], using=cabineo(count=2))
    (c,) = contacts(p["top"], p["left"])
    assert (c.lo, c.hi) == pytest.approx((30, 500))
    holes = [op for op in p["top"].ops if getattr(op, "name", "").startswith("cabineo_left")]
    assert holes and min(getattr(op, "u") for op in holes) > 30


def test_no_interference_sees_the_rounded_corner():
    for rounded, expected in ((False, ["m.panel overlaps m.puck"]), (True, [])):
        registry.reset()
        with module("m", BOX) as m:
            panel = board("panel", ply15).on(m.bottom)
            if rounded:
                panel.fillet(panel.front.left, 50)
            # a 10 x 10 block in the corner, which the fillet leaves clear
            board("puck", ply15).on(m.bottom).between(m.front, m.front + 10, m.left, m.left + 10)
        assert no_interference(m) == expected


def test_the_emit_plan_draws_true_arcs_tangent_to_the_edges():
    m, panel = _panel(Box.from_size(width=400, depth=300, height=200, origin=(2400.0, -800.0, 300.0)))
    with m:
        panel.fillet(panel.front.left, 20).chamfer(panel.back.right, 10)
    plan = plan_layout(build_layout())
    (part,) = plan.parts
    (loop,) = part.body.loops
    (arc,) = [c for c in loop if isinstance(c, Arc)]
    assert arc.radius == pytest.approx(20, abs=1e-9)
    assert arc.center == pytest.approx((2420, -780, 300))
    assert sorted([arc.a, arc.b]) == [pytest.approx((2400, -780, 300)), pytest.approx((2420, -800, 300))]
    # the lines next to the arc start where it ends, square to its radius there
    lines = [c for c in loop if isinstance(c, Line)]
    assert len(lines) == 5                                   # four edges and the chamfer
    for end in (arc.a, arc.b):
        (line,) = [ln for ln in lines if end in (ln.a, ln.b)]
        far = line.b if line.a == end else line.a
        radial = [e - c for e, c in zip(end, arc.center)]
        along = [f - e for f, e in zip(far, end)]
        assert abs(sum(r * a for r, a in zip(radial, along))) < 1e-6 * math.hypot(*along)
    assert any({ln.a, ln.b} == {(2700.0, -410.0, 300.0), (2690.0, -400.0, 300.0)} for ln in lines)


def test_the_preview_mesh_has_the_rounded_corner():
    m, panel = _panel()
    with m:
        panel.fillet(panel.front.left, 20).chamfer(panel.back.right, 10)
    layout = build_layout()
    (part,) = layout["modules"][0]["parts"]
    volume = float(mesh_part(part, layout["frame"]).volume)
    assert volume == pytest.approx((300 * 400 - CORNER * 400 - 50) * 15, rel=1e-5)


# -- errors --------------------------------------------------------------------------------------

def test_an_edge_along_a_face_is_not_a_corner():
    m, panel = _panel()
    with m, pytest.raises(LangError, match=r"m\.panel: fillet\(\): front\.top runs along the top face, not "
                                           r"through the board\. .* \(front\.left\)"):
        panel.fillet(panel.front.top, 5)
    m, side = _side()
    # the inner face is the right one
    with m, pytest.raises(LangError, match=r"front\.right runs along the right face.* \(front\.bottom\)"):
        side.fillet(side.front.inner, 5)


def test_the_sharp_tip_of_a_tapered_board_is_rounded():
    """Found by fuzzing: a corner sharper than 28 degrees could not be
    rounded, whatever the radius (see test_shapes, a sharp corner with long
    edges)."""
    tip = math.radians(20)
    with module("m", BOX) as m:
        wedge = board("wedge", ply15, polygon([(0, 0), (300, 0), (0, 300 * math.tan(tip))])).on(m.bottom)
        wedge.fillet(wedge.top.outline, 3)
    from lang.core.corners import find
    assert find(wedge.outline) == []


def test_a_corner_that_is_gone_is_an_error():
    m, panel = _panel()
    with m:
        panel.cut(rect(depth=60, width=40), at=panel.top.front.left, name="notch")
        with pytest.raises(LangError, match=r"fillet\(\): the outline has no corner at front\.left any more.*"
                                            r"fillet\(panel\.<cut>, \.\.\.\)"):
            panel.fillet(panel.front.left, 5)
        panel.fillet(panel.front.right, 5)
        with pytest.raises(LangError, match=r"no corner at front\.right any more"):
            panel.fillet(panel.front.right, 5)
        with pytest.raises(LangError, match=r"chamfer\(\): the outline has no corner at front\.right"):
            panel.chamfer(panel.front.right, 2)


def test_a_radius_too_large_for_the_edges_is_an_error():
    m, panel = _panel()
    with m:
        with pytest.raises(LangError, match=r"fillet\(301\): an edge at front\.left is too short for the arc, so "
                                            r"the corner cannot be rounded with it\."):
            panel.fillet(panel.front.left, 301)
        with pytest.raises(LangError, match=r"fillet\(160\): the arcs at (front\.left and back\.left|back\.left "
                                            r"and front\.left) need more than the edge between them\."):
            panel.fillet([panel.front.left, panel.back.left], 160)
        with pytest.raises(LangError, match=r"chamfer\(301\): an edge at front\.left is too short for the chamfer"):
            panel.chamfer(panel.front.left, 301)
        with pytest.raises(LangError, match=r"fillet\(\): the radius must be positive, got 0\."):
            panel.fillet(panel.front.left, 0)
        with pytest.raises(LangError, match=r"chamfer\(\): the size must be positive, got -1\."):
            panel.chamfer(panel.front.left, -1)
        assert panel.outline.area == 300 * 400                 # nothing changed


def test_an_arc_running_into_a_through_cut_is_an_error():
    m, panel = _panel()
    with m:
        panel.cut(rect(depth=20, width=20), at=panel.top.front(5).left(5), name="window")
        with pytest.raises(LangError, match=r"fillet\(40\): the arc at front\.left runs into another contour"):
            panel.fillet(panel.front.left, 40)


def test_a_fillet_taking_material_where_an_operation_lies_is_an_error():
    m, panel = _panel()
    with m:
        panel.hole(d=5, depth=8, at=panel.top.front(8).left(8), name="pin")
        with pytest.raises(LangError, match=r"fillet\(30\) takes material where the hole 'pin' lies, which was "
                                            r"made before it"):
            panel.fillet(panel.front.left, 30)
        panel.fillet(panel.front.left, 10)                       # clear of it


def test_a_fillet_after_a_joint_on_its_corner_is_an_error():
    cab, p = carcass(back=False)
    with cab:
        p["bottom"].join(p["left"], p["right"], using=cabineo(count=2))
        with pytest.raises(LangError, match=r"cab\.bottom: fillet\(60\) takes material where the hole "
                                            r"'cabineo_left_1a' lies"):
            p["bottom"].fillet(p["bottom"].front.left, 60)


def test_what_fillet_does_not_take():
    m, panel = _panel()
    with m:
        panel.pocket(rect(depth=40, width=40), at=panel.top.center, depth=5, name="tray")
        panel.cut(circle(30), at=panel.top.back(40).right(40), name="port")
        other = board("other", ply15).on(m.top)
        cases = [
            (panel.tray, r"the pocket 'tray' is not a through cut"),
            (panel.port, r"the cut 'port' left no corners in the outline"),
            ("front.left", r"takes edges, operations and outlines themselves, not the name 'front\.left'"),
            (other.front.left, r"Edge\(m\.other\.front\.left\) is not an edge of this board"),
            (panel.front.outline, r"Face\(m\.panel\.front\) is a narrow face"),
            ([], r"name the corners, e\.g\. fillet\(panel\.front\.left, \.\.\.\)"),
        ]
        for what, message in cases:
            with pytest.raises(LangError, match=message):
                panel.fillet(what, 5)  # type: ignore[arg-type]
    assert all(isinstance(op, Cut) or op.kind == "pocket" for op in panel.ops)


def test_corners_of_a_hair_thin_hole_are_refused_not_a_crash():
    """Found by fuzzing: an outline with a hole 2e-38 thin (a boolean of
    shapes meeting along a line can leave one). Cutting off the hole's
    corners used up its edges and left a ring of two points, and shapely
    raised a ValueError."""
    from shapely.geometry import Polygon
    from lang.core.cutouts import chamfered, corner_points, filleted
    outline = Polygon([(103.75, -196.5), (71.25, -196.5), (71.25, 35.5), (103.75, 35.5)],
                      [[(71.25, 2.1163343496927108e-38), (12.5, -9.476569618361552e-59),
                        (71.25, -9.476569618361552e-59)]])
    hole = Polygon([(103.75, -196.5), (71.25, -196.5), (71.25, 2.1163343496927108e-38), (12.5, -9.476569618361552e-59),
                    (71.25, -9.476569618361552e-59), (71.25, 35.5), (103.75, 35.5)])
    for shape in (outline, hole):
        corners = [p for p, _ in corner_points(shape)]
        chamfered(shape, 6, corners)                       # refused or cut off, not a crash
        filleted(shape, 6)
