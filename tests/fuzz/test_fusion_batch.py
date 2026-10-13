"""The Fusion batch check's half outside Fusion (`fusion_batch.py`)."""
import json
import math
from pathlib import Path

import pytest

import fusion_batch
from lang import *
from lang.core.layout import build_layout
from tests.helpers import ply15


def _board_with_a_hole() -> None:
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15, rect(depth=300, width=400).rounded(50)).on(m.bottom)
        panel.hole(d=40, at=panel.top.center, depth=through)


def test_the_polygons_part_is_the_arcs_outside_them_and_the_holes_24_sides():
    _board_with_a_hole()
    (part,) = build_layout()["modules"][0]["parts"]
    from shapely.geometry import Polygon
    corners = 400 * 300 - (4 - math.pi) * 50 ** 2 - Polygon(part["outline"][0]).area    # true arcs hold more
    hole = math.pi * 20 ** 2 - 12 * 20 ** 2 * math.sin(2 * math.pi / 24)              # than the 24-sided prism
    assert fusion_batch.tessellation(part) == pytest.approx((corners - hole) * 15, rel=1e-3)


def test_explain_tells_the_polygons_from_findings(tmp_path: Path):
    _board_with_a_hole()
    layout = build_layout()
    out = tmp_path / "one"
    fusion_batch.write(out, layout)
    preview = json.loads(Path(f"{out}.volumes.json").read_text())["m.panel"]
    polygons = fusion_batch.tessellation(layout["modules"][0]["parts"][0])
    for volume, solids, problems, verdict in ((preview + polygons, 1, [], "the polygons"),
                                              (preview + polygons + 50, 1, [], "UNEXPLAINED +50.0 mm3"),
                                              (preview + polygons, 2, [], "UNEXPLAINED"),
                                              (preview, 1, ["m.panel: the hole failed"], "the hole failed")):
        Path(f"{out}.fusion.json").write_text(json.dumps(
            {"volumes": {"m.panel": {"volume": volume, "solids": solids}}, "problems": problems, "checks": []}))
        (line,) = fusion_batch.explain(out, threshold=1e-6)
        assert verdict in line
    Path(f"{out}.fusion.json").write_text(json.dumps({"volumes": {}, "problems": [], "checks": []}))
    assert fusion_batch.explain(out) == ["m.panel: not drawn"]


def test_a_batch_builds_again_from_its_cases(tmp_path: Path):
    cases = fusion_batch.draw_cases(1, 0)
    assert len(cases) == 1 and cases == fusion_batch.draw_cases(1, 0)      # the same for the same seed
    fusion_batch.write(tmp_path / "batch", fusion_batch.build_cases(cases), cases)
    again = fusion_batch.read_cases(tmp_path / "batch.cases.txt")
    assert again == cases
    fusion_batch.write(tmp_path / "again", fusion_batch.build_cases(again))
    assert (tmp_path / "again.json").read_text() == (tmp_path / "batch.json").read_text()
    assert json.loads((tmp_path / "batch.volumes.json").read_text())["m0.panel"] > 0


def test_examples_build_as_lang_build_builds_them(tmp_path: Path):
    folder = tmp_path / "builds"
    folder.mkdir()
    (folder / "shelf.py").write_text(
        "from lang import *\n"
        "with module('shelf', Box.from_size(width=400, depth=300, height=100)) as m:\n"
        "    board('top', material('ply', t=15)).on(m.bottom)\n")
    (path,) = fusion_batch.build_examples(tmp_path / "out", folder)
    assert path == tmp_path / "out" / "shelf" / "layout"
    assert json.loads(Path(f"{path}.volumes.json").read_text()) == {"shelf.top": pytest.approx(400 * 300 * 15)}
