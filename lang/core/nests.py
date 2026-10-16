"""Nests declared in the build (`Scope.nest`, `design/nesting.md`): which
boards go onto the machine together. Each nest is a node of the settings'
chain under the scope it is declared on, for its own values
(`carcass.use(nesting.margin(15))`).

A nest is declared on a module or a scope: `cab.nest("carcass",
material=ply15)` takes the nested boards of that material in it, its
sub-scopes' too but not those of a module inside it, which has nests of
its own; `cab.nest("fronts", [front1, front2])` the boards named, anywhere
inside it, so a root module's nest may name boards of several modules (a
remake), and a `nest(False)` board named is its own blank, sawn to size.
Its name is unique in its module and holds no dot or path separator; its
path is the scope's and its name (`kitchen.carcass`). A board is in one
nest of its module at most.

What no declared nest of its module takes makes one nest per material per
module, named after the material's label made file-safe
(`kitchen.birch_15`): a build that declares none nests each module's
boards by material, and a board a nest around its module names (a remake)
stays in its module's nest too. Its module is the innermost module around
a board (a top-level scope that is no module counts as one; boards outside
every scope make the root's, `birch_15`).

The layout step resolves the selections (`layout_nests`) and writes each
module's nests, declared and default, with their parts' paths and the
nest's own settings; the nest step reads them there (`lang.nesting`).
"""
from __future__ import annotations

import re
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Self, TypeVar

from . import keys
from .errors import LangError
from .layout_types import NestLayout
from .material import SheetMaterial
from .settings import Binding, Node, Setting

from .scope import Scope

if TYPE_CHECKING:
    from .part import Board

T = TypeVar("T")

#: What a nest's name may not hold: it is a part of its path, and a folder.
_NOT_IN_NAME = re.compile(r"[./\\]")


class Nest:
    """A nest declared on a scope (`Scope.nest`): its boards, chosen by
    material or by name, and its node of the settings' chain."""

    def __init__(self, scope: Scope, name: str, material: SheetMaterial | None, named: list[Board] | None):
        self.scope = scope
        self.name = name
        #: The material whose nested boards it takes, or None for boards named.
        self.material = material
        self._named = named
        #: The nest's node of the settings' chain, under its scope's.
        self.settings = Node(lambda: self.path, lambda: scope.settings, lambda: scope.frame)

    @property
    def path(self) -> str:
        return f"{self.scope.path}.{self.name}"

    @property
    def parts(self) -> list[Board]:
        """Its boards as the build stands now: those named, or the nested
        boards of its material in its scope (`own_boards`)."""
        if self._named is not None:
            return list(self._named)
        assert self.material is not None
        label = self.material.label
        return [b for b in own_boards(self.scope) if nested(b) and b.material.label == label]

    def use(self, *bindings: Binding[Any]) -> Self:
        """Uses settings on the nest, for the nest step: `carcass.use(nesting.
        margin(15), nesting.seconds(120))`, another bed for a nest cut on
        another machine. A nest's own value comes before its parts'. The
        boards' `material`, `grain` and `nest` are theirs, not a nest's."""
        for binding in bindings:
            key = getattr(binding, "key", None)
            spelling = keys.OWN_SPELLING.get(key) if key is not None else None
            if key is not None and spelling is not None:
                raise LangError(f"use({binding!r}) on a nest: {key.name} is a board's, said on the board "
                                f"({spelling}) or in its scope.", self.path)
        self.settings.use(*bindings)
        return self

    def value(self, key: Setting[T]) -> T:
        """The value of a setting as the nest sees it: its own, else its
        scope's and those above, else the key's default. (The nest step
        reads its parts' too: `lang.nesting.resolve`.)"""
        return self.settings.read(key, self.path)[0]

    def __repr__(self) -> str:
        return f"Nest({self.path})"


def declare(scope: Scope, name: object, parts: object, material: object) -> Nest:
    """`scope.nest(name, parts)` or `scope.nest(name, material=...)`, checked."""
    if not isinstance(name, str) or not name.strip() or name != name.strip() or _NOT_IN_NAME.search(name):
        raise LangError(f"nest({name!r}): a nest's name is a word for a folder, with no dot, slash or space at "
                        "its ends, as nest('carcass', material=ply15).", scope.path)
    what = f"nest({name!r})"
    if (parts is None) == (material is None):
        raise LangError(f"{what}: give either its material (nest({name!r}, material=ply15)) or its boards "
                        f"(nest({name!r}, [front1, front2])), {'not both' if parts is not None else 'one of them'}.",
                        scope.path)
    module = home(scope)
    other = next((s.nests_declared[name] for s in _own_scopes(module) if name in s.nests_declared), None)
    if other is not None:
        raise LangError(f"{what}: {module.path} has a nest of that name already, {other.path}.", scope.path)
    if material is not None:
        nest = Nest(scope, name, keys.sheet_material(material, what), None)
    else:
        nest = Nest(scope, name, None, _named(scope, what, parts))
    scope.nests_declared[name] = nest
    return nest


def _named(scope: Scope, what: str, parts: object) -> list[Board]:
    from .part import Board
    if not isinstance(parts, (list, tuple)):
        raise LangError(f"{what}: give its boards as a list, [front1, front2], not {parts!r}.", scope.path)
    boards: list[Board] = []
    prefix = scope.path + "."
    for part in parts:  # pyright: ignore[reportUnknownVariableType]
        if not isinstance(part, Board):
            raise LangError(f"{what}: {part!r} is not a board.", scope.path)
        if part.kind == "slat":
            raise LangError(f"{what}: {part.path} is a slat; slats are not nested, they go on the cut list by "
                            "length.", scope.path)
        if not part.path.startswith(prefix):
            raise LangError(f"{what}: {part.path} is not in {scope.path}; a nest names boards of its scope, and a "
                            "nest of the root module those of every module in it.", scope.path)
        if any(b is part for b in boards):
            raise LangError(f"{what}: {part.path} is named twice.", scope.path)
        boards.append(part)
    if not boards:
        raise LangError(f"{what}: name at least one board.", scope.path)
    return boards


# -- which boards ------------------------------------------------------------------------------

def nested(board: Board) -> bool:
    """Whether a board goes into its material's nest: a board (not a slat),
    not made by hand, its `nest` setting True."""
    return board.kind == "board" and not board.manual_part and board.nested


def own_boards(scope: Scope) -> list[Board]:
    """A scope's boards and its sub-scopes', not those of a module inside it."""
    out = list(scope.parts.values())
    for child in scope.children.values():
        if not child.is_module:
            out += own_boards(child)
    return out


def _own_scopes(scope: Scope) -> list[Scope]:
    """A scope and its sub-scopes, not a module inside it or its scopes."""
    return [scope] + [s for child in scope.children.values() if not child.is_module for s in _own_scopes(child)]


def home(scope: Scope) -> Scope:
    """The module a scope's nests and boards belong to: the innermost
    module at or around it, else its top-level scope."""
    while not scope.is_module and scope.parent is not None:
        scope = scope.parent
    return scope


def _module_of(board: Board) -> str:
    """The path of the module a board belongs to, "" outside every scope."""
    scope = board.scope
    return home(scope).path if isinstance(scope, Scope) else ""


def file_safe(label: str) -> str:
    """A material's label as a default nest's name: `birch 15` is
    `birch_15`, `birch 1.5` `birch_1_5`."""
    return re.sub(r"[^A-Za-z0-9_-]+", "_", label).strip("_") or "material"


def layout_nests(roots: Sequence[Scope], loose: Sequence[Board]) -> dict[str, list[NestLayout]]:
    """Every nest of the build by the path of the top-level scope it is in
    ("" for the boards outside every scope): the nests declared, in the
    order of their scopes and declarations, then a default nest per module
    and material for the nested boards no declared nest of their module
    takes (a nest around the module, a remake, may name them again). A
    board in two nests of one module, a manual board named, and a default
    nest's name taken by a declared one are errors."""
    declared: list[tuple[Scope, Nest, list[Board]]] = []
    for root in roots:
        for scope in _scopes(root):
            for nest in scope.nests_declared.values():
                parts = nest.parts
                for b in parts:
                    if b.manual_part:
                        raise LangError(f"{nest.path} names {b.path}, which is made by hand (manual()) and not "
                                        "nested.", nest.path)
                declared.append((root, nest, parts))
    taken: dict[tuple[int, int], Nest] = {}           # (module, board) -> nest
    for _root, nest, parts in declared:
        module = home(nest.scope)
        for b in parts:
            other = taken.setdefault((id(module), id(b)), nest)
            if other is not nest:
                raise LangError(f"{b.path} is in two nests of {module.path}, {other.path} and {nest.path}; a board "
                                "is in one nest of its module.", nest.path)
    out: dict[str, list[NestLayout]] = {root.path: [] for root in roots}
    paths: dict[str, str] = {}
    for root, nest, parts in declared:
        out[root.path].append(_record(nest.path, home(nest.scope).path, "material" if nest.material else "parts",
                                      nest.material.label if nest.material else None, parts,
                                      nest.settings.own_layout()))
        paths[nest.path] = "declared"
    # The default nests: per module and material, in the build's order.
    groups: dict[tuple[str, str], tuple[str, list[Board]]] = {}
    for root, boards in [(r.path, r.all_parts()) for r in roots] + [("", list(loose))]:
        for b in boards:
            if not nested(b) or _taken_at_home(b, taken):
                continue
            module = _module_of(b)
            groups.setdefault((module, b.material.label), (root, []))[1].append(b)
    for (module, label), (root, boards) in groups.items():
        path = f"{module}.{file_safe(label)}" if module else file_safe(label)
        if path in paths:
            raise LangError(f"{path} is the name of the nest of {module or 'the root'}'s {label} boards that no "
                            f"nest names, and of {'a nest declared' if paths[path] == 'declared' else 'another'}; "
                            "give the declared nest another name.", path)
        paths[path] = label
        out.setdefault(root, []).append(_record(path, module, "default", label, boards, {}))
    _left_out(out, roots, loose, taken, declared)
    return {root: nests for root, nests in out.items() if nests or root}


def _taken_at_home(board: Board, taken: dict[tuple[int, int], Nest]) -> bool:
    """Whether a declared nest of the board's own module takes it."""
    scope = board.scope
    return isinstance(scope, Scope) and (id(home(scope)), id(board)) in taken


def _scopes(scope: Scope) -> list[Scope]:
    return [scope] + [s for child in scope.children.values() for s in _scopes(child)]


def _record(path: str, module: str, by: str, material: str | None, parts: list[Board],
            settings: dict[str, Any]) -> NestLayout:
    return {"path": path, "module": module, "by": by, "material": material,  # pyright: ignore[reportReturnType]
            "parts": [b.path for b in parts], "left_out": [], "settings": settings}


def _left_out(out: dict[str, list[NestLayout]], roots: Sequence[Scope], loose: Sequence[Board],
              taken: dict[tuple[int, int], Nest], declared: list[tuple[Scope, Nest, list[Board]]]) -> None:
    """Lists each board of a sheet material that no nest of its module
    takes (`nest(False)`, manual) with the nests of its module and material
    that choose by material and whose scope holds it, so a nest's file says
    what of its kind stayed out."""
    by_path = {n["path"]: n for nests in out.values() for n in nests}
    domains = [(nest, home(nest.scope).path, {id(b) for b in own_boards(nest.scope)})
               for _root, nest, _parts in declared if nest.material is not None]
    for b in [b for r in roots for b in r.all_parts()] + list(loose):
        if b.kind != "board" or nested(b) or _taken_at_home(b, taken):
            continue
        label = b.material.label
        module = _module_of(b)
        for nest, nest_module, domain in domains:
            assert nest.material is not None
            if nest.material.label == label and nest_module == module and id(b) in domain:
                by_path[nest.path]["left_out"].append(b.path)
        default = f"{module}.{file_safe(label)}" if module else file_safe(label)
        if default in by_path and by_path[default]["by"] == "default":
            by_path[default]["left_out"].append(b.path)
