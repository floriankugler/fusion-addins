"""Fuzzing the snapshot's Fusion-free half and its reading (`snapshots`):
`chain()` gives back the chain a sketch's curves form however they come,
and refuses several chains, branches and curves around nothing; the
writer's snapshot does not depend on the order the items come in, `dumps`
and `content_hash` are deterministic, and `master()` reads back what was
written."""
from hypothesis import given

from snapshots import ChainCase, MasterCase, chain_cases, chain_problems, master_cases, snapshot_problems


@given(chain_cases())
def test_chain_joins_a_sketchs_curves_however_they_come(case: ChainCase):
    assert chain_problems(case) == []


@given(master_cases())
def test_a_snapshot_reads_back_as_written_whatever_the_order(case: MasterCase):
    assert snapshot_problems(case) == []
