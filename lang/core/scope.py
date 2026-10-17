"""Scopes and modules: namespaces of parts with a path, a box and a frame.

A module is a scope with a box that compiles into its own document.
`module(name, box)` takes the enclosing frame as it is: in the van, the
van's own terms, left being the driver's side, as for the floor or a wall
panel. With `front=` it is written in its own frame:
`module(name, box, front=box.right)` makes it open toward the box's right
side, and inside it front, back, left, right, width and depth are the
module's own (see `directions`), left and right a cabinetmaker's,
standing in front of it. Such a module always says which way it opens, also
when that is the van's front. Parts register in the current scope under
their name. Direction names on a scope are its box's sides (`cab.left`), since
carcass parts are usually named after directions too; such parts are
reached with `cab["left"]`. Other names resolve to parts, child scopes and
exports through attribute access.

`with module(...)` writes a module's body in place. `@module` on a function
that takes its scope makes a module type, called like a constructor
(`kitchen(box, front=box.right, drawers=4)`), whose body runs lazily, the
first time its parts are needed (`ModuleBody`), so `.use()` on what the
call returns comes first.

Every scope and the root (outside every module) is a node of the settings'
chain (`settings.py`): `use()` and `value()` act on the current one,
`Scope.use()` and `Scope.value()` on one in hand.
"""
from __future__ import annotations

import functools
import inspect
from collections.abc import Generator, Sequence
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from typing import (TYPE_CHECKING, Any, Callable, Concatenate, Generic, ParamSpec, Protocol, Self, TypeVar, cast,
                    overload)

from . import directions
from .box import Box
from .directions import AXES, EXTENT_NAMES, Direction, ExtentName, Frame
from .errors import LangError
from .layout_types import HardwareBodyLayout, HardwareLayout, SnapshotLayout
from .refs import Pos, Side
from .settings import Binding, Node, Setting
from .where import where

if TYPE_CHECKING:
    from .material import SheetMaterial
    from .nests import Nest
    from .part import Board

Check = Callable[["Scope"], list[str]]
#: A hardware object's own `mount` keywords, which `Scope.mount` passes on;
#: a module body's own keywords, which its constructor takes.
P = ParamSpec("P")
T = TypeVar("T")


class SnapshotSource(Protocol):
    """A snapshot of the master in use (`lang.master.Master`)."""
    path: Path
    hash: str
    notes: list[str]

    def to_layout(self) -> SnapshotLayout: ...


class Mountable(Protocol[P]):
    """Hardware that can be mounted in a scope (see `lang.hardware`). Its
    `mount` names the parts it goes on as typed keywords, and
    `Scope.mount` takes the same, so the type checker and the editor see
    them: `cab.mount(hinge, door=door, carcass=left)`."""

    def mount(self, scope: Scope, /, *args: P.args, **kwargs: P.kwargs) -> None: ...


class Registry:
    def __init__(self) -> None:
        self.roots: list[Scope] = []
        self.root_parts: list[Board] = []
        #: Snapshots of the master the build reads, recorded in the layout.
        self.snapshots: list[SnapshotSource] = []

    def reset(self) -> None:
        """Forgets everything a build made, the world frame included: the
        next build starts from the default frame unless it sets its own."""
        self.roots.clear()
        self.root_parts.clear()
        self.snapshots.clear()
        _stack.clear()
        _root.settings = _root_node()
        directions.set_frame(Frame())

    def run_bodies(self) -> None:
        """Runs every lazy module's body not run yet, those the bodies make
        included: before the layout writes anything, since a body may still
        change parts of another module (a join)."""
        def run(scope: Scope) -> None:
            for child in list(scope.children.values()):
                run(child)
        for root in list(self.roots):
            run(root)

    def use_snapshot(self, snapshot: SnapshotSource) -> None:
        """Records a snapshot the build reads; one entry per file and hash."""
        if not any(s is snapshot for s in self.snapshots):
            self.snapshots.append(snapshot)


registry = Registry()
_stack: list[Scope] = []


class _Root:
    """The implicit scope outside any `with module()`: no box, no path, the
    world frame. It is the top of the settings' chain, so `use()` outside
    every module applies to all of them."""
    path = ""
    box: Box | None = None
    is_module = False

    def __init__(self) -> None:
        self.settings = _root_node()

    @property
    def frame(self) -> Frame:
        return directions.frame

    def register(self, part: Board) -> None:
        registry.root_parts.append(part)

    def unregister(self, part: Board) -> None:
        registry.root_parts[:] = [p for p in registry.root_parts if p is not part]


def _root_node() -> Node:
    return Node(lambda: "root", lambda: None, lambda: directions.frame)


_root = _Root()


def current() -> Scope | _Root:
    return _stack[-1] if _stack else _root


@contextmanager
def within(scope: Scope | _Root) -> Generator[None]:
    """Makes `scope` the current one for a while, wherever the call is:
    the parts a board makes for itself (a lip's strips) go into the board's
    scope and are named in its frame."""
    saved = _stack[:]
    _stack[:] = [] if isinstance(scope, _Root) else [scope]
    try:
        yield
    finally:
        _stack[:] = saved


directions.set_current_frame_provider(lambda: current().frame)


class Scope:
    def __init__(self, name: str, box: Box | None = None, is_module: bool = False,
                 frame: Frame | None = None, body: Callable[[Scope], object] | None = None):
        if not name or "." in name:
            raise LangError(f"Scope name {name!r} must be non-empty and contain no dots.")
        self.name = name
        #: The build file's line that opened it (`lang.core.where`): the
        #: `module(...)` or `scope(...)` call, a module type's call.
        self.where = where()
        self.parent: Scope | None = _stack[-1] if _stack else None
        self.is_module = is_module
        self.frame: Frame = frame if frame is not None else current().frame
        self._box = box.in_frame(self.frame) if box is not None else None
        #: A lazy module's body, until it runs (`_run_body`).
        self._body = body
        self._parts: dict[str, Board] = {}
        self._children: dict[str, Scope] = {}
        self._hardware: list[HardwareLayout] = []
        self._exports: dict[str, Any] = {}
        self._nests: dict[str, Nest] = {}
        #: The checks run on this scope: a module's start with
        #: `no_interference`, which `uncheck()` turns off [decided by
        #: Florian, 2026-10-15, syntax.md item 4].
        self.checks: list[Check] = [_no_interference()] if is_module else []
        self.problems: list[str] = []
        parent = self.parent
        self.settings = Node(lambda: self.path, lambda: parent.settings if parent is not None else _root.settings,
                             lambda: self.frame)
        if parent is not None:
            parent._register_child(self)
        else:
            registry.roots.append(self)

    # -- what the body makes -------------------------------------------------------------

    def _run_body(self) -> None:
        """Runs a lazy module's body, once, with the module as the current
        scope wherever the first use is."""
        body = self._body
        if body is None:
            return
        self._body = None
        with within(self):
            returned = body(self)
        if returned is not None:
            raise LangError(f"the body of the module {self.name!r} returned {returned!r}; a module body returns "
                            "nothing, and publishes what others need with export().", self.path)

    @property
    def parts(self) -> dict[str, Board]:
        self._run_body()
        return self._parts

    @property
    def children(self) -> dict[str, Scope]:
        self._run_body()
        return self._children

    @property
    def hardware(self) -> list[HardwareLayout]:
        self._run_body()
        return self._hardware

    @property
    def exports(self) -> dict[str, Any]:
        self._run_body()
        return self._exports

    @property
    def nests_declared(self) -> dict[str, Nest]:
        """The nests declared on this scope (`nest()`), by name."""
        self._run_body()
        return self._nests

    # -- identity --------------------------------------------------------------------

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

    def require_box(self, what: str) -> Box:
        """The scope's box (its own or the enclosing one's), or an error
        naming `what` needed it."""
        box = self.box
        if box is None:
            raise LangError(f"{what}: this scope has no box.", self.path)
        return box

    # -- the box's sides and extents -------------------------------------------------

    def side(self, direction: str) -> Side:
        return replace(self.require_box(direction).side(direction), label=f"{self.path}.{direction}")

    @property
    def front(self) -> Side:
        return self.side("front")

    @property
    def back(self) -> Side:
        return self.side("back")

    @property
    def left(self) -> Side:
        return self.side("left")

    @property
    def right(self) -> Side:
        return self.side("right")

    @property
    def top(self) -> Side:
        return self.side("top")

    @property
    def bottom(self) -> Side:
        return self.side("bottom")

    def extent(self, name: ExtentName) -> float:
        return self.require_box("extent").extent(name)

    @property
    def width(self) -> float:
        return self.extent("width")

    @property
    def depth(self) -> float:
        return self.extent("depth")

    @property
    def height(self) -> float:
        return self.extent("height")

    def center(self, name: ExtentName) -> Pos:
        return self.require_box("center").center(name)

    @property
    def interior(self) -> Box:
        """The box inside the parts placed on its sides: for each side, the
        inner face of a board lying on it and covering the side's middle
        (a carcass side, a bottom between the sides, a back), else the side
        itself. A small part on a side, such as a foot or a cleat in a
        corner, does not count."""
        b = self.require_box("interior")
        inner = b
        for part in self.parts.values():
            pb = part.box()
            t = part.t_axis
            if not all(pb.lo[a] - 1e-9 <= (b.lo[a] + b.hi[a]) / 2 <= pb.hi[a] + 1e-9 for a in AXES if a != t):
                continue
            if abs(pb.lo[t] - b.lo[t]) < 1e-9 and pb.hi[t] < b.hi[t]:
                inner = inner.with_side(self.frame.direction_of(t, -1), max(inner.lo[t], pb.hi[t]))
            elif abs(pb.hi[t] - b.hi[t]) < 1e-9 and pb.lo[t] > b.lo[t]:
                inner = inner.with_side(self.frame.direction_of(t, 1), min(inner.hi[t], pb.lo[t]))
        return inner

    # -- registration -----------------------------------------------------------------------

    def register(self, part: Board) -> None:
        if part.name in self._parts or part.name in self._children:
            raise LangError(f"name {part.name!r} already used in this scope.", self.path)
        self._parts[part.name] = part

    def unregister(self, part: Board) -> None:
        """Takes back a part a refused operation made (a lip's strips)."""
        if self._parts.get(part.name) is part:
            del self._parts[part.name]

    def _register_child(self, child: Scope) -> None:
        if child.name in self._parts or child.name in self._children:
            raise LangError(f"name {child.name!r} already used in this scope.", self.path)
        self._children[child.name] = child

    def __getattr__(self, name: str) -> Any:
        """Parts, child scopes and exports by name, a lazy module's after
        its body ran. Direction names are properties (the box's sides), so a
        part named `left` is `cab["left"]`."""
        if name.startswith("_") or "_parts" not in self.__dict__:
            raise AttributeError(name)
        self._run_body()
        if name in self._parts:
            return self._parts[name]
        if name in self._children:
            return self._children[name]
        if name in self._exports:
            return self._exports[name]
        raise AttributeError(f"{self.path!r} has no part, scope or export named {name!r}.")

    def __getitem__(self, name: str) -> Board:
        """A part by name, also for names that are directions (`cab["left"]`).
        Child scopes are attributes (`cab.drawer1`) or `child()`."""
        if name in self.parts:
            return self.parts[name]
        raise KeyError(f"{self.path!r} has no part named {name!r}.")

    def child(self, name: str) -> Scope:
        try:
            return self.children[name]
        except KeyError:
            raise LangError(f"no scope named {name!r}.", self.path) from None

    def part(self, name: str) -> Board:
        try:
            return self.parts[name]
        except KeyError:
            raise LangError(f"no part named {name!r}.", self.path) from None

    def all_parts(self) -> list[Board]:
        out = list(self.parts.values())
        for child in self.children.values():
            out.extend(child.all_parts())
        return out

    def all_hardware(self) -> list[HardwareLayout]:
        out = list(self.hardware)
        for child in self.children.values():
            out.extend(child.all_hardware())
        return out

    def place_hardware(self, name: str, bodies: list[HardwareBodyLayout]) -> HardwareLayout:
        """Records a bought part as bodies made of world boxes, with the
        build file's line that mounted it. Hardware objects call this from
        `mount`, with a name from `unique_hardware_name` where one scope
        may hold several."""
        if name in self.parts or name in self.children:
            raise LangError(f"hardware name {name!r} collides with a part or scope name.", self.path)
        if any(item["name"] == name for item in self.hardware):
            raise LangError(f"hardware name {name!r} is used twice in this scope.", self.path)
        item: HardwareLayout = {"path": f"{self.path}.{name}", "kind": "hardware", "name": name, "bodies": bodies,
                                "where": where()}
        self._hardware.append(item)
        return item

    def unique_hardware_name(self, base: str) -> str:
        """`base`, or `base_2`, `base_3`... when a part, a child scope or a
        hardware item of this scope has that name: for hardware of which
        one scope may hold several, such as the hinges of two doors."""
        taken = set(self.parts) | set(self.children) | {item["name"] for item in self.hardware}
        name, n = base, 2
        while name in taken:
            name, n = f"{base}_{n}", n + 1
        return name

    # -- API -------------------------------------------------------------------------------------

    def export(self, name: str, value: object) -> Scope:
        """Publishes a value for other modules, read as `module.<name>`. The
        name must be free: not a part's or child scope's, not a direction or
        alias (`cab.top` is the box's side), not an attribute of a scope
        (`width`, `interior`, `mount`...), each of which would hide it."""
        if name in self.parts or name in self.children:
            raise LangError(f"export {name!r} collides with a part or scope name.", self.path)
        if self.frame.is_direction(name) or name in EXTENT_NAMES:
            raise LangError(f"export {name!r}: cab.{name} is the box's {name}, which would hide it; "
                            "choose another name, e.g. worktop.", self.path)
        if name.startswith("_") or hasattr(Scope, name) or name in self.__dict__:
            raise LangError(f"export {name!r}: a scope's {name} would hide it; choose another name.", self.path)
        self._exports[name] = value
        return self

    def use(self, *bindings: Binding[Any]) -> Self:
        """Uses settings on this scope, for everything in it that reads
        them: `kitchen.use(chamfer_size(0.5))`. Each key once per scope, and
        before anything in it has read it (`settings.py`)."""
        self.settings.use(*bindings)
        return self

    def value(self, key: Setting[T]) -> T:
        """The value of a setting as this scope sees it: its own, else the
        nearest scope's above it, else the root's, else the key's default."""
        return self.settings.read(key, self.path)[0]

    @overload
    def nest(self, name: str, /, *, material: SheetMaterial) -> Nest: ...

    @overload
    def nest(self, name: str, parts: Sequence[Board], /) -> Nest: ...

    def nest(self, name: str, parts: Sequence[Board] | None = None, /, *,
             material: SheetMaterial | None = None) -> Nest:
        """Declares a nest of this module or scope (`lang.core.nests`):
        `cab.nest("carcass", material=ply15)` for its nested boards of a
        material (its sub-scopes' too, not a module's inside it), or
        `cab.nest("fronts", [front1, front2])` for boards named anywhere in
        it, a `nest(False)` board among them its own blank. The name is
        unique in the module, the nest's path `cab.carcass`; a board is in
        one nest of its module. The nest takes settings of its own:
        `cab.nest(...).use(nesting.margin(15))`. What no nest names, the
        nested boards of a material, makes a nest of its own per module."""
        from .nests import declare
        return declare(self, name, parts, material)

    def check(self, *checks: Check) -> Scope:
        """Adds checks to run on this scope, each once: a module runs
        `no_interference` already, and asking for it again changes
        nothing."""
        for fn in checks:
            if fn not in self.checks:
                self.checks.append(fn)
        return self

    def uncheck(self, *checks: Check) -> Scope:
        """Turns checks off on this scope: `cab.uncheck(no_interference)`
        for a module whose parts overlap on purpose. A check the scope
        does not run is an error."""
        for fn in checks:
            if fn not in self.checks:
                raise LangError(f"uncheck({getattr(fn, '__name__', fn)}): this scope does not run it.", self.path)
            self.checks.remove(fn)
        return self

    def mount(self, hardware: Mountable[P], /, *args: P.args, **kwargs: P.kwargs) -> Scope:
        """Mounts hardware in this scope: `drawer.mount(slide, sides=(left,
        right), front=face.back)`. The hardware decides what that means;
        the keywords are its own `mount`'s, checked by the type checker.
        Hardware goes on boards: a slat takes none for now."""
        for arg in [*args, *kwargs.values()]:
            items: list[object] = list(cast("list[object] | tuple[object, ...]", arg)) \
                if isinstance(arg, (list, tuple)) else [arg]
            for item in items:
                if getattr(item, "kind", None) == "slat":
                    raise LangError(f"mount(): {getattr(item, 'path', item)} is a slat; hardware goes on boards (a "
                                    "slat takes no operations, joins or hardware for now).", self.path)
        hardware.mount(self, *args, **kwargs)
        return self

    def run_checks(self) -> list[str]:
        """The problems of this scope's checks and its children's, once
        each: a module in a module finds its own overlaps again in the
        outer one's."""
        self._run_body()
        problems: list[str] = []
        for fn in self.checks:
            problems.extend(fn(self))
        for child in self.children.values():
            problems.extend(child.run_checks())
        self.problems = list(dict.fromkeys(problems))
        return self.problems

    # -- context manager --------------------------------------------------------------------------

    def __enter__(self) -> Scope:
        self._run_body()
        _stack.append(self)
        return self

    def __exit__(self, *exc: object) -> None:
        popped = _stack.pop()
        assert popped is self

    def __repr__(self) -> str:
        return f"Scope({self.path})"


@overload
def module(name: str, box: Box, front: Side | Direction | None = None, mirrored: bool = False) -> Scope: ...


@overload
def module(name: Callable[Concatenate[Scope, P], None], /) -> ModuleBody[P]: ...


def module(name: str | Callable[Concatenate[Scope, P], None], box: Box | None = None,
           front: Side | Direction | None = None, mirrored: bool = False) -> Scope | ModuleBody[P]:
    """A module: a scope with a box that compiles into its own document.

    `with module(name, box):` writes its body in place. Without `front=` it
    takes the enclosing frame as it is: in the van, the van's own terms
    (left is the driver's side), as for the floor, the ceiling or a wall
    panel. With `front=`, where it opens, a side of its box
    (`front=box.right`) or a direction, it is written in its own frame
    [decided by Florian 2026-10-12, one constructor since 2026-10-16]:
    top stays up, and left and right are a cabinetmaker's, standing in
    front of it, also when it opens toward the van's front
    (`front=box.front`). `mirrored=True` swaps left and right.

    `@module` on a function that takes its scope makes a module type
    (`ModuleBody`): `def kitchen(cab: Scope, *, drawers: int = 3)` is then
    called as `kitchen(box, front=box.right, drawers=4)`."""
    if not isinstance(name, str):
        if box is not None or front is not None or mirrored:
            raise LangError("@module takes the body alone; the box, front= and name= go to the call that makes "
                            "the module.")
        return ModuleBody(name)
    if box is None:
        raise LangError(f"module({name!r}): give its box, module({name!r}, box).")
    return Scope(name, box, is_module=True, frame=_module_frame(name, front, mirrored))


def _module_frame(name: str, front: Side | Direction | None, mirrored: bool) -> Frame:
    """The frame of a module made where the call is: the enclosing one,
    mirrored if asked; with `front=`, its own."""
    parent_frame = current().frame
    if front is None:
        return parent_frame.mirrored() if mirrored else parent_frame
    facing = front.outward if isinstance(front, Side) else front
    up = parent_frame.direction("top")
    if facing.axis == up.axis:
        raise LangError(f"module({name!r}): front= must face sideways; {facing.name} is up or down.")
    return Frame.derived(facing, up, mirrored)


#: What a module type's call takes itself, so a body cannot have them.
_MODULE_KEYWORDS = ("box", "front", "name", "mirrored")


class ModuleBody(Generic[P]):
    """A module type, made by `@module` from a body that takes its scope and
    keywords of its own:

        @module
        def kitchen(cab: Scope, *, drawers: int = 3) -> None:
            ...

    `kitchen(box, front=None, name=None, mirrored=False, drawers=4)` makes
    the module, named after the function unless `name=` says otherwise,
    and returns its scope. Its parent is the scope current at the call, so
    its path and frame are fixed then; the body runs the first time the
    module's parts are needed (a part, a child scope or an export by name,
    a check, the layout) [proposed in `design/proposals/settings.md`,
    Modules], so `.use()` on the scope it returns comes first, and settings
    the parent uses after the call still apply. The body's own keywords
    change what the module is; settings change how its parts are made
    [decided 2026-10-16]."""

    def __init__(self, body: Callable[Concatenate[Scope, P], None]):
        try:
            params = list(inspect.signature(body).parameters.values())
        except (TypeError, ValueError):
            params = []
        own = params[1:]
        if not params or params[0].kind not in (inspect.Parameter.POSITIONAL_ONLY,
                                                inspect.Parameter.POSITIONAL_OR_KEYWORD) \
                or any(p.kind not in (inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.VAR_KEYWORD) for p in own):
            raise LangError(f"@module {getattr(body, '__name__', body)!r}: a module body takes its scope, then "
                            "keywords of its own only: def kitchen(cab: Scope, *, drawers: int = 3).")
        taken = [p.name for p in own if p.name in _MODULE_KEYWORDS]
        if taken:
            raise LangError(f"@module {getattr(body, '__name__', body)!r}: the keyword {taken[0]!r} is the module "
                            f"call's own ({', '.join(_MODULE_KEYWORDS)}); give the body's another name.")
        self._body = body
        functools.update_wrapper(self, body)
        self.__name__: str = getattr(body, "__name__", "module")

    def __call__(self, box: Box, front: Side | Direction | None = None, name: str | None = None,
                 mirrored: bool = False, *args: P.args, **kwargs: P.kwargs) -> Scope:
        made = name if name is not None else self.__name__
        return Scope(made, box, is_module=True, frame=_module_frame(made, front, mirrored),
                     body=lambda scope: self._body(scope, *args, **kwargs))

    def __repr__(self) -> str:
        return f"module({self.__name__})"


def scope(name: str, box: Box | None = None) -> Scope:
    """A sub-scope. Without a box it inherits the enclosing one."""
    return Scope(name, box)


def check(*checks: Check) -> None:
    """Registers checks on the current scope. A module runs
    `no_interference` without asking."""
    cur = current()
    if isinstance(cur, _Root):
        raise LangError("check() outside any module.")
    cur.check(*checks)


def use(*bindings: Binding[Any]) -> None:
    """Uses settings on the current scope, for everything in it that reads
    them, or on the root outside every module: `use(material(ply15),
    chamfer_size(1))`, `use(*house)`. Each key once per scope, before
    anything in it reads it (`settings.py`)."""
    current().settings.use(*bindings)


def value(key: Setting[T]) -> T:
    """The value of a setting where the call is: the current scope's, else
    the nearest above, the root's, the key's default."""
    cur = current()
    return cur.settings.read(key, cur.path or "root")[0]


def uncheck(*checks: Check) -> None:
    """Turns checks off on the current scope: `uncheck(no_interference)`
    inside a module whose parts overlap on purpose."""
    cur = current()
    if isinstance(cur, _Root):
        raise LangError("uncheck() outside any module.")
    cur.uncheck(*checks)


def _no_interference() -> Check:
    """The check every module runs unless it is turned off, imported here
    since the checks import scopes."""
    from .checks import no_interference
    return no_interference
