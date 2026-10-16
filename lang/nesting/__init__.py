"""Nesting: a build's nests on the stock on hand and the sheets bought, for
the machine's bed (`design/nesting.md`).

    python -m lang.nesting examples/van.py                  # every nest
    python -m lang.nesting examples/van.py kitchen.birch_15

A build declares its nests (`cab.nest("carcass", material=ply15)`, else one
per material per module) and uses this package's keys for the machine and
the nest (`use(nesting.bed((2000, 1000)))`, `keys`), which are all a build
file imports from here, without the solvers. After the layout step, like
the preview: `resolve` reads a nest's parts and values from the layout,
`inventory` the stock on hand, `items` the parts as the nest sees them,
`packing` nests them with PackingSolver, `sawing` saws the blanks out of
the stock, `refill` empties a sheet into the others, `nest` runs the steps
per material, `verify` checks the result apart from the solvers, `draw`
draws it. The nest file's shape is in `nest_types`; the Fusion emitter
draws a nest through `lang.emit.nested`.
"""
from .keys import bed, kerf, keep_across, keep_area, least_seconds, margin, max_cuts, rate, refill, seconds, spacing

__all__ = ["bed", "kerf", "max_cuts", "spacing", "margin", "keep_across", "keep_area", "seconds", "rate",
           "least_seconds", "refill"]
