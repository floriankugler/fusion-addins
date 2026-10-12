"""Door latches (lang/hardware/latches.py) against the door_latch_native
add-in: the expected positions are worked out by hand the way the add-in
works them out (main.py: `_door_hole_groups` and `_carcass_holes`), from
the door edge on the door's inner face and the carcass face's front edge.

The cabinet is 600 wide, 500 deep and 720 high. In the van's terms (no
front=) its front is at x 0 (front is -x), its left side at y 0..15 (left
is -y), the top board at z 705..720; an inset door fills the opening
between the sides, the bottom and the top less 2 mm all round: x 0..15,
y 17..583, z 17..703."""
from pathlib import Path
from typing import get_args

import pytest

from lang import *
from lang.build import run_build
from lang.core.checks import _box_hits  # type: ignore[reportPrivateUsage]
from lang.core.directions import AXES
from lang.core.layout import build_layout
from lang.core.layout_types import HardwareLayout
from lang.core.ops import Hole, Pocket
from lang.core.scope import registry
from lang.emit.plan import HoleStep, PocketStep, plan_layout
from lang.hardware.latches import LATCH_SHAPES, DoorLatch, LatchModel
from lib import door_latches
from helpers import ply15


PREDRILL = 25.4 / 8


def _carcass(cab: Scope) -> dict[str, Board]:
    left = board("left", ply15).on(cab.left)
    right = board("right", ply15).on(cab.right)
    top = board("top", ply15).on(cab.top).between(left, right)
    bottom = board("bottom", ply15).on(cab.bottom).between(left, right)
    return {"left": left, "right": right, "top": top, "bottom": bottom}


def _inset_door(latch: DoorLatch | None = None, carcass: str = "top", front: bool = False,
                thickness: float = 15) -> tuple[Scope, dict[str, Board]]:
    box = Box.from_size(width=600, depth=500, height=720)
    with (cabinet("cab", box, front=box.front) if front else module("cab", box)) as cab:
        parts = _carcass(cab)
        door = board("door", material("birch", t=thickness)).on(cab.front).between(
            parts["left"], parts["right"], parts["bottom"], parts["top"]).inset(2)
        parts["door"] = door
        if latch is not None:
            cab.mount(latch, door=door, carcass=parts[carcass])
    return cab, parts


def _holes(part: Board) -> dict[str, tuple[float, float, float, str, float, bool]]:
    return {op.name or "": (op.u, op.v, op.d, op.face, op.depth, op.through) for op in part.ops if isinstance(op, Hole)}


def _pockets(part: Board) -> dict[str, Pocket]:
    return {op.name or "": op for op in part.ops if isinstance(op, Pocket)}


def test_the_latch_names_are_the_libs():
    assert set(get_args(LatchModel)) == set(door_latches.LATCHES) == set(LATCH_SHAPES)


def test_pull_lock_on_an_inset_door():
    """The add-in: the door edge (15, 17..583, 703), the carcass edge (0,
    15..585, 705). distance = -(0, 0, -1).((15, 17, 703) - (0, 15, 705)) =
    -2, so the hole lies 34 - 2 = 32 below the door edge, at z 671, 34 below
    the carcass face; gap = (1, 0, 0).((0, 15, 705) - (15, 300, 703)) = -15,
    and the keeper's pair lies 29 behind the door's front face (x 0), as the
    lock's drawing measures it from the bezel: 29 - 15 = 14 behind its inner
    face, 14 + 15 = 29 behind the carcass edge. One latch: the middle of the
    edge, y 300."""
    _, parts = _inset_door(DoorLatch("Pull Lock 44"))
    door, top = parts["door"], parts["top"]
    # the door's inner face is its back (+x); u, v are y, z
    assert _holes(door) == {"pull_lock_top_1": (300, 671, 38.1, "back", 15, True)}
    counterbore = _pockets(door)["pull_lock_top_1_counterbore"]
    assert (counterbore.face, counterbore.depth, counterbore.depth_spec) == ("back", 5, "to(front, -10)")
    assert counterbore.shape.bounds == pytest.approx((276, 647, 324, 695))
    assert [type(op) for op in door.ops] == [Hole, Pocket]          # the hole first, as in the add-in
    # the strike's pair in the top's underside, the door's own left (+y) first; u, v are x, y
    assert _holes(top) == {"pull_lock_door_1a": (29, 309.5, PREDRILL, "bottom", 3, False),
                           "pull_lock_door_1b": (29, 290.5, PREDRILL, "bottom", 3, False)}


def test_pull_lock_counterbore_only_on_a_door_thicker_than_the_remaining_material():
    _, parts = _inset_door(DoorLatch("Pull Lock 44"), thickness=10)
    assert _pockets(parts["door"]) == {} and list(_holes(parts["door"])) == ["pull_lock_top_1"]
    registry.reset()
    _, parts = _inset_door(DoorLatch("Pull Lock 44"), thickness=12)
    assert _pockets(parts["door"])["pull_lock_top_1_counterbore"].depth == 2


def test_everlock_on_an_overlay_drawer_face():
    """A drawer face in front of the carcass (x -15..0) whose top covers
    the top board's front edge (z 718). The add-in: distance = -(0, 0,
    -1).((0, 2, 718) - (0, 15, 705)) = 13, so the holes lie 13 + inset below
    the face's edge, i.e. inset below the carcass face at z 705: the pilot
    rows at 679 and 663, 26 to either side; the finger hole at 675. gap =
    (1, 0, 0).((0, 15, 705) - (0, 300, 718)) = 0: the strike's pair 25
    behind the carcass edge, 14 to either side."""
    box = Box.from_size(width=600, depth=500, height=720)
    with module("cab", box) as cab:
        parts = _carcass(cab)
        with scope("drawer1", cab.interior) as d:
            face = (board("face", ply15).on(cab.front.gap(15), toward=cab.back)
                    .between(cab.left.into(2), cab.right.into(2), cab.bottom.into(500), cab.top.into(2)))
        d.mount(DoorLatch("Everlock"), door=face, carcass=parts["top"])
    pilot = (PREDRILL, "back", 3, False)
    # a and b nearer the carcass face, from the face's own left (+y)
    assert _holes(face) == {"everlock_top_1a": (326, 679, *pilot), "everlock_top_1b": (274, 679, *pilot),
                            "everlock_top_1c": (326, 663, *pilot), "everlock_top_1d": (274, 663, *pilot),
                            "everlock_top_1": (300, 675, 25, "back", 15, True)}
    assert _holes(parts["top"]) == {"everlock_face_1a": (25, 314, PREDRILL, "bottom", 3, False),
                                    "everlock_face_1b": (25, 286, PREDRILL, "bottom", 3, False)}
    # the boxes go into the drawer's scope, named by the face
    assert [h["path"] for h in d.hardware] == ["cab.drawer1.face_latches"]


def test_ll66_beside_the_cabinetmakers_right_and_left():
    """In a cabinet (front=box.front: the front -x, its left +y), a door
    latched beside a side: the edge is upright, x 15 and y 17 (the right
    side's inner face at y 15) or y 583 (the left's at y 585), z 17..703,
    one latch in its middle at z 360. The add-in: the normal into the door
    face from its right edge is +y, distance = -(0, 1, 0).((15, 17, z) -
    (0, 15, z)) = -2, so the pilots lie 10 - 2 = 8 inside the door's edge,
    10 from the side, 28 above and below; the counter plate's pair 24
    behind the door's inner face (x 39), 10 above and below. Numbered from
    the bottom."""
    pilot = (PREDRILL, "back", 3, False)
    for which, side_face, y in (("right", 15, 25), ("left", 585, 575)):
        registry.reset()
        cab, parts = _inset_door(DoorLatch("LL-66"), carcass=which, front=True)
        side = parts[which]
        assert side.box().lo["y"] == (0 if which == "right" else 585)      # the cabinetmaker's right is -y
        assert _holes(parts["door"]) == {f"ll66_{which}_1a": (y, 332, *pilot), f"ll66_{which}_1b": (y, 388, *pilot)}
        inward = "right" if which == "right" else "left"                     # world names: +y is right
        assert _holes(side) == {"ll66_door_1a": (39, 350, PREDRILL, inward, 3, False),
                                "ll66_door_1b": (39, 370, PREDRILL, inward, 3, False)}
        assert side.inner.world_name == inward and side.inner.value == side_face
        (latch,) = cab.hardware[0]["bodies"]
        assert latch["name"] == "latch_1"
        plate = latch["boxes"][-1]                                          # the counter plate, last
        assert side_face in (plate["min"][1], plate["max"][1])             # against the side
        assert all(not _holes(p) for name, p in parts.items() if name not in ("door", which))


def test_several_latches_from_the_ends_numbered_from_the_doors_left():
    """Three latches 80 from the ends of the 566 long edge: y 97, 300 and
    503, numbered from the door's own left, +y in the van's terms."""
    _, parts = _inset_door(DoorLatch("Pull Lock 44", count=3, end=80))
    holes = _holes(parts["door"])
    assert [holes[f"pull_lock_top_{i}"][0] for i in (1, 2, 3)] == [503, 300, 97]
    assert len(_holes(parts["top"])) == 6 and len(_pockets(parts["door"])) == 3


def _world(cab: Scope) -> tuple[dict[str, dict[str, tuple[float, float, float, str, float, bool]]],
                                list[HardwareLayout]]:
    """Every part's holes (u, v, d, world face, depth, through) and the hardware."""
    return {p.name: _holes(p) for p in cab.all_parts()}, cab.all_hardware()


def test_a_module_in_the_vans_terms_and_a_cabinet_give_the_same_latches():
    """The same construction in the van's terms and in a cabinet facing the
    same way: the same holes (layouts store world names) and the same
    boxes, named the same, since the latches are numbered from the door's
    own left whatever the frame."""
    plain, _ = _inset_door(DoorLatch("Pull Lock 44", count=2))
    plain_world = _world(plain)
    registry.reset()
    cabinet, _ = _inset_door(DoorLatch("Pull Lock 44", count=2), front=True)
    cabinet_world = _world(cabinet)
    # the sides are called left and right the other way round, nothing else differs
    swap = {"left": "right", "right": "left"}
    assert {swap.get(k, k): v for k, v in plain_world[0].items()} == cabinet_world[0]
    assert plain_world[1] == cabinet_world[1]
    assert [b["name"] for b in cabinet_world[1][0]["bodies"]] == ["latch_1", "latch_2"]


def test_the_latch_and_its_strike_as_boxes():
    """Closed, from `LATCH_SHAPES`, one body: the Pull Lock's parts measured
    from the door's front face (x 0; the door is 15 thick, its inner face at
    x 15), the bezel proud of it, the housing through the door's hole; the
    keeper under the top (z 705) behind the door."""
    cab, parts = _inset_door(DoorLatch("Pull Lock 44"))
    (item,) = cab.hardware
    assert item["path"] == "cab.door_latches"
    (body,) = item["bodies"]
    assert body["name"] == "latch_1"
    boxes = body["boxes"]
    shape = LATCH_SHAPES["Pull Lock 44"]
    assert len(boxes) == len(shape.front) + len(shape.strike_front)
    bezel, housing = boxes[0], boxes[1]
    (a0, a1), (b0, b1), (c0, c1) = shape.front[0]
    assert bezel == {"min": [c0, 300 + a0, 705 - b1], "max": [c1, 300 + a1, 705 - b0]}   # x = depth behind the front
    assert bezel["max"][0] == 0 and housing["min"][0] == 0                                  # on and from the front
    (a0, a1), (b0, b1), (c0, c1) = shape.strike_front[0]                          # also from the front
    assert boxes[len(shape.front)] == {"min": [c0, 300 + a0, 705 - b1], "max": [c1, 300 + a1, 705 - b0]}
    # the pawl reaches behind the keeper's lip, which it catches
    pawl, lip = boxes[len(shape.front) - 1], boxes[-1]
    assert pawl["max"][0] > lip["max"][0] and pawl["min"][0] <= lip["min"][0]
    assert DoorLatch("Pull Lock 44").reach == 50.9 == shape.reach       # the backing plate, not the bezel
    assert DoorLatch("Everlock").reach == 60 and DoorLatch("LL-66").reach == 24.6
    # nothing overlaps a board's material, holes and the counterbore counted out
    overlaps = {name for b in boxes for name, part in parts.items() if _overlaps(part, b["min"], b["max"])}
    assert overlaps == set()
    assert no_interference(cab) == []
    # touching the top: the keeper's leg and lip lie on its underside
    assert boxes[len(shape.front)]["max"][2] == parts["top"].box().lo["z"]


def _overlaps(part: Board, lo: list[float], hi: list[float]) -> bool:
    """Whether a world box takes some of the part's material, holes and
    pockets counted out (the check `no_interference` makes)."""
    return _box_hits(part, Box(dict(zip(AXES, lo)), dict(zip(AXES, hi))))  # type: ignore[arg-type]


def test_refused_as_the_add_in_refuses():
    with pytest.raises(LangError, match="expected"):
        DoorLatch("Pull lock 44")                          # type: ignore[arg-type]
    cases: list[tuple[LatchModel, float]] = [("Everlock", 16), ("Pull Lock 44", 19), ("LL-66", 20)]
    for model, too_large in cases:
        with pytest.raises(LangError, match="too large"):
            DoorLatch(model, pilot=(too_large, 3))
        DoorLatch(model, pilot=(too_large - 0.1, 3))
    with pytest.raises(LangError):
        DoorLatch("Everlock", count=0)
    with pytest.raises(LangError):
        DoorLatch("Everlock", count=2, end=0)
    DoorLatch("Everlock", count=1, end=0)                  # one latch: the end offset is not used
    with pytest.raises(LangError):
        DoorLatch("Everlock", pilot=(3, 0))
    with pytest.raises(TypeError):
        DoorLatch("Everlock", 2)  # type: ignore[misc]           # count is keyword-only
    with pytest.raises(LangError, match="too short"):
        _inset_door(DoorLatch("Everlock", count=2, end=283))   # 566 <= 2 x 283


def test_refuses_latches_that_do_not_fit_and_changes_nothing():
    box = Box.from_size(width=600, depth=500, height=720)
    with module("cab", box) as cab:
        parts = _carcass(cab)
        back = board("back", ply15).on(cab.back).between(parts["left"], parts["right"])
        # a door whose upper edge lies 30 below the top: the counterbore,
        # 10 to 58 below the carcass face, does not lie on it
        low = board("low", ply15).on(cab.front).between(parts["left"], parts["right"], cab.bottom.into(300),
                                                        cab.top.into(45))
        with pytest.raises(LangError, match="does not fit on cab.low's back face"):
            cab.mount(DoorLatch("Pull Lock 44"), door=low, carcass=parts["top"])
        assert low.ops == [] and parts["top"].ops == [] and cab.hardware == []
        # a door narrower than the Everlock's pilot columns
        narrow = board("narrow", ply15).on(cab.front).between(cab.left.into(100), cab.left.into(140),
                                                              cab.bottom.into(300), cab.top.into(17))
        with pytest.raises(LangError, match="does not fit on cab.narrow's back face"):
            cab.mount(DoorLatch("Everlock"), door=narrow, carcass=parts["top"])
        # the LL-66's station centre must lie on the door too: a notch between its pilots
        notched = board("notched", ply15).on(cab.front).between(cab.left.into(200), cab.left.into(400),
                                                                cab.bottom.into(300), cab.top.into(17))
        notched.cut(rect(width=40, height=20), at=notched.front.top)
        with pytest.raises(LangError, match="does not fit"):
            cab.mount(DoorLatch("LL-66"), door=notched, carcass=parts["top"])
        with pytest.raises(LangError, match="parallel"):
            cab.mount(DoorLatch("Everlock"), door=low, carcass=back)
        with pytest.raises(LangError, match="two boards"):
            cab.mount(DoorLatch("Everlock"), door=low, carcass=low)
        with pytest.raises(LangError, match="narrow face"):
            cab.mount(DoorLatch("Everlock"), door=low, carcass=parts["top"].front)
        with pytest.raises(TypeError, match="carcass"):
            cab.mount(DoorLatch("Everlock"), door=low)  # type: ignore[call-arg]
        with pytest.raises(TypeError, match="count"):
            cab.mount(DoorLatch("Everlock"), door=low, carcass=parts["top"], count=2)  # type: ignore[call-arg]
        # a shelf across the middle of a tall door: which face?
        shelf = board("shelf", ply15).center(cab.center("height")).between(parts["left"], parts["right"], back)
        tall = board("tall", ply15).on(cab.front.gap(15), toward=cab.back)
        with pytest.raises(LangError, match="across the middle"):
            cab.mount(DoorLatch("Everlock"), door=tall, carcass=shelf)
        cab.mount(DoorLatch("Everlock"), door=tall, carcass=shelf.bottom)     # named, it is clear
    assert {h[1] for h in _holes(tall).values()} == {360 - 7.5 - 26, 360 - 7.5 - 42, 360 - 7.5 - 30}


def test_layout_plan_and_preview():
    """The layout carries the holes and the boxes; the emitter's plan drills
    the lock's hole before the counterbore around it and the strike's pair
    as one hole step; the preview meshes the boxes."""
    _inset_door(DoorLatch("Pull Lock 44"))
    layout = build_layout()
    (module_layout,) = layout["modules"]
    assert [h["path"] for h in module_layout["hardware"]] == ["cab.door_latches"]
    plan = plan_layout(layout)
    assert plan.problems == []
    door = next(p for p in plan.parts if p.path == "cab.door")
    hole, counterbore = door.steps
    assert isinstance(hole, HoleStep) and isinstance(counterbore, PocketStep)
    assert (hole.points, hole.d, hole.depth) == ([(15.0, 300.0, 671.0)], 38.1, None)
    assert counterbore.depth == 5
    top = next(p for p in plan.parts if p.path == "cab.top")
    (pilots,) = top.steps
    assert isinstance(pilots, HoleStep) and len(pilots.points) == 2 and (pilots.d, pilots.depth) == (PREDRILL, 3)
    assert {b.name for b in plan.hardware[0].bodies} == {"latch_1"}

    from lang.preview.mesh import build_scene
    scene = build_scene(layout)
    names = {node.rsplit(".", 1)[1] for node in scene.graph.nodes_geometry if "door_latches" in node}
    assert names == {"latch_1"}
    door_mesh = scene.geometry["cab.door"]
    assert door_mesh.is_volume


def test_example_builds_and_its_drawer_boxes_clear_the_latches(tmp_path: Path):
    example = Path(__file__).resolve().parents[1] / "examples" / "door_latch.py"
    layout = run_build(example, tmp_path, scene=False)
    assert layout["problems"] == [] and plan_layout(layout).problems == []
    cab = registry.roots[0]
    parts = cab.all_parts()
    latches = [h for h in cab.all_hardware() if h["name"].endswith("_latches")]
    assert [h["path"] for h in latches] == ["locker.door_latches", "locker.drawer1.face_latches",
                                            "locker.drawer2.face_latches"]
    for item in latches:
        for body in item["bodies"]:
            for b in body["boxes"]:
                assert not [p.path for p in parts if _overlaps(p, b["min"], b["max"])], body["name"]
    door = cab.part("door")
    assert len([op for op in door.ops if isinstance(op, Hole)]) == 2 and len(_pockets(door)) == 2


# -- the review's fixes (findings 25, 31) --------------------------------------------------------------------

def test_thresholds_have_a_tolerance():
    """A door a hair thicker than the 10 mm the counterbore leaves gets no
    counterbore of a hair's depth; a carcass board whose face lies at the
    door's middle, give or take a hair, is as ambiguous as one across it."""
    _, parts = _inset_door(DoorLatch("Pull Lock 44"), thickness=10 + 1e-7)
    assert _pockets(parts["door"]) == {}
    registry.reset()
    box = Box.from_size(width=600, depth=500, height=720)
    with module("cab", box) as cab:
        carcass = _carcass(cab)
        door = board("door", ply15).on(cab.front.gap(15), toward=cab.back)        # z 0..720, its middle at 360
        shelf = board("shelf", ply15).on(Pos("z", 360 + 1e-7), toward=cab.top).between(carcass["left"],
                                                                                       carcass["right"])
        with pytest.raises(LangError, match="lies across the middle of the door"):
            cab.mount(DoorLatch("Everlock"), door=door, carcass=shelf)


def test_a_pilot_in_a_pocket_made_before_is_refused():
    """`Board.hole_fits` sees the operations made before (the add-in's
    probes do): a pilot hole of the strike in a pocket of the top."""
    box = Box.from_size(width=600, depth=500, height=720)
    with module("cab", box) as cab:
        parts = _carcass(cab)
        door = board("door", ply15).on(cab.front).between(parts["left"], parts["right"], parts["bottom"],
                                                          parts["top"]).inset(2)
        top = parts["top"]
        # the strike's pair at x 29, y 290.5 and 309.5 under the top
        top.pocket(rect(depth=10, width=10), at=top.bottom.front(Pos("x", 24)).left(Pos("y", 305)), depth=3)
        with pytest.raises(LangError, match=r"the hole 'pull_lock_door_1a' \(3.2 mm\) does not fit on cab.top's "
                                            "bottom face"):
            cab.mount(DoorLatch("Pull Lock 44"), door=door, carcass=top)
    assert not [op for op in door.ops + top.ops if isinstance(op, Hole)]


def test_pilot_depth_short_of_the_far_face():
    with pytest.raises(LangError, match=r"the pilot depth \(15 mm\) must be less than cab.door's thickness"):
        _inset_door(DoorLatch("Everlock", pilot=(3, 15)))
