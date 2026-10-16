"""Compiler: the modeling language's Fusion side (see DESIGN.md).

Two commands so far:

- Compile: pick a layout file written by `lang.build` and draw it into a
  new direct-modeling document with `lang.emit`; or a nest file written by
  `lang.nesting` (`nest.json`) and draw each material's nest into a document
  of its own (`lang.emit.nested`).
- Snapshot: read the active document, the master, into a snapshot file
  for build files (`lang.emit.snapshot`).

Copy Path comes later.
"""
import importlib
import importlib.util
import json
import os
import sys
from types import ModuleType

import adsk.core
import adsk.fusion

from lib import addin, ui_placement
from lib.fusionbootstrap.runtime import RuntimeInfo

_addin: addin.Addin | None = None
_snapshot_addin: addin.Addin | None = None

#: The add-in lives in <repo>/addins-src/compiler; the language in <repo>/lang.
#: realpath, because Fusion loads the add-in through a symlink in dev mode.
ADDIN_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(os.path.dirname(ADDIN_DIR))
EMIT_DIR = os.path.join(REPO_DIR, "lang", "emit")

#: The directories the file dialogs open in; the last ones used.
_last_dir: str | None = None
_last_snapshot_dir: str | None = None


def run(context, runtime_info: RuntimeInfo):
    global _addin, _snapshot_addin
    _addin = Compiler(runtime_info)
    _snapshot_addin = Snapshot(runtime_info)
    # Dev support: allow external tooling to restart this add-in by firing the
    # custom event '<id>_reload' (see lib/fusionbootstrap/reloader.py).
    from lib.fusionbootstrap import reloader
    entry = os.path.join(os.path.dirname(os.path.abspath(__file__)), "compiler.py")
    reloader.ensure(runtime_info.id + "_reload", entry)


def stop(context):
    global _addin, _snapshot_addin
    for instance in (_addin, _snapshot_addin):
        if instance:
            instance.shutdown()
    _addin = None
    _snapshot_addin = None


def load_emit_module(name: str) -> ModuleType:
    """Loads `lang.emit.<name>` fresh from the repo without importing `lang`
    itself, which needs shapely (see lang/emit/__init__.py)."""
    for module in [n for n in sys.modules if n.startswith("lang.emit")]:
        del sys.modules[module]
    spec = importlib.util.spec_from_file_location(
        "lang.emit", os.path.join(EMIT_DIR, "__init__.py"), submodule_search_locations=[EMIT_DIR])
    if spec is None or spec.loader is None:
        raise RuntimeError(f"lang/emit not found at {EMIT_DIR}")
    package = importlib.util.module_from_spec(spec)
    sys.modules["lang.emit"] = package
    spec.loader.exec_module(package)
    return importlib.import_module(f"lang.emit.{name}")


class Compiler(addin.Addin):
    @property
    def plugin_name(self) -> str:
        return "Compile Layout"

    @property
    def plugin_desc(self) -> str:
        return "Draws a layout or nest file of the modeling language into new documents."

    @property
    def plugin_tooltip(self) -> str:
        return ("Pick a layout.json written by the modeling language's build step and "
                "draw its parts into a new direct-modeling document, or a nest.json written by "
                "its nest step and draw each material's sheets, blanks and parts into a document.")

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
        dialog.filter = "Layout and nest files (*.json);;All files (*.*)"
        dialog.isMultiSelectEnabled = False
        dialog.initialDirectory = _last_dir or os.path.join(REPO_DIR, "out")
        if dialog.showOpen() != adsk.core.DialogResults.DialogOK:
            return
        path = dialog.filename
        _last_dir = os.path.dirname(path)
        emit = load_emit_module("fusion")
        with open(path) as fh:
            is_nest = "materials" in json.load(fh)
        if is_nest:
            reports = emit.emit_nest_file(path, log=lambda line: None)
            summary = "\n\n".join(r.summary() for r in reports)
        else:
            summary = emit.emit_file(path, log=lambda line: None).summary()
        self.app.activeViewport.fit()
        self.ui.messageBox(summary, "Compile layout")


class Snapshot(addin.Addin):
    @property
    def create_command_id(self) -> str:
        return self.runtime_info.id + "_snapshot"

    @property
    def plugin_name(self) -> str:
        return "Snapshot Master"

    @property
    def plugin_desc(self) -> str:
        return "Reads the active document, the master, into a snapshot file for build files."

    @property
    def plugin_tooltip(self) -> str:
        return ("Writes the planes, sketches (as contours), bodies (as boxes) and user parameters "
                "of the active document to a snapshot.json, which build files read with "
                "master(). Names starting with __ are left out.")

    @property
    def has_command_ui(self) -> bool:
        return False

    @property
    def resource_dir(self) -> str:
        return os.path.join(ADDIN_DIR, "Resources")

    def get_ui_placement(self) -> ui_placement.UIPlacement:
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id=self.runtime_info.id + "_create",
            insert_before=False,
        )
        return ui_placement.UIPlacement(panel_id="SolidModifyPanel", command=command)

    def execute(self):
        global _last_snapshot_dir
        if adsk.fusion.Design.cast(self.app.activeProduct) is None:
            self.ui.messageBox("The active document is not a design.", "Snapshot master")
            return
        dialog = self.ui.createFileDialog()
        dialog.title = "Write snapshot"
        dialog.filter = "Snapshot files (*.json);;All files (*.*)"
        dialog.initialDirectory = _last_snapshot_dir or REPO_DIR
        dialog.initialFilename = "snapshot.json"
        if dialog.showSave() != adsk.core.DialogResults.DialogOK:
            return
        path = dialog.filename
        _last_snapshot_dir = os.path.dirname(path)
        snapshot = load_emit_module("snapshot")
        summary = snapshot.write_snapshot(path)
        self.ui.messageBox(summary.text(), "Snapshot master")
