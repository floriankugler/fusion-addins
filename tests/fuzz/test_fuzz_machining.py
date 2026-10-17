"""Fuzzing the CAM plan (`machining.py`): random nests planned and checked.
A case nests with the solvers, a fraction of a second, so it gets a
fraction of the profile's examples."""
from hypothesis import given, settings

from boards import Feature
from machining import PlanCase, plan_cases, run_plan
from nesting import PartCase

#: The profile's number of examples (`tests/conftest.py`).
EXAMPLES = settings().max_examples


@settings(max_examples=max(4, EXAMPLES // 5))
@given(plan_cases())
def test_a_plan_machines_every_operation_once_or_says_why_not(case: PlanCase):
    assert run_plan(case) == []


# -- cases fuzzing found, where the plan and its check saw a cutter's reach or a
# part's hold otherwise (lang.cam.regions, lang.cam.verify) -----------------------------------------

def _one(part: PartCase, *, dogbones: bool = False, tabs: str = "", cutter: str = "dc",
         finish: tuple[bool, bool, bool] = (False, False, False), tab_margin: float = 6.0, waste_area: float = 10.0,
         named: bool = False) -> PlanCase:
    return PlanCase((part,), (dogbones,), (0.0,), (tabs,), cutter, finish, tab_margin, waste_area, named)


def test_a_parts_hold_is_the_same_wherever_the_nest_lays_it():
    """Shrunk on the blank, a narrow neck pinched off or not as the part
    lay, so its tabs came and went with its place: a hold is measured in the
    part's own frame [found by fuzzing, 2026-10-17]."""
    part = PartCase(material=2, side="right", size=(55.5, 80.0), features=(
        Feature("slot", 1, 30.92371546261258, 39.5, 33.40993405872519, 34.12992389194038, 0.0, None),
        Feature("pocket", 1, 5.0, 32.267404853558624, 40.0, 12.0, 45.0, None),
        Feature("notch", 0, 11.55841683558535, 35.5, 78.93060309479175, 93.0, 0.0, 0.5),
        Feature("hole", 1, 28.5, 65.0, 5.5, 0.0, 0.0, 0.9327604084429254)), grain="second", machined=1, machine=1)
    assert run_plan(_one(part, dogbones=True, cutter="udc", finish=(True, True, True), tab_margin=12.0,
                         waste_area=40.0, named=True)) == []


def test_the_plan_writes_its_rings_unrounded():
    """Rounded to a nanometre, a ring where a circle meets an edge at a
    glancing angle recovered its arcs otherwise, and the check saw other
    corners than the plan [found by fuzzing, 2026-10-17]."""
    part = PartCase(material=0, side="right", size=(877.0292709021292, 95.0),
                    origin=(378.0, -1460.29921094084, 333.0), features=(
        Feature("hole", 0, 1.0, 78.77059028462224, 4.5, 0.0, 0.0, None),
        Feature("pocket", 1, 47.88126092980788, 60.2090271344357, 109.0, 0.0, 108.59034371367083, 0.5),
        Feature("slot", 0, 259.8204621998555, 51.0, 0.5, 61.65101452945601, 356.58398838179215, 0.3688785543924187),
        Feature("edge_hole", 2, 0.0, 95.0, 11.5, 6.0, 0.0, None)), grain="second", nested=False, machine=1)
    assert run_plan(_one(part, tabs="none", tab_margin=3.0, waste_area=0.0, named=True)) == []


def test_a_rest_has_room_around_what_it_takes():
    """A rest that was only what the wider cutter left missed the corner's
    fillet beside it, which a cutter a hair smaller leaves with it: a rest
    reaches into what the wider one cleared (now a cutter's diameter and the
    clearance) [found by fuzzing, 2026-10-17]."""
    part = PartCase(material=2, side="back", size=(126.02619231962115, 344.94422405029616), features=(
        Feature("hole", 0, 7.0, 307.94422405029616, 25.0, 0.0, 0.0, 0.5),
        Feature("hole", 0, 10.0, 324.94422405029616, 18.55368990985904, 0.0, 0.0, 0.6308834993105018)),
        grain="second", machined=1)
    assert run_plan(_one(part, tabs="none", finish=(False, True, False))) == []


def test_a_corner_on_the_edge_of_being_a_fillet_is_no_fault():
    """Of two mirror-image corners where a round pocket meets the board's
    edge, one fillet passed and the other did not as the noise fell: the
    check is lenient by a hundredth [found by fuzzing, 2026-10-17]."""
    part = PartCase(material=0, side="right", size=(40.0, 300.0), origin=(415.0, 0.0, -2986.5), frame=13,
                    features=(Feature("hole", 1, 37.65, 276.0, 18.0, 0.0, 0.0, 0.24574370009769742),),
                    grain="second", machined=1, nested=False)
    assert run_plan(_one(part, tabs="auto", cutter="udc", finish=(False, True, False), tab_margin=3.0,
                         named=True)) == []


def test_each_piece_of_a_pocket_has_its_own_rests():
    """A pocket in two pieces shares its operation, and one piece's rests
    were judged against the other's cutter [found by fuzzing, 2026-10-17]."""
    part = PartCase(material=0, side="front", size=(137.0, 119.5), origin=(2717.0, 0.0, 30.0), features=(
        Feature("slot", 1, 52.5, 25.43747801059446, 38.0, 92.0, 90.0, 0.5),),
        opening=(0.6714566566125633, 0.8), machined=1)
    assert run_plan(_one(part, tabs="forced", cutter="udc", tab_margin=3.0)) == []
