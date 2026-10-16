"""Nests a build's nests.

    python -m lang.nesting examples/van.py                       # every nest
    python -m lang.nesting examples/van.py kitchen.birch_15 floor.birch_15
    python -m lang.nesting out/van/layout.json --inventory stock.toml

Runs the build file (or reads a layout file) and nests each nest named, by
its path (`kitchen.carcass`), or every nest of the build: those it declares
and one per material per module for what they do not name
(`lang.core.nests`). Each nest's values are the build's settings
(`lang.nesting.keys`: the bed, the saw, the gaps, the time), its stock the
sheets of each material's size, bought, and the pieces on hand in the
inventory, `inventory.toml` beside the source unless `--inventory` names
another (`lang.nesting.inventory`). The nests of one run share the stock on
hand, in their order: a piece one uses is not there for the next. The
inventory file is only read.

Writes each nest into `--out` (default `out/<build>`, beside the preview's
build) under its module and name, `out/van/kitchen/birch_15/`: `nest.json`
(the nest, `lang/nesting/nest_types.py`), `nest.layout.json` (the layout
nested, for the Fusion emitter) and `nest.svg` (the drawing the preview
shows). Problems are printed and kept in the nest file; a nest whose parts
cannot be nested (a part larger than the bed, two values its parts give of
a setting it needs one of) is an error, and the others are nested still.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import replace
from pathlib import Path

from ..build import describe, layout_of
from ..core.errors import LangError
from ..core.layout_types import Layout
from ..emit.plan import check_version
from .draw import draw_nest
from .inventory import NAME, read_inventory
from .nest import Options, nest_layout
from .nest_types import NestFile
from .resolve import nest_folder, nests_of
from .workshop import OnHand


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


def used_up(inventory: list[OnHand], nest: NestFile) -> list[OnHand]:
    """The stock on hand less what a nest used of it."""
    counts = [o.count for o in inventory]
    for m in nest["materials"]:
        for label in m["on_hand_used"]:
            k = next(k for k, o in enumerate(inventory)
                     if o.material == m["material"] and o.label() == label and counts[k] > 0)
            counts[k] -= 1
    return [replace(o, count=n) for o, n in zip(inventory, counts) if n > 0]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m lang.nesting", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path, help="the build file (.py), or a layout file (.json)")
    parser.add_argument("nests", nargs="*", help="the nests to nest, by path (kitchen.carcass); none: all")
    parser.add_argument("--inventory", type=Path, help=f"the stock on hand (default: {NAME} beside the source)")
    parser.add_argument("--out", type=Path, help="where to write (default: out/<build>)")
    parser.add_argument("--mode", choices=["anytime", "deterministic"], default="anytime")
    parser.add_argument("--no-refill", action="store_true", help="leave out refill (emptying a sheet into the others)")
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
    source: Path = args.source
    name = source.stem if source.suffix != ".json" else source.parent.name
    out_dir: Path = args.out or Path("out") / name
    inventory_file: Path | None = args.inventory
    if inventory_file is None and (source.parent / NAME).exists():
        inventory_file = source.parent / NAME
    inventory: list[OnHand] = read_inventory(inventory_file) if inventory_file is not None else []
    layout = load(source)
    every = nests_of(layout)
    by_path = {n["path"]: n for n in every}
    unknown = [n for n in args.nests if n not in by_path]
    if unknown:
        raise LangError(f"No nest {', '.join(unknown)} in {source} (its nests: "
                        f"{', '.join(by_path) or 'none'}).")
    chosen = [by_path[n] for n in dict.fromkeys(args.nests)] if args.nests else every
    options = Options(mode=args.mode, refill_seconds=0.0 if args.no_refill else Options().refill_seconds)
    failed = 0
    for nest in chosen:
        if not nest["parts"]:
            print(f"{nest['path']}: no part to nest")
            continue
        t0 = time.perf_counter()
        try:
            result, parts = nest_layout(layout, nest["path"], inventory, source=str(source), options=options,
                                        log=lambda line, path=nest["path"]: print(f"{path}: {line}"))
        except LangError as error:
            failed += 1
            print(f"{nest['path']}: {describe(error)}", file=sys.stderr)
            continue
        inventory = used_up(inventory, result)
        where = out_dir / nest_folder(nest)
        where.mkdir(parents=True, exist_ok=True)
        (where / "nest.json").write_text(json.dumps(result, indent=1))
        (where / "nest.layout.json").write_text(json.dumps(layout, indent=1))
        items = {item.path: item for items in parts.by_material.values() for item in items}
        (where / "nest.svg").write_text(draw_nest(result, items))
        for m in result["materials"]:
            bought = ", ".join(f"{n} x {size}" for size, n in m["bought"].items()) or "nothing"
            print(f"{nest['path']}: {m['material']}: bought {bought}"
                  + (f", on hand {', '.join(m['on_hand_used'])}" if m["on_hand_used"] else "")
                  + f"; cuts per piece {[len(s['cuts']) for s in m['sheets']]}; used {m['used_area']:.2f} m2, "
                  f"kept {m['kept_area']:.2f} m2")
        for problem in result["problems"]:
            print(f"{nest['path']}: problem: {problem}")
        print(f"{nest['path']}: nested in {time.perf_counter() - t0:.1f} s -> {where / 'nest.json'}")
    nested = {path for n in every for path in n["parts"]}
    for m in layout["modules"]:
        for part in m["parts"]:
            if part["path"] not in nested:
                why = "slat" if part["kind"] == "slat" else "manual" if part["manual"] else "nest(False)"
                print(f"not nested: {part['path']} ({why})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
