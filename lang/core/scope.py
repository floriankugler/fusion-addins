"""Scopes and modules: namespaces of parts with a path and a box.

A module is a scope with a box that compiles into its own document. Parts
register in the current scope under their name; `scope.name` returns the
part or child scope. The registry collects the root modules of a build.
"""
from __future__ import annotations

from typing import Any

from .box import Box
from .errors import LangError

_stack: list["Scope"] = []


class Registry:
    def __init__(self):
        self.roots: list[Scope] = []
        self.root_parts: list = []

    def reset(self) -> None:
        self.roots.clear()
        self.root_parts.clear()
        _stack.clear()


registry = Registry()


class _Root:
    """The implicit scope outside any `with module()`: no box, no path."""
    path = ""
    box = None
    default_grain = None
    is_module = False

    def _register(self, part) -> None:
        registry.root_parts.append(part)


_root = _Root()


def current():
    return _stack[-1] if _stack else _root


class Scope:
    def __init__(self, name: str, box: Box | None = None, is_module: bool = False):
        if not name or "." in name:
            raise LangError(f"Scope name {name!r} must be non-empty and contain no dots.")
        self.name = name
        self.parent = _stack[-1] if _stack else None
        self.is_module = is_module
        self._box = box
        self.parts: dict[str, Any] = {}
        self.children: dict[str, Scope] = {}
        self.exports: dict[str, Any] = {}
        self.checks: list = []
        self.problems: list[str] = []
        self.default_grain: str | None = None
        if self.parent is not None:
            self.parent._register_child(self)
        else:
            registry.roots.append(self)

    # -- identity ----------------------------------------------------------

    @property
    def path(self) -> str:
        if self.parent is None:
            return self.name
        return f"{self.parent.path}.{self.name}"

    @property
    def box(self) -> Box | None:
        if self._box is not None:
            return self._box
        return self.parent.box if self.parent is not None else None

    def center(self, axis_or_name: str):
        return self._need_box("center").center(axis_or_name)

    def extent(self, axis_or_name: str) -> float:
        return self._need_box("extent").extent(axis_or_name)

    def _need_box(self, what: str) -> Box:
        if self.box is None:
            raise LangError(f"{what}: this scope has no box.", self.path)
        return self.box

    @property
    def interior(self) -> Box:
        """The box inside the parts placed on its sides: for each side, the
        inner face of a board lying on it, else the side itself."""
        b = self.box
        if b is None:
            raise LangError("interior: this scope has no box.", self.path)
        inner = b
        for part in self.parts.values():
            pb = part.box()
            t = part.t_axis
            if abs(pb.lo[t] - b.lo[t]) < 1e-9 and pb.hi[t] < b.hi[t]:
                inner = inner.with_side(_direction(t, -1), max(inner.lo[t], pb.hi[t]))
            elif abs(pb.hi[t] - b.hi[t]) < 1e-9 and pb.lo[t] > b.lo[t]:
                inner = inner.with_side(_direction(t, 1), min(inner.hi[t], pb.lo[t]))
        return inner

    # -- registration --------------------------------------------------------

    def _register(self, part) -> None:
        if part.name in self.parts or part.name in self.children:
            raise LangError(f"name {part.name!r} already used in this scope.", self.path)
        self.parts[part.name] = part

    def _register_child(self, child: "Scope") -> None:
        if child.name in self.parts or child.name in self.children:
            raise LangError(f"name {child.name!r} already used in this scope.", self.path)
        self.children[child.name] = child

    def __getattr__(self, name: str):
        """Direction names are the box's sides (`cab.left`), since carcass
        parts are usually named after directions too; such parts are
        reached with `cab["left"]`. Other names resolve to parts, child
        scopes and exports."""
        if name.startswith("_"):
            raise AttributeError(name)
        from . import directions
        if directions.frame.is_direction(name):
            box = self.box
            if box is None:
                raise AttributeError(f"{self.path!r} has no box, so no side {name!r}; a part of that name is {self.path}[{name!r}].")
            return box.side(name)
        if name in directions.frame.extents:
            return self._need_box(name).extent(name)
        parts = self.__dict__.get("parts", {})
        if name in parts:
            return parts[name]
        children = self.__dict__.get("children", {})
        if name in children:
            return children[name]
        exports = self.__dict__.get("exports", {})
        if name in exports:
            return exports[name]
        raise AttributeError(f"{self.path!r} has no part, scope or export named {name!r}.")

    def __getitem__(self, name: str):
        """A part or child scope by name, also for names that are directions."""
        if name in self.parts:
            return self.parts[name]
        if name in self.children:
            return self.children[name]
        raise KeyError(f"{self.path!r} has no part or scope named {name!r}.")

    def all_parts(self) -> list:
        out = list(self.parts.values())
        for child in self.children.values():
            out.extend(child.all_parts())
        return out

    # -- API -----------------------------------------------------------------

    def export(self, name: str, value) -> "Scope":
        if name in self.parts or name in self.children:
            raise LangError(f"export {name!r} collides with a part or scope name.", self.path)
        self.exports[name] = value
        return self

    def check(self, *checks) -> "Scope":
        self.checks.extend(checks)
        return self

    def run_checks(self) -> list[str]:
        self.problems = []
        for fn in self.checks:
            self.problems.extend(fn(self))
        for child in self.children.values():
            self.problems.extend(child.run_checks())
        return self.problems

    # -- context manager -----------------------------------------------------

    def __enter__(self) -> "Scope":
        _stack.append(self)
        return self

    def __exit__(self, *exc) -> None:
        popped = _stack.pop()
        assert popped is self

    def __repr__(self) -> str:
        return f"Scope({self.path})"


def _direction(axis: str, sign: int):
    from . import directions
    return directions.frame.direction_of(axis, sign)


def module(name: str, box: Box) -> Scope:
    """A module: a scope with a box that compiles into its own document."""
    if box is None:
        raise LangError("module() needs a box.", name)
    return Scope(name, box, is_module=True)


def scope(name: str, box: Box | None = None) -> Scope:
    """A sub-scope. Without a box it inherits the enclosing one."""
    return Scope(name, box)


def check(*checks) -> None:
    """Registers checks on the current scope."""
    cur = current()
    if cur is _root:
        raise LangError("check() outside any module.")
    cur.check(*checks)
