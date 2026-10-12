"""The layout step: resolve every part and write the layout JSON.

The layout file is the contract between the language and its consumers
(preview, emitter); its shape is in `layout_types.py`.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import directions
from .layout_types import LAYOUT_VERSION, ExportValue, Layout, ModuleLayout, SnapshotLayout
from .refs import Pos, as_pos
from .scope import registry


def build_layout() -> Layout:
    """Resolves all registered modules and parts into one layout dict."""
    f = directions.frame
    modules: list[ModuleLayout] = []
    problems: list[str] = []
    for root in registry.roots:
        parts = [part.to_layout() for part in root.all_parts()]
        problems.extend(root.run_checks())
        box = root.box
        notes = [note for part in root.all_parts() for note in part.notes]
        modules.append({
            "path": root.path,
            "box": box.as_dict() if box else None,  # type: ignore[typeddict-item]
            "parts": parts,
            "hardware": root.all_hardware(),
            "exports": {k: _export_value(v) for k, v in root.exports.items()},
            "problems": list(root.problems) + notes,
        })
    loose = [part.to_layout() for part in registry.root_parts]
    if loose:
        notes = [note for part in registry.root_parts for note in part.notes]
        modules.append({"path": "", "box": None, "parts": loose, "hardware": [], "exports": {}, "problems": notes})
    # One entry per snapshot file and hash, however often it was read.
    snapshots: dict[tuple[str, str], SnapshotLayout] = {}
    for snapshot in registry.snapshots:
        snapshots.setdefault((str(snapshot.path), snapshot.hash), snapshot.to_layout())
        problems.extend(note for note in snapshot.notes if note not in problems)
    return {
        "version": LAYOUT_VERSION,
        "units": "mm",
        "frame": {d.name: f"{'+' if d.sign > 0 else '-'}{d.axis}" for d in f.directions()},
        "modules": modules,
        "problems": problems,
        "snapshots": list(snapshots.values()),
    }


def _export_value(value: object) -> ExportValue | float | str:
    if isinstance(value, (int, float)):
        return float(value)
    try:
        pos: Pos = as_pos(value)
        return {"axis": pos.axis, "value": pos.value}
    except Exception:
        return str(value)


def write_layout(path: str | Path) -> Layout:
    layout = build_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(layout, indent=1))
    return layout
