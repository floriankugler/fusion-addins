"""`Shape.rounded()`, `Shape.clip()`, `-` and `+` on shapes, and operations
given a shape without area."""
import math
import re
from collections.abc import Callable

import pytest
from shapely.geometry import Point

from lang import *
from lang.core.ops import Pocket
from lang.emit.arcs import Arc2, Line2, fit
from helpers import ply15

#: What a quarter circle of radius 1 leaves of its square.
CORNER = 1 - math.pi / 4


def _curves(shape: Shape) -> list[str]:
    """The lines and arcs of the shape's one ring, an arc as `arc r=<radius>
    <sweep in degrees>`, starting with the first arc."""
    (ring,) = shape.rings()
    out: list[str] = []
    for c in fit(ring):
        if isinstance(c, Arc2):
            sweep = math.degrees(abs(math.remainder(math.atan2(c.b[1] - c.center[1], c.b[0] - c.center[0])
                                                    - math.atan2(c.a[1] - c.center[1], c.a[0] - c.center[0]),
                                                    2 * math.pi)))
            out.append(f"arc r={c.radius:.6g} {sweep:.4g}")
        else:
            assert isinstance(c, Line2)
            out.append("line")
    first = next(i for i, c in enumerate(out) if c.startswith("arc"))
    return out[first:] + out[:first]


def test_half_the_narrow_width_rounds_the_ends_fully():
    for shape in (rect(depth=80, width=12), rect(depth=12, width=80)):
        slot = shape.rounded(6)
        assert slot.bounds == pytest.approx(shape.bounds)
        assert slot.axes == shape.axes
        assert slot.area == pytest.approx(80 * 12 - 4 * CORNER * 36, abs=0.02)
        # each end one half circle, not two quarters with a line between
        assert _curves(slot) == ["arc r=6 180", "line", "arc r=6 180", "line"]


def test_half_the_width_with_rounding_noise_is_still_a_slot():
    width = 0.1 * 3 * 40                                  # 12.000000000000002
    slot = rect(depth=80, width=width).rounded(width / 2 + 1e-9)
    assert _curves(slot) == ["arc r=6 180", "line", "arc r=6 180", "line"]


def test_a_radius_beyond_half_the_narrow_width_is_an_error():
    with pytest.raises(LangError, match=r"rounded\(6\.5\): the radius is more than half the shape's narrow "
                                        r"width \(12, "):
        rect(depth=80, width=12).rounded(6.5)
    with pytest.raises(LangError, match=r"rounded\(6\.000001\): .* narrow width \(12, "):
        rect(depth=80, width=12).rounded(6 + 1e-6)
    with pytest.raises(LangError, match=r"rounded\(10\.5\): .* narrow width \(20, "):
        circle(20).rounded(10.5)


def test_every_corner_is_rounded_concave_ones_too():
    ell = polygon([(0, 0), (100, 0), (100, 30), (30, 30), (30, 100), (0, 100)])
    rounded = ell.rounded(5)
    # five convex corners lose a little, the concave one at (30, 30) gains as much
    assert rounded.area == pytest.approx(ell.area - 4 * CORNER * 25, abs=0.02)
    assert rounded.geometry.contains(Point(30.5, 30.5))
    assert not rounded.geometry.contains(Point(99.5, 0.5))
    assert _curves(rounded) == ["arc r=5 90", "line"] * 6


def test_arcs_are_not_corners():
    for shape, radius in ((rect(depth=80, width=40).rounded(10), 10), (rect(depth=80, width=12).rounded(6), 6),
                          (circle(30), 15), (circle(30), 5)):
        assert shape.rounded(radius).geometry.symmetric_difference(shape.geometry).area < 1e-6


def test_rounding_with_zero_or_a_negative_radius():
    shape = rect(depth=80, width=12)
    assert shape.rounded(0) is shape
    with pytest.raises(LangError, match="must not be negative"):
        shape.rounded(-1)


def test_an_edge_too_short_for_its_arcs_is_an_error():
    # the clip's edge is 7.1 long; each 135 degree corner needs 4.1 of it
    with pytest.raises(LangError, match=r"rounded\(10\): an edge of the shape is too short"):
        rect(depth=80, width=60).clip(back=5, right=5).rounded(10)
    rect(depth=80, width=60).clip(back=5, right=5).rounded(8)


def test_a_sharp_corner_with_long_edges_is_rounded():
    """Found by fuzzing: a corner sharper than 28 degrees could not be
    rounded however long its edges, and the error blamed an edge too short.
    The fillet's centre lies r / cos(turn / 2) from the corner; the check
    against far-off centres divided by the sine."""
    tip = math.radians(20)
    shape = polygon([(0, 0), (300, 0), (0, 300 * math.tan(tip))]).rounded(2)
    # the 20 degree tip loses r^2 (cot(tip/2) - (pi - tip)/2)
    lost = 4 * (1 / math.tan(tip / 2) - (math.pi - tip) / 2)
    others = 4 * (1 - math.pi / 4) + 4 * (1 / math.tan((math.pi / 2 - tip) / 2) - (math.pi / 2 + tip) / 2)
    assert shape.area == pytest.approx(300 * 300 * math.tan(tip) / 2 - lost - others, abs=0.01)


def test_a_rounded_slot_cuts_and_pockets():
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        with board("panel", ply15).on(m.bottom).show(m.top) as panel:
            before = panel.outline.area
            panel.cut(rect(depth=80, width=12).rounded(6), at=panel.top.center, name="oblong")
            panel.pocket(rect(depth=60, width=10).rounded(5), at=panel.top.front(20), depth=5, name="groove")
    slot = 80 * 12 - 4 * CORNER * 36
    assert panel.outline.area == pytest.approx(before - slot, abs=0.02)
    groove = panel.op("groove").op
    assert isinstance(groove, Pocket)
    assert groove.shape.area == pytest.approx(60 * 10 - 4 * CORNER * 25, abs=0.02)


#: A shape without area: what a difference leaves of a shape inside another.
EMPTY = circle(10).difference(circle(20))

#: Each operation that takes a shape, by the name its error gives.
OPERATIONS: list[tuple[str, Callable[[Board], object]]] = [
    ("cut()", lambda p: p.cut(EMPTY, at=p.top.center)),
    ("pocket()", lambda p: p.pocket(EMPTY, at=p.top.center, depth=5)),
    ("pocket()", lambda p: p.pocket(EMPTY, at=p.front.center, depth=5)),
    ("cutout()", lambda p: p.cutout(EMPTY, at=p.bottom.center)),
    ("add_cut()", lambda p: p.add_cut(EMPTY)),
    ("add_pocket()", lambda p: p.add_pocket(p.top, EMPTY, 5)),
    ("add_edge_pocket()", lambda p: p.add_edge_pocket(p.left, EMPTY, 5)),
    ("add_to_outline()", lambda p: p.add_to_outline(EMPTY)),
    ("cut()", lambda p: p.cut(rect(depth=20, width=20).intersection(rect(depth=20, width=20).moved(20, 0)),
                              at=p.top.center)),           # two squares side by side share only an edge
]


@pytest.mark.parametrize("what, operation", OPERATIONS)
def test_an_operation_with_an_empty_shape_is_an_error(what: str, operation: Callable[[Board], object]):
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        panel = board("panel", ply15).on(m.bottom).show(m.top)
        with pytest.raises(LangError, match=rf"m\.panel: {re.escape(what)}: the shape is empty"):
            operation(panel)
        assert panel.ops == []


def test_a_board_with_an_empty_shape_is_an_error():
    with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
        with pytest.raises(LangError, match=r"m\.panel: board\(\): the shape is empty"):
            board("panel", ply15, rect(depth=100, width=100).difference(rect(depth=200, width=200))).on(m.bottom)


# -- clip ---------------------------------------------------------------------------

def test_clip_names_the_corner_by_its_two_edges():
    """In the world frame a depth x height rectangle lies in (x, z), its back
    at high x: 380 off along the top edge and 120 down the back edge."""
    shape = rect(depth=500, height=720).clip(top=380, back=120)
    assert shape.area == pytest.approx(500 * 720 - 380 * 120 / 2)
    inside = shape.geometry
    assert not inside.contains(Point(495, 715)) and inside.contains(Point(105, 715))
    assert inside.contains(Point(495, 595))


def test_clip_follows_the_frame_the_shape_is_made_in():
    """In a cabinet facing the van's right, front is +y: the cabinet's
    front corner of a width x height rectangle is the van's right one."""
    van = Box.from_size(width=2000, depth=1000, height=1000)
    with module("cab", van, front=van.right):
        shape = rect(depth=100, height=100).clip(top=10, front=10)
    assert shape.axes == ("y", "z")
    assert not shape.geometry.contains(Point(99, 99)) and shape.geometry.contains(Point(1, 99))


def test_clip_on_a_raw_shape_uses_left_right_bottom_top():
    shape = polygon([(0, 0), (40, 0), (40, 20), (0, 20)]).clip(right=10, bottom=4)
    assert shape.area == pytest.approx(800 - 20)
    assert not shape.geometry.contains(Point(39.5, 0.5))


def test_clip_errors():
    with pytest.raises(LangError, match="name the corner by its two edges"):
        rect(depth=50, height=50).clip(top=10)
    with pytest.raises(LangError, match="lie on one axis"):
        rect(depth=50, height=50).clip(top=10, bottom=10)
    with pytest.raises(LangError, match="left is not an edge of a shape in depth x height"):
        rect(depth=50, height=50).clip(top=10, left=10)
    with pytest.raises(LangError, match="raw shape has no plane yet"):
        polygon([(0, 0), (40, 0), (40, 20)]).clip(front=5, top=5)
    with pytest.raises(LangError, match="the leg must be positive"):
        rect(depth=50, height=50).clip(top=10, back=0)


# -- - and + ------------------------------------------------------------------------------------------

def test_minus_and_plus_are_difference_and_union():
    """Decided by Florian, 2026-10-15 (syntax.md item 13): `a - b` takes
    material away and `a + b` adds it, as build123d spells them; the
    methods stay, and the operators are them exactly."""
    plate = rect(depth=100, height=60)
    hole = circle(20, (50, 30))
    tab = rect(depth=20, height=80)
    assert (plate - hole).geometry.equals_exact(plate.difference(hole).geometry, 0)
    assert (plate + tab).geometry.equals_exact(plate.union(tab).geometry, 0)
    assert (plate - hole).area == pytest.approx(6000 - math.pi * 100, abs=0.1)
    assert (plate + tab).bounds == (0, 0, 100, 80)
    assert (plate - hole + tab).axes == (plate - hole).axes == plate.axes == ("x", "z")


def test_minus_and_plus_keep_the_plane_and_clean_as_the_methods_do():
    """A raw shape takes the plane of the one it is combined with; two
    planes are an error; what is narrower than 0.01 mm goes, as from every
    shape."""
    assert (circle(10) + rect(depth=20, height=20)).axes == ("x", "z") == (circle(10) - rect(depth=20, height=20)).axes
    assert (circle(10, (10, 10)) - rect(depth=20, height=20)).is_empty()
    with pytest.raises(LangError, match="Shapes lie in different planes: depth x height and width x height"):
        _ = rect(depth=20, height=20) - rect(width=20, height=20)
    sliver = rect(depth=100, height=60) - rect(depth=100, height=59.995)
    assert sliver.is_empty()


def test_minus_or_plus_a_number_is_an_error():
    with pytest.raises(LangError, match=r"shape \+ 5: \+ takes another shape; a shape moves with moved\(\)"):
        _ = rect(depth=20, height=20) + 5  # type: ignore[operator]  -- a number is a type error too
    with pytest.raises(LangError, match=r"shape - 0.5: - takes another shape; .* grows with offset\(\)"):
        _ = rect(depth=20, height=20) - 0.5  # type: ignore[operator]
