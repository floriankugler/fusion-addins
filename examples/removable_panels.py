"""A seat base with two removable panels on sliding brackets (Häfele
Pacofix PF / PF-L, the same part as Keku AS).

The sides are the frame boards. The front cover lies over their front
edges with a 3 mm gap (room for a felt strip): the brackets read the gap
from the model and drill the sides 37 behind the cover's back face, 34
behind their edges. The rear panel is set in between the sides, top and
bottom, flush with their back edges and 1.5 mm clear of them; its
brackets drill the sides 37 in front of it. Each panel hangs on two
brackets per side, Keku's minimum of four, and comes off square to
itself. The cover's frame parts are screwed to the sides with Euro
screws, the rest with chipboard screws into pilot holes. Top and bottom
are joined to the sides with Cabineos. Built on its own, the base stands
across the vehicle behind the cab and opens toward the rear."""
from lang import *
from lang.hardware.sliding_brackets import SlidingBracket

ply18 = material("birch", t=18, sheet=(2500, 1250))
ply12 = material("birch", t=12, sheet=(2500, 1250))
GAP = 3          # between the cover and the sides' front edges
CLEARANCE = 1.5  # around the rear panel


def seat_base(name: str, box: Box, front: Side | None = None) -> Scope:
    """A seat base in its own frame: two sides, a top and a bottom, a
    removable cover over the front and a removable panel set in at the
    back."""
    with module(name, box, front=front) as cab:
        behind = cab.front.into(ply12.t + GAP)     # the sides' front edges
        left = board("left", ply18).on(cab.left).between(behind)
        right = board("right", ply18).on(cab.right).between(behind)
        top = board("top", ply18).on(cab.top).between(left, right, behind)
        bottom = board("bottom", ply18).on(cab.bottom).between(left, right, behind)
        top.join(left, right, using=cabineo(count=2))
        bottom.join(left, right, using=cabineo(count=2))

        cover = board("cover", ply12).on(cab.front)
        rear = (board("rear", ply12).on(cab.back)
                .between(left.gap(CLEARANCE), right.gap(CLEARANCE), bottom.gap(CLEARANCE), top.gap(CLEARANCE)))
        # Euro screws into the sides on the cover's System 32 line, two
        # brackets per side 50 from the ends; the rear panel on pilot holes
        cab.mount(SlidingBracket(frame_hole="euro"), panel=cover, frame=[left, right])
        cab.mount(SlidingBracket(), panel=rear, frame=[left, right])
        check(no_interference, fits_sheet)
    return cab


if __name__ == "__build__":   # run as the build file, not imported
    # Across the vehicle, opening toward the rear (+x): 800 wide across
    # the vehicle, 400 deep along it, 450 high.
    box = Box.from_size(width=800, depth=400, height=450)
    seat_base("seatbase", box, front=box.back)
