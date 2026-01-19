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

## Coding Style & Naming Conventions

- Language: Python 3, 4-space indentation, no tabs.
- Naming: `snake_case` for functions/variables, lowercase filenames, add-in folder names match manifest names (e.g., `dog_bones`).
- Keep add-in entrypoints in `main.py` and use shared helpers from `lib/`.

## Testing Guidelines

- No automated test suite is present. Validate changes by loading the add-in in Fusion 360 and running the command interactively.
- Prefer testing against a simple sample model that exercises each tool path (e.g., a single board with edges).

## Commit & Pull Request Guidelines

- Commit messages follow short, imperative sentences without prefixes (e.g., "Improve curve healing...").
- PRs should explain user-visible behavior changes, list add-ins affected, and include screenshots or screen recordings when UI changes are involved.
- Link any related issues and note if a vendored `_build/` update is included.

## Configuration & Environment Notes

- Fusion 360 AddIns folder (macOS): `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns`.
- Use `addins-src/` for development; use `_build/` for distribution-ready artifacts.
- Use `fusion_api_docs/INDEX.md` to find API types and members, then reference the specific Markdown file for details.
