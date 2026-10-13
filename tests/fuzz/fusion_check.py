"""The Fusion half of the Fusion batch check (`fusion_batch.py` is the
other): run inside Fusion, it draws layouts that `fusion_batch.py` wrote
into one new direct document, each with an emitter of its own, and
compares every part's body with the preview's mesh. It writes Fusion's
side next to each layout (`<out>.fusion.json`: volumes, solids, problems)
for `fusion_batch.py explain`, and returns a summary.

From an MCP script (Fusion's Python has no shapely; this file imports only
`lang.emit`, loaded without its parent package)::

    import importlib.util
    def run(_context: str):
        pass
    spec = importlib.util.spec_from_file_location(
        'fusion_check', '<repo>/tests/fuzz/fusion_check.py')
    check = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check)
    print(check.check(['<repo>/out/fuzz/batch']))

Then close the document it made (the active one; check its name first).
"""
from __future__ import annotations

import gc
import importlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

REPO = Path(__file__).resolve().parents[2]

#: Bodies whose volume differs from the preview's by more than this share
#: are listed; the preview's polygons alone make up to about 0.08 % (see
#: `fusion_batch.tessellation`).
THRESHOLD = 3e-4


def _emitter() -> tuple[ModuleType, ModuleType]:
    """`lang.emit.fusion` and `lang.emit.plan`, loaded afresh from the repo
    without the parent package."""
    for name in [n for n in sys.modules if n.startswith("lang.emit")]:
        del sys.modules[name]
    spec = importlib.util.spec_from_file_location("lang.emit", REPO / "lang" / "emit" / "__init__.py",
                                                  submodule_search_locations=[str(REPO / "lang" / "emit")])
    assert spec is not None and spec.loader is not None
    package = importlib.util.module_from_spec(spec)
    sys.modules["lang.emit"] = package
    spec.loader.exec_module(package)
    return importlib.import_module("lang.emit.fusion"), importlib.import_module("lang.emit.plan")


def check(paths: list[str], threshold: float = THRESHOLD) -> str:
    """Draws each layout `<path>.json` and compares its parts with
    `<path>.volumes.json`; writes `<path>.fusion.json`."""
    fusion, plan = _emitter()
    design = fusion.new_document("direct")
    lines: list[str] = []
    gc.disable()
    try:
        for path in paths:
            layout = json.loads(Path(path + ".json").read_text())
            preview: dict[str, float] = json.loads(Path(path + ".volumes.json").read_text())
            emitter: Any = fusion.Emitter(design)
            report = emitter.emit(plan.plan_layout(layout))
            drawn = emitter.bodies()
            volumes = {name: {"volume": sum(b.volume for b in bodies) * 1000.0,
                              "solids": sum(b.lumps.count for b in bodies)}
                       for name, bodies in drawn.items() if name in preview}
            Path(path + ".fusion.json").write_text(json.dumps(
                {"volumes": volumes, "problems": list(report.problems), "checks": list(report.checks)}, indent=1))
            differ: list[str] = []
            for name, want in preview.items():
                got = volumes.get(name)
                if got is None:
                    differ.append(f"{name}: not drawn")
                    continue
                rel = (got["volume"] - want) / want if want else 0.0
                if got["solids"] != 1 or abs(rel) > threshold:
                    differ.append(f"{name}: {got['solids']} solid(s), {rel * 100:+.4f} %")
            label = Path(path).parent.name if Path(path).name == "layout" else Path(path).name
            lines.append(f"{label}: {report.parts} parts, {report.features} features, "
                         f"{len(report.problems)} problems, {len(differ)} bodies differ")
            lines += [f"   problem: {p[:200]}" for p in report.problems]
            lines += [f"   differs: {d}" for d in differ]
    finally:
        gc.enable()
    lines.append(f"(document {design.parentDocument.name}; close it when done)")
    return "\n".join(lines)
