import pytest

from lang import *
from lang.core.layout import build_layout
from lang.core.ops import Cut, Hole
from lang.core.layout_types import HardwareLayout
from lang.core.scope import registry
from lang.hardware.slides import BOTTOM_HEIGHT, INNER_FACE_OFFSET, DrawerSlide
from lib.drawer_slides import DYNAPRO_40, MOVENTO_760H


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
    assert slide.side_lift == BOTTOM_HEIGHT - 11.5 == 16.5
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
    assert DrawerSlide(DYNAPRO_40, nl=450, hook_predrill=(3, 10)).hook_predrill == (3, 10)
    with pytest.raises(LangError):   # no Blum data yet
        DrawerSlide(MOVENTO_760H, nl=500).machine_box(sides=(l, r), front=f, back=k, floor=floor)


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
    # the runner pair's model, placed from the left side's inner face
    (runners,) = d.hardware
    assert runners["path"] == "cab.drawer1.runners" and runners["model"].endswith("433.19.608.stp")
    # the module is in the van's terms (no front=), so the drawer's left, seen
    # standing in front of it, is the module's right side, at y 585..600:
    # model x toward the drawer's right (-y), y to the back, z up
    assert runners["axes"] == {"x": "-y", "y": "+x", "z": "+z"}
    # 4 behind the face's back, on the left runner's side's inner face, the screw row 38 above the bay bottom (0 here)
    assert runners["origin"] == pytest.approx([15 + 4, 585, 38 - 35.9])
    assert runners["bodies"][0]["offset"] == [0, 0, 0]
    assert runners["bodies"][1]["offset"] == [570 - 400, 0, 0]       # the right runner at the right side
    layout = build_layout()
    assert layout["modules"][0]["hardware"] == [runners]


def test_preview_places_the_runner_meshes():
    """The preview takes the runners from the glTF file: each runner's mesh
    lies against its carcass side, the right one moved by the inner width
    less the file's pair distance."""
    from lang.preview.mesh import build_scene
    slide = DrawerSlide(DYNAPRO_40, nl=450)
    with module("cab", Box.from_size(width=600, depth=500, height=300)) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        bay = cab.interior
        with scope("drawer1", bay) as d:
            face = board("face", ply15).on(bay.front)
        d.mount(slide, sides=(left, right), front=face.back)
    scene = build_scene(build_layout())
    bounds = {}
    for node in scene.graph.nodes_geometry:
        if "runners" in node:
            transform, geometry = scene.graph[node]
            mesh = scene.geometry[geometry].copy()
            mesh.apply_transform(transform)
            bounds[node.rsplit(".", 1)[1]] = mesh.bounds.round(1).tolist()
            assert len(mesh.faces) > 1000     # the real model, not an envelope box
    # the left-hand runner on the drawer's left, seen from its front (+y here), the right-hand one on its right
    assert bounds["Body1"][1][1] == 585.0 and bounds["Body1"][0][1] == pytest.approx(527.9)
    assert bounds["Body2"][0][1] == 15.0 and bounds["Body2"][1][1] == pytest.approx(72.1)
    assert bounds["Body1"][0][0] == pytest.approx(19 - 2.6) and bounds["Body1"][1][0] == pytest.approx(19 + 447.5)
    assert bounds["Body1"][0][2] == pytest.approx(2.1 - 1.0)


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


def test_runners_are_rotated_never_mirrored_whatever_the_frame():
    """A left-hand and a right-hand runner, placed by the drawer's own left
    and right: the same in a module in the van's terms, whose left is the
    drawer's right, as in a cabinet. The model's axes form a rotation."""
    import numpy as np
    plain, cabinet = _runners(front=False), _runners(front=True)
    assert plain["axes"] == cabinet["axes"] and plain["origin"] == pytest.approx(cabinet["origin"])
    axes = plain["axes"]
    m = np.array([[(1 if code[0] == "+" else -1) * (code[1] == a) for a in "xyz"] for code in
                  (axes["x"], axes["y"], axes["z"])])
    assert round(float(np.linalg.det(m))) == 1
