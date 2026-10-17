"""Taking shapely's results apart, and cleaning them.

A boolean or a section in shapely returns a polygon, a multi-polygon, a
line, a collection of all of these, or an empty geometry, depending on
what it found. `parts_of` and `polygons_of` give the pieces in one form, so
callers need not ask which kind came back.

`clean` takes out what a boolean leaves where two edges coincide (the same
edge or arc made twice, by two calculations that round differently): it
cannot tell on which side such an edge lies, and leaves spikes, slivers
and walls of no width. Every `Shape` is cleaned when it is made.
"""
from __future__ import annotations

import numpy as np
import shapely
from shapely.geometry import LinearRing, MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry

#: Points nearer than this (mm) are one point, and a ring that turns back
#: along itself within it has a spike there.
SAME_POINT = 1e-6
#: How near (mm) two rings run along each other in a wall of no width: a
#: boolean's rounding, far under what a circle touching a line within
#: `SAME_POINT` shares with it (0.004 mm for a radius of 2 m).
_WALL = 1e-9
#: The narrowest (mm) piece or hole the language keeps: nothing narrower is
#: meant [Florian, 2026-10-13], so narrower ones are what booleans leave.
NARROWEST = 0.01
#: A ring's points, n by 2.
Ring = np.ndarray[tuple[int, int], np.dtype[np.float64]]


def parts_of(g: BaseGeometry) -> list[BaseGeometry]:
    """The pieces of a geometry: the members of a multi-part one or a
    collection, else the geometry itself; empty pieces left out."""
    members: list[BaseGeometry] = list(getattr(g, "geoms", [g]))
    return [p for p in members if not p.is_empty]


def polygons_of(g: BaseGeometry) -> list[Polygon]:
    """The polygons with area in a geometry, however nested (a
    multi-polygon, a collection with lines and points in it)."""
    if isinstance(g, Polygon):
        return [g] if not g.is_empty and g.area > 0 else []
    if isinstance(g, MultiPolygon) or hasattr(g, "geoms"):
        return [p for sub in getattr(g, "geoms", []) for p in polygons_of(sub)]
    return []


def clean(g: BaseGeometry) -> BaseGeometry:
    """`g` without what booleans of coincident edges leave [decided with
    Florian, 2026-10-13]: points nearer than `SAME_POINT` to the one before;
    spikes, where a ring runs out and back along itself; pieces and holes
    narrower than `NARROWEST` on average (twice their area over their
    length: the crescents between two drawings of one arc, hairlines), a
    narrow piece opened first, so that wider ones a hairline joins stay;
    and walls of no width, where a hole runs along another ring for more
    than `NARROWEST` (a band cut across a shape exactly as tall leaves one
    piece held by two such walls instead of two pieces): they are opened. An
    invalid geometry is made valid first, its shells united and its holes
    taken out (a move rounds where two rings nearly touch into a crossing).

    Every other vertex stays where it is: arcs are recovered from vertices
    that lie on their circle within 1e-7 mm (`lang.emit.arcs`), and snapping
    to any grid moves them off it. A geometry with nothing to clean comes
    back as it is; of a collection (a boolean's lines and points with its
    areas), only the areas."""
    if g.is_empty:
        return g
    changed = False
    if not g.is_valid:
        # (64 crescents between a circle and a polygon drawn in it, two
        # nearly touching where their vertices nearly coincide: moved 11
        # down, the rounding crossed them in a figure of eight [found by
        # fuzzing, 2026-10-13])
        g, changed = shapely.make_valid(g, method="structure", keep_collapsed=False), True
    if isinstance(g, Polygon):
        polygons: list[Polygon] = [g]
    elif isinstance(g, MultiPolygon):
        polygons = list(g.geoms)
    elif hasattr(g, "geoms"):           # a collection (a shape cut by what it lost): its areas only
        polygons, changed = polygons_of(g), True
    else:
        return g
    out: list[Polygon] = []
    for poly in polygons:
        cleaned = _clean_polygon(poly)
        if cleaned is None:
            out.append(poly)
        else:
            changed = True
            out.extend(cleaned)
    if not changed:
        return g
    if not out:
        return Polygon()
    return out[0] if len(out) == 1 else MultiPolygon(out)


def _clean_polygon(poly: Polygon, walls: bool = True, remake: bool = True) -> list[Polygon] | None:
    """The polygon's clean pieces, or None when it has nothing to clean.
    A ring is judged narrow without its spikes [found by fuzzing the
    placement, 2026-10-14: a strip 0.2 by 7 mm with a hairline tail 175 mm
    long was narrower than 0.01 mm on average, and went with it]."""
    # (rings as numpy arrays, which shapely takes without visiting each point in Python: a
    # list of tuples cost the van's build 0.4 s)
    exterior = _without_spikes(poly.exterior)
    shell = np.asarray(poly.exterior.coords) if exterior is None else exterior
    if len(shell) < 4:
        return []
    if _narrow(poly.exterior if exterior is None else LinearRing(shell)):
        # (narrow on average, it may be wider pieces that a hairline of no width joins: two
        # slivers of a box beside a pocket, 0.09 mm wide, joined along the pocket's side 6e-14
        # apart, went with it [found by fuzzing the checks, 2026-10-14])
        return _opened(poly) if walls else []
    holes: list[LinearRing | Ring] = []
    changed = exterior is not None
    for ring in poly.interiors:
        kept = _without_spikes(ring)
        if (kept is not None and len(kept) < 4) or _narrow(ring if kept is None else LinearRing(kept)):
            changed = True
            continue
        changed = changed or kept is not None
        holes.append(ring if kept is None else kept)
    if changed:
        made = Polygon(shell, holes)
        if not made.is_valid:
            # (what is left touches or crosses itself where a spike's way back ran along another
            # edge: made valid as an invalid input is, and its pieces cleaned [found by fuzzing,
            # 2026-10-14: a spike 200 mm out, beside an edge in line with it, was kept])
            return _valid_pieces(made, walls) if remake else None
        poly = made
    if walls and len(poly.interiors) > 0 and _has_walls(poly):
        return _opened(poly)
    if _narrow(poly.exterior):
        return []
    return [poly] if changed else None


def _valid_pieces(poly: Polygon, walls: bool) -> list[Polygon]:
    """An invalid polygon made valid (its shells united, as `clean` makes
    an invalid input valid), each piece cleaned."""
    pieces: list[Polygon] = []
    for piece in polygons_of(shapely.make_valid(poly, method="structure", keep_collapsed=False)):
        # (once: a piece that would come out invalid again stays as it is)
        again = _clean_polygon(piece, walls, remake=False)
        pieces.extend([piece] if again is None else again)
    return pieces


def opened(g: BaseGeometry) -> BaseGeometry:
    """`g` cleaned and opened by `SAME_POINT`: parted wherever walls or
    hairlines of no width hold it together, also where an outer ring runs
    along itself (which `clean`, looking for holes along other rings, does
    not see); for regions whose corners count, as the dog bones'. Costs a
    buffer each way, so not for every shape."""
    pieces = [q for poly in polygons_of(clean(g)) for q in _opened(poly)]
    if not pieces:
        return Polygon()
    return pieces[0] if len(pieces) == 1 else MultiPolygon(pieces)


def _opened(poly: Polygon) -> list[Polygon]:
    """The polygon opened by `SAME_POINT`, which parts it where walls or
    hairlines of no width hold it together, each part cleaned."""
    opened = poly.buffer(-SAME_POINT, join_style="mitre", mitre_limit=1e6).buffer(
        SAME_POINT, join_style="mitre", mitre_limit=1e6)
    pieces: list[Polygon] = []
    for piece in polygons_of(opened):
        again = _clean_polygon(piece, walls=False)
        pieces.extend([piece] if again is None else again)
    return pieces


def _narrow(ring: LinearRing) -> bool:
    """Whether the ring encloses less than `NARROWEST` wide on average."""
    length = ring.length
    return length == 0 or 2 * abs(Polygon(ring).area) < NARROWEST * length


def _without_spikes(ring: LinearRing) -> Ring | None:
    """The ring's points (closed, n by 2) without points within
    `SAME_POINT` of the one before and without spike tips, or None when it
    has neither."""
    pts = np.asarray(ring.coords)[:-1, :2]
    changed = False
    while len(pts) >= 3:
        before, after = np.roll(pts, 1, axis=0), np.roll(pts, -1, axis=0)
        come, go, across = pts - before, after - pts, after - before
        repeated = np.hypot(come[:, 0], come[:, 1]) <= SAME_POINT
        span = np.hypot(across[:, 0], across[:, 1])
        off = np.abs(across[:, 0] * come[:, 1] - across[:, 1] * come[:, 0]) / np.maximum(span, 1e-300)
        # (where the points either side coincide the ring runs out and back the same way:
        # a spike of any length [found by fuzzing dog bones, 2026-10-13: one 0.07 mm out,
        # its base points 1e-12 apart, made a corner at one place of the board only])
        off = np.where(span > SAME_POINT, off, 0.0)
        spike = ((come * go).sum(axis=1) < 0) & (off <= SAME_POINT)
        drop = repeated | spike
        if not drop.any():
            break
        drop &= ~np.roll(drop, 1)       # one of each run at a time, so a spike's base stays
        if not drop.any():
            drop[np.argmax(repeated | spike)] = True
        pts = pts[~drop]
        changed = True
    if not changed:
        return None
    return np.concatenate([pts, pts[:1]])


def _has_walls(poly: Polygon) -> bool:
    """Whether a hole runs along the exterior or another hole within
    `_WALL` for more than `NARROWEST`."""
    rings = [poly.exterior, *poly.interiors]
    tree = shapely.STRtree(rings)
    for i, ring in enumerate(rings[1:], start=1):
        for j in tree.query(ring, predicate="dwithin", distance=_WALL):
            if j != i and (j < i or j == 0):
                if ring.intersection(rings[int(j)].buffer(_WALL)).length > NARROWEST:
                    return True
    return False
