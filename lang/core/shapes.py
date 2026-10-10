"""2D shapes in a local (u, v) frame, in millimetres, backed by shapely.

A rectangle names its extents the way the project names them,
`rect(depth=60, height=100)`, and so knows which two world axes it lies in;
when it is placed on a face, `in_plane` turns it so that its u and v are the
face's axes, or fails when the face lies in another plane. A circle has no
orientation, and `polygon(points)` is the raw escape hatch whose u and v are
the face's axes in x, y, z order.

Anchors of a shape are named in the 2D sense: `left`/`right` along u,
`bottom`/`top` along v, `center`, and corners such as `bottom.left`. When a
shape is placed on a face of a part, the face maps world direction names
to u and v.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from shapely import affinity
from shapely.geometry import MultiPolygon, Point, Polygon
from shapely.geometry import box as shapely_box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from . import directions
from .directions import AXES, Axis
from .errors import LangError

Ring = list[tuple[float, float]]
#: The two world axes a shape's u and v are bound to, or None for a raw shape.
Axes = tuple[Axis, Axis] | None
_ANCHOR_U: dict[str, float] = {"left": 0.0, "right": 1.0}
_ANCHOR_V: dict[str, float] = {"bottom": 0.0, "top": 1.0}


@dataclass(frozen=True)
class Anchor:
    """A point of a shape's bounding box as fractions (0, 0.5 or 1) of its
    extent, plus which edges it names."""
    fu: float
    fv: float
    names_u: bool
    names_v: bool


def parse_anchor(name: str, u_names: dict[str, float] = _ANCHOR_U,
                 v_names: dict[str, float] = _ANCHOR_V) -> Anchor:
    """Parses `"center"`, `"left"`, `"top"`, `"bottom.left"` and the like.
    The dictionaries map edge names to 0 or 1 on their axis, so a face can
    pass world direction names instead of the 2D defaults."""
    if name == "center":
        return Anchor(0.5, 0.5, False, False)
    fu, fv = 0.5, 0.5
    names_u = names_v = False
    for part in name.split("."):
        if part in u_names:
            if names_u:
                raise LangError(f"Anchor {name!r} names two edges on the same axis.")
            fu, names_u = u_names[part], True
        elif part in v_names:
            if names_v:
                raise LangError(f"Anchor {name!r} names two edges on the same axis.")
            fv, names_v = v_names[part], True
        else:
            raise LangError(
                f"Anchor {name!r}: {part!r} is not an edge of this face; "
                f"expected {', '.join(list(u_names) + list(v_names))} or center."
            )
    return Anchor(fu, fv, names_u, names_v)


class Shape:
    def __init__(self, geometry: BaseGeometry, axes: Axes = None):
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

    def clip(self, corner: str, **sizes: float) -> Shape:
        """Cuts a corner off along a diagonal. `corner` names a corner in the
        2D sense (`"top.right"`) and `sizes` the leg lengths along the two
        edges it names, keyed by those edge names: `.clip("top.right", top=380,
        right=120)` removes a triangle whose legs run 380 along the top edge
        and 120 down the right edge."""
        anchor = parse_anchor(corner)
        if not (anchor.names_u and anchor.names_v):
            raise LangError(f"clip: {corner!r} is not a corner.")
        u_edge = next(n for n in corner.split(".") if n in _ANCHOR_U)
        v_edge = next(n for n in corner.split(".") if n in _ANCHOR_V)
        try:
            along_u = sizes[v_edge]   # the leg along the top/bottom edge runs in u
            along_v = sizes[u_edge]   # the leg along the left/right edge runs in v
        except KeyError as missing:
            raise LangError(f"clip: give the leg length along {missing.args[0]!r}.") from None
        cx, cy = self.anchor_point(anchor)
        su = -1 if anchor.fu > 0.5 else 1
        sv = -1 if anchor.fv > 0.5 else 1
        triangle = Polygon([(cx, cy), (cx + su * along_u, cy), (cx, cy + sv * along_v)])
        return self._derived(self.geometry.difference(triangle))

    def rounded(self, radius: float) -> Shape:
        """Rounds every corner, the inside ones as a cutter would leave
        them."""
        g = self.geometry.buffer(-radius, join_style="round").buffer(radius, join_style="round")
        return self._derived(g)

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
    for name, a in directions.frame.extents.items():
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
    given = {name: size for name, size in (("width", width), ("depth", depth), ("height", height))
             if size is not None}
    if len(given) != 2:
        raise LangError("rect: name exactly two extents, e.g. rect(depth=60, height=100).")
    for name, size in given.items():
        if size <= 0:
            raise LangError(f"rect: {name} must be positive, got {size}.")
    by_axis: dict[Axis, float] = {directions.frame.axis_of_extent(name): float(size)
                                  for name, size in given.items()}
    if len(by_axis) != 2:
        raise LangError("rect: the two extents name the same axis in this frame.")
    u, v = cast(tuple[Axis, Axis], tuple(sorted(by_axis, key=AXES.index)))
    return box_shape(0.0, 0.0, by_axis[u], by_axis[v], (u, v))


def circle(diameter: float, center: tuple[float, float] = (0.0, 0.0), resolution: int = 32) -> Shape:
    return Shape(Point(*center).buffer(diameter / 2.0, resolution=resolution))


def polygon(points: list[tuple[float, float]]) -> Shape:
    """A raw point list, the escape hatch: u and v are the face's two world
    axes in x, y, z order."""
    return Shape(Polygon([(float(u), float(v)) for u, v in points]))
