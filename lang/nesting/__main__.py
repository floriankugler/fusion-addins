"""Nests the parts of build files (or layout files) for the workshop.

    python -m lang.nesting examples/van.py
    python -m lang.nesting examples/van.py examples/shelf.py --out out/nest
    python -m lang.nesting out/van/layout.json --bed 2000x1000 --sheet 2470x1240 \\
        --sheet "birch 15:1525x1525*2" --offcut "birch 15:1250x600"

The workshop (bed, spacing, saw, stock on hand) comes from `--workshop`,
else from `workshop.toml` beside the first source when there is one; the
options below replace what it says (`--sheet` all its sheets, `--offcut`
all its offcuts). Several sources are nested together; their parts' paths
then start with the source's name (`van:floor.batten0`).

Writes into `--out` (default `out/<name>`, beside the preview's build):
`nest.json` (the nest, `lang/nesting/nest_types.py`), `nest.layout.json` (the
layout nested, for the Fusion emitter) and `nest.svg` (the drawing the
preview shows). Problems are printed and kept in the nest file; a part the
nest cannot take at all is an error, as in the layout step.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
import time
from pathlib import Path

from ..build import describe, layout_of
from ..core.errors import LangError
from ..core.layout_types import Layout
from ..emit.plan import check_version
from .draw import draw_nest
from .nest import Options, nest_layout
from .workshop import Workshop, parse_offcut, parse_sheet, parse_size, read_workshop, with_overrides


def load(source: Path) -> Layout:
    """A build file's layout (run here), or a layout file's."""
    if source.suffix == ".json":
        layout: Layout = json.loads(source.read_text())
        try:
            check_version(layout)
        except ValueError as error:
            raise LangError(f"{source}: {error}") from None
        return layout
    return layout_of(source)


def merged(layouts: list[tuple[str, Layout]]) -> Layout:
    """Several layouts as one, each part's path after its source's name."""
    if len(layouts) == 1:
        return layouts[0][1]
    first = layouts[0][1]
    out: Layout = {"version": first["version"], "units": first["units"], "frame": first["frame"], "modules": [],
                   "problems": [], "snapshots": []}
    for name, layout in layouts:
        if layout["frame"] != first["frame"]:
            raise LangError(f"{name} is written in another world frame than {layouts[0][0]}; nest them apart.")
        for module in copy.deepcopy(layout["modules"]):
            module["path"] = f"{name}:{module['path']}"
            for part in module["parts"]:
                part["path"] = f"{name}:{part['path']}"
            out["modules"].append(module)
        out["problems"] += [f"{name}: {p}" for p in layout["problems"]]
        out["snapshots"] += layout["snapshots"]
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m lang.nesting", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("sources", nargs="+", type=Path, help="build files (.py) or layout files (.json)")
    parser.add_argument("--workshop", type=Path, help="the workshop file (default: workshop.toml beside the first "
                                                      "source)")
    parser.add_argument("--out", type=Path, help="where to write (default: out/<name>)")
    parser.add_argument("--bed", help="the machine's bed, LxW")
    parser.add_argument("--sheet", action="append", help="a size of sheet on hand, [MATERIAL:]LxW[*COUNT], the "
                                                         "grain along L; again for each (replaces the file's)")
    parser.add_argument("--offcut", action="append", help="an offcut on hand, MATERIAL:LxW; again for each "
                                                          "(replaces the file's)")
    parser.add_argument("--no-offcuts", action="store_true", help="leave the file's offcuts out")
    parser.add_argument("--spacing", type=float)
    parser.add_argument("--margin", type=float)
    parser.add_argument("--kerf", type=float)
    parser.add_argument("--max-cuts", type=int)
    parser.add_argument("--keep-across", type=float, help="mm a rest needs across to be kept")
    parser.add_argument("--keep-area", type=float, help="m2 a rest needs to be kept")
    parser.add_argument("--seconds", type=float, help="the nest's time per material at most (0.6 s a part)")
    parser.add_argument("--mode", choices=["anytime", "deterministic"], default="anytime")
    parser.add_argument("--no-refill", action="store_true", help="leave out refill (emptying a sheet into the others)")
    parser.add_argument("--material", help="nest this material only (as the layout names it, 'birch 15')")
    parser.add_argument("--traceback", action="store_true", help="print an error's whole stack")
    args = parser.parse_args(argv)
    try:
        return _run(args)
    except Exception as error:
        if args.traceback:
            raise
        print(describe(error), file=sys.stderr)
        return 1


def _run(args: argparse.Namespace) -> int:
    sources: list[Path] = args.sources
    name = "+".join(s.stem if s.suffix != ".json" else s.parent.name for s in sources)
    out_dir: Path = args.out or Path("out") / name
    workshop_file: Path | None = args.workshop
    if workshop_file is None and (sources[0].parent / "workshop.toml").exists():
        workshop_file = sources[0].parent / "workshop.toml"
    workshop = read_workshop(workshop_file) if workshop_file is not None else Workshop()
    offcuts = [parse_offcut(o) for o in args.offcut] if args.offcut else ([] if args.no_offcuts else None)
    workshop = with_overrides(
        workshop, bed=parse_size(args.bed, "--bed") if args.bed else None,
        sheets=[parse_sheet(s) for s in args.sheet] if args.sheet else None, offcuts=offcuts,
        spacing=args.spacing, margin=args.margin, kerf=args.kerf, max_cuts=args.max_cuts,
        keep_across=args.keep_across, keep_area=args.keep_area, seconds=args.seconds)
    layouts = [(s.stem if s.suffix != ".json" else s.parent.name, load(s)) for s in sources]
    layout = merged(layouts)
    t0 = time.perf_counter()
    options = Options(mode=args.mode, refill_seconds=0.0 if args.no_refill else Options().refill_seconds)
    nest, parts = nest_layout(layout, workshop, source=" ".join(str(s) for s in sources), material=args.material,
                              options=options, log=print)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "nest.json").write_text(json.dumps(nest, indent=1))
    (out_dir / "nest.layout.json").write_text(json.dumps(layout, indent=1))
    items = {item.path: item for items in parts.by_material.values() for item in items}
    (out_dir / "nest.svg").write_text(draw_nest(nest, items))
    for m in nest["materials"]:
        bought = ", ".join(f"{n} x {size}" for size, n in m["bought"].items()) or "no sheets"
        print(f"{m['material']}: {bought}" + (f", offcuts {', '.join(m['offcuts_used'])}" if m["offcuts_used"] else "")
              + f"; cuts per piece {[len(s['cuts']) for s in m['sheets']]}; used {m['used_area']:.2f} m2, "
              f"kept {m['kept_area']:.2f} m2")
    for p in nest["left_out"]:
        print(f"not nested: {p['path']} ({p['why']})")
    for problem in nest["problems"]:
        print(f"problem: {problem}")
    print(f"nest in {time.perf_counter() - t0:.1f} s -> {out_dir / 'nest.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
