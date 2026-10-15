"""Fuzzing `Board.lip()` on random boards (`lips.lip_cases`): it must keep
what it promises, the board lying, standing or upright, anywhere
(`lips.run_case`)."""
from hypothesis import given

from boards import KNOWN
from lips import LipCase, lip_cases, run_case


@given(lip_cases())
def test_lips_keep_their_promises_on_any_board(case: LipCase):
    assert [p for p in run_case(case) if not p.startswith(KNOWN)] == []
