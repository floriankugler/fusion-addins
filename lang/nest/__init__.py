"""Nesting: a layout's parts on the stock on hand, for the machine's bed
(`design/nesting.md`).

    python -m lang.nest examples/van.py --workshop examples/workshop.toml

Plain Python after the layout step, like the preview: `items` reads the
parts from the layout, `packing` nests them with PackingSolver, `sawing`
saws the blanks out of the stock, `refill` empties a sheet into the others,
`nest` runs the steps per material, `verify` checks the result apart from
the solvers, `draw` draws it, `workshop` reads the stock and the machine.
The nest file's shape is in `nest_types`; the Fusion emitter draws a nest
through `lang.emit.nested`.
"""
from ..core.layout import layout_hash
from .nest import Options, nest_layout
from .workshop import Offcut, Sheet, Workshop, read_workshop

__all__ = ["Options", "layout_hash", "nest_layout", "Offcut", "Sheet", "Workshop", "read_workshop"]
