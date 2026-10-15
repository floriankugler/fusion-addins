"""A van cabinet held shut by latches: an inset door above a fixed shelf
and two inset drawers below it, a rail between them, every front held by
Pull Lock 44 push locks, as the van's cabinets have them. The door gets
two in its upper edge, which catch on the carcass top; each drawer face
one, which catches on the shelf or the rail above it. A latch drills its
door and the board it catches on (the lock's hole and counterbore in the
front, the strike's pilot holes under the board) and places itself as
boxes. Behind a drawer face it takes room, so the drawer box stays
`latch.reach` below the board above. The door's hinges are not modelled
here. Built on its own, the cabinet stands against the driver's wall and
opens toward the aisle, like the drawer cabinet."""
from lang import *

from stock import ply9, ply12, ply15

REVEAL = 2.0  # around each inset front


def latched_cabinet(name: str, box: Box, slide: DrawerSlide, model: LatchModel = "Pull Lock 44", *,
                    front: Side, drawer_height: float = 180) -> Scope:
    """A cabinet in its own frame: from the bottom up a drawer bay
    `drawer_height` high, a rail, a second bay, a shelf and the door's
    compartment above it. A `model` latch holds every front."""
    with cabinet(name, box, front=front) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        bottom = board("bottom", ply15).on(cab.bottom).between(left, right)
        top = board("top", ply15).on(cab.top).between(left, right)
        back = board("back", ply9).on(cab.back).between(left, right, bottom, top)
        bottom.join(left, right, using=cabineo(count=3))
        top.join(left, right, using=cabineo(count=3))
        back.join(left, right, bottom, top, using=domino("4x20", count=2))

        # the rest, above the shelf, is the door's compartment
        lower_bay, rail_space, upper_bay, shelf_space, _ = cab.interior.split(
            "height", [drawer_height, ply15.thickness, drawer_height, ply15.thickness])
        # the rail at the front, deep enough for the strike behind the face
        rail = board("rail", ply15).on(rail_space.bottom).between(left, right, cab.front, cab.front.into(80))
        shelf = board("shelf", ply15).on(shelf_space.bottom).between(left, right, back)
        rail.join(left, right, using=domino("4x20", count=1))
        shelf.join(left, right, using=cabineo(count=2))

        door = board("door", ply15).on(cab.front).between(left, right, shelf.top, top).inset(REVEAL)
        cab.mount(latch(model, count=2), door=door, carcass=top)

        drawer_latch = latch(model)
        for i, (bay, catch) in enumerate(((lower_bay, rail), (upper_bay, shelf)), 1):
            d = drawer(f"drawer{i}", bay, slide, drawer_latch, catch)
            d.mount(slide, sides=(left, right), front=d.face.back)     # pre-drills the carcass
            d.mount(drawer_latch, door=d.face, carcass=catch)          # the lock in the face, the strike under `catch`

        check(fits_sheet)
    return cab


def drawer(name: str, bay: Box, slide: DrawerSlide, latch: DoorLatch, catch: Board) -> Scope:
    """A drawer in its `bay` with an inset face. The slide sizes the box
    behind the face; its top stays clear of the latch that holds the face
    to `catch`, the board above the bay."""
    with scope(name, bay) as d:
        face = board("face", ply15).on(bay.front).inset(REVEAL)
        box_top = catch.bottom.gap(latch.reach)
        box = slide.drawer_box(bay, front=face.back, side_thickness=ply12.thickness,
                               height=(box_top - bay.bottom) - slide.side_lift)
        l = board("left", ply12).on(box.left).between(box)
        r = board("right", ply12).on(box.right).between(box)
        f = board("front", ply12).on(box.front).between(l, r, box.bottom, box.top)
        k = board("back", ply12).on(box.back).between(l, r, box.bottom, box.top)
        floor = board("floor", ply9).on(box.bottom.into(slide.recess)).between(l, r, f, k)
        floor.join(l, r, f, k, using=groove(5, clearance=(0.5, 0.5)))
        slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)
    return d


if __name__ == "__build__":   # run as the build file, not imported
    # Against the driver's wall (left, -y), opening toward the aisle: in
    # world terms 500 across the vehicle and 600 along it; inside the
    # module the cabinet is 600 wide and 500 deep.
    box = Box.from_size(width=500, depth=600, height=720)
    latched_cabinet("locker", box, drawer_slide("Dynapro 40", nl=450), front=box.right)
