"""Where the build file wrote something: the line of the build file that led
to a call, found as the innermost frame of the stack outside the language.

The language is `lang/` and the shared `lib/`, and Python with its packages
(the venv and the installation behind it) and code without a file
(`<frozen runpy>`, `<string>`) count with it; everything else is the
build's own: build files, the helpers they import, tests. So a board the
standard library's `carcass()` makes points at the build file's
`carcass(...)` line, the operations a `join` makes in both boards share the
join's line, and the boards a loop makes share the loop body's line.

A file is shown relative to the working directory when it lies in it
(`examples/van.py`), else by its whole path. The walk costs a few frames
per call, each a dictionary lookup: the parts, modules, hardware and
operations of a build record their line (`where`), the settings' reads
and uses theirs with the code (`build_line`).
"""
from __future__ import annotations

import linecache
import sys
from functools import cache
from pathlib import Path
from types import FrameType

_LANG = Path(__file__).resolve().parents[1]
#: The language and the shared lib it reads.
LANGUAGE = (_LANG, _LANG.parent / "lib")
#: Code that is not the build's own: the language, Python and its packages.
_NOT_BUILD = (*LANGUAGE, Path(sys.prefix).resolve(), Path(sys.base_prefix).resolve())


def where() -> str:
    """The build file's line that led here, `examples/van.py:45`, without
    its code; "" when no frame outside the language led here."""
    frame = _build_frame(sys._getframe(1))    # pyright: ignore[reportPrivateUsage] - a cheap walk, run per part and operation
    return f"{shown(frame.f_code.co_filename)}:{frame.f_lineno}" if frame is not None else ""


def build_line() -> str:
    """The build file's line that led here with its code, `path:line:
    code`; "?" when no frame outside the language led here."""
    frame = _build_frame(sys._getframe(1))    # pyright: ignore[reportPrivateUsage] - a cheap walk, since every read names its line
    if frame is None:
        return "?"
    name = frame.f_code.co_filename
    code = linecache.getline(name, frame.f_lineno).strip()
    return f"{shown(name)}:{frame.f_lineno}: {code}" if code else f"{shown(name)}:{frame.f_lineno}"


def _build_frame(frame: FrameType | None) -> FrameType | None:
    while frame is not None and not is_build_code(frame.f_code.co_filename):
        frame = frame.f_back
    return frame


@cache
def is_build_code(filename: str) -> bool:
    """Whether a frame's file is the build's own, not the language's or
    Python's."""
    if filename.startswith("<"):        # <frozen runpy>, <string>
        return False
    path = Path(filename).resolve()
    return not any(path.is_relative_to(d) for d in _NOT_BUILD)


@cache
def in_language(filename: str) -> bool:
    """Whether a file is the language's own (`lang/`, `lib/`)."""
    if filename.startswith("<"):
        return False
    path = Path(filename).resolve()
    return any(path.is_relative_to(d) for d in LANGUAGE)


@cache
def shown(filename: str) -> str:
    """A file as lines name it: relative to the working directory when it
    lies in it, else its whole path."""
    path = Path(filename).resolve()
    cwd = Path.cwd()
    return str(path.relative_to(cwd)) if path.is_relative_to(cwd) else str(path)

