"""Concealed hinges: the drilling pattern of the Blum CLIP top 110 hinge for
thin doors, as the concealed_hinge_native add-in places it, in mm.

Each hinge needs a pair of holes in the door's inner face and a pair of
pre-drill holes for the mounting plate's screws in the face of the carcass
board the door is hinged on. Both pairs lie `HOLE_PAIR_SPACING` apart
along the hinged edge, centred on the hinge:

- The door holes, `DOOR_CUP_DIAMETER` wide and `DOOR_CUP_DEPTH` deep,
  form a row parallel to the hinged edge, the model's `door_row` from the
  carcass board's face toward the door's middle, whatever the door's
  overlay or gap (27 for the +0 model, 30 for +3).
- The carcass holes lie `CARCASS_ROW_INSET` behind the door's inner face,
  their diameter and depth the add-in's pre-drill settings.
- A door gets two hinges, their centres the End Margin from the ends of
  its hinged edge. Two hinges must stay more than `2 * HINGE_HALF_EXTENT`
  apart, a hole pair's outer extent (half the spacing plus a hole's
  radius) on each side.

Source: the add-in's constants (concealed_hinge_native/main.py, "Blum CLIP
top hinge drilling specification"); the data sheet they were taken from is
not in the repo. Shared by the add-in (which converts to cm) and the
modeling language (lang/hardware/hinges.py). Plain Python without Fusion
imports; `python3 -m lib.concealed_hinges` runs its self-checks.
"""
from dataclasses import dataclass


#: Distance between the two holes of a pair, along the hinged edge.
HOLE_PAIR_SPACING = 32.0
#: Diameter of the door holes (the add-in calls them cups).
DOOR_CUP_DIAMETER = 10.0
#: Depth of the door holes, flat-bottomed.
DOOR_CUP_DEPTH = 5.0
#: The carcass holes' row behind the door's inner face.
CARCASS_ROW_INSET = 38.5
#: A hole pair's outer extent from the hinge's centre along the edge: half
#: the pair spacing plus a door hole's radius. Two hinges must stay more
#: than twice this apart.
HINGE_HALF_EXTENT = HOLE_PAIR_SPACING / 2 + DOOR_CUP_DIAMETER / 2

# -- the add-in's dialog defaults and limits ------------------------------------------

#: Default distance from each end of the door's hinged edge to the
#: nearest hinge centre (End Margin).
DEFAULT_END_MARGIN = 60.0
#: The dialog's smallest End Margin (its validation alone would allow
#: `HINGE_HALF_EXTENT`).
MIN_END_MARGIN = 27.0
#: Default diameter of the carcass pre-drill holes: 1/8 inch.
DEFAULT_PREDRILL_DIAMETER = 25.4 / 8
#: Default depth of the carcass pre-drill holes.
DEFAULT_PREDRILL_DEPTH = 3.0
#: The dialog's smallest pre-drill diameter and depth.
MIN_PREDRILL = 0.1


@dataclass(frozen=True)
class HingeModel:
    #: Dropdown value; stored with editable results, so never reuse one.
    value: int
    name: str
    #: The door holes' row from the carcass board's face, toward the door's
    #: middle.
    door_row: float


CLIP_TOP_THIN_0 = HingeModel(0, "Blum CLIP top 110 Thin +0", 27.0)
CLIP_TOP_THIN_3 = HingeModel(1, "Blum CLIP top 110 Thin +3", 30.0)

#: Every model by name, in dropdown order.
HINGE_MODELS: dict[str, HingeModel] = {model.name: model for model in (CLIP_TOP_THIN_0, CLIP_TOP_THIN_3)}


def _self_check() -> None:
    models = list(HINGE_MODELS.values())
    assert [model.value for model in models] == list(range(len(models)))
    assert len({model.name for model in models}) == len(models)
    assert HINGE_HALF_EXTENT == 21.0
    # The +3 model sits 3 mm further from the carcass board, nothing else changes.
    assert CLIP_TOP_THIN_3.door_row - CLIP_TOP_THIN_0.door_row == 3.0
    assert HINGE_HALF_EXTENT <= MIN_END_MARGIN <= DEFAULT_END_MARGIN
    assert MIN_PREDRILL <= DEFAULT_PREDRILL_DIAMETER and MIN_PREDRILL <= DEFAULT_PREDRILL_DEPTH
    # The door holes stay clear of the carcass board's face.
    for model in models:
        assert model.door_row > DOOR_CUP_DIAMETER / 2
    # Converted to cm as the add-in does, the values are the literals it had.
    assert HOLE_PAIR_SPACING / 10 == 3.2 and DOOR_CUP_DIAMETER / 10 == 1.0 and DOOR_CUP_DEPTH / 10 == 0.5
    assert CARCASS_ROW_INSET / 10 == 3.85
    assert {model.value: model.door_row / 10 for model in models} == {0: 2.7, 1: 3.0}
    assert DEFAULT_END_MARGIN / 10 == 6 and MIN_END_MARGIN / 10 == 2.7
    assert DEFAULT_PREDRILL_DIAMETER / 10 == 2.54 / 8 and DEFAULT_PREDRILL_DEPTH / 10 == 0.3
    assert MIN_PREDRILL / 10 == 0.01
    print("concealed_hinges: all checks passed")
    for model in models:
        print(f"  {model.name}: door holes {model.door_row:g} from the carcass face, "
              f"carcass holes {CARCASS_ROW_INSET:g} behind the door")


if __name__ == "__main__":
    _self_check()
