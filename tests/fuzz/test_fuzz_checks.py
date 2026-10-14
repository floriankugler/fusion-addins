"""Fuzzing the design checks (`lang.core.checks`) on random scenes of
boards and hardware (`checks.scenes`): `no_interference`, `inside_box`,
`fits_sheet` and `inside(contour)` must tell an overlap from touching as
the truth has it, and say the same wherever the scene lies
(`checks.run_case`)."""
from hypothesis import given

from boards import KNOWN
from checks import Scene, run_case, scenes


@given(scenes())
def test_the_checks_tell_overlapping_from_touching_in_any_scene(scene: Scene):
    assert [p for p in run_case(scene) if not p.startswith(KNOWN)] == []
