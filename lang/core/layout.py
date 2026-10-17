"""The layout step: resolve every part and write the layout JSON.

The layout file is the contract between the language and its consumers
(preview, emitter); its shape is in `layout_types.py`.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from . import directions
from .errors import LangError
from .layout_types import (LAYOUT_VERSION, ExportValue, Layout, MaterialLayout, ModuleLayout, NestLayout,
                           SnapshotLayout)
from .material import SheetMaterial
from .nests import layout_nests
from .refs import as_pos
from .scope import registry


def build_layout() -> Layout:
    """Resolves all registered modules and parts into one layout dict,
    after running the lazy modules' bodies (`registry.run_bodies`). Each
    module lists its own problems (its checks' and the notes its parts
    left); the layout's `problems` are all of them, once each, and the
    snapshots' notes."""
    f = directions.frame
    registry.run_bodies()
    modules: list[ModuleLayout] = []
    problems: list[str] = []
    nests = layout_nests(registry.roots, registry.root_parts)
    for root in registry.roots:
        all_parts = root.all_parts()
        parts = [part.to_layout() for part in all_parts]
        checks = root.run_checks()
        box = root.box
        notes = [note for part in all_parts for note in part.notes]
        modules.append({
            "path": root.path,
            "where": root.where,
            "box": box.as_dict() if box else None,
            "parts": parts,
            "hardware": root.all_hardware(),
            "exports": {k: _export_value(v) for k, v in root.exports.items()},
            "problems": checks + notes + _empty(nests[root.path]),
            "nests": nests[root.path],
        })
        problems += checks + notes + _empty(nests[root.path])
    loose = [part.to_layout() for part in registry.root_parts]
    if loose:
        notes = [note for part in registry.root_parts for note in part.notes]
        modules.append({"path": "", "where": "", "box": None, "parts": loose, "hardware": [], "exports": {},
                        "problems": notes, "nests": nests.get("", [])})
        problems += notes
    # One entry per snapshot file and hash, however often it was read.
    snapshots: dict[tuple[str, str], SnapshotLayout] = {}
    for snapshot in registry.snapshots:
        snapshots.setdefault((str(snapshot.path), snapshot.hash), snapshot.to_layout())
        problems += snapshot.notes
    return {
        "version": LAYOUT_VERSION,
        "units": "mm",
        "frame": {d.name: f"{'+' if d.sign > 0 else '-'}{d.axis}" for d in f.directions()},
        "modules": modules,
        "problems": list(dict.fromkeys(problems)),
        "snapshots": list(snapshots.values()),
        "sheet_materials": _materials(),
    }


def _empty(nests: list[NestLayout]) -> list[str]:
    """A problem for each declared nest that takes no board."""
    return [f"{n['path']}: no board to nest" for n in nests if not n["parts"]]


def _materials() -> dict[str, MaterialLayout]:
    """The boards' sheet materials by label; two of one label must be the
    same material, else the nest could not tell which sheets to buy."""
    out: dict[str, MaterialLayout] = {}
    seen: dict[str, SheetMaterial] = {}
    parts = [p for root in registry.roots for p in root.all_parts()] + list(registry.root_parts)
    for part in parts:
        material = part.material
        if not isinstance(material, SheetMaterial):
            continue
        first = seen.setdefault(material.label, material)
        if first != material:
            raise LangError(f"two materials are called {material.label}: {first} and {material}; give them names "
                            "of their own.", part.path, part.where)
        out[material.label] = {"thickness": material.thickness, "grain": material.grain,
                               "size": list(material.size) if material.size is not None else None}
    return dict(sorted(out.items()))


def _export_value(value: object) -> ExportValue | float | str:
    """A number, a position (anything `as_pos` takes), or else its text."""
    if isinstance(value, (int, float)):
        return float(value)
    try:
        pos = as_pos(value)
    except LangError:
        return str(value)
    return {"axis": pos.axis, "value": pos.value}


def layout_hash(layout: Layout) -> str:
    """The hash of a layout's content, whatever its formatting: a nest
    records the layout it nested by it (`lang.nesting`)."""
    text = json.dumps(layout, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def write_layout(path: str | Path) -> Layout:
    """Builds the layout and writes it as compact JSON (half the size of an
    indented one, for the page and the server to fetch and parse on every
    build)."""
    layout = build_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(layout_json(layout))
    return layout


def layout_json(layout: Layout) -> str:
    """The layout as the files have it: compact JSON."""
    return json.dumps(layout, separators=(",", ":"))
