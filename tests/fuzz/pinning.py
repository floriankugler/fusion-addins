"""Random builds edited at random and random sequences of marks, for
fuzzing pinning (`lang.nesting.pinning`) and the inventory written back
(`lang.nesting.ledger`) against a plain model. A case is plain data.

A `PinCase` is a build nest's parts (paths with fingerprints, of two
materials), an inventory (entries of either material in a few sizes, with
counts given or not, a comment above some of them, loose comments after
some, a comment at the top) and steps:

- `nest`: a run of the nest as the command makes it (`plan_run`): the nest
  whole while it is not marked, else what is not made of it into its next
  second nest; nested by a stand-in for the solver that puts the parts on
  sheets at random (one left over now and then), bought or pieces on hand
  from the inventory, with rests kept or not;
- `mark`: a nest written so far marked as made, whole or by random sheets,
  some marked before;
- `edit`: a part's fingerprint changed (an operation changed), a part moved
  (its fingerprint kept), a part added or removed;
- `fix`: a part marked as fixed by hand, made and changed since or not.

`pinning_problems` runs the steps on files in a scratch folder (the state
file and the inventory written and read back each time) and checks each
against the model: a run nests every part while the nest is not marked,
and once it is, exactly the parts changed since they were made, those of
its nests not on a sheet made and those new, each with its reason, under
the next name of the chain, and reports the parts made that are gone; a
nest marked is never written again; a mark is refused exactly for a nest
whose next nest is marked; a part made counts as made as the latest mark
or fix has it; a fix is refused exactly for a part not made, gone or
unchanged; and the inventory holds what the model says after every mark
(a piece on hand used comes out of the first entry of its size, its count
lowered or the entry gone, a kept rest goes in at the end, a sheet marked
twice does nothing the second time), with every comment kept in order but
those above the entries removed.
"""
from __future__ import annotations

import random
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from hypothesis import strategies as st

from lang.core.errors import LangError
from lang.nesting.inventory import inventory_from
from lang.nesting.ledger import write_back
from lang.nesting.nest_types import NEST_VERSION, NestFile
from lang.nesting.pinning import (chain, fix, mark, open_name, plan_run, read_state, second_name, sheets_of,
                                  write_state)

BASE = "m.carcass"
MATERIALS = ("birch 15", "birch 9")
#: The sizes of the pieces on hand and of the rests (mm), and the sheet bought.
SIZES = ((1250.0, 600.0), (900.0, 450.0), (2500.0, 655.0))
SHEET = (2500.0, 1250.0)
WHEN = "2026-10-16T17:00:00+02:00"

#: A step: ("nest", seed), ("mark", nest index, sheets or None), ("edit", kind, part index, seed),
#: ("fix", part index).
Step = tuple[Any, ...]


@dataclass(frozen=True)
class Entry:
    material: int
    size: int
    count: int | None          # None: not written (1)
    above: bool                # a comment right above it
    after: bool                # a loose comment after it
    inside: bool = False       # a comment between its keys
    tight: bool = False        # its keys written key=value


@dataclass(frozen=True)
class PinCase:
    #: Each part's material and fingerprint, by its index (`m.p<k>`).
    parts: tuple[tuple[int, str], ...]
    entries: tuple[Entry, ...]
    steps: tuple[Step, ...]


@st.composite
def pin_cases(draw: st.DrawFn) -> PinCase:
    parts = tuple((draw(st.integers(0, 1)), f"f{k}") for k in range(draw(st.integers(1, 6))))
    entries = tuple(Entry(draw(st.integers(0, 1)), draw(st.integers(0, len(SIZES) - 1)),
                          draw(st.one_of(st.none(), st.integers(1, 3))), draw(st.booleans()), draw(st.booleans()),
                          draw(st.booleans()), draw(st.booleans()))
                    for _ in range(draw(st.integers(0, 4))))
    steps: list[Step] = [("nest", draw(st.integers(0, 2 ** 16)))]
    for _ in range(draw(st.integers(1, 9))):
        kind = draw(st.sampled_from(["nest", "nest", "mark", "mark", "mark", "edit", "edit", "fix"]))
        if kind == "nest":
            steps.append(("nest", draw(st.integers(0, 2 ** 16))))
        elif kind == "mark":
            sheets = draw(st.one_of(st.none(), st.lists(st.integers(0, 5), min_size=1, max_size=3)))
            steps.append(("mark", draw(st.integers(0, 3)), None if sheets is None else tuple(sheets)))
        elif kind == "edit":
            steps.append(("edit", draw(st.sampled_from(["change", "move", "add", "remove"])),
                          draw(st.integers(0, 9)), draw(st.integers(0, 2 ** 16))))
        else:
            steps.append(("fix", draw(st.integers(0, 9))))
    return PinCase(parts, entries, tuple(steps))


# -- the inventory and its model ----------------------------------------------------------------

def _ledger_text(case: PinCase) -> tuple[str, list[Any]]:
    """The inventory's text, and its model: a list of comments
    ("comment", text) and entries ("entry", [material, length, width,
    count], its comments, above it and between its keys)."""
    lines = ["# The stock on hand.", ""]
    items: list[Any] = [("comment", "# The stock on hand.")]
    for k, e in enumerate(case.entries):
        above = [f"# entry {k}"] if e.above else []
        lines += above
        length, width = SIZES[e.size]
        eq = "=" if e.tight else " = "
        lines += ["[[stock]]", f'material{eq}"{MATERIALS[e.material]}"']
        inside = [f"# inside {k}"] if e.inside else []
        lines += inside + [f"size{eq}[{length:g}, {width:g}]"]
        if e.count is not None:
            lines.append(f"count{eq}{e.count}" + ("" if e.tight else "   # as counted"))
        items.append(("entry", [MATERIALS[e.material], length, width, e.count or 1], above + inside))
        lines.append("")
        if e.after:
            lines += [f"# loose after {k}", ""]
            items.append(("comment", f"# loose after {k}"))
    return "\n".join(lines) + "\n", items


def _ledger_problems(path: Path, items: list[Any], when: str) -> list[str]:
    text = path.read_text()
    got = inventory_from(tomllib.loads(text))
    want = [(m, l, w, n) for kind, *rest in items if kind == "entry" for m, l, w, n in [rest[0]]]
    problems: list[str] = []
    if [(o.material, o.length, o.width, o.count) for o in got] != want:
        problems.append(f"{when}: the inventory holds {got}, the model's {want}")
    comments = [line.strip() for line in text.splitlines() if line.strip().startswith("#")]
    want_comments = [c for kind, *rest in items for c in ([rest[0]] if kind == "comment" else rest[1])]
    if comments != want_comments:
        problems.append(f"{when}: the inventory's comments are {comments}, the model's {want_comments}")
    return problems


def _take(items: list[Any], material: str, size: list[float]) -> None:
    for k, (kind, *rest) in enumerate(items):
        if kind == "entry" and rest[0][0] == material and rest[0][1:3] == size and rest[0][3] > 0:
            rest[0][3] -= 1
            if rest[0][3] == 0:
                del items[k]
            return


# -- the stand-in for the solver ---------------------------------------------------------------

def _nest_file(name: str, parts: dict[str, tuple[int, str]], items: list[Any], seed: int,
               written: str) -> NestFile:
    """The parts on sheets at random: per material one sheet or more,
    bought or a piece on hand the inventory has, rests kept or not, a part
    left over now and then."""
    rng = random.Random(seed)
    materials: list[dict[str, Any]] = []
    left = {k: rest[0][3] for k, (kind, *rest) in enumerate(items) if kind == "entry"}
    for mi, material in enumerate(MATERIALS):
        paths = [p for p, (m, _f) in parts.items() if m == mi]
        if not paths:
            continue
        unplaced = [p for p in paths if rng.random() < 0.1]
        placed = [p for p in paths if p not in unplaced]
        n = rng.randint(1, max(1, len(placed)))
        sheets: list[dict[str, Any]] = []
        for s in range(n):
            on_hand = [k for k, c in left.items() if c > 0 and items[k][1][0] == material]
            if on_hand and rng.random() < 0.5:
                k = rng.choice(on_hand)
                left[k] -= 1
                size, bought = items[k][1][1:3], False
            else:
                size, bought = list(SHEET), True
            sheets.append({"name": str(s + 1), "stock": "sheet", "bought": bought, "size": size, "cuts": [],
                           "blanks": [], "rests": [{"rect": [0.0, 0.0, *SIZES[rng.randrange(len(SIZES))]],
                                                    "keep": rng.random() < 0.6} for _ in range(rng.randint(0, 2))]})
        for k, path in enumerate(placed):
            sheet = sheets[k] if k < n else rng.choice(sheets)
            sheet["blanks"].append({"name": f"{sheet['name']}.{len(sheet['blanks']) + 1}", "rect": [0, 0, 1, 1],
                                    "own_blank": False,
                                    "parts": [{"path": path, "fingerprint": parts[path][1], "up": "top",
                                               "turn": 0.0, "at": [0, 0], "transform": []}]})
        materials.append({"material": material, "thickness": 15.0, "sheets": [s for s in sheets if s["blanks"]],
                          "bought": {}, "on_hand_used": [], "parts_area": 0.0, "stock_area": 0.0,
                          "kept_area": 0.0, "used_area": 0.0, "unplaced": unplaced, "notes": []})
    nest: dict[str, Any] = {"version": NEST_VERSION, "name": name, "follows": "" if name == BASE else BASE,
                            "reasons": {}, "written": written, "source": "", "layout_hash": "", "settings": {},
                            "materials": materials, "left_out": [], "problems": []}
    return cast(NestFile, nest)


# -- running a case ------------------------------------------------------------------------------

def pinning_problems(case: PinCase) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        return _run(case, Path(tmp))


def _run(case: PinCase, folder: Path) -> list[str]:
    ledger = folder / "inventory.toml"
    text, items = _ledger_text(case)
    ledger.write_text(text)
    parts: dict[str, tuple[int, str]] = {f"m.p{k}": p for k, p in enumerate(case.parts)}
    added = len(parts)
    files: dict[str, NestFile] = {}
    marked: dict[str, set[tuple[str, str]]] = {}           # the model's marks, in the chain's order
    made: dict[str, str] = {}                              # path -> fingerprint as made
    problems: list[str] = []
    for n, step in enumerate(case.steps):
        when = f"step {n} {step}"
        state = read_state(folder)
        now = {p: f for p, (_m, f) in parts.items()}
        if step[0] == "nest":
            run = plan_run(state, BASE, now, {name: files[name] for name in chain(state, BASE) if name in files})
            want_name = BASE if not marked else second_name(BASE, len(marked) + 1)
            before = {p for name in marked for p in _held(files[name])}
            want: dict[str, str] | None = None
            if marked:
                want = {}
                for p, f in now.items():
                    if p in made:
                        if made[p] != f:
                            want[p] = "changed"
                    else:
                        want[p] = "not made" if p in before else "new"
            if run.name != want_name or run.parts != want:
                problems.append(f"{when}: the run nests {run.parts} as {run.name}, the model's {want} as {want_name}")
                break
            gone = [p for p in made if p not in now]
            if run.standing is not None and run.standing.gone != gone:
                problems.append(f"{when}: gone {run.standing.gone}, the model's {gone}")
            if run.name in marked:
                problems.append(f"{when}: a run would write {run.name}, which is marked as made")
                break
            nested = parts if want is None else {p: parts[p] for p in want}
            if not nested:
                files.pop(run.name, None)
                continue
            files[run.name] = _nest_file(run.name, nested, items, step[1], f"2026-10-16T{10 + n:02d}:00:00+02:00")
        elif step[0] == "mark":
            names = list(files)
            if not names:
                continue
            name = names[step[1] % len(names)]
            nest = files[name]
            every = sheets_of(nest)
            chosen = None if step[2] is None or not every else list(dict.fromkeys(every[k % len(every)]
                                                                                   for k in step[2]))
            order = list(marked)
            refused = not every or name in order[:-1] or \
                (name not in marked and name != (second_name(BASE, len(order) + 1) if order else BASE))
            try:
                result = mark(state, nest, chosen, WHEN)
            except LangError as e:
                if not refused:
                    problems.append(f"{when}: refused ({e}), the model marks it")
                continue
            if refused:
                problems.append(f"{when}: marked, though the model refuses it")
                continue
            new = [k for k in (chosen if chosen is not None else every) if k not in marked.get(name, set())]
            if result.sheets != new:
                problems.append(f"{when}: newly marked {result.sheets}, the model's {new}")
            if not new:
                if result.change:
                    problems.append(f"{when}: sheets marked before change the inventory")
                continue
            marked.setdefault(name, set()).update(new)
            for m in nest["materials"]:
                for s in m["sheets"]:
                    if (m["material"], s["name"]) not in new:
                        continue
                    for b in s["blanks"]:
                        for p in b["parts"]:
                            made[p["path"]] = p["fingerprint"]
                    if not s["bought"]:
                        _take(items, m["material"], s["size"])
            groups: dict[tuple[str, float, float, str], list[Any]] = {}
            for m in nest["materials"]:
                for s in m["sheets"]:
                    if (m["material"], s["name"]) not in new:
                        continue
                    note = f"# kept from {name} {m['material']} sheet {s['name']}, marked made {WHEN[:10]}"
                    for r in s["rests"]:
                        if r["keep"]:
                            key = (m["material"], r["rect"][2], r["rect"][3], note)
                            groups.setdefault(key, [m["material"], r["rect"][2], r["rect"][3], 0])[3] += 1
            for (_m, _l, _w, note), entry in groups.items():
                items.append(("entry", entry, [note]))
            try:
                write_back(ledger, result.change)
            except LangError as e:
                problems.append(f"{when}: the inventory was not written: {e}")
                break
            write_state(folder, state)
            problems += _ledger_problems(ledger, items, when)
            again = mark(state, nest, chosen, WHEN)
            if again.sheets or again.change:
                problems.append(f"{when}: marked again, it marks {again.sheets} and changes the inventory by "
                                f"{again.change}")
        elif step[0] == "edit":
            kind, k, seed = step[1], step[2], step[3]
            paths = list(parts)
            if kind == "add" or not paths:
                parts[f"m.p{added}"] = (seed % 2, f"g{seed}")
                added += 1
            elif kind == "remove":
                del parts[paths[k % len(paths)]]
            elif kind == "change":
                path = paths[k % len(paths)]
                parts[path] = (parts[path][0], f"h{seed}")
            # "move": the fingerprint stays
        else:
            paths = list(parts) + ["m.nowhere"]
            path = paths[step[1] % len(paths)]
            refused = path not in made or path not in now or made[path] == now[path]
            try:
                fix(state, BASE, [path], now, WHEN)
            except LangError as e:
                if not refused:
                    problems.append(f"{when}: refused ({e}), the model fixes it")
                continue
            if refused:
                problems.append(f"{when}: fixed, though the model refuses it")
                continue
            made[path] = now[path]
            write_state(folder, state)
        if state["made"].get(BASE, {}) and {p: r["fingerprint"] for p, r in state["made"][BASE].items()} != made:
            problems.append(f"{when}: made {state['made'][BASE]}, the model's {made}")
        if chain(state, BASE) != list(marked) or open_name(state, BASE) != (
                second_name(BASE, len(marked) + 1) if marked else BASE):
            problems.append(f"{when}: the chain is {chain(state, BASE)}, the model's {list(marked)}")
        if problems:
            break
    return problems


def _held(nest: NestFile) -> list[str]:
    return [p["path"] for m in nest["materials"] for s in m["sheets"] for b in s["blanks"] for p in b["parts"]] + \
        [p for m in nest["materials"] for p in m["unplaced"]]


__all__ = ["PinCase", "pin_cases", "pinning_problems"]
