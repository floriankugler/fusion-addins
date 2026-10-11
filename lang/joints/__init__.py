"""Joint types: objects with their settings, applied with `part.join(joint)`.

Each reduces to operations on both parts (cuts, pockets, holes), so the
emitter needs nothing per joint. Half laps join crossing boards
(`lang.core.crossing`), connectors, tenons and screws boards that meet edge-on
(`lang.core.contact`, shared machinery in `common`). See DESIGN.md, "Joints and hardware".
"""
from .connectors import Cabineo, Clamex, Domino, cabineo, clamex, domino
from .laps import HalfLap, half_lap
from .screws import Screws, screws
from .tenons import Tenons, tenons

__all__ = ["HalfLap", "half_lap", "Domino", "Clamex", "Cabineo", "domino", "clamex", "cabineo", "Tenons", "tenons",
           "Screws", "screws"]
