"""Fuzzing `-` and `+` on shapes [decided by Florian, 2026-10-15,
syntax.md item 13]: for random shapes as the language makes them
(`fuzzing.recipes`), each raw or in one of three planes, `a - b` is
`a.difference(b)` and `a + b` is `a.union(b)` exactly, chained too: the
same coordinates, the same plane, or the same refusal."""
from collections.abc import Callable

from hypothesis import given
from hypothesis import strategies as st

from fuzzing import Recipe, recipes
from lang import LangError
from lang.core.shapes import Axes, Shape

PLANES: list[Axes] = [None, ("x", "z"), ("y", "z"), ("x", "y")]


def _made(how: Callable[[], Shape]) -> tuple[str, object]:
    """The shape's coordinates (as WKB) and plane, or the refusal."""
    try:
        s = how()
    except LangError as e:
        return ("refused", str(e))
    return ("made", (s.geometry.wkb, s.axes))


@given(st.lists(st.tuples(recipes(), st.sampled_from(PLANES)), min_size=3, max_size=3))
def test_minus_and_plus_are_difference_and_union_exactly(drawn: list[tuple[Recipe, Axes]]):
    a, b, c = (Shape(recipe.geometry(), plane) for recipe, plane in drawn)
    assert _made(lambda: a - b) == _made(lambda: a.difference(b))
    assert _made(lambda: a + b) == _made(lambda: a.union(b))
    assert _made(lambda: a - b + c) == _made(lambda: a.difference(b).union(c))
    assert _made(lambda: a + b - c) == _made(lambda: a.union(b).difference(c))
