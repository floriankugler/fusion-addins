"""Preview server: rebuilds on every save and serves the viewer.

    python -m lang.preview examples [--out out] [--port 8765]
    python -m lang.preview examples/drawer_cabinet.py [--out out] [--port 8765]

Given a folder, it serves every build file in it, each built into a
directory of its own under --out (out/van/...), and the page switches
between them. A build file is a `.py` file that imports `lang`. One that
another file in the folder imports is a library and not listed, unless it
keeps a build of its own under `if __name__ == "__build__":` as
drawer_cabinet.py does; names starting with `_` are skipped. The folder is
scanned again after every change, so a new build file shows up and a
deleted one goes.

Builds run in a subprocess (so modules reload cleanly), one at a time, and
only for the designs the open pages show: each page asks for the state of
its design every 0.7 s, which builds it when it changed since its last
build or was not built since the server started. A change marks what it may
affect as stale: a save of a build file that nothing imports that design,
any other change (the `lang` package, `lib`, a shared module or a
snapshot in the folder) every design. A build rewrites the layout and
scene and bumps version.txt; the page reloads the scene, keeping the
camera, or shows the build's error.

Given a single build file, it builds into --out itself, on every save,
whether a page shows it or not.

The nest view: a design's nests are those its layout lists (declared in
the build, else one per material per module), each followed by its second
nests where it is marked as made (`lang.nesting.pinning`); each one's
files (`python -m lang.nesting`, written under the design's out directory
as `<module>/<nest>/nest.json` and `nest.svg`) are shown when there are
any, with what changed since by the parts' fingerprints (a nest stays good
when only another module changed) and, for a nest marked as made, its
sheets made and what is not made of it. The page's "nest again" (POST
/nest?design=...&nest=kitchen.carcass) nests the chosen nest again (a nest
marked as made: its second nest), with the inventory beside the build
file, one nest at a time. Nests are never run on a save: one takes seconds
to minutes. The marks (POST /made?design=...&nest=...[&sheet=2...], POST
/fixed?design=...&nest=...&part=...) run `python -m lang.nesting --made`
or `--fixed` and answer with what it printed; they wait while a nest of
the design runs.

The CAM plan: each nest with a nest file says whether a plan
(`python -m lang.cam`, `cam.json` beside the nest file, served with it)
was written for it, when, and whether it is stale: planned for another
nest file than the one beside it (the nest was written again since), or
of another version. "Plan again" (POST /plan?design=...&nest=...) plans
the nest named, a second nest by its own name, with the build's CAM
settings as they are now; nests and plans run one at a time, a plan's
output in cam.log beside it.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, unquote, urlsplit

from watchfiles import watch

VIEWER_DIR = Path(__file__).parent / "viewer"
REPO = Path(__file__).resolve().parents[2]
SHOWN = 3.0     # seconds a page counts as open after it last asked for its design
TIMEOUT = 120.0  # seconds a build may take before it is stopped and counts as failed
NEST_TIMEOUT = 900.0  # seconds a nest may take

# Read as text, not parsed, so that a file stays listed while an edit
# leaves it unparsable.
_IMPORTS_LANG = re.compile(r"^(?:from\s+lang(?:\.\w+)*\s+import|import\s+lang\b)", re.MULTILINE)
_OWN_BUILD = re.compile(r"""^if\s+__name__\s*==\s*["']__build__["']""", re.MULTILINE)
_IMPORT = re.compile(r"^(?:from\s+(\w+)|import\s+(\w+))", re.MULTILINE)


def scan(folder: Path) -> tuple[list[Path], set[str]]:
    """The build files in `folder`, by name, and the names of the modules
    in it that its files import."""
    sources: dict[Path, str] = {}
    for path in sorted(folder.glob("*.py")):
        try:
            sources[path] = path.read_text(encoding="utf-8", errors="replace")
        except OSError:     # gone since the glob
            pass
    names = {path.stem for path in sources}
    imported = {name for text in sources.values() for match in _IMPORT.findall(text)
                for name in match if name in names}
    files = [path for path, text in sources.items()
             if not path.name.startswith("_") and _IMPORTS_LANG.search(text)
             and (path.stem not in imported or _OWN_BUILD.search(text))]
    return files, imported


@dataclass(eq=False)
class Design:
    """A build file, where it builds to, and how its builds went."""
    file: Path
    out: Path
    url: str                        # of `out`, as the page asks for it
    stale: bool = True              # changed since its last build, or not built yet
    building: bool = False
    ok: bool = False                # whether its last build went through
    builds: int = 0                 # builds finished since the server started
    #: The nests asked for, by path, the first one running.
    nesting: list[str] = field(default_factory=list[str])
    #: The nests whose last run asked for failed.
    nest_failed: set[str] = field(default_factory=set[str])
    #: The nests whose plans were asked for, by path (a second nest's own), and those whose last plan failed.
    planning: list[str] = field(default_factory=list[str])
    plan_failed: set[str] = field(default_factory=set[str])

    @property
    def version(self) -> str | None:
        """The version of the build in `out`, from now or an earlier run."""
        try:
            return (self.out / "version.txt").read_text()
        except OSError:
            return None


class Designs:
    """The build files served and their state, shared by the page's
    requests, the watcher and the builder thread."""

    def __init__(self, source: Path, out_dir: Path):
        self.single = source.is_file()
        self.folder = source.parent if self.single else source
        self.out_dir = out_dir
        self.cond = threading.Condition()
        self.designs: dict[str, Design] = {}
        self.imported: set[str] = set()
        self.pages: dict[str, tuple[str, float]] = {}  # page id -> the design it shows, when it last asked
        if self.single:
            self.designs[source.stem] = Design(source, out_dir, "out/")
        else:
            self.rescan()

    def rescan(self) -> None:
        """Finds the build files again; those still there keep their state."""
        files, imported = scan(self.folder)
        with self.cond:
            self.designs = {path.stem: self.designs.get(path.stem)
                            or Design(path, self.out_dir / path.stem, f"out/{quote(path.stem)}/")
                            for path in files}
            self.imported = imported

    def counts(self, path: Path) -> bool:
        """Whether a change to `path` may change a build: Python anywhere
        watched, and JSON in the folder (a master snapshot) unless a build
        wrote it."""
        return path.suffix == ".py" or (path.suffix == ".json" and path.is_relative_to(self.folder)
                                        and not path.is_relative_to(self.out_dir))

    def changed(self, paths: set[Path]) -> None:
        """Marks the designs that changes to `paths` may affect as stale."""
        if not self.single:
            self.rescan()
        with self.cond:
            for path in paths:
                own = self.designs.get(path.stem)
                if own is not None and own.file == path and path.stem not in self.imported:
                    own.stale = True
                else:
                    for design in self.designs.values():
                        design.stale = True
            self.cond.notify_all()

    def status(self, name: str, page: str = "") -> dict[str, Any]:
        """The designs, and the state of the one named, which the page shows
        from now on instead of what it showed before; it builds when stale."""
        with self.cond:
            now = time.monotonic()
            self.pages = {p: seen for p, seen in self.pages.items() if now - seen[1] < SHOWN}
            self.pages[page] = (name, now)
            design = self.designs.get(name)
            if design is not None:
                self.cond.notify_all()
            state = None if design is None else {
                "name": name, "url": design.url, "version": design.version, "builds": design.builds,
                "state": "building" if design.stale or design.building else "ok" if design.ok else "failed",
                "nests": nest_state(design),
            }
            return {"folder": self.folder.name, "designs": list(self.designs), "design": state}

    def ask_nest(self, name: str, nest: str) -> bool:
        """Asks for one of the design's nests by path (a second nest: the
        nest it follows); False when there is no such design or its layout
        has no such nest."""
        with self.cond:
            design = self.designs.get(name)
            nest = _base_of(design, nest) if design is not None else ""
            if design is None or not nest:
                return False
            if nest not in design.nesting:
                design.nesting.append(nest)
            design.nest_failed.discard(nest)
            self.cond.notify_all()
            return True

    def ask_plan(self, name: str, nest: str) -> bool:
        """Asks for a plan of one of the design's nests by its path as the
        nests are listed (a second nest's own); False when there is no such
        design or nest, or the nest is not nested."""
        with self.cond:
            design = self.designs.get(name)
            if design is None or not any(e["path"] == nest and "version" in e for e in nest_state(design)):
                return False
            if nest not in design.planning:
                design.planning.append(nest)
            design.plan_failed.discard(nest)
            self.cond.notify_all()
            return True

    def pin(self, name: str, args: list[str]) -> tuple[int, str]:
        """Runs a mark (`--made ...` or `--fixed ...`) for a design: the
        HTTP status and what the command printed."""
        with self.cond:
            design = self.designs.get(name)
            if design is None:
                return 404, f"no design {name}"
            if design.nesting:
                return 409, f"a nest of {name} is running ({design.nesting[0]}); mark it when it is done"
        command = [sys.executable, "-m", "lang.nesting", str(design.file), *args, "--out", str(design.out)]
        try:
            result = subprocess.run(command, capture_output=True, text=True, cwd=str(REPO), timeout=TIMEOUT)
            log, ok = (result.stdout + result.stderr).strip(), result.returncode == 0
        except subprocess.TimeoutExpired:
            log, ok = f"error: the mark took longer than {TIMEOUT:g} s and was stopped.", False
        print(f"{design.file.stem}: {' '.join(args)}: {'ok' if ok else 'FAILED'}", flush=True)
        return (200 if ok else 400), log

    def nest_forever(self) -> None:
        """Runs the nests and plans asked for, one at a time, nests first."""
        while True:
            with self.cond:
                while (design := next((d for d in self.designs.values() if d.nesting or d.planning), None)) is None:
                    self.cond.wait()
                nesting = bool(design.nesting)
                if nesting:
                    nest = design.nesting[0]
                    folder = next((d for path, d in _folders(design) if path == nest), nest.replace(".", "/"))
                else:
                    nest = design.planning[0]
                    folder = next((e["dir"] for e in nest_state(design) if e["path"] == nest), "")
            if nesting:
                ok = renest(design.file, design.out, nest, folder)
            else:
                ok = bool(folder) and replan(design.file, design.out, nest, folder)
            with self.cond:
                (design.nesting if nesting else design.planning).remove(nest)
                if not ok:
                    (design.nest_failed if nesting else design.plan_failed).add(nest)

    def next_build(self) -> Design | None:
        """A stale design that a page shows; given a single build file, that
        one, shown or not."""
        now = time.monotonic()
        shown = {name for name, seen in self.pages.values() if now - seen < SHOWN}
        for name, design in self.designs.items():
            if design.stale and (self.single or name in shown):
                return design
        return None

    def build_forever(self) -> None:
        while True:
            with self.cond:
                while (design := self.next_build()) is None:
                    self.cond.wait()
                design.stale, design.building = False, True
            ok = rebuild(design.file, design.out)
            with self.cond:
                design.building, design.ok = False, ok
                design.builds += 1


def _nests(design: Design) -> list[dict[str, Any]]:
    """The nests the design's last layout lists that have parts."""
    try:
        layout = json.loads((design.out / "layout.json").read_text())
        return [n for m in layout["modules"] for n in m.get("nests", []) if n["parts"]]
    except (OSError, ValueError, KeyError, TypeError):
        return []


def _folders(design: Design) -> list[tuple[str, str]]:
    """Each nest's path and its folder under the design's out directory."""
    from lang.nesting.resolve import nest_folder
    return [(n["path"], nest_folder(n).as_posix()) for n in _nests(design)]  # pyright: ignore[reportArgumentType]


def _base_of(design: Design, nest: str) -> str:
    """The layout's nest a nest named stands for: itself, or the one a
    second nest follows (`kitchen.carcass-2`); "" for none."""
    paths = {path for path, _folder in _folders(design)}
    if nest in paths:
        return nest
    head, _, k = nest.rpartition("-")
    return head if k.isdigit() and head in paths else ""


def nest_state(design: Design) -> list[dict[str, Any]]:
    """The design's nests as the page shows them: each nest of its layout,
    then its second nests where it is marked as made, each by its path and
    its folder (`dir`, under the design's url) with:

    - `state`: `none` (not nested), `running`, `failed` (the log), `ok`
      (its parts are as the build has them), `changed` (parts changed since
      it was written, or another set of parts: nest again), `made` (marked
      as made, every sheet), `sheets` (some of its sheets marked);
    - `version` (the nest file's time) for the page to reload it;
    - `follows`: the nest a second nest follows, else "";
    - `sheets`, as [material, name], and `made`, those marked made;
    - `changed`, `new`, `gone`: for a nest not marked, its parts changed,
      new to it and gone from it since its file; for the first nest of one
      marked, against what is made: `changed` (made, changed since), `new`,
      `not_made` (on a sheet not made), which its second nest takes, `gone`
      (made, not in the build's nest now), and `made_parts`, by what each
      was made; `next`, for a nest marked whose next nest is marked too,
      that one (its sheets cannot be marked any more);
    - `plan`: its CAM plan (`_plan_entry`)."""
    from lang.core.errors import LangError
    from lang.nesting.pinning import chain, changes, empty, plan_run, read_state, second_folder, sheets_of
    from lang.nesting.resolve import nest_folder
    out: list[dict[str, Any]] = []
    try:
        state = read_state(design.out)
    except LangError:
        state = empty()
    prints = _fingerprints(design.out / "layout.json")
    for nest in _nests(design):
        base = nest["path"]
        folder = nest_folder(nest)  # pyright: ignore[reportArgumentType]
        current = {p: prints[p] for p in nest["parts"] if p in prints}
        busy = "running" if base in design.nesting else "failed" if base in design.nest_failed else None
        marked = chain(state, base)
        if not marked:
            entry = _nest_entry(design, base, folder, "")
            file = entry.pop("file", None)
            if busy:
                entry["state"] = busy
            elif file is not None:
                found = changes(file, current)
                entry |= {"state": "changed" if found else "ok", "changed": found.changed, "new": found.new,
                          "gone": found.gone}
            if busy == "failed":
                entry["log"] = _read(design.out / folder / "nest.log")
            out.append(entry)
            continue
        files: dict[str, Any] = {}
        for k, name in enumerate(marked, 1):
            entry = _nest_entry(design, name, folder if k == 1 else second_folder(folder, k), base if k > 1 else "")
            file = entry.pop("file", None)
            if file is not None:
                files[name] = file
            made = state["nests"][name]["sheets"]
            entry["made"] = [[m, sheet] for m, sheets in made.items() for sheet in sheets]
            whole = file is None or len(entry["made"]) >= len(sheets_of(file))
            entry["state"] = "made" if whole else "sheets"
            if k < len(marked):
                entry["next"] = marked[k]       # what it left was nested anew there, and that is marked
            out.append(entry)
        run = plan_run(state, base, current, files)
        st = run.standing
        assert st is not None
        out[-len(marked)] |= {"changed": st.changed, "new": st.new, "not_made": st.not_made, "gone": st.gone,
                              "made_parts": st.made}
        entry = _nest_entry(design, run.name, second_folder(folder, run.k), base)
        file = entry.pop("file", None)
        if busy:
            entry["state"] = busy
            if busy == "failed":
                entry["log"] = _read(design.out / folder / "nest.log")
        elif file is not None:
            wanted = {p: current[p] for p in st.reasons}
            found = changes(file, wanted)
            entry |= {"state": "changed" if found else "ok", "changed": found.changed, "new": found.new,
                      "gone": found.gone}
        elif not st.reasons:
            continue                    # nothing is left for a second nest
        out.append(entry)
    return out


def _nest_entry(design: Design, path: str, folder: Path, follows: str) -> dict[str, Any]:
    """A nest's entry with what its file says (`file`, popped by the
    caller), `state` `none` without one, and its plan."""
    from lang.nesting.pinning import sheets_of
    entry: dict[str, Any] = {"path": path, "dir": folder.as_posix() + "/", "follows": follows, "state": "none",
                             "sheets": [], "made": [], "changed": [], "new": [], "gone": []}
    file = design.out / folder / "nest.json"
    nest = _nest_file(file)
    if nest is not None:
        entry |= {"file": nest, "version": str(file.stat().st_mtime_ns),
                  "sheets": [[m, s] for m, s in sheets_of(nest)]}
    entry["plan"] = _plan_entry(design, path, design.out / folder, nest)
    return entry


def _plan_entry(design: Design, path: str, folder: Path, nest: Any) -> dict[str, Any]:
    """A nest's CAM plan, `cam.json` in its folder: `state` `none` (no plan,
    or no nest file to plan), `running` (asked for), `failed` (its `log`),
    `ok` (planned for the nest file beside it) or `stale` (`why`: planned
    for another nest file, which a nest written again since is, or of
    another version: plan again); `written` (when it was planned) and
    `nest_written` (when the nest it was planned for was), and `version`
    (the file's time) for the page to reload it."""
    from lang.cam.plan_types import CAM_VERSION
    busy = "running" if path in design.planning else "failed" if path in design.plan_failed else None
    out: dict[str, Any] = {"state": busy or "none"}
    if busy == "failed":
        out["log"] = _read(folder / "cam.log")
    file = folder / "cam.json"
    if nest is None or (head := _plan_head(file)) is None:
        return out
    out |= {"written": head.get("written", ""), "nest_written": head.get("nest_written", ""),
            "version": str(file.stat().st_mtime_ns)}
    if busy:
        return out
    if head.get("version") != CAM_VERSION:
        out |= {"state": "stale", "why": f"a plan of version {head.get('version')}, this preview reads {CAM_VERSION}"}
    elif head.get("nest_written") != nest["written"] or head.get("layout_hash") != nest["layout_hash"]:
        out |= {"state": "stale", "why": f"planned for the nest written {head.get('nest_written')}, "
                                         f"the nest beside it was written {nest['written']}"}
    else:
        out["state"] = "ok"
    return out


_plan_heads: dict[Path, tuple[int, dict[str, Any] | None]] = {}


def _plan_head(path: Path) -> dict[str, Any] | None:
    """A plan file's own fields (its version, nest, when it and its nest
    were written, the layout's hash), kept while the file is unchanged; None
    for none."""
    try:
        mtime = path.stat().st_mtime_ns
    except OSError:
        return None
    cached = _plan_heads.get(path)
    if cached is None or cached[0] != mtime:
        try:
            plan = json.loads(path.read_text())
            head = {k: plan.get(k) for k in ("version", "nest", "nest_written", "layout_hash", "written")} \
                if isinstance(plan, dict) else None  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        except (OSError, ValueError):
            head = None
        cached = (mtime, head)
        _plan_heads[path] = cached
    return cached[1]


_nest_files: dict[Path, tuple[int, Any]] = {}


def _nest_file(path: Path) -> Any:
    """A nest file of this version (with fingerprints), kept while it is
    unchanged; None for none or another version."""
    from lang.nesting.nest_types import NEST_VERSION
    try:
        mtime = path.stat().st_mtime_ns
    except OSError:
        return None
    cached = _nest_files.get(path)
    if cached is None or cached[0] != mtime:
        try:
            nest = json.loads(path.read_text())
            cached = (mtime, nest if isinstance(nest, dict) and nest.get("version") == NEST_VERSION else None)  # pyright: ignore[reportUnknownMemberType]
        except (OSError, ValueError):
            cached = (mtime, None)
        _nest_files[path] = cached
    return cached[1]


_prints: dict[Path, tuple[int, dict[str, str]]] = {}


def _fingerprints(path: Path) -> dict[str, str]:
    """The parts' fingerprints of a built layout (`lang.nesting.fingerprint`),
    kept while the file is unchanged."""
    from lang.nesting.fingerprint import fingerprints
    try:
        mtime = path.stat().st_mtime_ns
    except OSError:
        return {}
    cached = _prints.get(path)
    if cached is None or cached[0] != mtime:
        try:
            cached = (mtime, fingerprints(json.loads(path.read_text())))
        except (OSError, ValueError, KeyError, TypeError):
            cached = (mtime, {})
        _prints[path] = cached
    return cached[1]


def _read(path: Path) -> str:
    try:
        return path.read_text()
    except OSError:
        return ""


def renest(build_file: Path, out_dir: Path, nest: str, folder: str) -> bool:
    """Nests one of the design's nests into `out_dir` (`python -m
    lang.nesting`), its output in nest.log in the nest's `folder` there."""
    command = [sys.executable, "-m", "lang.nesting", str(build_file), nest, "--out", str(out_dir)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=str(REPO), timeout=NEST_TIMEOUT)
        log, ok = (result.stdout + result.stderr).strip(), result.returncode == 0
    except subprocess.TimeoutExpired:
        log, ok = f"error: the nest took longer than {NEST_TIMEOUT:g} s and was stopped.", False
    (out_dir / folder).mkdir(parents=True, exist_ok=True)
    (out_dir / folder / "nest.log").write_text(log + "\n")
    print(f"{build_file.stem}: nest {nest} {'ok' if ok else 'FAILED'}", flush=True)
    return ok


def replan(build_file: Path, out_dir: Path, nest: str, folder: str) -> bool:
    """Plans one of the design's nests in `out_dir` (`python -m lang.cam`),
    its output in cam.log in the nest's `folder` there."""
    command = [sys.executable, "-m", "lang.cam", str(build_file), nest, "--out", str(out_dir)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=str(REPO), timeout=TIMEOUT)
        log, ok = (result.stdout + result.stderr).strip(), result.returncode == 0
    except subprocess.TimeoutExpired:
        log, ok = f"error: the plan took longer than {TIMEOUT:g} s and was stopped.", False
    (out_dir / folder).mkdir(parents=True, exist_ok=True)
    (out_dir / folder / "cam.log").write_text(log + "\n")
    print(f"{build_file.stem}: plan {nest} {'ok' if ok else 'FAILED'}", flush=True)
    return ok


class _Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, designs: Designs, **kwargs: Any):
        self.designs = designs
        super().__init__(*args, directory=str(VIEWER_DIR), **kwargs)

    def do_GET(self) -> None:
        url = urlsplit(self.path)
        if url.path != "/status.json":
            super().do_GET()
            return
        query = parse_qs(url.query)
        body = json.dumps(self.designs.status(query.get("design", [""])[0], query.get("page", [""])[0])).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        url = urlsplit(self.path)
        query = parse_qs(url.query)
        design, nest = query.get("design", [""])[0], query.get("nest", [""])[0]
        if url.path in ("/nest", "/plan"):
            ok = (self.designs.ask_nest if url.path == "/nest" else self.designs.ask_plan)(design, nest)
            self.send_response(200 if ok else 404)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        given = [nest, *query.get("sheet", []), *query.get("part", [])]
        if any(v.startswith("-") for v in given):       # read as the command's options
            status, text = 400, "a nest, a sheet or a part does not start with -"
        elif url.path == "/made" and nest:
            status, text = self.designs.pin(design, ["--made", nest, *query.get("sheet", [])])
        elif url.path == "/fixed" and nest and query.get("part"):
            status, text = self.designs.pin(design, ["--fixed", nest, *query["part"]])
        else:
            self.send_error(404)
            return
        body = text.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def translate_path(self, path: str) -> str:
        path = path.split("?", 1)[0].split("#", 1)[0]
        if path.startswith("/out/"):
            out = self.designs.out_dir.resolve()
            target = (out / unquote(path[len("/out/"):])).resolve()
            return str(target if target.is_relative_to(out) else out / "missing")
        return super().translate_path(path)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, format: str, *args: Any) -> None:
        pass


def rebuild(build_file: Path, out_dir: Path, timeout: float = TIMEOUT) -> bool:
    """Builds into a scratch directory and moves the result into `out_dir`,
    the version last, so that the page never reads a file half written. A
    failed build, or one stopped after `timeout` seconds (an endless loop
    in a build file would otherwise hold up every design), leaves the last
    good one in place."""
    scratch = out_dir / ".build"
    shutil.rmtree(scratch, ignore_errors=True)
    command = [sys.executable, "-m", "lang.build", str(build_file), "--out", str(scratch)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=str(REPO), timeout=timeout)
    except subprocess.TimeoutExpired as expired:
        output = expired.stdout or ""
        output = output.decode() if isinstance(output, bytes) else output
        result = subprocess.CompletedProcess(command, -1, output,
                                             f"error: the build took longer than {timeout:g} s and was stopped.")
    ok = result.returncode == 0
    out_dir.mkdir(parents=True, exist_ok=True)
    if ok:
        for path in sorted(scratch.iterdir(), key=lambda p: p.name == "version.txt"):
            os.replace(path, out_dir / path.name)
    shutil.rmtree(scratch, ignore_errors=True)
    log = (result.stdout + result.stderr).strip().replace(str(scratch), str(out_dir))
    (out_dir / "build.log").write_text(log + "\n")
    print(f"{build_file.stem}: build {'ok' if ok else 'FAILED'}: {log}", flush=True)
    return ok


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serve the live preview of a build file, or of every build file in a folder.")
    parser.add_argument("source", help="a build file, or a folder of them")
    parser.add_argument("--out", default="out")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    source = Path(args.source).resolve()
    if not source.exists():
        parser.error(f"{args.source} does not exist")
    designs = Designs(source, Path(args.out).resolve())

    handler = functools.partial(_Handler, designs=designs)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    threading.Thread(target=designs.build_forever, daemon=True).start()
    threading.Thread(target=designs.nest_forever, daemon=True).start()
    what = source if designs.single else f"{len(designs.designs)} build files in {source}"
    print(f"preview at http://127.0.0.1:{args.port}/  ({what})", flush=True)

    watched = [designs.folder, REPO / "lang", REPO / "lib"]
    try:
        for changes in watch(*[path for path in watched if path.is_dir()]):
            paths = {Path(p).resolve() for _, p in changes}
            if paths := {path for path in paths if designs.counts(path)}:
                designs.changed(paths)
    except KeyboardInterrupt:
        pass
    server.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
