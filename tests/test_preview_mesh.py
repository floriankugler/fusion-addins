"""The preview's mesher and builds: version checks, failures reported
rather than hidden, and the build process's housekeeping."""
import math
from pathlib import Path
from typing import Any

import pytest
import trimesh

from lang import *
from lang.build import run_build
from lang.core import layout_types
from lang.core.layout import build_layout
from lang.emit import plan
from lang.preview.mesh import build_scene, mesh_hardware, mesh_part, write_scene
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
                     "    p = board('p', material('birch', t=15)).on(m.bottom)\n"
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
                     "    board('p', material('birch', t=15)).on(m.bottom)\n")
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
