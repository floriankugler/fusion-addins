"""Fuzzing the hardware (`lang.hardware`) on random cabinets
(`hardware.hardware_cases`): every mount must keep what it promises,
facing any way (`hardware.run_case`)."""
from hypothesis import given

from boards import KNOWN
from hardware import (CatchCase, DoorCase, DrawerCase, HatchCase, PanelCase, catch_cases, door_cases, drawer_cases,
                      hatch_cases, panel_cases, run_case)


@given(door_cases())
def test_hinges_and_latches_keep_their_promises_on_any_door(case: DoorCase):
    assert [p for p in run_case(case) if not p.startswith(KNOWN)] == []


@given(panel_cases())
def test_sliding_brackets_keep_their_promises_on_any_panel(case: PanelCase):
    assert [p for p in run_case(case) if not p.startswith(KNOWN)] == []


@given(hatch_cases())
def test_hatch_hinges_keep_their_promises_on_any_hatch(case: HatchCase):
    assert [p for p in run_case(case) if not p.startswith(KNOWN)] == []


@given(catch_cases())
def test_ball_catches_keep_their_promises_in_any_opening(case: CatchCase):
    assert [p for p in run_case(case) if not p.startswith(KNOWN)] == []


@given(drawer_cases())
def test_drawer_slides_keep_their_promises_in_any_bay(case: DrawerCase):
    assert [p for p in run_case(case) if not p.startswith(KNOWN)] == []
