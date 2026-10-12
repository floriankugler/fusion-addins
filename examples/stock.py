"""The sheet stock the examples are cut from: birch plywood in the
thicknesses the van uses, on 2500 x 1250 sheets (`fits_sheet` checks
against them). A library: build files import it, it builds nothing, and
the preview does not list it."""
from lang import material

SHEET = (2500.0, 1250.0)

ply9 = material("birch", t=9, sheet=SHEET)
ply12 = material("birch", t=12, sheet=SHEET)
ply15 = material("birch", t=15, sheet=SHEET)
ply18 = material("birch", t=18, sheet=SHEET)
