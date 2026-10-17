"""Screws, and connectors in the gaps between tenons (`gaps=`, `tenons=`)."""
import math

import pytest

from lang import *
from lang.core.ops import Hole
from lang.core.scope import registry
from lang.core.layout import build_layout
from lang.preview.mesh import FINE, mesh_part
from helpers import ply15, ply18


def _unit(shelf_at: float = 400) -> tuple[Scope, Board, Board, Board]:
    """Two 15 mm sides (y) and an 18 mm shelf between them, in a 600 wide
    (y), 300 deep (x), 800 high box."""
    with module("unit", Box.from_size(width=600, depth=300, height=800)) as u:
        left = board("left", ply15).on(u.left)
        right = board("right", ply15).on(u.right)
        shelf = board("shelf", ply18).on(Pos("z", shelf_at), toward=u.top).between(left, right)
    return u, left, right, shelf


def _holes(part: Board, prefix: str) -> list[Hole]:
    return [op for op in part.ops if isinstance(op, Hole) and (op.name or "").startswith(prefix)]


def test_screws_through_the_side_into_the_end():
    u, left, right, shelf = _unit()
    with u:
        shelf.join(left, right, using=screws(count=3, countersink=True))
    holes = _holes(left, "screw_shelf_")
    assert [h.name for h in holes] == ["screw_shelf_1", "screw_shelf_2", "screw_shelf_3"]
    h = holes[0]                                  # left's frame is (x, z), drilled from its outer face
    assert (h.face, h.u, h.v, h.d, h.through) == ("left", 60, 409, 4, True)
    assert h.chamfer == pytest.approx(2.2)        # a countersink 2 x 4 + 0.4 = 8.4 wide
    assert shelf.ops == [] and len(_holes(right, "screw_shelf_")) == 3



def test_a_countersink_must_lie_on_the_face_it_is_sunk_into():
    """Found in the Fusion batch check of the fuzzed joints: 4 mm screws
    into a 4 mm divider flush with the side's front edge; their
    countersinks, 8.4 across, reached 2.2 past that edge, and Fusion could
    not cut them. A countersink reaching past its board's edge is an
    error; without one, or 10 in from the edge, the screws are fine."""
    with module("unit", Box.from_size(width=600, depth=300, height=800)) as u:
        left = board("left", ply15).on(u.left)
        thin = sheet_material("birch", t=4)
        flush = board("flush", thin).on(Pos("x", 0), toward=u.back).between(left, Pos("y", 300), Pos("z", 100),
                                                                              Pos("z", 300))
        before = [list(left.ops), list(flush.ops)]
        with pytest.raises(LangError, match=r"^unit\.flush: screws with unit\.left: at z=150, the countersink "
                                            r"\(8\.4 mm across\) would not lie on unit\.left's left face: it reaches "
                                            r"past its edge"):
            flush.join(left, using=screws(count=2, end=50, countersink=True))
        assert [list(left.ops), list(flush.ops)] == before
        flush.join(left, using=screws(count=2, end=50))
        inset = board("inset", thin).on(Pos("x", 10), toward=u.back).between(left, Pos("y", 300), Pos("z", 400),
                                                                               Pos("z", 600))
        inset.join(left, using=screws(count=2, end=50, countersink=True))

def test_screws_and_cabineos_in_the_gaps_between_tenons():
    u, left, _, shelf = _unit()
    t = tenons(count=2, width=50, margin=50)      # tenons 50..100 and 200..250: gaps 50, 100, 50
    with u:
        shelf.join(left, using=t)
        shelf.join(left, using=screws(gaps=t))
        shelf.join(left, using=cabineo(gaps=t))
    assert [h.u for h in _holes(left, "screw_shelf_")] == [25, 150, 275]
    access = _holes(shelf, "cabineo_left_")
    assert sorted({h.u for h in access}) == [25, 150, 275] and len(access) == 9
    assert [h.u for h in _holes(left, "cabineo_shelf_")] == [25, 150, 275]


def test_two_screws_beside_each_tenon():
    u, left, _, shelf = _unit()
    t = tenons(count=2, width=50)                 # tenons 30..80 and 220..270
    with u:
        shelf.join(left, using=t)
        shelf.join(left, using=screws(gaps=t, offset=12))
    assert [h.u for h in _holes(left, "screw_shelf_")] == [18, 92, 208, 282]


def test_connectors_need_room_in_the_gaps():
    u, left, _, shelf = _unit()
    t = tenons(count=2, width=50)                 # end gaps of 30
    with u:
        shelf.join(left, using=t)
        with pytest.raises(LangError, match="30 mm gap .* narrower than the 40 mm a cabineo needs"):
            shelf.join(left, using=cabineo(gaps=t))
        with pytest.raises(LangError, match="narrower than the 120 mm a clamex needs"):
            shelf.join(left, using=clamex(gaps=t))


def test_screws_through_open_tenons():
    u, left, _, shelf = _unit(shelf_at=782)       # flush with the sides' top: the mortises run out of it
    t = tenons(count=2, width=50)
    with u:
        shelf.join(left, using=t)
        shelf.join(left, using=screws(tenons=t))
    (a, b) = _holes(shelf, "screw_left_")
    # from the shelf's top face, the open one, halfway along the 15 mm tenons
    assert (a.face, a.u, a.v, b.u, a.through) == ("top", 55, 7.5, 245, True)
    with u, pytest.raises(LangError, match="unit.shelf and unit.left are joined with screws already"):
        shelf.join(left, using=screws(tenons=t, offset=12))         # a second join of the pair with screws
    registry.reset()
    u, left, _, shelf = _unit(shelf_at=782)
    t = tenons(count=2, width=50)
    with u:
        shelf.join(left, using=t)
        shelf.join(left, using=screws(tenons=t, offset=12))
    assert [h.u for h in _holes(shelf, "screw_left_")] == [42, 68, 232, 258]


def test_gap_and_tenon_screw_errors():
    u, left, right, shelf = _unit()
    t = tenons(count=2, width=50)
    with u:
        with pytest.raises(LangError, match="screws with unit.left: the two are not joined with the tenons given"):
            shelf.join(left, using=screws(gaps=t))
        shelf.join(left, using=t)
        with pytest.raises(LangError, match="closed in on both sides"):
            shelf.join(left, using=screws(tenons=t))
        with pytest.raises(LangError, match="less than half the 50 mm tenons"):
            shelf.join(left, using=screws(tenons=t, offset=25))
        with pytest.raises(LangError, match="cabineo with unit.right: the two are not joined with the tenons given"):
            shelf.join(right, using=cabineo(gaps=t))
    for message, make in (("give one of count=, at=, gaps= or tenons=", lambda: screws()),
                          ("give one of count=, at=, gaps= or tenons=", lambda: screws(count=2, gaps=t)),
                          ("offset= places screws beside or in tenons", lambda: screws(count=2, offset=12)),
                          ("give one of count=, at= or gaps=", lambda: cabineo(count=2, gaps=t))):
        with pytest.raises(LangError, match=message):
            make()


@pytest.mark.parametrize("outer", ["left", "right"])
def test_the_preview_shows_countersinks(outer: str):
    u, left, right, shelf = _unit()
    with u:
        shelf.join(left if outer == "left" else right, using=screws(count=1, countersink=True))
    layout = build_layout()
    part = next(p for p in layout["modules"][0]["parts"] if p["path"] == f"unit.{outer}")
    volume = mesh_part(part, layout["frame"], level=FINE).volume
    r, c = 2.0, 2.2                               # a 4 mm screw, its countersink 8.4 wide
    hole = math.pi * r * r * 15                   # through the 15 mm side, 24-sided in the mesh
    sink = math.pi * c / 3 * ((r + c) ** 2 + (r + c) * r + r * r) - math.pi * r * r * c
    assert 300 * 800 * 15 - volume == pytest.approx(hole + sink, rel=0.01)
