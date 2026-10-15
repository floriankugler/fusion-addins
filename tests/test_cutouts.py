"""Face cutouts (`Board.cutout`, `lang.core.cutouts`), as the cutouts_native
add-in makes them: full, cross and triangles."""
import math

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
from helpers import EXAMPLES, ply12, ply15, run_example

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
    assert isinstance(cut, Cut) and cut.name == "openings"
    assert isinstance(chamfer, Chamfer) and chamfer.what == "openings" and chamfer.size == 1
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
    # for every millimetre of rim
    chamfer = 0.5 * pocket.shape.geometry.boundary.length
    expected = side.outline.area * 15 - pocket.shape.area * 12 - chamfer
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
        with pytest.raises(LangError, match="across the cutout 'openings'"):
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
    assert problems == ["cab.left: cutout 'openings' left out 1 piece(s) too small for the 8 mm corner radius."]


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
    run_example(EXAMPLES / "cutouts.py", run_name="__main__")
    _loops_are_continuous()


def test_a_border_closing_a_round_ended_board_leaves_nothing_to_cut_out():
    """Found by fuzzing: a slanted rail 22 wide with round ends, its border
    11, all but closes the inset; the sliver left had too few vertices once
    snapped onto its circles and shapely raised a ValueError."""
    from lang.core.shapes import slot_shape
    with module("m", Box.from_size(width=600, depth=500, height=720)) as m:
        rail = board("rail", ply15, slot_shape((73.0, 50.0), (172.0, 149.0), 22)).on(m.bottom)
        with pytest.raises(LangError, match="leaves nothing of the face"):
            rail.cutout(border=11)
    assert cutouts.grown(slot_shape((73.0, 50.0), (172.0, 149.0), 22).geometry, -11.0).is_empty


def test_a_cut_refused_for_lying_in_a_cutout_leaves_the_outline_as_it_was():
    """Found by fuzzing: a through cut made after a cutout, in its opening,
    was refused, but the outline had already taken it."""
    cab, side = _side()
    with cab:
        side.cutout()
        before = side.outline.geometry.wkt
        with pytest.raises(LangError, match="lies in the cutout"):
            side.cut(circle(30), at=side.inner.center, name="port")
    assert side.outline.geometry.wkt == before


def test_pieces_rounded_as_a_router_would_keep_their_new_arcs_off_a_large_arc():
    """Found by fuzzing: triangles in a back with corners rounded 197.5. A
    piece too tight for exact fillets is rounded as a router would, and its
    arcs put back on their circles; the 190 mm arc of the region pulled the
    vertices of the new 11 mm arcs beside it onto its circle too, leaving
    corners the router cannot cut."""
    from lang.core.geometry import polygons_of
    from lang.core.shapes import Shape
    with module("m", Box.from_size(width=631, depth=100, height=1124)) as m:
        back = board("back", sheet_material("birch", t=9), Shape(box(0, 0, 631, 1124)).rounded(197.5322915245099)).on(m.back)
        inner, outer = back.big_faces()[1], back.big_faces()[0]
        back.cutout(inner, pattern=triangles(9, 5, 27.5), border=7.809625022994677, around=27.5, radius=11,
                    depth=to(outer, -1), name="openings")
    op = back.op("openings").op
    assert isinstance(op, Pocket)
    for piece in polygons_of(op.shape.geometry):
        reached = piece.buffer(-10.89, quad_segs=64).buffer(10.89, quad_segs=64)
        assert max([g.area for g in polygons_of(piece.difference(reached))], default=0.0) < 0.12


def test_a_refused_cutout_leaves_no_note_of_pieces_left_out():
    """Found by fuzzing: a cutout noted the pieces too small for its radius
    and was then refused (here: it would cut the ring around a hole free),
    and the note stayed in the layout's problems."""
    cab, side = _side()
    with cab:
        side.hole(d=10, depth=10, at=side.inner.front(250).bottom(500), name="pin")
        with pytest.raises(LangError, match="free"):
            side.cutout(keep=Box.from_sides(front=Pos("x", 0), back=Pos("x", 500), left=Pos("y", 0),
                                            right=Pos("y", 15), bottom=Pos("z", 30), top=Pos("z", 360)),
                        around=0)
    assert side.notes == []


def test_material_kept_around_a_box_keeps_its_width_where_a_piece_is_rounded_as_a_router_would():
    """Found by fuzzing: aligned triangles in a side with corners rounded
    246 and boxes kept at two corners. Where a piece was too tight for
    exact fillets, putting its arcs back on their circles pulled the new 8
    mm arcs onto the 226 mm arc beside them: the opening came 0.33 nearer
    a kept box than around=, and left corners a router cannot cut."""
    from shapely.geometry import box as shapely_box
    from lang.core.geometry import polygons_of
    from lang.core.shapes import Shape
    around = 24.735671773755076
    with module("m", Box.from_size(width=100, depth=2051.8963873156627, height=741)) as m:
        side = board("side", ply12, Shape(box(0, 0, 2051.8963873156627, 741)).rounded(246.05583529874647)).on(m.left)
        boxes = [(1861.1499947555708, 0.0, 2078.649994755571, 107.0), (1.0, 2.0, 167.0, 64.0)]
        keep = [Box({"x": u0, "y": 0, "z": v0}, {"x": u1, "y": 12, "z": v1}) for u0, v0, u1, v1 in boxes]
        outer = next(f for f in side.big_faces() if f.direction == side.show_face.direction)
        side.cutout(pattern=triangles(3, 3, 25.0, aligned=True), around=around, depth=to(outer, -2), keep=keep)
    op = side.op("openings").op
    assert isinstance(op, Pocket)
    for u0, v0, u1, v1 in boxes:
        assert op.shape.geometry.distance(shapely_box(u0, v0, u1, v1)) >= around - 1e-3
    for piece in polygons_of(op.shape.geometry):
        reached = piece.buffer(-7.92, quad_segs=64).buffer(7.92, quad_segs=64)
        assert max([g.area for g in polygons_of(piece.difference(reached))], default=0.0) < 0.07


def test_a_channel_narrower_than_the_cutter_is_not_cut_out():
    """Found by fuzzing: a box kept 0.56 from the border left a channel that
    wide and 150 long between them, which the exact fillets of its corners
    kept; no cutter of radius 3 reaches into it. The opening parts there."""
    from shapely.geometry import box as shapely_box
    from lang.core.geometry import polygons_of
    with module("m", Box.from_size(width=88.6, depth=2400, height=100)) as m:
        rail = board("rail", ply12).on(m.bottom)
        keep = Box({"x": 1762.6, "y": 43.06, "z": 0}, {"x": 1912.2, "y": 120, "z": 12})
        rail.cutout(border=36, around=6.5, radius=3, depth=10, keep=keep)
    op = rail.op("openings").op
    assert isinstance(op, Pocket)
    assert len(polygons_of(op.shape.geometry)) == 2
    assert op.shape.geometry.intersection(shapely_box(1762.6, 36, 1912.2, 37)).area == 0


def test_a_line_meeting_a_large_arc_keeps_its_place_where_a_piece_is_rounded_as_a_router_would():
    """Found by fuzzing: a turned pocket at a corner rounded 203. Where a
    piece was rounded as a router would, a vertex of the edge kept around
    the pocket, near the corner's 183 mm arc, lay within the snap tolerance
    of that arc's circle and went onto it, turning the edge toward the
    pocket: less than around= of material was left."""
    from shapely import affinity
    from shapely.geometry import box as shapely_box
    from lang.core.shapes import Shape
    with module("m", Box.from_size(width=465, depth=2088.5397851525, height=100)) as m:
        panel = board("panel", sheet_material("birch", t=24), Shape(box(0, 0, 2088.5397851525, 465)).rounded(202.89706660649423))
        panel.on(m.bottom)
        pocket = affinity.rotate(shapely_box(85 - 41.25, 428.5 - 15.92, 85 + 41.25, 428.5 + 15.92), 30, origin=(85, 428.5))
        panel.add_pocket(panel.big_faces()[0], Shape(pocket), 5.5)
        panel.cutout(around=28, radius=4, depth=8)
    op = panel.op("openings").op
    assert isinstance(op, Pocket)
    assert op.shape.geometry.distance(pocket) >= 28 - 1e-3


def test_arcs_that_touch_in_the_example_meet_without_a_flat():
    """Found compiling fuzz boards in Fusion: where a corner's fillet,
    rounded as a router would, touches the material kept around a slot,
    the two arcs met through a short flat (30 in this example, up to 0.8
    long): an extra face each in Fusion, and rim chamfers failed along
    them. Arcs that touch meet where they touch."""
    run_example(EXAMPLES / "cutouts.py", run_name="__main__")
    layout = build_layout()
    flats: list[float] = []
    for part in layout["modules"][0]["parts"]:
        for op in part["ops"]:
            if op["kind"] != "cut" and op["kind"] != "pocket":
                continue
            for ring in op["shape"]:
                curves = fit(ring)
                for k, c in enumerate(curves):
                    a, b = curves[k - 1], curves[(k + 1) % len(curves)]
                    if isinstance(c, Line2) and isinstance(a, Arc2) and isinstance(b, Arc2):
                        d = math.dist(a.center, b.center)
                        if min(abs(d - a.radius - b.radius), abs(d - abs(a.radius - b.radius))) < 0.05:
                            flats.append(math.dist(c.a, c.b))
    assert flats == []


def test_an_offset_runs_its_arcs_on_to_meet_at_a_corner_as_fusion_does():
    """Checked in Fusion (sketch offset, as cutouts_native makes it): where
    an offset extends a corner with an arc, the arc runs on along its
    circle to meet the line or arc beside it. A circle cut by a line,
    grown 10, gets its corners where the line moved 10 meets the circle of
    60; a lens, where its two circles grown 10 cross. `grown` mitred the
    tangents, up to a millimetre off."""
    d_shape = cutouts.circle_geometry((0, 0), 50).intersection(box(-60, -60, 20, 60))
    grown_d = cutouts.grown(d_shape, 10)
    assert isinstance(grown_d, Polygon)
    for corner in ((30, 51.9615), (30, -51.9615)):
        assert min(math.dist(corner, p) for p in grown_d.exterior.coords) < 1e-3
    lens = cutouts.circle_geometry((180, 0), math.sqrt(1300)).intersection(
        cutouts.circle_geometry((220, 0), math.sqrt(1300)))
    grown_lens = cutouts.grown(lens, 10)
    assert isinstance(grown_lens, Polygon)
    for tip in ((200, 41.4863), (200, -41.4863)):
        assert min(math.dist(tip, p) for p in grown_lens.exterior.coords) < 1e-3


def _rounded_rect(cx: float, cy: float, w: float, h: float, r: float, angle: float) -> Polygon:
    from shapely import affinity
    turned = affinity.rotate(box(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), angle, origin=(cx, cy))
    assert isinstance(turned, Polygon)
    out = cutouts.filleted(turned, r)
    assert out is not None
    return out


def test_an_inset_leaves_out_the_short_edge_it_turns_over():
    """Found by fuzzing: a strip 1.9 wide cut across a rounded board leaves a
    1.2 long edge where it leaves the board; inset 24, that edge turned over
    and the inset cut a corner of 0.7 nearer the outline than 24."""
    from shapely import affinity
    strip = affinity.rotate(box(8.39 - 0.95, -33 - 123.25, 8.39 + 0.95, -33 + 123.25), 49.394, origin=(8.39, -33))
    shape = _rounded_rect(2.5, -117, 146.5, 362.5, 71.785, 45).difference(strip)
    inset = cutouts.grown(shape, -24)
    assert inset.difference(shape).area < 1e-3
    assert min(shape.boundary.distance(Point(p)) for g in [inset] for poly in getattr(g, "geoms", [g])
               for p in poly.exterior.coords) > 24 - 0.05


def test_a_mitred_inset_that_crosses_itself_is_made_valid_inside_the_shape():
    """Found by fuzzing: where the exact offset does not hold (here several
    curves vanish), `grown` falls back on shapely's mitred inset, which
    crossed itself; it was returned invalid, and made valid as it was, it
    kept a loop 85 mm2 outside the shape."""
    from shapely import affinity
    plank = affinity.rotate(box(150 - 169.5, 6 - 60.25, 150 + 169.5, 6 + 60.25), 113.87076114073832, origin=(150, 6))
    shape = Point(200, 199).buffer(4, quad_segs=16).union(plank) \
        .union(_rounded_rect(20, -8, 76.5, 186.33816842793146, 17.234659367932753, 0.99999)) \
        .difference(cutouts.circle_geometry((-200, -181.5), 150))
    inset = cutouts.grown(shape, -14)
    assert inset.is_valid and inset.difference(shape).area < 1e-3


def test_an_offset_does_not_turn_an_edge_onto_an_arc_beside_it():
    """Found by fuzzing: grown 12, the mitred corner where a long edge met
    an arc of 51 lay within the snap tolerance of the arc's offset circle
    and was moved onto it, turning the edge: material within 12 of the
    shape was left out of the offset."""
    from shapely import affinity
    plank = affinity.rotate(box(11 - 22, -144.05 - 136, 11 + 22, -144.05 + 136), 45, origin=(11, -144.05))
    shape = plank.intersection(_rounded_rect(22, -63, 181, 255, 50.76781764318775, 45))
    grown = cutouts.grown(shape, 12)
    assert shape.buffer(12 - 1e-3, quad_segs=64).difference(grown).area < 0.05


def test_openings_touching_the_outline_at_a_point_are_an_error():
    """Found compiling fuzz boards in Fusion: a cutout with no border and
    sharp corners had openings touching the board's edge at single points,
    and Fusion made no profile of the outline (the part was left out)."""
    with module("m", Box.from_size(width=300, depth=400, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom)
        with pytest.raises(LangError, match="touches the board's outline at a point only"):
            panel.cutout(pattern=triangles(4, 3, 20), border=0, radius=0)
        panel.cutout(pattern=triangles(4, 3, 20), border=10, radius=0)     # with a border
    assert panel.has_operation("openings")


def test_pocket_openings_touching_the_outline_at_a_point_are_an_error_too():
    """Found compiling fuzz boards in Fusion: one row of triangles with no
    border and sharp corners reached from edge to edge, each apex on the
    far edge; as a pocket the material either side met at that point only,
    and Fusion chamfered no rim through it ("non-manifold edge or
    vertex"). Only through cutouts were checked."""
    with module("m", Box.from_size(width=300, depth=400, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom)
        with pytest.raises(LangError, match="touches the board's outline at a point only"):
            panel.cutout(pattern=triangles(6, 1, 5), border=0, radius=0, depth=5, chamfer=1)
        assert not panel.has_operation("openings") and panel.ops == []
        panel.cutout(pattern=triangles(6, 1, 5), border=10, radius=0, depth=5, chamfer=1)
    assert panel.has_operation("openings")


def test_an_opening_that_touches_itself_at_a_point_is_an_error():
    """Found by fuzzing: the material kept 2 around a through pocket, turned
    45 degrees at a board's corner, pinched a pocket cutout's opening to a
    point (1e-14 across); Fusion made no surface of it ("Cover failed to
    make a surface"), and the preview could not mesh it."""
    from shapely import affinity
    from lang.core.shapes import Shape
    with module("m", Box.from_size(width=41, depth=40, height=100)) as m:
        panel = board("panel", sheet_material("birch", t=6)).on(m.bottom)
        top = panel.big_faces()[0]
        panel.add_hole(top, (0, 0), 2, through)
        panel.add_pocket(top, Shape(affinity.rotate(box(-27, -7.5, 27, 7.5), 45, origin=(0, 0))), through)
        with pytest.raises(LangError, match=r"an opening touches itself at a point only \(x 13.7886, y 27.2236\)"):
            panel.cutout(border=0, around=2, radius=8, depth=3)
        panel.cutout(border=0, around=3, radius=8, depth=3)
    assert panel.has_operation("openings")


def test_an_offset_closing_a_hole_leaves_no_speck_of_it():
    """Found by fuzzing: a ring around a hole of 0.5 (16 segments a
    quarter), grown by 0.5, kept a hole 0.6 um across, which no drawing
    can make."""
    from shapely.geometry import Point as P
    ring = P(0, 0).buffer(1, quad_segs=64).difference(P(0, 0).buffer(0.5, quad_segs=16))
    grown = cutouts.grown(ring, 0.5)
    assert isinstance(grown, Polygon) and len(grown.interiors) == 0
    assert grown.area == pytest.approx(math.pi * 1.5 ** 2, rel=1e-3)


def test_an_inset_of_a_notched_outline_keeps_the_border():
    """Found by fuzzing: a tapered board with a turned notch in its edge,
    inset by a border of 33.5; offset curve by curve, the notch's short
    edges vanished in the wrong order and the inset came 0.4 near the
    outline. Outlines of lines only are offset mitred, exactly."""
    outline = Polygon([(448.0, 0.0), (114.581188, 0.0), (138.717251, 24.136062), (122.100241, 40.753072),
                       (87.402372, 6.055203), (93.457575, 0.0), (0.0, 0.0), (0.0, 435.960215),
                       (2.560516, 435.960215), (2.560516, 471.246822), (448.0, 79.273343)])
    inset = cutouts.grown(outline, -33.53137272894515)
    from lang.core.geometry import polygons_of
    assert min(outline.boundary.distance(Point(q)) for g in polygons_of(inset) for q in g.exterior.coords) \
        > 33.53137272894515 - 1e-6


def _keeps(offset: object, shape: object, d: float) -> float:
    """How near the offset's boundary comes to the shape, sampled every mm."""
    from lang.core.geometry import polygons_of
    near = math.inf
    for poly in polygons_of(offset):  # pyright: ignore[reportArgumentType]
        for ring in [poly.exterior, *poly.interiors]:
            pts = list(ring.coords)
            for a, b in zip(pts, pts[1:]):
                n = max(2, math.ceil(math.dist(a, b)))
                for k in range(n):
                    q = Point(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n)
                    near = min(near, shape.distance(q))  # pyright: ignore[reportAttributeAccessIssue]
    return near


def test_an_offset_leaves_out_the_slivers_a_boolean_leaves():
    """Found by fuzzing: a square turned 45 degrees, cut away by a band
    exactly as wide, left a hairline of 7e-18 mm2 along its edge; grown by
    1, it became a piece of 3.8 mm2 that was never there."""
    from shapely import affinity
    from shapely.geometry import box as shapely_box
    from lang.core.cutouts import grown
    from lang.core.geometry import polygons_of
    diamond = affinity.rotate(shapely_box(-0.5, 25.5, 0.5, 26.5), 45, origin=(0, 26))
    band = affinity.rotate(shapely_box(-43.5, 25.5, 43.5, 26.5), 45, origin=(0, 26))
    shape = shapely_box(-0.5, -0.5, 0.5, 0.5).union(diamond.difference(band))
    assert len(polygons_of(shape)) == 2                         # the square and a hairline
    out = grown(shape, 1.0)
    assert isinstance(out, Polygon) and out.area == pytest.approx(9)


def test_a_mitred_outward_offset_that_crosses_itself_keeps_its_distance():
    """Found by fuzzing: a board with a slot 13 wide, grown 12 (the slot
    closes); shapely's mitred offset crossed itself, and made valid it
    left a hole whose edge came 1 near the board."""
    from shapely import affinity
    plank = affinity.rotate(box(58.5 - 156, -195 - 146.5, 58.5 + 156, -195 + 146.5), 45, origin=(58.5, -195))
    shape = plank.difference(_rounded_rect(-24, -129.39168986042338, 167, 13, 5.1121214425749875, 167.74464669019994)) \
        .difference(Point(-199.5, 84).buffer(87.56326547666144, quad_segs=8)) \
        .intersection(_rounded_rect(57, -199, 175, 152, 38.96699518115837, 45))
    assert _keeps(cutouts.grown(shape, 12), shape, 12) > 12 - 0.06


def test_an_offset_whose_edge_passes_near_between_its_ends_is_refused():
    """Found by fuzzing: grown 21.5, a corner where the offset curves did
    not meet was joined by dropping a curve, and the edge that left passed
    0.8 nearer the board than 21.5 between its ends, where the check, which
    looked at ends and middles only, did not see it (Fusion bridges such a
    corner with a line). Now the offset is checked along its edges and the
    mitred one taken instead."""
    shape = _rounded_rect(0, 76, 73.34223977009138, 300.3733725850022, 7.334223977009138, 120.45463784150706) \
        .difference(_rounded_rect(59.5, 188.5, 399, 183, 60.32945596815371, 45))
    assert _keeps(cutouts.grown(shape, 21.52965333733873), shape, 21.53) > 21.52965333733873 - 0.25


def test_an_arc_drawn_on_whole_degrees_keeps_its_first_step_above_half_a_degree():
    """Found by fuzzing: an arc's ends are left half a degree clear of the
    whole degrees between them; a step of exactly half a degree is
    `lang.emit.arcs`' smallest, and rounding put it just below, so the
    arc was found one vertex late and a short line was left (a circle of
    16 segments a quarter united with an exact one and grown 0.004, its
    mirror image found whole). Ends are 0.6 degrees clear now."""
    from shapely import affinity
    from shapely.geometry.polygon import orient
    from shapely.ops import unary_union
    shape = unary_union([Point(0, 65).buffer(56.5, quad_segs=32), cutouts.circle_geometry((0, 0), 119)])
    grown = cutouts.grown(shape, 0.00390625)
    for g in (grown, affinity.scale(grown, -1, 1, origin=(0, 0))):
        assert isinstance(g, Polygon)
        ring = [(float(x), float(y)) for x, y in list(orient(g, 1.0).exterior.coords)[:-1]]
        assert [type(c).__name__ for c in fit(ring)] == ["Arc2", "Arc2"]


def test_a_border_next_to_a_notch_by_a_rounded_corner_keeps_its_width():
    """Found by fuzzing: a small turned notch where a board's rounded
    corner begins; offset curve by curve, the notch's offset did not meet
    the corner arc's, the shorter curve was dropped, and the inset came
    0.17 nearer the outline than the border, inside the 1 % of the offset
    the check allowed. It falls back to the mitred offset now."""
    from shapely import affinity
    from shapely.geometry import box as shapely_box
    from lang.core.shapes import Shape
    with module("m", Box.from_size(width=354, depth=354, height=100)) as m:
        panel = board("panel", sheet_material("birch", t=6), Shape(shapely_box(0, 0, 354, 354)).rounded(47.015625)).on(m.bottom)
        panel.add_cut(Shape(affinity.rotate(shapely_box(341.5, 17, 343.5, 23), 45, origin=(342.5, 20))))
        (outline,) = panel.outline.polygons()
        panel.cutout(border=20, around=20, radius=0)
    op = panel.op("openings").op
    assert isinstance(op, Cut)
    assert op.shape.geometry.distance(outline.exterior) >= 20 - 0.03


def test_an_inset_loses_nothing_farther_than_the_border():
    """Found by fuzzing (a cross's band cut into): a slot 2 wide cut
    through a board's rounded corner; offset curve by curve, its walls
    turned over at an inset of 20, and the inset lost its corner beside the
    slot, 255 mm2, though it kept its distance and lay in the shape. The
    cross was laid out over what was left, 17 mm narrower, and its
    openings ran into the bands."""
    from shapely.geometry import Point as P
    from lang.core.shapes import Shape
    board_outline = Shape(box(0, 0, 121, 118.5)).rounded(29.625).difference(Shape(box(15, 2.5, 17, 63.5)))
    (outline,) = board_outline.polygons()
    assert len(outline.interiors) == 0                  # the slot runs out through the corner
    inset = cutouts.grown(outline, -20)
    assert inset.bounds[0] == pytest.approx(20) and inset.contains(P(30, 90))
