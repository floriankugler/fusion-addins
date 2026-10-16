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
from .layout_types import LAYOUT_VERSION, ExportValue, Layout, ModuleLayout, SnapshotLayout
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
    for root in registry.roots:
        all_parts = root.all_parts()
        parts = [part.to_layout() for part in all_parts]
        checks = root.run_checks()
        box = root.box
        notes = [note for part in all_parts for note in part.notes]
        modules.append({
            "path": root.path,
            "box": box.as_dict() if box else None,
            "parts": parts,
            "hardware": root.all_hardware(),
            "exports": {k: _export_value(v) for k, v in root.exports.items()},
            "problems": checks + notes,
        })
        problems += checks + notes
    loose = [part.to_layout() for part in registry.root_parts]
    if loose:
        notes = [note for part in registry.root_parts for note in part.notes]
        modules.append({"path": "", "box": None, "parts": loose, "hardware": [], "exports": {}, "problems": notes})
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
    }


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
    layout = build_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(layout, indent=1))
    return layout
