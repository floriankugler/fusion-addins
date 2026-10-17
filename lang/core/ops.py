"""Operations on a part, as stored in its layout.

Positions are in the part's (u, v) frame, the frame of its outline. `face`
names the face the operation is made from, by world direction. Depths are
resolved to millimetres from the face; `depth_spec` keeps how the build
file gave it (`"through"`, `"to(outer, leave=3)"`, `"10"`), for a reader of the
layout file only: no consumer interprets it. `where` is the build file's
line that made the operation, a join's or a mount's for what they make;
it takes no part in comparing operations.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .shapes import Shape, circle

#: The smallest chamfer (mm) an operation takes, besides 0 for none: Fusion
#: fails on far smaller ones (6e-5 mm, compiling fuzz boards 2026-10-12),
#: and a hundredth of a millimetre is less than any tool leaves anyway.
MIN_CHAMFER = 0.01


@dataclass(frozen=True)
class DogBone:
    """A dog bone in a cut's or pocket's shape (`lang.core.dogbones`): the
    circle drawn as a relief, its centre in the shape's frame and its
    diameter, for a cutter of `tool` mm. The shape has it already; this
    says what it is, for the CAM plan, which mills it with a dog bone
    cutter where the operation's own is too wide."""
    center: tuple[float, float]
    d: float
    tool: float

    @property
    def shape(self) -> Shape:
        return circle(self.d, self.center)


@dataclass
class Cut:
    """A through cut; it has already been subtracted from the outline."""
    shape: Shape
    name: str | None = None
    chamfer: float = 0.0
    #: The dog bones its shape holds.
    dogbones: tuple[DogBone, ...] = ()
    kind: Literal["cut"] = "cut"
    #: The build file's line that made it (`lang.core.where`), set when the board records it.
    where: str = field(default="", compare=False, repr=False)


@dataclass(frozen=True)
class SlotLine:
    """A slot's centre line: the centres of its round ends, in the frame of
    the face it is cut from, and its width."""
    start: tuple[float, float]
    end: tuple[float, float]
    width: float


@dataclass
class Pocket:
    shape: Shape
    face: str
    depth: float
    depth_spec: str
    name: str | None = None
    chamfer: float = 0.0
    #: For a slot (`Board.slot`), its centre line; its `shape` is the slot.
    slot: SlotLine | None = None
    #: The dog bones its shape holds.
    dogbones: tuple[DogBone, ...] = ()
    kind: Literal["pocket"] = "pocket"
    #: The build file's line that made it (`lang.core.where`), set when the board records it.
    where: str = field(default="", compare=False, repr=False)


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
    kind: Literal["hole"] = "hole"
    #: The build file's line that made it (`lang.core.where`), set when the board records it.
    where: str = field(default="", compare=False, repr=False)


@dataclass
class Chamfer:
    #: An edge name (`front.inner`), `outline`, or an operation's name.
    what: str
    size: float
    face: str
    kind: Literal["chamfer"] = "chamfer"
    #: The build file's line that made it (`lang.core.where`), set when the board records it.
    where: str = field(default="", compare=False, repr=False)


@dataclass
class VGroove:
    """A straight 90 degree V-groove in a big face, as a V-bit cuts it: from
    (u0, v0) to (u1, v1), `depth` deep and twice as wide at the face. Its
    ends are cut square; a groove meant to run out of the board starts
    outside it."""
    u0: float
    v0: float
    u1: float
    v1: float
    face: str
    depth: float
    name: str | None = None
    kind: Literal["vgroove"] = "vgroove"
    #: The build file's line that made it (`lang.core.where`), set when the board records it.
    where: str = field(default="", compare=False, repr=False)


@dataclass
class EdgeOp:
    """An operation on a narrow face, positioned in that face's own (s, t)
    frame: s along the face, t across the thickness. It starts `offset`
    in front of the face, its depth measured from there: a box joint's
    finger grooves start at the fingers' tips, which reach past the
    board's box."""
    face: str
    op: Hole | Pocket
    s: float = 0.0
    t: float = 0.0
    offset: float = 0.0
    kind: Literal["edge"] = "edge"
    #: The build file's line that made it (`lang.core.where`), set when the board records it.
    where: str = field(default="", compare=False, repr=False)


Op = Cut | Pocket | Hole | Chamfer | VGroove | EdgeOp
