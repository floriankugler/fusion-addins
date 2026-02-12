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
    result: Point3D = points[0]
    for p in points[1:]:
        result.x = result.x + p.x
        result.y = result.y + p.y
        result.z = result.z + p.z
    return scaled_by(result.asVector(), 1/len(points)).asPoint()

def transform_point(point: Point3D, t: Matrix3D) -> Point3D:
    copy = point.copy()
    copy.transformBy(t)
    return copy

def compute_points_along_vector(origin: Point3D, direction: Vector3D, positions: list[float]) -> list[Vector3D]:
    normal = normalized(direction)
    return [add(origin.asVector(), scaled_by(normal, x)) for x in positions]

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