"""Joint types: objects with their settings, applied with `part.join(joint)`.

Each reduces to operations on both parts (cuts, pockets, holes), so the
emitter needs nothing per joint. Half laps join crossing boards
(`lang.core.crossing`), connectors, tenons, screws, box joints and grooves boards that meet
edge-on (`lang.core.contact`, shared machinery in `common`). See design/joints.md.
"""
from .box_joints import BoxJoint, box_joint
from .connectors import Cabineo, Clamex, Domino, cabineo, clamex, domino
from .grooves import Groove, groove
from .laps import HalfLap, half_lap
from .screws import Screws, screws
from .tenons import Tenons, tenons

__all__ = ["HalfLap", "half_lap", "Domino", "Clamex", "Cabineo", "domino", "clamex", "cabineo", "Tenons", "tenons",
           "Screws", "screws", "BoxJoint", "box_joint", "Groove", "groove"]
