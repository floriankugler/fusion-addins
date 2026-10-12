"""Dog bones, as the dog_bones_native add-in makes them: a router leaves its
radius in every inside corner, so each gets a round relief, here for a
6 mm cutter, 0.1 mm wider.

The panel has every kind of inside corner. It asks for its dog bones first:
they are put into the corners it has when the layout is built, so the
operations after the call get theirs too. A notch at its front left corner,
a V notch in its back edge (an acute corner), a window with one corner
clipped (three square corners and two obtuse ones), a through pocket, a
dado 5 deep, a recess 4 deep with a well 10 deep in it (the well's reliefs
start on the recess's floor) and a pocket from below. Round shapes get
none: a slot, a window with rounded corners, a hole, and the dado's corner
that the hole covers.

The shelf has only its cable notch relieved (`at=`); its window stays as
the router leaves it. In the frame below, the rails are half lapped with
the cross boards, the left rail with corner dog bones (the default), the
right one with hidden ones, which the cross boards cover."""
from lang import *

ply15 = material("birch", t=15, sheet=(2500, 1250))

with module("panels", Box.from_size(width=600, depth=400, height=200)) as m:
    with board("panel", ply15).on(m.bottom).show(m.top) as panel:
        panel.dogbones()
        top = panel.top
        panel.cut(rect(depth=60, width=80), at=top.front.left, name="notch")
        panel.cut(polygon([(60, 0), (0, 20), (60, 40)]), at=top.back.left(150), name="vee")
        panel.cut(rect(depth=80, width=60).clip(back=20, right=20), at=top.center, name="window")
        panel.pocket(rect(depth=60, width=60), at=top.front(40).right(40), depth=through, name="through")
        panel.pocket(rect(depth=120, width=20), at=top.back(60).right(150), depth=5, name="dado")
        panel.hole(d=20, at=top.back(180).right(170), depth=through, name="bolt")     # over a dado corner
        panel.pocket(rect(depth=100, width=100), at=top.front(140).left(40), depth=4, name="recess")
        panel.pocket(rect(depth=40, width=40), at=top.front(170).left(70), depth=10, name="well")
        panel.pocket(rect(depth=60, width=40), at=panel.bottom.back(40).right(40), depth=6, name="below")
        panel.cut(rect(depth=80, width=12).rounded(6), at=top.front(60).right(200), name="slot")
        panel.cut(rect(depth=60, width=60).rounded(10), at=top.back(60).left(250), name="rounded")

    with board("shelf", ply15).on(m.top).show(m.top) as shelf:
        shelf.cut(rect(depth=50, width=100), at=shelf.top.back.right, name="cable")
        shelf.cut(rect(depth=60, width=60), at=shelf.top.center, name="window")
        shelf.dogbones(at=shelf.cable)

with module("frame", Box.from_size(width=400, depth=300, height=40, origin=(0, 700, 0))) as f:
    crosses = [board(f"cross{i}", ply15).center(f.front + x) for i, x in enumerate((60, 150, 240))]
    left_rail = board("left_rail", ply15).center(f.left + 100)
    right_rail = board("right_rail", ply15).center(f.left + 300)
    left_rail.join(crosses, using=half_lap(toward=f.top))
    right_rail.join(crosses, using=half_lap(toward=f.top, dogbones="hidden"))
    check(no_interference)
