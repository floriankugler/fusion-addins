from __future__ import annotations

from typing import Any, get_args


class LangError(Exception):
    """An error in a build, naming the part it concerns.

    `path` is the dotted path of the part or scope (`kitchen.drawer2.left`)
    or None for errors outside any part. `where` is the build file's line
    of what the error is about (`examples/van.py:45`, `lang.core.where`),
    which the message starts with, or "": a board found wrong when it
    resolves, which may be long after the line that made it, names that
    line (`locate`)."""

    def __init__(self, message: str, path: str | None = None, where: str = ""):
        self.path = path
        self.message = message
        self.where = where
        super().__init__(self._text())

    def _text(self) -> str:
        text = f"{self.path}: {self.message}" if self.path else self.message
        return f"{self.where}: {text}" if self.where else text

    def locate(self, where: str) -> None:
        """Names `where` as the line the error is about, unless it names
        one already (the innermost board found wrong wins). It changes the
        error itself, so a bare `raise` after it keeps its traceback."""
        if where and not self.where:
            self.where = where
            self.args = (self._text(),)


def one_of[T](value: T, choices: Any, what: str, path: str | None = None) -> T:
    """`value` when it is one of the values of `choices`, a Literal type
    such as `ExtentName`; else a LangError naming them. The type checker
    catches a wrong value in the editor, but a build also runs without it
    (the preview rebuilds on every save), so the API checks again."""
    allowed = get_args(choices)
    if value not in allowed:
        names = [repr(a) for a in allowed]
        expected = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " or " + names[-1]
        raise LangError(f"{what}: expected {expected}, not {value!r}.", path)
    return value
