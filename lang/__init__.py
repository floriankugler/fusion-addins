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
from .core.nests import Nest
from .core.material import SheetMaterial, SlatMaterial, sheet_material, slat_material
from .core.faces import Anchor, Edge, Face, Operation, Outline
from .core.keys import chamfer_size, grain, material, nest
from .core.part import Board, Joint, Slat, board, slat
from .core.refs import Pos, Side, spread, through, to
from .core.scope import ModuleBody, Scope, check, module, scope, uncheck, use, value
from .core.settings import Binding, Setting, setting
from .core.shapes import Shape, circle, polygon, rect
from .hardware import (BallCatch, BracketModel, CatchModel, ConcealedHinge, DoorLatch, DrawerSlide, HatchHinge,
                       HatchHingeModel, HingeModel, LatchModel, SlideModel, SlidingBracket, ball_catch, drawer_slide,
                       hatch_hinge, hinge, latch, sliding_bracket)
from .joints import box_joint, cabineo, clamex, domino, groove, half_lap, screws, tenons
from .master import Master, Plane, master
from . import cam, nesting

__all__ = [
    "Direction", "Frame", "set_frame", "world_frame",
    "Pos", "Side", "spread", "to", "through",
    "Box", "Shape", "rect", "circle", "polygon", "cross", "triangles",
    "SheetMaterial", "SlatMaterial", "sheet_material", "slat_material",
    "Board", "Slat", "Face", "Edge", "Anchor", "Outline", "Operation", "Joint", "board", "slat",
    "Scope", "ModuleBody", "module", "scope", "check", "uncheck",
    "Setting", "Binding", "setting", "use", "value", "material", "grain", "nest", "chamfer_size", "Nest", "nesting",
    "cam",
    "no_interference", "fits_sheet", "inside", "inside_box", "LangError",
    "master", "Master", "Plane", "Contour", "half_lap", "domino", "clamex", "cabineo", "tenons", "screws",
    "box_joint", "groove",
    "drawer_slide", "hinge", "hatch_hinge", "ball_catch", "latch", "sliding_bracket",
    "DrawerSlide", "SlideModel", "ConcealedHinge", "HingeModel", "HatchHinge", "HatchHingeModel",
    "BallCatch", "CatchModel", "DoorLatch", "LatchModel", "SlidingBracket", "BracketModel",
]
