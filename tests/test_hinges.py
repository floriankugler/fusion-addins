"""Concealed hinges as hardware: the holes the concealed_hinge_native add-in
drills, at the positions its code computes, and the hinges as boxes.

The add-in, from the selected door edge and carcass edge (main.py):

- hinge centres on the carcass edge's line, End Margin in from the door
  edge's ends (`_hinge_positions`);
- door holes at the hinge centres +-16 along the edge, in a row
  -n.(door edge start - carcass edge start) + 27 (+0) or 30 (+3) from the
  door edge, n pointing from the door edge into the door's face
  (`_door_hole_centers`): 27 or 30 from the carcass board's face;
- carcass holes in a row 38.5 - gap from the carcass edge, the gap being
  how far the door's inner face lies in front of the carcass edge
  (`_carcass_hole_centers`): 38.5 behind the door's inner face.

The numbers below are worked out from those formulas by hand."""
from pathlib import Path
from typing import Any, get_args

import pytest

from lang import *
from lang.build import run_build
from lang.core.layout import build_layout
from lang.core.ops import Hole
from lang.core.scope import registry
from lang.emit.plan import FaceRef, HoleStep, plan_layout
from lang.hardware.hinges import HINGE_SHAPES, ConcealedHinge, HingeModel
from lib import concealed_hinges
from helpers import ply12, ply15, ply9

BOX = Box.from_size(width=500, depth=350, height=700)


def _holes(part: Board) -> list[tuple[str | None, str, float, float, float, float]]:
    return [(op.name, op.face, op.u, op.v, op.d, op.depth) for op in part.ops if isinstance(op, Hole)]


def _overlay(hinge: ConcealedHinge, front: bool = False, gap: float = 0.0,
             hinged_on_y0: bool = True) -> tuple[Scope, Board, Board, Board]:
    """A 500 wide, 350 deep, 700 high carcass behind a 12 mm overlay door
    that covers it but for 1.5 mm all round, `gap` in front of it; in the
    van's terms (front -x at x = 0, left -y at y = 0, height up z) or in a
    cabinet opening the same way, whose left is +y. The door is hinged on
    the side at y 0..15 (the module's left in the van's terms, its right
    in the cabinet's), or the one at y 485..500. Returns the scope, the
    door, the side it is hinged on and the other side."""
    with (cabinet("cab", BOX, front=BOX.front) if front else module("cab", BOX)) as cab:
        behind = cab.front.into(12 + gap)
        low, high = (cab.right, cab.left) if front else (cab.left, cab.right)
        near = board("near", ply15).on(low).between(behind)
        far = board("far", ply15).on(high).between(behind)
        door = board("door", ply12).on(cab.front).inset(1.5)
        hinged, other = (near, far) if hinged_on_y0 else (far, near)
        cab.mount(hinge, door=door, carcass=hinged)
    return cab, door, hinged, other


# -- positions -------------------------------------------------------------------------------

def test_holes_lie_where_the_add_in_puts_them():
    """Door x 0..12, y 1.5..498.5, z 1.5..698.5; side y 0..15 from x 12.
    Hinges 60 in from the door edge's ends: z 61.5 and 638.5. Door holes in
    its back face (x 12), -(1.5 - 15) + 27 = 40.5 from its edge at y 1.5,
    so y 42; carcass holes in the side's inner face (y 15), 38.5 - 0 behind
    the carcass edge at x 12, so x 50.5. 10 x 5 in the door, 1/8 inch x 3
    in the side."""
    _, door, side, other = _overlay(ConcealedHinge())
    zs = [45.5, 77.5, 622.5, 654.5]
    names = ["1a", "1b", "2a", "2b"]
    assert _holes(door) == [(f"hinge_near_{n}", "back", 42.0, z, 10.0, 5.0) for n, z in zip(names, zs)]
    assert _holes(side) == [(f"hinge_door_{n}", "right", 50.5, z, 25.4 / 8, 3.0) for n, z in zip(names, zs)]
    assert _holes(other) == []
    assert ConcealedHinge().stations(door, side) == [Pos("z", 61.5), Pos("z", 638.5)]


def test_the_door_rows_follow_the_carcass_face_and_the_carcass_rows_the_door():
    """With the door 2 mm in front of the carcass (carcass from x 14) the
    add-in's gap is 2: the carcass row 38.5 - 2 behind the carcass edge, so
    still x 50.5, 38.5 behind the door's back face. +3 puts the door row 30
    from the side's face. On the side at y 485..500: n points -y, the door
    row at y 485 - 27."""
    _, door, side, _ = _overlay(ConcealedHinge("Blum CLIP top 110 Thin +3"), gap=2)
    assert {(u, face) for _, face, u, *_ in _holes(side)} == {(50.5, "right")}
    assert {u for _, _, u, *_ in _holes(door)} == {45.0}
    registry.reset()
    _, door, side, _ = _overlay(ConcealedHinge(), hinged_on_y0=False)
    assert {u for _, _, u, *_ in _holes(door)} == {458.0}
    assert {(u, face) for _, face, u, *_ in _holes(side)} == {(50.5, "left")}
    assert [name for name, *_ in _holes(door)][:2] == ["hinge_far_1a", "hinge_far_1b"]


def test_an_inset_door():
    """A door between the sides, 2 mm from each, flush with their fronts:
    its edge at y 17 lies 2 past the side's face, so the door row is
    -(17 - 15) + 27 = 25 from it, y 42 again; its back face is 12 behind
    the carcass edge (gap -12), so the carcass row is 38.5 + 12 = 50.5
    behind the side's front edge at x 0."""
    with module("cab", BOX) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        door = board("door", ply12).on(cab.front).between(left.gap(2), right.gap(2), cab.bottom + 2, cab.top - 2)
        cab.mount(ConcealedHinge(), door=door, carcass=left)
    assert {(u, face) for _, face, u, *_ in _holes(door)} == {(42.0, "back")}
    assert {(u, face) for _, face, u, *_ in _holes(left)} == {(50.5, "right")}
    assert sorted({v for *_, v, _, _ in _holes(left)}) == [46.0, 78.0, 622.0, 654.0]   # door z 2..698


def test_count_spreads_hinges_evenly_between_the_margins():
    """The add-in makes two; more go evenly between the outer two."""
    _, door, side, _ = _overlay(ConcealedHinge(end=100, count=3))
    stations = [100 + 1.5, 350.0, 698.5 - 100]
    assert sorted({v for *_, v, _, _ in _holes(door)}) == sorted(s + d for s in stations for d in (-16, 16))
    assert [name for name, *_ in _holes(side)] == [f"hinge_door_{i}{c}" for i in (1, 2, 3) for c in "ab"]


def test_a_flap_hinged_on_the_top_numbers_its_hinges_from_its_own_left():
    """Hinged on the top's underside (z 685): the door row 27 below it, at z
    658, the edge along y. Seen from in front of the door (from -x) its left
    is +y, the cabinet's left, so hinge 1 is the one at y 498.5 - 60 and
    its hole a the one nearer the door's left end."""
    with cabinet("cab", BOX, front=BOX.front) as cab:
        behind = cab.front.into(12)
        left = board("left", ply15).on(cab.left).between(behind)
        right = board("right", ply15).on(cab.right).between(behind)
        top = board("top", ply15).on(cab.top).between(left, right, behind)
        flap = board("flap", ply12).on(cab.front).inset(1.5)
        cab.mount(ConcealedHinge(), door=flap, carcass=top)
    ys = [454.5, 422.5, 77.5, 45.5]
    names = ["1a", "1b", "2a", "2b"]
    assert _holes(flap) == [(f"hinge_top_{n}", "back", y, 658.0, 10.0, 5.0) for n, y in zip(names, ys)]
    assert _holes(top) == [(f"hinge_flap_{n}", "bottom", 50.5, y, 25.4 / 8, 3.0) for n, y in zip(names, ys)]


def test_two_doors_on_a_partition_take_its_two_faces():
    """A partition at y 242.5..257.5 between two doors, each in a scope of
    its own and named alike: each door's holes 27 from the partition's
    face toward it, the plates' holes on that face, and the hinge items
    named apart in the cabinet."""
    with cabinet("cab", BOX, front=BOX.front) as cab:
        behind = cab.front.into(12)
        wall = board("wall", ply15).center(cab.center("width")).between(behind)
        doors: list[Board] = []
        for name, limits in (("one", (cab.right, cab.center("width") - 1.5)),
                             ("two", (cab.center("width") + 1.5, cab.left))):
            with scope(name):
                doors.append(board("door", ply12).on(cab.front).between(*limits))
        for door in doors:
            cab.mount(ConcealedHinge(), door=door, carcass=wall)
    one, two = doors
    assert {(h[1], h[2]) for h in _holes(one)} == {("back", 242.5 - 27)}
    assert {(h[1], h[2]) for h in _holes(two)} == {("back", 257.5 + 27)}
    holes = _holes(wall)
    assert [(name, face) for name, face, *_ in holes] == (
        [(f"hinge_door_{n}", "left") for n in ("1a", "1b", "2a", "2b")]
        + [(f"hinge_door_{n}_2", "right") for n in ("1a", "1b", "2a", "2b")])
    assert [item["name"] for item in cab.hardware] == ["door_hinges", "door_hinges_2"]


# -- frames ---------------------------------------------------------------------------------

def _result(front: bool) -> tuple[Any, ...]:
    registry.reset()
    cab, door, side, other = _overlay(ConcealedHinge(), front=front)
    return _holes(door), _holes(side), _holes(other), cab.hardware


def test_a_cabinet_and_a_module_in_the_vans_terms_hinge_a_door_alike():
    """The same door on the same physical side, once in a module in the
    van's terms and once in a cabinet with front=: the same holes, names
    and hinge bodies, numbered from the bottom in both."""
    plain, cabinet = _result(front=False), _result(front=True)
    assert plain == cabinet
    assert [b["name"] for b in plain[3][0]["bodies"]] == ["hinge_1", "hinge_2"]


def test_hinges_on_the_cabinetmakers_left_or_right():
    """In a cabinet opening toward -x, the cabinetmaker's left is +y: hinged
    on the left side the door's holes lie near its left edge, on the right
    side near its right edge, each in the side's inner face."""
    def build(on: str) -> tuple[Board, Board]:
        registry.reset()
        with cabinet("cab", BOX, front=BOX.front) as cab:
            behind = cab.front.into(12)
            left = board("left", ply15).on(cab.left).between(behind)
            right = board("right", ply15).on(cab.right).between(behind)
            door = board("door", ply12).on(cab.front).inset(1.5)
            side = left if on == "left" else right
            cab.mount(ConcealedHinge(), door=door, carcass=side)
        return door, side
    door, side = build("left")
    assert side.box().lo["y"] == 485 and {h[2] for h in _holes(door)} == {485 - 27.0}
    assert {h[1] for h in _holes(side)} == {side.inner.world_name}
    assert door.left.value == 498.5                            # the cabinet's left is +y
    door, side = build("right")
    assert side.box().hi["y"] == 15 and {h[2] for h in _holes(door)} == {15 + 27.0}
    assert {h[1] for h in _holes(side)} == {side.inner.world_name}


# -- the hinges as boxes ------------------------------------------------------------------------

def _box(b: Any) -> Box:
    return Box(dict(zip("xyz", b["min"])), dict(zip("xyz", b["max"])))  # type: ignore[arg-type]


@pytest.mark.parametrize("model", list(HINGE_SHAPES))
def test_hinges_are_placed_as_boxes_from_the_door_and_the_side(model: HingeModel):
    """Per hinge a body of the model's boxes (cup, arm, clip, plate), each
    measured across from the side's face (y 15, toward +y), back from the
    door's back face (x 12, toward +x) and along the edge from the hinge's
    centre (z 61.5 and 638.5). The boxes join, so a hinge is one body, and
    they touch the door and the side without reaching into them."""
    cab, door, side, _ = _overlay(ConcealedHinge(model))
    (item,) = cab.hardware
    assert item["path"] == "cab.door_hinges" and item["name"] == "door_hinges"
    assert [b["name"] for b in item["bodies"]] == ["hinge_1", "hinge_2"]
    shape = HINGE_SHAPES[model].boxes()
    assert list(shape) == ["cup", "arm", "clip", "plate"]
    for body, z in zip(item["bodies"], (61.5, 638.5)):
        assert body["boxes"] == [{"min": [12 + back[0], 15 + across[0], z + along[0]],
                                  "max": [12 + back[1], 15 + across[1], z + along[1]]}
                                 for across, back, along in shape.values()]
        boxes = [_box(b) for b in body["boxes"]]
        joined = {0}
        for _ in boxes:
            joined |= {j for j, b in enumerate(boxes) if any(b.overlaps(boxes[i]) for i in joined)}
        assert joined == set(range(len(boxes)))
        assert not any(b.overlaps(door.box()) or b.overlaps(side.box()) for b in boxes)
    assert build_layout()["modules"][0]["hardware"] == [item]


def _example(tmp_path: Path) -> Any:
    example = Path(__file__).resolve().parent.parent / "examples" / "hinged_door.py"
    return run_build(example, tmp_path, scene=False)


def test_the_example_builds_and_its_hinges_clear_every_part(tmp_path: Path):
    layout = _example(tmp_path)
    (module_,) = layout["modules"]
    assert layout["problems"] == [] and module_["problems"] == []
    (item,) = module_["hardware"]
    parts = {p["path"]: p for p in module_["parts"]}
    for body in item["bodies"]:
        for b in body["boxes"]:
            for path, part in parts.items():
                assert not _box(b).overlaps(_box(part["box"])), (body["name"], path)


def test_the_example_plans_its_hinge_holes_and_bodies(tmp_path: Path):
    """The cabinet opens toward +y, so its left side lies at x 435..450 and
    the door at y 338..350: the door holes at x 435 - 27 in the door's back
    face (y 338), the carcass holes 38.5 behind it (y 299.5) in the side's
    inner face (x 435), 61.5 and 538.5 up the 597 mm door."""
    plan = plan_layout(_example(tmp_path))
    assert plan.problems == []
    door = next(p for p in plan.parts if p.path == "hingecab.door")
    (cups,) = door.steps
    assert isinstance(cups, HoleStep) and (cups.d, cups.depth) == (10.0, 5.0)
    assert cups.face == FaceRef("y", -1, 338.0)
    assert cups.points == [(408.0, 338.0, z) for z in (45.5, 77.5, 522.5, 554.5)]
    left = next(p for p in plan.parts if p.path == "hingecab.left")
    (predrill,) = [s for s in left.steps if isinstance(s, HoleStep) and s.d == 25.4 / 8]
    assert predrill.depth == 3.0 and predrill.face == FaceRef("x", -1, 435.0)
    assert predrill.points == [(435.0, 299.5, z) for z in (45.5, 77.5, 522.5, 554.5)]
    (hinges,) = plan.hardware
    assert hinges.path == "hingecab.door_hinges" and hinges.component == ("hingecab",)
    assert [b.name for b in hinges.bodies] == ["hinge_1", "hinge_2"] and all(len(b.boxes) == 4 for b in hinges.bodies)


def test_preview_draws_each_hinge_as_one_body():
    """Each hinge meshes as the union of its boxes, one closed volume as
    large as their bounds."""
    from lang.preview.mesh import build_scene
    cab, *_ = _overlay(ConcealedHinge())
    first = cab.hardware[0]["bodies"][0]["boxes"]
    bounds = [[min(b["min"][i] for b in first) for i in range(3)], [max(b["max"][i] for b in first) for i in range(3)]]
    scene = build_scene(build_layout())
    meshes: dict[str, Any] = {}
    for node in scene.graph.nodes_geometry:
        if "door_hinges" in node:
            transform, geometry = scene.graph[node]
            mesh = scene.geometry[geometry].copy()
            mesh.apply_transform(transform)
            meshes[node.rsplit(".", 1)[1]] = mesh
    assert set(meshes) == {"hinge_1", "hinge_2"}
    assert meshes["hinge_1"].is_volume and meshes["hinge_1"].body_count == 1
    assert meshes["hinge_1"].bounds.round(3).tolist() == bounds


# -- what it refuses ------------------------------------------------------------------------------

def test_the_model_names_are_the_add_ins():
    assert list(get_args(HingeModel)) == list(concealed_hinges.HINGE_MODELS) == list(HINGE_SHAPES)
    assert ConcealedHinge().name == "Blum CLIP top 110 Thin +0" and ConcealedHinge().door_row == 27
    assert ConcealedHinge("Blum CLIP top 110 Thin +3").door_row == 30


@pytest.mark.parametrize("make, message", [
    (lambda: ConcealedHinge("Blum CLIP top 110 Thin +6"), "ConcealedHinge(): expected 'Blum CLIP top 110 Thin +0'"),  # type: ignore[arg-type]
    (lambda: ConcealedHinge(end=26.9), "end= must be at least 27 mm, not 26.9 mm."),
    (lambda: ConcealedHinge(count=1), "a door takes at least two hinges, not 1."),
    (lambda: ConcealedHinge(pilot=(0.0, 3.0)), "the pilot diameter must be at least 0.1 mm"),
    (lambda: ConcealedHinge(pilot=(3.0, 0.05)), "the pilot depth must be at least 0.1 mm"),
])
def test_settings_the_add_ins_dialog_refuses(make: Any, message: str):
    with pytest.raises(LangError) as error:
        make()
    assert message in str(error.value)


#: Doors and carcass boards the add-in refuses to hinge, built in the
#: module `cab` (BOX in the van's terms, its left side 15 thick behind a
#: 12 mm door), and the reason it gives.
REFUSED: list[tuple[str, str]] = [
    # the door's edge must leave room for end=, then for two hinges more than 42 apart (and 56.2, below)
    ("short door", "the door's hinged edge (120 mm) is too short for hinges 60 mm from its ends."),
    ("door for one hinge", "too short for 2 hinges at least 56.2 mm apart"),
    # the door holes must land on the door, the carcass holes on the carcass board
    ("narrow door", "the door hole (10 mm) does not fit on cab.door's back face"),
    ("shallow carcass", "the pilot hole (3.2 mm) does not fit on cab.strip's left face"),
    # a cup's rim off the door: its centre 27 from the side's face, on a door 31 wide
    ("cup rim off the door", "the door hole (10 mm) does not fit on cab.door's back face"),
    # a cup over a hole drilled before, its centre clear of it
    ("cup over a hole", "the door hole (10 mm) does not fit on cab.door's back face"),
    # the carcass pilots as deep as the side is thick
    ("deep pilots", "the pilot depth (15 mm) must be less than cab.left's thickness (15 mm)."),
    # two boards, standing square to each other
    ("one board", "two different boards"),
    ("parallel boards", "lie in parallel planes"),
]


@pytest.mark.parametrize("case, message", REFUSED)
def test_mounting_refuses_what_the_add_in_refuses(case: str, message: str):
    hinge = ConcealedHinge()
    with module("cab", BOX) as cab:
        behind = cab.front.into(12)
        left = board("left", ply15).on(cab.left).between(behind)
        carcass = left
        if case == "short door":
            door = board("door", ply12).on(cab.front).between(cab.bottom, cab.bottom + 120)
        elif case == "door for one hinge":
            door = board("door", ply12).on(cab.front).between(cab.bottom, cab.bottom + 162)
        elif case == "narrow door":
            door = board("door", ply12).on(cab.front).between(cab.left, cab.left + 40)
        elif case == "cup rim off the door":
            door = board("door", ply12).on(cab.front).between(cab.left, cab.left + 46)
        elif case == "cup over a hole":
            door = board("door", ply12).on(cab.front)
            # the lowest cup at y 42, z 44 (60 - 16): a 6 mm hole 6 below its
            # centre, under its rim
            door.hole(d=6, depth=3, at=door.back.left(Pos("y", 42)).bottom(Pos("z", 38)))
        elif case == "deep pilots":
            door = board("door", ply12).on(cab.front)
            hinge = ConcealedHinge(pilot=(3, 15))
        elif case == "shallow carcass":
            door = board("door", ply12).on(cab.front)
            carcass = board("strip", ply15).on(cab.right).between(behind, behind + 30)
        elif case == "one board":
            door = left
        else:
            door = board("door", ply12).on(cab.front)
            carcass = board("back", ply9).on(cab.back)
        before = [op for op in door.ops + carcass.ops if isinstance(op, Hole)]
        with pytest.raises(LangError) as error:
            cab.mount(hinge, door=door, carcass=carcass)
    assert message in str(error.value)
    assert [op for op in door.ops + carcass.ops if isinstance(op, Hole)] == before


def test_mount_takes_a_door_and_a_carcass_board_once():
    """The keywords are `mount`'s own (typed: a misspelt or missing one is
    a TypeError, and pyright reports it, see typing_checks.py); hinging a
    door on the same board twice is refused."""
    hinge = ConcealedHinge()
    with module("cab", BOX) as cab:
        left = board("left", ply15).on(cab.left).between(cab.front.into(12))
        door = board("door", ply12).on(cab.front)
        with pytest.raises(TypeError, match="carcass"):
            cab.mount(hinge, door=door)  # type: ignore[call-arg]
        with pytest.raises(TypeError, match="side"):
            cab.mount(hinge, door=door, carcass=left, side=left)  # type: ignore[call-arg]
        cab.mount(hinge, door=door, carcass=left)
        before = (list(door.ops), list(left.ops))
        with pytest.raises(LangError, match="cab.door is hinged on cab.left already"):
            cab.mount(hinge, door=door, carcass=left)
        assert (door.ops, left.ops) == before                   # a refused mount changes nothing


# -- the vocabulary of the review (findings 26, 31, 44) -----------------------------------------------------

def test_carcass_takes_a_face_like_the_latches():
    """`carcass=` takes the face the mounting plates go on, as a latch's
    does: needed where the door's middle lies within the carcass board's
    thickness, such as a door centred on a partition."""
    with cabinet("cab", BOX, front=BOX.front) as cab:
        behind = cab.front.into(12)
        wall = board("wall", ply15).center(cab.center("width")).between(behind)
        door = board("door", ply12).on(cab.front).between(cab.center("width") - 100, cab.center("width") + 100)
        with pytest.raises(LangError, match=r"the middle of cab\.door lies within cab\.wall's thickness; name the "
                                            r"face the mounting plates go on, carcass=wall\.right or wall\.left"):
            cab.mount(ConcealedHinge(), door=door, carcass=wall)
        with pytest.raises(LangError, match="narrow face"):
            cab.mount(ConcealedHinge(), door=door, carcass=wall.front)
        cab.mount(ConcealedHinge(), door=door, carcass=wall.left)
    # the wall's left face (+y in a cabinet facing -x) at y 257.5, the door row 27 from it
    assert {(h[1], h[2]) for h in _holes(wall)} == {("right", 50.5)}
    assert {h[2] for h in _holes(door)} == {257.5 + 27}
    registry.reset()
    with module("cab", BOX) as cab:
        left = board("left", ply15).on(cab.left).between(cab.front.into(12))
        door = board("door", ply12).on(cab.front)
        with pytest.raises(LangError, match=r"cab\.door lies behind cab\.left's left face"):
            cab.mount(ConcealedHinge(), door=door, carcass=left.left)      # the outer face, away from the door
        cab.mount(ConcealedHinge(), door=door, carcass=left.right)
    assert {(h[1], h[2]) for h in _holes(left)} == {("right", 50.5)}      # as with carcass=left


def test_settings_are_spelt_as_elsewhere():
    """`end=` as for connectors, latches, catches and brackets (it was
    `margin=`), `pilot=` for the pre-drill (it was `predrill=`), `count`
    keyword-only."""
    hinge = ConcealedHinge(count=3, end=80, pilot=(3, 4))
    assert (hinge.count, hinge.end, hinge.pilot) == (3, 80.0, (3.0, 4.0))
    with pytest.raises(TypeError):
        ConcealedHinge(margin=60)  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        ConcealedHinge(predrill=(3, 3))  # type: ignore[call-arg]


def test_the_plus_3_hinge_stands_on_the_plate_the_lib_says():
    """The +3 model's boxes are the +0 model's raised by the difference of
    their door rows in lib.concealed_hinges (3), not a number of its own."""
    raised = concealed_hinges.CLIP_TOP_THIN_3.door_row - concealed_hinges.CLIP_TOP_THIN_0.door_row
    assert raised == 3
    assert HINGE_SHAPES["Blum CLIP top 110 Thin +3"] == HINGE_SHAPES["Blum CLIP top 110 Thin +0"].raised(raised)
    assert HINGE_SHAPES["Blum CLIP top 110 Thin +3"].plate[0] == (0.0, 11.5)


def test_hinges_closer_than_their_plates_are_long_are_refused():
    """Found by fuzzing: hinges 42 to 56.2 mm apart pass the add-in's rule,
    whose hole pairs then just clear each other, but their mounting plates,
    56.2 long, meet; the layout check reported it. Refused [Florian,
    2026-10-13]: 50 apart is refused, 56.2 apart fits."""
    for height, fits in ((170, False), (176.2, True)):       # 60 from the ends: 50 and 56.2 apart
        registry.reset()
        with module("cab", BOX) as cab:
            side = board("side", ply15).on(cab.left).between(cab.front.into(12))
            door = board("door", ply12).on(cab.front).between(cab.bottom, cab.bottom + height)
            if fits:
                cab.mount(ConcealedHinge(), door=door, carcass=side)
                assert build_layout()["problems"] == []
                continue
            with pytest.raises(LangError, match=r"^cab\.door: Blum CLIP top 110 Thin \+0: the door's hinged edge "
                                                r"\(170 mm\) is too short for 2 hinges at least 56\.2 mm apart, 60 mm "
                                                r"from its ends: their mounting plates would meet\.$"):
                cab.mount(ConcealedHinge(), door=door, carcass=side)
            assert door.ops == [] and side.ops == [] and cab.hardware == []
