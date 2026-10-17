"""Fuzzing the nest (`nesting.py`): how it sees parts, its saw plans and
whole nests, each checked from the outside. The solvers' cases take a
fraction of a second each, so they get a fraction of the profile's
examples."""
from hypothesis import given, settings
from hypothesis import strategies as st

from nesting import (NestCase, PartCase, SawCase, TreeCase, nest_cases, part_cases, run_nest, run_parts, run_saw,
                     run_tree, saw_cases, tree_cases)


@given(st.lists(part_cases(), min_size=1, max_size=4).map(tuple))
def test_the_nest_sees_each_part_from_its_machining_face(cases: tuple[PartCase, ...]):
    assert run_parts(cases) == []


@given(tree_cases())
def test_simplifying_a_saw_plan_keeps_every_blank_and_the_sheet_covered(case: TreeCase):
    assert run_tree(case) == []


#: The profile's number of examples (`tests/conftest.py`).
EXAMPLES = settings().max_examples


@settings(max_examples=max(5, EXAMPLES // 4))
@given(saw_cases())
def test_a_saw_plan_saws_every_blank_it_can_once(case: SawCase):
    assert run_saw(case) == []


@settings(max_examples=max(4, EXAMPLES // 6))
@given(nest_cases())
def test_a_nest_is_what_it_must_be_for_any_parts_and_workshop(case: NestCase):
    assert run_nest(case) == []
