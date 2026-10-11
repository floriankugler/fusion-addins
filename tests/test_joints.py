"""Joints: half laps between crossing boards, and the crossing test."""
import pytest
from shapely.geometry import Point

from lang import *
from lang.core.crossing import crossing
from lang.core.layout import build_layout
from lang.core.scope import registry

ply15 = material("birch", t=15)


@pytest.fixture(autouse=True)
def fresh_registry():
    registry.reset()
    yield
    registry.reset()


def _grid(n_cross: int = 1) -> tuple[Scope, list[Board], Board]:
    """Boards across (thickness on x) and one along (thickness on y), all
    30 high, in a 1000 x 600 x 30 box."""
    with module("grid", Box.from_size(width=600, depth=1000, height=30)) as g:
        cross = [board(f"cross{i}", ply15).center(Pos("x", 200 + 300 * i)) for i in range(n_cross)]
        long = board("long", ply15).center(Pos("y", 300))
        check(no_interference)
    return g, cross, long


def test_crossing_boards_are_found_and_parallel_ones_are_not():
    _, (a, b), long = _grid(2)
    c = crossing(a, long)
    assert c is not None and c.axis == "z" and (c.lo, c.hi) == (0, 30)
    assert crossing(a, b) is None                       # parallel
    assert [p for p in build_layout()["problems"] if "overlaps" in p] == [
        "grid.cross0 overlaps grid.long", "grid.cross1 overlaps grid.long"]


def test_a_half_lap_notches_both_boards_to_the_middle():
    g, (a,), long = _grid()
    with g:
        long.join(a, using=half_lap(toward=g.top))
    # the board along is notched from the top over the cross board's thickness
    assert long.outline.geometry.contains(Point(200, 10))
    assert not long.outline.geometry.contains(Point(200, 20))
    assert long.outline.geometry.contains(Point(180, 20))
    # the cross board from below over the long one's thickness
    assert not a.outline.geometry.contains(Point(300, 10)) and a.outline.geometry.contains(Point(300, 20))
    assert long.has_operation("lap_cross0") and a.has_operation("lap_long")
    assert build_layout()["problems"] == []             # lapped boards no longer overlap


def test_split_and_clearance():
    g, (a,), long = _grid()
    with g:
        long.join(a, using=half_lap(toward=g.bottom, at=g.bottom + 10, clearance=0.5))
    # notched from below now, up to z = 10, and 16 mm wide (192 to 208)
    assert not long.outline.geometry.contains(Point(192.2, 5))
    assert long.outline.geometry.contains(Point(192.2, 15))
    assert long.outline.geometry.contains(Point(191.8, 5))
    # the cross board from above, down to z = 10
    assert not a.outline.geometry.contains(Point(300, 15)) and a.outline.geometry.contains(Point(300, 5))


def test_a_half_lap_joins_only_the_boards_named():
    g, (a, b), long = _grid(2)
    with g:
        long.join(a, using=half_lap(toward=g.top))
    assert long.has_operation("lap_cross0") and not long.has_operation("lap_cross1")
    assert b.ops == []
    with g:
        long.join([b], using=half_lap(toward=g.top))          # a list works too
    assert long.has_operation("lap_cross1")


def test_half_lap_errors():
    g, (a,), long = _grid()
    with g:
        with pytest.raises(LangError, match="does not run along"):
            long.join(a, using=half_lap(toward=g.front))
        with pytest.raises(LangError, match="outside the height"):
            long.join(a, using=half_lap(toward=g.top, at=g.top + 5))
        other = board("other", ply15).center(Pos("x", 900)).between(Pos("y", 0), Pos("y", 100))
        with pytest.raises(LangError, match="cross0 does not cross|other does not cross"):
            long.join(a, other, using=half_lap(toward=g.top))
        with pytest.raises(LangError, match="name the boards"):
            long.join(using=half_lap(toward=g.top))
        with pytest.raises(LangError, match="named twice"):
            long.join(a, [a], using=half_lap(toward=g.top))
        with pytest.raises(LangError, match="to itself"):
            long.join(long, using=half_lap(toward=g.top))
    assert long.ops == [] and a.ops == []                 # nothing is cut when a join fails
    with pytest.raises(LangError, match="at=.* is not on the axis"):
        half_lap(toward=frame.direction("top"), at=Pos("x", 3))
