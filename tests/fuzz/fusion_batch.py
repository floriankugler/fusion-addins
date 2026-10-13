"""The Fusion batch check, its half outside Fusion (`fusion_check.py` runs
inside): fuzz boards, or the examples, compiled in Fusion and compared with
the preview. A case that passes every Fusion-free check can still fail in
Fusion (a profile it cannot make, a chamfer it cannot cut, a body that
comes out in two), and only this finds those.

    .venv/bin/python tests/fuzz/fusion_batch.py build out/fuzz/batch --count 40 --seed 1
    .venv/bin/python tests/fuzz/fusion_batch.py rebuild out/fuzz/batch.cases.txt out/fuzz/batch2
    .venv/bin/python tests/fuzz/fusion_batch.py examples out/fuzz/examples
    .venv/bin/python tests/fuzz/fusion_batch.py joints out/fuzz/joints --count 40 --seed 1
    .venv/bin/python tests/fuzz/fusion_batch.py hardware out/fuzz/hardware --count 36 --seed 1
    .venv/bin/python tests/fuzz/fusion_batch.py corners out/fuzz/corners --count 40 --seed 1

`build` draws boards until `count` pass every check of
`boards.run_cutout`, builds them into one layout (modules `m0`, `m1`...)
and writes `<out>.json`, the preview's volume per part
(`<out>.volumes.json`) and the cases (`<out>.cases.txt`, one `m<i>: <case>`
a line, for `rebuild` with today's code or for building one again by
hand). `examples` writes every build file in `examples/` the same way, as
`<out>/<example>/layout`; `joints` draws joints that pass every check
of `joints.check` (pairs, corners, crossings, frames) the same way,
`hardware` cabinets with hardware mounted that pass every check of
`hardware.run_case` (hinges, latches, sliding brackets, hatch hinges, ball
catches, slides), `corners` boards with dog bones and chamfers that
pass every check of `corners.run_case`, and `rebuild` builds any kind of
cases file again. Then, in Fusion, `fusion_check.check([...])`
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
from hypothesis import strategies as st  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402

import boards  # noqa: E402
import corners  # noqa: E402
import hardware  # noqa: E402
import joints  # noqa: E402
from boards import BoardCase, CutoutCall, Feature  # noqa: E402
from corners import CornerOpCase  # noqa: E402
from hardware import CatchCase, DoorCase, DrawerCase, HatchCase, PanelCase  # noqa: E402
from joints import CornerCase, CrossCase, FrameCase, JointCase, JointSpec, PairCase  # noqa: E402
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


def draw_joint_cases(count: int, at: int) -> list[JointCase]:
    """About `count` joints (rounded up to as many of each kind) that pass
    every check of `joints.check` and are joined, as many of each kind (every joint between boards that
    meet edge-on, tenons with a joint in their gaps, box joints, half laps,
    grooves in a frame), the same ones for the same `at`."""
    kinds: list[st.SearchStrategy[JointCase]] = [
        *(joints.pair_cases().filter(lambda c, k=k: c.joint.kind == k and c.after is None)
          for k in ("domino", "clamex", "cabineo", "screws", "tenons", "groove")),
        joints.pair_cases().filter(lambda c: c.after is not None),
        joints.corner_cases(), joints.cross_cases(), joints.frame_cases()]
    quota = -(-count // len(kinds))
    found: list[JointCase] = []
    for i, kind in enumerate(kinds):
        mine: list[JointCase] = []

        @settings(max_examples=quota * 60, database=None, deadline=None, phases=[Phase.generate],
                  suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
        @seed(at * 100 + i)
        @given(kind)
        def collect(case: JointCase) -> None:
            if len(mine) >= quota or case in mine or joints.check(case):
                return
            with fresh():
                try:
                    joints.apply(case, "m")
                except (LangError, joints.Refused):
                    return          # refused: nothing to compile
            mine.append(case)

        collect()
        found += mine
    return found


def draw_hardware_cases(count: int, at: int) -> list[hardware.Case]:
    """About `count` cabinets with hardware (as many of each kind: hinges,
    latches, sliding brackets, hatch hinges, ball catches, slides) whose
    mount is accepted and keeps every promise, the same ones for the same
    `at`."""
    kinds: list[st.SearchStrategy[hardware.Case]] = [
        hardware.door_cases().filter(lambda c: c.kind == "hinge"), hardware.door_cases().filter(lambda c: c.kind == "latch"),
        hardware.panel_cases(), hardware.hatch_cases(), hardware.catch_cases(), hardware.drawer_cases()]
    quota = -(-count // len(kinds))
    found: list[hardware.Case] = []
    for i, kind in enumerate(kinds):
        mine: list[hardware.Case] = []

        @settings(max_examples=quota * 60, database=None, deadline=None, phases=[Phase.generate],
                  suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
        @seed(at * 100 + i)
        @given(kind)
        def collect(case: hardware.Case) -> None:
            if len(mine) < quota and case not in mine and hardware.accepted(case):
                mine.append(case)

        collect()
        found += mine
    return found


def draw_corner_cases(count: int, at: int) -> list[CornerOpCase]:
    """About `count` boards with dog bones, corner chamfers or rim
    chamfers (as many of each) that are accepted and keep every promise,
    the same ones for the same `at`."""
    kinds: list[st.SearchStrategy[CornerOpCase]] = [
        corners.corner_op_cases().filter(lambda c, k=k: c.op == k) for k in ("dogbones", "corner chamfer", "rim chamfer")]
    quota = -(-count // len(kinds))
    found: list[CornerOpCase] = []
    for i, kind in enumerate(kinds):
        mine: list[CornerOpCase] = []

        @settings(max_examples=quota * 60, database=None, deadline=None, phases=[Phase.generate],
                  suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
        @seed(at * 100 + i)
        @given(kind)
        def collect(case: CornerOpCase) -> None:
            if len(mine) < quota and case not in mine and corners.accepted(case):
                mine.append(case)

        collect()
        found += mine
    return found


Case = BoardCase | JointCase | hardware.Case | CornerOpCase


def build_cases(cases: Sequence[Case]) -> Layout:
    """The cases as one layout, module `m<i>` for case i."""
    registry.reset()
    for i, case in enumerate(cases):
        if isinstance(case, BoardCase):
            problems = boards._run_cutout(case, f"m{i}", pipeline=False)  # pyright: ignore[reportPrivateUsage]
            if problems:
                raise AssertionError(f"m{i} no longer passes: {problems[0]}")
        elif isinstance(case, (DoorCase, PanelCase, HatchCase, CatchCase, DrawerCase)):
            hardware.apply(case, f"m{i}")
        elif isinstance(case, CornerOpCase):
            corners.apply(case, f"m{i}")
        else:
            joints.apply(case, f"m{i}")
    layout = build_layout()
    registry.reset()
    return layout


def write(out: Path, layout: Layout, cases: Sequence[Case] | None = None) -> None:
    """`<out>.json`, `<out>.volumes.json` and, given cases, `<out>.cases.txt`."""
    out.parent.mkdir(parents=True, exist_ok=True)
    Path(f"{out}.json").write_text(json.dumps(layout))
    Path(f"{out}.volumes.json").write_text(json.dumps(preview_volumes(layout), indent=1))
    if cases is not None:
        Path(f"{out}.cases.txt").write_text("".join(f"m{i}: {c!r}\n" for i, c in enumerate(cases)))


def preview_volumes(layout: Layout) -> dict[str, float]:
    return {p["path"]: float(mesh_part(p, layout["frame"]).volume) for m in layout["modules"] for p in m["parts"]}


def read_cases(path: Path) -> list[Case]:
    names = {"BoardCase": BoardCase, "CutoutCall": CutoutCall, "Feature": Feature, "PairCase": PairCase,
             "JointSpec": JointSpec, "CornerCase": CornerCase, "CrossCase": CrossCase, "FrameCase": FrameCase,
             "DoorCase": DoorCase, "PanelCase": PanelCase, "HatchCase": HatchCase, "CatchCase": CatchCase,
             "DrawerCase": DrawerCase, "CornerOpCase": CornerOpCase}
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
        elif inner["kind"] == "pocket":
            polygons, drawn = _areas(inner["shape"])
            if op["kind"] == "edge":            # (in a narrow face: as deep as given, or through)
                extra -= (drawn - polygons) * (inner["depth"] or 0.0)
            else:
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
    joined = commands.add_parser("joints", help="draw passing joints into one layout")
    joined.add_argument("out", type=Path)
    joined.add_argument("--count", type=int, default=40)
    joined.add_argument("--seed", type=int, default=0)
    mounted = commands.add_parser("hardware", help="draw cabinets with hardware into one layout")
    mounted.add_argument("out", type=Path)
    mounted.add_argument("--count", type=int, default=36)
    mounted.add_argument("--seed", type=int, default=0)
    cornered = commands.add_parser("corners", help="draw boards with dog bones and chamfers into one layout")
    cornered.add_argument("out", type=Path)
    cornered.add_argument("--count", type=int, default=40)
    cornered.add_argument("--seed", type=int, default=0)
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
    elif args.command == "joints":
        with fresh():
            found = draw_joint_cases(args.count, args.seed)
        write(args.out, build_cases(found), found)
        print(f"{len(found)} joints -> {args.out}.json")
    elif args.command == "hardware":
        with fresh():
            mounts = draw_hardware_cases(args.count, args.seed)
        write(args.out, build_cases(mounts), mounts)
        print(f"{len(mounts)} cabinets -> {args.out}.json")
    elif args.command == "corners":
        with fresh():
            boards_ = draw_corner_cases(args.count, args.seed)
        write(args.out, build_cases(boards_), boards_)
        print(f"{len(boards_)} boards -> {args.out}.json")
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
