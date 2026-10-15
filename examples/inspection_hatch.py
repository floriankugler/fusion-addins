"""An inspection hatch in a floor panel, held in its opening by Ganter GN
450 ball catches, drilled as the ball_catch add-in drills them.

The opening is a through cut with rounded corners. `catch.hatch()` makes
the hatch from it: the opening shrunk by the 3 mm slot the catches need,
flush with the panel. Mounted, the catches drill a pilot hole for each
holder into the panel's underside beside the opening's left and right
edges, and one for each ball into the hatch's underside, and they hang
under the floor as boxes, between the battens. Both rims are chamfered on
top, and the hatch has a finger hole to lift it by."""
from lang import *

from stock import ply15


catch = ball_catch()    # GN 450: 4 catches 40 mm from the ends of the straight edges, pilot holes 2 x 4

# A piece of the van floor in the van's own terms: 1200 along the vehicle,
# 800 across, the panel on four battens running across.
with module("floor", Box.from_size(width=800, depth=1200, height=60)) as f:
    panel = board("panel", ply15).on(f.top).show(f.top)
    for i, x in enumerate(spread(f.front.into(ply15.t / 2), f.back.into(ply15.t / 2), count=4)):
        board(f"batten{i}", ply15).center(x).between(f.bottom, panel)

    # the opening between the middle battens, its corners rounded
    panel.cut(rect(width=400, depth=300).rounded(20), at=panel.top.center, name="opening")
    hatch = catch.hatch("hatch", panel.opening)
    hatch.hole(d=25, depth=through, at=hatch.top.front(30), name="finger", chamfer=1)
    panel.chamfer(panel.opening, 1)
    hatch.chamfer(hatch.top.outline, 1)

    # the catches on the opening's left and right edges, two each, screwed
    # to the underside (the faces that are not shown)
    f.mount(catch, opening=panel.opening, edge=panel.opening.left, hatch=hatch)
    check(no_interference, fits_sheet)
