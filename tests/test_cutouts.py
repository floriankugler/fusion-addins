"""Face cutouts (`Board.cutout`, `lang.core.cutouts`), as the cutouts_native
add-in makes them: full, cross and triangles."""
import math
from pathlib import Path

import pytest
from shapely.geometry import Point, Polygon, box

from lang import *
from lang.core import cutouts
from lang.core.layout import build_layout
from lang.core.ops import Chamfer, Cut, Pocket
from lang.core.scope import registry
from lang.emit.arcs import Arc2, Line2, fit
from lang.emit.plan import Arc, ChamferStep, Line, PocketStep, ShapeContour, pieces, plan_layout
from lang.preview.mesh import mesh_part
from lib import cutout_patterns as data
from helpers import ply15

CAB = Box.from_size(width=600, depth=500, height=720)


def _side() -> tuple[Scope, Board]:
    """A 15 mm side on the cabinet's left: its outline is x 0..500 (depth),
    z 0..720 (height); the outer face is y = 0, the inner y = 15."""
    with module("cab", CAB) as cab:
        side = board("left", ply15).on(cab.left)
    return cab, side


def _material(part: Board, *points: tuple[float, float]) -> list[bool]:
    return [bool(part.outline.geometry.contains(Point(p))) for p in points]


def test_a_full_cutout_keeps_the_border_from_the_inner_face():
    cab, side = _side()
    with cab:
        side.cutout(chamfer=1)
    cut, chamfer = side.ops
    assert isinstance(cut, Cut) and cut.name == "cutout"
    assert isinstance(chamfer, Chamfer) and chamfer.what == "cutout" and chamfer.size == 1
    assert chamfer.face == side.inner.world_name == "right"          # not the show face
    assert side.machine_face.world_name == "right"
    # the border is 20 wide, the corners rounded with 8
    assert _material(side, (19.9, 300), (20.1, 300), (480.1, 300), (250, 700.1), (22, 22)) == \
        [True, False, True, True, True]
    hole = box(20, 20, 480, 700)
    # (the arcs are polygons with a vertex every degree)
    assert side.outline.area == pytest.approx(500 * 720 - hole.area + (4 - math.pi) * 64, abs=0.05)


def test_the_cutout_spares_what_the_board_has_and_names_material_cut_free():
    cab, side = _side()
    with cab:
        side.hole(d=10, depth=10, at=side.inner.front(25).bottom(300), name="pin")   # near the border
        side.cutout()
    # the ring of 20 around the pin joins the border; its centre stays material
    assert _material(side, (25, 300), (25 + 5 + 19.9, 300), (25 + 5 + 20.1, 300 + 40)) == [True, True, False]
    registry.reset()
    cab, side = _side()
    with cab:
        side.hole(d=10, depth=10, at=side.inner.center, name="pin")
        with pytest.raises(LangError, match="around the hole 'pin' free"):
            side.cutout()
    assert side.ops[-1].kind == "hole"                                   # a failed cutout changes nothing


def test_rings_around_round_features_are_exact_circles():
    cab, side = _side()
    with cab:
        side.cut(circle(30), at=side.inner.front(40).bottom(360), name="port")   # its ring meets the border
        side.cutout()
    # the opening's contour near the port is an arc of radius 15 + 20 about it
    curves = [c for ring in side.outline.rings()[1:] for c in fit(ring)]
    radii = sorted({round(c.radius, 9) for c in curves if isinstance(c, Arc2)})
    assert 35.0 in radii and 8.0 in radii
    assert not [c for c in curves if isinstance(c, Line2) and math.dist(c.a, c.b) < 0.05]


def test_a_pocket_cutout_has_several_pieces_in_the_layout():
    cab, side = _side()
    with cab:
        side.cutout(pattern=cross(40), depth=to(side.outer, -3), chamfer=1)
    pocket = side.ops[0]
    assert isinstance(pocket, Pocket) and pocket.depth == 12 and pocket.face == "right"
    part = build_layout()["modules"][0]["parts"][0]
    op = part["ops"][0]
    assert op["kind"] == "pocket" and len(pieces(op["shape"])) == 4
    plan = plan_layout(build_layout())
    steps = plan.parts[0].steps
    assert isinstance(steps[0], PocketStep) and len(steps[0].shapes) == 4
    assert isinstance(steps[1], ChamferStep) and isinstance(steps[1].contour, ShapeContour)
    assert len(steps[1].contour.loops) == 4
    mesh = mesh_part(part, build_layout()["frame"])
    # the preview shows the rims' chamfer too: half a square millimetre
    # for every millimetre of rim (its pocket tool reaches 0.005 deeper)
    chamfer = 0.5 * pocket.shape.geometry.boundary.length
    expected = side.outline.area * 15 - pocket.shape.area * 12.005 - chamfer
    assert mesh.volume == pytest.approx(expected, rel=1e-5)


def test_the_cross_leaves_two_diagonal_bands():
    cab, side = _side()
    with cab:
        side.cutout(pattern=cross(40))
    centre = (250, 360)
    assert _material(side, centre, (250, 100), (100, 360)) == [True, False, False]
    # material along the diagonals, 20 either side of them
    d = (460, 680)
    n = math.hypot(*d)
    at = (20 + d[0] * 0.25, 20 + d[1] * 0.25)
    normal = (-d[1] / n, d[0] / n)
    assert _material(side, (at[0] + normal[0] * 19, at[1] + normal[1] * 19),
                     (at[0] + normal[0] * 21, at[1] + normal[1] * 21)) == [True, False]
    with cab, pytest.raises(LangError, match="too wide"):
        board("other", ply15).on(cab.right).cutout(pattern=cross(400))


def test_triangles_lie_a_true_spacing_apart():
    cab, side = _side()
    with cab:
        side.cutout(pattern=triangles(4, 5, spacing=20, along="height"))
    ops = side.ops
    holes = [r for r in side.outline.rings()[1:]]
    assert len(holes) == 5 * 5                                         # 4 pitches: 5 columns, 5 rows
    polys = [Polygon(r) for r in holes]
    gaps = sorted(a.distance(b) for i, a in enumerate(polys) for b in polys[i + 1:])
    assert gaps[0] == pytest.approx(20, abs=1e-6)
    assert isinstance(ops[0], Cut)


def test_aligned_triangle_tips_touch_the_next_row():
    sizes = data.triangles(460, 680, 8, 6, 20, aligned_radius=8)
    frame = cutouts.PatternFrame((20, 20, 480, 700), 0, (-1, -1))
    result = cutouts.openings(box(20, 20, 480, 700), frame, triangles(8, 6, 20, aligned=True), 8, "t")
    first_row = [p for p in result.pieces if p.bounds[1] < 21]
    # the upward triangles of the first row reach exactly to its top, the
    # downward ones exactly to its bottom
    assert max(p.bounds[3] for p in first_row) == pytest.approx(20 + sizes.height, abs=1e-6)
    assert min(p.bounds[1] for p in result.pieces) == pytest.approx(20, abs=1e-6)
    assert result.dropped == 0


def test_the_start_corner_and_direction_of_triangles():
    cab, side = _side()
    with cab:
        side.cutout(pattern=triangles(4, 3, 20, along="depth", start=side.inner.top.back))
    # the first triangle points away from its corner, so at the top back
    # corner there is a half triangle reaching into the corner
    assert _material(side, (472, 692)) == [False]
    assert _material(side, (28, 692)) == [False]                      # 4 pitches: the front end too
    # the second column points the other way: its tip, not its base, is at the top
    sizes = data.triangles(460, 680, 4, 3, 20)
    assert _material(side, (480 - sizes.pitch_u, 692)) == [True]


def test_operations_after_a_cutout_must_not_fall_into_it():
    cab, side = _side()
    with cab:
        side.cutout(name="vent")
        side.hole(d=5, depth=10, at=side.inner.front(10).bottom(100))    # in the border
        with pytest.raises(LangError, match="lies in the cutout 'vent'"):
            side.hole(d=5, depth=10, at=side.inner.center)


def test_keep_leaves_material_where_a_shelf_meets_the_side():
    with module("cab", CAB) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        shelf = board("shelf", ply15).on(Pos("z", 300), toward=cab.top).between(left, right)
        left.cutout(keep=[shelf])
        shelf.join(left, right, using=screws(count=2))
        # the shelf strip, 20 either side
        assert _material(left, (250, 307), (250, 300 - 19), (250, 315 + 19), (250, 300 - 21)) == \
            [True, True, True, False]
        right.cutout(keep=[shelf])
        with pytest.raises(LangError, match="across the cutout 'cutout'"):
            board("shelf2", ply15).on(Pos("z", 500), toward=cab.top).between(left, right).join(
                right, using=screws(count=2))


def test_pieces_too_small_for_the_radius_are_left_out_and_noted():
    cab, side = _side()
    with cab:
        # material from 30 to 360 in height: a 10 mm sliver at the bottom
        side.cutout(keep=Box.from_sides(front=Pos("x", 0), back=Pos("x", 500), left=Pos("y", 0),
                                        right=Pos("y", 15), bottom=Pos("z", 30), top=Pos("z", 360)),
                    around=0)
    assert _material(side, (250, 25), (250, 500)) == [True, False]
    problems = build_layout()["modules"][0]["problems"]
    assert problems == ["cab.left: cutout 'cutout' left out 1 piece(s) too small for the 8 mm corner radius."]


def test_a_region_limits_the_cutout():
    cab, side = _side()
    with cab:
        side.cutout(rect(depth=200, height=100), at=side.inner.bottom(100))
    cut = side.ops[0]
    assert isinstance(cut, Cut)
    u0, v0, u1, v1 = cut.shape.bounds
    assert (u0, v0, u1, v1) == pytest.approx((150, 100, 350, 200))
    with cab, pytest.raises(LangError, match="narrow face"):
        side.cutout(side.front)


def test_shared_pattern_math():
    w, h = data.triangle_dimensions(560, 360, 8, 6, 20)
    assert (w, h) == pytest.approx((84.2232, 43.3333), abs=1e-4)


def _loops_are_continuous() -> None:
    """Every loop the emitter draws starts each curve where the one before
    ends, as Fusion needs to make a wire of it."""
    for part in plan_layout(build_layout()).parts:
        loops = list(part.body.loops)
        for step in part.steps:
            if isinstance(step, PocketStep):
                loops += [loop for shape in step.shapes for loop in shape]
        for loop in loops:
            ends = [(c.a, c.b) for c in loop if isinstance(c, (Line, Arc))]
            for (_, b), (a, _) in zip(ends, ends[1:] + ends[:1]):
                assert math.dist(a, b) < 1e-9


def test_rings_keep_sharp_corners_that_the_fillets_round():
    """As Fusion offsets a loop: a pocket's ring is a larger rectangle,
    here ending on the border line; the cutout's fillets round its
    corners like any other."""
    cab, side = _side()
    with cab:
        side.pocket(rect(depth=40, height=20), at=side.right.bottom(40), depth=5, name="dado")
        side.hole(d=10, depth=through, at=side.right.front(25).bottom(300), name="pin")
        side.cutout(side.right, chamfer=1)
    curves = [c for ring in side.outline.rings()[1:] for c in fit(ring)]
    assert sorted({round(c.radius, 6) for c in curves if isinstance(c, Arc2)}) == [8.0, 25.0]
    # the ring spans x 210..290 and z 20..80: its top left corner is
    # rounded with 8 about (218, 72); where its bottom left corner meets
    # the border, the opening's corner is rounded with 8 about (202, 28)
    assert _material(side, (211, 79), (213, 77), (209, 20.5), (200.5, 20.5)) == [False, True, True, False]
    _loops_are_continuous()


def test_the_example_s_loops_are_continuous():
    import runpy
    runpy.run_path(str(Path(__file__).parents[1] / "examples" / "cutouts.py"))
    _loops_are_continuous()
