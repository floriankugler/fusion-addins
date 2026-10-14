"""Fuzzing the master's contours as limits (`contours.contour_cases`): a
board the contours limit keeps what `between()` promises, built any way
(`contours.run_case`); and the round offset behind every clearance
(`lang.core.contours.round_offset`) keeps it, and is the same however
its rings come."""
import math
from collections.abc import Sequence

from hypothesis import given
from hypothesis import strategies as st
from shapely import affinity
from shapely.geometry import MultiLineString, MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry

from boards import KNOWN
from contours import ContourCase, contour_cases, run_case
from fuzzing import line_polygons, recipes, shifts, sizes
from lang.core.contours import round_offset
from lang.core.geometry import polygons_of


@given(contour_cases())
def test_contour_limits_keep_their_promises_on_any_board(case: ContourCase):
    assert [p for p in run_case(case) if not p.startswith(KNOWN)] == []


def _shapes() -> st.SearchStrategy[BaseGeometry]:
    """Areas as the language makes them, with arcs and holes, or of lines."""
    lines = line_polygons().map(lambda s: s.polygon() or Polygon())
    return st.one_of(recipes(grow=False).map(lambda r: r.geometry()), lines).filter(lambda g: not g.is_empty)


def _rerun(g: BaseGeometry, reverse: bool, start: int, every: int) -> BaseGeometry:
    """The same area, each ring run the other way, started `start` points
    on, with points added along every `every`-th edge (0: none)."""
    def ring(coords: Sequence[Sequence[float]]) -> list[tuple[float, float]]:
        pts = [(float(c[0]), float(c[1])) for c in coords[:-1]]
        if every:
            more: list[tuple[float, float]] = []
            for j, (p, q) in enumerate(zip(pts, pts[1:] + pts[:1])):
                more.append(p)
                if j % every == 0:
                    more += [(p[0] + f * (q[0] - p[0]), p[1] + f * (q[1] - p[1])) for f in (0.25, 0.5)]
            pts = more
        k = start % len(pts)
        pts = pts[k:] + pts[:k]
        return pts[::-1] if reverse else pts
    polys = [Polygon(ring(list(p.exterior.coords)), [ring(list(h.coords)) for h in p.interiors])
             for p in polygons_of(g)]
    return polys[0] if len(polys) == 1 else MultiPolygon(polys)


def _thinner(g: BaseGeometry, width: float) -> bool:
    """Whether every piece of `g` is narrower than `width` everywhere."""
    return all(p.area <= 1e-9 or p.buffer(-width / 2).is_empty for p in polygons_of(g))


@given(_shapes(), sizes(0.5, 30), st.booleans(), st.booleans(), st.integers(0, 40), st.sampled_from([0, 0, 1, 3]),
       st.booleans(), shifts())
def test_a_round_offset_is_the_same_however_its_rings_come(g: BaseGeometry, d: float, grow: bool, reverse: bool,
                                                           start: int, every: int, mirror: bool,
                                                           shift: tuple[float, float]):
    """The same area with its rings run the other way, started elsewhere,
    with points added along edges gives the same offset; grown or shrunk,
    it keeps at least the distance from the area's edges, less only by its
    arcs' chords, and more by no more than GEOS's simplification (a
    hundredth of the distance a pass), which is all that a mirrored or
    moved area may change: a clearance up to about a hundredth more than
    asked, never less, is accepted [decided by Florian, 2026-10-14]."""
    distance = d if grow else -d
    got = round_offset(g, distance)
    assert got.is_valid
    again = round_offset(_rerun(g, reverse, start, every), distance)
    assert again.symmetric_difference(got).area <= 1e-9 * max(1.0, got.length)
    edges = MultiLineString([(p, q) for poly in polygons_of(g) for r in (poly.exterior, *poly.interiors)
                             for p, q in zip(r.coords, r.coords[1:])])
    capsules = edges.buffer(d, quad_segs=32)
    truth = g.union(capsules) if grow else g.difference(capsules)
    # (its arcs' chords, an eighth of a quarter turn, up to 1.5 times that as GEOS rounds their
    # number, about twice as deep where two arcs' chords cross; a strip shrunk to nothing)
    chords = 2 * d * (1 - math.cos(0.75 * math.pi / 16)) + 1e-6
    simplified = 0.02 * d
    less, more = (truth.difference(got), got.difference(truth)) if grow else (got.difference(truth), truth.difference(got))
    assert _thinner(less, 2 * chords)
    assert _thinner(more, 2 * (chords + simplified))

    def moved(x: BaseGeometry) -> BaseGeometry:
        if mirror:
            x = affinity.affine_transform(x, [0, 1, 1, 0, 0, 0])
        return affinity.translate(x, *shift)
    elsewhere = round_offset(moved(g), distance)
    assert _thinner(elsewhere.symmetric_difference(moved(got)), 2 * (chords + simplified))
