import pytest

from lang import *
from lang.core.layout import build_layout
from lang.core.ops import Hole
from lang.core.scope import registry
from lang.hardware.slides import INNER_FACE_OFFSET, SIDE_LIFT, DrawerSlide
from lib.drawer_slides import DYNAPRO_40, MOVENTO_760H


@pytest.fixture(autouse=True)
def fresh_registry():
    registry.reset()
    yield
    registry.reset()


ply15 = material("birch", t=15)
ply12 = material("birch", t=12)


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
    assert box.bottom.value == bay.bottom.value + SIDE_LIFT and box.height == 150


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
    assert runners["axes"] == {"x": "+y", "y": "+x", "z": "+z"}      # model x toward the right, y to the back
    # 4 behind the face's back, on the left side's inner face, the screw row 38 above the bay bottom (0 here)
    assert runners["origin"] == pytest.approx([15 + 4, 15, 38 - 35.9])
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
    assert bounds["Body1"][0][1] == 15.0 and bounds["Body1"][1][1] == pytest.approx(72.1)   # on the left side
    assert bounds["Body2"][1][1] == 585.0 and bounds["Body2"][0][1] == pytest.approx(527.9)  # on the right side
    assert bounds["Body1"][0][0] == pytest.approx(19 - 2.6) and bounds["Body1"][1][0] == pytest.approx(19 + 447.5)
    assert bounds["Body1"][0][2] == pytest.approx(2.1 - 1.0)
