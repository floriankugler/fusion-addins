"""A modeling language for flat furniture, embedded in Python.

See DESIGN.md. Nothing in this package imports Fusion; the Fusion emitter
lives in `lang.emit` (phase 2) and reads the layout JSON this package writes.

The public surface is re-exported here so a build file can do
`from lang import *`.
"""
from .core.box import Box
from .core.checks import fits_sheet, inside, inside_box, no_interference
from .core.contours import Contour
from .core.cutouts import cross, triangles
from .core.directions import Direction, Frame, set_frame, world_frame
from .core.errors import LangError
from .core.material import Material, material
from .core.faces import Anchor, Edge, Face, Operation, Outline
from .core.part import Board, board
from .core.refs import Pos, Side, spread, through, to
from .core.scope import Scope, cabinet, check, module, scope
from .core.shapes import Shape, circle, polygon, rect
from .hardware import (BallCatch, BracketModel, CatchModel, ConcealedHinge, DoorLatch, DrawerSlide, HatchHinge,
                       HatchHingeModel, HingeModel, LatchModel, SlideModel, SlidingBracket)
from .joints import box_joint, cabineo, clamex, domino, groove, half_lap, screws, tenons
from .master import Master, Plane, master

__all__ = [
    "Direction", "Frame", "set_frame", "world_frame",
    "Pos", "Side", "spread", "to", "through",
    "Box", "Shape", "rect", "circle", "polygon", "Material", "material", "cross", "triangles",
    "Board", "Face", "Edge", "Anchor", "Outline", "Operation", "board",
    "Scope", "module", "cabinet", "scope", "check",
    "no_interference", "fits_sheet", "inside", "inside_box", "LangError",
    "master", "Master", "Plane", "Contour", "half_lap", "domino", "clamex", "cabineo", "tenons", "screws",
    "box_joint", "groove",
    "DrawerSlide", "SlideModel", "ConcealedHinge", "HingeModel", "HatchHinge", "HatchHingeModel",
    "BallCatch", "CatchModel", "DoorLatch", "LatchModel", "SlidingBracket", "BracketModel",
]
