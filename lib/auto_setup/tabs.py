"""Manual tab placement along contour loops.

Tab count is derived from the contour length with degressive density: short
contours get one tab per DENSITY_SHORT spacing, and the spacing widens
linearly up to DENSITY_LONG for long contours (clamped beyond the reference
lengths, so very large parts still gain tabs slowly). A configurable minimum
count is the floor, so even very small parts are held safely.

Placement: the tabs are distributed evenly around the contour perimeter,
anchored at the middle of the longest usable stretch. Tabs keep one tab width
of clearance from ordinary (convex) corners, and three tab widths from inner
(concave) corners - a tab jammed into a concave corner is hard to trim after
milling. When an ideal position falls into a blocked zone, it is snapped to
the minimum allowed distance from the offending corner, preferring the
position closer to the previous tab (smaller gaps over larger ones). If both
directions would collide with an already placed tab, the tab is dropped with
a warning. All lengths in cm.
"""

import adsk.core, adsk.fusion
from bisect import bisect_right

# Tab density references: (contour length, tab spacing), both cm. Spacing is
# interpolated linearly between them and clamped outside.
DENSITY_SHORT = (20.0, 5.0)    # 200mm contour -> one tab per 50mm
DENSITY_LONG = (300.0, 30.0)   # 3000mm contour -> one tab per 300mm

# Corner clearances, in tab widths.
CONVEX_MARGIN_FACTOR = 1.0
CONCAVE_MARGIN_FACTOR = 3.0
# Minimum distance between two tabs, in tab widths.
MIN_SEPARATION_FACTOR = 2.0
# Junctions with less than this turn angle count as smooth, not as corners.
SMOOTH_JUNCTION_SIN = 0.09  # ~5 degrees


def tab_count(perimeter: float, min_count: int) -> int:
    length_short, spacing_short = DENSITY_SHORT
    length_long, spacing_long = DENSITY_LONG
    if perimeter <= length_short:
        spacing = spacing_short
    elif perimeter >= length_long:
        spacing = spacing_long
    else:
        t = (perimeter - length_short) / (length_long - length_short)
        spacing = spacing_short + t * (spacing_long - spacing_short)
    return max(min_count, round(perimeter / spacing))


def compute_tab_points(
    edges: list[adsk.fusion.BRepEdge],
    tab_width: float,
    min_count: int,
    warnings: list[str],
    label: str,
) -> list[adsk.core.Point3D]:
    if not edges:
        warnings.append(f'{label}: no contour edges found for tab placement.')
        return []

    loop = _Loop(edges)
    count = tab_count(loop.perimeter, min_count)
    intervals = _valid_intervals(loop, tab_width)
    if not intervals:
        longest = max(range(len(edges)), key=lambda i: loop.lengths[i])
        warnings.append(
            f'{label}: no edge is long enough for tabs '
            f'(tab width {tab_width * 10:.1f}mm); placed a single tab on the longest edge.')
        return [loop.point_at(loop.cumulative[longest] + loop.lengths[longest] / 2)]

    # Anchor the even distribution at the middle of the longest usable range.
    anchor_start, anchor_end = max(intervals, key=lambda iv: iv[1] - iv[0])
    anchor = (anchor_start + anchor_end) / 2
    spacing = loop.perimeter / count
    min_separation = tab_width * MIN_SEPARATION_FACTOR

    positions = [anchor]
    for i in range(1, count):
        ideal = (anchor + i * spacing) % loop.perimeter
        for candidate in _snap_candidates(ideal, intervals, loop.perimeter):
            if all(_loop_distance(candidate, p, loop.perimeter) >= min_separation
                   for p in positions):
                positions.append(candidate)
                break
    if len(positions) < count:
        warnings.append(
            f'{label}: placed {len(positions)} of {count} tabs '
            '(corner clearances are respected).')

    return [loop.point_at(p) for p in positions]


def _snap_candidates(ideal: float, intervals: list[tuple[float, float]],
                     perimeter: float) -> list[float]:
    """The ideal position if valid; otherwise the nearest valid positions,
    preferring the one behind the ideal (towards the previous tab)."""
    backward, backward_distance = None, float('inf')
    forward, forward_distance = None, float('inf')
    for start, end in intervals:
        if start <= ideal <= end:
            return [ideal]
        distance = (ideal - end) % perimeter
        if distance < backward_distance:
            backward, backward_distance = end, distance
        distance = (start - ideal) % perimeter
        if distance < forward_distance:
            forward, forward_distance = start, distance
    return [c for c in (backward, forward) if c is not None]


def _valid_intervals(loop: '_Loop', tab_width: float) -> list[tuple[float, float]]:
    edge_count = len(loop.edges)
    if edge_count == 1:
        # A single closed edge (circle): the parametric seam is not a corner.
        return [(0.0, loop.perimeter)]
    margins = [_corner_margin(loop, i, tab_width) for i in range(edge_count)]
    intervals = []
    for i in range(edge_count):
        start = loop.cumulative[i] + margins[i]
        end = loop.cumulative[i] + loop.lengths[i] - margins[(i + 1) % edge_count]
        if end > start:
            intervals.append((start, end))
    return intervals


def _corner_margin(loop: '_Loop', junction_index: int, tab_width: float) -> float:
    factor = CONCAVE_MARGIN_FACTOR if loop.is_concave_junction(junction_index) \
        else CONVEX_MARGIN_FACTOR
    return tab_width * factor


def _loop_distance(pos_a: float, pos_b: float, perimeter: float) -> float:
    delta = abs(pos_a - pos_b) % perimeter
    return min(delta, perimeter - delta)


class _Loop:
    """An ordered, direction-corrected view of a closed edge loop."""

    def __init__(self, edges: list[adsk.fusion.BRepEdge]):
        self.edges = edges
        self.lengths = [edge.length for edge in edges]
        self.perimeter = sum(self.lengths)
        self.cumulative = []
        offset = 0.0
        for length in self.lengths:
            self.cumulative.append(offset)
            offset += length
        self.reversed = self._edge_orientations()
        self._normal = None

    def _edge_orientations(self) -> list[bool]:
        """Whether each edge's parametric direction opposes the loop direction,
        determined by which endpoint is shared with the next edge."""
        flags = []
        count = len(self.edges)
        for i, edge in enumerate(self.edges):
            if count == 1 or not edge.startVertex or not edge.endVertex:
                flags.append(False)
                continue
            next_edge = self.edges[(i + 1) % count]
            next_tokens = {v.entityToken for v in (next_edge.startVertex, next_edge.endVertex) if v}
            if edge.endVertex.entityToken in next_tokens:
                flags.append(False)
            elif edge.startVertex.entityToken in next_tokens:
                flags.append(True)
            else:
                flags.append(False)  # disconnected? fall back to parametric order
        return flags

    def point_at(self, position: float) -> adsk.core.Point3D:
        position %= self.perimeter
        index = min(bisect_right(self.cumulative, position) - 1, len(self.edges) - 1)
        fraction = (position - self.cumulative[index]) / self.lengths[index]
        if self.reversed[index]:
            fraction = 1 - fraction
        evaluator = self.edges[index].evaluator
        _, param_min, _ = evaluator.getParameterExtents()
        _, param = evaluator.getParameterAtLength(
            param_min, fraction * self.lengths[index])
        _, point = evaluator.getPointAtParameter(param)
        return point

    def is_concave_junction(self, junction_index: int) -> bool:
        """True if the corner at the start of edge junction_index is concave
        (the angle outside the enclosed shape is less than 180 degrees)."""
        junction = self.cumulative[junction_index]
        epsilon = min(0.05,
                      self.lengths[junction_index] * 0.4,
                      self.lengths[junction_index - 1] * 0.4)
        at = self.point_at(junction).asVector()
        before = self.point_at(junction - epsilon).asVector()
        after = self.point_at(junction + epsilon).asVector()
        incoming = before.copy()
        incoming.scaleBy(-1.0)
        incoming.add(at)  # at - before
        outgoing = after.copy()
        outgoing.subtract(at)
        if incoming.length < 1e-9 or outgoing.length < 1e-9:
            return False
        turn = incoming.crossProduct(outgoing)
        magnitude = turn.length / (incoming.length * outgoing.length)
        if magnitude < SMOOTH_JUNCTION_SIN:
            return False
        return turn.dotProduct(self._loop_normal()) < 0

    def _loop_normal(self) -> adsk.core.Vector3D:
        """Newell normal of the loop, consistent with the traversal direction."""
        if self._normal is None:
            samples = max(32, 8 * len(self.edges))
            points = [self.point_at(i * self.perimeter / samples).asVector()
                      for i in range(samples)]
            normal = adsk.core.Vector3D.create(0, 0, 0)
            for i in range(samples):
                a, b = points[i], points[(i + 1) % samples]
                normal.add(a.crossProduct(b))
            self._normal = normal
        return self._normal
