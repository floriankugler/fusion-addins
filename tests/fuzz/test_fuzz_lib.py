"""Fuzz tests of the plain data modules in lib/ that compute: the stations
along an edge (`lib.stations` and the three callers that keep their own
refusals), the drawer slides' choice of holes, the hatch hinges'
overlap limit, and the cutouts' triangle and rhombus solvers. The hardware checks measure the language against
`lib.stations`, so it is checked here on its own."""
from __future__ import annotations

import itertools
import math

from hypothesis import assume, given
from hypothesis import strategies as st

from lib import connector_data, cutout_patterns, door_latches, drawer_slides, hatch_hinges, sliding_brackets
from lib import stations as station_rule

_lengths = st.floats(0.0, 5000.0, allow_nan=False)
_ends = st.floats(-50.0, 3000.0, allow_nan=False)
_counts = st.integers(-1, 20)


def _close(a: float, b: float, scale: float) -> bool:
    return abs(a - b) <= 1e-9 * max(1.0, scale)


@given(_lengths, st.integers(1, 20), st.floats(0.0, 2500.0, allow_nan=False))
def test_stations_are_spread_evenly_from_end_to_end(length: float, count: int, end: float):
    got = station_rule.stations(length, count, end)
    assert len(got) == count
    if count == 1:
        assert got == [length / 2]
        return
    assert got[0] == end and _close(got[-1], length - end, length)
    gaps = [b - a for a, b in zip(got, got[1:])]
    assert all(_close(g, gaps[0], length) for g in gaps)
    # the same seen from the other end
    assert all(_close(length - a, b, length) for a, b in zip(got, reversed(got)))
    if 2 * end < length:
        # (within rounding: the rule keeps the floats of the copies it replaced, end +
        # index * spacing, whose last can lie an ulp past the stretch)
        slack = 1e-9 * max(1.0, length)
        assert all(-slack <= a < b <= length + slack for a, b in zip(got, got[1:]))


@given(_lengths, _counts, _ends)
def test_each_caller_refuses_what_it_says_and_spreads_the_rest_as_the_rule(length: float, count: int, end: float):
    """`connector_data` refuses only no station, `sliding_brackets` also a
    stretch no longer than twice `end` (for more than one), `door_latches`
    also an end offset that is not positive; what they accept is
    `lib.stations`'."""
    refused = {
        "connectors": count < 1,
        "brackets": count < 1 or (count > 1 and length <= 2 * end),
        "latches": count < 1 or (count > 1 and (end <= 0 or length <= 2 * end)),
    }
    callers = {"connectors": connector_data.stations, "brackets": sliding_brackets.stations,
               "latches": door_latches.stations}
    for name, caller in callers.items():
        try:
            got = caller(length, count, end)
        except ValueError:
            assert refused[name], f"{name} refused {length, count, end}"
            continue
        assert not refused[name], f"{name} accepted {length, count, end}"
        assert got == station_rule.stations(length, count, end)


@st.composite
def _candidates(draw: st.DrawFn) -> tuple[list[float], int]:
    """Sorted distinct hole positions, on a 9 mm grid as the slides' are or
    anywhere, and how many to choose."""
    if draw(st.booleans()):
        steps = draw(st.lists(st.integers(1, 30), min_size=1, max_size=11))
        positions = list(itertools.accumulate([draw(st.integers(0, 40))] + [9 * s for s in steps]))
    else:
        positions = sorted(set(draw(st.lists(st.floats(0, 700, allow_nan=False), min_size=2, max_size=12))))
    assume(len(positions) >= 2)
    return [float(p) for p in positions], draw(st.integers(1, len(positions)))


def _cost(chosen: list[float], first: float, last: float) -> float:
    count = len(chosen)
    return sum((c - (first + (last - first) * k / (count - 1))) ** 2 for k, c in enumerate(chosen))


@given(_candidates())
def test_the_slides_take_the_holes_nearest_even_spacing(case: tuple[list[float], int]):
    """`choose_holes` against every choice: the front-most and rearmost hole
    and, between them, the holes with the least squared distance to equal
    spacing."""
    candidates, count = case
    got = drawer_slides.choose_holes(candidates, count)
    assert len(got) == count and got == sorted(set(got)) and set(got) <= set(candidates)
    if count == 1:
        assert got == [candidates[0]]
        return
    first, last = candidates[0], candidates[-1]
    assert got[0] == first and got[-1] == last
    best = min(_cost([first, *middle, last], first, last)
               for middle in itertools.combinations(candidates[1:-1], count - 2))
    assert math.isclose(_cost(got, first, last), best, rel_tol=1e-9, abs_tol=1e-9)


@given(st.sampled_from(hatch_hinges.HINGE_SPECS), st.floats(-10.0, 60.0, allow_nan=False),
       st.booleans())
def test_the_hatch_overlap_limit_follows_its_table_in_mm_and_in_cm(spec: hatch_hinges.HingeSpec, t: float,
                                                                    limited: bool):
    got = spec.overlap_limit(t, limited)
    if limited:
        assert got == spec.limited_max_overlap
    else:
        table = spec.max_overlap
        overlaps = [o for _, o in table]
        assert min(overlaps) <= got <= max(overlaps)
        for (t0, o0), (t1, o1) in zip(table, table[1:]):
            if t0 <= t <= t1:
                assert math.isclose(got, o0 + (o1 - o0) * (t - t0) / (t1 - t0), abs_tol=1e-9)
        if t <= table[0][0]:
            assert got == table[0][1]
        if t >= table[-1][0]:
            assert got == table[-1][1]
    assert math.isclose(spec.in_cm().overlap_limit(t / 10, limited), got / 10, abs_tol=1e-12)


_extents = st.floats(20.0, 2000.0, allow_nan=False)


@given(_extents, _extents, st.integers(1, 12), st.integers(1, 10), st.floats(0.5, 60.0, allow_nan=False),
       st.one_of(st.none(), st.floats(0.5, 30.0, allow_nan=False)))
def test_the_triangles_keep_the_spacing_or_are_refused(extent_u: float, extent_v: float, columns: int, rows: int,
                                                        spacing: float, radius: float | None):
    """`triangles` keeps what it says or raises ValueError: the sharp
    triangles span the extent, columns pitches of half a width and the gap
    along u; facing sides `spacing` apart, sharp or with the tips rounded
    with `radius` and aligned; a rounded tip's circle touching both sides."""
    try:
        got = cutout_patterns.triangles(extent_u, extent_v, columns, rows, spacing, aligned_radius=radius)
    except ValueError:
        return
    w, h, apex = got.width, got.height, got.apex_height
    assert w > 0 and h > 0 and math.isclose(h, (extent_v - (rows - 1) * spacing) / rows, rel_tol=1e-12)
    assert math.isclose(got.pitch_u, extent_u / columns) and math.isclose(got.pitch_v, h + spacing)
    gap = cutout_patterns._gap(w, apex, h, got.pitch_u)  # type: ignore[reportPrivateUsage]
    assert math.isclose(gap, spacing, rel_tol=1e-9, abs_tol=1e-9)
    if radius is None:
        assert apex == h
        assert math.isclose(columns * (w / 2 + spacing * math.hypot(h, w / 2) / h), extent_u, rel_tol=1e-9)
    else:
        assert apex >= h - 1e-9
        # the tip's circle, centred `radius` below the height on the altitude, one radius from a side
        half = w / 2
        distance = half * (apex - (h - radius)) / math.hypot(half, apex)
        assert math.isclose(distance, radius, rel_tol=1e-9, abs_tol=1e-9)


@given(st.floats(1.0, 500.0, allow_nan=False), st.floats(1.0, 500.0, allow_nan=False),
       st.floats(0.0, 60.0, allow_nan=False))
def test_the_rhombuses_fill_their_pitches_but_for_the_spacing(pitch_u: float, pitch_v: float, spacing: float):
    w, h = cutout_patterns.rhombus_dimensions(pitch_u, pitch_v, spacing)
    assume(w > 0 and h > 0)
    assert math.isclose(w + spacing * math.hypot(w, h) / h, pitch_u, rel_tol=1e-9)
    assert math.isclose(h + spacing * math.hypot(w, h) / w, pitch_v, rel_tol=1e-9)
