"""2D shapes in a local (u, v) frame, in millimetres, backed by shapely.

A shape has no world directions of its own. Its anchors are named in the
2D sense: `left`/`right` along u, `bottom`/`top` along v, `center`, and
corners such as `bottom.left`. When a shape is placed on a face of a part,
the face maps world direction names to u and v.
"""
from __future__ import annotations

from dataclasses import dataclass

from shapely import affinity
from shapely.geometry import Polygon, MultiPolygon, Point, box as shapely_box
from shapely.ops import unary_union

from .errors import LangError

_ANCHOR_U = {"left": 0.0, "right": 1.0}
_ANCHOR_V = {"bottom": 0.0, "top": 1.0}


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
    def __init__(self, geometry):
        if isinstance(geometry, MultiPolygon):
            if len(geometry.geoms) == 1:
                geometry = geometry.geoms[0]
        self.geometry = geometry

    # -- construction ------------------------------------------------------

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        return self.geometry.bounds

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
        return self.geometry.area

    def anchor_point(self, anchor: Anchor) -> tuple[float, float]:
        x0, y0, x1, y1 = self.bounds
        return (x0 + anchor.fu * (x1 - x0), y0 + anchor.fv * (y1 - y0))

    def moved(self, du: float, dv: float) -> "Shape":
        return Shape(affinity.translate(self.geometry, du, dv))

    def union(self, other: "Shape") -> "Shape":
        return Shape(unary_union([self.geometry, other.geometry]))

    def difference(self, other: "Shape") -> "Shape":
        return Shape(self.geometry.difference(other.geometry))

    def intersection(self, other: "Shape") -> "Shape":
        return Shape(self.geometry.intersection(other.geometry))

    def offset(self, distance: float) -> "Shape":
        """Outward offset (negative inward), with sharp corners kept."""
        return Shape(self.geometry.buffer(distance, join_style="mitre"))

    def clip(self, corner: str, **sizes: float) -> "Shape":
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
        return Shape(self.geometry.difference(triangle))

    def rounded(self, radius: float) -> "Shape":
        """Rounds every corner, the inside ones as a cutter would leave
        them."""
        g = self.geometry.buffer(-radius, join_style="round").buffer(radius, join_style="round")
        return Shape(g)

    # -- export ------------------------------------------------------------

    def rings(self) -> list[list[tuple[float, float]]]:
        """Exterior ring first, then holes, each as a list of (u, v)."""
        polys = self.geometry.geoms if isinstance(self.geometry, MultiPolygon) else [self.geometry]
        out = []
        for poly in polys:
            out.append([tuple(map(float, p)) for p in poly.exterior.coords[:-1]])
            for hole in poly.interiors:
                out.append([tuple(map(float, p)) for p in hole.coords[:-1]])
        return out

    def polygons(self) -> list[Polygon]:
        return list(self.geometry.geoms) if isinstance(self.geometry, MultiPolygon) else [self.geometry]

    def is_empty(self) -> bool:
        return self.geometry.is_empty

    def __repr__(self) -> str:
        x0, y0, x1, y1 = self.bounds
        return f"Shape({x1 - x0:g} x {y1 - y0:g})"


def rect(width: float, height: float) -> Shape:
    """A rectangle with its bottom-left corner at the origin."""
    if width <= 0 or height <= 0:
        raise LangError(f"rect: width and height must be positive ({width} x {height}).")
    return Shape(shapely_box(0.0, 0.0, float(width), float(height)))


def circle(diameter: float, center=(0.0, 0.0), resolution: int = 32) -> Shape:
    return Shape(Point(*center).buffer(diameter / 2.0, resolution=resolution))


def polygon(points) -> Shape:
    """A raw point list, the escape hatch."""
    return Shape(Polygon([(float(u), float(v)) for u, v in points]))
