"""Plans a build's nests for the machine.

    python -m lang.cam examples/drawer_cabinet.py                       # every nest nested
    python -m lang.cam examples/drawer_cabinet.py drawercab.birch_15     # the nests named
    python -m lang.cam examples/drawer_cabinet.py --from-nest            # without running the build

Plans every nest that has a nest file under the build's out folder
(`out/<build>`, as `python -m lang.nesting` writes them), or those named
by their path, and writes each plan beside its nest, `cam.json`
(`lang/cam/plan_types.py`). The geometry is the nest's: its file and the
layout it nested (`nest.layout.json`). The CAM settings are the build's as
it is now, so a CAM setting changed since the nest holds without nesting
again; the build is run for them, unless `--from-nest` says to take the
layout nested. A part changed since the nest is planned as nested, and
said so: nest it again for the change.

Prints each setup's operations, what it leaves out (but what is in a
narrow face, which is taken care of) and its problems; the plan's own
check (`verify`) adds what it finds to the problems.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ..build import describe, layout_of
from ..core.errors import LangError
from ..core.layout_types import Layout
from ..emit.plan import check_version
from ..nesting.fingerprint import fingerprints
from ..nesting.pinning import changes, nest_files, read_nest
from .plan import plan_nest
from .plan_types import CamFile
from .verify import verify

NAME = "cam.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m lang.cam", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path, help="the build file (.py)")
    parser.add_argument("nests", nargs="*", help="the nests to plan, by path (kitchen.carcass); none: every nest "
                                                 "nested")
    parser.add_argument("--out", type=Path, help="where the nests are (default: out/<build>)")
    parser.add_argument("--from-nest", action="store_true",
                        help="take the CAM settings from the layout nested, not from the build as it is now")
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
    out_dir: Path = args.out or Path("out") / source.stem
    files = nest_files(out_dir)
    unknown = [n for n in args.nests if n not in files]
    if unknown:
        raise LangError(f"No nest file of {', '.join(unknown)} under {out_dir} (nested: "
                        f"{', '.join(files) or 'none'}); nest it first: python -m lang.nesting {source}")
    chosen = list(args.nests) or list(files)
    if not chosen:
        raise LangError(f"No nest under {out_dir}; nest the build first: python -m lang.nesting {source}")
    build: Layout | None = None if args.from_nest else layout_of(source)
    prints = fingerprints(build) if build is not None else {}
    failed = 0
    for name in chosen:
        file = files[name]
        try:
            nest = read_nest(file)
            layout: Layout = json.loads((file.parent / "nest.layout.json").read_text())
            try:
                check_version(layout)
            except ValueError as error:
                raise LangError(f"{file.parent / 'nest.layout.json'}: {error} Nest it again.") from None
            if build is not None:
                parts = [p["path"] for m in nest["materials"] for s in m["sheets"] for b in s["blanks"]
                         for p in b["parts"]]
                found = changes(nest, {p: prints[p] for p in parts if p in prints})
                if found.changed:
                    print(f"{name}: changed since nested, planned as nested: {', '.join(found.changed)}")
                if found.gone:
                    print(f"{name}: no longer in the build, planned as nested: {', '.join(found.gone)}")
            plan = plan_nest(nest, layout, settings=build)
            found_problems = verify(plan, nest, layout)
            plan["problems"] += [f"check: {p}" for p in found_problems]
        except (LangError, OSError, ValueError) as error:
            failed += 1
            print(f"{name}: {describe(error) if isinstance(error, LangError) else error}", file=sys.stderr)
            continue
        target = file.parent / NAME
        target.write_text(json.dumps(plan, indent=1))
        _report(plan)
        print(f"{name}: planned -> {target}")
    return 1 if failed else 0


def _report(plan: CamFile) -> None:
    for setup in plan["setups"]:
        print(f"{setup['name']}: {len(setup['parts'])} part(s)"
              + (", its own blank" if setup["stock"]["own_blank"] else ""))
        for op in setup["operations"]:
            tabs = op["params"]["tabs"]
            print(f"  {op['name']}: {len(op['features'])} feature(s)"
                  + (f", {len(tabs['positions'])} tab(s)" if tabs is not None else ""))
        # what is left out, an operation a line with its chamfer and dog bones
        lines: dict[tuple[str, int, str], list[str]] = {}
        notes: dict[tuple[str, int, str], str] = {}
        for left in setup["left_out"]:
            if left["why"] == "narrow face":
                continue
            r = left["op"]
            key = (left["part"], r["index"], left["why"])
            lines.setdefault(key, []).append(r["aspect"])
            if left["note"] and not notes.get(key):
                notes[key] = left["note"]
        for (part, index, why), aspects in lines.items():
            ref = next(lo["op"] for lo in setup["left_out"] if lo["part"] == part and lo["op"]["index"] == index)
            what = ref["name"] or ref["kind"] if index >= 0 else "the outline"
            reliefs = sum(1 for a in aspects if a.startswith("relief"))
            extra = [a for a in aspects if a not in ("op",) and not a.startswith("relief")]
            more = ", ".join(extra + ([f"{reliefs} dog bone(s)"] if reliefs else []))
            note = notes.get((part, index, why), "")
            print(f"  left out: {part} {what}" + (f" ({more})" if more else "") + f": {why}"
                  + (f", {note}" if note else ""))
        for problem in setup["problems"]:
            print(f"  problem: {problem}")
    for problem in plan["problems"]:
        if problem.startswith("check: "):
            print(f"{plan['nest']}: {problem}")


if __name__ == "__main__":
    sys.exit(main())
