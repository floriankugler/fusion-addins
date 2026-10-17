"""Random nests declared in random modules with random nesting settings,
and random inventories, for fuzzing which part lands in which nest with
which values (`lang.core.nests`, `lang.nesting.resolve`) and what a nest
may use and buy (`lang.nesting.inventory`, `workshop_of`, `used_up`), each
against a plain model. A case is plain data.

A `NestsCase` is a build: modules at the root, the first holding some of
the others now and then; in each module boards of three materials, some
in sub-scopes, some `nest(False)` or manual; the root, the modules (in
their block or from outside after it), the sub-scopes, the boards and the
nests using random values of four nesting keys (`bed`, without a default;
`margin` and `refill`, of which a nest needs one value; `spacing`, of
which the larger holds between two parts); and nests declared on modules
and sub-scopes, by material (some before the boards they take) or by
boards named anywhere in their scope. `nests_problems` builds it and
compares every nest in the layout with the model's: each declared nest's
boards, a default nest per module and material for the nested boards no
declared nest of their module takes (a nest of the first module naming a
board of a module inside it leaves it in that module's), the errors of a manual board named or a board in two
nests of one module; each nest's values as `resolve` gives them with the
model's (its own, else its parts' along their chains, else the default,
the first key the parts disagree on or none gives refused, each part's
spacing, the sources); and a declared nest's `value()`, its own else its
scope's chain.

A `LedgerCase` is an inventory (entries of the build's materials and
another, with sizes and counts given or not) written as TOML, and small
parts of two materials, one with a sheet size, in two modules.
`ledger_problems` reads it back, then nests every nest in turn as the
command does, the stock on hand shared: a nest is refused exactly when a
material has neither a size nor anything left on hand, buys the material's
size only and only where it has one, uses no piece more often than is
left, leaves parts over only where nothing is to be bought, and `used_up`
takes what it used out.
"""
from __future__ import annotations

from collections import Counter
from contextlib import nullcontext
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hypothesis import strategies as st

from fuzzing import fresh, sizes
from lang import Board, Box, Scope, board, module, nesting, no_interference, scope, sheet_material, uncheck, use
from lang.core.errors import LangError
from lang.core.layout import build_layout
from lang.core.layout_types import Layout
from lang.core.nests import file_safe
from lang.core.settings import Binding
from lang.nesting.__main__ import used_up
from lang.nesting.inventory import read_inventory
from lang.nesting.nest import Options, nest_layout
from lang.nesting.resolve import nest_of, nests_of, resolve, workshop_of
from lang.nesting.workshop import OnHand

MATS = (sheet_material("birch", t=15), sheet_material("birch", t=9),
        sheet_material("mdf", t=16, grain=False, size=(2500, 1250)))
#: The keys varied, the values each takes, and the keys' defaults (None: none).
VALUES: dict[str, tuple[Any, ...]] = {"bed": ((2000.0, 1000.0), (2500.0, 1250.0)), "margin": (10.0, 12.0),
                                      "spacing": (10.0, 20.0), "refill": (True, False)}
DEFAULTS: dict[str, Any] = {"bed": None, "margin": 10.0, "spacing": 10.0, "refill": True}
#: The order `resolve` takes them in (`keys.KEYS`).
ORDER = ("bed", "spacing", "margin", "refill")
KEY = {"bed": nesting.bed, "margin": nesting.margin, "spacing": nesting.spacing, "refill": nesting.refill}
#: A use: key name and the index of its value.
Use = tuple[str, int]


def bindings(uses: tuple[Use, ...]) -> list[Binding[Any]]:
    return [KEY[k](VALUES[k][v]) for k, v in uses]


# -- the case -------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class BoardCase:
    #: -1: in the module itself, else its sub-scope.
    scope: int
    material: int
    nested: bool = True
    manual: bool = False
    uses: tuple[Use, ...] = ()


@dataclass(frozen=True)
class ModuleCase:
    #: Inside the first module (never the first).
    inside: bool
    scopes: int
    boards: tuple[BoardCase, ...]
    uses: tuple[Use, ...] = ()
    scope_uses: tuple[tuple[Use, ...], ...] = ()
    #: The module's uses from outside, after its block (`m.use()`).
    late: bool = False


@dataclass(frozen=True)
class NestDecl:
    module: int
    #: -1: on the module, else on its sub-scope.
    scope: int
    #: By material (its index), or None for boards named (module, board).
    material: int | None
    parts: tuple[tuple[int, int], ...] = ()
    uses: tuple[Use, ...] = ()
    #: A nest by material on a module, declared before its boards.
    early: bool = False


@dataclass(frozen=True)
class NestsCase:
    modules: tuple[ModuleCase, ...]
    nests: tuple[NestDecl, ...]
    root: tuple[Use, ...] = ()


@st.composite
def _uses(draw: st.DrawFn, often: float = 0.3) -> tuple[Use, ...]:
    out: list[Use] = []
    for key in ORDER:
        if draw(st.integers(0, 99)) < often * 100:
            out.append((key, draw(st.integers(0, len(VALUES[key]) - 1))))
    return tuple(out)


@st.composite
def nests_cases(draw: st.DrawFn) -> NestsCase:
    n = draw(st.integers(1, 4))
    modules: list[ModuleCase] = []
    for i in range(n):
        scopes = draw(st.integers(0, 2))
        boards = tuple(BoardCase(draw(st.integers(-1, scopes - 1)), draw(st.integers(0, len(MATS) - 1)),
                                 draw(st.integers(0, 4)) > 0, draw(st.integers(0, 12)) == 0, draw(_uses(0.1)))
                       for _ in range(draw(st.integers(1, 5))))
        modules.append(ModuleCase(i > 0 and draw(st.booleans()), scopes, boards, draw(_uses(0.25)),
                                  tuple(draw(_uses(0.15)) for _ in range(scopes)), draw(st.booleans())))
    case = NestsCase(tuple(modules), (), draw(_uses(0.5)))
    nests: list[NestDecl] = []
    for _ in range(draw(st.integers(0, 4))):
        i = draw(st.integers(0, n - 1))
        s = draw(st.integers(-1, modules[i].scopes - 1))
        if draw(st.booleans()):
            nests.append(NestDecl(i, s, draw(st.integers(0, len(MATS) - 1)), (), draw(_uses(0.3)),
                                  s == -1 and draw(st.booleans())))
        else:
            domain = _domain(case, i, s)
            if not domain:
                continue
            k = draw(st.integers(1, min(3, len(domain))))
            parts = tuple(draw(st.permutations(domain))[:k])
            nests.append(NestDecl(i, s, None, parts, draw(_uses(0.3))))
    return NestsCase(case.modules, tuple(nests), case.root)


def _domain(case: NestsCase, i: int, s: int) -> list[tuple[int, int]]:
    """The boards a nest on module i (or its sub-scope s) may name: those in
    it, and on the first module those of the modules inside it."""
    out = [(i, j) for j, b in enumerate(case.modules[i].boards) if s == -1 or b.scope == s]
    if s == -1 and i == 0:
        out += [(k, j) for k, m in enumerate(case.modules) if m.inside for j in range(len(m.boards))]
    return out


# -- the model ------------------------------------------------------------------------------------------

def module_path(case: NestsCase, i: int) -> str:
    return f"m0.m{i}" if case.modules[i].inside else f"m{i}"


def board_path(case: NestsCase, i: int, j: int) -> str:
    b = case.modules[i].boards[j]
    return module_path(case, i) + (f".s{b.scope}" if b.scope >= 0 else "") + f".b{j}"


def scope_path(case: NestsCase, i: int, s: int) -> str:
    return module_path(case, i) + (f".s{s}" if s >= 0 else "")


def _ordered(case: NestsCase, i: int) -> list[int]:
    """A module's boards in the order the build lists them: its own, then
    each sub-scope's."""
    boards = case.modules[i].boards
    return [j for s in range(-1, case.modules[i].scopes) for j, b in enumerate(boards) if b.scope == s]


def _nested(b: BoardCase) -> bool:
    return b.nested and not b.manual


def model_nests(case: NestsCase) -> tuple[dict[str, dict[str, Any]], str | None]:
    """The nests by path (module, by, material, parts), or the error the
    build must stop with: a manual board named first, then a board in two
    nests of one module."""
    out: dict[str, dict[str, Any]] = {}
    chosen = [_parts(case, decl) for decl in case.nests]
    error: str | None = None
    if any(case.modules[i].boards[j].manual for decl, parts in zip(case.nests, chosen) if decl.material is None
           for i, j in parts):
        error = "made by hand"
    elif any(a.module == b.module and set(pa) & set(pb) for k, (a, pa) in enumerate(zip(case.nests, chosen))
             for b, pb in list(zip(case.nests, chosen))[k + 1:]):
        error = "is in two nests of"
    # A board stays in its module's default nest unless a nest of that module takes it.
    named = {(i, j) for decl, parts in zip(case.nests, chosen) for i, j in parts if i == decl.module}
    for k, (decl, parts) in enumerate(zip(case.nests, chosen)):
        out[f"{scope_path(case, decl.module, decl.scope)}.n{k}"] = {
            "module": module_path(case, decl.module), "by": "material" if decl.material is not None else "parts",
            "material": MATS[decl.material].label if decl.material is not None else None,
            "parts": [board_path(case, i, j) for i, j in parts], "decl": k, "boards": parts}
    groups: dict[tuple[int, str], list[tuple[int, int]]] = {}
    for i in _module_order(case):
        for j in _ordered(case, i):
            b = case.modules[i].boards[j]
            if _nested(b) and (i, j) not in named:
                groups.setdefault((i, MATS[b.material].label), []).append((i, j))
    for (i, label), parts in groups.items():
        out[f"{module_path(case, i)}.{file_safe(label)}"] = {
            "module": module_path(case, i), "by": "default", "material": label,
            "parts": [board_path(case, a, b) for a, b in parts], "decl": None, "boards": parts}
    # Left out: the boards of a nest's module and material that are not nested and that no nest of
    # their module takes, in its scope for a nest by material.
    for n in out.values():
        n["left_out"] = []
        if n["by"] == "parts":
            continue
        decl = case.nests[n["decl"]] if n["decl"] is not None else None
        i = decl.module if decl is not None else next(k for k in range(len(case.modules))
                                                       if module_path(case, k) == n["module"])
        for j in _ordered(case, i):
            b = case.modules[i].boards[j]
            if (MATS[b.material].label == n["material"] and not _nested(b) and (i, j) not in named
                    and (decl is None or decl.scope == -1 or b.scope == decl.scope)):
                n["left_out"].append(board_path(case, i, j))
    return out, error


def _parts(case: NestsCase, decl: NestDecl) -> list[tuple[int, int]]:
    if decl.material is None:
        return list(decl.parts)
    return [(decl.module, j) for j in _ordered(case, decl.module)
            if (decl.scope == -1 or case.modules[decl.module].boards[j].scope == decl.scope)
            and _nested(case.modules[decl.module].boards[j])
            and case.modules[decl.module].boards[j].material == decl.material]


def _module_order(case: NestsCase) -> list[int]:
    """The modules in the build's order: each top-level one, the first
    followed by those inside it."""
    out: list[int] = []
    for i, m in enumerate(case.modules):
        if not m.inside:
            out.append(i)
            if i == 0:
                out += [k for k, mk in enumerate(case.modules) if mk.inside]
    return out


def _chain(case: NestsCase, i: int, s: int) -> list[tuple[tuple[Use, ...], str]]:
    """The uses along a scope's chain, nearest first, with their sources."""
    m = case.modules[i]
    chain = [(m.scope_uses[s], scope_path(case, i, s))] if s >= 0 else []
    chain.append((m.uses, module_path(case, i)))
    if m.inside:
        chain.append((case.modules[0].uses, "m0"))
    chain.append((case.root, "root"))
    return chain


def _lookup(chain: list[tuple[tuple[Use, ...], str]], key: str) -> tuple[Any, str]:
    for uses, source in chain:
        for k, v in uses:
            if k == key:
                return VALUES[k][v], source
    return DEFAULTS[key], "default"


def part_value(case: NestsCase, i: int, j: int, key: str) -> tuple[Any, str]:
    b = case.modules[i].boards[j]
    return _lookup([(b.uses, board_path(case, i, j))] + _chain(case, i, b.scope), key)


def model_values(case: NestsCase, path: str, nest: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
    """A nest's values (key -> (value, source), and `spacing` per part), or
    the key it is refused for."""
    own: dict[str, Any] = {}
    if nest["decl"] is not None:
        own = {k: VALUES[k][v] for k, v in case.nests[nest["decl"]].uses}
    out: dict[str, Any] = {}
    for key in ORDER:
        if key in own:
            out[key] = (own[key], path)
            if key == "spacing":
                out["part_spacing"] = {board_path(case, i, j): own[key] for i, j in nest["boards"]}
            continue
        given = [part_value(case, i, j, key) for i, j in nest["boards"]]
        source = ", ".join(dict.fromkeys(src for _v, src in given))
        if key == "spacing":
            out["part_spacing"] = {board_path(case, i, j): v for (i, j), (v, _s) in zip(nest["boards"], given)}
            out[key] = (min(v for v, _s in given), source)
            continue
        if len({repr(v) for v, _s in given}) > 1 or given[0][0] is None:
            return out, key
        out[key] = (given[0][0], source)
    return out, None


# -- building and checking ----------------------------------------------------------------------------

def build(case: NestsCase) -> dict[tuple[int, int], Board]:
    """The case as a build; returns its boards."""
    use(*bindings(case.root))
    made: dict[tuple[int, int], Board] = {}
    mods: dict[int, Scope] = {}
    subs: dict[tuple[int, int], Scope] = {}

    def one(i: int) -> None:
        m = case.modules[i]
        box = Box.from_size(width=600, depth=500, height=720, origin=(2000.0 * i, 0, 0))
        with module(f"m{i}", box) as mod:
            uncheck(no_interference)
            if not m.late:
                use(*bindings(m.uses))
            for k, decl in enumerate(case.nests):
                if decl.early and decl.module == i:
                    _declare(case, k, mod, made)
            for s in range(m.scopes):
                with scope(f"s{s}") as sub:
                    use(*bindings(m.scope_uses[s]))
                subs[(i, s)] = sub
            for j, b in enumerate(m.boards):
                with subs[(i, b.scope)] if b.scope >= 0 else nullcontext():
                    made[(i, j)] = part = board(f"b{j}", MATS[b.material]).on(mod.bottom)
                if b.manual:
                    part.manual()
                if not b.nested:
                    part.nest(False)
                if b.uses:
                    part.use(*bindings(b.uses))
            if i == 0:
                for k, mk in enumerate(case.modules):
                    if mk.inside:
                        one(k)
        if m.late:
            mod.use(*bindings(m.uses))
        mods[i] = mod

    for i, m in enumerate(case.modules):
        if not m.inside:
            one(i)
    for k, decl in enumerate(case.nests):
        if not decl.early:
            target = mods[decl.module] if decl.scope < 0 else subs[(decl.module, decl.scope)]
            _declare(case, k, target, made)
    return made


#: The nests the last build declared, by their index in the case.
_declared: dict[int, Any] = {}


def _declare(case: NestsCase, k: int, target: Scope, made: dict[tuple[int, int], Board]) -> None:
    decl = case.nests[k]
    if decl.material is not None:
        nest = target.nest(f"n{k}", material=MATS[decl.material])
    else:
        nest = target.nest(f"n{k}", [made[p] for p in decl.parts])
    nest.use(*bindings(decl.uses))
    _declared[k] = nest


def nests_problems(case: NestsCase) -> list[str]:
    with fresh():
        _declared.clear()
        build(case)
        want, error = model_nests(case)
        try:
            layout = build_layout()
        except LangError as e:
            if error is None:
                return [f"the layout refused: {e}"]
            return [] if error in str(e) else [f"refused for another reason than the model's ({error}): {e}"]
        if error is not None:
            return [f"not refused, though the model says {error!r}"]
        return _compare(case, layout, want)


def _compare(case: NestsCase, layout: Layout, want: dict[str, dict[str, Any]]) -> list[str]:
    problems: list[str] = []
    got = {n["path"]: n for n in nests_of(layout)}
    if set(got) != set(want):
        return [f"the nests are {sorted(got)}, the model's {sorted(want)}"]
    for path, w in want.items():
        g = got[path]
        for field in ("module", "by", "material", "parts", "left_out"):
            if g[field] != w[field]:
                problems.append(f"{path}: its {field} is {g[field]!r}, the model's {w[field]!r}")
        if not w["parts"]:
            if f"{path}: no board to nest" not in layout["problems"]:
                problems.append(f"{path}: takes nothing and says nothing")
            continue
        values, refused = model_values(case, path, w)
        try:
            r = resolve(layout, nest_of(layout, path))
        except LangError as e:
            if refused is None:
                problems.append(f"{path}: refused ({e}), the model gives values")
            elif f"nesting.{refused}" not in str(e):
                problems.append(f"{path}: refused for another key than {refused}: {e}")
            continue
        if refused is not None:
            problems.append(f"{path}: not refused, though its parts give no one {refused}")
            continue
        for key in ORDER:
            value, source = values[key]
            gv = r.values[f"nesting.{key}"]
            gv = tuple(gv) if isinstance(gv, list) else gv
            if gv != value or r.sources[f"nesting.{key}"] != source:
                problems.append(f"{path}: {key} {gv!r} from {r.sources[f'nesting.{key}']!r}, the model's {value!r} "
                                f"from {source!r}")
        if r.spacing != values["part_spacing"]:
            problems.append(f"{path}: the parts' spacings {r.spacing}, the model's {values['part_spacing']}")
    for k, nest in _declared.items():
        decl = case.nests[k]
        own = {key: VALUES[key][v] for key, v in decl.uses}
        for key in ORDER:
            want_value = own.get(key, _lookup(_chain(case, decl.module, decl.scope), key)[0])
            try:
                got_value = nest.value(KEY[key])
            except LangError:
                got_value = None
            if got_value != want_value:
                problems.append(f"{nest.path}: value({key}) {got_value!r}, the model's {want_value!r}")
    return problems


# -- inventories ----------------------------------------------------------------------------------------

LEDGER_MATS = (sheet_material("birch", t=15, size=(2500, 1250)), sheet_material("birch", t=9))
#: The labels an inventory names: the build's two, and one it does not have.
LABELS = ("birch 15", "birch 9", "oak 20")


@dataclass(frozen=True)
class LedgerCase:
    #: Label index, length, width, count (None: not given, 1).
    entries: tuple[tuple[int, float, float, int | None], ...]
    #: Module (0 or 1), material (0: with a size, 1: without), length, width.
    parts: tuple[tuple[int, int, float, float], ...]


@st.composite
def ledger_cases(draw: st.DrawFn) -> LedgerCase:
    entry = st.tuples(st.integers(0, len(LABELS) - 1), sizes(200, 2600), sizes(200, 1300),
                      st.one_of(st.none(), st.integers(1, 3)))
    part = st.tuples(st.integers(0, 1), st.integers(0, 1), sizes(60, 600), sizes(60, 600))
    return LedgerCase(tuple(draw(st.lists(entry, max_size=4))), tuple(draw(st.lists(part, min_size=1, max_size=4))))


def _toml(case: LedgerCase) -> str:
    out: list[str] = []
    for m, length, width, count in case.entries:
        out += ["[[stock]]", f'material = "{LABELS[m]}"', f"size = [{length!r}, {width!r}]"]
        if count is not None:
            out.append(f"count = {count}")
    return "\n".join(out) + "\n"


def ledger_problems(case: LedgerCase, folder: Path | None = None) -> list[str]:
    import tempfile
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(folder or tmp) / "inventory.toml"
        path.write_text(_toml(case))
        inventory = read_inventory(path)
    want = [OnHand(LABELS[m], length, width, 1 if count is None else count) for m, length, width, count in case.entries]
    if inventory != want:
        return [f"read back as {inventory}, written {want}"]
    with fresh():
        use(nesting.bed((2000, 1000)), nesting.refill(False))
        for k in range(2):
            with module(f"p{k}", Box.from_size(width=600, depth=500, height=720, origin=(3000.0 * k, 0, 0))):
                uncheck(no_interference)
                for n, (mod, mat, length, width) in enumerate(case.parts):
                    if mod == k:
                        free = Box.from_size(width=width, depth=length, height=20, origin=(3000.0 * k, 600.0 * n, 0))
                        board(f"b{n}", LEDGER_MATS[mat]).on(free.bottom).between(free.front, free.back, free.left,
                                                                                    free.right)
        layout = build_layout()
        left = list(inventory)
        for nest in nests_of(layout):
            label = nest["material"]
            assert label is not None                    # the default nests, one material each
            sized = label == LEDGER_MATS[0].label
            on_hand = Counter({o.label(): o.count for o in left if o.material == label})
            try:
                result, _parts = nest_layout(layout, nest["path"], left,
                                             options=Options(seconds=0.2, saw_seconds=0.05, refill_seconds=0))
            except LangError as e:
                if "cannot be nested" in str(e) and not sized and _misfit(case, nest["parts"], left, label):
                    continue
                if sized or on_hand:
                    problems.append(f"{nest['path']}: refused ({e}), though it has {'a size' if sized else on_hand}")
                elif "no sheet size to buy" not in str(e):
                    problems.append(f"{nest['path']}: refused for another reason: {e}")
                continue
            if not sized and not on_hand:
                problems.append(f"{nest['path']}: nested with nothing to buy or on hand")
            ws = workshop_of(layout, nest, resolve(layout, nest), left)
            if ws.on_hand != tuple(o for o in left if o.material == label):
                problems.append(f"{nest['path']}: given {ws.on_hand} on hand, not its material's of {left}")
            (m,) = result["materials"]
            if (sized and any(size != "2500x1250" for size in m["bought"])) or (not sized and m["bought"]):
                problems.append(f"{nest['path']}: bought {m['bought']}")
            if Counter(m["on_hand_used"]) - on_hand:
                problems.append(f"{nest['path']}: used {m['on_hand_used']} of {dict(on_hand)} on hand")
            if m["unplaced"] and sized:
                problems.append(f"{nest['path']}: parts left over though sheets are to be bought")
            if m["unplaced"] and "left over" not in " ".join(result["problems"]):
                problems.append(f"{nest['path']}: parts left over and not said")
            after = used_up(left, result)
            for o in {(o.material, o.label()) for o in left}:
                before_n = sum(x.count for x in left if (x.material, x.label()) == o)
                after_n = sum(x.count for x in after if (x.material, x.label()) == o)
                used = Counter(m["on_hand_used"])[o[1]] if o[0] == label else 0
                if after_n != before_n - used:
                    problems.append(f"{nest['path']}: {o} left {after_n}, {before_n} less {used} used")
            left = after
    return problems


def _misfit(case: LedgerCase, paths: list[str], left: list[OnHand], label: str) -> bool:
    """Whether one of the parts may fit no piece on hand (with its margins of
    10 mm, give or take the solver polygon's growth, and the bed)."""
    pieces = [(o.length, o.width) for o in left if o.material == label]
    for path in paths:
        _mod, _mat, length, width = case.parts[int(path.rsplit(".b", 1)[1])]
        if not any(min(a, 2000) >= x + 22 and min(b, 1000) >= y + 22 for a, b in pieces
                   for x, y in ((length, width), (width, length))):
            return True
    return False


__all__ = ["NestsCase", "nests_cases", "nests_problems", "LedgerCase", "ledger_cases", "ledger_problems"]
