# Repository Guidelines

## Project Structure & Module Organization

- `addins-src/` contains the editable Fusion 360 add-ins. Each add-in has a `main.py`, `<addin>.py`, a `<addin>.manifest`, and `Resources/` icons.
- `lib/` is the shared Python library used by add-ins (utility modules, Fusion helpers).
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
