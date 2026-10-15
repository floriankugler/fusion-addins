"""Connector dimensions in mm: Festool DOMINO, Lamello Clamex P and Lamello
Cabineo, as the connectors_native add-in machines them.

Each connector joins a board that meets another one edge-on (its end or
edge against the other board's face). Both boards are machined from their
big faces only; nothing is cut into a narrow face, which a 3-axis machine
cannot reach:

- Domino: a slot in the face of the board that is met. The mortise in the
  edge-on board's end is cut later with the Domino machine; optional
  V-grooves on that board's face mark where.
- Clamex P: an access hole (P-14) or slot (P-10) in the edge-on board's
  face near its end, and two guide holes in the other board's face.
- Cabineo: a pocket of three overlapping circles in the edge-on board's
  face, open toward its end, and a hole for the screw in the other board's
  face.

"From the edge" is measured across the edge-on board's face, away from the
line where its end meets the face that carries the access holes.

Shared by connectors_native (the Domino part through lib/domino.py) and the
modeling language (lang/joints/connectors.py). Plain Python without Fusion
imports: `python3 -m lib.connector_data` runs its self-checks.
"""
from dataclasses import dataclass

from . import stations as _stations


# -- positions along the edge -------------------------------------------------------

#: Distance from each end of the edge to the first and last Clamex or
#: Cabineo connector (the add-in's End Offset default), mm.
DEFAULT_END_OFFSET = 60.0


def stations(length: float, count: int, end_offset: float) -> list[float]:
    """Distances from the start of an edge `length` long: `count` stations,
    the first and last `end_offset` from the ends and the rest evenly
    spaced between them (`lib.stations`). A single station is centred.
    Unit-free; the edge's length is not checked against the offset."""
    if count < 1:
        raise ValueError("At least one connector is needed.")
    return _stations.stations(length, count, end_offset)


# -- Domino --------------------------------------------------------------------------

@dataclass(frozen=True)
class DominoSize:
    """Festool DOMINO tenon dimensions in mm, as published in Festool's
    technical data ("thickness x length x width")."""

    #: Dropdown value; stored with editable results, so never reuse one.
    value: int
    thickness: float
    width: float
    length: float

    @property
    def name(self) -> str:
        return f"{self.thickness:g} x {self.length:g}"

    @property
    def key(self) -> str:
        """The name without spaces, e.g. "5x30"."""
        return f"{self.thickness:g}x{self.length:g}"


DOMINO_SIZES = [
    DominoSize(420, 4, 16.6, 20),
    DominoSize(530, 5, 18.8, 30),
    DominoSize(640, 6, 19.8, 40),
    DominoSize(836, 8, 21.9, 36),
    DominoSize(840, 8, 21.9, 40),
    DominoSize(850, 8, 21.9, 50),
    DominoSize(880, 8, 21.9, 80),
    DominoSize(8100, 8, 21.9, 100),
    DominoSize(1050, 10, 23.9, 50),
    DominoSize(1080, 10, 23.9, 80),
    DominoSize(10100, 10, 23.9, 100),
    DominoSize(12100, 12, 25.9, 100),
    DominoSize(12140, 12, 25.9, 140),
    DominoSize(1475, 14, 27.9, 75),
    DominoSize(14100, 14, 27.9, 100),
    DominoSize(14140, 14, 27.9, 140),
]

#: Distance from the board end to the first and last Domino set by the
#: machine's built-in stop latches (stop pins on older machines), mm.
DOMINO_STOP_LATCH = 37.0
#: The same with the additional stop ZA-DF 500/700 fitted, mm.
DOMINO_ADDITIONAL_STOP = 20.0
#: Added to half the Domino's length to get the slot depth, mm.
DOMINO_DEPTH_OFFSET = 0.5
#: The slots are this much shorter and narrower than the Domino, their
#: outline inset by half of it on every side, so the Domino fits tight;
#: the slot's depth is not changed, mm.
DOMINO_SLOT_UNDERSIZE = 0.2
#: The two wider mortise settings of the Domino DF 500 (13, 19 or 23 mm
#: plus the cutter diameter), as extra slot length, mm.
DOMINO_LOOSE_STEPS = (6.0, 10.0)
#: Depth and length (from the edge) of the V-groove marks, mm.
DOMINO_MARK_DEPTH = 0.3
DOMINO_MARK_LENGTH = 4.0


@dataclass(frozen=True)
class FenceStop:
    """A height stop of the Domino machine's fence. Stops are labelled with
    the board thickness they centre the mortise on, so the mortise ends up
    half that far from the face the fence rests on."""

    #: Dropdown value; stored with editable results, so never reuse one.
    value: int
    thickness: float
    label: str

    @property
    def name(self) -> str:
        return f"{self.thickness:g} mm ({self.label})"


FENCE_STOPS = [
    FenceStop(1000 + thickness, thickness, "Festool")
    for thickness in (16, 20, 22, 25, 28, 36, 40)
] + [
    # Aftermarket (e.g. 3D-printed) stop gauges add further thicknesses.
    FenceStop(2000 + thickness, thickness, "Alternative")
    for thickness in (10, 12, 13, 16, 18)
]


def domino_size(key: str) -> DominoSize:
    """A size by its key, e.g. "5x30"."""
    for size in DOMINO_SIZES:
        if size.key == key:
            return size
    raise ValueError(
        f"Unknown Domino size {key!r}; sizes: "
        + ", ".join(size.key for size in DOMINO_SIZES)
    )


# -- Clamex P ------------------------------------------------------------------------

@dataclass(frozen=True)
class ClamexModel:
    name: str
    #: Centres of the access hole (one) or of the access slot's two ends,
    #: from the edge, mm.
    access_centers: tuple[float, ...]
    #: Diameter of the access hole or width of the access slot, mm.
    access_width: float


CLAMEX_P10 = ClamexModel("P-10", (5.0, 7.5), 6.0)
CLAMEX_P14 = ClamexModel("P-14", (7.5,), 6.0)
CLAMEX_MODELS = {"P-10": CLAMEX_P10, "P-14": CLAMEX_P14}
#: The two guide holes in the other board lie this far apart, centred on
#: the connector and on the edge-on board's thickness, mm.
CLAMEX_GUIDE_SPACING = 101.0
CLAMEX_GUIDE_DIAMETER = 7.7
CLAMEX_GUIDE_DEPTH = 8.0
# The access hole or slot is half the edge-on board's thickness deep.
#: The narrowest gap between tenons (or beside them) a Clamex fits in, mm.
CLAMEX_MIN_GAP = 120.0


# -- Cabineo -------------------------------------------------------------------------

#: Centres of the three overlapping circles of the access pocket, from the
#: edge; the first breaks through the edge-on board's end, mm.
CABINEO_ACCESS_CENTERS = (3.6, 14.8, 26.0)
CABINEO_ACCESS_DIAMETER = 15.0
CABINEO_ACCESS_DEPTH = 10.5
#: Access depth with a flush relief, mm.
CABINEO_FLUSH_ACCESS_DEPTH = 11.0
#: The flush relief: a slot from the edge to the last access centre, this
#: wide and deep, mm.
CABINEO_FLUSH_RELIEF_WIDTH = 16.7
CABINEO_FLUSH_RELIEF_DEPTH = 0.8
#: The anti-break relief: the access circles widened by this much on every
#: side, and this deep (defaults), mm.
CABINEO_ANTI_BREAK_DISTANCE = 0.6
CABINEO_ANTI_BREAK_DEPTH = 0.8
#: Centre of the screw hole in the other board, from the access face across
#: the edge-on board's thickness, mm; with a flush relief.
CABINEO_GUIDE_OFFSET = 5.0
CABINEO_FLUSH_GUIDE_OFFSET = 5.8
#: The narrowest gap between tenons (or beside them) a Cabineo fits in, mm.
CABINEO_MIN_GAP = 40.0


@dataclass(frozen=True)
class GuideHole:
    """The hole for the Cabineo's screw or insert in the other board, mm.
    A threaded insert also has a shallow, wider collar."""

    diameter: float
    depth: float
    collar_diameter: float | None = None
    collar_depth: float | None = None


#: By model; the Cabineo 8 M6 by the part it takes.
CABINEO_GUIDE_HOLES = {
    "8": GuideHole(5.0, 8.0),
    "12": GuideHole(5.0, 12.0),
    "8 M6 x 12.3": GuideHole(8.0, 13.5),
    "8 M6 x 15.3": GuideHole(8.0, 16.5),
    "8 M6 threaded insert": GuideHole(7.9, 13.5, 12.7, 0.8),
}


# -- Screws ---------------------------------------------------------------------------

#: The tenon add-in's defaults: screw diameter, and the distance of the
#: two-sided screws from a tenon's edge, mm.
SCREW_DIAMETER = 4.0
SCREW_OFFSET = 12.0
#: A countersunk head (SPAX Universal) is about twice as wide as the thread
#: (3.5 -> 7.0, 4.0 -> 8.0, 4.5 -> 8.8, 5.0 -> 9.7 mm); a 90 degree
#: countersink twice the diameter plus this wide lets it sit just below the
#: surface, mm.
SCREW_COUNTERSINK_MARGIN = 0.4


def countersink_diameter(screw: float) -> float:
    return 2 * screw + SCREW_COUNTERSINK_MARGIN


def _self_check() -> None:
    assert stations(100, 1, 10) == [50]
    assert stations(100, 3, 10) == [10, 50, 90]
    assert [size.key for size in DOMINO_SIZES][:3] == ["4x20", "5x30", "6x40"]
    assert len({size.value for size in DOMINO_SIZES}) == len(DOMINO_SIZES)
    assert domino_size("8x50").width == 21.9
    # Undersized, the thinnest Domino still leaves a slot.
    assert 0 < DOMINO_SLOT_UNDERSIZE < min(size.thickness for size in DOMINO_SIZES)
    assert len({stop.value for stop in FENCE_STOPS}) == len(FENCE_STOPS)
    # The access pocket's first circle breaks through the board's end.
    assert CABINEO_ACCESS_CENTERS[0] < CABINEO_ACCESS_DIAMETER / 2
    print("connector_data: all checks passed")


if __name__ == "__main__":
    _self_check()
