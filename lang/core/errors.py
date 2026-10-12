from typing import Any, get_args


class LangError(Exception):
    """An error in a build, naming the part it concerns.

    `path` is the dotted path of the part or scope (`kitchen.drawer2.left`)
    or None for errors outside any part."""

    def __init__(self, message: str, path: str | None = None):
        self.path = path
        self.message = message
        super().__init__(f"{path}: {message}" if path else message)


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
