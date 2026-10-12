import pytest

from lang import *
from lang.core.layout import build_layout
from lang.core.ops import Cut, Hole
from lang.core.layout_types import HardwareBodyLayout, HardwareLayout
from lang.core.scope import registry
from lang.core.checks import _has_material  # type: ignore[reportPrivateUsage]
from lang.hardware.slides import BOTTOM_HEIGHT, INNER_FACE_OFFSET, DrawerSlide
from lib.drawer_slides import DYNAPRO_40, DYNAPRO_50_70, MOVENTO_760H, MOVENTO_766H, SlideModel


@pytest.fixture(autouse=True)
def fresh_registry():
    registry.reset()
    yield
    registry.reset()


ply15 = material("birch", t=15)
ply12 = material("birch", t=12)
ply9 = material("birch", t=9)


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
    assert DrawerSlide(DYNAPRO_40, nl=450, hook_hole=(3, 10)).hook_hole == (3, 10)


def _drawer(slide: DrawerSlide, machine: bool = True) -> tuple[Scope, dict[str, Board]]:
    """A drawer in a 600 x 500 x 300 cabinet in the van's terms, built as
    the example builds one: 12 mm sides, front and back, a 9 mm floor in
    grooves, the runners mounted from the face's back."""
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
            floor = board("floor", ply9).on(box.bottom + slide.recess).between(l.into(5), r.into(5), f, k)
            for side in (l, r):
                side.cut(floor.box().grown(top=0.5, left=0.5, right=0.5), name="floor_groove")
            if machine:
                slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)
        d.mount(slide, sides=(left, right), front=face.back)
    return d, {"carcass_left": left, "carcass_right": right, "face": face, "left": l, "right": r,
               "front": f, "back": k, "floor": floor}


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


def _bounds(body: HardwareBodyLayout) -> tuple[list[float], list[float]]:
    boxes = body["boxes"]
    return ([min(b["min"][i] for b in boxes) for i in range(3)], [max(b["max"][i] for b in boxes) for i in range(3)])


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
    assert _bounds(by_name["left"]) == ([15, 585 - 90, 1.1], [15 + 451.5, 585, 49])
    assert _bounds(by_name["right"]) == ([15, 15, 1.1], [15 + 451.5, 15 + 90, 49])
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
def test_runners_leave_room_for_the_drawer_box(model: SlideModel):
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
    with (module("cab", box, front=box.front) if front else module("cab", box)) as cab:
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
    assert _bounds(left)[1][1] == 585                       # the drawer's left is +y, facing +x
