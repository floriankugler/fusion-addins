"""Taking shapely's results apart.

A boolean or a section in shapely returns a polygon, a multi-polygon, a
line, a collection of all of these, or an empty geometry, depending on
what it found. These two functions give the pieces in one form, so callers
need not ask which kind came back.
"""
from __future__ import annotations

from shapely.geometry import MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry


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
