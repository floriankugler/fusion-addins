# Repository Guidelines

## Project Structure & Module Organization

- `addins-src/` contains the editable Fusion 360 add-ins. Each add-in has a `main.py`, `<addin>.py`, a `<addin>.manifest`, and `Resources/` icons.
- `lib/` is the shared Python library used by add-ins (utility modules, Fusion helpers).
  - `lib/domino.py` holds all Festool Domino code (sizes, machine stops, dialog inputs, validation, sketches and cuts), shared by `connectors_native` (Domino connector type) and `tenons_native` (Domino tenon type). Change Domino behavior there, not in the add-ins.
  - `lib/edge_sketch.py` holds the fully constrained sketch and cut helpers along a selected edge that `connectors_native` and `lib/domino.py` build with.
- `_build/` holds versioned, self-contained add-in builds produced for distribution.
- `tools/` includes helper scripts for symlinking and vendoring builds.
- `img/` contains documentation screenshots referenced in `README.md`.
- `fusion_api_docs/` stores the Fusion 360 API reference. Start with `fusion_api_docs/INDEX.md`, then open the per-type or per-member Markdown files as needed.

## Build, Test, and Development Commands

- `tools/symlink_lib.sh`  
  Creates `lib/` symlinks inside each `addins-src/<addin>/` for shared code during development.
- `tools/symlink_addins.sh --dev`  
  Symlinks `addins-src/*` into the Fusion 360 AddIns folder for live dev.
- `tools/symlink_addins.sh`  
  Symlinks `_build/*` into the Fusion 360 AddIns folder (release builds).
- `python3 tools/vendor.py`  
  Vendors `addins-src/` + `lib/` into `_build/` and writes versioned manifests.

### First-Time Setup for New Add-Ins

- After creating a new `addins-src/<addin>/` directory, always run these commands in order:
  1. `tools/symlink_lib.sh`
  2. `tools/symlink_addins.sh --dev`
- The first command adds the shared `lib/` link inside the new add-in. The second makes the new add-in discoverable in Fusion's Scripts and Add-Ins dialog.
- After refreshing the links, reopen the Scripts and Add-Ins dialog and run the new add-in. Restart Fusion if it does not rescan the AddIns folder.
- This first-time linking step is required even when the other development add-ins are already linked.

### Dev Cycle: Restarting Add-Ins After Code Changes

- After changing an add-in's code (or shared `lib/` code), restart the add-in programmatically through the Fusion MCP server instead of asking the user to stop/start it in the Scripts and Add-Ins dialog.
- IMPORTANT: do NOT call `bootstrap.stop`/`bootstrap.run` directly from an MCP script. Event handlers registered during an MCP script execution are torn down when the execution ends — the add-in's commands re-register but their buttons silently do nothing afterwards. Instead, fire the add-in's self-reload custom event; the reload then runs inside the add-in's own (persistent) handler.
- Custom events do NOT dispatch during `adsk.doEvents()` inside a script execution — they run only after the script returns. So the reload takes TWO separate MCP executions (verified 2026-08-01):

  ```python
  # Execution 1: fire the event and return. fireCustomEvent's return value is
  # meaningless in current Fusion builds (False even on success) - ignore it.
  import adsk.core
  adsk.core.Application.get().fireCustomEvent('com_floriankugler_<addin>_reload')
  ```

  ```python
  # Execution 2: check the result.
  import sys
  reloader = sys.modules['lib.fusionbootstrap.reloader']
  print(reloader.last_result('com_floriankugler_<addin>_reload'))  # expect 'ok #n'
  ```

- The self-reload event is provided by `lib/fusionbootstrap/reloader.py`; an add-in opts in by calling `reloader.ensure(runtime_info.id + '_reload', <entry .py path>)` in its `main.run()`. The event is only registered when Fusion itself starts the add-in — after adding reloader support (or after a Fusion restart), the add-in must be started once via the Scripts and Add-Ins dialog before scripted reloads work.
- Stopping an add-in via the Scripts and Add-Ins dialog unregisters its custom events. `reloader.ensure` therefore re-registers unconditionally on every start. (An older version skipped re-registration when it thought the event still existed, leaving dead events after a manual stop/start cycle; `fusionbootstrap` is excluded from dev reload, so that fix only takes effect after a full Fusion restart.)
- Dev mode (no vendored `lib/__version__.py`) reloads all `lib.*` modules (except `fusionbootstrap`) on start, so library changes are picked up too. The reload runs two passes because a single pass can leave a class subclassing a stale base from a module reloaded later (e.g. a table input subclassing `lib.inputs.Input`), which silently breaks isinstance checks — the visible symptom is inputs missing from a dialog. `lib.inputs.Inputs` additionally duck-types its membership check as a second line of defense. Verify after a reload that the add-in's command definitions exist again (`ui.commandDefinitions.itemById(...)`).
- Precondition: the add-in's `Addin` subclasses must override `resource_dir` with an ABSOLUTE path. Fusion resolves the base class's relative `'Resources'` against the caller's context, which fails with "relative resourceFolder path not found" when the restart is triggered from outside Fusion's own add-in launcher.
- The reload cannot run while a command dialog is open in Fusion (scripts are rejected); close the dialog or retry later.

## Coding Style & Naming Conventions

- Language: Python 3, 4-space indentation, no tabs.
- Naming: `snake_case` for functions/variables, lowercase filenames, add-in folder names match manifest names (e.g., `dog_bones`).
- Keep add-in entrypoints in `main.py` and use shared helpers from `lib/`.

## Fusion Modeling Rules

### Sketches

- Always make sure that sketches are fully constrained, unless told otherwise.
- Never use fixed geometry, unless you're explicitly instructed to do so.
- Give every created parameter and feature a stable, human-readable name that describes its purpose. This includes naming the model parameters associated with sketch dimensions.
- Minimize the amount of explicit dimensions within a sketch within reason.

    Leverage all the other constraints available to position and dimension sketch geometry relative to each other instead of using explicit dimensions over and over. For example use the following constraints: equal, horizontal/vertical, colinear, parallel, perpendicular, tangent, etc.
- Use constraints to position geometry relative to each other that belongs to each other.

    For example, when creating the whole pattern for a hinge, a drawer slide or something similar, the different geometries should be constrained relative to each other. Then only use the minimal amount of constraints necessary to position this group of sketch curves to an outside geometry.

    Another example of this is to constraining the position of a rectangle or a center-to-center slot. When possible, the rectangles width and height should be dimensioned internally, and then it should be positioned relative to external geometry. A slot should have a length instead of specifying the distance of both of its endpoints to an external geometry.
- If there are multiple sketches involved in creating the features for one part, project from the first sketch to position the elements in the other sketch.

    For example, a hinge might need hole patterns on two different surfaces. The sketch for the second surface should project geometry from the first sketch to align the elements on the second sketch. Only use the minimal amount of constraints necessary to position the sketch geometry relative to outside features.
- Don't duplicate values or expressions within one sketch that should be the same.

    For example, if there are two pairs of holes, and both should be 25mm apart, specify this 25mm dimension for one hole pair, and then reference that dimension to space the other holes the same.

### Extrudes

- The distance of extrusions should be specified relative to other geometry whe this makes sense semantically, instead of specifying a fixed dimension. For example, to extrude a whole all the way through a board, the extrusion should be specified to cut to the opposite face instead of the thickness of the board at runtime of the addin.
- When the extrusion should not start at the profile plane, but from another object, use the extrusions "from object" feature instead of specifying a fixed dimension. Even when it should not start exactly from another object, but from another object + some offset, you can do that with that "from object" extrusion start option.

### Holes

- Round holes should generally be created using the hole feature instead of creating a circle in a sketch and then extruding that circle. There are exceptions to this rule though. For example, the hole feature works well for fixed depth holes or holes all the way through a part. For holes that stop short of the opposite face with an offset, the hole feature is not a good fit since it doesn't provide that offset option.
- Always use the "hole to object" feature for holes that should go through the whole body, instead of specifying a fixed hole depth.
- Fixed-depth hole features must always be flat-bottomed (tip angle 180 deg) instead of using the default drill point.


## Editable Results (Group Edit)

Native-feature add-ins (`connectors_native`, `tenons_native`, `box_joint`, `cutouts_native`, `concealed_hinge_native`, `door_latch_native`, `dog_bones_native`) can edit a result they created earlier. Implemented in `lib/group_edit.py` and `lib/addin.py`.

- User flow: select any sketch or feature of the add-in's timeline group, then start the command. The dialog opens with the stored settings and the timeline rolled back to just before the group. OK deletes the old group and rebuilds it at the same position, keeping the group's name. Cancel leaves everything untouched. Without such a selection the command creates a new result as usual.
- Mechanics: `Addin.group_features()` creates the timeline group and stores the dialog state as a JSON attribute (`<add-in id>` / `editState`) on the group's first member. Each input contributes `Input.save_state()`; selections are stored as entity tokens. Starting the command with a member selected restores the state in the command's `activate` event, after `group.rollTo(True)` + `command.beginStep()`, so tokens resolve to the entities as they were before the group modified them.

### Opting In a Native Add-In

- `execute()` must create every feature at the timeline marker and must not modify anything outside the features it creates (user parameters excepted, see below).
- Finish `execute()` with `self.group_features(first, last, name)` instead of creating the timeline group yourself, then override `group_edit_enabled` to return `True`.
- Every input must implement `save_state()` / `restore_state()`. The `lib.inputs` types do; custom `Input` subclasses need their own (e.g. `_OptionalFloatInput` in `connectors_native`).
- `restore_state()` re-selects entities through `SelectionCommandInput.addSelection`, which runs the add-in's `pre_select` like a click does. `pre_select` must accept the stored entities one at a time, in their original order, judged against what is selected so far.
- State that lives outside the inputs goes through `edit_state_extra()` / `restore_edit_state_extra()`. Example: `box_joint` stores its user-parameter prefix, so an edit updates the existing `boxJoint…` parameters instead of minting a second set, and it loads the dialog from those parameters' current values, so changes made in Change Parameters win over the stored state.

### Limitations

- A rebuild gives every face and edge a new identity. Deleting the old group makes Fusion silently delete later features that reference its geometry (e.g. a fillet on a cut edge). `Addin` detects this and refuses the edit with a message naming those features; later features that only reference the bodies, or faces that existed before the group, survive.
- The stored state wins over manual changes to the group's own sketch dimensions or feature parameters made after creation, unless the add-in reads them back in `restore_edit_state_extra()`.
- Features a user moved into the group are deleted with it on rebuild.
- Only groups created with state are editable. For older groups, the command just opens in create mode.
- If an upstream change means a stored entity token no longer resolves, that selection stays empty and the user selects it again.
- `command.beginStep()` is a preview API. Inside a command, `rollTo` takes effect only after it; Cancel still undoes the roll.

### Testing Group Edit Through MCP

- Add-ins that Fusion has not started can be driven within one script execution: load `addins-src/<addin>/main.py` with `importlib`, construct the `Addin` subclass with a `RuntimeInfo` (id from `bootstrap._load_id`), run the scenario, then call `addin.shutdown()`.
- With Fusion's native MCP server, `commandDefinitions.itemById(...).execute()` opens the dialog only after the script returns, and while a dialog is open only read-only scripts run. Never press OK (`doExecute`) from a read-only script: it crashed Fusion (2026-10-04), because validation reads entity tokens, which writes. Instead build the inputs with `addin.create_inputs()`, seed `.value` of dropdown/integer/checkbox inputs from `default_value` and FloatInput `.expression`, assign `addin.inputs`, and call `addin._validation_error()` and `addin.execute()` directly. Visibility rules can be checked by calling each input's `update_visibility()`.
- Create (older MCP add-in, where commands ran inside the script): `commandDefinitions.itemById(addin.create_command_id).execute()`, pump `adsk.doEvents()`, fill the inputs (`input.addSelection`, values), then `parentCommand.doExecute(True)`.
- Edit: `ui.activeSelections.add(<group member>)` before executing the command definition. The API cannot select a `TimelineGroup` itself ("invalid argument entity").
- Check the validation verdict before `doExecute(True)`: with invalid inputs it ends the command with the timeline roll committed, leaving the marker rolled back. The OK button is disabled in that state, so users cannot hit this.

## Testing Guidelines

- No automated test suite is present. Validate changes by loading the add-in in Fusion 360 and running the command interactively.
- Prefer testing against a simple sample model that exercises each tool path (e.g., a single board with edges).
- Whenever a test is performed through the Fusion MCP server, capture a screenshot of the resulting model and show it in the task conversation.
- Close every temporary Fusion document created during development or testing before finishing the task. Do not save disposable test documents unless the user explicitly requests it.

## Commit & Pull Request Guidelines

- Commit messages follow short, imperative sentences without prefixes (e.g., "Improve curve healing...").
- PRs should explain user-visible behavior changes, list add-ins affected, and include screenshots or screen recordings when UI changes are involved.
- Link any related issues and note if a vendored `_build/` update is included.

## Configuration & Environment Notes

- Fusion 360 AddIns folder (macOS): `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns`.
- Use `addins-src/` for development; use `_build/` for distribution-ready artifacts.
- Use `fusion_api_docs/INDEX.md` to find API types and members, then reference the specific Markdown file for details.
