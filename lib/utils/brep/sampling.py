"""Probe points for testing what geometry lies along an edge.

Every "does this face mate with that edge" test in the joinery add-ins works
by sampling points along the edge and asking whether they land on a candidate
face. How those samples are laid out decides which joints can be found at all,
so the layout lives here rather than being re-derived at each call site.
"""

import math
from .. import vector
import adsk.core, adsk.fusion
from adsk.core import Point3D, Vector3D

# Fusion's internal length unit is cm, so this is a 1 cm target spacing: a
# mating face shorter than that along the edge can slip between the samples.
# The cap keeps the spacing at 1 cm for edges up to 2 m, which covers any
# sheet-good board, and degrades gracefully beyond that.
PROBE_SPACING = 1.0
MIN_PROBE_COUNT = 9
MAX_PROBE_COUNT = 201


def probe_count_for_edge(
    edge: adsk.fusion.BRepEdge,
    spacing: float = PROBE_SPACING,
    min_count: int = MIN_PROBE_COUNT,
    max_count: int = MAX_PROBE_COUNT,
) -> int:
    if spacing <= 0:
        return min_count
    return max(min_count, min(max_count, math.ceil(edge.length / spacing)))


def sample_points_along_edge(
    edge: adsk.fusion.BRepEdge,
    count: int | None = None,
    offset: Vector3D | None = None,
) -> list[Point3D]:
    """Points spread evenly over the whole edge, never on an end vertex.

    The samples sit at the centres of `count` equal sub-segments. Sampling the
    vertices instead would put two of the probes exactly on the edge's
    boundary, where containment is decided by tolerance rather than geometry,
    and would waste them on the two spots a shorter mating face is least
    likely to reach.

    `offset` is added to every point, e.g. to lift the probes off the edge and
    onto an adjacent face.
    """
    if count is None:
        count = probe_count_for_edge(edge)
    if count < 1:
        return []
    evaluator = edge.evaluator
    ok, lower, upper = evaluator.getParameterExtents()
    if not ok:
        return []
    params = [
        lower + (upper - lower) * ((i + 0.5) / count) for i in range(count)
    ]
    ok, points = evaluator.getPointsAtParameters(params)
    if not ok or not points:
        return []
    if offset is None:
        return list(points)
    return [
        vector.add(p.asVector(), offset).asPoint() for p in points
    ]
