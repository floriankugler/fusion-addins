"""The standard library (`lang.std`, `design/std.md`): written on the
public API only, and each block the same as the lines it replaces."""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

import pytest

from lang import (Board, Box, LangError, board, box_joint, cabineo, domino, drawer_slide, groove, module,
                  rect, scope, sheet_material)
from lang.core.layout import build_layout
from lang.std import Carcass, OpenCarcass, carcass, drawer_box

ply9 = sheet_material("birch", t=9)
ply12 = sheet_material("birch", t=12)
ply15 = sheet_material("birch", t=15)

STD = Path(__file__).resolve().parent.parent / "lang" / "std"


# -- the rule -----------------------------------------------------------------------------------

def test_every_std_module_imports_the_public_api_only():
    """`lang.std` is written as a build file is: `from lang import ...`
    and the standard library, nothing from `lang.core`, `lang.joints` or
    `lang.hardware` [decided by Florian, 2026-10-15, syntax.md item 2]."""
    allowed_roots = {"lang", "lang.std", "typing", "collections", "collections.abc", "__future__"}
    for path in sorted(STD.glob("*.py")):
        tree = ast.parse(path.read_text(), str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ""] if node.level == 0 else ["lang.std"]
            else:
                continue
            for m in modules:
                assert m in allowed_roots or m in sys.stdlib_module_names, f"{path.name} imports {m}"


# -- carcass ------------------------------------------------------------------------------------

def _module_layout(name: str) -> str:
    """One module's layout as text, its name replaced and its lines left
    out (`where`: a board the library makes has the library call's, one
    written by hand its own), so two modules written differently can be
    compared."""
    layout = build_layout()
    mod = next(m for m in layout["modules"] if m["path"] == name)
    text = re.sub(r', "where": "[^"]*"', "", json.dumps(mod, sort_keys=True))
    return re.sub(rf"\b{name}\.", "m.", text.replace(f'"{name}"', '"m"'))


def test_carcass_writes_the_drawer_cabinet_s_lines():
    """`carcass()` with a toe kick, a 9 mm back and three Cabineos is the
    carcass of `examples/drawer_cabinet.py` as it was written by hand,
    board for board and operation for operation."""
    box = Box.from_size(width=500, depth=600, height=720)
    with module("hand", box, front=box.right) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        for side in (left, right):
            side.cut(rect(depth=60, height=100), at=side.outer.bottom.front, name="toekick")
        bottom = board("bottom", ply15).on(left.toekick.top, toward=cab.top).between(left, right)
        top = board("top", ply15).on(cab.top).between(left, right)
        back = board("back", ply9).on(cab.back).between(left, right, bottom, top)
        bottom.join(left, right, using=cabineo(count=3))
        top.join(left, right, using=cabineo(count=3))
        back.join(left, right, bottom, top, using=domino("4x20", count=2))
    with module("std", box, front=box.right) as cab:
        c = carcass(cab, ply15, back=ply9, toekick=(60, 100), joins=cabineo(count=3))
    assert isinstance(c, Carcass) and [p.name for p in c] == ["left", "right", "bottom", "top", "back"]
    assert c.bottom.bottom.value == pytest.approx(cab.bottom.value + 100)
    assert _module_layout("std") == _module_layout("hand")


def test_carcass_defaults_and_front_limit():
    """Without `joins` and `back_joins` the carcass is joined with two
    Cabineos and two Dominos, as the wall cabinets are; `front=` holds the
    sides, the bottom and the top back from the front, as a position or as
    a board standing there."""
    box = Box.from_size(width=350, depth=450, height=600)
    with module("hand", box, front=box.right) as cab:
        behind = cab.front.into(ply12.thickness)
        left = board("left", ply15).on(cab.left).between(behind)
        right = board("right", ply15).on(cab.right).between(behind)
        bottom = board("bottom", ply15).on(cab.bottom).between(left, right, behind)
        top = board("top", ply15).on(cab.top).between(left, right, behind)
        back = board("back", ply9).on(cab.back).between(left, right, bottom, top)
        bottom.join(left, right, using=cabineo(count=2))
        top.join(left, right, using=cabineo(count=2))
        back.join(left, right, bottom, top, using=domino("4x20", count=2))
    with module("std", box, front=box.right) as cab:
        c = carcass(cab, ply15, back=ply9, front=cab.front.into(ply12.thickness))
    assert _module_layout("std") == _module_layout("hand")
    assert c.left.front.value == pytest.approx(cab.front.into(ply12.thickness).value)
    with module("door", box, front=box.right) as cab:
        door = board("door", ply12).on(cab.front)
        d = carcass(cab, ply15, back=ply9, front=door)
    assert d.left.front.value == pytest.approx(door.back.value)
    assert d.top.front.value == pytest.approx(door.back.value)
    assert d.back.left.value == pytest.approx(d.left.right.value)


def test_carcass_without_a_back():
    """`back=None` makes four boards, joined bottom and top to the sides;
    `back_joins=` is then an error, since there is nothing to join."""
    box = Box.from_size(width=800, depth=400, height=450)
    with module("open", box, front=box.back) as cab:
        c = carcass(cab, ply15)
        assert isinstance(c, OpenCarcass) and [p.name for p in c] == ["left", "right", "bottom", "top"]
        assert sorted(cab.parts) == ["bottom", "left", "right", "top"]
        assert len(c.left.ops) == 4          # a screw hole per Cabineo, two from the bottom and two from the top
        assert len(c.bottom.ops) == 12       # three overlapping holes per Cabineo, two a side
    with module("m", box):
        with pytest.raises(LangError, match=r"carcass\(\): back_joins= given, but back=None"):
            carcass(cab, ply15, back_joins=domino("4x20", count=2))  # type: ignore[call-overload]


def test_carcass_toekick_lifts_the_bottom_onto_the_notch():
    box = Box.from_size(width=600, depth=500, height=720)
    with module("m", box) as m:
        c = carcass(m, ply15, back=ply9, toekick=(70, 120))
    assert c.left.has_operation("toekick") and c.right.has_operation("toekick")
    assert c.bottom.bottom.value == pytest.approx(m.bottom.value + 120)
    assert c.bottom.front.value == pytest.approx(m.front.value)        # the bottom runs over the notch to the front
    assert c.left.toekick.back.value == pytest.approx(m.front.value + 70)   # the notch's depth, in the default frame
    assert build_layout()["problems"] == []


# -- drawer box ---------------------------------------------------------------------------------

def test_drawer_box_writes_the_drawer_cabinet_s_drawer():
    """`drawer_box()` is the drawer of `examples/drawer_cabinet.py` as it
    was written by hand: the slide sizes the box, box joints at the
    corners, the floor in grooves, the slide's cut-outs and hook holes, and
    the runners pre-drilling the carcass sides."""
    slide = drawer_slide("Dynapro 40", nl=450)
    box = Box.from_size(width=500, depth=600, height=720)

    def cabinet_with(name: str, by_hand: bool) -> None:
        with module(name, box, front=box.right) as cab:
            left, right, bottom, _, _ = carcass(cab, ply15, back=ply9, joins=cabineo(count=3))
            bay = cab.interior.with_sides(bottom=bottom.top)
            with scope("drawer", bay) as d:
                face = board("face", ply15).on(bay.front).between(bay.shrunk(1.5)).inset(1.5)
                if by_hand:
                    dbox = slide.drawer_box(bay, front=face.back, side_thickness=ply12.thickness,
                                            height=bay.height - 30)
                    l = board("left", ply12).on(dbox.left).between(dbox)
                    r = board("right", ply12).on(dbox.right).between(dbox)
                    f = board("front", ply12).on(dbox.front).between(l, r, dbox.bottom, dbox.top)
                    k = board("back", ply12).on(dbox.back).between(l, r, dbox.bottom, dbox.top)
                    for end in (f, k):
                        end.join(l, r, using=box_joint(7, margin=2, clearance=(0.1, 0.1)))
                    floor = board("floor", ply9).on(dbox.bottom.into(slide.recess)).between(l, r, f, k)
                    floor.join(l, r, f, k, using=groove(5, clearance=(0.5, 0.5)))
                    slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)
                    d.mount(slide, sides=(left, right), front=face.back)
                else:
                    made = drawer_box(d, bay, slide, front=face.back, height=bay.height - 30, material=ply12,
                                      floor=ply9, corners=box_joint(7, margin=2, clearance=(0.1, 0.1)),
                                      floor_joint=groove(5, clearance=(0.5, 0.5)), carcass=(left, right))
                    assert [p.name for p in made[:5]] == ["left", "right", "front", "back", "floor"]
                    assert made.box.height == pytest.approx(bay.height - 30)
                    assert isinstance(made.floor, Board)

    cabinet_with("hand", True)
    cabinet_with("std", False)
    assert _module_layout("std") == _module_layout("hand")
    assert build_layout()["problems"] == []


def test_drawer_box_without_corners_and_floor_joint():
    """`corners=None` leaves the corners to the shop and `floor_joint=None`
    the floor resting on the runners: the boards, the slide's machining and
    the runners are still made."""
    slide = drawer_slide("Movento 760H", nl=450)
    box = Box.from_size(width=500, depth=600, height=400)
    with module("c", box, front=box.right) as cab:
        left, right, _, _ = carcass(cab, ply15)
        with scope("drawer", cab.interior) as d:
            face = board("face", ply15).on(cab.interior.front)
            made = drawer_box(d, cab.interior, slide, front=face.back, height=150, material=ply12, floor=ply9,
                              corners=None, floor_joint=None, carcass=(left, right))
    names = {p.name: [getattr(op, "name", None) or "" for op in p.ops] for p in made[:5]}
    assert not any(n.startswith(("notch_", "gap_", "groove_")) for ns in names.values() for n in ns)
    assert any(n.startswith("coupling_") for n in names["front"])
    for side in (left, right):
        assert any((getattr(op, "name", None) or "").startswith("slide_") for op in side.ops)
    assert [h["path"] for h in cab.all_hardware()] == ["c.drawer.runners"]
