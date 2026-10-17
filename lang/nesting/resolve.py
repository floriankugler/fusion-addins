"""A nest's parts and values as the layout gives them (`lang.core.nests`,
`keys`): which nest, the values of the nesting keys for it, and its stock.

A key's value for a nest is the nest's own (`carcass.use(...)`), else its
parts': each part's along its chain as the layout carries it (the part, its
scopes, the root), else the key's default. Where the nest needs one value
(every key but `spacing`) the parts must agree, else the nest is refused,
naming two parts that differ and where each value came from; a nest with
no `bed` anywhere is refused. Between two parts the larger of their
spacings holds: each part keeps its own (`Resolved.spacing`), the nest the
least as its solvers' spacing.

The stock: the sheets of each of the nest's materials, bought in the
material's size (`sheet_material(..., size=)`), and the inventory's pieces
of it on hand; a material with neither is refused by name.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..core.errors import LangError
from ..core.layout_types import JsonValue, Layout, NestLayout, PartLayout
from .keys import JOINS, KEYS
from .workshop import OnHand, Sheet, Workshop

#: The source of a value no node gives.
DEFAULT = "default"


def nests_of(layout: Layout) -> list[NestLayout]:
    """Every nest of the layout, in the layout's order."""
    return [n for m in layout["modules"] for n in m["nests"]]


def nest_of(layout: Layout, path: str) -> NestLayout:
    """The nest named `path` (`kitchen.carcass`), or an error listing them."""
    nests = nests_of(layout)
    for n in nests:
        if n["path"] == path:
            return n
    names = ", ".join(n["path"] for n in nests) or "none"
    raise LangError(f"No nest {path!r} in the build (its nests: {names}).")


def nest_folder(nest: NestLayout) -> Path:
    """Where a nest's files go under a build's out folder: its module's
    folder, then its name (`kitchen/carcass`); a nest of the boards outside
    every module directly by its name."""
    module = nest["module"]
    return Path(module, nest["path"][len(module) + 1:]) if module else Path(nest["path"])


@dataclass(frozen=True)
class Resolved:
    """A nest's values: per key's name its value and where it came from,
    and each part's spacing."""
    values: dict[str, Any]
    sources: dict[str, str]
    #: Each part's spacing (mm), the nest's own for all where it has one.
    spacing: dict[str, float]


def resolve(layout: Layout, nest: NestLayout) -> Resolved:
    """The nest's values (see the module's doc)."""
    parts = _parts(layout, nest)
    if not parts:
        raise LangError(f"{nest['path']}: no part to nest.")
    values: dict[str, Any] = {}
    sources: dict[str, str] = {}
    spacing: dict[str, float] = {}
    for key in KEYS:
        name = key.name
        own = nest["settings"].get(name)
        if own is not None:
            values[name], sources[name] = own["value"], own["source"]
            if JOINS[name] == "max":
                spacing = {p["path"]: float(own["value"]) for p in parts}      # pyright: ignore[reportArgumentType]
            continue
        given = [(p["path"], *_value(p, name, key.default if key.has_default else None)) for p in parts]
        if JOINS[name] == "max":
            spacing = {path: float(v) for path, v, _src in given}            # pyright: ignore[reportArgumentType]
            values[name], sources[name] = min(spacing.values()), _sources(given)
            continue
        first = given[0]
        other = next((g for g in given if g[1] != first[1]), None)
        if other is not None:
            raise LangError(f"{nest['path']}: its parts give two values of {name}: {first[0]} {_shown(first[1])} "
                            f"({first[2]}), {other[0]} {_shown(other[1])} ({other[2]}); a nest takes one. Use "
                            f"{name}(...) on the nest, or one above both.")
        if first[1] is None:
            raise LangError(f"{nest['path']}: no {name} is used for it or its parts; use({name}((2000, 1000))) "
                            "at the root of the build gives the machine's, the nest's .use() one of its own.")
        values[name], sources[name] = first[1], _sources(given)
    return Resolved(values, sources, spacing)


def _parts(layout: Layout, nest: NestLayout) -> list[PartLayout]:
    by_path = {p["path"]: p for m in layout["modules"] for p in m["parts"]}
    missing = [path for path in nest["parts"] if path not in by_path]
    if missing:
        raise LangError(f"{nest['path']}: the layout has no part {missing[0]}.")
    return [by_path[path] for path in nest["parts"]]


def _value(part: PartLayout, name: str, default: object) -> tuple[JsonValue, str]:
    given = part["settings"].get(name)
    if given is not None:
        return given["value"], given["source"]
    return default, DEFAULT  # pyright: ignore[reportReturnType]


def _sources(given: list[tuple[str, JsonValue, str]]) -> str:
    """Where the parts' values came from: one source, or each once."""
    return ", ".join(dict.fromkeys(src for _path, _v, src in given))


def _shown(value: JsonValue) -> str:
    if value is None:
        return "none"
    if isinstance(value, list):
        return " x ".join(f"{v:g}" if isinstance(v, (int, float)) else str(v) for v in value)
    return f"{value:g}" if isinstance(value, (int, float)) and not isinstance(value, bool) else str(value)


def workshop_of(layout: Layout, nest: NestLayout, resolved: Resolved, inventory: Sequence[OnHand] = ()) -> Workshop:
    """The values a nest runs with, its stock with them: per material of its
    parts the sheets to buy (its size) and the pieces on hand."""
    materials = sorted({p["material"] for p in _parts(layout, nest)})
    sheets: list[Sheet] = []
    for label in materials:
        info = layout["sheet_materials"].get(label)
        size = info["size"] if info is not None else None
        if size is not None:
            sheets.append(Sheet(label, size[0], size[1]))
        elif not any(o.material == label for o in inventory):
            raise LangError(f"{nest['path']}: {label} has no sheet size to buy (sheet_material(..., size=(2500, "
                            "1250))) and none on hand in the inventory (inventory.toml).")
    v = resolved.values
    bed = v["nesting.bed"]
    return Workshop(
        bed=(float(bed[0]), float(bed[1])), spacing=float(v["nesting.spacing"]), margin=float(v["nesting.margin"]),
        kerf=float(v["nesting.kerf"]), max_cuts=int(v["nesting.max_cuts"]),
        keep_across=float(v["nesting.keep_across"]), keep_area=float(v["nesting.keep_area"]),
        seconds=float(v["nesting.seconds"]), rate=float(v["nesting.rate"]),
        least_seconds=float(v["nesting.least_seconds"]), refill=bool(v["nesting.refill"]),
        sheets=tuple(sheets), on_hand=tuple(o for o in inventory if o.material in materials))
