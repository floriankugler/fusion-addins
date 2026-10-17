"""Fuzzing the preview's levels (`lang.preview.levels`) on random boards
(see `boards`): at the normal level, which draws the layout's arcs again
with fewer segments, a board meshes as closed as at the fine one, with as
much material as its curves allow (`boards.run_levels`)."""
from hypothesis import given

from boards import BoardCase, board_cases, run_levels


@given(board_cases())
def test_the_normal_level_meshes_as_the_fine_one_within_its_curves(case: BoardCase):
    assert run_levels(case) == []
