"""Compiler: the modeling language's Fusion side (see DESIGN.md).

One command so far, Compile: pick a layout file written by `lang.build`
and draw it into a new direct-modeling document with `lang.emit`.
Snapshot and Copy Path come later.
"""
import importlib
import importlib.util
import os
import sys
from types import ModuleType

import adsk.core
import adsk.fusion

from lib import addin, ui_placement
from lib.fusionbootstrap.runtime import RuntimeInfo

_addin: addin.Addin | None = None

#: The add-in lives in <repo>/addins-src/compiler; the language in <repo>/lang.
#: realpath, because Fusion loads the add-in through a symlink in dev mode.
ADDIN_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(os.path.dirname(ADDIN_DIR))
EMIT_DIR = os.path.join(REPO_DIR, "lang", "emit")

#: The directory the file dialog opens in; the last one used.
_last_dir: str | None = None


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = Compiler(runtime_info)
    # Dev support: allow external tooling to restart this add-in by firing the
    # custom event '<id>_reload' (see lib/fusionbootstrap/reloader.py).
    from lib.fusionbootstrap import reloader
    entry = os.path.join(os.path.dirname(os.path.abspath(__file__)), "compiler.py")
    reloader.ensure(runtime_info.id + "_reload", entry)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


def load_emitter() -> ModuleType:
    """Loads `lang.emit.fusion` fresh from the repo without importing `lang`
    itself, which needs shapely (see lang/emit/__init__.py)."""
    for name in [n for n in sys.modules if n.startswith("lang.emit")]:
        del sys.modules[name]
    spec = importlib.util.spec_from_file_location(
        "lang.emit", os.path.join(EMIT_DIR, "__init__.py"), submodule_search_locations=[EMIT_DIR])
    if spec is None or spec.loader is None:
        raise RuntimeError(f"lang/emit not found at {EMIT_DIR}")
    package = importlib.util.module_from_spec(spec)
    sys.modules["lang.emit"] = package
    spec.loader.exec_module(package)
    return importlib.import_module("lang.emit.fusion")


class Compiler(addin.Addin):
    @property
    def plugin_name(self) -> str:
        return "Compile Layout"

    @property
    def plugin_desc(self) -> str:
        return "Draws a layout file of the modeling language into a new document."

    @property
    def plugin_tooltip(self) -> str:
        return ("Pick a layout.json written by the modeling language's build step and "
                "draw its parts into a new direct-modeling document.")

    @property
    def has_command_ui(self) -> bool:
        return False

    @property
    def resource_dir(self) -> str:
        return os.path.join(ADDIN_DIR, "Resources")

    def get_ui_placement(self) -> ui_placement.UIPlacement:
        section = ui_placement.PlacementSpec(
            id="SeparatorBeforeCustomAddins",
            anchor_id="FusionMoveCommand",
            insert_before=True,
        )
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id=section.id,
            insert_before=True,
        )
        return ui_placement.UIPlacement(
            panel_id="SolidModifyPanel",
            command=command,
            section=section,
        )

    def execute(self):
        global _last_dir
        dialog = self.ui.createFileDialog()
        dialog.title = "Compile layout"
        dialog.filter = "Layout files (*.json);;All files (*.*)"
        dialog.isMultiSelectEnabled = False
        dialog.initialDirectory = _last_dir or os.path.join(REPO_DIR, "out")
        if dialog.showOpen() != adsk.core.DialogResults.DialogOK:
            return
        path = dialog.filename
        _last_dir = os.path.dirname(path)
        emit = load_emitter()
        report = emit.emit_file(path, log=lambda line: None)
        self.app.activeViewport.fit()
        self.ui.messageBox(report.summary(), "Compile layout")
