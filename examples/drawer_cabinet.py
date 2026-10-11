"""The drawer cabinet from DESIGN.md: boards and their placement, cuts,
pockets and holes, and drawer slides as the first hardware. The slide
dictates the drawer box and pre-drills the carcass sides; joints are not
modelled yet. Built on its own, it stands in a box of its own; van.py
imports `drawer_cabinet` and places it in the master's kitchen box."""
from lang import *
from lang.hardware.slides import DrawerSlide
from lib.drawer_slides import DYNAPRO_40

ply15 = material("birch", t=15, sheet=(2500, 1250))
ply12 = material("birch", t=12, sheet=(2500, 1250))
ply9 = material("birch", t=9, sheet=(2500, 1250))
GAP = 3  # between fronts


def drawer_cabinet(name: str, box: Box, n: int, slide: DrawerSlide, front: Side | None = None,
                   bottom_drawer: float | None = None) -> Scope:
    """A drawer cabinet in its own frame: front is where the drawers open,
    wherever the cabinet stands. `front=` places it (see `module`). With
    `bottom_drawer=` the lowest bay gets that height and the others share
    the rest; otherwise all bays are equal."""
    with module(name, box, front=front) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        # toe kick notch in both sides, named so its edges can be referred to
        for side in (left, right):
            side.cut(rect(depth=60, height=100), at=side.outer.bottom.front, name="toekick")
        # the bottom sits on the toe kick, not on the floor
        bottom = board("bottom", ply15).on(left.toekick.top, toward=cab.top).between(left, right)
        top = board("top", ply15).on(cab.top).between(left, right)
        board("back", ply9).on(cab.back).between(left, right, bottom, top)

        # shelf-pin holes on the inner faces, lined up on both sides
        for side in (left, right):
            for z in spread(bottom.top + 100, top.bottom - 100, pitch=32):
                side.hole(d=5, depth=10, at=side.inner.front(37).bottom(z))

        # The opening above the bottom is what the drawers occupy; the area
        # the faces share is the opening less half a gap all round, so that
        # the outer faces keep a full gap to the carcass. Both are divided
        # the same way.
        opening = cab.interior.with_sides(bottom=bottom.top)
        fronts = opening.shrunk(left=GAP / 2, right=GAP / 2, top=GAP / 2, bottom=GAP / 2)
        bays = divide(opening, n, bottom_drawer)
        panels = divide(fronts, n, bottom_drawer)
        for i, (bay, panel) in enumerate(zip(bays, panels), 1):
            d = drawer(f"drawer{i}", bay, panel, slide)
            d.mount(slide, sides=(left, right), front=d.face.back)   # pre-drills the carcass

        cab.export("worktop", top.top)   # for whatever stands on the cabinet
        check(no_interference, fits_sheet)
    return cab


def divide(space: Box, n: int, first: float | None) -> list[Box]:
    """`n` bays stacked in `space`: equal, or the first one `first` high
    and the others sharing the rest."""
    if first is None:
        return space.split("height", n)
    lowest, rest = space.split("height", [first])
    return [lowest] + rest.split("height", n - 1)


def drawer(name: str, bay: Box, panel: Box, slide: DrawerSlide) -> Scope:
    """A drawer in its `bay`, the space it occupies in the carcass, with its
    face covering `panel`, its share of the cabinet front, less half a gap
    on every side. The slide sizes the box behind the face."""
    with scope(name, bay) as d:
        face = (board("face", ply15).on(bay.front)
                .between(panel.left, panel.right, panel.bottom, panel.top).inset(GAP / 2))
        box = slide.drawer_box(bay, front=face.back, side_thickness=ply12.t, height=bay.height - 30)

        l = board("left", ply12).on(box.left).between(box.front, box.back, box.bottom, box.top)
        r = board("right", ply12).on(box.right).between(box.front, box.back, box.bottom, box.top)
        f = board("front", ply12).on(box.front).between(l, r, box.bottom, box.top)
        k = board("back", ply12).on(box.back).between(l, r, box.bottom, box.top)
        # the floor reaches 5 mm into the sides
        floor = (board("floor", ply9)
                 .on(box.bottom + slide.recess)
                 .between(l.into(5), r.into(5), f, k))
        # the grooves: what the floor occupies in each side, with 0.5 mm of
        # room above the floor and beyond its edges
        room = floor.box().grown(top=0.5, left=0.5, right=0.5)
        for side in (l, r):
            side.cut(room, name="floor_groove")
        slide.machine_box(sides=(l, r), front=f, back=k, floor=floor)   # cut-outs and hook holes
    return d


if __name__ == "__build__":   # run as the build file, not imported
    # The cabinet stands against the driver's wall (left, -y) and opens toward
    # the aisle. Its 600 mm front runs along the vehicle, so in world terms the
    # box is 500 wide (across the vehicle) and 600 deep (along it); inside the
    # module the cabinet is 600 wide and 500 deep.
    box = Box.from_size(width=500, depth=600, height=720)
    slide = DrawerSlide(DYNAPRO_40, nl=450)
    cabinet = drawer_cabinet("drawercab", box, 3, slide, front=box.right, bottom_drawer=230)
