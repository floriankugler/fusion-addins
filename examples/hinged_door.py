"""A wall cabinet with a hinged door: concealed hinges as hardware.

The carcass stands behind an overlay door, which covers it all round but
for half a gap. The bottom and top are joined to the sides with Cabineos,
the back to all four with Dominos, as in the drawer cabinet; a shelf
halfway up rests on four pins. The door hangs on two Blum CLIP top 110
hinges for thin doors on the cabinet's left side: `cab.mount(hinge,
door=door, carcass=left)` drills the door's inner face and the side's
inner face as the Concealed Hinge add-in does and places the hinges as
boxes. `carcass=right` hangs it on the other side. Built on its own, it
hangs on the driver's wall and opens toward the aisle."""
from lang import *
from lang.std import carcass

from stock import ply9, ply12, ply15

GAP = 3  # around the door


def hinged_cabinet(name: str, box: Box, hinge: ConcealedHinge, *, front: Side) -> Scope:
    """A cabinet in its own frame with one overlay door hinged on its left
    side, the hinges `hinge`. `front=` places it (see `cabinet`)."""
    with cabinet(name, box, front=front) as cab:
        # the carcass stands behind the door
        left, right, bottom, top, back = carcass(cab, ply15, back=ply9, front=cab.front.into(ply12.thickness))

        # a shelf halfway up, 1 mm clear of the sides and 20 mm back from
        # the door, on a pin 37 mm in from each end of both sides
        shelf = (board("shelf", ply15)
                 .center((bottom.top + top.bottom) / 2)
                 .between(left.gap(1), right.gap(1), back, cab.front.into(ply12.thickness + 20)))
        for side in (left, right):
            for edge in (side.inner.front, side.inner.back):
                side.hole(d=5, depth=10, at=edge(37).bottom(shelf.bottom.gap(6)))

        door = board("door", ply12).on(cab.front).inset(GAP / 2)
        cab.mount(hinge, door=door, carcass=left)
        check(fits_sheet)
    return cab


if __name__ == "__build__":   # run as the build file, not imported
    # On the driver's wall (left, -y), opening toward the aisle: its 450 mm
    # front runs along the vehicle, so in world terms the box is 350 wide
    # (across the vehicle) and 450 deep (along it).
    box = Box.from_size(width=350, depth=450, height=600)
    hinged_cabinet("hingecab", box, hinge("Blum CLIP top 110 Thin +0"), front=box.right)
