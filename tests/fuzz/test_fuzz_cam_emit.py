"""Fuzzing the CAM emitter's mapping (`cam_emit.py`): random plans mapped
into the nested document, and random nests planned and mapped. A real
case nests with the solvers, so it gets a fraction of the profile's
examples."""
from hypothesis import given, settings

from cam_emit import EmitCase, emit_plans, run_emit_nest, run_emit_plan
from machining import PlanCase, plan_cases

#: The profile's number of examples (`tests/conftest.py`).
EXAMPLES = settings().max_examples


@given(emit_plans())
def test_a_plan_is_mapped_where_the_nested_document_has_its_blanks(case: EmitCase):
    assert run_emit_plan(case) == []


@settings(max_examples=max(3, EXAMPLES // 8))
@given(plan_cases())
def test_a_planned_nests_holes_and_grooves_are_bound_where_the_document_draws_them(case: PlanCase):
    assert run_emit_nest(case) == []
