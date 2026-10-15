"""Every operation kind on one board, as a check of the preview and the
emitter: cuts (with a circle), pockets to a depth and through, holes to a
depth and through, slots (straight, at an angle with a chamfer, and a
stepped one of two slots), chamfers along the outline, an edge, a cut, a
pocket, a slot and a hole, a hole and a pocket into narrow faces, and
corners of the outline rounded (one, and those a cut made, the inside one
too) and cut off.

No two chamfers share an edge: Fusion cannot chamfer an edge twice, and
an edge that one chamfer consumed no longer exists for the next."""
from lang import *

from stock import ply15


with module("ops", Box.from_size(width=400, depth=300, height=100)) as m:
    with board("panel", ply15).on(m.bottom).show(m.top) as panel:
        top = panel.top
        panel.cut(rect(depth=60, width=40), at=top.front.left, name="notch")
        panel.cut(circle(30), at=top.back(50).right(50), name="port", chamfer=1)
        panel.fillet(panel.notch, 6)                                # the corners the notch made
        panel.fillet(panel.front.right, 20)                         # a corner, named by its two narrow faces
        panel.chamfer(panel.back.left, 15)                          # a corner cut off
        panel.pocket(rect(depth=120, width=20), at=top.front(30), depth=5, name="dado", chamfer=1)
        panel.pocket(rect(depth=40, width=40), at=top.back(40).left(40), depth=through, name="window")
        panel.hole(d=10, at=top.center, depth=through, name="bolt", chamfer=1)
        panel.slot(8, top.front(60).left(120), top.front(140).left(120), depth=5, name="vent")
        panel.chamfer(panel.vent, 0.5)                              # a slot's rim, by name
        panel.slot(6, top.back(110).left(110), top.back(60).left(160), depth=through, name="angled", chamfer=0.5)
        panel.slot(12, at=top.front(220).right(120), centers=40, along="depth", depth=4, name="mount_head")
        panel.slot(6, at=top.front(220).right(120), centers=40, along="depth", depth=through, name="mount")
        panel.chamfer(top.outline, 2)                               # the show face's outer contour
        panel.chamfer(panel.back.bottom, 1)                         # an edge of the other big face
        panel.hole(d=8, depth=30, at=panel.front.right(50))         # into the front narrow face
        panel.pocket(rect(depth=40, height=6), at=panel.right.center, depth=10)   # slot in the right narrow face
        for x in spread(panel.front + 40, panel.back - 40, pitch=100):
            panel.hole(d=5, depth=8, at=top.right(25).front(x))     # a column 25 mm from the right edge

    # a standing board, to check that a vertical show face and its edges resolve
    with board("side", ply15).on(m.left).between(m.front, m.back, m.bottom, m.top).show("inner") as side:
        side.fillet(side.back.top, 30)                              # a corner of a standing board
        side.chamfer(side.inner.outline, 1)
        side.chamfer(side.front.outer, 1)
        side.hole(d=5, depth=10, at=side.inner.front(37).bottom(50))
