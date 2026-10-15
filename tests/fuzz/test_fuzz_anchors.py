"""Fuzzing `anchor.center(pos)` on random boards (see `boards`): a cut,
pocket or hole centred on a position along one axis of a big or narrow
face, named by an edge or the face's middle along the other, the position
given as a `Pos`, a box side, a face moved or a master's plane. The
shape's bounds must have their middle on the position and their side on
the edge (`boards.run_center`) [decided by Florian, 2026-10-15, syntax.md
item 6]."""
from hypothesis import given

from boards import CenterCase, center_cases, run_center


@given(center_cases())
def test_a_shape_centred_on_a_position_has_its_middle_there(case: CenterCase):
    assert run_center(case) == []
