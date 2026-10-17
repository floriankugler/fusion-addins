"""How exactly the preview meshes a layout: its levels, by name.

Kept apart from the mesher (`lang.preview.mesh`), which imports trimesh, so
that the build's command line and the preview server know the names
without it.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Level:
    """A level of the preview's meshes. `tolerance`: how far (mm) a chord
    may lie inside its arc where the mesher draws the layout's arcs and
    circles again (recovered with `lang.emit.arcs.fit`), never with more
    segments than the layout's polygon gives them; None to mesh the
    layout's polygons as they are, a vertex a degree on the language's
    circles. Only the triangles change, never the layout. (A level that
    leaves operations out, the rough one of
    `design/proposals/detail-levels.md`, would say here what it leaves
    out.)"""
    name: str
    tolerance: float | None


#: The layout's polygons as they are; what the tests and the Fusion batch
#: check mesh at, as they compare volumes.
FINE = Level("fine", None)
#: Arcs drawn with chords at most 0.05 mm inside them: a relief circle of
#: radius 3 gets 18 segments instead of 360, a corner of radius 500 still
#: about 220 a full turn. The preview's default.
NORMAL = Level("normal", 0.05)
#: The levels by name, finest first.
LEVELS = {level.name: level for level in (FINE, NORMAL)}
