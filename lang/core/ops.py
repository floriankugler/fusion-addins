"""Operations on a part, as stored in its layout.

Positions are in the part's (u, v) frame, the frame of its outline. `face`
names the face the operation is made from, by world direction. Depths are
resolved to millimetres from the face, with the original spec kept.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .shapes import Shape


@dataclass
class Cut:
    """A through cut; it has already been subtracted from the outline."""
    shape: Shape
    name: str | None = None
    chamfer: float = 0.0

    kind = "cut"


@dataclass
class Pocket:
    shape: Shape
    face: str
    depth: float
    depth_spec: str
    name: str | None = None
    chamfer: float = 0.0

    kind = "pocket"


@dataclass
class Hole:
    u: float
    v: float
    d: float
    face: str
    depth: float
    depth_spec: str
    name: str | None = None
    chamfer: float = 0.0
    through: bool = False

    kind = "hole"


@dataclass
class Chamfer:
    #: An edge name (`front.inner`), `outline`, or an operation's name.
    what: str
    size: float
    face: str

    kind = "chamfer"


@dataclass
class EdgeOp:
    """An operation on a narrow face, positioned in that face's own (s, t)
    frame: s along the face, t across the thickness."""
    face: str
    op: Hole | Pocket
    s: float = 0.0
    t: float = 0.0

    kind = "edge"


Op = Cut | Pocket | Hole | Chamfer | EdgeOp
