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
the build, else one per material per module); each one's files
(`python -m lang.nesting`, written under the design's out directory as
`<module>/<nest>/nest.json` and `nest.svg`) are shown when there are any,
marked stale when their layout is not the one built last. The page's
"nest again" (POST /nest?design=...&nest=kitchen.carcass) nests the chosen
nest again, with the inventory beside the build file, one nest at a time.
Nests are never run on a save: one takes seconds to minutes.
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
        """Asks for one of the design's nests by path; False when there is
        no such design or its layout has no such nest."""
        with self.cond:
            design = self.designs.get(name)
            if design is None or not any(n["path"] == nest for n in _nests(design)):
                return False
            if nest not in design.nesting:
                design.nesting.append(nest)
            design.nest_failed.discard(nest)
            self.cond.notify_all()
            return True

    def nest_forever(self) -> None:
        while True:
            with self.cond:
                while (design := next((d for d in self.designs.values() if d.nesting), None)) is None:
                    self.cond.wait()
                nest = design.nesting[0]
                folder = next((d for path, d in _folders(design) if path == nest), nest.replace(".", "/"))
            ok = renest(design.file, design.out, nest, folder)
            with self.cond:
                design.nesting.remove(nest)
                if not ok:
                    design.nest_failed.add(nest)

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


def nest_state(design: Design) -> list[dict[str, Any]]:
    """The design's nests as the page shows them, each by its path and its
    folder (`dir`, under the design's url) with its state: `none`,
    `running`, `failed` (the log), `ok` or `stale` (its layout is not the
    one built last), and its version (the nest file's time) for the page
    to reload it."""
    out: list[dict[str, Any]] = []
    for path, folder in _folders(design):
        entry: dict[str, Any] = {"path": path, "dir": folder + "/"}
        file = design.out / folder / "nest.json"
        if path in design.nesting:
            entry["state"] = "running"
        elif path in design.nest_failed:
            entry |= {"state": "failed", "log": _read(design.out / folder / "nest.log")}
        else:
            try:
                nest = json.loads(file.read_text())
                entry["version"] = str(file.stat().st_mtime_ns)
                fresh = nest.get("layout_hash") == _layout_hash(design.out / "layout.json")
                entry["state"] = "ok" if fresh else "stale"
            except (OSError, ValueError):
                entry["state"] = "none"
        out.append(entry)
    return out


_hashes: dict[Path, tuple[int, str | None]] = {}


def _layout_hash(path: Path) -> str | None:
    """The hash of a built layout (`lang.core.layout.layout_hash`), kept
    while the file is unchanged."""
    from lang.core.layout import layout_hash
    try:
        mtime = path.stat().st_mtime_ns
    except OSError:
        return None
    cached = _hashes.get(path)
    if cached is None or cached[0] != mtime:
        try:
            cached = (mtime, layout_hash(json.loads(path.read_text())))
        except (OSError, ValueError):
            cached = (mtime, None)
        _hashes[path] = cached
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
        if url.path != "/nest":
            self.send_error(404)
            return
        query = parse_qs(url.query)
        ok = self.designs.ask_nest(query.get("design", [""])[0], query.get("nest", [""])[0])
        self.send_response(200 if ok else 404)
        self.send_header("Content-Length", "0")
        self.end_headers()

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
