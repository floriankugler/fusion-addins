"""Joint types: objects with their settings, applied with `part.join(joint)`.

Each reduces to operations on both parts (cuts, pockets, holes), so the
emitter needs nothing per joint. See DESIGN.md, "Joints and hardware".
"""
from .laps import HalfLap, half_lap

__all__ = ["HalfLap", "half_lap"]
