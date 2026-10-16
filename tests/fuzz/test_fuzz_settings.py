"""Fuzzing the settings (`settings`): random chains of modules, lazy
modules, scopes, boards and named operations, each using keys at a moment
of its own, give at every node the value of the nearest use, the default
or the error of a key without one, and the layout carries what each part's
chain uses; random orders of uses and reads follow set once and freezing,
and a refused use changes nothing."""
from hypothesis import given

from settings import ChainCase, OrderCase, chain_cases, chain_problems, order_cases, order_problems


@given(chain_cases())
def test_every_node_reads_the_nearest_use(case: ChainCase):
    assert chain_problems(case) == []


@given(order_cases())
def test_uses_and_reads_in_any_order_keep_set_once_and_freezing(case: OrderCase):
    assert order_problems(case) == []
