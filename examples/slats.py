"""Slats and lips: a shelf unit with lipped plywood and a shelf on oak
cleats, and a slatted bed base.

The unit's top overhangs the sides by 10 mm and is lipped on its front and
both sides; the front strip, lipped first, runs through the corners and the
side strips butt against it. The sides and the bottom are lipped along
their fronts, which stay the finished faces everything measures from. The
shelf rests on two cleats, slats with a wide face on a side and a narrow
face under the shelf, and has 0.5 mm banding along its front.

The bed base is slats only: three rails standing on edge, and slats lying
flat across them, spread along the bed.

Slats stand in for the real ones, made by hand: they take no operations,
joins or hardware for now."""
from lang import *

from stock import oak, pine, ply9, ply18


box = Box.from_size(width=620, depth=320, height=800)
with module("unit", box, front=box.front) as unit:
    top = board("top", ply18).on(unit.top)
    left = board("left", ply18).on(unit.left.into(10)).between(unit.bottom, top, unit.front.into(10), unit.back)
    right = board("right", ply18).on(unit.right.into(10)).between(unit.bottom, top, unit.front.into(10), unit.back)
    bottom = board("bottom", ply18).on(unit.bottom).between(left, right, unit.front.into(10), unit.back)
    back = board("back", ply9).on(unit.back).between(left, right, bottom, top)

    top.lip([top.front, top.left, top.right], 10, oak)          # the front runs through both corners
    for part in (left, right, bottom):
        part.lip(part.front, 10, oak)

    top.join(left, right, using=cabineo(count=2))
    bottom.join(left, right, using=cabineo(count=2))
    back.join(left, right, bottom, top, using=domino("4x20", count=2))

    # the shelf rests on a cleat on either side, 20 back from the sides' fronts
    height = unit.center("height")
    for side in (left, right):
        slat(f"cleat_{side.name}", oak, section=(15, 30)).on(side.inner).edge_on(height, toward=unit.bottom) \
            .between(back, side.front.into(20))
    shelf = board("shelf", ply18).on(height, toward=unit.top).between(left, right, back, left.front.into(20))
    shelf.lip(shelf.front, 0.5, oak)                            # banding
    check(fits_sheet)


bed = Box.from_size(width=1400, depth=2000, height=100, origin=(0, 800, 0))     # beside the unit
with module("bed", bed) as base:
    rails = [
        slat("rail_left", pine, section=(40, 60)).edge_on(base.bottom).on(base.left),
        slat("rail_middle", pine, section=(40, 60)).edge_on(base.bottom).center(base.center("width")),
        slat("rail_right", pine, section=(60, 40)).edge_on(base.bottom).on(base.right),    # sizes in either order
    ]
    for i, x in enumerate(spread(base.front.into(50), base.back.into(50), count=15)):
        slat(f"slat{i + 1}", pine, section=(20, 70)).on(rails[0].top).center(x).between(base.left, base.right)
