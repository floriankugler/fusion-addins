"""The emitter's plan and the preview's mesh read every operation alike.

One board lying flat, 200 deep (x 0..200), 150 wide (y 0..150), 15 thick
(z 0..15), gets one operation per case: every kind, on a big face and a
narrow one, to a depth, through and `to()` a face, with and without a
chamfer. Each case checks the depth the plan gives Fusion and the volume
the preview's mesh removes, worked out by hand. Holes are meshed as
24-gons inscribed in their circle (`CYLINDER`), countersinks revolved with
32 sections; a chamfer along a contour removes a band that narrows from
its size at the face to nothing at its depth.
"""
import math
from collections.abc import Callable
from dataclasses import dataclass

import pytest

from lang import *
from lang.core.layout import build_layout
from lang.emit.plan import ChamferStep, HoleStep, PocketStep, Step, VGrooveStep, plan_layout
from lang.preview.mesh import mesh_part
from helpers import ply15

#: A 24-gon's area over its circumscribed circle's radius squared.
CYLINDER = 12 * math.sin(math.pi / 12)
W, H, T = 200.0, 150.0, 15.0


def cylinder(d: float, h: float) -> float:
    return CYLINDER * (d / 2) ** 2 * h


def countersink(d: float, c: float) -> float:
    """What a 90 degree countersink of size `c` removes beside a hole of
    diameter `d`: the cone's frustum less the hole's cylinder."""
    r, big = d / 2, d / 2 + c
    return math.pi * c / 3 * (big * big + big * r + r * r) - math.pi * r * r * c


def contour_chamfer(w: float, h: float, c: float) -> float:
    """A chamfer of size `c` around a w x h opening."""
    return (w + h) * c * c + 4 * c ** 3 / 3


def outline_chamfer(w: float, h: float, c: float) -> float:
    """A chamfer of size `c` along the outline of a w x h face."""
    return (w + h) * c * c - 4 * c ** 3 / 3


Op = Callable[[Board], object]


@dataclass(frozen=True)
class Case:
    name: str
    op: Op
    #: The plan's first step, and its depth (None through; for chamfers unused).
    step: type
    depth: float | None
    #: The volume the mesh removes, mm³.
    removed: float
    #: Whether the operation is chamfered (the plan has a chamfer step).
    chamfered: bool = False
    #: Absolute tolerance, mm³: polygons standing for circles differ a little.
    tolerance: float = 0.05


CASES = [
    Case("hole top 5", lambda p: p.hole(8, at=p.top.center, depth=5), HoleStep, 5, cylinder(8, 5)),
    Case("hole top through", lambda p: p.hole(8, at=p.top.center, depth=through), HoleStep, None, cylinder(8, T)),
    Case("hole top to bottom", lambda p: p.hole(8, at=p.top.center, depth=to(p.bottom, leave=3)), HoleStep, 12,
         cylinder(8, 12)),
    Case("hole bottom 5", lambda p: p.hole(8, at=p.bottom.center, depth=5), HoleStep, 5, cylinder(8, 5)),
    Case("hole front 30", lambda p: p.hole(8, at=p.front.center, depth=30), HoleStep, 30, cylinder(8, 30)),
    Case("hole front through", lambda p: p.hole(8, at=p.front.center, depth=through), HoleStep, None,
         cylinder(8, W)),
    Case("hole front to back", lambda p: p.hole(8, at=p.front.center, depth=to(p.back, leave=20)), HoleStep, 180,
         cylinder(8, 180)),
    Case("pocket top 5", lambda p: p.pocket(rect(depth=40, width=20), at=p.top.center, depth=5), PocketStep, 5,
         40 * 20 * 5),
    Case("pocket top through", lambda p: p.pocket(rect(depth=40, width=20), at=p.top.center, depth=through),
         PocketStep, None, 40 * 20 * T),
    Case("pocket right 10", lambda p: p.pocket(rect(depth=20, height=6), at=p.right.center, depth=10), PocketStep,
         10, 20 * 6 * 10),
    Case("pocket right through", lambda p: p.pocket(rect(depth=20, height=6), at=p.right.center, depth=through),
         PocketStep, None, 20 * 6 * H),
    Case("vgroove top", lambda p: p.add_vgroove(p.top, (50, 20), (150, 20), 2), VGrooveStep, 2, 2 * 2 * 100),
    Case("chamfer front.top", lambda p: p.chamfer(p.front.top, 2), ChamferStep, None, 2 * 2 / 2 * H, True),
    Case("chamfer top outline", lambda p: p.chamfer(p.top.outline, 1), ChamferStep, None,
         outline_chamfer(W, H, 1), True),
    Case("pocket top chamfered", lambda p: p.pocket(rect(depth=40, width=20), at=p.top.center, depth=5, chamfer=1),
         PocketStep, 5, 40 * 20 * 5 + contour_chamfer(40, 20, 1), True),
    Case("pocket right chamfered", lambda p: p.pocket(rect(depth=20, height=6), at=p.right.center, depth=10,
                                                     chamfer=1),
         PocketStep, 10, 20 * 6 * 10 + contour_chamfer(20, 6, 1), True),
    Case("pocket right named chamfer", lambda p: p.pocket(rect(depth=20, height=6), at=p.right.center, depth=10,
                                                         name="mortise").chamfer(p.mortise, 1),
         PocketStep, 10, 20 * 6 * 10 + contour_chamfer(20, 6, 1), True),
    Case("hole top chamfered", lambda p: p.hole(8, at=p.top.center, depth=5, chamfer=1), HoleStep, 5,
         cylinder(8, 5) + countersink(8, 1), True, 0.3),
    Case("hole front chamfered", lambda p: p.hole(8, at=p.front.center, depth=30, chamfer=1), HoleStep, 30,
         cylinder(8, 30) + countersink(8, 1), True, 0.3),
    Case("hole front named chamfer", lambda p: p.hole(8, at=p.front.center, depth=30, name="pin").chamfer(p.pin, 1),
         HoleStep, 30, cylinder(8, 30) + countersink(8, 1), True, 0.3),
]


def _build(op: Op) -> tuple[list[Step], float]:
    """The plan's steps for the board and the volume its mesh lost."""
    with module("m", Box.from_size(width=H, depth=W, height=100)) as m:
        p = board("p", ply15).on(m.bottom)
        op(p)
    layout = build_layout()
    (part,) = layout["modules"][0]["parts"]
    problems: list[str] = []
    mesh = mesh_part(part, layout["frame"], problems.append)
    assert problems == [] and mesh.is_volume
    (plan,) = plan_layout(layout).parts
    return plan.steps, W * H * T - float(mesh.volume)


@pytest.mark.parametrize("case", CASES, ids=[case.name for case in CASES])
def test_plan_and_mesh_agree(case: Case):
    steps, lost = _build(case.op)
    assert isinstance(steps[0], case.step)
    if isinstance(steps[0], (HoleStep, PocketStep, VGrooveStep)):
        assert steps[0].depth == case.depth
    assert any(isinstance(s, ChamferStep) for s in steps) == case.chamfered
    assert lost == pytest.approx(case.removed, abs=case.tolerance)


def test_a_v_groove_has_no_rim_to_chamfer():
    with module("m", Box.from_size(width=H, depth=W, height=100)) as m:
        p = board("p", ply15).on(m.bottom)
        p.add_vgroove(p.top, (50, 20), (150, 20), 2, name="mark")
        with pytest.raises(LangError, match="a V-groove has no rim to chamfer"):
            p.chamfer(p.mark, 1)
