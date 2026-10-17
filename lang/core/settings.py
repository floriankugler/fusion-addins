"""Settings: typed values that flow down the build (`design/api.md`,
Settings).

A key is a `Setting`, made by `setting(default, name)` where the code that
reads it lives; `setting(..., name)` makes one without a default, which is
an error to read where nothing uses it. A key called with a value is a
`Binding` (`chamfer_size(0.5)`), which a node of the build uses: a scope
(`use()` in its `with` block, `cab.use()` on one in hand), a part or a
named operation (`.use()`), or the root, outside every module. A reader
takes the value nearest to it along its chain, the operation, the part,
its scopes innermost first, the root, then the key's default
(`value(key)`, `part.value(key)`).

A node uses a key once. A key read during the build freezes for the nodes
the read passed through: using it on one of them afterwards would change
what was read after the fact, so it is an error naming the reader and the
line that read it [proposed in `design/proposals/settings.md`, Freezing].
A key nothing reads during the build (`nest`, `grain`) is never frozen.

This module holds the mechanism only: `scope.py` gives scopes and the root
their nodes and has `use()` and `value()`, `part.py` gives parts and named
operations theirs and defines the core's keys.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from types import EllipsisType
from typing import Any, Generic, TypeVar, cast

from .directions import Frame
from .errors import LangError
from .layout_types import JsonValue, SettingLayout
from .where import build_line

T = TypeVar("T")


class Setting(Generic[T]):
    """A key: a typed value with a name and, unless it was made with `...`,
    a default. Call it with a value to make a binding: `chamfer_size(0.5)`.

    `check` takes a value as a build file gives it and returns it as the
    key holds it, or raises a LangError; `to_layout` gives the value as the
    layout writes it, in the frame of the node that set it, or None to
    leave it out (by default a value that is JSON data is written as it
    is, anything else is left out); `hint` names the call that sets the key
    for one node, for the error of a key without a default ("chamfer(what,
    size) gives a chamfer its own, or ")."""

    def __init__(self, default: T | EllipsisType, name: str, *, check: Callable[[object, str], T] | None = None,
                 to_layout: Callable[[T, Frame], JsonValue | None] | None = None, hint: str = "",
                 source: str = "default"):
        if not name:
            raise LangError("setting(): a key needs a name, e.g. setting(3.0, 'drawer_gap').")
        self.name = name
        self._check = check
        self._to_layout = to_layout
        self.hint = hint
        #: Where the default comes from, as provenance names it: "default",
        #: or "master: Spalt" for a parameter of the master.
        self.source = source
        self._default: T | EllipsisType = ... if default is ... else self.checked(default, f"setting({name!r})")

    @property
    def has_default(self) -> bool:
        return self._default is not ...

    @property
    def default(self) -> T:
        if self._default is ...:
            raise LangError(f"setting {self.name!r} has no default.")
        return self._default

    def checked(self, value: object, what: str) -> T:
        """The value as the key holds it, or a LangError naming `what`."""
        return self._check(value, what) if self._check is not None else cast(T, value)

    def layout_value(self, value: T, frame: Frame) -> JsonValue | None:
        if self._to_layout is not None:
            return self._to_layout(value, frame)
        return cast(JsonValue, value) if is_json(value) else None

    def __call__(self, value: T) -> Binding[T]:
        return Binding(self, self.checked(value, f"{self.name}()"), build_line())

    def __repr__(self) -> str:
        return f"setting({self.name!r})"


def setting(default: T | EllipsisType, name: str, *, check: Callable[[object, str], T] | None = None,
            to_layout: Callable[[T, Frame], JsonValue | None] | None = None, hint: str = "") -> Setting[T]:
    """A key with a default, `drawer_gap = setting(3.0, "drawer_gap")`, or
    without one, `setting(..., "front_gap")`, typed by its annotation
    (`front_gap: Setting[float] = setting(..., "front_gap")`): then reading
    it where no node uses it is an error. Define it where the code that
    reads it lives; its name is what errors and the layout call it."""
    return Setting(default, name, check=check, to_layout=to_layout, hint=hint)


@dataclass(frozen=True)
class Binding(Generic[T]):
    """A key with a value (`chamfer_size(0.5)`), for `use()`; `where` is the
    build line that made it."""
    key: Setting[T]
    value: T
    where: str

    def __repr__(self) -> str:
        return f"{self.key.name}({self.value!r})"


@dataclass(frozen=True)
class _Read:
    """A read that passed through a node: who read the key, and where."""
    reader: str
    where: str


@dataclass(frozen=True)
class _Bound:
    value: object
    where: str


class Node:
    """The settings of one node of the build's chain: what it uses, and the
    reads that passed through it, which freeze those keys for it. `label`
    is what provenance and errors call the node, `parent` the next node up
    (None at the root), `frame` the frame its extent names are read in;
    each is asked when needed, since a part's path is known only once it
    is registered."""

    def __init__(self, label: Callable[[], str], parent: Callable[[], Node | None], frame: Callable[[], Frame]):
        self._label = label
        self._parent = parent
        self._frame = frame
        self._bound: dict[Setting[Any], _Bound] = {}
        self._frozen: dict[Setting[Any], _Read] = {}
        #: The keys read with this node as the reader, in order.
        self.read_keys: list[Setting[Any]] = []

    @property
    def label(self) -> str:
        return self._label()

    @property
    def parent(self) -> Node | None:
        return self._parent()

    @property
    def frame(self) -> Frame:
        return self._frame()

    def chain(self) -> list[Node]:
        """This node and those above it, nearest first."""
        out: list[Node] = []
        node: Node | None = self
        while node is not None:
            out.append(node)
            node = node.parent
        return out

    def use(self, *bindings: Binding[Any]) -> None:
        """Uses bindings on this node, all or none: each key once, and not
        after a read that passed through here."""
        given: dict[Setting[Any], Binding[Any]] = {}
        for binding in bindings:
            if not isinstance(binding, Binding):    # pyright: ignore[reportUnnecessaryIsInstance] - build files are not checked
                raise LangError(f"use() takes bindings, a key called with a value such as chamfer_size(0.5); not "
                                f"{binding!r}.", self.label)
            key = binding.key
            first = self._bound.get(key)
            where = first.where if first is not None else given[key].where if key in given else None
            if where is not None:
                raise LangError(f"{key.name} used twice on {self.label} (first at {where}); a node uses a "
                                "setting once.")
            read = self._frozen.get(key)
            if read is not None:
                raise LangError(f"{binding!r} on {self.label} comes after {read.reader} read {key.name}, at "
                                f"{read.where}; what was read there would no longer hold. Use it before that "
                                "line.")
            given[key] = binding
        for key, binding in given.items():
            self._bound[key] = _Bound(binding.value, binding.where)

    def own(self, key: Setting[T]) -> T | None:
        """What this node itself uses for `key`, or None."""
        bound = self._bound.get(key)
        return cast(T, bound.value) if bound is not None else None

    def uses(self, key: Setting[Any]) -> bool:
        return key in self._bound

    def bound_keys(self) -> list[Setting[Any]]:
        return list(self._bound)

    def lookup(self, key: Setting[T]) -> tuple[T, Node | None]:
        """The value for `key` along the chain from here and the node that
        set it (None for the default), without reading it: it freezes
        nothing. A key without a default and set nowhere is a LangError."""
        found = self._find(key)
        if found is not None:
            return cast(T, found._bound[key].value), found
        return key.default, None

    def read(self, key: Setting[T], reader: str) -> tuple[T, Node | None]:
        """Reads `key` for `reader` (what errors call it: a part's path, "the
        chamfer of kitchen.left"), from this node up, freezing it on every
        node the read passed through; returns the value and the node that
        set it (None for the default). A key without a default and set
        nowhere is a LangError naming the key and how to set it."""
        found = self._find(key)
        if found is None and not key.has_default:
            raise LangError(f"{reader} reads {key.name}, which has no default and is set nowhere above it; "
                            f"{key.hint}use({key.name}(...)) in a scope above sets it for everything in it.")
        read = _Read(reader, build_line())
        node: Node | None = self
        while node is not None and node is not found:
            node._frozen.setdefault(key, read)
            node = node.parent
        if key not in self.read_keys:
            self.read_keys.append(key)
        if found is not None:
            return cast(T, found._bound[key].value), found
        return key.default, None

    def _find(self, key: Setting[Any]) -> Node | None:
        node: Node | None = self
        while node is not None:
            if key in node._bound:
                return node
            node = node.parent
        return None

    def to_layout(self, skip: Callable[[Setting[Any]], bool] = lambda key: False) -> dict[str, SettingLayout]:
        """The keys set along the chain from here, each with its value and
        the node that set it, and the keys read here whose default came
        from somewhere ("master: Spalt"); keys `skip` names and values the
        layout does not take (`Setting.layout_value`) are left out."""
        out: dict[str, SettingLayout] = {}
        seen: set[Setting[Any]] = set()
        for node in self.chain():
            for key, bound in node._bound.items():
                if key in seen or skip(key):
                    continue
                seen.add(key)
                value = key.layout_value(bound.value, node.frame)
                if value is not None:
                    out[key.name] = {"value": value, "source": node.label}
        for key in self.read_keys:
            if key in seen or skip(key) or not key.has_default or key.source == "default":
                continue
            value = key.layout_value(key.default, self.frame)
            if value is not None:
                out[key.name] = {"value": value, "source": key.source}
        return dict(sorted(out.items()))

    def own_layout(self) -> dict[str, SettingLayout]:
        """The keys this node itself uses, as `to_layout` writes them."""
        out: dict[str, SettingLayout] = {}
        for key, bound in self._bound.items():
            value = key.layout_value(bound.value, self.frame)
            if value is not None:
                out[key.name] = {"value": value, "source": self.label}
        return out


def is_json(value: object) -> bool:
    """Whether `value` is JSON data: None, a bool, a finite number, a
    string, or lists and string-keyed dicts of them."""
    if value is None or isinstance(value, (bool, int, str)):
        return True
    if isinstance(value, float):
        return value == value and value not in (float("inf"), float("-inf"))
    if isinstance(value, (list, tuple)):
        return all(is_json(v) for v in cast("list[object]", value))
    if isinstance(value, dict):
        items = cast("dict[object, object]", value)
        return all(isinstance(k, str) and is_json(v) for k, v in items.items())
    return False

