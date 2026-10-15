"""A van built against its master document: the floor battens
(design/placement.md, "Contours as limits") and the drawer cabinet
standing in the master's kitchen box.

The master is the sample that tools/van_master.py builds in Fusion; its
snapshot is van_snapshot.json next to this file. Nothing below names a
coordinate of the vehicle: the planes, the floor outline with its wheel
arches, the cross-section of the ribbed floor, the batten pitch and the
kitchen's place all come from the master.
"""
from lang import *

from stock import ply12, ply15
from drawer_cabinet import drawer_cabinet

# The master's axes are the world axes; this is the van's choice of front,
# left (the driver's side) and top. It is the language's default frame, so
# the call only states it; a van whose master runs the other way would set
# its own here, before reading the master (every build starts from the
# default, and world_frame() reads the one in use).
set_frame(Frame(front="-x", left="-y", top="+z"))

# The master index: names as they are in Fusion.
van = master("van_snapshot.json")
floor_level = van.plane("Bodenniveau")        # top of the finished floor
floor_front = van.plane("Boden vorne")        # where the battens start and end
floor_back = van.plane("Boden hinten")
floor_outline = van.contour("Bodenumriss")    # usable floor in plan view, with the wheel arches
floor_profile = van.contour("Bodenprofil")    # cross-section of the vehicle floor


def floor(name: str, box: Box) -> Scope:
    """A grid of battens under two floor panels. The battens' tops are the
    panels' underside and they keep 2 mm off the vehicle floor: the ones
    across follow its profile, the ones along stand on it. All of them stop
    3 mm short of the floor outline, so the ones across between the wheel
    arches are shorter and the outer ones along are cut in two by the
    arches. Where they cross they are half lapped. The panels take the
    outline as it is and meet over the middle batten across."""
    with module(name, box) as f:
        top = floor_level - ply12.thickness
        above_floor = floor_profile.gap(2)
        inside = floor_outline.gap(3)
        pitch = van.param("Lattenabstand")
        battens = [
            board(f"batten{i}", ply15).center(x).between(top, above_floor, inside)
            for i, x in enumerate(spread(floor_front, floor_back, pitch=pitch))
        ]
        # Six along, evenly spaced, the outer two with their outer faces where
        # the battens across end. The wheel arches cut the outer two in two,
        # so each is two boards: one from each end, as far as the outline
        # lets it.
        # Each is notched from the top where it crosses a batten, which is
        # notched from below.
        edge = 3 + ply15.thickness / 2
        lap = half_lap(toward=f.top)
        for i, y in enumerate(spread(f.left.into(edge), f.right.into(edge), count=6)):
            if i in (0, 5):
                pieces = [board(f"long{i}_front", ply15).center(y).between(top, above_floor, inside, floor_front),
                          board(f"long{i}_back", ply15).center(y).between(top, above_floor, inside, floor_back)]
                for piece in pieces:
                    # the battens on its side of the wheel arch
                    piece.join([b for b in battens if b.box().overlaps(piece.box())], using=lap)
            else:
                # Longer than the machine's bed: sawn and notched by hand.
                long = board(f"long{i}", ply15).center(y).between(top, above_floor, inside, floor_front, floor_back)
                long.nest(False).join(battens, using=lap)
        middle = battens[len(battens) // 2]
        joint = (middle.front + middle.back) / 2
        # Larger than the bed (and a sheet): cut by hand from a bigger panel.
        board("panel_front", ply12).on(f.top).between(floor_outline, f.front, joint).nest(False)
        board("panel_back", ply12).on(f.top).between(floor_outline, joint, f.back).nest(False)
        check(no_interference)
    return f


floor("floor", van.box("Boden"))

# The cabinet stands in the master's kitchen box, against the driver's wall,
# and opens toward the aisle.
kitchen_box = van.box("Moebel.Kueche")
slide = drawer_slide("Dynapro 40", nl=450)
kitchen = drawer_cabinet("kitchen", kitchen_box, 3, slide, front=kitchen_box.right, bottom_drawer=230)
kitchen.check(inside_box, inside(floor_outline))
