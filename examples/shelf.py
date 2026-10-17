"""A small shelf unit: two sides and three shelves on through tenons, as a
check of the tenon joint in the preview and in Fusion. The bottom shelf has
corner dog bones and countersunk screws in the gaps between its tenons, the
middle one hidden dog bones; the top's tenons are as wide as the gaps
between them. The top is flush with the sides, so its mortises run out of
their top edge and its tenons lie open: they are screwed from above."""
from lang import *

from stock import ply18, workshop

use(*workshop)   # the machine the nests are made for


box = Box.from_size(width=600, depth=250, height=900)
with module("shelf", box, front=box.front) as unit:
    left = board("left", ply18).on(unit.left)
    right = board("right", ply18).on(unit.right)
    bottom = board("bottom", ply18).on(unit.bottom.into(60)).between(left, right)
    middle = board("middle", ply18).center(unit.center("height")).between(left, right)
    top = board("top", ply18).on(unit.top).between(left, right)

    low = tenons(count=2, width=60)
    bottom.join(left, right, using=low)
    bottom.join(left, right, using=screws(gaps=low, countersink=True))
    middle.join(left, right, using=tenons(count=2, width=60, dogbones="hidden"))
    high = tenons(count=3, even=True)
    top.join(left, right, using=high)
    top.join(left, right, using=screws(tenons=high, countersink=True))
    top.join(left, right, using=screws(gaps=high, countersink=True))
    check(fits_sheet)
