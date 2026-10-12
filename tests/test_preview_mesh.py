"""The preview's mesher and builds: version checks, failures reported
rather than hidden, and the build process's housekeeping."""
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
