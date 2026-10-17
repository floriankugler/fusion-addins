"""The CAM plan file's shape, version 1: what `python -m lang.cam` writes
per nest (`cam.json`, beside the nest's `nest.json`), read by the Fusion
emitter, which repeats `CAM_VERSION` and refuses others, and by the
preview.

A plan is the nest's blanks as setups, one per blank: its stock, and its
operations in the order they run, each a Fusion operation made from one of
Florian's templates (`lang.cam.tooling`), with the parameters the emitter
sets on it and the features it machines. No toolpaths.

Millimetres. A setup's frame is its blank's in the nest file: x along the
blank's length (the sheet's grain), y across, from the blank's corner, so a
point is where the nest's `transform` puts it; Z zero is the stock's top,
always [decided 2026-10-15], negative into it. Every feature's geometry is
given in that frame, at the stock's top (the parts lie machining face up),
for the emitter to find the faces and edges by position, as it finds a
chamfer's now. Depths are millimetres down from the stock's top; None is
through. Rings run counter-clockwise around what they enclose, holes
clockwise, as the layout's.
"""
from __future__ import annotations

from typing import Literal, TypedDict

from ..core.layout_types import JsonValue, SettingLayout

CAM_VERSION = 1

Point = list[float]
#: A closed ring of [x, y] points, the first not repeated.
Ring = list[Point]


class OpRef(TypedDict):
    """What of a layout operation a feature machines or the plan leaves
    out: the operation's index in its part's `ops` (in the nest's layout;
    -1 for the outline), its name, its kind, and the aspect: `op` (the
    operation itself, for a cut its share of the outline), `chamfer` (its
    chamfer), `relief <k>` (its k-th dog bone), `ring <k>` (the outline's
    k-th ring, 0 the outer one, from the machining face)."""
    index: int
    name: str | None
    kind: str
    aspect: str


class ToolOut(TypedDict):
    """The template's cutter, its widest tool."""
    #: Fusion's tool type ("flat end mill", "chamfer mill").
    type: str
    diameter: float
    flute: float | None
    #: The flank's angle against the axis (45 for the 90 degree V-bit).
    taper: float | None
    tip: float


class HeightOut(TypedDict):
    """A height parameter as Fusion takes it: its mode and offset (mm, up)."""
    mode: Literal["from stock top", "from stock bottom", "from hole bottom", "from contour"]
    offset: float


class TabsOut(TypedDict):
    """Tabs at given positions, on the contours they lie on; every other
    contour of the operation gets none (`tabsPerContour` 0)."""
    width: float
    height: float
    #: [x, y] on the contours, in the setup's frame.
    positions: list[Point]


class ParamsOut(TypedDict):
    """What the emitter sets on the operation the template makes."""
    top: HeightOut
    bottom: HeightOut
    #: Several depths (`doMultipleDepths`); None: as the template has it.
    multiple_depths: bool | None
    #: A V-groove's passes above its last (Trace's `numberOfStepdowns`);
    #: None: as the template has it.
    stepdowns: int | None
    #: The contours cut in the order given (`preserveOrder`).
    preserve_order: bool
    #: A bore's cutting feed is the template's times this, the hole's
    #: diameter in tool diameters (Auto Setup's rule, capped there); None:
    #: the template's.
    feed_scale: float | None
    tabs: TabsOut | None


class ContourFeature(TypedDict):
    """A contour cut along a part's outline: its outer ring, or an inner
    one whose waste survives the cut."""
    what: Literal["outer", "inner"]
    part: str
    ops: list[OpRef]
    #: The contour, the part's material on its left: counter-clockwise for
    #: the outer, clockwise for an inner one.
    ring: Ring


class PocketFeature(TypedDict):
    """A pocket's region (one of its pieces, or an inner contour's waste
    taken out whole, `depth` None), or a rest: where a wider cutter of the
    same pocket did not reach."""
    what: Literal["pocket", "rest"]
    part: str
    ops: list[OpRef]
    #: The region: its outer ring, then its islands.
    rings: list[Ring]
    depth: float | None
    #: A slot's centre line (its round ends' centres) and width, else None.
    slot: SlotOut | None


class SlotOut(TypedDict):
    start: Point
    end: Point
    width: float


class HoleFeature(TypedDict):
    what: Literal["hole"]
    part: str
    ops: list[OpRef]
    center: Point
    d: float
    depth: float | None


class DogboneFeature(TypedDict):
    """A dog bone the operation it belongs to cannot reach (`lang.core.dogbones`):
    milled along its wall with a dog bone cutter, or plunged with a drill
    of its diameter."""
    what: Literal["dogbone"]
    part: str
    ops: list[OpRef]
    center: Point
    d: float
    #: The cutter it was drawn for.
    tool: float
    depth: float | None
    #: Its wall: points along the circle where it borders the material,
    #: from one end to the other, the material on the right.
    arc: list[Point]


class ChamferFeature(TypedDict):
    """A 45 degree chamfer along an edge at the stock's top, `size` along
    both faces: the edge as it is before the chamfer, the material on its
    left, closed or open; a hole's rim also by its centre and diameter."""
    what: Literal["chamfer"]
    part: str
    ops: list[OpRef]
    size: float
    paths: list[PathOut]
    hole: HoleRim | None


class PathOut(TypedDict):
    points: list[Point]
    closed: bool


class HoleRim(TypedDict):
    center: Point
    d: float


class GrooveFeature(TypedDict):
    """A 90 degree V-groove from `start` to `end`, `depth` deep."""
    what: Literal["vgroove"]
    part: str
    ops: list[OpRef]
    start: Point
    end: Point
    depth: float


Feature = ContourFeature | PocketFeature | HoleFeature | DogboneFeature | ChamferFeature | GrooveFeature

#: An operation's kind: the template kind it is made from, but `release`,
#: made from the contour template (the thin last pass that cuts the skin).
OperationKind = Literal["drill", "bore", "pocket", "contour", "dogbone", "chamfer", "groove", "release"]


class OperationOut(TypedDict):
    #: What Fusion calls it ("6 mm: contours, roughing").
    name: str
    kind: OperationKind
    #: The template file's name without its extension, and its label.
    template: str
    label: str
    tool: ToolOut
    params: ParamsOut
    features: list[Feature]


class StockOut(TypedDict):
    material: str
    #: The sheet (`1`) and the blank (`1.2`) in the nest file.
    sheet: str
    blank: str
    #: The blank on its sheet: x, y, w, h.
    rect: list[float]
    #: Its thickness, nominal: the material's.
    thickness: float
    #: A `nest(False)` board's own blank: its operations only, no outline.
    own_blank: bool


class PartOut(TypedDict):
    """A part on the blank, as the plan holds it."""
    path: str
    #: Its footprint shrunk by `cam.tab_margin` (cm²): its hold, by which
    #: it is released.
    hold: float
    #: `cam.tabs` for it, and whether it gets tabs, with the count.
    tab_policy: Literal["none", "auto", "forced"]
    tabs: int


class ReleaseOut(TypedDict):
    """A contour cut free by a release operation, in the order they run."""
    part: str
    what: Literal["outer", "inner"]
    #: The ring's index in the part's outline.
    ring: int
    #: The cutter's diameter.
    tool: float


class LeftOutOut(TypedDict):
    part: str
    op: OpRef
    #: `other face` (made from the part's other big face, reported),
    #: `narrow face` (taken care of, not reported [decided 2026-10-15]),
    #: `nothing fits` (no template's cutter), `hand work` (an own blank's
    #: outline), `gone` (nothing left of it).
    why: Literal["other face", "narrow face", "nothing fits", "hand work", "gone"]
    note: str


class SetupOut(TypedDict):
    #: `<nest> <material> <sheet>.<blank>`.
    name: str
    stock: StockOut
    parts: list[PartOut]
    operations: list[OperationOut]
    #: The release operations' contours, smallest hold first.
    release_order: list[ReleaseOut]
    left_out: list[LeftOutOut]
    problems: list[str]


class CamSettings(TypedDict):
    """The values the plan ran with (`lang.cam.keys`): per key the value
    for the nest, or the default, where it came from, and the parts and
    named operations that have values of their own."""
    values: dict[str, JsonValue]
    sources: dict[str, str]
    parts: dict[str, dict[str, SettingLayout]]
    #: Part path, then operation name.
    ops: dict[str, dict[str, dict[str, SettingLayout]]]
    #: Where the settings were read: the build as it is now ("build"), or
    #: the layout nested ("nest").
    read_from: Literal["build", "nest"]
    #: The templates' folder read.
    templates: str
    #: The smallest cutter (mm) the nest's manufacturing groups and the
    #: checks may count on: `cam.smallest_cutter`, else the narrowest
    #: cutter of the pocket and contour templates for the nest's cutter.
    smallest_cutter: float


class CamFile(TypedDict):
    version: int
    #: The nest planned: its name, when it was written and its layout's
    #: hash, as its file says them; the emitter refuses a plan whose nest
    #: is not the file beside it.
    nest: str
    nest_written: str
    layout_hash: str
    #: When this plan was written, ISO 8601 with the time zone.
    written: str
    settings: CamSettings
    setups: list[SetupOut]
    #: What the plan could not do or found wrong, every setup's too.
    problems: list[str]


__all__ = ["CAM_VERSION", "OpRef", "ToolOut", "HeightOut", "TabsOut", "ParamsOut", "ContourFeature", "PocketFeature",
           "SlotOut", "HoleFeature", "DogboneFeature", "ChamferFeature", "PathOut", "HoleRim", "GrooveFeature",
           "Feature", "OperationKind", "OperationOut", "StockOut", "PartOut", "ReleaseOut", "LeftOutOut", "SetupOut",
           "CamSettings", "CamFile"]
