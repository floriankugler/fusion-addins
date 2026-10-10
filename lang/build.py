"""Runs a build file and writes its layout, and optionally the preview scene.

    python -m lang.build examples/drawer_cabinet.py --out out/

A build file is ordinary Python that creates modules with `from lang import *`.
The build runs in a fresh registry every time.
"""
from __future__ import annotations

import argparse
import runpy
import sys
import time
from pathlib import Path

from .core.errors import LangError
from .core.layout import write_layout
from .core.scope import registry


def run_build(build_file: str | Path, out_dir: str | Path, scene: bool = True) -> dict:
    registry.reset()
    build_file = Path(build_file).resolve()
    out_dir = Path(out_dir)
    sys.path.insert(0, str(build_file.parent))
    try:
        runpy.run_path(str(build_file), run_name="__build__")
    finally:
        sys.path.pop(0)
    layout = write_layout(out_dir / "layout.json")
    if scene:
        from .preview.mesh import write_scene
        write_scene(layout, out_dir / "scene.glb")
    (out_dir / "version.txt").write_text(str(time.time_ns()))
    return layout


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("build_file")
    parser.add_argument("--out", default="out")
    parser.add_argument("--no-scene", action="store_true", help="write the layout only")
    args = parser.parse_args(argv)
    try:
        layout = run_build(args.build_file, args.out, scene=not args.no_scene)
    except LangError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    parts = sum(len(m["parts"]) for m in layout["modules"])
    print(f"{parts} parts in {len(layout['modules'])} module(s) -> {args.out}")
    for problem in layout["problems"]:
        print(f"check: {problem}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
