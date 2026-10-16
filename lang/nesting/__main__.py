"""Nests a build's nests, and marks nests as made.

    python -m lang.nesting examples/van.py                       # every nest
    python -m lang.nesting examples/van.py kitchen.birch_15 floor.birch_15
    python -m lang.nesting out/van/layout.json --inventory stock.toml
    python -m lang.nesting examples/van.py --status              # what changed, nesting nothing
    python -m lang.nesting examples/van.py --made kitchen.birch_15        # made, every sheet
    python -m lang.nesting examples/van.py --made kitchen.birch_15 1 2    # sheets 1 and 2
    python -m lang.nesting examples/van.py --fixed kitchen.birch_15 kitchen.left

Runs the build file (or reads a layout file) and nests each nest named, by
its path (`kitchen.carcass`), or every nest of the build: those it declares
and one per material per module for what they do not take
(`lang.core.nests`). Each nest's values are the build's settings
(`lang.nesting.keys`: the bed, the saw, the gaps, the time), its stock the
sheets of each material's size, bought, and the pieces on hand in the
inventory, `inventory.toml` beside the source unless `--inventory` names
another (`lang.nesting.inventory`). The nests of one run share the stock on
hand, in their order: a piece one uses is not there for the next. A nest
run says which of its parts changed since its file was written
(`lang.nesting.fingerprint`).

Writes each nest into `--out` (default `out/<build>`, beside the preview's
build) under its module and name, `out/van/kitchen/birch_15/`: `nest.json`
(the nest, `lang/nesting/nest_types.py`), `nest.layout.json` (the layout
nested, for the Fusion emitter) and `nest.svg` (the drawing the preview
shows). Problems are printed and kept in the nest file; a nest whose parts
cannot be nested (a part larger than the bed, two values its parts give of
a setting it needs one of) is an error, and the others are nested still.

Pinning (`lang.nesting.pinning`): `--made NEST [SHEET ...]` marks a nest
as made, whole or the sheets named (`2`, or `birch 15:2` where two
materials have a sheet 2), in `made.json` in the out folder, and writes the
inventory back: the pieces on hand those sheets used come out, the rests
they kept go in; it runs no build. A nest marked is never nested again:
running it nests what is not made of it (parts changed, new, or on sheets
not made) into its second nest, `kitchen.birch_15-2`, and reports the parts
made that the build no longer has. `--fixed NEST PART ...` marks parts
changed since they were made as fixed by hand, made as they are now.
`--status` says for each nest what changed and what a run would nest.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

from ..build import describe, layout_of
from ..core.errors import LangError
from ..core.layout_types import Layout, NestLayout
from ..emit.plan import check_version
from .draw import draw_nest
from .fingerprint import fingerprints
from .inventory import NAME, read_inventory
from .ledger import write_back
from .nest import Options, nest_layout
from .nest_types import NestFile
from .pinning import (Standing, State, chain, changes, chosen_sheets, fix, mark, nest_files, now, open_name,
                      read_nest, read_state, second_folder, sheet_label, standing, write_state)
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
    pinning = parser.add_mutually_exclusive_group()
    pinning.add_argument("--made", nargs="+", metavar=("NEST", "SHEET"),
                         help="mark a nest as made, whole or the sheets named, and write the inventory back")
    pinning.add_argument("--fixed", nargs="+", metavar=("NEST", "PART"),
                         help="mark parts of a nest made and changed since as fixed by hand")
    pinning.add_argument("--status", action="store_true", help="say what changed since each nest, nest nothing")
    parser.add_argument("--traceback", action="store_true", help="print an error's whole stack")
    args = parser.parse_args(argv)
    if (args.made or args.fixed) and args.nests:
        parser.error("--made and --fixed name their nest themselves; give no nests besides")
    if args.fixed is not None and len(args.fixed) < 2:
        parser.error("--fixed takes a nest and the parts fixed: --fixed kitchen.carcass kitchen.left")
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
    inventory_file: Path = args.inventory or source.parent / NAME
    if args.made is not None:
        return _mark(out_dir, args.made[0], args.made[1:], inventory_file)
    inventory: list[OnHand] = read_inventory(inventory_file) if inventory_file.exists() else []
    layout = load(source)
    every = nests_of(layout)
    by_path = {n["path"]: n for n in every}
    state = read_state(out_dir)
    if args.fixed is not None:
        return _fix(layout, by_path, state, out_dir, args.fixed[0], args.fixed[1:])
    unknown = [n for n in args.nests if _base(n, by_path, state) is None]
    if unknown:
        raise LangError(f"No nest {', '.join(unknown)} in {source} (its nests: "
                        f"{', '.join(by_path) or 'none'}).")
    chosen = [by_path[b] for b in dict.fromkeys(_base(n, by_path, state) or "" for n in args.nests)] \
        if args.nests else every
    options = Options(mode=args.mode, refill_seconds=0.0 if args.no_refill else Options().refill_seconds)
    prints = fingerprints(layout)
    failed = 0
    for nest in chosen:
        path = nest["path"]
        if not nest["parts"]:
            print(f"{path}: no part to nest")
            continue
        folder = out_dir / nest_folder(nest)
        current = {p: prints[p] for p in nest["parts"] if p in prints}
        second: tuple[str, dict[str, str]] | None = None
        target = folder
        if path in state["nests"]:
            k = len(chain(state, path)) + 1
            target_name, target = open_name(state, path), second_folder(folder, k)
            if target_name in by_path:
                raise LangError(f"{target_name} is the name of {path}'s next nest, as it is marked as made, and of "
                                "a nest of the build; give that nest another name.")
            st = _standing(state, path, current, folder)
            _say_standing(path, st)
            if not st.reasons:
                print(f"{path}: everything made, nothing to nest")
                if target.exists() and not args.status:
                    shutil.rmtree(target)
                    print(f"{path}: {target_name} removed, as nothing is left for it")
                continue
            second = (target_name, st.reasons)
            print(f"{path}: {len(st.reasons)} part(s) to nest anew into {target_name}")
        else:
            _say_changes(path, folder, current)
        if args.status:
            continue
        t0 = time.perf_counter()
        try:
            result, parts = nest_layout(layout, path, inventory, source=str(source), options=options,
                                        log=_logger(second[0] if second is not None else path), second=second)
        except LangError as error:
            failed += 1
            print(f"{path}: {describe(error)}", file=sys.stderr)
            continue
        if result["name"] in state["nests"]:      # never: a nest marked is written no more
            raise LangError(f"{result['name']} is marked as made; its file is not written again.")
        inventory = used_up(inventory, result)
        target.mkdir(parents=True, exist_ok=True)
        (target / "nest.json").write_text(json.dumps(result, indent=1))
        (target / "nest.layout.json").write_text(json.dumps(layout, indent=1))
        items = {item.path: item for items in parts.by_material.values() for item in items}
        (target / "nest.svg").write_text(draw_nest(result, items))
        for m in result["materials"]:
            bought = ", ".join(f"{n} x {size}" for size, n in m["bought"].items()) or "nothing"
            print(f"{result['name']}: {m['material']}: bought {bought}"
                  + (f", on hand {', '.join(m['on_hand_used'])}" if m["on_hand_used"] else "")
                  + f"; cuts per piece {[len(s['cuts']) for s in m['sheets']]}; used {m['used_area']:.2f} m2, "
                  f"kept {m['kept_area']:.2f} m2")
        for problem in result["problems"]:
            print(f"{result['name']}: problem: {problem}")
        print(f"{result['name']}: nested in {time.perf_counter() - t0:.1f} s -> {target / 'nest.json'}")
    if args.status:
        return 1 if failed else 0
    nested = {path for n in every for path in n["parts"]}
    for m in layout["modules"]:
        for part in m["parts"]:
            if part["path"] not in nested:
                why = "slat" if part["kind"] == "slat" else "manual" if part["manual"] else "nest(False)"
                print(f"not nested: {part['path']} ({why})")
    return 1 if failed else 0


def _logger(name: str) -> Callable[[str], None]:
    return lambda line: print(f"{name}: {line}")


def _base(name: str, by_path: dict[str, NestLayout], state: State) -> str | None:
    """The build nest a name given stands for: itself, or the one a second
    nest of its follows (`kitchen.carcass-2`)."""
    if name in by_path:
        return name
    entry = state["nests"].get(name)
    if entry is not None and entry["follows"] in by_path:
        return entry["follows"]
    head, _, k = name.rpartition("-")
    return head if k.isdigit() and head in by_path else None


def _standing(state: State, base: str, current: dict[str, str], folder: Path) -> Standing:
    files: dict[str, NestFile] = {}
    for k, name in enumerate(chain(state, base), 1):
        file = (folder if k == 1 else second_folder(folder, k)) / "nest.json"
        if file.exists():
            files[name] = read_nest(file)
    return standing(state, base, current, files)


def _say_standing(path: str, st: Standing) -> None:
    print(f"{path}: marked as made; {len(st.made)} part(s) made and unchanged"
          + "".join(f"; {what} {', '.join(paths)}" for what, paths in
                    (("changed since made:", st.changed), ("not made:", st.not_made), ("new:", st.new),
                     ("made, gone from the build:", st.gone)) if paths))


def _say_changes(path: str, folder: Path, current: dict[str, str]) -> None:
    """What changed since a nest not marked was written, by its parts'
    fingerprints."""
    file = folder / "nest.json"
    if not file.exists():
        print(f"{path}: not nested yet")
        return
    try:
        found = changes(read_nest(file), current)
    except LangError as error:
        print(f"{path}: {error}")
        return
    print(f"{path}: " + ("; ".join(f"{what} {', '.join(paths)}" for what, paths in
                                   (("changed since nested:", found.changed), ("new:", found.new),
                                    ("gone:", found.gone)) if paths)
                         if found else "its parts are as nested"))


def _mark(out_dir: Path, name: str, sheets: list[str], inventory_file: Path) -> int:
    files = nest_files(out_dir)
    if name not in files:
        raise LangError(f"No nest file of {name} under {out_dir} (nested: {', '.join(files) or 'none'}); nest it "
                        "first.")
    nest = read_nest(files[name])
    state = read_state(out_dir)
    marked = mark(state, nest, chosen_sheets(nest, sheets) if sheets else None, now())
    for material, sheet in marked.before:
        print(f"{name}: {sheet_label(material, sheet)} was marked as made before")
    if not marked.sheets:
        print(f"{name}: nothing new to mark; the inventory is left as it is")
        return 0
    notes = write_back(inventory_file, marked.change)
    write_state(out_dir, state)
    print(f"{name}: marked as made: {', '.join(sheet_label(m, s) for m, s in marked.sheets)}"
          + (f" (follows {nest['follows']})" if nest["follows"] else ""))
    for note in notes:
        print(f"{name}: {note}")
    if marked.change:
        print(f"{name}: inventory written: {inventory_file}")
    return 0


def _fix(layout: Layout, by_path: dict[str, NestLayout], state: State, out_dir: Path, name: str,
         parts: list[str]) -> int:
    base = _base(name, by_path, state)
    if base is None:
        raise LangError(f"No nest {name} in the build (its nests: {', '.join(by_path) or 'none'}).")
    prints = fingerprints(layout)
    current = {p: prints[p] for p in by_path[base]["parts"] if p in prints}
    for note in fix(state, base, parts, current, now()):
        print(f"{base}: {note}")
    write_state(out_dir, state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
