"""Fuzzing the placement algebra (modules, scopes, boxes, positions,
directions and frames, faces and anchors, `on`, `between`, `center`,
`inset`, `show`) on random designs (`placement.placement_cases`): each
must come out the same moved, in another world frame and written another
way, and keep what placement promises (`placement.run_case`)."""
from hypothesis import given

from boards import KNOWN
from placement import PlacementCase, placement_cases, run_case


@given(placement_cases())
def test_a_design_comes_out_the_same_wherever_and_however_it_is_placed(case: PlacementCase):
    assert [p for p in run_case(case) if not p.startswith(KNOWN)] == []
