"""Fuzzing the placement of slats (`slats.slat_cases`): on(), edge_on(),
center() and between() put a slat where they say, in any world frame,
anywhere (`slats.run_case`)."""
from hypothesis import given

from slats import SlatCase, run_case, slat_cases


@given(slat_cases())
def test_slats_lie_where_their_placement_says(case: SlatCase):
    assert run_case(case) == []
