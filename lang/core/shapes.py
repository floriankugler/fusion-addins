"""2D shapes in a local (u, v) frame, in millimetres, backed by shapely.

A rectangle names its extents the way the project names them,
`rect(depth=60, height=100)`, and so knows which two world axes it lies in;
when it is placed on a face, `in_plane` turns it so that its u and v are the
face's axes, or fails when the face lies in another plane. A circle has no
orientation, and `polygon(points)` is the raw escape hatch whose u and v are
the face's axes in x, y, z order.

A shape is placed on a face with an `Anchor`: which point of its bounding
box (a corner, the middle of an edge, the centre) goes onto the face's
point; the face maps the direction names it was given to u and v.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import cast

from shapely import affinity, maximum_inscribed_circle
from shapely.geometry import MultiPolygon, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from . import directions
from .cutouts import arc_points, circle_geometry, filleted
from .directions import AXES, Axis, ExtentName
from .errors import LangError
from .geometry import clean

Ring = list[tuple[float, float]]
#: The two world axes a shape's u and v are bound to, or None for a raw shape.
Axes = tuple[Axis, Axis] | None
#: A raw shape's edges (it has no plane until it is placed): left and right
#: along u, bottom and top along v, each with whether it is the high end.
_RAW_EDGES: dict[str, tuple[int, bool]] = {"left": (0, False), "right": (0, True),
                                           "bottom": (1, False), "top": (1, True)}


@dataclass(frozen=True)
class Anchor:
    """A point of a shape's bounding box as fractions (0, 0.5 or 1) of its
    extent, plus which edges it names."""
    fu: float
    fv: float
    names_u: bool
    names_v: bool


class Shape:
    def __init__(self, geometry: BaseGeometry, axes: Axes = None):
        geometry = clean(geometry)          # what booleans of coincident edges leave (`geometry.clean`)
        if isinstance(geometry, MultiPolygon) and len(geometry.geoms) == 1:
            geometry = geometry.geoms[0]
        self.geometry: BaseGeometry = geometry
        self.axes: Axes = axes

    def _derived(self, geometry: BaseGeometry, other: Shape | None = None) -> Shape:
        """A shape made from this one (and `other`), keeping the axes."""
        axes = self.axes
        if other is not None and other.axes is not None:
            if axes is not None and other.axes != axes:
                raise LangError(f"Shapes lie in different planes: {_plane(axes)} and {_plane(other.axes)}.")
            axes = other.axes
        return Shape(geometry, axes)

    def in_plane(self, u: Axis, v: Axis, path: str | None = None) -> Shape:
        """This shape with its u and v along the world axes `u` and `v`: as
        it is for a raw shape, turned over when its extents were named the
        other way round, an error when it lies in another plane."""
        if self.axes is None or self.axes == (u, v):
            return self
        if self.axes == (v, u):
            return Shape(affinity.affine_transform(self.geometry, [0, 1, 1, 0, 0, 0]), (u, v))
        raise LangError(
            f"a shape in {_plane(self.axes)} cannot be placed on a face in {_plane((u, v))}.", path)

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        x0, y0, x1, y1 = self.geometry.bounds
        return (float(x0), float(y0), float(x1), float(y1))

    @property
    def width(self) -> float:
        b = self.bounds
        return b[2] - b[0]

    @property
    def height(self) -> float:
        b = self.bounds
        return b[3] - b[1]

    @property
    def area(self) -> float:
        return float(self.geometry.area)

    def anchor_point(self, anchor: Anchor) -> tuple[float, float]:
        x0, y0, x1, y1 = self.bounds
        return (x0 + anchor.fu * (x1 - x0), y0 + anchor.fv * (y1 - y0))

    def moved(self, du: float, dv: float) -> Shape:
        return self._derived(affinity.translate(self.geometry, du, dv))

    def union(self, other: Shape) -> Shape:
        return self._derived(unary_union([self.geometry, other.geometry]), other)

    def difference(self, other: Shape) -> Shape:
        return self._derived(self.geometry.difference(other.geometry), other)

    def intersection(self, other: Shape) -> Shape:
        return self._derived(self.geometry.intersection(other.geometry), other)

    def offset(self, distance: float) -> Shape:
        """Outward offset (negative inward), with sharp corners kept."""
        return self._derived(self.geometry.buffer(distance, join_style="mitre"))

    def clip(self, *, front: float | None = None, back: float | None = None, left: float | None = None,
             right: float | None = None, top: float | None = None, bottom: float | None = None) -> Shape:
        """Cuts a corner off along a diagonal. The corner is named by its
        two edges, each with the length of the cut along it:
        `rect(depth=500, height=720).clip(top=380, back=120)` takes a
        triangle off the top back corner whose legs run 380 along the top
        edge and 120 along the back edge. A rectangle's edges are named as
        the frame names the plane it lies in (front and back along the
        depth...); a raw shape (`polygon`, `circle`), which has no plane
        until it is placed, has left and right along u, bottom and top
        along v."""
        named = {n: s for n, s in (("front", front), ("back", back), ("left", left), ("right", right),
                                   ("top", top), ("bottom", bottom)) if s is not None}
        if len(named) != 2:
            raise LangError(f"clip: name the corner by its two edges with the cut's length along each, "
                            f"e.g. clip(top=380, back=120); got {', '.join(named) or 'none'}.")
        legs: dict[int, tuple[bool, float]] = {}       # per axis (0 u, 1 v): the edge's end, the leg along it
        for name, size in named.items():
            if size <= 0:
                raise LangError(f"clip: {name}={size:g}; the leg must be positive.")
            index, high = self._edge(name)
            if index in legs:
                raise LangError(f"clip: {', '.join(named)} lie on one axis; name two edges that meet at a corner.")
            legs[index] = (high, size)
        (high_u, along_v), (high_v, along_u) = legs[0], legs[1]   # the u edge runs along v, and the v edge along u
        x0, y0, x1, y1 = self.bounds
        cx, cy = (x1 if high_u else x0), (y1 if high_v else y0)
        su, sv = (-1 if high_u else 1), (-1 if high_v else 1)
        triangle = Polygon([(cx, cy), (cx + su * along_u, cy), (cx, cy + sv * along_v)])
        return self._derived(self.geometry.difference(triangle))

    def _edge(self, name: str) -> tuple[int, bool]:
        """Which axis (0 u, 1 v) an edge named by direction is the end of,
        and whether it is the high end."""
        if self.axes is None:
            if name not in _RAW_EDGES:
                raise LangError(f"clip: a raw shape has no plane yet, so its edges are left, right, bottom and "
                                f"top, not {name}.")
            return _RAW_EDGES[name]
        d = directions.current_frame().direction(name)
        if d.axis not in self.axes:
            raise LangError(f"clip: {name} is not an edge of a shape in {_plane(self.axes)}.")
        return self.axes.index(d.axis), d.sign > 0

    def rounded(self, radius: float) -> Shape:
        """Rounds every corner with `radius`, convex and concave alike: as a
        cutter of that radius leaves the inside corners of a pocket or cut
        in this shape (its convex ones) or of a board with this outline
        (its concave ones). The arcs are exact, worked out on the lines and
        arcs the shape stands for, as the cutouts' fillets are.

        Half the shape's narrow width rounds its ends fully, so
        `rect(depth=80, width=12).rounded(6)` is a slot. A larger radius,
        no circle of which fits in the shape, is an error, and so is one
        too large for an edge between two corners."""
        if radius < 0:
            raise LangError(f"rounded({radius:.10g}): the radius must not be negative.")
        if radius == 0:
            return self
        pieces: list[Polygon] = []
        for poly in self.polygons():
            # A polygon standing for an arc lies inside it by up to half a
            # percent of the radius, so a circle rounded with its own radius
            # fits; a shape with corners fits within 1e-7 (`filleted`).
            fits = not poly.buffer(-radius * 0.994, join_style="round").is_empty
            out = filleted(poly, radius) if fits else None
            if out is None:
                if not fits or poly.buffer(-radius, join_style="round").is_empty:
                    width = 2 * float(maximum_inscribed_circle(poly).length)
                    raise LangError(
                        f"rounded({radius:.10g}): the radius is more than half the shape's narrow width "
                        f"({round(width, 1):g}, the largest circle in it), so nothing would be left.")
                raise LangError(
                    f"rounded({radius:.10g}): an edge of the shape is too short for the arcs at its ends, "
                    "so not every corner can be rounded with it.")
            pieces.append(out)
        return self._derived(unary_union(pieces)) if pieces else self

    # -- export ---------------------------------------------------------------------

    def polygons(self) -> list[Polygon]:
        g = self.geometry
        if isinstance(g, MultiPolygon):
            return list(g.geoms)
        if isinstance(g, Polygon):
            return [g]
        if g.is_empty:
            return []
        raise LangError(f"Shape is not an area: {g.geom_type}.")

    def rings(self) -> list[Ring]:
        """Exterior ring first, then holes, each as a list of (u, v)."""
        out: list[Ring] = []
        for poly in self.polygons():
            out.append([(float(x), float(y)) for x, y in cast(list[tuple[float, float]], list(poly.exterior.coords))[:-1]])
            for hole in poly.interiors:
                out.append([(float(x), float(y)) for x, y in cast(list[tuple[float, float]], list(hole.coords))[:-1]])
        return out

    def is_empty(self) -> bool:
        return bool(self.geometry.is_empty)

    def __repr__(self) -> str:
        x0, y0, x1, y1 = self.bounds
        plane = f" in {_plane(self.axes)}" if self.axes else ""
        return f"Shape({x1 - x0:g} x {y1 - y0:g}{plane})"


def _extent_name(axis: Axis) -> str:
    for name, a in directions.current_frame().extents.items():
        if a == axis:
            return name
    return axis


def _plane(axes: tuple[Axis, Axis]) -> str:
    return f"{_extent_name(axes[0])} x {_extent_name(axes[1])}"


def box_shape(u0: float, v0: float, u1: float, v1: float, axes: Axes = None) -> Shape:
    """A raw rectangle by its corners in a (u, v) frame; for internal use,
    build files say `rect(depth=..., height=...)`."""
    return Shape(shapely_box(u0, v0, u1, v1), axes)


def rect(*, width: float | None = None, depth: float | None = None, height: float | None = None) -> Shape:
    """A rectangle with its extents named as the project names them, two of
    `width`, `depth` and `height`, e.g. `rect(depth=60, height=100)`. It
    lies in the plane of those two axes and can only be placed on a face in
    that plane. Its corner nearest the origin sits at (0, 0)."""
    candidates: list[tuple[ExtentName, float | None]] = [("width", width), ("depth", depth), ("height", height)]
    given: dict[ExtentName, float] = {name: size for name, size in candidates if size is not None}
    if len(given) != 2:
        raise LangError("rect: name exactly two extents, e.g. rect(depth=60, height=100).")
    for name, size in given.items():
        if size <= 0:
            raise LangError(f"rect: {name} must be positive, got {size}.")
    f = directions.current_frame()
    by_axis: dict[Axis, float] = {f.axis_of_extent(name): float(size) for name, size in given.items()}
    if len(by_axis) != 2:
        raise LangError("rect: the two extents name the same axis in this frame.")
    u, v = cast(tuple[Axis, Axis], tuple(sorted(by_axis, key=AXES.index)))
    return box_shape(0.0, 0.0, by_axis[u], by_axis[v], (u, v))


def slot_shape(start: tuple[float, float], end: tuple[float, float], width: float) -> Shape:
    """A raw slot: the line from `start` to `end` widened to `width`, with
    round ends drawn as every circle is (`circle`); for joints and
    hardware, which compute their own positions."""
    r = width / 2
    length = math.dist(start, end)
    if length == 0:
        return circle(width, start)
    nx, ny = -(end[1] - start[1]) / length * r, (end[0] - start[0]) / length * r      # across, to the left
    ends = [arc_points(end, r, (end[0] - nx, end[1] - ny), (end[0] + nx, end[1] + ny), True, math.pi),
            arc_points(start, r, (start[0] + nx, start[1] + ny), (start[0] - nx, start[1] - ny), True, math.pi)]
    return Shape(Polygon(ends[0] + ends[1]))


def circle(diameter: float, center: tuple[float, float] = (0.0, 0.0)) -> Shape:
    """A circle, its vertices on the whole degrees about its centre, as every
    circle and arc the language makes, so that two drawings of one circle
    coincide (`cutouts.circle_geometry`)."""
    return Shape(circle_geometry((float(center[0]), float(center[1])), diameter / 2.0))


def polygon(points: list[tuple[float, float]]) -> Shape:
    """A raw point list, the escape hatch: u and v are the face's two world
    axes in x, y, z order."""
    return Shape(Polygon([(float(u), float(v)) for u, v in points]))
