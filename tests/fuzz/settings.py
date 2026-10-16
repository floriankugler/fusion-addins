"""Random chains of nodes and bindings, and random orders of uses and
reads, for fuzzing the settings (`lang.core.settings`) against a plain
model of what they promise. A case is plain data, and the checks look from
the outside, through `use()`, `.use()`, `value()`, `.value()` and the
layout.

A `ChainCase` is a build's tree: modules at the root, written in place
(`with module()`) or lazy (an `@module` body), each opening toward a world
direction or in the enclosing frame, in them scopes, lazy modules and
boards, on the boards named operations. Each node uses some of three test
keys (`a` and `b` with defaults, `c` without) at a moment of its own: a
module's or scope's `use()` at the top of its block or at its end, a lazy
module's `.use()` on what its call returns or `use()` in its body, the
root's before or after the modules; and the core's: a material (a board's
own or a scope's, of three, one without grain), `nest` and a grain extent
(a board's own modifiers, or a scope's, early or late). `chain_problems`
builds it, reads every test key at every node and compares the value with
the model's (the nearest node that uses the key, else its default, else
the error of a key without one), and every part in the layout with the
model: its `settings` and `op_settings` (the keys used along its chain,
each from the node that used it), its material, whether it is nested, and
its grain, an inherited extent read in the frame of the node that used it;
a board without a material along its chain, or with an inherited grain
along its thickness, must fail the build with that error.

An `OrderCase` is a fixed tree (the root; a module `m`; in it a scope `s`
with a board `b` and its named operation `notch`, a board `c`, and a lazy
module `L` whose body makes a board `d`) and a random sequence of uses and
reads. `order_problems` plays it against the model of set once and
freezing: a use is refused when the node used the key before, or when a
read passed through the node (a read at it or below that no nearer use
stopped), naming the first such reader; a refused use changes nothing; a
read gives the nearest value, the default, or the error of a key without
one, which freezes nothing.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

from hypothesis import strategies as st

from fuzzing import fresh
from lang import (Binding, Board, Box, Frame, Operation, Scope, Setting, SheetMaterial, board, grain, material, module,
                  nest, scope, setting, sheet_material, use, value, world_frame)
from lang.core.directions import Axis, ExtentName
from lang.core.errors import LangError
from lang.core.layout import build_layout
from lang.core.layout_types import SettingLayout

BOX = Box.from_size(width=600, depth=500, height=720)
PLY = sheet_material("birch", t=15)
c_key: Setting[float] = setting(..., "c")
KEYS: tuple[Setting[float], ...] = (setting(0.0, "a"), setting(10.0, "b"), c_key)
#: (key index, value, late): a use, and whether it comes late (see the module docstring).
Use = tuple[int, int, bool]


# -- the model --------------------------------------------------------------------------------------------

@dataclass(eq=False)
class Model:
    """A node as the model sees it: its label (a path, "root"), its parent,
    what it uses, and the first reader of each key that passed through it."""
    label: str
    parent: Model | None
    uses: dict[int, float] = field(default_factory=lambda: {})
    frozen: dict[int, str] = field(default_factory=lambda: {})

    def resolve(self, key: int) -> tuple[float | None, Model | None]:
        node: Model | None = self
        while node is not None:
            if key in node.uses:
                return node.uses[key], node
            node = node.parent
        default = KEYS[key]
        return (default.default if default.has_default else None), None

    def read(self, key: int) -> float | None:
        """The value the language must give, freezing what the read
        passes; None for the error of a key without a default."""
        got, found = self.resolve(key)
        if got is None:
            return None
        node: Model | None = self
        while node is not None and node is not found:
            node.frozen.setdefault(key, self.label)
            node = node.parent
        return got

    def use(self, key: int, v: float) -> str | None:
        """The error the language must give for the use, or None, in which
        case the node now uses it."""
        name = KEYS[key].name
        if key in self.uses:
            return f"{name} used twice on {self.label}"
        if key in self.frozen:
            return f"on {self.label} comes after {self.frozen[key]} read {name}"
        self.uses[key] = v
        return None


Handle = Scope | Board | Operation | None      # None: the root


def read(handle: Handle, key: Setting[float]) -> float:
    return value(key) if handle is None else handle.value(key)


def apply(handle: Handle, key: Setting[float], v: float) -> None:
    if handle is None:
        use(key(v))
    else:
        handle.use(key(v))


def outcome[T](fn: Callable[[], T]) -> tuple[T | None, str | None]:
    """What a call gives, or its LangError's message."""
    try:
        return fn(), None
    except LangError as error:
        return None, str(error)


# -- chains -----------------------------------------------------------------------------------------------

#: The materials a chain case uses: two grained, one without grain.
MATERIALS = (sheet_material("birch", t=12), sheet_material("birch", t=15), sheet_material("mdf", t=16, grain=False))
#: The world directions a module may open toward, or None for the enclosing frame.
FRONTS = (None, "front", "back", "left", "right")
EXTENTS: tuple[ExtentName, ...] = ("width", "depth", "height")


@dataclass(frozen=True)
class Spec:
    """A node of a chain case: a module in place, a lazy one, a scope or a
    board, and what it uses: test keys (`uses`), a material (index into
    `MATERIALS`; a board's own, `board(name, material)`, else used at the
    node's first moment, since a board reads it when it is placed), `nest`
    and a grain extent (a board's own `nest()` and `grain()`; for a board
    only "depth" or "height", never its thickness), late or early. A module
    opens toward a world direction or takes the enclosing frame; a module
    or scope has children, a board named operations, each with its uses."""
    kind: Literal["module", "lazy", "scope", "board"]
    uses: tuple[Use, ...] = ()
    material: int | None = None
    nest: bool | None = None
    grain: ExtentName | None = None
    late_core: bool = False
    front: int = 0
    children: tuple[Spec, ...] = ()
    ops: tuple[tuple[Use, ...], ...] = ()


@dataclass(frozen=True)
class ChainCase:
    root_uses: tuple[Use, ...]
    root_material: int | None
    root_nest: bool | None
    modules: tuple[Spec, ...]


def _uses() -> st.SearchStrategy[tuple[Use, ...]]:
    return st.lists(st.tuples(st.integers(0, 2), st.integers(1, 9), st.booleans()), max_size=3,
                    unique_by=lambda u: u[0]).map(tuple)


def _materials() -> st.SearchStrategy[int | None]:
    return st.none() | st.integers(0, len(MATERIALS) - 1)


def _nests() -> st.SearchStrategy[bool | None]:
    return st.none() | st.booleans()


def chain_cases() -> st.SearchStrategy[ChainCase]:
    boards = st.builds(Spec, kind=st.just("board"), uses=_uses(), material=_materials(), nest=_nests(),
                       grain=st.none() | st.sampled_from(["depth", "height"]),
                       ops=st.lists(_uses(), max_size=2).map(tuple))

    def scopes(kind: st.SearchStrategy[str], inner: st.SearchStrategy[Spec]) -> st.SearchStrategy[Spec]:
        return st.builds(Spec, kind=kind, uses=_uses(), material=_materials(), nest=_nests(),
                         grain=st.none() | st.sampled_from(EXTENTS), late_core=st.booleans(),
                         front=st.integers(0, len(FRONTS) - 1), children=st.lists(inner, max_size=3).map(tuple))

    nodes = st.recursive(boards, lambda inner: scopes(st.sampled_from(["scope", "lazy"]), inner), max_leaves=8)
    return st.builds(ChainCase, root_uses=_uses(), root_material=_materials(), root_nest=_nests(),
                     modules=st.lists(scopes(st.sampled_from(["module", "lazy"]), nodes), min_size=1,
                                      max_size=2).map(tuple))


@dataclass(eq=False)
class CoreModel:
    """What the model knows of a node beyond `Model`: its frame, and the
    core keys it uses."""
    frame: Frame
    material: SheetMaterial | None = None
    nest: bool | None = None
    grain: ExtentName | None = None


@dataclass
class Made:
    """The nodes a chain case made, each with its model, as they come
    (a lazy module's when its body runs)."""
    nodes: list[tuple[Model, Handle]] = field(default_factory=lambda: [])
    boards: list[tuple[Model, list[Model]]] = field(default_factory=lambda: [])
    core: dict[str, CoreModel] = field(default_factory=lambda: {})


@module
def lazy_node(cab: Scope, *, spec: Spec, model: Model, made: Made) -> None:
    """A lazy module of a chain case: its early uses in its body, then its
    children."""
    _early(None, spec)
    use(*(KEYS[k](float(v)) for k, v, late in spec.uses if not late))
    _children(cab, spec, model, made)


def _use_all(handle: Handle, model: Model, uses: tuple[Use, ...], late: bool | None = None) -> None:
    for k, v, is_late in uses:
        if late is None or is_late == late:
            apply(handle, KEYS[k], float(v))
            model.uses[k] = float(v)


def _core(spec: Spec) -> list[Binding[Any]]:
    out: list[Binding[Any]] = []
    if spec.nest is not None:
        out.append(nest(spec.nest))
    if spec.grain is not None:
        out.append(grain(spec.grain))
    return out


def _early(handle: Scope | None, spec: Spec) -> None:
    """A scope's first uses: its material, and nest and grain unless they come late."""
    bindings: list[Binding[Any]] = [material(MATERIALS[spec.material])] if spec.material is not None else []
    if not spec.late_core:
        bindings += _core(spec)
    if handle is None:
        use(*bindings)
    else:
        handle.use(*bindings)


def _late(handle: Scope | None, spec: Spec) -> None:
    if spec.late_core:
        if handle is None:
            use(*_core(spec))
        else:
            handle.use(*_core(spec))


def _children(cab: Scope, spec: Spec, model: Model, made: Made) -> None:
    for i, child in enumerate(spec.children):
        _make(child, cab, f"{child.kind[0]}{i}", model, made)


def _make(spec: Spec, parent: Scope | None, name: str, parent_model: Model, made: Made) -> None:
    label = f"{parent.path}.{name}" if parent is not None else name
    model = Model(label, parent_model)
    parent_frame = made.core[parent_model.label].frame
    facing = FRONTS[spec.front]
    frame = parent_frame if spec.kind in ("scope", "board") or facing is None else \
        Frame.derived(world_frame().direction(facing), world_frame().direction("top"))
    made.core[label] = CoreModel(frame, MATERIALS[spec.material] if spec.material is not None else None,
                                 spec.nest, spec.grain)
    front = world_frame().direction(facing) if spec.kind in ("module", "lazy") and facing is not None else None
    if spec.kind == "board":
        assert parent is not None
        b = board(name, MATERIALS[spec.material] if spec.material is not None else None).on(parent.left)
        if spec.grain is not None:
            b.grain(spec.grain)
        if spec.nest is not None:
            b.nest(spec.nest)
        ops: list[Model] = []
        for i, op_uses in enumerate(spec.ops):
            b.hole(5, at=b.inner.front(20 + 10 * i).bottom(50), depth=5, name=f"op{i}")
            op_model = Model(f"{label}.op{i}", model)
            _use_all(b.op(f"op{i}"), op_model, op_uses)
            made.nodes.append((op_model, b.op(f"op{i}")))
            ops.append(op_model)
        _use_all(b, model, spec.uses)
        made.nodes.append((model, b))
        made.boards.append((model, ops))
    elif spec.kind == "lazy":
        m = lazy_node(BOX, front, name=name, spec=spec, model=model, made=made)
        for k, v, late in spec.uses:
            if not late:
                model.uses[k] = float(v)        # the body uses them, when it runs
        _use_all(m, model, spec.uses, late=True)
        _late(m, spec)                          # from outside, after the call
        made.nodes.append((model, m))
    else:
        with (module(name, BOX, front=front) if spec.kind == "module" else scope(name)) as s:
            _early(None, spec)
            _use_all(None, model, spec.uses, late=False)       # use() in the block, at its top
            _children(s, spec, model, made)
            _use_all(None, model, spec.uses, late=True)        # and at its end
            _late(None, spec)
        made.nodes.append((model, s))


def chain_problems(case: ChainCase) -> list[str]:
    with fresh():
        made = Made()
        root = Model("root", None)
        made.core["root"] = CoreModel(world_frame(), MATERIALS[case.root_material]
                                      if case.root_material is not None else None, case.root_nest)
        errors = _expected_errors(case, made, root)
        try:
            if case.root_material is not None:
                use(material(MATERIALS[case.root_material]))
            _use_all(None, root, case.root_uses, late=False)
            for i, spec in enumerate(case.modules):
                _make(spec, None, f"m{i}", root, made)
            _use_all(None, root, case.root_uses, late=True)
            if case.root_nest is not None:
                use(nest(case.root_nest))
            layout = build_layout()
        except LangError as error:
            if not any(e in str(error) for e in errors):
                return [f"the build failed: {error}; expected {sorted(errors) or 'no error'}"]
            return []
        if errors:
            return [f"the build did not fail; expected one of {sorted(errors)}"]
        problems: list[str] = []
        parts = {p["path"]: p for m in layout["modules"] for p in m["parts"]}
        for model, ops in made.boards:
            part = parts[model.label]
            want, axis, nested = _layout_of(model, made)
            if part["settings"] != dict(sorted(want.items())):
                problems.append(f"the layout's settings of {model.label}: {part['settings']}, expected {want}")
            if part["grain"] != axis or part["nest"] != nested or part["material"] != want["material"]["value"]:
                problems.append(f"{model.label}: grain {part['grain']}, nest {part['nest']}, {part['material']}; "
                                f"expected {axis}, {nested}, {want['material']['value']}")
            op_want = {op.label.rsplit(".", 1)[1]: {KEYS[k].name: {"value": v, "source": op.label}
                                                    for k, v in sorted(op.uses.items())} for op in ops if op.uses}
            if part["op_settings"] != op_want:
                problems.append(f"the layout's op_settings of {model.label}: {part['op_settings']}, "
                                f"expected {op_want}")
        for model, handle in [(root, None), *made.nodes]:
            for k, key in enumerate(KEYS):
                want = model.read(k)
                got, error = outcome(lambda: read(handle, key))
                if want is None:
                    if error is None or f"reads {key.name}, which has no default" not in error:
                        problems.append(f"{model.label} read {key.name}: {got!r} ({error}), expected the error "
                                        "of a key without a default")
                elif error is not None or got != want:
                    problems.append(f"{model.label} read {key.name}: {got!r} ({error}), expected {want}")
        return problems


def _chain(model: Model) -> list[Model]:
    out: list[Model] = []
    node: Model | None = model
    while node is not None:
        out.append(node)
        node = node.parent
    return out


def _nearest[T](model: Model, made: Made, what: Callable[[CoreModel], T | None]) -> tuple[T, Model] | None:
    for node in _chain(model):
        got = what(made.core[node.label])
        if got is not None:
            return got, node
    return None


def _grain_of(model: Model, made: Made) -> tuple[Axis | None, Model | None]:
    """A board's grain axis and the node it comes from, None for none."""
    own = made.core[model.label]
    if own.grain is not None:
        return own.frame.axis_of_extent(own.grain), model
    stuff = _nearest(model, made, lambda c: c.material)
    if stuff is None or not stuff[0].grain:
        return None, None
    found: tuple[ExtentName, Model] | None = _nearest(model, made, lambda c: c.grain)
    if found is None:
        return None, None
    return made.core[found[1].label].frame.axis_of_extent(found[0]), found[1]


def _expected_errors(case: ChainCase, made: Made, root: Model) -> set[str]:
    """The errors the build may fail with: a board with no material along
    its chain, and a grain from above along a board's thickness. Lazy
    modules' boards are made only when their bodies run, so this walks the
    case itself."""
    errors: set[str] = set()

    def walk(spec: Spec, label: str, parent: Model, frame: Frame) -> None:
        model = Model(label, parent)
        facing = FRONTS[spec.front]
        if spec.kind in ("module", "lazy") and facing is not None:
            frame = Frame.derived(world_frame().direction(facing), world_frame().direction("top"))
        made.core.setdefault(label, CoreModel(frame, MATERIALS[spec.material] if spec.material is not None else None,
                                              spec.nest, spec.grain))
        if spec.kind == "board":
            if _nearest(model, made, lambda c: c.material) is None:
                errors.add(f"{label} reads material, which has no default")
            else:
                axis, source = _grain_of(model, made)
                if source is not model and axis == frame.axis_of_extent("width"):
                    assert source is not None
                    errors.add(f"{label}: grain {axis} from {source.label} is the thickness axis")
        for i, child in enumerate(spec.children):
            walk(child, f"{label}.{child.kind[0]}{i}", model, frame)

    for i, spec in enumerate(case.modules):
        walk(spec, f"m{i}", root, world_frame())
    return errors


def _layout_of(model: Model, made: Made) -> tuple[dict[str, SettingLayout], Axis | None, bool]:
    """A board's settings as the layout must carry them, its grain axis
    and whether it is nested."""
    out: dict[str, SettingLayout] = {}
    for node in _chain(model):
        for k, v in node.uses.items():
            out.setdefault(KEYS[k].name, {"value": v, "source": node.label})
    stuff = _nearest(model, made, lambda c: c.material)
    assert stuff is not None
    out["material"] = {"value": stuff[0].label, "source": stuff[1].label}
    nested = _nearest(model, made, lambda c: c.nest)
    if nested is not None:
        out["nest"] = {"value": nested[0], "source": nested[1].label}
    axis, source = _grain_of(model, made)
    if source is not None:
        out["grain"] = {"value": axis, "source": source.label}
    return out, axis, nested[0] if nested is not None else True


# -- orders of uses and reads ------------------------------------------------------------------------------

#: The fixed tree's nodes: labels and parents, by index.
LABELS = ("root", "m", "m.s", "m.s.b", "m.s.b.notch", "m.c", "m.L", "m.L.d")
PARENTS = (None, 0, 1, 2, 3, 1, 1, 6)
#: ("use" or "read", node, key, value)
Event = tuple[Literal["use", "read"], int, int, int]


@dataclass(frozen=True)
class OrderCase:
    events: tuple[Event, ...]


def order_cases() -> st.SearchStrategy[OrderCase]:
    event = st.tuples(st.sampled_from(["use", "read"]), st.integers(0, len(LABELS) - 1), st.integers(0, 2),
                      st.integers(1, 9))
    return st.builds(OrderCase, st.lists(event, max_size=20).map(tuple))


@module
def bay(cab: Scope) -> None:
    board("d", PLY).on(cab.top)


def order_problems(case: OrderCase) -> list[str]:
    with fresh():
        with module("m", BOX) as m:
            with scope("s"):
                b = board("b", PLY).on(m.left)
                b.hole(5, at=b.inner.center, depth=5, name="notch")
            c = board("c", PLY).on(m.right)
            lazy = bay(BOX, name="L")
        s = m.child("s")
        handles: list[Handle] = [None, m, s, b, b.notch, c, lazy, None]
        models: list[Model] = []
        for i, label in enumerate(LABELS):
            parent = PARENTS[i]
            models.append(Model(label, models[parent] if parent is not None else None))
        problems: list[str] = []
        for n, (kind, node, k, v) in enumerate(case.events):
            handle = handles[node] if node != 7 else lazy["d"]     # d is made when L's body runs
            key = KEYS[k]
            if kind == "use":
                want = models[node].use(k, float(v))
                _, error = outcome(lambda: apply(handle, key, float(v)))
                if (want is None) != (error is None) or (want is not None and error is not None and want not in error):
                    problems.append(f"event {n}, {key.name}({v}) on {LABELS[node]}: {error}, expected {want}")
            else:
                want = models[node].read(k)
                got, error = outcome(lambda: read(handle, key))
                if want is None:
                    if error is None or f"reads {key.name}, which has no default" not in error:
                        problems.append(f"event {n}, {LABELS[node]} read {key.name}: {got!r} ({error}), expected "
                                        "the error of a key without a default")
                elif error is not None or got != want:
                    problems.append(f"event {n}, {LABELS[node]} read {key.name}: {got!r} ({error}), expected {want}")
        return problems
