"""Face cutouts, as the Face Cutout add-in makes them, on a small cabinet
joined with Cabineos and Dominos: a full cutout in the left side, aligned
triangles in the right side, a cross in the back, and a cross pocketed
into the bottom that leaves 5 mm. The cutouts come after the joins, so
they keep material around the connectors' holes and slots; the sides also
keep a strip where the shelf meets them. Every cutout is cut from the
inner face, which carries the chamfer."""
from lang import *
from lang.std import carcass

from stock import ply15


box = Box.from_size(width=600, depth=400, height=700)
with module("cutouts", box, front=box.front) as unit:
    left, right, bottom, top, back = carcass(unit, ply15, back=ply15)
    shelf = board("shelf", ply15).center(unit.center("height")).between(left, right, back)

    shelf.join(left, right, using=cabineo(count=2))

    left.cutout(keep=[shelf], chamfer=1)
    right.cutout(pattern=triangles(4, 3, spacing=25, aligned=True), keep=[shelf], chamfer=1)
    back.cutout(pattern=cross(60), chamfer=1)
    bottom.cutout(pattern=cross(40), depth=to(bottom.outer, leave=5), chamfer=1)
