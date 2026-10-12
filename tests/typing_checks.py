"""What the type checker must report in a build file.

Pyright checks this file with the rest (`.venv/bin/pyright`); pytest does
not run it. Each line marked `# type: ignore` must have an error: if a
change to the language made it pass, pyright reports the comment as
unnecessary, and the check fails.
"""
# pyright: reportUnnecessaryTypeIgnoreComment=true
from lang import *

ply15 = material("birch", t=15)


def operations() -> None:
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        side = board("side", ply15).on(m.left)
        _ = side.toekick.top                                                 # a named operation: fine
        side.pocket(rect(depth=50, height=50), at=side.inner.center)          # type: ignore  # no depth
        side.hole(5, side.inner.center)                                       # type: ignore  # no depth
        side.pocket(rect(depth=50, height=50), side.inner.center, 5)          # type: ignore  # depth by position
        side.hoel(d=5, at=side.inner.center, depth=10)                        # type: ignore  # a misspelt method
        side.fillet(side.front.bottom, r=5)                                   # type: ignore  # radius=, not r=


def shapes() -> None:
    rect(depth=50, height=50).clip(top=10, back=10)
    rect(depth=50, height=50).clip("top.back", top=10, back=10)               # type: ignore  # no strings
    rect(depth=50, height=50).clip(top=10, bak=10)                            # type: ignore  # a misspelt edge
