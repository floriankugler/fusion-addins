"""Hardware: bought parts with their own rules (see design/hardware.md).
A hardware object knows what it dictates about the parts around it and
what it does to them when mounted; `scope.mount(hardware, ...)`
hands it the scope, with the keywords of the hardware's own typed `mount`,
which the type checker checks at the call.

So far: drawer slides (`DrawerSlide`, `slides`), concealed hinges
(`ConcealedHinge`, `hinges`), lift-up hatch hinges (`HatchHinge`,
`hatch_hinges`), ball catches for inspection hatches (`BallCatch`,
`ball_catches`), door latches (`DoorLatch`, `latches`) and sliding brackets
for removable panels (`SlidingBracket`, `sliding_brackets`), each with a
string literal type of its models. Each places its bought part as boxes
(`scope.place_hardware`) from one table of sizes measured from the makers'
CAD models and drawings, kept apart from the drilling data in `lib/`.
What they share is in `common`: one tolerance, the numbering along an
edge, world boxes, and the checks of every hole (`Board.hole_fits`, a
pilot hole short of the far face).
"""
from .ball_catches import BallCatch, CatchModel
from .hatch_hinges import HatchHinge, HatchHingeModel
from .hinges import ConcealedHinge, HingeModel
from .latches import DoorLatch, LatchModel
from .slides import DrawerSlide, SlideModel
from .sliding_brackets import BracketModel, SlidingBracket

__all__ = [
    "DrawerSlide", "SlideModel", "ConcealedHinge", "HingeModel", "HatchHinge", "HatchHingeModel",
    "BallCatch", "CatchModel", "DoorLatch", "LatchModel", "SlidingBracket", "BracketModel",
]
