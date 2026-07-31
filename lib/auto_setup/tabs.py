"""Manual tab placement along contour loops.

Density is governed by the minimum tab spacing: straight edges receive as many
symmetrically centered tabs as the spacing allows (total roughly perimeter /
spacing). The minimum tab count is a floor that kicks in on small or curvy
contours, where curved edges make up the deficit. All lengths in cm.

Algorithm (per closed loop):
1. Straight edges longer than 2x tab width get k tabs at even fractions
   (k maximal with gap >= max(min_spacing, tab_width)), which also guarantees
   at least one tab width of margin to the edge endpoints.
2. A global pass enforces min spacing along the whole loop (also across edge
   boundaries); on conflict the tab hosted by the shorter edge is dropped.
3. If fewer than min_count tabs result, curved edges (sorted by radius,
   largest first) get one tab at their arc midpoint; a remaining deficit is
   distributed evenly along the largest curve (covers circular contours).
4. If nothing qualifies at all, one tab is placed on the midpoint of the
   longest edge and a warning is emitted.
"""

import adsk.core, adsk.fusion
from dataclasses import dataclass


@dataclass
class _Candidate:
    point: adsk.core.Point3D
    loop_position: float
    is_line: bool
    host_length: float


def compute_tab_points(
    edges: list[adsk.fusion.BRepEdge],
    tab_width: float,
    min_spacing: float,
    min_count: int,
    warnings: list[str],
    label: str,
) -> list[adsk.core.Point3D]:
    if not edges:
        warnings.append(f'{label}: no contour edges found for tab placement.')
        return []

    perimeter = sum(edge.length for edge in edges)
    cumulative = []
    offset = 0.0
    for edge in edges:
        cumulative.append(offset)
        offset += edge.length

    candidates: list[_Candidate] = []
    spacing = max(min_spacing, tab_width)
    for edge, start in zip(edges, cumulative):
        if not adsk.core.Line3D.cast(edge.geometry):
            continue
        length = edge.length
        if length < 2 * tab_width:
            continue
        count = max(1, int(length / spacing) - 1)
        for i in range(count):
            fraction = (i + 1) / (count + 1)
            candidates.append(_Candidate(
                point=_point_at_fraction(edge, fraction),
                loop_position=start + fraction * length,
                is_line=True,
                host_length=length,
            ))

    candidates = _enforce_spacing(candidates, perimeter, min_spacing)

    if len(candidates) < min_count:
        candidates += _curve_tabs(
            edges, cumulative, perimeter, candidates, min_spacing, min_count)

    if not candidates:
        longest = max(edges, key=lambda e: e.length)
        warnings.append(
            f'{label}: no edge qualifies for tabs '
            f'(tab width {tab_width * 10:.1f}mm); placed a single tab on the longest edge.')
        candidates.append(_Candidate(
            point=_point_at_fraction(longest, 0.5),
            loop_position=0.0, is_line=False, host_length=longest.length))
    elif len(candidates) < min_count:
        warnings.append(
            f'{label}: only {len(candidates)} of {min_count} requested tabs fit '
            'with the given spacing.')

    return [c.point for c in candidates]


def _curve_tabs(
    edges: list[adsk.fusion.BRepEdge],
    cumulative: list[float],
    perimeter: float,
    existing: list[_Candidate],
    min_spacing: float,
    min_count: int,
) -> list[_Candidate]:
    curves = []
    for edge, start in zip(edges, cumulative):
        geometry = edge.geometry
        circle = adsk.core.Circle3D.cast(geometry)
        arc = adsk.core.Arc3D.cast(geometry)
        if circle or arc:
            radius = (circle or arc).radius
            curves.append((radius, edge, start))
    curves.sort(key=lambda c: c[0], reverse=True)
    if not curves:
        return []

    added: list[_Candidate] = []

    def try_add(edge, start, fraction):
        candidate = _Candidate(
            point=_point_at_fraction(edge, fraction),
            loop_position=start + fraction * edge.length,
            is_line=False,
            host_length=edge.length,
        )
        for other in existing + added:
            if _loop_distance(candidate.loop_position, other.loop_position, perimeter) < min_spacing:
                return
        added.append(candidate)

    # One tab per curve, largest radius first.
    for _, edge, start in curves:
        if len(existing) + len(added) >= min_count:
            return added
        try_add(edge, start, 0.5)

    # Still short: distribute the deficit evenly along the largest curve,
    # relative to the midpoint tab placed above (covers circular contours).
    deficit = min_count - len(existing) - len(added)
    if deficit > 0:
        _, edge, start = curves[0]
        for i in range(deficit):
            if len(existing) + len(added) >= min_count:
                break
            try_add(edge, start, (0.5 + (i + 1) / (deficit + 1)) % 1.0)
    return added


def _enforce_spacing(candidates: list[_Candidate], perimeter: float,
                     min_spacing: float) -> list[_Candidate]:
    """Drop tabs closer than min_spacing along the loop, shorter host edge first."""
    remaining = sorted(candidates, key=lambda c: c.loop_position)
    while len(remaining) > 1:
        conflict = None
        for idx in range(len(remaining)):
            a = remaining[idx]
            b = remaining[(idx + 1) % len(remaining)]
            if a is b:
                continue
            if _loop_distance(a.loop_position, b.loop_position, perimeter) < min_spacing:
                conflict = (a, b)
                break
        if not conflict:
            break
        a, b = conflict
        # Keep the tab hosted by the longer edge (lines beat curves); on equal
        # priority drop the later tab, so alternating tabs survive.
        priority_a = (a.is_line, a.host_length)
        priority_b = (b.is_line, b.host_length)
        remaining.remove(b if priority_b <= priority_a else a)
    return remaining


def _loop_distance(pos_a: float, pos_b: float, perimeter: float) -> float:
    delta = abs(pos_a - pos_b) % perimeter
    return min(delta, perimeter - delta)


def _point_at_fraction(edge: adsk.fusion.BRepEdge, fraction: float) -> adsk.core.Point3D:
    evaluator = edge.evaluator
    _, param_min, _ = evaluator.getParameterExtents()
    _, param = evaluator.getParameterAtLength(param_min, fraction * edge.length)
    _, point = evaluator.getPointAtParameter(param)
    return point
