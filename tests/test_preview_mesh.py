"""The preview's mesher and builds: version checks, failures reported
rather than hidden, and the build process's housekeeping."""
import math
from pathlib import Path
from typing import Any

import numpy as np
import pytest
import trimesh
from shapely.geometry import Polygon

from lang import *
from lang.build import run_build
from lang.core import layout_types
from lang.core.layout import build_layout
from lang.core.scope import registry
from lang.emit import plan
from lang.preview.mesh import FINE, NORMAL, MeshCache, build_scene, mesh_hardware, mesh_part, part_key, write_scene
from helpers import ply15


def _panel() -> None:
    with module("m", Box.from_size(width=300, depth=200, height=100)) as m:
        p = board("p", ply15).on(m.bottom)
        p.hole(8, at=p.top.center, depth=5)
        m.place_hardware("lock", [{"name": "body", "boxes": [
            {"min": [0, 0, 20], "max": [10, 10, 30]}, {"min": [5, 5, 25], "max": [15, 15, 35]}]}])


def test_the_plan_and_the_writer_agree_on_the_layout_version():
    assert plan.LAYOUT_VERSION == layout_types.LAYOUT_VERSION == build_layout()["version"]


def test_a_layout_of_another_version_is_refused():
    _panel()
    old = build_layout()
    old["version"] = 2
    with pytest.raises(ValueError, match="layout version 2 is not supported"):
        plan.plan_layout(old)
    with pytest.raises(ValueError, match="layout version 2 is not supported"):
        build_scene(old)


def _failing(*args: Any, **kwargs: Any) -> Any:
    raise RuntimeError("manifold gave up")


def test_a_failed_boolean_is_reported_and_the_board_left_uncut(monkeypatch: pytest.MonkeyPatch):
    _panel()
    layout = build_layout()
    part = layout["modules"][0]["parts"][0]
    monkeypatch.setattr(trimesh.boolean, "difference", _failing)
    problems: list[str] = []
    mesh = mesh_part(part, layout["frame"], problems.append)
    assert problems == ["m.p: the preview could not cut its operations (manifold gave up); it shows the board uncut."]
    assert mesh.volume == pytest.approx(300 * 200 * 15)


def test_a_failed_hardware_union_shows_the_boxes_apart(monkeypatch: pytest.MonkeyPatch):
    _panel()
    item = build_layout()["modules"][0]["hardware"][0]
    monkeypatch.setattr(trimesh.boolean, "union", _failing)
    problems: list[str] = []
    ((path, mesh),) = mesh_hardware(item, problems.append)
    assert path == "m.lock.body" and len(mesh.faces) == 24
    assert problems == ["m.lock.body: the preview could not unite its boxes (manifold gave up); it shows them apart."]


def test_write_scene_returns_the_problems_and_the_build_prints_them(monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
                                                                     capsys: pytest.CaptureFixture[str]):
    _panel()
    monkeypatch.setattr(trimesh.boolean, "difference", _failing)
    assert write_scene(build_layout(), tmp_path / "scene.glb") == [
        "m.p: the preview could not cut its operations (manifold gave up); it shows the board uncut."]
    build = tmp_path / "build.py"
    build.write_text("from lang import *\n"
                     "with module('m', Box.from_size(width=300, depth=200, height=100)) as m:\n"
                     "    p = board('p', sheet_material('birch', t=15)).on(m.bottom)\n"
                     "    p.hole(8, at=p.top.center, depth=5)\n")
    run_build(build, tmp_path / "out")
    assert "preview: m.p: the preview could not cut its operations" in capsys.readouterr().err


def test_a_build_imports_its_folder_s_modules_afresh(tmp_path: Path):
    """A helper module next to the build file is imported again by the
    next build in the same process, so an edit to it shows."""
    (tmp_path / "sizes.py").write_text("WIDTH = 300\n")
    build = tmp_path / "build.py"
    build.write_text("from lang import *\nfrom sizes import WIDTH\n"
                     "with module('m', Box.from_size(width=WIDTH, depth=200, height=100)) as m:\n"
                     "    board('p', sheet_material('birch', t=15)).on(m.bottom)\n")
    first = run_build(build, tmp_path / "out", scene=False)
    (tmp_path / "sizes.py").write_text("WIDTH = 400\n")
    second = run_build(build, tmp_path / "out", scene=False)
    widths = [layout["modules"][0]["box"]["max"][1] for layout in (first, second)]  # type: ignore[index]
    assert widths == [300, 400]


def test_an_edge_shorter_than_a_micrometre_does_not_break_the_mesh():
    """Found by fuzzing: a notch centred a hair (1e-45) off the board's edge
    left an edge that short in the outline; the triangulation made faces
    without area of it, and the boolean refused the board as no volume.
    Shapes are cleaned of such edges now (`geometry.clean`); the mesher
    still merges points that near."""
    from shapely.geometry import Point
    from lang.core.shapes import Shape
    with module("m", Box.from_size(width=100, depth=243, height=116)) as m:
        panel = board("panel", ply15).on(m.left)
        panel.add_cut(Shape(Point(217.0, 1.401298464324817e-45).buffer(40.25, quad_segs=32)))
        panel.hole(10, at=panel.outer.center, depth=5)
    layout = build_layout()
    (part,) = layout["modules"][0]["parts"]
    assert min(math.dist(a, b) for ring in part["outline"] for a, b in zip(ring, ring[1:] + ring[:1])) > 1e-6
    problems: list[str] = []
    mesh = mesh_part(part, layout["frame"], problems.append)
    assert problems == [] and mesh.is_watertight


def test_a_shape_that_touches_itself_at_a_point_meshes():
    """Found by fuzzing: a cutout's opening pinched to a point, 1e-14
    across; the triangulation left an open edge there, and the preview
    showed the board uncut. (The language refuses such openings now; the
    mesher copes with any shape that comes so near itself.)"""
    from shapely.geometry import Polygon
    from trimesh.creation import extrude_polygon
    from lang.preview.mesh import _extruded_polygon  # pyright: ignore[reportPrivateUsage]
    # a square with a triangle open to the outside through a gap of 2e-14
    pinched = Polygon([(0, 0), (4, 0), (4, 4), (2 + 1e-14, 4), (3, 2), (1, 2), (2 - 1e-14, 4), (0, 4)])
    assert pinched.is_valid and not extrude_polygon(pinched, 3).is_volume
    mesh = _extruded_polygon(pinched, 3)
    assert mesh.is_volume and mesh.volume == pytest.approx((16 - 2) * 3, rel=1e-5)


def _sides(mesh: Any, center: tuple[float, float], r: float) -> int:
    """The sides of a round pocket's wall in a mesh: its faces standing
    upright within `r` of the centre, two triangles a side."""
    upright = np.abs(mesh.face_normals[:, 2]) < 1e-9
    near = np.hypot(mesh.triangles_center[:, 0] - center[0], mesh.triangles_center[:, 1] - center[1]) < r + 1e-6
    return int((upright & near).sum()) // 2


def test_a_circle_pocket_at_the_normal_level_has_the_sides_its_tolerance_needs():
    """At the normal level the mesher draws a circle again with chords at
    most 0.05 mm inside it: a pocket of radius 3, 360 points in the layout,
    gets 18 sides and takes that polygon's volume; at the fine level it
    keeps its 360."""
    with module("m", Box.from_size(width=300, depth=200, height=100)) as m:
        p = board("p", ply15).on(m.bottom)
        p.pocket(circle(6), at=p.top.center, depth=5)
    layout = build_layout()
    (part,) = layout["modules"][0]["parts"]
    (pocket,) = part["ops"]
    assert pocket["kind"] == "pocket"
    ring = pocket["shape"][0]
    assert len(ring) == 360
    center = (sum(q[0] for q in ring) / 360, sum(q[1] for q in ring) / 360)
    n = math.ceil(2 * math.pi / (2 * math.acos(1 - 0.05 / 3)))
    assert n == 18
    fine, normal = mesh_part(part, layout["frame"], level=FINE), mesh_part(part, layout["frame"], level=NORMAL)
    assert (_sides(fine, center, 3), _sides(normal, center, 3)) == (360, 18)
    assert fine.volume == pytest.approx(300 * 200 * 15 - Polygon(ring).area * 5, rel=1e-10)
    gon = n / 2 * 3 ** 2 * math.sin(2 * math.pi / n)
    assert normal.volume == pytest.approx(300 * 200 * 15 - gon * 5, rel=1e-10)
    assert mesh_part(part, layout["frame"]).volume == normal.volume       # the default


def test_an_arc_the_layout_draws_coarser_than_the_level_keeps_its_points():
    """The normal level never draws an arc with more segments than the
    layout has for it: a corner of radius 100 drawn with eight segments a
    quarter (11.25 degrees, finer would take 3.6) stays as it is, and a
    shape with nothing coarser to draw stays the layout's polygon."""
    from shapely.geometry import box as shapely_box
    from lang.preview.mesh import _redrawn  # pyright: ignore[reportPrivateUsage]
    rounded = shapely_box(0, 0, 400, 300).buffer(-100).buffer(100, quad_segs=8)
    ring = [[x, y] for x, y in list(rounded.exterior.coords)[:-1]]
    assert _redrawn(ring, 0.05) is ring
    with module("m", Box.from_size(width=300, depth=400, height=100)) as m:
        board("p", ply15, Shape(rounded)).on(m.bottom)
    layout = build_layout()
    (part,) = layout["modules"][0]["parts"]
    assert mesh_part(part, layout["frame"], level=NORMAL).volume == mesh_part(part, layout["frame"], level=FINE).volume


def test_the_build_meshes_at_the_level_asked_and_says_which(tmp_path: Path):
    build = tmp_path / "build.py"
    build.write_text("from lang import *\n"
                     "with module('m', Box.from_size(width=300, depth=200, height=100)) as m:\n"
                     "    p = board('p', sheet_material('birch', t=15)).on(m.bottom)\n"
                     "    p.pocket(circle(6), at=p.top.center, depth=5)\n")
    from lang.build import main
    assert main([str(build), "--out", str(tmp_path / "fine"), "--level", "fine"]) == 0
    run_build(build, tmp_path / "normal")
    run_build(build, tmp_path / "layout", scene=False)
    assert (tmp_path / "fine" / "level.txt").read_text() == "fine"
    assert (tmp_path / "normal" / "level.txt").read_text() == "normal"
    assert not (tmp_path / "layout" / "level.txt").exists()
    scenes: list[Any] = [trimesh.load(tmp_path / name / "scene.glb") for name in ("fine", "normal")]
    faces = [sum(len(g.faces) for g in scene.geometry.values()) for scene in scenes]
    assert faces[0] > 10 * faces[1]
    with pytest.raises(SystemExit):
        main([str(build), "--level", "rough"])


def _workshop(depth: float = 5) -> None:
    """Two modules with the operations a part's mesh is made of: holes,
    pockets, a cut, chamfers, V-grooves' and narrow faces' work."""
    with module("m", Box.from_size(width=600, depth=400, height=300)) as m:
        bottom = board("bottom", ply15).on(m.bottom)
        bottom.pocket(circle(20), at=bottom.top.center, depth=depth, chamfer=1)
        bottom.hole(8, at=bottom.top.front(50), depth=10)
        bottom.cut(rect(width=100, depth=60), at=bottom.top.back)
        side = board("left", ply15).on(m.left)
        side.hole(5, at=side.front.center, depth=20)
        side.chamfer(side.outer.outline, 1)
        side.chamfer(side.front.top, 2)
        board("right", ply15).on(m.right)
    with module("n", Box.from_size(width=300, depth=300, height=200)) as n:
        board("top", ply15).on(n.top).pocket(rect(width=50, depth=50), at=n["top"].bottom.center, depth=3)


def test_a_scene_from_the_mesh_cache_is_the_one_meshed_anew(tmp_path: Path):
    """The second build takes every part's mesh from the cache and writes
    the same file to the bit; after one part changed it meshes that one
    alone, and the cache holds the last build's meshes only."""
    _workshop()
    layout = build_layout()
    count = sum(len(m["parts"]) for m in layout["modules"])
    first = MeshCache(tmp_path / "cache")
    build_scene(layout, cache=first).export(str(tmp_path / "first.glb"))
    assert first.meshed == count and len(list((tmp_path / "cache").glob("*.npz"))) == count
    second = MeshCache(tmp_path / "cache")
    build_scene(layout, cache=second).export(str(tmp_path / "second.glb"))
    assert second.meshed == 0
    write_scene(layout, tmp_path / "anew.glb")
    assert (tmp_path / "first.glb").read_bytes() == (tmp_path / "second.glb").read_bytes() \
        == (tmp_path / "anew.glb").read_bytes()
    for level in (FINE, NORMAL):        # a level of its own
        assert write_scene(layout, tmp_path / f"{level.name}.glb", level, tmp_path / "cache") == []
        write_scene(layout, tmp_path / f"{level.name}-anew.glb", level)
        assert (tmp_path / f"{level.name}.glb").read_bytes() == (tmp_path / f"{level.name}-anew.glb").read_bytes()
    registry.reset()
    _workshop(depth=7)                  # the bottom's pocket deeper
    changed = build_layout()
    third = MeshCache(tmp_path / "cache")
    build_scene(changed, cache=third).export(str(tmp_path / "third.glb"))
    third.prune()
    assert third.meshed == 1 and len(list((tmp_path / "cache").glob("*.npz"))) == count
    write_scene(changed, tmp_path / "changed.glb")
    assert (tmp_path / "third.glb").read_bytes() == (tmp_path / "changed.glb").read_bytes()


def test_a_part_s_key_is_what_its_mesh_comes_from():
    _workshop()
    layout = build_layout()
    part = layout["modules"][0]["parts"][0]
    frame = layout["frame"]
    key = part_key(part, frame, NORMAL)
    renamed = part.copy()
    renamed["path"], renamed["material"], renamed["settings"] = "x.y", "oak", {}
    assert part_key(renamed, frame, NORMAL) == key
    moved, turned = part.copy(), part.copy()
    moved["box"] = {"min": [0.0, 0.0, 1.0], "max": part["box"]["max"]}
    turned["show"] = "top" if part["show"] != "top" else "bottom"
    assert len({key, part_key(moved, frame, NORMAL), part_key(turned, frame, NORMAL), part_key(part, frame, FINE),
                part_key(part, {**frame, "top": "-z", "bottom": "+z"}, NORMAL)}) == 5


def test_a_part_whose_boolean_failed_is_not_kept_and_says_so_each_time(monkeypatch: pytest.MonkeyPatch,
                                                                        tmp_path: Path):
    _panel()
    layout = build_layout()
    monkeypatch.setattr(trimesh.boolean, "difference", _failing)
    for _ in range(2):
        assert write_scene(layout, tmp_path / "scene.glb", cache=tmp_path / "cache") == [
            "m.p: the preview could not cut its operations (manifold gave up); it shows the board uncut."]
        assert list((tmp_path / "cache").glob("*.npz")) == []


def test_the_build_keeps_its_meshes_beside_the_scene(tmp_path: Path):
    build = tmp_path / "build.py"
    build.write_text("from lang import *\n"
                     "with module('m', Box.from_size(width=300, depth=200, height=100)) as m:\n"
                     "    p = board('p', sheet_material('birch', t=15)).on(m.bottom)\n"
                     "    p.pocket(circle(6), at=p.top.center, depth=5)\n")
    from lang.build import main
    assert main([str(build), "--out", str(tmp_path / "out")]) == 0
    assert len(list((tmp_path / "out" / ".mesh").glob("*.npz"))) == 1
    assert main([str(build), "--out", str(tmp_path / "other"), "--mesh-cache", str(tmp_path / "meshes")]) == 0
    assert len(list((tmp_path / "meshes").glob("*.npz"))) == 1 and not (tmp_path / "other" / ".mesh").exists()
    assert main([str(build), "--out", str(tmp_path / "none"), "--no-mesh-cache"]) == 0
    assert not (tmp_path / "none" / ".mesh").exists()
    assert (tmp_path / "out" / "scene.glb").read_bytes() == (tmp_path / "none" / "scene.glb").read_bytes()
