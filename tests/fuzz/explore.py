"""Runs a fuzz check over many random examples without stopping at the
first failure, and prints the kinds of problems found, each with its
smallest example: a survey to triage before Hypothesis shrinks one kind at
a time.

    .venv/bin/python tests/fuzz/explore.py arcs 2000

The checks are the `CHECKS` below: a strategy and a function from an
example to its problems (strings; the words before the first digit or
quote name the kind). An exception other than LangError is a problem of
its own kind."""
from __future__ import annotations

import math
import re
import sys
import time
import traceback
import warnings
from collections.abc import Callable
from pathlib import Path
from typing import Any

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[2])]

from hypothesis import strategies as st  # noqa: E402
from hypothesis.errors import NonInteractiveExampleWarning  # noqa: E402

import boards  # noqa: E402
import checks  # noqa: E402
import contours  # noqa: E402
import corners  # noqa: E402
import fuzzing  # noqa: E402
import hardware  # noqa: E402
import joints  # noqa: E402
from lang.core.errors import LangError  # noqa: E402

Check = tuple[st.SearchStrategy[Any], Callable[[Any], list[str]]]


def _fillets(example: tuple[fuzzing.Lines, float]) -> list[str]:
    from lang.core import cutouts
    shape, r = example
    poly = shape.polygon()
    if poly is None:
        return []
    got, want = cutouts.filleted(poly, r), fuzzing.reference_fillet(poly, r)
    if want is None:
        return [] if got is None or got.is_valid else ["an invalid fillet where none fits"]
    if got is None:
        return ["refused, though every arc fits"]
    problems: list[str] = []
    off = got.hausdorff_distance(want)
    if off > r * (1 - math.cos(math.radians(0.8))) + 1e-6:     # as test_fuzz_fillets: an arc's end step
        problems.append(f"the fillet lies {off:.3g} off the reference")
    if cutouts.corner_points(got):
        problems.append(f"corners left: {len(cutouts.corner_points(got))}")
    return problems


def _chamfers(example: tuple[fuzzing.Lines, float]) -> list[str]:
    from lang.core import cutouts
    shape, size = example
    poly = shape.polygon()
    if poly is None:
        return []
    corners = [p for p, _ in cutouts.corner_points(poly)]
    got, want = cutouts.chamfered(poly, size, corners), fuzzing.reference_chamfer(poly, size)
    if want is None:
        return [] if got is None or got.is_valid else ["an invalid chamfer where none fits"]
    if got is None:
        return ["refused, though every cut fits"]
    off = got.hausdorff_distance(want)
    return [f"the chamfer lies {off:.3g} off the reference"] if off > 1e-6 else []


_radii = st.one_of(st.sampled_from([1.0, 3.0, 6.0, 8.0, 20.0]), fuzzing.floats(0.1, 40))
CHECKS: dict[str, Check] = {
    "arcs": (fuzzing.recipes(), fuzzing.recipe_problems),
    "fillets": (st.tuples(fuzzing.line_polygons(), _radii), _fillets),
    "chamfers": (st.tuples(fuzzing.line_polygons(), _radii), _chamfers),
    "offsets": (fuzzing.recipes(), fuzzing.offset_problems),
    "cutouts": (boards.board_cases(), boards.run_cutout),
    "joints": (joints.pair_cases(), joints.run_pair),
    "box_joints": (joints.corner_cases(), joints.run_corner),
    "half_laps": (joints.cross_cases(), joints.run_cross),
    "grooves": (joints.frame_cases(), joints.run_frame),
    "doors": (hardware.door_cases(), hardware.run_case),
    "panels": (hardware.panel_cases(), hardware.run_case),
    "hatches": (hardware.hatch_cases(), hardware.run_case),
    "catches": (hardware.catch_cases(), hardware.run_case),
    "drawers": (hardware.drawer_cases(), hardware.run_case),
    "corners": (corners.corner_op_cases(), corners.run_case),
    "dogbones": (corners.corner_op_cases().filter(lambda c: c.op == "dogbones"), corners.run_case),
    "board_chamfers": (corners.corner_op_cases().filter(lambda c: c.op != "dogbones"), corners.run_case),
    "checks": (checks.scenes(), checks.run_case),
    "contours": (contours.contour_cases(), contours.run_case),
}


def kind_of(problem: str) -> str:
    return re.split(r"[-0-9(\['\"]", problem, maxsplit=1)[0].strip()


def main() -> None:
    name, count = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 500
    strategy, check = CHECKS[name]
    if len(sys.argv) > 3:
        extra = sys.argv[3]
        check = getattr(fuzzing, extra) if hasattr(fuzzing, extra) else check
    found: dict[str, tuple[int, str, str]] = {}
    counts: dict[str, int] = {}
    start = time.time()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", NonInteractiveExampleWarning)
        for _ in range(count):
            example = strategy.example()
            with fuzzing.fresh():
                try:
                    problems = check(example)
                except LangError:
                    problems = []
                except Exception as e:
                    frame = traceback.extract_tb(e.__traceback__)[-1]
                    problems = [f"{type(e).__name__} at {Path(frame.filename).name}:{frame.lineno}: {e}"]
            for p in problems:
                kind = kind_of(p) if not p[0].isupper() or " at " not in p else p.split(":")[0] + ":" + \
                    p.split(":")[1]
                counts[kind] = counts.get(kind, 0) + 1
                text = repr(example)
                if kind not in found or len(text) < found[kind][0]:
                    found[kind] = (len(text), text, p)
    print(f"{count} examples in {time.time() - start:.1f} s")
    for kind, (_, text, p) in sorted(found.items(), key=lambda kv: -counts[kv[0]]):
        print(f"\n[{counts[kind]}] {kind}\n  {p}\n  {text}")


if __name__ == "__main__":
    main()
