"""Every operation kind on one board, as a check of the preview and the
emitter: cuts (with a circle), pockets to a depth and through, holes to a
depth and through, chamfers along the outline, an edge, a cut, a pocket
and a hole, and a hole and a pocket into narrow faces.

No two chamfers share an edge: Fusion cannot chamfer an edge twice, and
an edge that one chamfer consumed no longer exists for the next."""
from lang import *

ply15 = material("birch", t=15, sheet=(2500, 1250))

with module("ops", Box.from_size(width=400, depth=300, height=100)) as m:
    panel = (board("panel", ply15).on(m.bottom).show("top")
             .cut(rect(60, 40), at="front.left", name="notch")
             .cut(circle(30), at=("back.right", 50, 50), name="port", chamfer=1)
             .pocket(rect(120, 20), at=("front", 30), depth=5, name="dado", chamfer=1)
             .pocket(rect(40, 40), at=("back.left", 40, 40), depth=through, name="window")
             .hole(d=10, at="center", depth=through, name="bolt", chamfer=1)
             .chamfer("outline", 2)                     # the show face's outer contour
             .chamfer("back.bottom", 1)                 # an edge of the other big face
             .hole(d=8, depth=30, face="front", at=("right", 50))      # into the front narrow face
             .pocket(rect(40, 6), face="right", at="center", depth=10))  # slot in the right narrow face
    for x in spread(panel.front + 40, panel.back - 40, pitch=100):
        panel.hole(d=5, depth=8, at=("right", 25, x))   # a column 25 mm from the right edge

    # a standing board, to check that a vertical show face and its edges resolve
    side = (board("side", ply15).on(m.left).between(m.front, m.back, m.bottom, m.top).show("inner")
            .chamfer("outline", 1)
            .chamfer("front.outer", 1)
            .hole(d=5, depth=10, face="inner", at=("front", 37, Pos("z", 50))))
