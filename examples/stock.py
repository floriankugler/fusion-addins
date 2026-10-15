"""The stock the examples are made of: birch plywood in the thicknesses the
van uses, on 2500 x 1250 sheets (`fits_sheet` checks against them), and
solid wood for slats and lips, by species only (a slat has its own
section, a lip its own thickness). A library: build files import it, it
builds nothing, and the preview does not list it."""
from lang import sheet_material, slat_material

SHEET = (2500.0, 1250.0)

ply9 = sheet_material("birch", t=9, size=SHEET)
ply12 = sheet_material("birch", t=12, size=SHEET)
ply15 = sheet_material("birch", t=15, size=SHEET)
ply18 = sheet_material("birch", t=18, size=SHEET)

oak = slat_material("oak")
pine = slat_material("pine")
