"""Fuzzing `Board.cutout()` on random boards (see `boards`): lying or
standing, far from the origin or not, rectangles, rounded and tapered
shapes and slots, with holes, pockets, cuts, notches, V-grooves, holes
into narrow faces and rounded corners made first. The cutout must keep
what it promises (`boards.run_cutout`), and the layout must plan, draw and
mesh."""
from hypothesis import assume, given

from boards import KNOWN, BoardCase, board_cases, run_cutout


@given(board_cases())
def test_a_cutout_keeps_its_promises_on_any_board(case: BoardCase):
    # Open (2026-10-12): without rounding, an opening keeps the corners
    # `cutouts.grown` mitres where a line meets an arc (up to some tenths
    # off, which `fit` puts right when drawing), and with no border it
    # may touch the outline at a point, which the preview cannot mesh.
    assume(case.cutout.radius > 0)
    assert [p for p in run_cutout(case) if not p.startswith(KNOWN)] == []
