"""Fuzzing the joints between boards that meet edge-on (`lang.joints`) on
random pairs (`joints.pair_cases`): every joint must keep what it
promises (`joints.run_pair`)."""
from hypothesis import given

from boards import KNOWN
from joints import (CornerCase, CrossCase, FrameCase, PairCase, corner_cases, cross_cases, frame_cases,
                    pair_cases, run_corner, run_cross, run_frame, run_pair)


@given(pair_cases())
def test_a_joint_keeps_its_promises_on_any_pair(case: PairCase):
    assert [p for p in run_pair(case) if not p.startswith(KNOWN)] == []


@given(corner_cases())
def test_a_box_joint_keeps_its_promises_at_any_corner(case: CornerCase):
    assert [p for p in run_corner(case) if not p.startswith(KNOWN)] == []


@given(cross_cases())
def test_a_half_lap_keeps_its_promises_on_any_crossing(case: CrossCase):
    assert [p for p in run_cross(case) if not p.startswith(KNOWN)] == []


@given(frame_cases())
def test_a_groove_keeps_its_promises_in_any_frame(case: FrameCase):
    assert [p for p in run_frame(case) if not p.startswith(KNOWN)] == []
