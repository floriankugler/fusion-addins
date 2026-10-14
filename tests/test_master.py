"""Reading the master's snapshot, and contours as limits (fixture:
examples/van_snapshot.json, the snapshot of tools/van_master.py)."""
import math
from pathlib import Path

import pytest
from shapely.geometry import MultiPolygon, Point, Polygon, box

from lang import *
from lang.core.contours import round_offset
from lang.core.geometry import polygons_of
from lang.core.layout import build_layout
from lang.core.refs import as_pos
from helpers import ply12, ply15

FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "van_snapshot.json"


@pytest.fixture
def van() -> Master:
    return master(FIXTURE)


# -- reading ---------------------------------------------------------------------

def test_relative_paths_start_at_the_calling_file():
    van = master("../examples/van_snapshot.json")
    assert van.path == FIXTURE
    assert van.source == "van master (tools/van_master.py)"


def test_planes_are_positions(van: Master):
    level = van.plane("Bodenniveau")
    assert as_pos(level) == Pos("z", 40)
    assert level - 12 == Pos("z", 28)
    assert van.plane("Wand FS").position == Pos("y", -890)
    assert (van.plane("Boden vorne") + van.plane("Boden hinten")) / 2 == Pos("x", 1700)
    # a plane in a moved component, in world coordinates
    assert van.plane("Bett.oben").position == Pos("z", 1000)


def test_a_tilted_plane_is_an_error_when_used(van: Master):
    roof = van.plane("Dach geneigt")         # binding it is fine
    with pytest.raises(LangError, match="tilted"):
        board("x", ply15).on(roof, toward=world_frame().direction("top")).box()


def test_boxes_and_parameters(van: Master):
    k = van.box("Moebel.Kueche")
    assert (k.lo["x"], k.lo["y"], k.lo["z"]) == (300, -890, 40)
    assert (k.width, k.depth, k.height) == (500, 600, 720)
    assert van.param("Lattenabstand") == 400
    assert van.param("Neigung") == pytest.approx(10)


def test_contours(van: Master):
    outline = van.contour("Bodenumriss")
    assert outline.closed and outline.normal_axis == "z"
    profile = van.contour("Bodenprofil")
    assert not profile.closed and profile.normal_axis == "x"


def test_missing_names_and_problems(van: Master):
    with pytest.raises(LangError, match="did you mean 'Bodenniveau'"):
        van.plane("Bodenniveu")
    with pytest.raises(LangError, match="separate chains"):
        van.contour("Fenster")
    with pytest.raises(LangError, match="no box 'Garage'"):
        van.box("Garage")


def test_frame_takes_the_opposites_from_three_directions():
    f = Frame(front="+y", left="+x", top="+z")
    assert f.direction("back").code == "-y" and f.direction("right").code == "-x"
    assert f.direction("bottom").code == "-z"


def test_layout_records_the_snapshot(van: Master):
    with module("m", van.box("Radkasten FS")):
        board("b", ply15).on(Box.from_sides(front=Pos("x", 2000), back=Pos("x", 2900), left=Pos("y", -890),
                                            right=Pos("y", -675), top=Pos("z", 250),
                                            bottom=Pos("z", 0)).top)
    layout = build_layout()
    [snapshot] = layout.get("snapshots", [])
    assert snapshot["hash"] == van.hash and snapshot["file"] == "van_snapshot.json"
    assert set(snapshot["boxes"]) >= {"Moebel.Kueche", "Bett"} and "Bodenumriss" in snapshot["contours"]
    # the filleted body is only a bounding box, which the layout says
    assert any("Radkasten FS" in p and "cuboid" in p for p in layout["problems"])


# -- contours as limits ---------------------------------------------------------------

def _battens(van: Master, *xs: float) -> list[Board]:
    outline, profile = van.contour("Bodenumriss"), van.contour("Bodenprofil")
    top = van.plane("Bodenniveau") - ply12.t
    with module("floor", van.box("Boden")):
        return [board(f"batten{i}", ply15).center(Pos("x", x)).between(top, profile.gap(2), outline)
                for i, x in enumerate(xs)]


def test_a_batten_follows_the_floor_profile(van: Master):
    [b] = _battens(van, 100)
    box = b.box()
    assert (box.lo["y"], box.hi["y"]) == pytest.approx((-890, 890))
    assert box.hi["z"] == pytest.approx(28)
    assert box.lo["z"] == pytest.approx(-6)          # 2 mm above the valleys at -8
    g = b.outline.geometry                            # (y, z)
    assert g.contains(Point(0, -5)) and not g.contains(Point(0, -6.5))       # in a valley
    assert g.contains(Point(-450, 2.5)) and not g.contains(Point(-450, 1.5))  # on a rib at 0
    assert not g.contains(Point(-889, 16.5))         # the floor rises to 15 at the wall


def test_battens_end_at_the_tighter_face_of_the_floor_outline(van: Master):
    clear, arch, arch_end = _battens(van, 1700, 2500, 2900)
    assert (clear.box().lo["y"], clear.box().hi["y"]) == pytest.approx((-890, 890))
    assert (arch.box().lo["y"], arch.box().hi["y"]) == pytest.approx((-675, 675))
    # Centred on the arch's rear end: the front face (x = 2892.5) is still
    # beside the arch's rounded corner, the rear face (2907.5) beside the
    # rounded wall corner (866.34), and the front one is tighter. The arc is
    # sampled at 0.1 mm, which is up to 0.2 mm on y where it runs steeply.
    lo, hi = arch_end.box().lo["y"], arch_end.box().hi["y"]
    assert lo == pytest.approx(-698.66, abs=0.25) and hi == pytest.approx(698.66, abs=0.25)


def test_a_panel_takes_the_outline_in_its_own_plane(van: Master):
    outline = van.contour("Bodenumriss")
    with module("floor", van.box("Boden")) as floor:
        panel = board("panel", ply12).on(floor.top).between(outline.gap(1), Pos("x", 1700), floor.back)
    box = panel.box()
    assert (box.lo["x"], box.hi["x"]) == pytest.approx((1700, 3399))
    assert (box.lo["y"], box.hi["y"]) == pytest.approx((-889, 889))
    g = panel.outline.geometry                        # (x, y)
    assert g.contains(Point(2500, 670)) and not g.contains(Point(2500, 680))   # the wheel arch notch
    assert g.contains(Point(3000, 880))


def test_an_open_contour_in_the_board_plane_is_an_edge(van: Master):
    edge = van.contour("Bett.Kante")                   # a line along x at y = -890, z = 900
    shelf = board("shelf", ply15).on(Pos("z", 1000), toward=world_frame().direction("bottom")).between(
        edge.gap(10), Pos("y", -500), Pos("x", 2400), Pos("x", 3000))
    box = shelf.box()
    assert (box.lo["y"], box.hi["y"]) == pytest.approx((-880, -500))


def test_an_open_contour_in_a_perpendicular_plane_gives_a_position(van: Master):
    edge = van.contour("Bett.Kante")
    side = board("side", ply15).center(Pos("x", 3000)).between(edge.gap(5), Pos("y", 0), Pos("z", 0), Pos("z", 500))
    assert (side.box().lo["y"], side.box().hi["y"]) == pytest.approx((-885, 0))
    with pytest.raises(LangError, match="does not reach"):
        board("past", ply15).center(Pos("x", 3500)).between(edge, Pos("y", 0), Pos("z", 0), Pos("z", 500)).box()


def test_contour_errors(van: Master):
    with pytest.raises(LangError, match="outside contour 'Bodenumriss'"):
        _battens(van, 3500)[0].box()
    with pytest.raises(LangError, match="split the board into 2 pieces"):
        with module("floor", van.box("Boden")) as floor:
            # a strip along the wall is cut in two by the wheel arch
            board("strip", ply12).on(floor.top).between(van.contour("Bodenumriss"), Pos("x", 1900),
                                                        Pos("x", 3000), Pos("y", -800), Pos("y", -750)).box()
    with pytest.raises(LangError, match="leave nothing"):
        with module("floor2", van.box("Boden")) as floor:
            board("strip", ply12).on(floor.top).between(van.contour("Bodenumriss"), Pos("x", 2400),
                                                        Pos("x", 2600), Pos("y", -800), Pos("y", -700)).box()


def _contour(name: str, points: list[tuple[float, float]], closed: bool, normal: str = "z") -> Contour:
    """A contour in the plane through the origin perpendicular to `normal`,
    its points in that plane's other two axes in x, y, z order."""
    i = "xyz".index(normal)
    axis = [0.0, 0.0, 0.0]
    axis[i] = 1.0

    def at(p: tuple[float, float]) -> tuple[float, float, float]:
        c = list(p)
        c.insert(i, 0.0)
        return (c[0], c[1], c[2])
    return Contour(name, tuple(at(p) for p in points), closed, (0.0, 0.0, 0.0), (axis[0], axis[1], axis[2]))


def test_a_board_across_a_contour_fits_over_its_whole_thickness():
    """A notch in the contour whose tip lies between the board's faces
    stops the board at the tip; sectioned at the two faces alone, the
    board ran 75 mm into it. Fuzzing found it."""
    notched = _contour("notched", [(0, 0), (200, 0), (200, 500), (110, 500), (100, 400), (90, 500), (0, 500)], True)
    b = board("b", ply15).center(Pos("x", 100)).between(notched, Pos("z", 0), Pos("z", 50))
    assert (b.box().lo["y"], b.box().hi["y"]) == pytest.approx((0, 400))
    # beside the notch, the board reaches the contour's edge
    beside = board("beside", ply15).center(Pos("x", 50)).between(notched, Pos("z", 0), Pos("z", 50))
    assert beside.box().hi["y"] == pytest.approx(500)


def test_an_open_contour_across_the_board_keeps_clear_over_its_whole_thickness():
    """A dip of the contour between the board's faces stops the board at
    its bottom; the tighter of the contour's crossings at the two faces ran
    the board 75 mm into it. Fuzzing found it."""
    dip = _contour("dip", [(0, 500), (90, 500), (100, 400), (110, 500), (200, 500)], False)
    b = board("b", ply15).center(Pos("x", 100)).between(dip, Pos("y", 0), Pos("z", 0), Pos("z", 50))
    assert b.box().hi["y"] == pytest.approx(400)


def test_an_open_contours_clearance_keeps_the_board_on_its_side():
    """The clearance to an open contour across the board does not carry
    the board past it: with the board's other limit inside the clearance it
    is an error, and where the clearance passes the middle of the room, the
    board lies beyond the clearance on the middle's side. They made a board
    inside the clearance, and one from the room's far end across the
    contour. Fuzzing found both."""
    edge = _contour("edge", [(0, 45), (200, 45)], False)
    inside_it = board("inside_it", ply15).center(Pos("x", 100)).between(edge.gap(10), Pos("y", 50), Pos("z", 0),
                                                                      Pos("z", 50))
    with pytest.raises(LangError, match="clearance reaches past the board's other limit"):
        inside_it.box()
    with module("m", Box({"x": 0, "y": 0, "z": 0}, {"x": 200, "y": 100, "z": 50})):
        b = board("b", ply15).center(Pos("x", 100)).between(edge.gap(10))
    assert (b.box().lo["y"], b.box().hi["y"]) == pytest.approx((55, 100))


def test_an_open_contours_clearance_counts_at_a_face_whichever_way_it_runs():
    """A contour that only just crosses the board's far face keeps the
    board its clearance there too, and a contour bending under the board
    gives the same end run either way. The offset contour fell short of the
    face ("the clearance moves it off the board"), and so did one run of
    the bent contour, not the other. Fuzzing found both."""
    slant = [(0.0, 100.0), (107.55, 110.0)]
    bent = [(630.0, 23.2), (230.0, 23.2), (211.5, 20.8), (167.7, 20.8), (149.1, 23.2), (50.0, 23.2)]
    for i, points in enumerate([slant, slant[::-1]]):
        b = board(f"slant{i}", ply15).center(Pos("x", 100)).between(
            _contour("slant", points, False).gap(3), Pos("y", 300), Pos("z", 0), Pos("z", 50))
        # 3 from the contour's end at the face's corner, the arc a polygon a little inside
        assert b.box().lo["y"] == pytest.approx(110 + math.sqrt(3 ** 2 - 0.05 ** 2), abs=0.015)
    for i, points in enumerate([bent, bent[::-1]]):
        b = board(f"bent{i}", material("thick", t=40)).center(Pos("x", 134)).between(
            _contour("bent", points, False).into(17), Pos("y", 1000), Pos("z", 0), Pos("z", 50))
        assert b.box().lo["y"] == pytest.approx(6.2)


def test_a_clearance_does_not_depend_on_how_the_contours_points_run():
    """The same outline, run the other way with points added along two of
    its edges, keeps the board where it was: GEOS's offset, which
    simplifies what it offsets as the points come, moved the board's end
    0.03 mm (the whole offset 0.14 mm) for a 26 mm gap. Fuzzing found it."""
    points = [(3.9415, 125.9767), (4.4927, 126.3301), (56.21, 141.3801), (56.21, 0.0), (3.7272, 2.4822)]
    back = points[::-1]
    resampled: list[tuple[float, float]] = []
    for j, (p, q) in enumerate(zip(back, back[1:] + back[:1])):
        resampled.append(p)
        if j % 3 == 0:
            resampled += [(p[0] + f * (q[0] - p[0]), p[1] + f * (q[1] - p[1])) for f in (0.3, 0.5, 0.7)]
    lows: list[float] = []
    for i, ring in enumerate([points, resampled]):
        b = board(f"panel{i}", ply15).center(Pos("z", 0)).between(_contour("outline", ring, True).gap(26))
        lows.append(b.box().lo["x"])
    assert lows[1] == pytest.approx(lows[0], abs=1e-9)


def test_an_area_shrunk_by_half_its_width_leaves_nothing_valid():
    """Found by fuzzing the contours: a slot 1 mm wide, turned 66.2
    degrees, shrunk by 0.5 left GEOS's sliver of no width along its
    spine, an invalid polygon; what an offset leaves is cleaned now, so
    nothing is left."""
    from shapely import affinity
    from lang.core.contours import round_offset
    slot = affinity.rotate(rect(depth=10, width=1).rounded(0.5).geometry, 66.2, origin=(0, 0))
    shrunk = round_offset(slot, -0.5)
    assert shrunk.is_valid and shrunk.area < 1e-6
    assert round_offset(slot, -0.25).is_valid and round_offset(slot, -0.25).area > 4


def test_an_offset_is_the_same_with_points_along_its_edges():
    """Points added along the edges of an area do not change its offset:
    simplified away, the points Douglas-Peucker split at stayed, and the
    square's four corners outside a rounded square grew otherwise.
    Fuzzing found it."""
    square = box(-1, -1, 1, 1)
    corners = square.difference(Shape(square).rounded(0.5).geometry)

    def along(ring: list[tuple[float, float]]) -> list[tuple[float, float]]:
        return [x for p, q in zip(ring, ring[1:] + ring[:1])
                for x in (p, (p[0] + 0.25 * (q[0] - p[0]), p[1] + 0.25 * (q[1] - p[1])))]
    more = MultiPolygon([Polygon(along([(x, y) for x, y in p.exterior.coords][:-1])) for p in polygons_of(corners)])
    assert round_offset(more, 1).symmetric_difference(round_offset(corners, 1)).area == 0


def test_a_closed_contour_around_nothing_is_an_error():
    """A closed contour of two points (a snapshot's sketch of one line
    drawn twice, before the writer refused it) is a LangError, not
    shapely's. Fuzzing found it."""
    twice = _contour("twice", [(0, 0), (100, 0)], True)
    b = board("b", ply15).center(Pos("z", 0)).between(twice, Pos("x", 0), Pos("x", 50), Pos("y", 0), Pos("y", 50))
    with pytest.raises(LangError, match="closed around nothing"):
        b.box()


def test_an_end_picks_one_piece_of_a_cut_up_board(van: Master):
    """A batten along the wall is cut in two by the wheel arch: with both
    ends it is an error that names the pieces, one end takes its piece."""
    outline = van.contour("Bodenumriss")
    front, back = van.plane("Boden vorne"), van.plane("Boden hinten")
    with module("floor", van.box("Boden")):
        whole = board("whole", ply15).center(Pos("y", -880)).between(outline, front, back, Pos("z", 0), Pos("z", 28))
        with pytest.raises(LangError, match=r"cuts the board into 2 pieces on x \(0.0 to 1965.3, 2934.7 to 3400.0\)"):
            whole.box()
        first = board("first", ply15).center(Pos("y", -880)).between(outline, front, Pos("z", 0), Pos("z", 28))
        last = board("last", ply15).center(Pos("y", -880)).between(outline, back, Pos("z", 0), Pos("z", 28))
    assert (first.box().lo["x"], first.box().hi["x"]) == pytest.approx((20, 1965.3), abs=0.05)
    assert (last.box().lo["x"], last.box().hi["x"]) == pytest.approx((2934.7, 3380), abs=0.05)


# -- checks ------------------------------------------------------------------------

def test_inside_box_and_inside_contour(van: Master):
    outline = van.contour("Bodenumriss")
    with module("cab", van.box("Moebel.Kueche")) as cab:
        board("left", ply15).on(cab.left)
        board("top", ply15).on(cab.top).between(Pos("y", -890), Pos("y", -300))   # 90 mm too deep
        check(inside_box, inside(outline))
    with module("over_arch", Box.from_size(width=400, depth=400, height=500, origin=(2300, -890, 40))) as m:
        board("bottom", ply15).on(m.bottom)
        check(inside(outline, gap=5))
    problems = build_layout()["problems"]
    assert any(p.startswith("cab.top reaches out of cab's box") and "by 90" in p for p in problems)
    assert any(p.startswith("over_arch.bottom is not inside Bodenumriss with 5 mm") for p in problems)
    assert not any(p.startswith("cab.left") for p in problems)


def test_inside_does_not_count_a_rounding_past_the_contour():
    """A board across a contour whose face lies a rounding past the
    contour's edge (the snapshot rounds to 0.1 micrometre) is inside it:
    `between()` takes it, and `inside()` reported the sliver as "0 mm²
    outside". Fuzzing found it."""
    band = _contour("band", [(-3.0, 0.0), (3.0, 0.0), (3.0, 50.0), (-3.0, 50.0)], True)
    with module("m", Box({"x": -10, "y": 0, "z": 0}, {"x": 10, "y": 50, "z": 50})):
        b = board("b", material("thin", t=6)).center(Pos("x", 1.192092896e-07)).between(band)
        check(inside(band))
    assert (b.box().lo["y"], b.box().hi["y"]) == (0, 50)
    assert build_layout()["problems"] == []


# -- the example ------------------------------------------------------------------

def test_the_van_example_builds_without_problems(tmp_path: Path):
    from lang.build import run_build
    layout = run_build(FIXTURE.parent / "van.py", tmp_path, scene=False)
    floor = next(m for m in layout["modules"] if m["path"] == "floor")
    battens = {p["path"]: p["box"] for p in floor["parts"] if "batten" in p["path"]}
    assert len(battens) == 9
    # the battens beside the wheel arches are shorter (batten7 straddles the rear end)
    short = sorted(path for path, b in battens.items() if b["max"][1] < 700)
    assert short == ["floor.batten5", "floor.batten6", "floor.batten7"]
    # six along, the outer two in two pieces each, lapped at all 48 crossings
    longs = [p for p in floor["parts"] if ".long" in p["path"]]
    assert len(longs) == 8
    laps = sum(1 for p in longs for op in p["ops"] if (op.get("name") or "").startswith("lap_"))
    assert laps == 48
    assert layout["problems"] == []
    assert layout.get("snapshots", [])[0]["hash"] == master(FIXTURE).hash


def test_a_helper_reads_the_master_relative_to_its_caller(tmp_path: Path):
    """A function in a library file reads the snapshot for the build files
    that call it: relative to the file it names, not its own."""
    van = master("van_snapshot.json", relative_to=FIXTURE.parent / "van.py")
    assert van.path == FIXTURE
    with pytest.raises(LangError, match="no snapshot at"):
        master("van_snapshot.json", relative_to=tmp_path / "build.py")


def test_a_snapshot_that_is_not_json_is_a_lang_error(tmp_path: Path):
    broken = tmp_path / "snapshot.json"
    broken.write_text("{ not json")
    with pytest.raises(LangError, match="snapshot.json is not a snapshot"):
        master(broken)


def test_planes_compute_like_positions(van: Master):
    level = van.plane("Bodenniveau")
    assert isinstance(level + 10, Pos) and (level - 10).value == level.value - 10
    assert ((level + level) / 2) == level.position and level - level == 0
