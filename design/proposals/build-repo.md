# Build repos and committed outputs

Status: proposed, nothing built. Today builds live in `examples/` in this
repo, and a build's output is the layout JSON in `out/`, not committed.

## A repo per van

Tooling stays in this repo; builds live in a separate repo, one folder per
van:

```
builds/<van>/
  build.py        which modules to compile, in what order
  master.py       index of names in the master document
  materials.py
  modules/
    floor.py
    kitchen.py
    ...
  snapshot.json   the master document, read once
  out/            derived files, committed
    layout/       one JSON per module
    parts/        one SVG per part
    cutlist.csv
    lock.json
```

- `build.py` orders the compiles, since modules read what other modules
  export (the kitchen reads the floor's top).
- `master.py` is an index that binds the master's names, says where
  exceptions apply (`floor_profile.replace(...)`, see `design/todo.md`) and
  may hold plain measured numbers where nothing needs drawing. Modules import
  it as `van` (`from . import master as van`).
- Three layers change at different speeds: the language rarely, the
  standard library now and then (see `standard-library.md`), a build
  constantly.

## Committed outputs

Committed next to the source:

- the layout JSON per module (the semantic diff);
- one SVG per part rendered from it by the preview's mesher (the visual
  diff);
- the cut list, with slats and runs by length;
- a lock file recording the snapshot hash and the tooling commit a compile
  used;
- later the nest file (see `nesting.md`).

## Fusion documents, not in git

| Document                    | Made by          | Contains                                 |
|-----------------------------|------------------|------------------------------------------|
| Vehicle                     | manufacturer     | imported geometry                        |
| Master                      | Florian, by hand | named planes and sketches                |
| Module reference (optional) | Florian, by hand | extra hand-drawn geometry for one module |
| One per module              | compiler         | generated parts, disposable              |
| Assembly                    | compiler or hand | links to all of the above                |

Assembling module documents into the van is easy by hand; an experiment on
how inserting many module documents performs was dropped as a priority.

Open: the package name, and whether path names are German (existing
documents use German component names) or English. Suggestion: English in
code, since the API and `lib/` are English and Claude writes most of it, with
an optional label override for the machine. Terminology: "module" collides
with Python's term and the `modules/` folder; "layout" collides with nesting.
Livable, but a conscious choice.
