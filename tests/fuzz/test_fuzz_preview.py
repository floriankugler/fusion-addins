"""Fuzzing the preview's mesher on random boards (see `boards`): at the
normal level (`lang.preview.levels`), which draws the layout's arcs again
with fewer segments, a board meshes as closed as at the fine one, with as
much material as its curves allow (`boards.run_levels`); and the mesh
cache gives back the mesh meshing gives (`boards.run_cache`)."""
from hypothesis import given

from boards import BoardCase, board_cases, run_cache, run_levels


@given(board_cases())
def test_the_normal_level_meshes_as_the_fine_one_within_its_curves(case: BoardCase):
    assert run_levels(case) == []


@given(board_cases())
def test_the_mesh_cache_gives_back_the_mesh_meshing_gives(case: BoardCase):
    assert run_cache(case) == []
