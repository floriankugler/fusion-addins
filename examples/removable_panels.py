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

ply18 = material("birch", t=18, sheet=(2500, 1250))
ply12 = material("birch", t=12, sheet=(2500, 1250))
CLEARANCE = 1.5  # around the rear panel


def seat_base(name: str, box: Box, front: Side | None = None) -> Scope:
    """A seat base in its own frame: two sides, a top and a bottom, a
    removable cover over the front and a removable panel set in at the
    back."""
    with module(name, box, front=front) as cab:
        behind = cab.front.into(ply12.t)          # the sides' front edges, against the cover
        left = board("left", ply18).on(cab.left).between(behind)
        right = board("right", ply18).on(cab.right).between(behind)
        top = board("top", ply18).on(cab.top).between(left, right, behind)
        bottom = board("bottom", ply18).on(cab.bottom).between(left, right, behind)
        top.join(left, right, using=cabineo(count=2))
        bottom.join(left, right, using=cabineo(count=2))

        cover = board("cover", ply12).on(cab.front)
        rear = (board("rear", ply12).on(cab.back)
                .between(left.gap(CLEARANCE), right.gap(CLEARANCE), bottom.gap(CLEARANCE), top.gap(CLEARANCE)))
        # two brackets per side, 50 from the ends; pilot holes for the bent
        # frame parts at the sides' front edges, Euro screws on the rear
        # panel's System 32 line
        cab.mount(SlidingBracket(), panel=cover, frame=[left, right])
        cab.mount(SlidingBracket("Pacofix PF-L", frame_hole="euro"), panel=rear, frame=[left, right])
        check(no_interference, fits_sheet)
    return cab


if __name__ == "__build__":   # run as the build file, not imported
    # Across the vehicle, opening toward the rear (+x): 800 wide across
    # the vehicle, 400 deep along it, 450 high.
    box = Box.from_size(width=800, depth=400, height=450)
    seat_base("seatbase", box, front=box.back)
