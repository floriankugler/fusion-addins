"""A modeling language for flat furniture, embedded in Python.

See DESIGN.md. Nothing in this package imports Fusion; the Fusion emitter
lives in `lang.emit` (phase 2) and reads the layout JSON this package writes.

The public surface is re-exported here so a build file can do
`from lang import *`.
"""
from .core.directions import Direction, Frame, frame, set_frame
from .core.refs import Pos, Side, spread, to, through
from .core.box import Box
from .core.shapes import Shape, rect
from .core.material import Material, material
from .core.part import Board, board
from .core.scope import Scope, module, scope, registry, check
from .core.checks import no_interference, fits_sheet
from .core.errors import LangError

__all__ = [
    "Direction", "Frame", "frame", "set_frame",
    "Pos", "Side", "spread", "to", "through",
    "Box", "Shape", "rect", "Material", "material",
    "Board", "board", "Scope", "module", "scope", "registry", "check",
    "no_interference", "fits_sheet", "LangError",
]
