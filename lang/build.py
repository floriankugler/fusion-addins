"""Runs a build file and writes its layout, and optionally the preview scene.

    python -m lang.build examples/drawer_cabinet.py --out out/ [--level fine|normal]

A build file is ordinary Python that creates modules with `from lang import *`.
The build runs in a fresh registry and the default world frame every time,
and the modules in the build file's folder that it imported (its own
helpers, other build files) are imported afresh by the next build in the
same process.

An error prints its message and the lines of the build files that led to
it (`examples/van.py:39: bottom.join(...)`), not the frames of runpy, this
module or the language; `--traceback` prints the whole stack instead.
"""
from __future__ import annotations

import argparse
import runpy
import sys
import time
import traceback
from pathlib import Path

from .core.errors import LangError
from .core.layout import build_layout, write_layout
from .core.layout_types import Layout
from .core.scope import registry
from .preview.levels import LEVELS, NORMAL, Level

LANG_DIR = Path(__file__).resolve().parent
_LANGUAGE = (LANG_DIR, LANG_DIR.parent / "lib")     # the language and the shared lib it reads
# Code that is not the build's own: the language, and Python with its
# packages (the venv and the installation behind it).
_NOT_BUILD_CODE = (*_LANGUAGE, Path(sys.prefix).resolve(), Path(sys.base_prefix).resolve())


def layout_of(build_file: str | Path) -> Layout:
    """Runs the build file and returns its layout, writing nothing."""
    run(build_file)
    return build_layout()


def run(build_file: str | Path) -> None:
    """Runs the build file in a fresh registry, and then the bodies of the
    lazy modules nothing needed yet (`registry.run_bodies`); its modules
    are then in `registry`."""
    registry.reset()
    build_path = Path(build_file).resolve()
    before = set(sys.modules)
    sys.path.insert(0, str(build_path.parent))
    try:
        runpy.run_path(str(build_path), run_name="__build__")
        registry.run_bodies()
    finally:
        sys.path.pop(0)
        _forget_modules_in(build_path.parent, before)


def run_build(build_file: str | Path, out_dir: str | Path, scene: bool = True, level: Level = NORMAL) -> Layout:
    """Runs the build file, writes its layout (and with `scene` the
    preview's glTF scene at the level, and the level's name in level.txt)
    into `out_dir`, and returns the layout. Problems meshing the scene are
    printed to stderr as `preview: ...`."""
    run(build_file)
    out_path = Path(out_dir)
    layout = write_layout(out_path / "layout.json")
    if scene:
        from .preview.mesh import write_scene
        for problem in write_scene(layout, out_path / "scene.glb", level):
            print(f"preview: {problem}", file=sys.stderr)
        (out_path / "level.txt").write_text(level.name)
    (out_path / "version.txt").write_text(str(time.time_ns()))
    return layout


def _forget_modules_in(folder: Path, before: set[str]) -> None:
    """Removes the modules from `folder` that the build imported, so the
    next build in this process imports them again, edited or not."""
    for name in set(sys.modules) - before:
        file = getattr(sys.modules[name], "__file__", None)
        if file and Path(file).resolve().is_relative_to(folder):
            del sys.modules[name]


def _is_build_code(filename: str) -> bool:
    if filename.startswith("<"):       # <frozen runpy>, <string>
        return False
    path = Path(filename).resolve()
    return not any(path.is_relative_to(d) for d in _NOT_BUILD_CODE)


def _is_language(filename: str) -> bool:
    path = Path(filename).resolve()
    return any(path.is_relative_to(d) for d in _LANGUAGE)


def _shown(filename: str) -> str:
    path = Path(filename).resolve()
    return str(path.relative_to(Path.cwd())) if path.is_relative_to(Path.cwd()) else str(path)


def describe(error: Exception) -> str:
    """The error as a build file's author needs it: the message, then each
    line of the build files the error passed through, outermost first. A
    Python error raised inside the language (a bug there, not in the build)
    also names the line it was raised at."""
    if isinstance(error, SyntaxError) and error.filename:   # raised compiling a file, no frame of its own
        line = f"  {_shown(error.filename)}:{error.lineno}: {(error.text or '').strip()}".rstrip()
        return f"{type(error).__name__}: {error.msg}\n{line}"
    if isinstance(error, LangError):
        lines = [f"error: {error}"]
    else:   # with Python's own hints ("Did you mean 'name'?")
        lines = "".join(traceback.format_exception_only(error)).rstrip().splitlines()
    frames = traceback.extract_tb(error.__traceback__)
    lines += [f"  {_shown(f.filename)}:{f.lineno}: {f.line or ''}".rstrip()
              for f in frames if _is_build_code(f.filename)]
    build = [i for i, f in enumerate(frames) if _is_build_code(f.filename)]
    inner = [f for f in frames[build[-1] + 1 if build else 0:] if _is_language(f.filename)]
    if not isinstance(error, LangError) and inner:
        lines.append(f"  raised in {_shown(inner[-1].filename)}:{inner[-1].lineno} ({inner[-1].name}); "
                     "--traceback prints the whole stack")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a build file and write its layout.")
    parser.add_argument("build_file")
    parser.add_argument("--out", default="out")
    parser.add_argument("--no-scene", action="store_true", help="write the layout only")
    parser.add_argument("--level", choices=list(LEVELS), default=NORMAL.name,
                        help="how exactly the scene is meshed: fine, the layout's polygons as they are; normal "
                             "(the default), arcs drawn again with chords at most 0.05 mm inside them")
    parser.add_argument("--traceback", action="store_true", help="print an error's whole stack")
    args = parser.parse_args(argv)
    try:
        layout = run_build(args.build_file, args.out, scene=not args.no_scene, level=LEVELS[args.level])
    except Exception as error:
        if args.traceback:
            raise
        print(describe(error), file=sys.stderr)
        return 1
    parts = sum(len(m["parts"]) for m in layout["modules"])
    print(f"{parts} parts in {len(layout['modules'])} module(s) -> {args.out}")
    for problem in layout["problems"]:
        print(f"check: {problem}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
