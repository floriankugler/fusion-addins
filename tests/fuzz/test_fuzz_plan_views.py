"""Fuzzing the preview's CAM layer (`plan_views.py`): random plans as the
nest view lists and draws them. A case nests and plans, a fraction of a
second, and runs the view's code in node, so it gets a fraction of the
profile's examples; skipped without node."""
import shutil

import pytest
from hypothesis import given, settings

from machining import PlanCase, plan_cases
from plan_views import run_view

#: The profile's number of examples (`tests/conftest.py`).
EXAMPLES = settings().max_examples

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node is not on PATH")


@settings(max_examples=max(3, EXAMPLES // 6))
@given(plan_cases())
def test_the_nest_view_lists_and_draws_a_plan_as_it_is(case: PlanCase):
    assert run_view(case) == []


def test_a_hole_across_the_parts_edge_is_a_notch_drawn_and_a_hole_planned():
    """The nest draws an 11 mm through hole that crosses the part's edge as
    a notch in its outline; the plan bores it beside a straight contour.
    The view draws both as they are [found by fuzzing the view's check,
    2026-10-17]."""
    from boards import Feature
    from nesting import PartCase
    part = PartCase(material=0, side="top", size=(55.5, 245.5), frame=13, features=(
        Feature("hole", 0, 54.5, 216.5, 11.0, 0.0, 0.0, None),), opening=(0.46248192810969574, 0.4500527992938383),
        grain="second", machined=1, machine=-1)
    case = PlanCase((part,), (False,), (1.0,), ("auto",), "dc", (False, True, False), 12.0, 40.0, False)
    assert run_view(case) == []
