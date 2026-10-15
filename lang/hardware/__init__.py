"""Hardware: bought parts with their own rules (see design/hardware.md).
A hardware object knows what it dictates about the parts around it and
what it does to them when mounted; `scope.mount(hardware, ...)`
hands it the scope, with the keywords of the hardware's own typed `mount`,
which the type checker checks at the call.

So far: drawer slides (`drawer_slide()`, `slides`), concealed hinges
(`hinge()`, `hinges`), lift-up hatch hinges (`hatch_hinge()`,
`hatch_hinges`), ball catches for inspection hatches (`ball_catch()`,
`ball_catches`), door latches (`latch()`, `latches`) and sliding brackets
for removable panels (`sliding_bracket()`, `sliding_brackets`), each with a
string literal type of its models. A build file makes hardware with the
lowercase factories, as it makes parts with `board()`; each returns an
instance of its class (`DrawerSlide`, `ConcealedHinge`, `HatchHinge`,
`BallCatch`, `DoorLatch`, `SlidingBracket`), exported for annotations.
Each places its bought part as boxes
(`scope.place_hardware`) from one table of sizes measured from the makers'
CAD models and drawings, kept apart from the drilling data in `lib/`.
What they share is in `common`: one tolerance, the numbering along an
edge, world boxes, and the checks of every hole (`Board.hole_fits`, a
pilot hole short of the far face).
"""
from .ball_catches import BallCatch, CatchModel, ball_catch
from .hatch_hinges import HatchHinge, HatchHingeModel, hatch_hinge
from .hinges import ConcealedHinge, HingeModel, hinge
from .latches import DoorLatch, LatchModel, latch
from .slides import DrawerSlide, SlideModel, drawer_slide
from .sliding_brackets import BracketModel, SlidingBracket, sliding_bracket

__all__ = [
    "drawer_slide", "hinge", "hatch_hinge", "ball_catch", "latch", "sliding_bracket",
    "DrawerSlide", "SlideModel", "ConcealedHinge", "HingeModel", "HatchHinge", "HatchHingeModel",
    "BallCatch", "CatchModel", "DoorLatch", "LatchModel", "SlidingBracket", "BracketModel",
]
