"""Fuzzing the standard library (`lang.std`) on random carcasses
(`carcasses.carcass_cases`): `carcass()` must keep what it promises,
facing any way (`carcasses.run_case`)."""
from hypothesis import given

from carcasses import CarcassCase, carcass_cases, run_case


@given(carcass_cases())
def test_carcass_keeps_its_promises_facing_any_way(case: CarcassCase):
    assert run_case(case) == []
