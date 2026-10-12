"""Face cutout patterns: the defaults and the sizes of the triangle, rhombus
and cross patterns, as the cutouts_native add-in lays them out.

A pattern is laid out in a rectangle `extent_u` by `extent_v`, the inset
outline of the face or a region, with its columns along u:

- Triangles: `rows` rows, alternately pointing up and down, the first and
  last column centred on the rectangle's ends so that they are halved.
  `spacing` is the true gap between neighbours, measured square to their
  sides. With aligned tips each triangle is drawn taller (`apex_height`),
  so that once its tip is rounded with the fillet radius, the tip touches
  the base line of the neighbouring row.
- Rhombuses: `columns` by `rows` cells, a rhombus centred on every corner
  and on every cell's centre, again `spacing` apart square to their sides.
- Cross: two bands along the rectangle's diagonals, `width` wide, leaving
  four wedges.

Shared by cutouts_native and the modeling language (lang/core/cutouts.py).
Plain Python without Fusion imports; the functions take any unit (the
add-in works in cm, the language in mm), the defaults are in mm.
`python3 -m lib.cutout_patterns` runs its self-checks.
"""
import math
from dataclasses import dataclass

# -- defaults, mm ------------------------------------------------------------------

#: Material kept inside the face's outer contour.
OUTER_INSET = 20.0
#: Material kept around each hole, pocket and other feature of the face.
INNER_INSET = 20.0
#: Radius of the cutout's corners; 0 leaves them sharp.
FILLET_RADIUS = 8.0
#: Size of the 45 degree chamfer on the cutout's rims, when chamfered.
CHAMFER = 1.0
COLUMNS = 8
ROWS = 6
#: True gap between neighbouring triangles or rhombuses.
SPACING = 20.0
#: Width of each diagonal band of the cross.
CROSS_WIDTH = 20.0


# -- triangles ----------------------------------------------------------------------

@dataclass(frozen=True)
class Triangles:
    """The size of the triangles in a pattern: the base `width`, the
    `height` of a row, and `apex_height`, how far the sharp apex lies from
    the base (the row height, or more for aligned tips). Columns are
    `pitch_u` apart, rows `pitch_v`."""
    width: float
    height: float
    apex_height: float
    pitch_u: float
    pitch_v: float


def triangle_dimensions(extent_u: float, extent_v: float, columns: int, rows: int,
                        spacing: float) -> tuple[float, float]:
    """The triangles' base width and height for sharp tips. Raises
    ValueError when the pattern does not fit."""
    height = (extent_v - (rows - 1) * spacing) / rows
    if height <= 1e-6:
        raise ValueError("Triangle spacing and row count leave no room for triangle height.")
    # The first triangle is centered on the start boundary and the final
    # triangle is centered on the opposite boundary. The requested column
    # count therefore describes the number of center-to-center pitches
    # across the rectangle:
    #
    #   extent_u = columns * (width / 2 + projected_edge_spacing)
    #
    # Solving that equation for width keeps both clipped end triangles
    # exactly one half wide.
    a = columns / 2
    b = columns * spacing
    coefficient = a * a - b * b / (4 * height * height)
    if abs(coefficient) <= 1e-9:
        raise ValueError("Triangle spacing is too large for the requested columns.")
    discriminant = a * a * extent_u * extent_u - coefficient * (extent_u * extent_u - b * b)
    if discriminant < -1e-8:
        raise ValueError("Triangle spacing is too large for the pattern boundary.")
    width = (a * extent_u - math.sqrt(max(0, discriminant))) / coefficient
    if width <= 1e-6 or extent_u - a * width < -1e-6:
        raise ValueError("The requested triangle pattern does not fit the boundary.")
    return width, height


def aligned_apex_height(width: float, height: float, radius: float) -> float:
    """How far the sharp apex of a triangle `width` wide lies from its base
    when its tip, rounded with `radius`, reaches exactly `height`: the
    tip's circle, centred `radius` below that height on the altitude,
    touches both sides. Raises ValueError when the tip cannot be rounded."""
    half = width / 2
    if half <= 1e-9:
        raise ValueError("The requested triangle pattern has no usable width.")
    if radius >= height - 1e-9:
        raise ValueError("The fillet radius is too large for the triangle tips.")
    # Distance from the centre (0, height - radius) to a side through
    # (half, 0) and (0, H) equals the radius:
    #   half * (H - height + radius) = radius * hypot(half, H),
    # squared: (1 - k) H^2 + 2 c H + c^2 - radius^2 = 0, with
    # k = (radius / half)^2 and c = radius - height.
    k = (radius / half) ** 2
    c = radius - height
    if abs(1 - k) < 1e-12:
        roots = [(radius * radius - c * c) / (2 * c)]
    else:
        disc = k * c * c + (1 - k) * radius * radius
        if disc < 0:
            raise ValueError("The fillet radius is too large for the triangle tips.")
        root = math.sqrt(disc)
        roots = [(-c + root) / (1 - k), (-c - root) / (1 - k)]
    # The squared equation also has the root on the far side of the circle.
    for apex in sorted(roots):
        if apex >= height - 1e-9 and abs(half * (apex + c) - radius * math.hypot(half, apex)) <= 1e-9 * max(1.0, apex):
            return apex
    raise ValueError("The fillet radius is too large for the triangle tips.")


def _gap(width: float, apex: float, height: float, pitch: float) -> float:
    """The true gap between an upward triangle centred at 0 with its base at
    0 and the downward one centred at `pitch` with its base at `height`,
    both `width` wide with their sharp apex `apex` from the base: the
    distance between their facing, parallel sides."""
    return (apex * (pitch - width) + width * height / 2) / math.hypot(apex, width / 2)


def triangles(extent_u: float, extent_v: float, columns: int, rows: int, spacing: float,
              aligned_radius: float | None = None) -> Triangles:
    """The pattern's triangles; with `aligned_radius` the tips are aligned:
    each rounded tip touches the base line of the next row. Raises
    ValueError when the pattern does not fit."""
    width, height = triangle_dimensions(extent_u, extent_v, columns, rows, spacing)
    pitch_u, pitch_v = extent_u / columns, height + spacing
    if aligned_radius is None:
        return Triangles(width, height, height, pitch_u, pitch_v)
    radius = aligned_radius
    if radius >= height - 1e-9:
        raise ValueError("The fillet radius is too large for the triangle tips.")

    def excess(w: float) -> float:
        return _gap(w, aligned_apex_height(w, height, radius), height, pitch_u) - spacing

    # The gap shrinks as the triangles widen. The tips can only be rounded
    # down to a width of about twice the radius; bracket the root between
    # the narrowest width that works and the sharp triangles' width, which
    # leaves too little gap once the apex rises.
    hi = width
    lo = hi
    for _ in range(200):
        lo /= 1.25
        try:
            if excess(lo) > 0:
                break
        except ValueError:
            raise ValueError("The fillet radius is too large for the triangle pattern.") from None
    else:
        raise ValueError("The fillet radius is too large for the triangle pattern.")
    if excess(hi) > 0:
        raise ValueError("The requested triangle pattern does not fit the boundary.")
    for _ in range(200):
        mid = (lo + hi) / 2
        if excess(mid) > 0:
            lo = mid
        else:
            hi = mid
        if hi - lo <= 1e-12 * max(1.0, width):
            break
    w = (lo + hi) / 2
    return Triangles(w, height, aligned_apex_height(w, height, radius), pitch_u, pitch_v)


# -- rhombuses ----------------------------------------------------------------------

def rhombus_dimensions(pitch_u: float, pitch_v: float, spacing: float) -> tuple[float, float]:
    """Solve rhombus width and height from the pitches and the true
    edge-to-edge spacing.

    For a rhombus with diagonals w (along u) and h (along v), the gap
    measured along u between two neighbours is s*hypot(w, h)/h and the
    gap along v is s*hypot(w, h)/w. Requiring pitch_u = w + gap_u and
    pitch_v = h + gap_v forces w/h == pitch_u/pitch_v, which reduces to
    the closed form below.
    """
    if pitch_u <= 0 or pitch_v <= 0:
        raise ValueError("The pattern boundary has no usable extent.")
    ratio = pitch_u / pitch_v
    height = pitch_v - spacing * math.sqrt(1 + ratio * ratio) / ratio
    width = ratio * height
    return width, height


# -- cross ---------------------------------------------------------------------------

def cross_max_width(extent_u: float, extent_v: float) -> float:
    """The widest the cross's bands may be: twice the distance from the
    middle of a side to the diagonal it is nearest."""
    return extent_u * extent_v / math.hypot(extent_u, extent_v)


def _self_check() -> None:
    w, h = triangle_dimensions(560, 360, 8, 6, 20)
    assert abs(h - (360 - 5 * 20) / 6) < 1e-12
    # 8 pitches of width/2 plus the gap measured along u span the rectangle
    assert abs(8 * (w / 2 + 20 * math.hypot(h, w / 2) / h) - 560) < 1e-9
    sharp = triangles(560, 360, 8, 6, 20)
    assert abs(_gap(sharp.width, sharp.apex_height, sharp.height, sharp.pitch_u) - 20) < 1e-9
    aligned = triangles(560, 360, 8, 6, 20, aligned_radius=8)
    assert aligned.apex_height > aligned.height
    assert abs(_gap(aligned.width, aligned.apex_height, aligned.height, aligned.pitch_u) - 20) < 1e-9
    # the rounded tip's centre lies one radius from both sides
    half, apex = aligned.width / 2, aligned.apex_height
    centre = aligned.height - 8
    assert abs(half * (apex - centre) / math.hypot(half, apex) - 8) < 1e-9
    rw, rh = rhombus_dimensions(70, 60, 20)
    assert abs(rw / rh - 70 / 60) < 1e-12
    assert abs(cross_max_width(3, 4) - 2.4) < 1e-12
    print("cutout_patterns: all checks passed")


if __name__ == "__main__":
    _self_check()
