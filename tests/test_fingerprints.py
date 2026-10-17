"""A part's fingerprint (`lang.nesting.fingerprint`): the same for the part
moved, turned in its plane or set facing another way, another when it is
machined otherwise (a hole added, another size, material, grain or
machining face); names and the order of operations do not count."""
from __future__ import annotations

import json
from collections.abc import Callable
from typing import Literal

import pytest

from lang import Board, Box, board, circle, module, rect, sheet_material, through
from lang.build import layout_of
from lang.core.layout import build_layout
from lang.core.scope import registry
from lang.nesting.fingerprint import LENGTH, fingerprint, fingerprints

from helpers import EXAMPLES, ply12, ply15

W, D, H = 600.0, 400.0, 300.0


def side(front: str = "front", origin: tuple[float, float, float] = (0.0, 0.0, 0.0),
         change: Callable[[Board], object] | None = None, on: str = "left") -> str:
    """The fingerprint of a cabinet's side with a notch, holes from both big
    faces and a narrow one, a pocket and a chamfer, the cabinet opening
    toward `front` at `origin`; `change` alters the side last."""
    registry.reset()
    width, depth = (W, D) if front in ("front", "back") else (D, W)
    box = Box.from_size(width=width, depth=depth, height=H, origin=origin)
    with module("cab", box, front=getattr(box, front)) as cab:
        b = board("side", ply15).on(getattr(cab, on)).grain("height")
        b.cut(rect(depth=60, height=40), at=b.inner.front.bottom)
        b.hole(8, at=b.inner.center, depth=10, name="pin")
        b.pocket(circle(20), at=b.outer.back.top, depth=4)
        b.hole(5, at=b.top.center, depth=20)
        b.chamfer(b.outer.top, 1)
        if change is not None:
            change(b)
    return fingerprints(build_layout())["cab.side"]


@pytest.mark.parametrize("front", ["front", "back", "left", "right"])
def test_a_part_keeps_its_fingerprint_moved_and_facing_another_way(front: str):
    first = side()
    assert len(first) == LENGTH and int(first, 16) >= 0
    assert side(front) == first
    assert side(front, (1234.5678, -77.7, 10.1)) == first
    assert side(front, (1e-7, 3e-9, 0.0)) == first


CHANGES: list[Callable[[Board], object]] = [
    lambda b: b.hole(5, at=b.inner.front(50).top(50), depth=3),                 # a hole added
    lambda b: b.hole(5, at=b.inner.front(50).top(50), depth=through),
    lambda b: b.pocket(rect(depth=30, height=30), at=b.inner.back.bottom, depth=2),
    lambda b: b.chamfer(b.outer.front, 1),
    lambda b: b.machine(b.inner),                                       # machined from its other face
]


@pytest.mark.parametrize("change", CHANGES)
def test_a_part_machined_otherwise_changes_its_fingerprint(change: Callable[[Board], object]):
    assert side(change=change) != side()


def test_a_hole_s_size_depth_or_place_changes_the_fingerprint():
    base = side(change=lambda b: b.hole(5, at=b.inner.front(50).top(50), depth=3))
    assert side(change=lambda b: b.hole(6, at=b.inner.front(50).top(50), depth=3)) != base
    assert side(change=lambda b: b.hole(5, at=b.inner.front(50).top(50), depth=4)) != base
    assert side(change=lambda b: b.hole(5, at=b.inner.front(51).top(50), depth=3)) != base
    assert side(change=lambda b: b.hole(5, at=b.inner.front(50).top(50), depth=3.0004)) == base


@pytest.mark.parametrize("x", [0.0, 3430.492742794835, 501.369153606508, 1234.5678])
def test_a_length_halfway_between_two_micrometres_keeps_its_fingerprint_moved(x: float):
    """A board 410.4875 long: moved, its length came out 410.48749999999995
    or 410.4875000000002, which rounded to micrometres made two parts
    (fuzzing found it, in another world frame). The grid is binary now."""
    def build(origin: float) -> str:
        registry.reset()
        with module("m", Box.from_size(width=359.201, depth=410.4875, height=H, origin=(origin, 0.0, 0.0))) as m:
            board("bottom", ply15).on(m.bottom)
        return fingerprints(build_layout())["m.bottom"]
    assert build(x) == build(0.0)


def test_another_material_thickness_or_grain_is_another_part():
    def build(material: object, grain: Literal["width", "depth"] | None) -> str:
        registry.reset()
        with module("m", Box.from_size(width=W, depth=D, height=H)) as m:
            b = board("bottom", material).on(m.bottom)  # pyright: ignore[reportArgumentType]
            if grain is not None:
                b.grain(grain)
        return fingerprints(build_layout())["m.bottom"]
    base = build(ply15, "depth")
    assert build(ply15, "width") != base and build(ply15, None) != base
    assert build(ply12, "depth") != base
    assert build(sheet_material("oak", t=15), "depth") != base
    free = sheet_material("mdf", t=15, grain=False)
    assert build(free, None) != base and build(free, None) == build(free, None)


def test_a_grain_turned_with_the_part_keeps_it():
    """A rectangle with its grain along its length and a hole near a
    corner, built lying across and along the depth, the hole at the corner
    a quarter turn takes it to: the same part turned. With the grain left
    as it was, another."""
    def build(across: bool, grain: Literal["width", "depth"]) -> str:
        registry.reset()
        width, depth = (W, D) if across else (D, W)
        with module("m", Box.from_size(width=width, depth=depth, height=H)) as m:
            b = board("bottom", ply15).on(m.bottom).grain(grain)
            b.hole(8, at=b.inner.left(40).front(30) if across else b.inner.back(40).left(30), depth=5)
        return fingerprints(build_layout())["m.bottom"]
    assert build(True, "width") == build(False, "depth")
    assert build(True, "width") != build(False, "width")


def test_names_and_the_order_of_operations_do_not_count():
    def build(order: int, names: tuple[str, str]) -> str:
        registry.reset()
        with module("m", Box.from_size(width=W, depth=D, height=H)) as m:
            b = board("bottom", ply15).on(m.bottom)
            holes = [lambda: b.hole(8, at=b.inner.center, depth=5, name=names[0]),
                     lambda: b.pocket(rect(width=40, depth=20), at=b.inner.left.front, depth=3, name=names[1])]
            for make in holes[::order]:
                make()
            b.chamfer(getattr(b, names[0]), 0.5)
        return fingerprints(build_layout())["m.bottom"]
    assert build(1, ("a", "b")) == build(-1, ("a", "b")) == build(1, ("pin", "recess"))


def test_a_chamfer_along_an_operation_takes_its_geometry():
    def build(d: float) -> str:
        registry.reset()
        with module("m", Box.from_size(width=W, depth=D, height=H)) as m:
            b = board("bottom", ply15).on(m.bottom)
            b.hole(d, at=b.inner.center, depth=5, name="pin")
            b.hole(8, at=b.inner.left(50).front(50), depth=5, name="other")
            b.chamfer(getattr(b, "pin"), 0.5)
        return fingerprints(build_layout())["m.bottom"]
    assert build(8) != build(9)


def test_a_mirror_image_is_another_part():
    """The side on the cabinet's left and on its right, notched at the same
    corner of their inner faces: mirror images, each the other's mirrored."""
    assert side(on="left") != side(on="right")
    registry.reset()
    side(on="right")
    layout = build_layout()
    part = layout["modules"][0]["parts"][0]
    assert fingerprint(part, layout["frame"], mirror=True) == side(on="left")


def test_equal_parts_share_a_fingerprint_and_the_example_s_drawers_two_and_three_are_alike():
    layout = layout_of(EXAMPLES / "drawer_cabinet.py")
    prints = fingerprints(layout)
    for name in ("face", "left", "right", "front", "back", "floor"):
        assert prints[f"drawercab.drawer2.{name}"] == prints[f"drawercab.drawer3.{name}"]
    assert prints["drawercab.drawer1.front"] != prints["drawercab.drawer2.front"]          # taller
    assert prints["drawercab.drawer1.floor"] == prints["drawercab.drawer2.floor"]
    # Read from the layout file as the nest reads it: the same.
    again = json.loads(json.dumps(layout))
    part = next(p for m in again["modules"] for p in m["parts"] if p["path"] == "drawercab.left")
    assert fingerprint(part, again["frame"]) == prints["drawercab.left"]


def test_slats_have_no_fingerprint():
    from lang import slat, slat_material
    with module("m", Box.from_size(width=W, depth=D, height=H)) as m:
        board("bottom", ply15).on(m.bottom)
        slat("rail", slat_material("oak"), section=(20, 40)).on(m.top).edge_on(m.front).between(m.left, m.right)
    assert list(fingerprints(build_layout())) == ["m.bottom"]

