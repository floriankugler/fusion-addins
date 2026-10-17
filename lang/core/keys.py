"""The core's settings (`settings.py`, `design/api.md`, Settings), read by
boards and their operations in `part.py`, exported bare from `lang`:

- `material`: what a board is made of. No default: a board has its own
  (`board(name, ply15)` uses it on the board) or takes the nearest one used
  above it, and a board with neither is an error, as a forgotten material
  always was.
- `grain`: the grain direction of a board of a grained material, what
  `grain()` takes; an extent is read in the frame of the node that uses
  it. Unset by default.
- `nest`: whether a board goes into the nest; True by default.
- `chamfer_size`: the size of a chamfer that gives none (mm, along both
  faces). No default: `chamfer(what)` needs one used above it.

The layout reads `grain` and `nest`, nothing during the build, so they are
never frozen. A board says `material`, `grain` and `nest` through its own
call and modifiers, which are the one spelling of these keys on a board
[decided 2026-10-16]; `Board.use()` refuses them, naming that spelling.
"""
from __future__ import annotations

from typing import Any, Union, cast

from .directions import Axis, Direction, ExtentName, Frame
from .errors import LangError, one_of
from .faces import Face
from .material import SheetMaterial, SlatMaterial
from .refs import Side
from .settings import Setting

#: What `grain()` takes: an extent, a box side or direction, a face of a part.
GrainSpec = Union[ExtentName, Side, Direction, Face]


def sheet_material(value: object, what: str) -> SheetMaterial:
    """`value` as the material key holds it, or an error naming `what`."""
    if isinstance(value, SheetMaterial):
        return value
    if isinstance(value, SlatMaterial):
        raise LangError(f"{what}: {value.label} is a slat material, solid wood without a thickness; the material "
                        "setting is the boards', which take a sheet_material(), and a slat names its own.")
    raise LangError(f"{what}: {value!r} is not a material; give a sheet_material().")


def grain_spec(value: object, what: str) -> GrainSpec:
    if isinstance(value, str):
        return cast(ExtentName, one_of(value, ExtentName, what))
    if isinstance(value, (Side, Direction, Face)):
        return value
    raise LangError(f"{what}: expected an extent ('width', 'depth' or 'height'), a box side or direction, or a "
                    f"face; not {value!r}.")


def grain_axis(spec: GrainSpec, frame: Frame) -> Axis:
    """The world axis a grain names; an extent is read in `frame`, the frame
    of the node that uses it."""
    return frame.axis_of_extent(spec) if isinstance(spec, str) else spec.axis


def _grain(value: object, what: str) -> GrainSpec | None:
    return None if value is None else grain_spec(value, what)


def _nested(value: object, what: str) -> bool:
    if not isinstance(value, bool):
        raise LangError(f"{what} takes True or False, not {value!r}.")
    return value


def _size(value: object, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise LangError(f"{what} takes a size in mm, not {value!r}.")
    return float(value)


material: Setting[SheetMaterial] = Setting(
    ..., "material", check=sheet_material, to_layout=lambda m, _: m.label,
    hint="board(name, material) gives a board its own, or ")
grain: Setting[GrainSpec | None] = Setting(
    None, "grain", check=_grain, to_layout=lambda spec, frame: None if spec is None else grain_axis(spec, frame))
nest: Setting[bool] = Setting(True, "nest", check=_nested)
chamfer_size: Setting[float] = Setting(
    ..., "chamfer_size", check=_size, hint="chamfer(what, size) gives a chamfer its own, or ")

#: The keys a board takes through a call or modifier of its own: `Board.use()`
#: refuses them, naming it.
OWN_SPELLING: dict[Setting[Any], str] = {
    material: "board(name, material)", grain: "grain()", nest: "nest()"}
