# Addins for Autodesk Fusion 360

This code is in alpha state and there are no guarantees that this will work correctly for your use case.
Furthermore, updates to this code might break existing usages of the addins.

## Addins

- **Lamello**

  This places the holes for Lamello Clamex and Cabineo connectors.
- **Sheet Good Tenons**

  Creates mortise and tenon connections between sheet good boards and also (optionally) places the holes for screw, Clamex or Cabineo connectors in one go.
- **Pattern Cutouts**

  This is a collection of differently shaped pattern cutouts, e.g. triangles, rhombuses etc. The cutouts take existing inner features of the selected faces into account.

  The Froli pattern computes the best froli grid for a given rectangular surface and places cutouts accordingly.
- **Concealed Hinge**

  This places holes for concealed hinges in the door and carcass boards. Currently there's just one type of hinge implemented (Blum cliptop 110 for thin doors).
- **Door Latch**

  Places holes for door latches in the door and carcass boards. Currently this supports Everlocks and the small 44mm pull locks.
- **Dog Bones**

  Creates dog bones for inner corners based on the tool diameter. Specific edges or faces can be selected.
- **Heal Sketch Lines**

  Connects sketch curves that should be connected but are not quite. This often happens when projecting or intersecting complex geometry from e.g. a vehicle model, so that the projected curves do not form a closed profile. This addin automatically heals these curves by placing coincident constraints for end points within a tolerance.

## Installation

To install release builds, either copy add-in folders from `_build` manually into the Fusion Addin directory, or symlink the contents of `_build` into that directory. On macOS the AddIns folder is `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns`.

Then go Fusion's Addin panel:

![](img/doc1.png)

In there you can run the addin by switching on the run toggle. Optionally, you can enable the run-on-startup checkbox, so that you don't have to repeat this process each time you launch Fusion.

![](img/doc2.png)

## Development

For live development from source:

```bash
tools/symlink_lib.sh
tools/symlink_addins.sh --dev
```

This links `addins-src/*` directly into Fusion and links each add-in's `lib/` to the shared repo `lib/`.

To work on the addins, make sure you have VS Code installed, right-click on the plugin's name in Fusion's addin panel and choose "Edit in code editor".

![](img/doc3.png)

## Build System

Release artifacts are produced by `tools/vendor.py`.

What `vendor.py` does:

- Recreates `_build/` from scratch on each run.
- Copies each add-in from `addins-src/<addin>/` into `_build/<addin>_v<version_with_underscores>/`.
- Renames `<addin>.manifest` and `<addin>.py` to include the same `_v...` suffix.
- Vendors the shared `lib/` folder into each built add-in.
- Writes `lib/__version__.py` inside each built add-in.
- Updates each built manifest's `version`.

### Versioning

- The build version is defined in `tools/vendor.py` as `SEMANTIC_VERSION`.
- Build folder/file suffixes replace `.` with `_`, for example:
  `1.0.1` -> `_v1_0_1`.
- The same semantic version is written to each vendored add-in's `lib/__version__.py` and manifest `version`.

### Breaking Changes and Add-in IDs

Fusion uses the manifest `id` to identify an add-in. For breaking changes, the build system can version the manifest IDs so old and new lines can coexist.

`tools/vendor.py` supports three modes:

- `python3 tools/vendor.py --none`
  Treat all add-ins as non-breaking. Manifest IDs stay unchanged.
- `python3 tools/vendor.py --all`
  Treat all add-ins as breaking. Manifest IDs get `_v<SEMANTIC_VERSION>` appended.
- `python3 tools/vendor.py`
  Prompt per add-in: `breaking change? [y/N]`.

Recommended release flow:

- Non-breaking release: bump `SEMANTIC_VERSION`, run `python3 tools/vendor.py --none`.
- Breaking release: bump `SEMANTIC_VERSION`, run `python3 tools/vendor.py` and mark only the changed add-ins as breaking (or use `--all` if all are breaking).

## License

GNU General Public License v3.0 or later

See [COPYING](COPYING) to see the full text.

## Attributions

- Lock icon by karl from [Noun Project](https://thenounproject.com/browse/icons/term/lock/) (CC BY 3.0)
- Hinage icon by Ruslan Dezign from [Noun Project](https://thenounproject.com/browse/icons/term/lock/) (CC BY 3.0)
- Triangular pattern icon by Made x Made from [Noun Project](https://thenounproject.com/browse/icons/term/lock/) (CC BY 3.0)
- Dog bone icon by shashank singh from <a href="https://thenounproject.com/browse/icons/term/dog-bone/">Noun Project</a> (CC BY 3.0)
