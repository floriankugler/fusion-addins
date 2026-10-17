"""A seat base with two removable panels on sliding brackets (Häfele
Pacofix, the same parts as Keku AS).

The sides are the frame boards. The front cover lies over their front
edges on the bent frame part PF-L-R, the default: its plate begins at
the cover's back face, so the sides' holes lie 8 behind it and the
cover's 19 in from the sides' faces. The rear panel is set in between
the sides, top and bottom, flush with their back edges and 1.5 mm clear
of them, on the straight frame part PF-L: its holes lie on the sides'
System 32 line, 37 in front of the panel, and take Euro screws. Each
panel hangs on two brackets per side, Keku's minimum of four, and comes
off square to itself. Top and bottom are joined to the sides with
Cabineos. Built on its own, the base stands across the vehicle behind
the cab and opens toward the rear."""
from lang import *
from lang.std import carcass

from stock import ply12, ply18, workshop

CLEARANCE = 1.5  # around the rear panel


def seat_base(name: str, box: Box, *, front: Side) -> Scope:
    """A seat base in its own frame: two sides, a top and a bottom, a
    removable cover over the front and a removable panel set in at the
    back."""
    with module(name, box, front=front) as cab:
        # the sides' front edges stand back by the cover; no back, the rear
        # panel is set in instead
        left, right, bottom, top = carcass(cab, ply18, front=cab.front.into(ply12.thickness))

        cover = board("cover", ply12).on(cab.front)
        rear = (board("rear", ply12).on(cab.back)
                .between(left, right, bottom, top).inset(CLEARANCE))
        # two brackets per side, 50 from the ends; pilot holes for the bent
        # frame parts at the sides' front edges, Euro screws on the rear
        # panel's System 32 line
        cab.mount(sliding_bracket(), panel=cover, frame=[left, right])
        cab.mount(sliding_bracket("Pacofix PF-L", frame_hole="euro"), panel=rear, frame=[left, right])
        check(fits_sheet)
    return cab


if __name__ == "__build__":   # run as the build file, not imported
    use(*workshop)   # the machine the nests are made for
    # Across the vehicle, opening toward the rear (+x): 800 wide across
    # the vehicle, 400 deep along it, 450 high.
    box = Box.from_size(width=800, depth=400, height=450)
    seat_base("seatbase", box, front=box.back)
