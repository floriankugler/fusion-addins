import math
import re
from collections.abc import Callable
from pathlib import Path

import pytest

from lang import *
from lang.core.layout import build_layout
from lang.core.ops import Cut, Hole, Op
from lang.core.layout_types import HardwareLayout
from lang.core.scope import registry
from lang.core.checks import _has_material  # type: ignore[reportPrivateUsage]
from lang.emit.plan import HoleStep, plan_layout
from lang.hardware.slides import BOTTOM_HEIGHT, BOX_MACHINING, INNER_FACE_OFFSET, DrawerSlide, HookHole, SlideModel
from lib import drawer_slides
from lib.drawer_slides import DYNAPRO_40, DYNAPRO_50_70, MOVENTO_760H, MOVENTO_766H
from helpers import bounds, ply12, ply15, ply18, ply9


def test_slide_dictates_the_drawer_box():
    slide = DrawerSlide(DYNAPRO_40, nl=450)
    assert slide.box_length == 440 and slide.depth_needed == 453 and slide.recess == 11.5
    with module("cab", Box.from_size(width=600, depth=500, height=300)) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        bay = cab.interior
        face = board("face", ply15).on(bay.front)
        box = slide.drawer_box(bay, front=face.back, side_thickness=ply12.t, height=150)
    # the drawer sides' inner faces sit 21 mm from the carcass sides
    assert box.left.value == left.inner.value + (INNER_FACE_OFFSET - 12) * left.inner.direction.sign
    assert box.right.value == right.inner.value + (INNER_FACE_OFFSET - 12) * right.inner.direction.sign
    assert box.width == 570 - 2 * 9
    assert box.front.value == face.back.value and box.depth == 440
    # the sides hang below the bottom panel, whose underside is 28 above the slide's bottom
    assert slide.side_lift == BOTTOM_HEIGHT["Grass"] - 11.5 == 16.5
    assert DrawerSlide(MOVENTO_760H, nl=450).side_lift == 28.5 - 13.5 == 15
    assert box.bottom.value == bay.bottom.value + 16.5 and box.height == 150


def test_slide_machines_the_drawer_box():
    slide = DrawerSlide(DYNAPRO_40, nl=450)
    with module("cab", Box.from_size(width=600, depth=500, height=300)) as cab:
        board("left", ply15).on(cab.left)
        board("right", ply15).on(cab.right)
        bay = cab.interior
        with scope("drawer1", bay):
            face = board("face", ply15).on(bay.front)
            box = slide.drawer_box(bay, front=face.back, side_thickness=12, height=150)
            l = board("left", ply12).on(box.left).between(box.front, box.back, box.bottom, box.top)
            r = board("right", ply12).on(box.right).between(box.front, box.back, box.bottom, box.top)
            f = board("front", ply12).on(box.front).between(l, r, box.bottom, box.top)
            k = board("back", ply12).on(box.back).between(l, r, box.bottom, box.top)
            floor = board("floor", ply9).on(box.bottom + slide.recess).between(l.into(5), r.into(5), f, k)
            slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)
    # the sides' inner faces (left is -y here), the floor's underside above the box bottom
    li, ri = l.inner.value, r.inner.value
    assert (li, ri) == (36, 564)
    z0, z1 = box.bottom.value, floor.bottom.value
    assert z1 == z0 + 11.5
    # cut-outs at both ends, from the lower edge to the floor's underside: 69 wide
    # in the front for the couplings, 35 in the back for the hooks (u = y, v = z)
    for board_, what, width in ((f, "coupling", 69), (k, "hook", 35)):
        cuts = {op.name: op.shape.bounds for op in board_.ops if isinstance(op, Cut)}
        assert cuts == {f"{what}_left": (li, z0, li + width, z1), f"{what}_right": (ri - width, z0, ri, z1)}
    # three hook pre-drill holes per side in the back board's rear face, 2 x 8 by default
    holes = [op for op in k.ops if isinstance(op, Hole)]
    assert all(h.face == "back" and h.d == 2 and h.depth == 8 for h in holes)
    assert {(h.u, h.v) for h in holes} == {
        (li + 42, z1 + 15), (li + 42, z1 + 47), (li + 10, z1 + 47),
        (ri - 42, z1 + 15), (ri - 42, z1 + 47), (ri - 10, z1 + 47)}
    # named by the side, as the cut-outs (the van's terms: the left side at y 36)
    assert [(h.name, h.u) for h in holes] == [("hook_left_a", li + 42), ("hook_left_b", li + 42),
                                              ("hook_left_c", li + 10), ("hook_right_a", ri - 42),
                                              ("hook_right_b", ri - 42), ("hook_right_c", ri - 10)]
    assert DrawerSlide(DYNAPRO_40, nl=450, hook_hole=(3, 10)).hook_hole == (3, 10)


def _drawer(slide: DrawerSlide, machine: bool = True, into: str = "lrf",
            floor_material: Material = ply9) -> tuple[Scope, dict[str, Board]]:
    """A drawer in a 600 x 500 x 300 cabinet in the van's terms, built
    much as the example builds one: 12 mm sides, front and back, a 9 mm
    floor in grooves in the sides and the front (`into`: l, r, f, k; not
    the back, as with Blum), the runners mounted from the face's back."""
    with module("cab", Box.from_size(width=600, depth=500, height=300)) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        bay = cab.interior
        with scope("drawer1", bay) as d:
            face = board("face", ply15).on(bay.front)
            box = slide.drawer_box(bay, front=face.back, side_thickness=12, height=150)
            l = board("left", ply12).on(box.left).between(box.front, box.back, box.bottom, box.top)
            r = board("right", ply12).on(box.right).between(box.front, box.back, box.bottom, box.top)
            f = board("front", ply12).on(box.front).between(l, r, box.bottom, box.top)
            k = board("back", ply12).on(box.back).between(l, r, box.bottom, box.top)
            floor = board("floor", floor_material).on(box.bottom + slide.recess).between(l, r, f, k)
            named = {"l": l, "r": r, "f": f, "k": k}
            floor.join(*(named[c] for c in into), using=groove(5, clearance=(0.5, 0.5)))
            if machine:
                slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)
        d.mount(slide, sides=(left, right), front=face.back)
    return d, {"carcass_left": left, "carcass_right": right, "face": face, "left": l, "right": r,
               "front": f, "back": k, "floor": floor}


@pytest.mark.parametrize("model, hook, thick, into", [
    (MOVENTO_760H, (6.0, 10.0), False, "cab.drawer1.floor"),
    (MOVENTO_760H, (6.0, through), False, "cab.drawer1.floor"),
    # 6.75 deep from the rear face of the 12 mm back: 5.25 short of its
    # inner face, past the floor's 5, inside its groove's 5.5
    (MOVENTO_760H, (6.0, 6.75), False, "groove_floor, where cab.drawer1.floor goes into it"),
    (DYNAPRO_40, (2.0, 8.0), True, "cab.drawer1.floor"),
])
def test_hook_holes_must_not_run_into_the_floor(model: drawer_slides.SlideModel, hook: HookHole, thick: bool,
                                                into: str):
    """Florian 2026-10-12: a rear hook hole that would run into the floor
    where it goes into the back board, or into its groove there, is an
    error, and nothing is cut. Blum's hole (6 mm, 11 above the floor's
    underside) meets a 9 mm floor grooved into the back; Grass's (15 and
    47 above) only a floor thicker than 14, here 18."""
    slide = DrawerSlide(model, nl=450, hook_hole=hook)
    material_ = ply18 if thick else ply9
    _, parts = _drawer(slide, machine=False, into="lrfk", floor_material=material_)
    k, f = parts["back"], parts["front"]
    up = 15 if thick else 11
    with pytest.raises(LangError, match=rf"cab\.drawer1\.back: .*: the rear hook's {hook[0]:g} mm hole \d+ from "
                                        rf"cab\.drawer1\.left's inner face and {up} above the floor's underside "
                                        rf"would run into {re.escape(into)}: leave the back board out of the floor's "
                                        "groove join"):
        slide.machine_box(sides=(parts["left"], parts["right"]), front=f, back=k, floor=parts["floor"])
    assert not [op for op in (*k.ops, *f.ops) if isinstance(op, (Cut, Hole))]       # nothing cut
    # with the floor in the sides and the front only, the back is drilled
    registry.reset()
    _, parts = _drawer(slide, into="lrf", floor_material=material_)
    family = "Grass" if model is DYNAPRO_40 else "Blum"
    assert len([op for op in parts["back"].ops if isinstance(op, Hole)]) == 2 * len(BOX_MACHINING[family].hook_holes)


def test_a_floor_placed_into_the_back_without_a_groove_is_checked_too():
    slide = DrawerSlide(MOVENTO_760H, nl=450)
    with module("cab", Box.from_size(width=600, depth=500, height=300)) as cab:
        bay = cab.interior
        with scope("drawer1", bay):
            box = slide.drawer_box(bay, front=bay.front, side_thickness=12, height=150)
            l = board("left", ply12).on(box.left).between(box.front, box.back, box.bottom, box.top)
            r = board("right", ply12).on(box.right).between(box.front, box.back, box.bottom, box.top)
            f = board("front", ply12).on(box.front).between(l, r, box.bottom, box.top)
            k = board("back", ply12).on(box.back).between(l, r, box.bottom, box.top)
            floor = board("floor", ply9).on(box.bottom + slide.recess).between(l, r, f, k.into(5))
            with pytest.raises(LangError, match=r"would run into cab\.drawer1\.floor: leave the back board out"):
                slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)

def test_slide_machines_a_blum_drawer_box():
    """Blum: 75 mm cut-outs at both ends of the front and the back board,
    and one 6 x 10 hole per rear hook into the back board's rear face, 7
    from the side's inner face and 11 above the floor's underside."""
    _, parts = _drawer(DrawerSlide(MOVENTO_760H, nl=450))
    f, k, floor = parts["front"], parts["back"], parts["floor"]
    li, ri = parts["left"].inner.value, parts["right"].inner.value
    z0, z1 = f.box().bottom.value, floor.bottom.value
    assert z1 - z0 == 13.5                                    # the middle of Blum's 12 to 15
    for board_, what in ((f, "coupling"), (k, "hook")):
        cuts = {op.name: op.shape.bounds for op in board_.ops if isinstance(op, Cut)}
        assert cuts == {f"{what}_left": (li, z0, li + 75, z1), f"{what}_right": (ri - 75, z0, ri, z1)}
    holes = [op for op in k.ops if isinstance(op, Hole)]
    assert all(h.face == "back" and h.d == 6 and h.depth == 10 for h in holes)
    assert {(h.u, h.v) for h in holes} == {(li + 7, z1 + 11), (ri - 7, z1 + 11)}


@pytest.mark.parametrize("model, diameter, count", [(DYNAPRO_40, 2.0, 6), (MOVENTO_760H, 6.0, 2)])
def test_hook_holes_through_the_back_go_in_from_its_inner_face(model: drawer_slides.SlideModel, diameter: float,
                                                               count: int):
    """Florian 2026-10-12: the rear hook holes may go all the way through
    the back board, `hook_hole=(d, through)`. Then they are drilled from
    the back board's inner face (front, toward the drawer's middle), so
    nothing is machined from its rear face; same places, through the 12
    mm back, and the plan drills them to the far face."""
    _, fixed = _drawer(DrawerSlide(model, nl=450))
    registry.reset()
    _, parts = _drawer(DrawerSlide(model, nl=450, hook_hole=(diameter, through)))
    holes = [op for op in parts["back"].ops if isinstance(op, Hole)]
    assert len(holes) == count
    assert all(h.face == "front" and h.d == diameter and h.through and h.depth == 12 for h in holes)
    assert ({(h.u, h.v) for h in holes}
            == {(h.u, h.v) for h in fixed["back"].ops if isinstance(h, Hole) and h.face == "back"})
    plan = plan_layout(build_layout())
    back = next(p for p in plan.parts if p.path == "cab.drawer1.back")
    (step,) = [s for s in back.steps if isinstance(s, HoleStep)]
    assert step.depth is None and len(step.points) == count


@pytest.mark.parametrize("hook_hole", [(0.0, 8.0), (2.0, 0.0), (-6.0, through)])
def test_bad_hook_holes_are_refused(hook_hole: HookHole):
    with pytest.raises(LangError, match="hook_hole= needs a diameter and a depth"):
        DrawerSlide(DYNAPRO_40, nl=450, hook_hole=hook_hole)


def test_slide_refuses_what_it_cannot_take():
    with pytest.raises(LangError):
        DrawerSlide(DYNAPRO_40, nl=700)           # not made in that length
    with pytest.raises(LangError):
        DrawerSlide(MOVENTO_760H, nl=500, bottom_recess=10)   # Blum allows 12 to 15
    slide = DrawerSlide(MOVENTO_760H, nl=500)
    with module("cab", Box.from_size(width=600, depth=500, height=300)) as cab:
        bay = cab.interior
        face = board("face", ply15).on(bay.front)
        with pytest.raises(LangError):
            slide.drawer_box(bay, front=face.back, side_thickness=12, height=150)   # 485 < 503 deep
        with pytest.raises(LangError):
            slide.drawer_box(bay, front=bay.front, side_thickness=19, height=150)   # sides too thick


def test_mount_predrills_the_carcass_sides():
    slide = DrawerSlide(DYNAPRO_40, nl=450, holes=4)
    with module("cab", Box.from_size(width=600, depth=500, height=300)) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        bay = cab.interior
        with scope("drawer1", bay) as d:
            face = board("face", ply15).on(bay.front)
        d.mount(slide, sides=(left, right), front=face.back)
    holes = [op for op in left.ops if isinstance(op, Hole)]
    assert len(holes) == 4 and all(h.face == "right" and h.d == 2 and h.depth == 4 for h in holes)
    # named by the drawer, a to d from the front
    assert [h.name for h in holes] == ["slide_drawer1_a", "slide_drawer1_b", "slide_drawer1_c", "slide_drawer1_d"]
    # a row 38 above the bay bottom, positions behind the runner's front (the face's back at x = 15)
    assert {h.v for h in holes} == {38.0}
    assert [h.u for h in holes] == [15 + p for p in slide.hole_positions()]
    assert slide.hole_positions() == [19, 69, 165, 261]
    assert len([op for op in right.ops if isinstance(op, Hole)]) == 4
    # the runner pair as boxes, a body per runner
    (runners,) = d.hardware
    assert runners["path"] == "cab.drawer1.runners" and [b["name"] for b in runners["bodies"]] == ["left", "right"]
    layout = build_layout()
    assert layout["modules"][0]["hardware"] == [runners]


def test_runners_lie_against_the_carcass_sides():
    """The module is in the van's terms (no front=), so the drawer's left,
    seen standing in front of it, is the module's right side, at y 585..600.
    Each runner's boxes start at its side's inner face, the runner front
    (the face's back, x = 15) and the bay's bottom (z = 0). Grass NL 450:
    the cabinet rail from 4 behind the runner front, the runner's end at NL
    + 1.5; 49 high; the coupling's box as wide as the front board's
    cut-out, 21 + 69 from the carcass side."""
    slide = DrawerSlide(DYNAPRO_40, nl=450)
    with module("cab", Box.from_size(width=600, depth=500, height=300)) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        with scope("drawer1", cab.interior) as d:
            face = board("face", ply15).on(cab.interior.front)
        d.mount(slide, sides=(left, right), front=face.back)
    (runners,) = d.hardware
    by_name = {b["name"]: b for b in runners["bodies"]}
    assert bounds(by_name["left"]) == ([15, 585 - 90, 1.1], [15 + 451.5, 585, 49])
    assert bounds(by_name["right"]) == ([15, 15, 1.1], [15 + 451.5, 15 + 90, 49])
    flange = by_name["left"]["boxes"][0]
    assert flange == {"min": [19, 582.5, 1.1], "max": [466.5, 585, 49]}
    # flange, base, drawer member, coupling, hook: the member's top carries
    # the floor, 28 above the bay's bottom, the coupling hangs below it and
    # the hook stands on it
    assert [b["max"][2] for b in by_name["left"]["boxes"]] == [49, 12.9, 28, 28, 34.9]
    assert by_name["left"]["boxes"][4]["min"][2] == 28


def test_runner_lengths_follow_the_nominal_length():
    for model, nl, end in ((DYNAPRO_40, 300, 301.5), (DYNAPRO_50_70, 750, 751.5), (MOVENTO_760H, 250, 252.5),
                           (MOVENTO_766H, 750, 752.5)):
        boxes = DrawerSlide(model, nl=nl).runner_boxes()
        assert max(y1 for _, (_, y1), _ in boxes.values()) == end
        assert boxes["hook"][1] == (nl - 10, end)           # behind the drawer box, NL - 10 long


@pytest.mark.parametrize("model", [DYNAPRO_40, MOVENTO_760H])
def test_runners_leave_room_for_the_drawer_box(model: drawer_slides.SlideModel):
    """The runner boxes touch the carcass sides, the drawer face, the floor
    and the back board, but overlap none of them: the couplings pass the
    front board through its cut-outs, the drawer members run below the
    floor and inside the drawer sides, the back board through its cut-outs.
    Without the cut-outs the couplings hit the front board and the drawer
    members the back board."""
    def overlaps(machine: bool) -> set[tuple[str, str]]:
        registry.reset()
        d, parts = _drawer(DrawerSlide(model, nl=450), machine)
        out: set[tuple[str, str]] = set()
        for body in d.hardware[0]["bodies"]:
            for b in body["boxes"]:
                box = Box(dict(zip("xyz", b["min"])), dict(zip("xyz", b["max"])))  # type: ignore[arg-type]
                for name, part in parts.items():
                    if box.overlaps(part.box()) and _has_material(part, box.intersection(part.box())):
                        out.add((body["name"], name))
        return out
    assert overlaps(machine=True) == set()
    assert overlaps(machine=False) == {(r, b) for r in ("left", "right") for b in ("front", "back")}


def test_preview_draws_the_runners_as_boxes():
    """The preview meshes each runner as the union of its boxes."""
    from lang.preview.mesh import build_scene
    slide = DrawerSlide(DYNAPRO_40, nl=450)
    with module("cab", Box.from_size(width=600, depth=500, height=300)) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        with scope("drawer1", cab.interior) as d:
            face = board("face", ply15).on(cab.interior.front)
        d.mount(slide, sides=(left, right), front=face.back)
    scene = build_scene(build_layout())
    meshes = {}
    for node in scene.graph.nodes_geometry:
        if "runners" in node:
            transform, geometry = scene.graph[node]
            mesh = scene.geometry[geometry].copy()
            mesh.apply_transform(transform)
            meshes[node.rsplit(".", 1)[1]] = mesh
    assert set(meshes) == {"left", "right"}
    assert meshes["left"].is_volume and meshes["left"].bounds.round(1).tolist() == [[15, 495, 1.1], [466.5, 585, 49]]
    assert meshes["right"].bounds.round(1).tolist() == [[15, 15, 1.1], [466.5, 105, 49]]


def _runners(front: bool) -> HardwareLayout:
    """The runners of a drawer mounted in a module in the van's terms, or in
    a cabinet opening the same way (front=box.front)."""
    registry.reset()
    slide = DrawerSlide(DYNAPRO_40, nl=450)
    box = Box.from_size(width=600, depth=500, height=300)
    with (cabinet("cab", box, front=box.front) if front else module("cab", box)) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        with scope("drawer1", cab.interior) as d:
            face = board("face", ply15).on(cab.interior.front)
        d.mount(slide, sides=(left, right), front=face.back)
    (runners,) = d.hardware
    return runners


def test_runners_are_named_by_the_drawers_own_sides_whatever_the_frame():
    """A left-hand and a right-hand runner, named by the drawer's own left
    and right: the same in a module in the van's terms, whose left is the
    drawer's right, as in a cabinet."""
    plain, cabinet = _runners(front=False), _runners(front=True)
    assert plain["bodies"] == cabinet["bodies"]
    left = next(b for b in plain["bodies"] if b["name"] == "left")
    assert bounds(left)[1][1] == 585                       # the drawer's left is +y, facing +x


def test_one_stations_rule_in_lib():
    """`lib.stations` spreads stations for every add-in and the language;
    the three callers in lib keep their own refusals (review finding 29)."""
    from lib import connector_data, door_latches, sliding_brackets, stations
    stations._self_check()  # type: ignore[reportPrivateUsage]
    for length, count, end in ((566.0, 1, 80.0), (566.0, 3, 80.0), (597.0, 2, 60.0), (1000.0, 7, 33.3)):
        expected = stations.stations(length, count, end)
        assert connector_data.stations(length, count, end) == expected
        assert door_latches.stations(length, count, end) == expected
        assert sliding_brackets.stations(length, count, end) == expected
    assert connector_data.stations(100, 2, 60) == [60, 40]           # no length check, as before
    assert door_latches.stations(100, 1, 0) == sliding_brackets.stations(100, 1, 0) == [50]
    for refused in (lambda: connector_data.stations(100, 0, 10), lambda: door_latches.stations(100, 2, 0),
                    lambda: door_latches.stations(160, 2, 80), lambda: sliding_brackets.stations(100, 2, 50)):
        with pytest.raises(ValueError):
            refused()


def test_the_add_ins_specs_in_cm_have_every_length_in_cm():
    """The add-ins read the hatch hinges', sliding brackets' and ball
    catches' specs through `in_cm()`: every length (a float, or a tuple of
    them) a tenth, counts and angles (ints) and names as they are. A length
    added to a spec and left out of `in_cm()` would reach Fusion ten times
    too large."""
    import dataclasses
    from lib import ball_catches, hatch_hinges, sliding_brackets

    def tenth(value: object) -> object:
        if isinstance(value, tuple):
            return tuple(tenth(v) for v in value)  # type: ignore[reportUnknownVariableType]
        return value / 10 if isinstance(value, float) else value

    specs = [*hatch_hinges.HINGE_SPECS, *sliding_brackets.BRACKETS.values(), *ball_catches.CATCHES.values()]
    for spec in specs:
        cm = spec.in_cm()
        for f in dataclasses.fields(spec):
            assert getattr(cm, f.name) == tenth(getattr(spec, f.name)), (spec.name, f.name)


# -- the slide's mount: plan, check everything, then drill (review findings 23, 24) ------------------------

def _bay() -> tuple[Scope, Scope, dict[str, Board]]:
    """The 600 x 500 x 300 cabinet in the van's terms with a top, its
    drawer scope and face; no slide is mounted."""
    with module("cab", Box.from_size(width=600, depth=500, height=300)) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        top = board("top", ply15).on(cab.top).between(left, right)
        with scope("drawer1", cab.interior.with_sides(top=top.bottom)) as d:
            face = board("face", ply15).on(d.front)
    return cab, d, {"left": left, "right": right, "top": top, "face": face}


def _untouched(cab: Scope) -> tuple[list[tuple[str, list[Op], str]], list[HardwareLayout]]:
    """Every board's operations and outline, and the hardware."""
    return [(p.path, list(p.ops), p.outline.geometry.wkt) for p in cab.all_parts()], cab.all_hardware()


@pytest.mark.parametrize("which, message", [
    ("left, top", r"cab\.top is not a side of the drawer's bay: it does not stand across the bay's width"),
    ("left, left", r"sides= names cab\.left twice"),
    ("left, inner", r"cab\.left and cab\.inner both stand on the drawer's"),
    # the drawer's own left, in the van's terms the side called right, first
    ("deep pilot", r"the pilot depth \(20 mm\) must be less than cab\.right's thickness \(15 mm\)"),
    ("pilot as deep as the side", r"the pilot depth \(15 mm\) must be less than cab\.right's thickness"),
    ("in a hole", r"the pilot hole \(2 mm\) does not fit on cab\.right's left face"),
])
def test_a_refused_slide_drills_nothing(which: str, message: str):
    """Everything is checked before a hole is drilled: the sides (one
    standing across the bay on each side of it), each pilot hole on its
    face and short of the far face. Before, (left, top) drilled the left
    side and (left, left) drilled it twice before they failed."""
    cab, d, parts = _bay()
    pilot = {"deep pilot": (2.0, 20.0), "pilot as deep as the side": (2.0, 15.0)}.get(which, (2.0, 4.0))
    slide = DrawerSlide("Dynapro 40", nl=450, pilot=pilot)
    left, right, top = parts["left"], parts["right"], parts["top"]
    sides = {"left, top": (left, top), "left, left": (left, left)}.get(which, (left, right))
    if which == "left, inner":
        with cab:
            sides = (left, board("inner", ply15).on(left.inner, toward=cab.right))
    if which == "in a hole":       # a shelf pin where the right side's first pilot goes (x 15 + 19, z 38)
        right.hole(d=5, depth=10, at=right.inner.front(Pos("x", 34)).bottom(Pos("z", 38)))
    before = _untouched(cab)
    with pytest.raises(LangError, match=message):
        d.mount(slide, sides=sides, front=parts["face"].back)
    assert _untouched(cab) == before


def test_a_partition_between_two_bays_takes_a_drawer_on_either_face():
    """Two drawers side by side, a partition between their bays in the
    middle of the cabinet: each slide drills the face of the partition
    toward its own bay, found from the bay's middle, not from the
    partition's `inner`, which is ambiguous for a board in the middle of
    its scope."""
    slide = DrawerSlide("Dynapro 40", nl=450)
    box = Box.from_size(width=1000, depth=500, height=300)
    with cabinet("cab", box, front=box.front) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        wall = board("wall", ply15).center(cab.center("width"))
        with pytest.raises(LangError, match="ambiguous"):
            _ = wall.inner                                      # what the slide used before
        bays = [cab.interior.with_sides(left=left.inner, right=wall.left),
                cab.interior.with_sides(left=wall.right, right=right.inner)]
        for i, (bay, sides) in enumerate(zip(bays, ((left, wall), (wall, right))), 1):
            with scope(f"drawer{i}", bay) as d:
                face = board("face", ply15).on(bay.front)
            d.mount(slide, sides=sides, front=face.back)
    faces = {op.name: op.face for op in wall.ops if isinstance(op, Hole)}
    # a cabinet (front=) facing -x: its left is +y, so the first bay is on the wall's +y side
    assert {face for name, face in faces.items() if name and name.startswith("slide_drawer1_")} == {"right"}
    assert {face for name, face in faces.items() if name and name.startswith("slide_drawer2_")} == {"left"}
    assert len(faces) == 8
    for i in (1, 2):
        (runners,) = cab.child(f"drawer{i}").hardware
        assert [b["name"] for b in runners["bodies"]] == ["left", "right"]
    assert no_interference(cab) == []


def test_a_drawer_runs_on_one_pair_of_slides():
    """A second mount in the same drawer scope is refused before anything
    is drilled (it drilled the row a second time before)."""
    cab, d, parts = _bay()
    d.mount(DrawerSlide("Dynapro 40", nl=450), sides=(parts["left"], parts["right"]), front=parts["face"].back)
    before = _untouched(cab)
    with pytest.raises(LangError, match=r"cab\.drawer1 has its runners already"):
        d.mount(DrawerSlide("Movento 760H", nl=450), sides=(parts["left"], parts["right"]), front=parts["face"].back)
    assert _untouched(cab) == before


def test_slide_settings_are_checked_where_the_slide_is_made():
    """holes= and pilot= are checked in the constructor, not halfway
    through drilling (holes=99 was a bare ValueError from lib)."""
    with pytest.raises(LangError, match=r"holes= must be 1 to 9, the odd holes of the runner, not 99"):
        DrawerSlide("Dynapro 40", nl=450, holes=99)
    with pytest.raises(LangError, match="holes= must be 1 to"):
        DrawerSlide("Dynapro 40", nl=450, holes=0)
    with pytest.raises(LangError, match=r"pilot= needs a diameter and a depth greater than zero, not 0 x 4"):
        DrawerSlide("Dynapro 40", nl=450, pilot=(0, 4))
    assert DrawerSlide("Dynapro 40", nl=450, holes=9).hole_positions()[-1] == 261
    assert DrawerSlide("Dynapro 40", nl=450).pilot == (2.0, 4.0)


def test_a_hook_hole_as_deep_as_the_back_is_refused():
    """A pilot hole must stop short of the far face; `through` says it
    goes all the way."""
    slide = DrawerSlide("Movento 760H", nl=450, hook_hole=(6, 12))
    with pytest.raises(LangError, match=r"the hook hole depth \(12 mm\) must be less than cab\.drawer1\.back's "
                                        r"thickness \(12 mm\)"):
        _drawer(slide)


def test_slides_by_model_name():
    """A build file names the model (review finding 43); a spec object of
    lib's still works, for a slide of your own."""
    from typing import get_args
    from lang.hardware.slides import SLIDE_MODELS
    assert get_args(SlideModel) == tuple(SLIDE_MODELS)
    assert {m.name for m in SLIDE_MODELS.values()} == {m.name for m in drawer_slides.SLIDE_MODELS}
    assert DrawerSlide("Dynapro 40", nl=450).model is DYNAPRO_40
    assert DrawerSlide(MOVENTO_766H, nl=450).model is MOVENTO_766H
    with pytest.raises(LangError, match=r"DrawerSlide\(\): expected 'Movento 760H'"):
        DrawerSlide("Dynapro 41", nl=450)  # type: ignore[arg-type]


# -- core helpers for hardware (review findings 25, 27) -----------------------------------------------

def test_hole_fits_on_the_face_region():
    """`Board.hole_fits`: the centre and the four points a radius away on
    the face, less the holes, pockets and V-grooves made into it and those
    through from the other face, and the circle clear of them."""
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom)          # x 0..300 (u), y 0..400 (v), faces top and bottom
        panel.pocket(rect(width=40, depth=40), at=panel.top.front(50).left(50), depth=5)
        panel.hole(d=10, depth=5, at=panel.bottom.front(Pos("x", 150)).left(Pos("y", 200)))
        panel.hole(d=10, depth=through, at=panel.bottom.front(Pos("x", 250)).left(Pos("y", 300)))
    top, bottom = panel.top, panel.bottom
    assert panel.hole_fits(top, (150, 100), 5)
    assert not panel.hole_fits(top, (299, 100), 5)               # its rim over the edge
    assert panel.hole_fits(top, (297.5, 100), 5)                 # tangent to the edge
    assert not panel.hole_fits(top, (70, 70), 2)                 # in the pocket on the top
    assert panel.hole_fits(bottom, (70, 70), 2)                  # the pocket does not reach the bottom
    assert not panel.hole_fits(bottom, (150, 200), 2)            # in the hole made into the bottom
    assert panel.hole_fits(top, (150, 200), 2)                   # which does not reach the top
    assert not panel.hole_fits(top, (250, 300), 2)               # a through hole counts on both faces
    # its circle overlapping the hole diagonally, every probe outside it
    assert not panel.hole_fits(bottom, (150 + 6.5, 200 + 6.5), 10)
    assert panel.hole_fits(bottom, (150 + 7.5, 200 + 7.5), 10)
    region = panel.face_region(top)
    assert region.area == pytest.approx(300 * 400 - 40 * 40 - math.pi * 25, rel=1e-3)
    with pytest.raises(LangError, match="narrow face"):
        panel.hole_fits(panel.front, (0, 0), 2)


def test_one_hardware_name_per_scope():
    """`place_hardware` refuses a second item of one name; hardware of
    which one scope holds several numbers it with `unique_hardware_name`."""
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        board("panel", ply15).on(m.bottom)
    m.place_hardware("door_hinges", [])
    with pytest.raises(LangError, match="hardware name 'door_hinges' is used twice in this scope"):
        m.place_hardware("door_hinges", [])
    with pytest.raises(LangError, match="collides with a part"):
        m.place_hardware("panel", [])
    assert m.unique_hardware_name("door_hinges") == "door_hinges_2"
    assert m.unique_hardware_name("panel") == "panel_2"
    assert m.unique_hardware_name("runners") == "runners"


# -- the hardware in the language (review finding 43) --------------------------------------------------

def test_lang_exports_the_hardware_and_no_example_imports_it_from_elsewhere():
    import lang
    import lang.hardware
    names = {"DrawerSlide", "SlideModel", "ConcealedHinge", "HingeModel", "HatchHinge", "HatchHingeModel",
             "BallCatch", "CatchModel", "DoorLatch", "LatchModel", "SlidingBracket", "BracketModel"}
    assert names <= set(lang.__all__) and names == set(lang.hardware.__all__)
    examples = Path(__file__).resolve().parent.parent / "examples"
    for path in examples.glob("*.py"):
        text = path.read_text()
        assert "lang.hardware" not in text and "from lib" not in text and "import lib" not in text, path.name


# -- every hardware: a refused mount changes nothing (review finding 32) --------------------------------

def _refused_slide() -> tuple[Scope, Callable[[], object], str]:
    cab, d, parts = _bay()
    return cab, lambda: d.mount(DrawerSlide("Dynapro 40", nl=450), sides=(parts["left"], parts["top"]),
                                front=parts["face"].back), "is not a side of the drawer's bay"


def _refused_hinge() -> tuple[Scope, Callable[[], object], str]:
    """The door holes fit; the carcass holes of the second hinge land in a
    hole drilled before."""
    box = Box.from_size(width=500, depth=350, height=700)
    with module("cab", box) as cab:
        left = board("left", ply15).on(cab.left).between(cab.front.into(12))
        door = board("door", ply12).on(cab.front)
        left.hole(d=5, depth=10, at=left.right.front(Pos("x", 50.5)).bottom(Pos("z", 640 + 16)))
    return cab, lambda: cab.mount(ConcealedHinge(), door=door, carcass=left), "does not fit on cab.left's right face"


def _refused_hatch_hinge() -> tuple[Scope, Callable[[], object], str]:
    """The left hinge fits; a hole in the hatch where the right one's
    upper pilot goes (in the van's terms the hatch's right is -y: 25 in
    from the side at y 18)."""
    box = Box.from_size(width=600, depth=320, height=350)
    with module("cab", box) as cab:
        left = board("left", ply18).on(cab.left).between(cab.front.into(18), cab.back)
        right = board("right", ply18).on(cab.right).between(cab.front.into(18), cab.back)
        top = board("top", ply18).on(cab.top).between(left, right, cab.front.into(18), cab.back)
        hatch = board("hatch", ply18).on(cab.front)
        hatch.hole(d=6, depth=5, at=hatch.back.left(Pos("y", 43)).bottom(Pos("z", 320)))
    return cab, lambda: cab.mount(HatchHinge("Free space 1.11"), hatch=hatch, sides=(left, right), top=top), \
        "pilot holes do not fit"


def _refused_catch() -> tuple[Scope, Callable[[], object], str]:
    """Catches 1 and 2 fit on the left edge; a hole in the panel under the
    holder of catch 3, on the right edge."""
    with module("floor", Box.from_size(width=800, depth=1000, height=100)) as f:
        panel = board("panel", ply15).on(f.bottom).show(f.top)
        panel.cut(rect(width=400, depth=300).rounded(20), at=panel.top.center, name="opening")
        catch = BallCatch()
        hatch = catch.hatch("hatch", panel.opening)
        panel.hole(d=4, depth=5, at=panel.bottom.front(Pos("x", 410)).left(Pos("y", 608.4)))
    return f, lambda: f.mount(catch, opening=panel.opening, edge=panel.opening.left, hatch=hatch), \
        "the holder of catch 3 does not fit"


def _refused_latch() -> tuple[Scope, Callable[[], object], str]:
    """The door's holes fit; a hole in the top where the strike's pair goes."""
    box = Box.from_size(width=600, depth=500, height=720)
    with module("cab", box) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        top = board("top", ply15).on(cab.top).between(left, right)
        door = board("door", ply15).on(cab.front).between(left, right, cab.bottom, top).inset(2)
        top.hole(d=5, depth=5, at=top.bottom.front(Pos("x", 29)).left(Pos("y", 309.5)))
    return cab, lambda: cab.mount(DoorLatch("Pull Lock 44"), door=door, carcass=top), \
        "does not fit on cab.top's bottom face"


def _refused_bracket() -> tuple[Scope, Callable[[], object], str]:
    """The brackets on the left side fit; a pocket on the right side under
    the frame part of bracket 3."""
    with module("cab", Box.from_size(width=600, depth=400, height=500)) as cab:
        left = board("left", ply18).on(cab.left).between(cab.front.into(12))
        right = board("right", ply18).on(cab.right).between(cab.front.into(12))
        cover = board("cover", ply12).on(cab.front)
        right.pocket(rect(depth=20, height=20), at=right.left.front(10).bottom(40), depth=5)   # x 22..42, z 40..60
    return cab, lambda: cab.mount(SlidingBracket(), panel=cover, frame=[left, right]), \
        "the frame part of bracket 3 does not fit on cab.right"


@pytest.mark.parametrize("case", [_refused_slide, _refused_hinge, _refused_hatch_hinge, _refused_catch,
                                  _refused_latch, _refused_bracket])
def test_a_refused_mount_changes_nothing(case: Callable[[], tuple[Scope, Callable[[], object], str]]):
    """Each hardware works out and checks every hole and box before it
    drills or places one: a mount refused late, after the first hinges,
    catches or brackets were found to fit, leaves every board's operations
    and outline and the scope's hardware as they were."""
    scope_, mount, message = case()
    before = _untouched(scope_)
    with pytest.raises(LangError, match=re.escape(message)):
        mount()
    assert _untouched(scope_) == before


def test_a_bay_exactly_deep_enough_is_deep_enough_at_any_origin():
    """Found by fuzzing: a bay exactly NL + 3 deep behind the runner's
    front, 518.05 - 15.05 at its origin, came out 502.99999999999994 and was
    refused, where the same cabinet facing another way was not. The depth
    is compared within the hardware's tolerance."""
    slide = DrawerSlide("Dynapro 50/70", nl=500)
    bay = Box.from_size(width=500, depth=518.0, height=300, origin=(0.05, 0, 0))     # x 0.05 to 518.05
    box = slide.drawer_box(bay, front=Pos("x", 15.05), side_thickness=12, height=100)
    assert box.hi["x"] - box.lo["x"] == pytest.approx(490)                          # NL - 10
    with pytest.raises(LangError, match="needs 503 mm behind the runner's front"):
        slide.drawer_box(bay, front=Pos("x", 15.06), side_thickness=12, height=100)
