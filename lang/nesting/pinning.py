"""Pinning: nests marked as made [decided 2026-10-16, `design/nesting.md`,
Pinning]. A van is built over weeks; a module's sheets are machined in one
go, and now and then a change in between means making parts again.

A nest is marked as made, whole or by sheets (`python -m lang.nesting
build.py --made kitchen.carcass [SHEET ...]`, or a click in the preview's
nest view), in the state file beside the nests, never in the build file.
A nest so marked is frozen: its file is never written again and it is
never nested again. Running it again compares its parts' fingerprints
(`fingerprint`) with the build's (`standing`):

- parts made and unchanged are left out;
- parts changed since they were made, parts of the nest on a sheet not
  marked made (or left over), and parts new to it are nested anew, into a
  second nest beside it: `kitchen.carcass-2` in the folder
  `kitchen/carcass-2/`, and once that one is marked too,
  `kitchen.carcass-3`, and so on (the nest and its second nests are its
  chain); its file says which nest it follows and why each part is in it;
- parts made that the build's nest no longer has are reported (gone).

A part changed since it was made can be marked as fixed (a hole added by
hand, `--fixed kitchen.carcass kitchen.left`): it counts as made as it is
now. What a part was made as is the latest of these per chain: a sheet
marked made in the nest or a second nest, or a fix. Being made is per
nest: a remake (`van.nest("remake", [k["left"]])`) names a part made in
its module's nest to make it again.

Marking writes the inventory back (`ledger`): the pieces on hand the
sheets marked used come out, their kept rests go in; a sheet marked twice
does nothing the second time.

The state file, `made.json` in the build's out folder (`out/<build>/`),
written by the tools:

    {"version": 1,
     "nests": {"kitchen.carcass": {"follows": "", "written": "2026-10-16T09:30:00+02:00",
                                   "sheets": {"birch 15": ["1", "2"]}}},
     "made": {"kitchen.carcass": {"kitchen.left": {"fingerprint": "3f2a9c...",
                                                   "by": "kitchen.carcass birch 15 sheet 1",
                                                   "when": "2026-10-16T17:02:11+02:00"}}}}

`nests`: each nest marked, by path: the build's nest it follows ("" for
the build's own), when its file was written (its `written`, which the
marks belong to), and its sheets marked made, per material, in the order
marked. `made`: per build nest (its chain), each part made: its
fingerprint as made, what made it (a nest's sheet, or `fixed`), and when
it was marked.
"""
from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TypedDict, cast

from ..core.errors import LangError
from .ledger import Change, Piece
from .nest_types import NEST_VERSION, NestFile

#: The state file's name in a build's out folder, and its version.
STATE = "made.json"
STATE_VERSION = 1
#: What made a part fixed by hand.
FIXED = "fixed"


class MarkedNest(TypedDict):
    #: The build's nest a second nest follows; "" for the build's own.
    follows: str
    #: When its file was written (its `written`): the marks belong to it.
    written: str
    #: The sheets marked made, per material, in the order marked.
    sheets: dict[str, list[str]]


class MadePart(TypedDict):
    #: Its fingerprint as made (`lang.nesting.fingerprint`).
    fingerprint: str
    #: What made it: `<nest> <material> sheet <name>`, or `fixed` by hand.
    by: str
    #: When it was marked, ISO 8601.
    when: str


class State(TypedDict):
    version: int
    #: The nests marked, by path.
    nests: dict[str, MarkedNest]
    #: Per build nest (its chain), each part made, by path.
    made: dict[str, dict[str, MadePart]]


def empty() -> State:
    return {"version": STATE_VERSION, "nests": {}, "made": {}}


def read_state(out_dir: Path) -> State:
    """The state file in `out_dir`, or an empty state where there is none."""
    path = out_dir / STATE
    if not path.exists():
        return empty()
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise LangError(f"{path}: {error}; the marks of the nests made cannot be read.") from None
    if not isinstance(data, dict) or data.get("version") != STATE_VERSION or \
            not isinstance(data.get("nests"), dict) or not isinstance(data.get("made"), dict):  # pyright: ignore[reportUnknownMemberType]
        raise LangError(f"{path}: not a state file of version {STATE_VERSION} (the marks of the nests made).")
    return cast(State, data)


def write_state(out_dir: Path, state: State) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    scratch = out_dir / (STATE + ".writing")
    scratch.write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n")
    scratch.replace(out_dir / STATE)


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


# -- names -------------------------------------------------------------------------------------

def second_name(base: str, k: int) -> str:
    """The k-th nest of a build nest's chain (k >= 2): `kitchen.carcass-2`."""
    return f"{base}-{k}"


def second_folder(folder: Path, k: int) -> Path:
    """Its folder, beside the build nest's: `kitchen/carcass-2`."""
    return folder.with_name(f"{folder.name}-{k}")


def chain(state: State, base: str) -> list[str]:
    """The nests of a build nest's chain marked as made, in order: the nest
    itself, then its second nests while each is marked."""
    out: list[str] = []
    name = base
    while name in state["nests"]:
        out.append(name)
        name = second_name(base, len(out) + 1)
    return out


def open_name(state: State, base: str) -> str:
    """The nest a run of a build nest writes: the nest itself while it is
    not marked, else the first of its second nests that is not."""
    marked = chain(state, base)
    return base if not marked else second_name(base, len(marked) + 1)


def base_of(nest: NestFile) -> str:
    """The build nest a nest file belongs to."""
    return nest["follows"] or nest["name"]


def nest_files(out_dir: Path) -> dict[str, Path]:
    """The nest files under a build's out folder, by the nest's path."""
    out: dict[str, Path] = {}
    for path in sorted(out_dir.rglob("nest.json")):
        if any(part.startswith(".") for part in path.relative_to(out_dir).parts):
            continue
        try:
            name = json.loads(path.read_text()).get("name")
        except (OSError, ValueError, AttributeError):
            continue
        if isinstance(name, str) and name:
            out[name] = path
    return out


def read_nest(path: Path) -> NestFile:
    """A nest file, of this version (one with fingerprints)."""
    try:
        nest = json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise LangError(f"{path}: {error}") from None
    if not isinstance(nest, dict) or nest.get("version") != NEST_VERSION:  # pyright: ignore[reportUnknownMemberType]
        found = nest.get("version") if isinstance(nest, dict) else None  # pyright: ignore[reportUnknownMemberType]
        raise LangError(f"{path}: a nest file of version {found}, without its parts' fingerprints; nest it again "
                        f"(version {NEST_VERSION}) before marking it.")
    return cast(NestFile, nest)


# -- what a nest holds -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Placed:
    fingerprint: str
    material: str
    sheet: str


def placed(nest: NestFile) -> dict[str, Placed]:
    """Each part a nest file places, with its fingerprint and its sheet."""
    out: dict[str, Placed] = {}
    for m in nest["materials"]:
        for s in m["sheets"]:
            for b in s["blanks"]:
                for p in b["parts"]:
                    out[p["path"]] = Placed(p["fingerprint"], m["material"], s["name"])
    return out


def sheets_of(nest: NestFile) -> list[tuple[str, str]]:
    """A nest's sheets as (material, name), in its order."""
    return [(m["material"], s["name"]) for m in nest["materials"] for s in m["sheets"]]


def sheet_label(material: str, sheet: str) -> str:
    return f"{material} sheet {sheet}"


def chosen_sheets(nest: NestFile, names: Sequence[str]) -> list[tuple[str, str]]:
    """The sheets named: `2` where one material has a sheet 2, else
    `birch 15:2` (or the label made file-safe, `birch_15:2`)."""
    every = sheets_of(nest)
    out: list[tuple[str, str]] = []
    for name in names:
        material, _, sheet = name.rpartition(":")
        found = [(m, s) for m, s in every if s == sheet and (not material or material in (m, _safe(m)))]
        if len(found) != 1:
            listed = ", ".join(f"{m}:{s}" for m, s in every) or "none"
            why = "names two sheets; say which material's" if found else "is no sheet of it"
            raise LangError(f"{nest['name']}: {name!r} {why} (its sheets: {listed}).")
        if found[0] not in out:
            out.append(found[0])
    return out


def _safe(label: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", label).strip("_")


# -- a nest against the build ----------------------------------------------------------------------

@dataclass(frozen=True)
class Changes:
    """A nest's file against the build: parts changed (another
    fingerprint), new to it, and gone from it, each in order."""
    changed: list[str] = field(default_factory=list[str])
    new: list[str] = field(default_factory=list[str])
    gone: list[str] = field(default_factory=list[str])

    def __bool__(self) -> bool:
        return bool(self.changed or self.new or self.gone)


def changes(nest: NestFile, now: Mapping[str, str]) -> Changes:
    """What changed since a nest file was written: `now` is the nest's
    parts in the build, path to fingerprint (its parts that the file left
    over count as placed)."""
    was = {path: p.fingerprint for path, p in placed(nest).items()}
    unplaced = {path for m in nest["materials"] for path in m["unplaced"]}
    return Changes([p for p, f in now.items() if p in was and was[p] != f],
                   [p for p in now if p not in was and p not in unplaced],
                   [p for p in list(was) + sorted(unplaced) if p not in now])


@dataclass(frozen=True)
class Standing:
    """A build nest marked as made against the build: each of its parts
    now made (and by what), changed since it was made, not made (in a nest
    of its chain, on a sheet not made or left over), or new; and the parts
    made that it no longer has."""
    made: dict[str, str] = field(default_factory=dict[str, str])
    changed: list[str] = field(default_factory=list[str])
    not_made: list[str] = field(default_factory=list[str])
    new: list[str] = field(default_factory=list[str])
    gone: list[str] = field(default_factory=list[str])
    #: The order of the nest's parts now.
    order: list[str] = field(default_factory=list[str])

    @property
    def reasons(self) -> dict[str, str]:
        """The parts to nest anew, in the nest's order, and why."""
        why = {p: "changed" for p in self.changed} | {p: "not made" for p in self.not_made} | \
            {p: "new" for p in self.new}
        return {p: why[p] for p in self.order if p in why}


def standing(state: State, base: str, now: Mapping[str, str], files: Mapping[str, NestFile]) -> Standing:
    """A build nest's parts (`now`, in order, path to fingerprint) against
    what its chain made; `files`, the chain's nest files by path, tell a
    part not made from a new one."""
    made = state["made"].get(base, {})
    before = {path for name in chain(state, base) if name in files for path in _held(files[name])}
    out = Standing(order=list(now))
    for path, print_ in now.items():
        record = made.get(path)
        if record is not None and record["fingerprint"] == print_:
            out.made[path] = record["by"]
        elif record is not None:
            out.changed.append(path)
        elif path in before:
            out.not_made.append(path)
        else:
            out.new.append(path)
    out.gone.extend(p for p in made if p not in now)
    return out


@dataclass(frozen=True)
class Run:
    """What a run of a build nest does: the nest it writes, its place in
    the chain (`k`, 1 for the nest itself, else its second nest's counter),
    and, for a nest marked as made, how it stands against the build and
    the parts to nest anew with why (none: nothing is left to nest)."""
    name: str
    k: int
    standing: Standing | None = None

    @property
    def parts(self) -> dict[str, str] | None:
        """The parts the run nests and why; None: the nest whole, as
        usual."""
        return None if self.standing is None else self.standing.reasons


def plan_run(state: State, base: str, now: Mapping[str, str], files: Mapping[str, NestFile]) -> Run:
    """What a run of the build nest `base` does (see the module's doc):
    `now` its parts in the build, path to fingerprint, `files` the nest
    files of its chain marked as made."""
    marked = chain(state, base)
    if not marked:
        return Run(base, 1)
    return Run(open_name(state, base), len(marked) + 1, standing(state, base, now, files))


def _held(nest: NestFile) -> list[str]:
    return list(placed(nest)) + [path for m in nest["materials"] for path in m["unplaced"]]


# -- marks -----------------------------------------------------------------------------------------

@dataclass
class Marked:
    """What a mark did: the sheets newly marked made, those marked before,
    and the inventory's change."""
    sheets: list[tuple[str, str]]
    before: list[tuple[str, str]]
    change: Change


def mark(state: State, nest: NestFile, sheets: Sequence[tuple[str, str]] | None, when: str) -> Marked:
    """Marks a nest's sheets (all where None) as made in `state`: its parts
    on them count as made as the file has them; returns what it did, the
    inventory's change for the sheets newly marked (a sheet marked before
    changes nothing)."""
    name = nest["name"]
    if not name:
        raise LangError("A nest without a name (not a nest of a build) cannot be marked as made.")
    base = base_of(nest)
    entry = state["nests"].get(name)
    if entry is not None and entry["written"] != nest["written"]:
        raise LangError(f"{name}: its file was written {nest['written']}, after it was marked as made "
                        f"({entry['written']}); the marks are the earlier file's.")
    if entry is None and name != base and open_name(state, base) != name:
        raise LangError(f"{name} follows {base}, whose nests before it are not all marked as made.")
    marked = chain(state, base)
    if name in marked[:-1]:
        raise LangError(f"{name}: what is not made of it was nested anew in {marked[marked.index(name) + 1]}, "
                        "which is marked as made; mark the sheets of the last nest.")
    chosen = sheets_of(nest) if sheets is None else list(sheets)
    if not chosen:
        raise LangError(f"{name}: it has no sheet to mark as made.")
    done = {(m, s) for m, names in (entry["sheets"] if entry else {}).items() for s in names}
    new = [k for k in chosen if k not in done]
    out = Marked(new, [k for k in chosen if k in done], Change())
    if not new:
        return out
    if entry is None:
        entry = MarkedNest(follows=nest["follows"], written=nest["written"], sheets={})
        state["nests"][name] = entry
    for material, sheet in new:
        entry["sheets"].setdefault(material, []).append(sheet)
    made = state["made"].setdefault(base, {})
    taken: list[Piece] = []
    added: list[tuple[Piece, str]] = []
    wanted = set(new)
    for m in nest["materials"]:
        for s in m["sheets"]:
            if (m["material"], s["name"]) not in wanted:
                continue
            by = f"{name} {sheet_label(m['material'], s['name'])}"
            for b in s["blanks"]:
                for p in b["parts"]:
                    made[p["path"]] = {"fingerprint": p["fingerprint"], "by": by, "when": when}
            if not s["bought"]:
                taken.append(Piece(m["material"], s["size"][0], s["size"][1]))
            note = f"kept from {by}, marked made {when[:10]}"
            for r in s["rests"]:
                if r["keep"]:
                    added.append((Piece(m["material"], r["rect"][2], r["rect"][3]), note))
    out.change = Change(tuple(taken), tuple(added))
    return out


def fix(state: State, base: str, parts: Sequence[str], now: Mapping[str, str], when: str) -> list[str]:
    """Marks parts made in a build nest's chain and changed since as fixed
    by hand: they count as made as the build has them now (`now`, path to
    fingerprint). Refuses a part not made there, gone, or unchanged."""
    made = state["made"].get(base, {})
    notes: list[str] = []
    for path in parts:
        record = made.get(path)
        if record is None:
            raise LangError(f"{path} is not made in {base} or a nest after it; only a part made can be fixed.")
        if path not in now:
            raise LangError(f"{path} is no longer in {base}; there is nothing to fix.")
        if record["fingerprint"] == now[path]:
            raise LangError(f"{path} is made and unchanged ({record['by']}); there is nothing to fix.")
    for path in parts:
        made[path] = {"fingerprint": now[path], "by": FIXED, "when": when}
        notes.append(f"{path}: fixed by hand, made as the build has it now")
    return notes


__all__ = ["STATE", "STATE_VERSION", "FIXED", "MarkedNest", "MadePart", "State", "empty", "read_state",
           "write_state", "now", "second_name", "second_folder", "chain", "open_name", "base_of", "nest_files",
           "read_nest", "Placed", "placed", "sheets_of", "sheet_label", "chosen_sheets", "Changes", "changes",
           "Standing", "standing", "Run", "plan_run", "Marked", "mark", "fix"]
