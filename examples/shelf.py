"""A small shelf unit: two sides and three shelves on through tenons, as a
check of the tenon joint in the preview and in Fusion. The bottom shelf has
corner dog bones, the middle one hidden ones, the top's tenons are as wide
as the gaps between them; the top is flush with the sides, so its mortises
run out of their top edge."""
from lang import *

ply18 = material("birch", t=18, sheet=(2500, 1250))

with module("shelf", Box.from_size(width=600, depth=250, height=900)) as unit:
    left = board("left", ply18).on(unit.left)
    right = board("right", ply18).on(unit.right)
    bottom = board("bottom", ply18).on(unit.bottom + 60).between(left, right)
    middle = board("middle", ply18).center(unit.center("height")).between(left, right)
    top = board("top", ply18).on(unit.top).between(left, right)

    bottom.join(left, right, using=tenons(count=2, width=60))
    middle.join(left, right, using=tenons(count=2, width=60, dogbones="hidden"))
    top.join(left, right, using=tenons(count=3, even=True))
    check(no_interference, fits_sheet)
