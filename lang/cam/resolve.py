"""The plan's settings as the layout gives them (`keys`), read as the nest
reads its own (`lang.nesting.resolve`).

A key the plan needs one value of (`keys.JOINS` "agree") is the nest's own
(`carcass.use(cam.skin(0.3))`), else its parts', each along its chain,
which must agree (else the plan is refused, naming two parts and where
each value came from), else the default. Any other key is read for a part
and, where it has a name, an operation of it: the operation's own
(`left.toekick.use(...)`), else the nest's, else the part's along its
chain, else the default: the proposal's precedence, nearest the reader
first, operation, nest, part, its scopes, the root
[`proposals/settings.md`, The chain].

A second nest (`kitchen.carcass-2`) takes the settings of the nest it
follows. The settings may be read from the build as it is now (the
command runs it, so a CAM setting changed since the nest holds without
nesting again) with the nest's layout for a part or nest the build no
longer has.
"""
from __future__ import annotations

import json
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, cast

from ..core.errors import LangError
from ..core.layout_types import JsonValue, Layout, NestLayout, PartLayout, SettingLayout
from ..core.settings import Setting
from . import keys
from .keys import JOINS, KEYS

DEFAULT = "default"
#: The repository, which a relative `cam.templates` is taken from.
REPO = Path(__file__).resolve().parents[2]


def _json(value: object) -> JsonValue:
    if isinstance(value, tuple):
        return [_json(v) for v in cast("tuple[object, ...]", value)]
    return cast(JsonValue, value)


@dataclass
class Values:
    """A nest's CAM settings: the nest's values of the keys it needs one
    of, and the rest read per part and operation (see the module's doc)."""
    parts: dict[str, PartLayout]
    nest: dict[str, SettingLayout]
    agreed: dict[str, tuple[JsonValue, str]] = field(default_factory=dict[str, tuple[JsonValue, str]])
    read_from: str = "nest"

    def value(self, key: Setting[Any], part: str | None = None, op: str | None = None) -> Any:
        return self.sourced(key, part, op)[0]

    def sourced(self, key: Setting[Any], part: str | None = None, op: str | None = None) -> tuple[JsonValue, str]:
        name = key.name
        if JOINS[name] == "agree":
            return self.agreed[name]
        layout = self.parts.get(part) if part is not None else None
        if layout is not None and op is not None:
            own = layout["op_settings"].get(op, {}).get(name)
            if own is not None:
                return own["value"], own["source"]
        own = self.nest.get(name)
        if own is not None:
            return own["value"], own["source"]
        if layout is not None:
            given = layout["settings"].get(name)
            if given is not None:
                return given["value"], given["source"]
        return _json(key.default), DEFAULT

    def templates_folder(self) -> Path:
        folder = Path(str(self.value(keys.templates)))
        return folder if folder.is_absolute() else REPO / folder


def resolve(layout: Layout, nest_path: str, parts: Sequence[str], fallback: Layout | None = None,
            read_from: str = "nest") -> Values:
    """The CAM settings of a nest and its parts from `layout`, a part or
    nest it does not have from `fallback` (the layout nested)."""
    by_path = _parts(layout)
    spare = _parts(fallback) if fallback is not None else {}
    chosen: dict[str, PartLayout] = {}
    for path in parts:
        part = by_path.get(path) or spare.get(path)
        if part is None:
            raise LangError(f"{nest_path}: the layout has no part {path}.")
        chosen[path] = part
    nest = _nest(layout, nest_path) or (_nest(fallback, nest_path) if fallback is not None else None)
    values = Values(chosen, dict(nest["settings"]) if nest is not None else {}, read_from=read_from)
    for key in KEYS:
        name = key.name
        if JOINS[name] != "agree":
            continue
        own = values.nest.get(name)
        if own is not None:
            values.agreed[name] = (own["value"], own["source"])
            continue
        given = [(path, *_given(part, key)) for path, part in chosen.items()]
        first = given[0] if given else None
        other = next((g for g in given if first is not None and g[1] != first[1]), None)
        if first is not None and other is not None:
            raise LangError(f"{nest_path}: its parts give two values of {name}: {first[0]} {first[1]!r} "
                            f"({first[2]}), {other[0]} {other[1]!r} ({other[2]}); the plan takes one. Use "
                            f"{name}(...) on the nest, or one above both.")
        values.agreed[name] = (first[1], first[2]) if first is not None else (_json(key.default), DEFAULT)
    return values


def _given(part: PartLayout, key: Setting[Any]) -> tuple[JsonValue, str]:
    given = part["settings"].get(key.name)
    if given is not None:
        return given["value"], given["source"]
    return _json(key.default), DEFAULT


def _parts(layout: Layout | None) -> dict[str, PartLayout]:
    if layout is None:
        return {}
    return {p["path"]: p for m in layout["modules"] for p in m["parts"]}


def _nest(layout: Layout | None, path: str) -> NestLayout | None:
    if layout is None:
        return None
    return next((n for m in layout["modules"] for n in m["nests"] if n["path"] == path), None)


def summary(values: Values) -> tuple[dict[str, JsonValue], dict[str, str], dict[str, dict[str, SettingLayout]],
                                     dict[str, dict[str, dict[str, SettingLayout]]]]:
    """The values for the plan file: per key the nest's, else the one its
    parts have most (the nest's or the default where several have as
    many), its source, and the parts' and named operations' own where they
    differ."""
    out: dict[str, JsonValue] = {}
    sources: dict[str, str] = {}
    for key in KEYS:
        base = values.sourced(key)
        given = [values.sourced(key, path) for path in values.parts]
        counted = Counter(json.dumps(v, sort_keys=True) for v, _src in given)
        most = max(counted.values(), default=0)
        if counted.get(json.dumps(base[0], sort_keys=True), 0) == most:
            out[key.name], sources[key.name] = base
        else:
            out[key.name], sources[key.name] = next((v, src) for v, src in given
                                                    if counted[json.dumps(v, sort_keys=True)] == most)
    parts: dict[str, dict[str, SettingLayout]] = {}
    ops: dict[str, dict[str, dict[str, SettingLayout]]] = {}
    for path, part in values.parts.items():
        for key in KEYS:
            if JOINS[key.name] == "agree":
                continue
            value, source = values.sourced(key, path)
            if value != out[key.name]:
                parts.setdefault(path, {})[key.name] = {"value": value, "source": source}
            for op in part["op_settings"]:
                if key.name in part["op_settings"][op]:
                    v, src = values.sourced(key, path, op)
                    ops.setdefault(path, {}).setdefault(op, {})[key.name] = {"value": v, "source": src}
    return out, sources, parts, ops
