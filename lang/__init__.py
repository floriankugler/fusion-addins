"""A modeling language for flat furniture, embedded in Python.

See DESIGN.md. Nothing in this package imports Fusion; the Fusion emitter
lives in `lang.emit` (phase 2) and reads the layout JSON this package writes.

The public surface is re-exported here so a build file can do
`from lang import *`.
"""
from .core.box import Box
from .core.checks import fits_sheet, no_interference
from .core.directions import Direction, Frame, frame, set_frame
from .core.errors import LangError
from .core.material import Material, material
from .core.part import Anchor, Board, Edge, Face, Outline, board
from .core.refs import Pos, Side, spread, through, to
from .core.scope import Scope, check, module, registry, scope
from .core.shapes import Shape, circle, polygon, rect

__all__ = [
    "Direction", "Frame", "frame", "set_frame",
    "Pos", "Side", "spread", "to", "through",
    "Box", "Shape", "rect", "circle", "polygon", "Material", "material",
    "Board", "Face", "Edge", "Anchor", "Outline", "board",
    "Scope", "module", "scope", "registry", "check",
    "no_interference", "fits_sheet", "LangError",
]
