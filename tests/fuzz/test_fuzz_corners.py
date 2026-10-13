"""Fuzzing `Board.dogbones()` and `Board.chamfer()` on random boards
(`corners.corner_op_cases`): each must keep what it promises, the board lying,
standing or upright, anywhere (`corners.run_case`)."""
from hypothesis import given

from boards import KNOWN
from corners import CornerOpCase, corner_op_cases, run_case


@given(corner_op_cases())
def test_dogbones_and_chamfers_keep_their_promises_on_any_board(case: CornerOpCase):
    assert [p for p in run_case(case) if not p.startswith(KNOWN)] == []
