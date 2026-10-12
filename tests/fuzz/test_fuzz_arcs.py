"""Fuzzing `lang.emit.arcs.fit`, which turns every ring the emitter draws
into lines and arcs: on shapes made the way the language makes them, the
curves must join up, lie on the shape's own circles, stay on the polygon
and not cross themselves; and moving, turning or mirroring the ring must
not change what is found."""
import math
from collections.abc import Callable, Sequence

from hypothesis import given
from hypothesis import strategies as st

from fuzzing import Point2, Recipe, recipe_problems, recipes, rings_of, shifts
from lang.emit.arcs import Arc2, Circle2, Curve2, Line2, fit


@given(recipes())
def test_fit_draws_every_ring_joined_up_on_its_circles(recipe: Recipe):
    assert recipe_problems(recipe) == []


Transform = Callable[[Point2], Point2]
Token = tuple[str, Point2, float, Point2, Point2]


def _tokens(curves: Sequence[Curve2], back: Transform, mirrored: bool) -> list[Token]:
    """The curves in the original frame, in the original ring's order."""
    out: list[Token] = []
    for c in curves:
        if isinstance(c, Circle2):
            out.append(("circle", back(c.center), c.radius, (0.0, 0.0), (0.0, 0.0)))
        elif isinstance(c, Arc2):
            a, b = (back(c.b), back(c.a)) if mirrored else (back(c.a), back(c.b))
            out.append(("arc", back(c.center), c.radius, a, b))
        else:
            assert isinstance(c, Line2)
            a, b = (back(c.b), back(c.a)) if mirrored else (back(c.a), back(c.b))
            out.append(("line", (0.0, 0.0), 0.0, a, b))
    return out[::-1] if mirrored else out


def _same(a: Token, b: Token, tol: float) -> bool:
    return a[0] == b[0] and math.dist(a[1], b[1]) <= tol and abs(a[2] - b[2]) <= tol \
        and math.dist(a[3], b[3]) <= tol and math.dist(a[4], b[4]) <= tol


def _rotation_of(a: list[Token], b: list[Token], tol: float) -> bool:
    if len(a) != len(b):
        return False
    return any(all(_same(a[i], b[(i + k) % len(b)], tol) for i in range(len(a))) for k in range(len(b)))


@given(recipes(), st.sampled_from(["move", "turn", "mirror"]), shifts())
def test_fit_finds_the_same_curves_moved_turned_and_mirrored(recipe: Recipe, how: str, shift: Point2):
    dx, dy = shift if how == "move" else (1234.5, -987.25)
    if how == "move":
        def there(p: Point2) -> Point2: return (p[0] + dx, p[1] + dy)
        def back(p: Point2) -> Point2: return (p[0] - dx, p[1] - dy)
    elif how == "turn":
        def there(p: Point2) -> Point2: return (-p[1], p[0])
        def back(p: Point2) -> Point2: return (p[1], -p[0])
    else:
        def there(p: Point2) -> Point2: return (-p[0], p[1])
        def back(p: Point2) -> Point2: return (-p[0], p[1])
    mirrored = how == "mirror"
    for ring in rings_of(recipe.geometry()):
        moved = [there(p) for p in ring]
        if mirrored:
            moved.reverse()
        original = _tokens(fit(ring), lambda p: p, False)
        again = _tokens(fit(moved), back, mirrored)
        assert _rotation_of(original, again, 1e-6), (len(original), len(again))
