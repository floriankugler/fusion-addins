from adsk.core import Matrix3D, Vector3D, Point3D

def scaled_by(vector: Vector3D, multiplier: float) -> Vector3D:
    result = vector.copy()
    result.scaleBy(multiplier)
    return result

def subtract(v1: Vector3D, v2: Vector3D) -> Vector3D:
    result = v1.copy()
    result.subtract(v2)
    return result

def add(v1: Vector3D, v2: Vector3D) -> Vector3D:
    result = v1.copy()
    result.add(v2)
    return result

def normalized(v: Vector3D) -> Vector3D:
    result = v.copy()
    result.normalize()
    return result

def dot_product(v1: Vector3D, v2: Vector3D) -> float:
    return v1.dotProduct(v2)

def center(points: list[Point3D]) -> Point3D:
    if not points:
        raise ValueError("points must not be empty")
    result = points[0].copy()
    for p in points[1:]:
        result.x = result.x + p.x
        result.y = result.y + p.y
        result.z = result.z + p.z
    return scaled_by(result.asVector(), 1 / len(points)).asPoint()

def transform_point(point: Point3D, t: Matrix3D) -> Point3D:
    copy = point.copy()
    copy.transformBy(t)
    return copy

def compute_points_along_vector(origin: Point3D, direction: Vector3D, positions: list[float]) -> list[Vector3D]:
    normal = normalized(direction)
    return [add(origin.asVector(), scaled_by(normal, x)) for x in positions]

# Angular slack, in radians, for the parallel/perpendicular tests below.
#
# Fusion's own Vector3D.isParallelTo/isPerpendicularTo compare exactly, so
# they report False for real modelled geometry: normals carry rounding noise
# from the modelling history, and a face normal of (1, 1.3e-11, 0) is not
# exactly perpendicular to (0, -1, 0). Observed noise in production designs
# is around 1e-11 rad; this leaves five orders of magnitude of headroom while
# staying far below any intentional angle (1e-6 rad is 6e-5 degrees).
ANGLE_TOLERANCE = 1e-6

def is_parallel_direction(v1: Vector3D, v2: Vector3D, tolerance: float = ANGLE_TOLERANCE) -> bool:
    """True when the vectors point along the same line, either way round.

    Uses the cross product rather than the dot product: near parallel the
    cross product grows linearly with the angle, so the tolerance means the
    same thing here as in is_perpendicular_direction, whereas |dot| - 1 goes
    quadratic and would make the tolerance angle-dependent.
    """
    a = normalized(v1)
    b = normalized(v2)
    return a.crossProduct(b).length <= tolerance

def is_perpendicular_direction(v1: Vector3D, v2: Vector3D, tolerance: float = ANGLE_TOLERANCE) -> bool:
    a = normalized(v1)
    b = normalized(v2)
    return abs(a.dotProduct(b)) <= tolerance

def is_equal_direction(v1: Vector3D, v2: Vector3D, tolerance: float = 1e-6) -> bool:
    v1n = normalized(v1)
    v2n = normalized(v2)
    dot = v1n.dotProduct(v2n)
    return abs(dot - 1.0) <= tolerance

def is_opposite_direction(v1: Vector3D, v2: Vector3D, tolerance: float = 1e-6) -> bool:
    v1n = normalized(v1)
    v2n = normalized(v2)
    dot = v1n.dotProduct(v2n)
    return abs(dot + 1.0) <= tolerance

def inverted(v: Vector3D) -> Vector3D:
    result = v.copy()
    result.scaleBy(-1)
    return result

def average(v1: Vector3D, v2: Vector3D) -> Vector3D:
    return scaled_by(add(v1, v2), 0.5)
