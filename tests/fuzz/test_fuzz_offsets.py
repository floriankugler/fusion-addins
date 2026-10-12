"""Fuzzing `cutouts.grown`, the offsets the cutouts keep material around
features with and inset the border by: grown it holds the shape, shrunk it
lies in it, and its boundary keeps the offset's distance from the shape
(`fuzzing.offset_problems`)."""
from hypothesis import given

from fuzzing import Recipe, offset_problems, recipes


@given(recipes())
def test_an_offset_keeps_its_distance(recipe: Recipe):
    assert offset_problems(recipe) == []
