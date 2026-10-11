"""A van built against its master document: the floor battens from DESIGN.md
("Master index and floor battens") and the drawer cabinet standing in the
master's kitchen box.

The master is the sample that tools/van_master.py builds in Fusion; its
snapshot is van_snapshot.json next to this file. Nothing below names a
coordinate of the vehicle: the planes, the floor outline with its wheel
arches, the cross-section of the ribbed floor, the batten pitch and the
kitchen's place all come from the master.
"""
from lang import *
from lang.hardware.slides import DrawerSlide
from lib.drawer_slides import DYNAPRO_40

from drawer_cabinet import drawer_cabinet, ply12, ply15

# The master's axes are the world axes; this is the van's choice of front,
# left (the driver's side) and top. Set it before reading the master.
set_frame(Frame(front="-x", left="-y", top="+z"))

# The master index: names as they are in Fusion.
van = master("van_snapshot.json")
floor_level = van.plane("Bodenniveau")        # top of the finished floor
floor_front = van.plane("Boden vorne")        # where the battens start and end
floor_back = van.plane("Boden hinten")
floor_outline = van.contour("Bodenumriss")    # usable floor in plan view, with the wheel arches
floor_profile = van.contour("Bodenprofil")    # cross-section of the vehicle floor


def floor(name: str, box: Box) -> Scope:
    """Battens across the vehicle under two floor panels. A batten's top is
    the panels' underside, its lower edge follows the floor profile 2 mm
    above it, and its ends stop at the floor outline, so the battens
    between the wheel arches are shorter. The panels take the outline as
    it is and meet over the middle batten."""
    with module(name, box) as f:
        top = floor_level - ply12.t
        pitch = van.param("Lattenabstand")
        battens = [
            board(f"batten{i}", ply15).center(x).between(top, floor_profile.gap(2), floor_outline)
            for i, x in enumerate(spread(floor_front, floor_back, pitch=pitch))
        ]
        middle = battens[len(battens) // 2]
        joint = (middle.front + middle.back) / 2
        board("panel_front", ply12).on(f.top).between(floor_outline, f.front, joint)
        board("panel_back", ply12).on(f.top).between(floor_outline, joint, f.back)
        check(no_interference)
    return f


floor("floor", van.box("Boden"))

# The cabinet stands in the master's kitchen box, against the driver's wall,
# and opens toward the aisle.
kitchen_box = van.box("Kueche")
slide = DrawerSlide(DYNAPRO_40, nl=450)
kitchen = drawer_cabinet("kitchen", kitchen_box, 3, slide, front=kitchen_box.right, bottom_drawer=230)
kitchen.check(inside_box, inside(floor_outline))
