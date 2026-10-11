from pathlib import Path

import pytest

from lang import *
from lang.build import run_build
from lang.core.layout import build_layout
from lang.core.scope import registry
from lang.emit.plan import (ChamferStep, CircleContour, EdgeContour, FaceRef, HoleStep, OutlineContour,
                            PocketStep, ShapeContour, plan_layout)


@pytest.fixture(autouse=True)
def fresh_registry():
    registry.reset()
    yield
    registry.reset()


ply15 = material("birch", t=15)
CAB = Box.from_size(width=600, depth=500, height=720)


def _plan_of(part: Board):
    plan = plan_layout(build_layout())
    return next(p for p in plan.parts if p.path == part.path)


def test_body_is_outline_on_lower_face_extruded_along_thickness():
    with module("cab", CAB) as cab:
        left = board("left", ply15).on(cab.left)
    p = _plan_of(left)
    assert p.component == ("cab",)
    assert p.body.thickness == 15
    assert p.body.direction == (0.0, 1.0, 0.0)
    ring = p.body.rings[0]
    assert all(pt[1] == 0.0 for pt in ring)
    assert {(pt[0], pt[2]) for pt in ring} == {(0.0, 0.0), (500.0, 0.0), (500.0, 720.0), (0.0, 720.0)}


def test_holes_batch_by_face_diameter_and_depth():
    with module("cab", CAB) as cab:
        left = board("left", ply15).on(cab.left)
        left.hole(d=5, depth=10, at=left.inner.front(37).bottom(Pos("z", 120)))
        left.hole(d=5, depth=10, at=left.inner.front(37).bottom(Pos("z", 152)))
        left.hole(d=5, depth=12, at=left.inner.front(37).bottom(Pos("z", 184)))
    steps = _plan_of(left).steps
    assert len(steps) == 2
    first, second = steps
    assert isinstance(first, HoleStep) and isinstance(second, HoleStep)
    assert first.face == FaceRef("y", 1, 15.0)
    assert first.face.into == (0.0, -1.0, 0.0)
    assert first.points == [(37.0, 15.0, 120.0), (37.0, 15.0, 152.0)]
    assert first.depth == 10 and second.depth == 12


def test_through_depth_is_none_and_pocket_chamfer_follows_pocket():
    with module("cab", CAB) as cab:
        bottom = board("bottom", ply15).on(cab.bottom)
        bottom.pocket(rect(depth=100, width=20), at=bottom.top.center, depth=through, chamfer=1)
        bottom.hole(d=6, at=bottom.top.center, depth=to(bottom.bottom))
    steps = _plan_of(bottom).steps
    pocket, chamfer, hole = steps
    assert isinstance(pocket, PocketStep) and pocket.depth is None
    assert pocket.face == FaceRef("z", 1, 15.0)
    assert all(pt[2] == 15.0 for pt in pocket.shapes[0][0])
    assert isinstance(chamfer, ChamferStep) and isinstance(chamfer.contour, ShapeContour)
    assert chamfer.contour.rings == pocket.shapes[0]
    assert isinstance(hole, HoleStep) and hole.depth is None


def test_cut_chamfer_and_named_contours():
    with module("cab", CAB) as cab:
        left = board("left", ply15).on(cab.left)
        (left.cut(rect(depth=60, height=100), at=left.outer.bottom.front, name="toekick", chamfer=1)
             .chamfer(left.outer.outline, 1)
             .chamfer(left.front.inner, 0.5)
             .hole(d=5, depth=10, at=left.inner.center, name="pin")
             .chamfer(left.pin, 0.5))
    steps = _plan_of(left).steps
    cut_chamfer, outline, edge, _hole, pin = steps
    show = FaceRef("y", -1, 0.0)
    assert isinstance(cut_chamfer, ChamferStep) and isinstance(cut_chamfer.contour, ShapeContour)
    assert cut_chamfer.contour.face == show
    assert all(pt[1] == 0.0 for pt in cut_chamfer.contour.rings[0])
    assert isinstance(outline, ChamferStep) and outline.contour == OutlineContour(show)
    assert isinstance(edge, ChamferStep)
    assert edge.contour == EdgeContour(FaceRef("x", -1, 0.0), FaceRef("y", 1, 15.0))
    assert isinstance(pin, ChamferStep)
    assert pin.contour == CircleContour(FaceRef("y", 1, 15.0), (250.0, 15.0, 360.0), 2.5)


def test_narrow_face_operations_map_to_the_face_plane():
    with module("cab", CAB) as cab:
        left = board("left", ply15).on(cab.left)
        left.hole(d=8, depth=30, at=left.front.bottom(50))
        left.pocket(rect(depth=20, width=6), at=left.top.center, depth=10)
    hole, pocket = _plan_of(left).steps
    assert isinstance(hole, HoleStep)
    assert hole.face == FaceRef("x", -1, 0.0)
    assert hole.points == [(0.0, 7.5, 50.0)]
    assert hole.depth == 30  # deeper than the thickness, but not through the 500 mm board
    assert isinstance(pocket, PocketStep)
    assert pocket.face == FaceRef("z", 1, 720.0)
    xs = {pt[0] for pt in pocket.shapes[0][0]}
    ys = {pt[1] for pt in pocket.shapes[0][0]}
    assert xs == {240.0, 260.0} and ys == {4.5, 10.5}
    assert all(pt[2] == 720.0 for pt in pocket.shapes[0][0])


def test_unknown_chamfer_target_is_a_problem_not_a_crash():
    # The language refuses such a chamfer; a hand-edited layout can still carry one.
    with module("cab", CAB) as cab:
        board("left", ply15).on(cab.left)
    layout = build_layout()
    layout["modules"][0]["parts"][0]["ops"].append(
        {"kind": "chamfer", "what": "nothing", "size": 1.0, "face": "left"})
    plan = plan_layout(layout)
    assert plan.problems and "nothing" in plan.problems[0]
    assert plan.parts[0].steps == []


def test_example_plans_completely(tmp_path: Path):
    example = Path(__file__).resolve().parent.parent / "examples" / "drawer_cabinet.py"
    layout = run_build(example, tmp_path, scene=False)
    plan = plan_layout(layout)
    assert len(plan.parts) == 23
    assert plan.problems == []
    sides = [p for p in plan.parts if p.path in ("drawercab.left", "drawercab.right")]
    for side in sides:
        pins, predrill = side.steps
        assert isinstance(pins, HoleStep) and isinstance(predrill, HoleStep)
        assert len(pins.points) == 13            # the column starts above the raised bottom
        assert len(predrill.points) == 12 and predrill.d == 2.0   # 3 drawers x 4 slide holes
    assert [p.component for p in plan.parts if p.path.endswith("floor")] == [
        ("drawercab", "drawer1"), ("drawercab", "drawer2"), ("drawercab", "drawer3")]
    # the runner pairs: one model per drawer, axes as world vectors, the right runner offset
    assert [h.path for h in plan.hardware] == [f"drawercab.drawer{i}.runners" for i in (1, 2, 3)]
    runners = plan.hardware[0]
    assert runners.component == ("drawercab", "drawer1") and runners.model.endswith(".stp")
    assert runners.axes == ((-1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 1.0))
    assert runners.origin == (585.0, 481.0, 117.1)
    assert [b.offset for b in runners.bodies] == [(0.0, 0.0, 0.0), (170.0, 0.0, 0.0)]
    # facts for Multi Arrange: the sides are machined from their inner faces,
    # where the shelf-pin and pre-drill holes are, which face each other
    left = next(p for p in plan.parts if p.path == "drawercab.left")
    right = next(p for p in plan.parts if p.path == "drawercab.right")
    assert left.facts is not None and right.facts is not None
    assert left.facts.material == "birch 15" and left.facts.thickness == 15 and left.facts.grained
    assert left.facts.grain is None                       # the example sets no grain
    assert left.facts.up == (-1.0, 0.0, 0.0)              # left side at x 585..600, inner face toward -x
    assert right.facts.up == (1.0, 0.0, 0.0)
    face = next(p for p in plan.parts if p.path == "drawercab.drawer1.face")
    assert face.facts is not None and face.facts.up == (0.0, 1.0, 0.0)   # nothing on it: its show face
