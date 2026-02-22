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
- **Flatten Design**

  Flattens a design hierarchy into the root component and deletes root-level bodies below a configurable size threshold.

## Installation

To install release builds, either copy add-in folders from `_build` manually into the Fusion Addin directory, or symlink the contents of `_build` into that directory. On macOS the AddIns folder is `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns`.

Before installing, refresh `_build`:

```bash
python3 tools/vendor.py
```

Then go Fusion's Addin panel:

![](img/doc1.png)

In there you can run the addin by switching on the run toggle. Optionally, you can enable the run-on-startup checkbox, so that you don't have to repeat this process each time you launch Fusion.

![](img/doc2.png)

## Defaults

Each add-in command provides two tabs:

- **Values**: normal command inputs.
- **Defaults**: configure persistent default values for that add-in.

On the **Defaults** tab, you can save defaults per input. Defaults can be either:

- Literal values (for example `20`, `true`, or a dropdown value id).
- Expressions (for example `thickness * 0.5`).

For dropdown inputs, hover over the **New default** field to see a tooltip with the available option names and their underlying value ids.

Expression defaults are evaluated by Fusion, so they can reference parameters from the active design. This makes it possible to define project-specific defaults driven by your model parameters.

Defaults are stored in one JSON file per add-in, in the parent folder of the add-in directories (typically the Fusion AddIns folder). The file name is the add-in id, e.g. `com_floriankugler_lamello.json`.

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
- Copies each add-in from `addins-src/<addin>/` into `_build/<addin>_<addin_version>.<lib_version>/`.
- Renames `<addin>.manifest` and `<addin>.py` to include the same version suffix.
- Vendors the shared `lib/` folder into each built add-in.
- Writes `lib/__version__.py` inside each built add-in.
- Updates each built manifest's `version`.
- Updates each built manifest's `id`.

### Versioning

- Shared library version metadata lives in `lib/version.json`:
  - `version`: release version of shared library code (use an integer).
  - `interface_id`: breaking-change counter of the shared library interface.
- Each add-in has its own version metadata in `addins-src/<addin>/version.json`:
  - `version`: release version of that add-in (use an integer).
  - `interface_id`: breaking-change counter of that add-in's interface.
- Build folder/file suffixes use:
  `<addin version>.<lib version>`, for example `_7.3`.
- Built manifest `version` and vendored `lib/__version__.py` use:
  `<addin version>.<lib version>`, for example `7.3`.

### Breaking Changes and Add-in IDs

Fusion uses the manifest `id` to identify add-ins. The build system generates deterministic IDs that are strictly coupled to add-in and shared-lib interface epochs:

- Built ID format:
  `<base_manifest_id>_<addin_interface_id>.<lib_interface_id>`
- Example:
  `com.floriankugler.dogbones_2.1`

Operational rules:

- Breaking add-in interface change: increment that add-in's `interface_id`.
- Breaking shared-lib interface change: increment `lib/interface_id`.

Build command:

```bash
python3 tools/vendor.py
```

## License

GNU General Public License v3.0 or later

See [COPYING](COPYING) to see the full text.

## Attributions

- Lock icon by karl from [Noun Project](https://thenounproject.com/browse/icons/term/lock/) (CC BY 3.0)
- Hinage icon by Ruslan Dezign from [Noun Project](https://thenounproject.com/browse/icons/term/lock/) (CC BY 3.0)
- Triangular pattern icon by Made x Made from [Noun Project](https://thenounproject.com/browse/icons/term/lock/) (CC BY 3.0)
- Dog bone icon by shashank singh from <a href="https://thenounproject.com/browse/icons/term/dog-bone/">Noun Project</a> (CC BY 3.0)
