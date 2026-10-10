"""The layout step: resolve every part and write the layout JSON.

The layout file is the contract between the language and its consumers
(preview, emitter). Version it on every incompatible change.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import directions
from .scope import registry

LAYOUT_VERSION = 1


def build_layout() -> dict:
    """Resolves all registered modules and parts into one layout dict."""
    f = directions.frame
    modules = []
    problems = []
    for root in registry.roots:
        parts = [part.to_layout() for part in root.all_parts()]
        problems.extend(root.run_checks())
        modules.append({
            "path": root.path,
            "box": root.box.as_dict() if root.box else None,
            "parts": parts,
            "exports": {k: _export_value(v) for k, v in root.exports.items()},
            "problems": list(root.problems),
        })
    loose = [part.to_layout() for part in registry.root_parts]
    if loose:
        modules.append({"path": "", "box": None, "parts": loose, "exports": {}, "problems": []})
    return {
        "version": LAYOUT_VERSION,
        "units": "mm",
        "frame": {d.name: f"{'+' if d.sign > 0 else '-'}{d.axis}" for d in f.directions()},
        "modules": modules,
        "problems": problems,
    }


def _export_value(value):
    if hasattr(value, "axis") and hasattr(value, "value"):
        return {"axis": value.axis, "value": float(value.value)}
    try:
        return float(value)
    except (TypeError, ValueError):
        return str(value)


def write_layout(path: str | Path) -> dict:
    layout = build_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(layout, indent=1))
    return layout
