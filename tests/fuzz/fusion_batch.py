"""The Fusion batch check, its half outside Fusion (`fusion_check.py` runs
inside): fuzz boards, or the examples, compiled in Fusion and compared with
the preview. A case that passes every Fusion-free check can still fail in
Fusion (a profile it cannot make, a chamfer it cannot cut, a body that
comes out in two), and only this finds those.

    .venv/bin/python tests/fuzz/fusion_batch.py build out/fuzz/batch --count 40 --seed 1
    .venv/bin/python tests/fuzz/fusion_batch.py rebuild out/fuzz/batch.cases.txt out/fuzz/batch2
    .venv/bin/python tests/fuzz/fusion_batch.py examples out/fuzz/examples

`build` draws boards until `count` pass every check of
`boards.run_cutout`, builds them into one layout (modules `m0`, `m1`...)
and writes `<out>.json`, the preview's volume per part
(`<out>.volumes.json`) and the cases (`<out>.cases.txt`, one `m<i>: <case>`
a line, for `rebuild` with today's code or for building one again by
hand). `examples` writes every build file in `examples/` the same way, as
`<out>/<example>/layout`. Then, in Fusion, `fusion_check.check([...])`
with those paths (without `.json`), and back here

    .venv/bin/python tests/fuzz/fusion_batch.py explain out/fuzz/batch [more paths]

lists every body that differs from the preview: how much, how much of
that the preview's polygons explain (`tessellation`), and Fusion's
problems for that part. What the polygons do not explain is a finding.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(Path(__file__).resolve().parent), str(REPO)]

from hypothesis import HealthCheck, Phase, given, seed, settings  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402

import boards  # noqa: E402
from boards import BoardCase, CutoutCall, Feature  # noqa: E402
from fuzzing import fresh, sample  # noqa: E402
from lang.core.errors import LangError  # noqa: E402
from lang.build import run_build  # noqa: E402
from lang.core.layout import build_layout  # noqa: E402
from lang.core.layout_types import Layout, PartLayout  # noqa: E402
from lang.core.scope import registry  # noqa: E402
from lang.emit.arcs import fit  # noqa: E402
from lang.emit.plan import pieces  # noqa: E402
from lang.preview.__main__ import scan  # noqa: E402
from lang.preview.mesh import _HOLE_SECTIONS, mesh_part  # noqa: E402  # pyright: ignore[reportPrivateUsage]

#: The share of a body's volume by which Fusion and the preview may differ
#: once the polygons' part is taken out (as `fusion_check.THRESHOLD`).
THRESHOLD = 3e-4


# -- building ---------------------------------------------------------------------------------------

def draw_cases(count: int, at: int) -> list[BoardCase]:
    """`count` fuzz boards that pass every Fusion-free check, the same
    ones for the same `at` (Hypothesis's seed)."""
    found: list[BoardCase] = []

    @settings(max_examples=count * 50, database=None, deadline=None, phases=[Phase.generate],
              suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
    @seed(at)
    @given(boards.board_cases())
    def collect(case: BoardCase) -> None:
        if len(found) >= count or case in found or boards.run_cutout(case):      # (Hypothesis repeats some)
            return
        with fresh():
            try:                        # (run_cutout passes a board it could not place)
                boards._run_cutout(case, pipeline=False)  # pyright: ignore[reportPrivateUsage]
            except LangError:
                return
        found.append(case)

    collect()
    return found


def build_cases(cases: Sequence[BoardCase]) -> Layout:
    """The cases as one layout, module `m<i>` for case i."""
    registry.reset()
    for i, case in enumerate(cases):
        problems = boards._run_cutout(case, f"m{i}", pipeline=False)  # pyright: ignore[reportPrivateUsage]
        if problems:
            raise AssertionError(f"m{i} no longer passes: {problems[0]}")
    layout = build_layout()
    registry.reset()
    return layout


def write(out: Path, layout: Layout, cases: Sequence[BoardCase] | None = None) -> None:
    """`<out>.json`, `<out>.volumes.json` and, given cases, `<out>.cases.txt`."""
    out.parent.mkdir(parents=True, exist_ok=True)
    Path(f"{out}.json").write_text(json.dumps(layout))
    Path(f"{out}.volumes.json").write_text(json.dumps(preview_volumes(layout), indent=1))
    if cases is not None:
        Path(f"{out}.cases.txt").write_text("".join(f"m{i}: {c!r}\n" for i, c in enumerate(cases)))


def preview_volumes(layout: Layout) -> dict[str, float]:
    return {p["path"]: float(mesh_part(p, layout["frame"]).volume) for m in layout["modules"] for p in m["parts"]}


def read_cases(path: Path) -> list[BoardCase]:
    names = {"BoardCase": BoardCase, "CutoutCall": CutoutCall, "Feature": Feature}
    return [eval(line.split(": ", 1)[1], names) for line in path.read_text().splitlines() if line.strip()]


def build_examples(out_dir: Path, folder: Path = REPO / "examples") -> list[Path]:
    """Every build file in `folder`, built as `lang.build` builds it; the
    paths to give `fusion_check.check`."""
    paths: list[Path] = []
    files, _ = scan(folder)
    for file in files:
        layout = run_build(file, out_dir / file.stem, scene=False)       # writes layout.json
        path = out_dir / file.stem / "layout"
        Path(f"{path}.volumes.json").write_text(json.dumps(preview_volumes(layout), indent=1))
        paths.append(path)
    registry.reset()
    return paths


# -- explaining ---------------------------------------------------------------------------------------

def _areas(rings: Any) -> tuple[float, float]:
    """A layout shape's area as its polygons and as the lines and arcs they
    stand for (`fit`, drawn finely), holes taken away."""
    polygons = drawn = 0.0
    for piece in pieces(rings):
        for k, ring in enumerate(piece):
            sign = 1.0 if k == 0 else -1.0
            polygons += sign * abs(Polygon(ring).area)
            drawn += sign * abs(Polygon(sample(fit(ring), math.radians(0.05))).area)
    return polygons, drawn


def tessellation(part: PartLayout) -> float:
    """How much more material (mm3) Fusion's body should have than the
    preview's mesh from the polygons alone: Fusion draws true arcs, the
    preview the polygons inside them, so an outline's convex arcs hold more
    in Fusion, and its holes and pockets take more (a hole is a 24-sided
    prism in the preview). A hole partly off the board takes less than
    this assumes."""
    t = float(part["thickness"])
    polygons, drawn = _areas(part["outline"])
    extra = (drawn - polygons) * t
    gon = _HOLE_SECTIONS / (2 * math.pi) * math.sin(2 * math.pi / _HOLE_SECTIONS)    # n-gon area / circle area
    for op in part["ops"]:
        inner: Any = op["op"] if op["kind"] == "edge" else op
        if inner["kind"] == "hole":
            if op["kind"] == "edge":
                depth = 0.0 if inner["through"] else inner["depth"]         # (through: as long as the board)
            else:
                depth = t if inner["through"] or inner["depth"] is None else min(inner["depth"], t)
            extra -= math.pi * (inner["d"] / 2) ** 2 * (1 - gon) * depth
        elif inner["kind"] == "pocket" and op["kind"] != "edge":
            polygons, drawn = _areas(inner["shape"])
            extra -= (drawn - polygons) * (t if inner["depth"] is None else min(inner["depth"], t))
    return extra


def explain(path: Path, threshold: float = THRESHOLD) -> list[str]:
    """The bodies of `<path>` that differ from the preview (after
    `fusion_check.check` wrote `<path>.fusion.json`), each with how much of
    the difference the polygons explain."""
    layout: Layout = json.loads(Path(f"{path}.json").read_text())
    preview: dict[str, float] = json.loads(Path(f"{path}.volumes.json").read_text())
    fusion = json.loads(Path(f"{path}.fusion.json").read_text())
    parts = {p["path"]: p for m in layout["modules"] for p in m["parts"]}
    lines: list[str] = []
    for name, want in preview.items():
        problems = [p for p in fusion["problems"] if p.startswith(name + ":")]
        got = fusion["volumes"].get(name)
        if got is None:
            lines.append(f"{name}: not drawn" + "".join(f"\n   {p[:200]}" for p in problems))
            continue
        diff = got["volume"] - want
        expected = tessellation(parts[name])
        rest = diff - expected
        if got["solids"] == 1 and abs(diff) <= threshold * want and not problems:
            continue
        verdict = ("the polygons" if got["solids"] == 1 and abs(rest) <= threshold * want
                   else f"UNEXPLAINED {rest:+.1f} mm3 ({rest / want * 100:+.4f} %)")
        lines.append(f"{name}: {got['solids']} solid(s), Fusion {diff:+.1f} mm3 ({diff / want * 100:+.4f} %), "
                     f"the polygons {expected:+.1f}: {verdict}" + "".join(f"\n   {p[:200]}" for p in problems))
    return lines


# -- the command line ---------------------------------------------------------------------------------

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0] if __doc__ else None)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build", help="draw passing fuzz boards into one layout")
    build.add_argument("out", type=Path)
    build.add_argument("--count", type=int, default=40)
    build.add_argument("--seed", type=int, default=0)
    rebuild = commands.add_parser("rebuild", help="build a batch's cases again with today's code")
    rebuild.add_argument("cases", type=Path)
    rebuild.add_argument("out", type=Path)
    examples = commands.add_parser("examples", help="build every example")
    examples.add_argument("out_dir", type=Path)
    explain_ = commands.add_parser("explain", help="list the bodies Fusion made differently")
    explain_.add_argument("paths", type=Path, nargs="+")
    args = parser.parse_args(argv)
    if args.command == "build":
        with fresh():
            cases = draw_cases(args.count, args.seed)
        write(args.out, build_cases(cases), cases)
        print(f"{len(cases)} boards -> {args.out}.json")
    elif args.command == "rebuild":
        cases = read_cases(args.cases)
        write(args.out, build_cases(cases), cases)
        print(f"{len(cases)} boards -> {args.out}.json")
    elif args.command == "examples":
        for path in build_examples(args.out_dir):
            print(path)
    else:
        for path in args.paths:
            lines = explain(path)
            print(f"{path}: {len(lines)} bodies differ" + "".join(f"\n  {line}" for line in lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
