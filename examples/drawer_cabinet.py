"""The drawer cabinet from DESIGN.md: boards and their placement, cuts,
pockets and holes, drawer slides as the first hardware, and connectors in
the carcass. The slide dictates the drawer box and pre-drills the carcass
sides; the bottom and top are joined to the sides with Cabineos, the back
to all four with Dominos. The drawer boxes are box-jointed at their
corners, their floors set into grooves in all four boards. The carcass
and the drawer boxes come from the standard library (`lang.std`). Built on its
own, it stands in a box of its own; van.py imports `drawer_cabinet` and
places it in the master's kitchen box."""
from lang import *
from lang.std import carcass, drawer_box

from stock import ply9, ply12, ply15

GAP = 3  # between fronts


def drawer_cabinet(name: str, box: Box, n: int, slide: DrawerSlide, *, front: Side,
                   bottom_drawer: float | None = None) -> Scope:
    """A drawer cabinet in its own frame: front is where the drawers open,
    wherever the cabinet stands. `front=` places it (see `cabinet`). With
    `bottom_drawer=` the lowest bay gets that height and the others share
    the rest; otherwise all bays are equal."""
    with module(name, box, front=front) as cab:
        # The carcass, from the standard library: sides with a toe kick notch
        # (named, so its edges can be referred to), the bottom on the notch
        # rather than on the floor, a top and a 9 mm back. Cabineos into the
        # sides, from the faces that are not the show faces (here the inner
        # ones); Dominos all round the back, slotted into the inner faces
        # too, so each carcass board is machined from one side. The back
        # carries the Dominos' marks on its show face.
        left, right, bottom, top, _back = carcass(cab, ply15, back=ply9, toekick=(60, 100), joins=cabineo(count=3))

        # shelf-pin holes on the inner faces, lined up on both sides
        for side in (left, right):
            for z in spread(bottom.top.gap(100), top.bottom.gap(100), pitch=32):
                side.hole(d=5, depth=10, at=side.inner.front(37).bottom(z))

        # The opening above the bottom is what the drawers occupy; the area
        # the faces share is the opening less half a gap all round, so that
        # the outer faces keep a full gap to the carcass. Both are divided
        # the same way.
        opening = cab.interior.with_sides(bottom=bottom.top)
        fronts = opening.shrunk(GAP / 2)
        bays = divide(opening, n, bottom_drawer)
        panels = divide(fronts, n, bottom_drawer)
        for i, (bay, panel) in enumerate(zip(bays, panels), 1):
            drawer(f"drawer{i}", bay, panel, slide, sides=(left, right))   # pre-drills the carcass

        cab.export("worktop", top.top)   # for whatever stands on the cabinet
        check(fits_sheet)
    return cab


def divide(space: Box, n: int, first: float | None) -> list[Box]:
    """`n` bays stacked in `space`: equal, or the first one `first` high
    and the others sharing the rest."""
    if first is None:
        return space.split("height", n)
    lowest, rest = space.split("height", [first])
    return [lowest] + rest.split("height", n - 1)


def drawer(name: str, bay: Box, panel: Box, slide: DrawerSlide, *, sides: tuple[Board, Board]) -> Scope:
    """A drawer in its `bay`, the space it occupies in the carcass, with its
    face covering `panel`, its share of the cabinet front, less half a gap
    on every side. The slide sizes the box behind the face and hangs it on
    the carcass `sides`."""
    with scope(name, bay) as d:
        face = board("face", ply15).on(bay.front).between(panel).inset(GAP / 2)
        # The box behind the face, from the standard library. Box joints at
        # the four corners: the sides run the full length and get the
        # notches, the front and back grow the fingers, which show on the
        # sides; the joints go before the slide's cut-outs at the front's
        # and back's lower ends, which they run along. The floor goes 5 mm
        # into all four, with 0.5 mm of room beyond its edges and above it,
        # its corners chamfered (3 mm by default); it lies in the sides'
        # lowest finger, so their grooves stop inside them and those in the
        # front and back run out into the joints' gaps. Then the slide's
        # cut-outs and hook holes, and its runners on the carcass sides.
        drawer_box(d, bay, slide, front=face.back, height=bay.height - 30, material=ply12, floor=ply9,
                   corners=box_joint(7, margin=2, clearance=(0.1, 0.1)), floor_joint=groove(5, clearance=(0.5, 0.5)),
                   carcass=sides)
    return d


if __name__ == "__build__":   # run as the build file, not imported
    # The cabinet stands against the driver's wall (left, -y) and opens toward
    # the aisle. Its 600 mm front runs along the vehicle, so in world terms the
    # box is 500 wide (across the vehicle) and 600 deep (along it); inside the
    # module the cabinet is 600 wide and 500 deep.
    box = Box.from_size(width=500, depth=600, height=720)
    slide = drawer_slide("Dynapro 40", nl=450)
    drawer_cabinet("drawercab", box, 3, slide, front=box.right, bottom_drawer=230)
