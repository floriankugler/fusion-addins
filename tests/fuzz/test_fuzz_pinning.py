"""Fuzzing pinning (`pinning`): random builds edited at random and random
sequences of runs, marks and fixes give the second nests, the parts made
and the inventory the model says, the inventory's comments kept."""
from hypothesis import given

from pinning import PinCase, pin_cases, pinning_problems


@given(pin_cases())
def test_runs_marks_and_fixes_follow_the_model(case: PinCase):
    assert pinning_problems(case) == []
