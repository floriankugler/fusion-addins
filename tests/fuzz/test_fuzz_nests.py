"""Fuzzing nests in the build (`nests`): random modules, scopes and
boards with random nest declarations and nesting settings put each part in
the nest the model says, with the values it says or the refusal; random
inventories are read as written, and a run of nests uses and buys only
what the model allows."""
from hypothesis import given, settings

from nests import LedgerCase, NestsCase, ledger_cases, ledger_problems, nests_cases, nests_problems

#: The profile's number of examples (`tests/conftest.py`).
EXAMPLES = settings().max_examples


@given(nests_cases())
def test_each_part_lands_in_the_model_s_nest_with_its_values(case: NestsCase):
    assert nests_problems(case) == []


@settings(max_examples=max(3, EXAMPLES // 8))
@given(ledger_cases())
def test_a_run_of_nests_uses_the_inventory_and_buys_as_the_model_allows(case: LedgerCase):
    assert ledger_problems(case) == []
