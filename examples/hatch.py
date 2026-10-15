"""A wall cabinet with a lift-up hatch on Häfele Free space 1.11 hinges.

The hatch overlays the carcass front and is part of the cabinet's box, the
carcass stands behind it. The hinges hang from the underside of the
carcass top: mounted, they drill the side panels and the closed hatch,
check that the hatch top reaches no higher above the top's underside than
they allow for its thickness (here 18 of at most 24 mm), and they say how
far down they reach inside, so the shelf below them stays clear. Bottom,
top and shelf are joined to the sides with Cabineos, the back to all four
with Dominos."""
from lang import *

from stock import ply9, ply18

GAP = 1.5   # between the hatch and its neighbours, at each side


def wall_cabinet(name: str, box: Box, hinge: HatchHinge, *, front: Side) -> Scope:
    """A wall cabinet in its own frame, opening toward `front`, with a
    lift-up hatch over its whole front and a fixed shelf below the hinges."""
    with cabinet(name, box, front=front) as cab:
        hatch = (board("hatch", ply18).on(cab.front)
                 .between(cab.left.into(GAP), cab.right.into(GAP), cab.bottom, cab.top))
        # The carcass behind the closed hatch; its front is the hatch's inner face.
        left = board("left", ply18).on(cab.left).between(hatch, cab.back)
        right = board("right", ply18).on(cab.right).between(hatch, cab.back)
        top = board("top", ply18).on(cab.top).between(left, right, hatch, cab.back)
        bottom = board("bottom", ply18).on(cab.bottom).between(left, right, hatch, cab.back)
        back = board("back", ply9).on(cab.back).between(left, right, bottom, top)
        # The shelf's upper face where the closed hinges end, set back 20 mm.
        shelf = (board("shelf", ply18).on(hinge.lowest(top), toward=cab.bottom)
                 .between(left, right, left.front.into(20), back))

        bottom.join(left, right, using=cabineo(count=2))
        top.join(left, right, using=cabineo(count=2))
        shelf.join(left, right, using=cabineo(count=2))
        back.join(left, right, bottom, top, using=domino("4x20", count=2))

        # Drills the side panels' inner faces and the hatch's inner face,
        # which faces the carcass, and places the two hinges.
        cab.mount(hinge, hatch=hatch, sides=(left, right), top=top)
        check(no_interference, fits_sheet)
    return cab


if __name__ == "__build__":   # run as the build file, not imported
    # Hung on the driver's wall (left, -y) above the worktop, opening toward
    # the aisle: 800 along the vehicle, 330 deep across it, 400 high. Inside
    # the module the cabinet is 800 wide and 330 deep.
    box = Box.from_size(width=330, depth=800, height=400, origin=(0, 0, 1400))
    wall_cabinet("wallcab", box, hatch_hinge("Free space 1.11"), front=box.right)
