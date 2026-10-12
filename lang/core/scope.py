"""Scopes and modules: namespaces of parts with a path, a box and a frame.

A module is a scope with a box that compiles into its own document. It is
written in its own frame: `module(name, box, front=box.right)` makes it
face the box's right side, and inside it front, back, left, right, width
and depth are the module's own (see `directions`), and left and right are
a cabinetmaker's, standing in front of it. Without `front=` it takes the
enclosing frame as it is: in the van, the van's own terms, left being the
driver's side, as for the floor or a wall panel. So a cabinet says which
way it opens, also when that is the van's front. Parts register in the
current scope under their
name. Direction names on a scope are its box's sides (`cab.left`), since
carcass parts are usually named after directions too; such parts are
reached with `cab["left"]`. Other names resolve to parts, child scopes and
exports through attribute access.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, ParamSpec, Protocol

from . import directions
from .box import Box
from .directions import AXES, EXTENT_NAMES, Axis, Direction, ExtentName, Frame
from .errors import LangError
from .layout_types import HardwareBodyLayout, HardwareLayout, SnapshotLayout
from .refs import Pos, Side

if TYPE_CHECKING:
    from .part import Board

Check = Callable[["Scope"], list[str]]
#: A hardware object's own `mount` keywords, which `Scope.mount` passes on.
P = ParamSpec("P")


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
        directions.set_frame(Frame())

    def use_snapshot(self, snapshot: SnapshotSource) -> None:
        """Records a snapshot the build reads; one entry per file and hash."""
        if not any(s is snapshot for s in self.snapshots):
            self.snapshots.append(snapshot)


registry = Registry()
_stack: list[Scope] = []


class _Root:
    """The implicit scope outside any `with module()`: no box, no path, the
    world frame."""
    path = ""
    box: Box | None = None
    default_grain: Axis | None = None
    is_module = False

    @property
    def frame(self) -> Frame:
        return directions.frame

    def register(self, part: Board) -> None:
        registry.root_parts.append(part)


_root = _Root()


def current() -> Scope | _Root:
    return _stack[-1] if _stack else _root


directions.set_current_frame_provider(lambda: current().frame)


class Scope:
    def __init__(self, name: str, box: Box | None = None, is_module: bool = False,
                 frame: Frame | None = None):
        if not name or "." in name:
            raise LangError(f"Scope name {name!r} must be non-empty and contain no dots.")
        self.name = name
        self.parent: Scope | None = _stack[-1] if _stack else None
        self.is_module = is_module
        self.frame: Frame = frame if frame is not None else current().frame
        self._box = box.in_frame(self.frame) if box is not None else None
        self.parts: dict[str, Board] = {}
        self.children: dict[str, Scope] = {}
        self.hardware: list[HardwareLayout] = []
        self.exports: dict[str, Any] = {}
        self.checks: list[Check] = []
        self.problems: list[str] = []
        self.default_grain: Axis | None = None
        if self.parent is not None:
            self.parent._register_child(self)
        else:
            registry.roots.append(self)

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
        return self.require_box(direction).side(direction)

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
        if part.name in self.parts or part.name in self.children:
            raise LangError(f"name {part.name!r} already used in this scope.", self.path)
        self.parts[part.name] = part

    def _register_child(self, child: Scope) -> None:
        if child.name in self.parts or child.name in self.children:
            raise LangError(f"name {child.name!r} already used in this scope.", self.path)
        self.children[child.name] = child

    def __getattr__(self, name: str) -> Any:
        """Parts, child scopes and exports by name. Direction names are
        properties (the box's sides), so a part named `left` is `cab["left"]`."""
        if name.startswith("_"):
            raise AttributeError(name)
        parts: dict[str, Board] = self.__dict__.get("parts", {})
        if name in parts:
            return parts[name]
        children: dict[str, Scope] = self.__dict__.get("children", {})
        if name in children:
            return children[name]
        exports: dict[str, Any] = self.__dict__.get("exports", {})
        if name in exports:
            return exports[name]
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
        """Records a bought part as bodies made of world boxes. Hardware
        objects call this from `mount`."""
        if name in self.parts or name in self.children:
            raise LangError(f"hardware name {name!r} collides with a part or scope name.", self.path)
        item: HardwareLayout = {"path": f"{self.path}.{name}", "kind": "hardware", "name": name, "bodies": bodies}
        self.hardware.append(item)
        return item

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
        self.exports[name] = value
        return self

    def check(self, *checks: Check) -> Scope:
        self.checks.extend(checks)
        return self

    def mount(self, hardware: Mountable[P], /, *args: P.args, **kwargs: P.kwargs) -> Scope:
        """Mounts hardware in this scope: `drawer.mount(slide, sides=(left,
        right), front=face.back)`. The hardware decides what that means;
        the keywords are its own `mount`'s, checked by the type checker."""
        hardware.mount(self, *args, **kwargs)
        return self

    def run_checks(self) -> list[str]:
        self.problems = []
        for fn in self.checks:
            self.problems.extend(fn(self))
        for child in self.children.values():
            self.problems.extend(child.run_checks())
        return self.problems

    # -- context manager --------------------------------------------------------------------------

    def __enter__(self) -> Scope:
        _stack.append(self)
        return self

    def __exit__(self, *exc: object) -> None:
        popped = _stack.pop()
        assert popped is self

    def __repr__(self) -> str:
        return f"Scope({self.path})"


def module(name: str, box: Box, front: Side | Direction | None = None, mirrored: bool = False) -> Scope:
    """A module: a scope with a box that compiles into its own document,
    written in its own frame. `front=` says which way it opens, as a side
    of its box (`front=box.right`) or a direction, and makes it a cabinet:
    top stays up and left is a cabinetmaker's, standing in front of the
    module. Without `front=` the enclosing frame is used as it is, the
    van's terms in the van (left is the driver's side): give a cabinet its
    front, also `front=box.front`. `mirrored=True` swaps left and right."""
    parent_frame = current().frame
    if front is None:
        frame = parent_frame.mirrored() if mirrored else parent_frame
    else:
        facing = front.outward if isinstance(front, Side) else front
        frame = Frame.derived(facing, parent_frame.direction("top"), mirrored)
    return Scope(name, box, is_module=True, frame=frame)


def scope(name: str, box: Box | None = None) -> Scope:
    """A sub-scope. Without a box it inherits the enclosing one."""
    return Scope(name, box)


def check(*checks: Check) -> None:
    """Registers checks on the current scope."""
    cur = current()
    if isinstance(cur, _Root):
        raise LangError("check() outside any module.")
    cur.check(*checks)
