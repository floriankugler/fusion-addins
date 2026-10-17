"""Chamfers in the preview's meshes (`lang.preview.mesh`): along an outline,
an edge, a cut, a pocket and a named hole."""
import math

import pytest

from lang import *
from lang.core.layout import build_layout
from lang.core.scope import registry
from lang.preview.mesh import FINE, mesh_part
from helpers import ply15


def _volume(part: Board) -> float:
    layout = build_layout()
    found = next(p for m in layout["modules"] for p in m["parts"] if p["path"] == part.path)
    return float(mesh_part(found, layout["frame"], level=FINE).volume)


def _panel() -> tuple[Scope, Board]:
    """A 400 x 300 panel, 15 thick, lying on the module's bottom."""
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom).show(m.top)
    return m, panel


def test_an_outline_chamfer_bevels_the_whole_contour():
    m, panel = _panel()
    plain = 400 * 300 * 15
    with m:
        panel.chamfer(panel.top.outline, 2)
    # at depth d the face is inset by 2 - d: perimeter * s - 4 s^2 removed
    c, perimeter = 2.0, 2 * (400 + 300)
    assert _volume(panel) == pytest.approx(plain - (perimeter * c * c / 2 - 4 * c ** 3 / 3), abs=0.05)


def test_an_edge_chamfer_bevels_one_edge():
    m, panel = _panel()
    with m:
        panel.chamfer(panel.front.top, 3)
    assert _volume(panel) == pytest.approx(400 * 300 * 15 - 0.5 * 9 * 400, abs=0.05)


def test_a_cut_chamfer_widens_the_opening_at_its_face():
    m, panel = _panel()
    with m:
        panel.cut(circle(40), at=panel.top.center, name="port", chamfer=1)
    r, c = 20.0, 1.0
    opening = math.pi * r * r * 15
    chamfer = math.pi * (r * c * c + c ** 3 / 3)
    assert _volume(panel) == pytest.approx(400 * 300 * 15 - opening - chamfer, rel=1e-5)


def test_pocket_and_named_hole_chamfers_take_material():
    m, panel = _panel()
    with m:
        panel.pocket(rect(width=100, depth=50), at=panel.top.center, depth=5, name="tray")
        panel.hole(d=10, depth=through, at=panel.top.front(40), name="bolt")
    without = _volume(panel)
    registry.reset()
    m, panel = _panel()
    with m:
        panel.pocket(rect(width=100, depth=50), at=panel.top.center, depth=5, name="tray", chamfer=1)
        panel.hole(d=10, depth=through, at=panel.top.front(40), name="bolt")
        panel.chamfer(panel.bolt, 1)
    # a rectangle's rim: 0.5 per millimetre, and its mitred corners: the
    # opening grows by s = 1 - depth, by 4 s^2 at the corners
    tray = 0.5 * 300 + 4 / 3
    bolt = math.pi * (5 * 1 + 1 / 3)
    assert without - _volume(panel) == pytest.approx(tray + bolt, rel=2e-3)


def test_a_chamfer_whose_contour_folds_when_moved_still_takes_its_material():
    """Found compiling fuzz boards in Fusion: the preview built a rim
    chamfer by moving each vertex of the contour along its mitre; where
    that folded the contour over itself (here a finger of material 1 wide
    reaching into the opening), the chamfer was left out unsaid, and the
    preview showed up to 0.3 % more material than Fusion."""
    from shapely.geometry import box
    from lang.core.shapes import Shape
    opening = box(150, 100, 250, 160).difference(box(199.5, 100, 200.5, 130))
    m, panel = _panel()
    with m:
        panel.add_cut(Shape(opening), name="window")
        panel.chamfer(panel.window, 2)
    # the chamfer takes, at each depth z from the face, the opening grown by 2 - z
    c, slices = 2.0, 400
    chamfer = sum((opening.buffer(c - (k + 0.5) * c / slices, join_style="mitre", mitre_limit=10.0).area - opening.area)
                  * c / slices for k in range(slices))
    plain = 400 * 300 * 15 - opening.area * 15
    assert plain - _volume(panel) == pytest.approx(chamfer, rel=0.02)
