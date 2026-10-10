"""Preview server: rebuilds on every save and serves the viewer.

    python -m lang.preview examples/drawer_cabinet.py [--out out] [--port 8765]

Watches the build file's directory and the `lang` package. Each save runs
the build in a subprocess (so modules reload cleanly), rewrites the layout
and scene, and bumps version.txt; the page polls that and reloads the
scene, keeping the camera.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

from watchfiles import watch

VIEWER_DIR = Path(__file__).parent / "viewer"


class _Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, out_dir: Path, **kwargs: Any):
        self.out_dir = out_dir
        super().__init__(*args, directory=str(VIEWER_DIR), **kwargs)

    def translate_path(self, path: str) -> str:
        path = path.split("?", 1)[0].split("#", 1)[0]
        if path.startswith("/out/"):
            return str(self.out_dir / path[len("/out/"):])
        return super().translate_path(path)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, format: str, *args: Any) -> None:
        pass


def rebuild(build_file: Path, out_dir: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "lang.build", str(build_file), "--out", str(out_dir)],
        capture_output=True, text=True, cwd=str(Path(__file__).resolve().parents[2]),
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "build.log").write_text(result.stdout + result.stderr)
    status = "ok" if result.returncode == 0 else "FAILED"
    print(f"build {status}: {(result.stdout + result.stderr).strip()}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("build_file")
    parser.add_argument("--out", default="out")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    build_file = Path(args.build_file).resolve()
    out_dir = Path(args.out).resolve()
    rebuild(build_file, out_dir)

    handler = functools.partial(_Handler, out_dir=out_dir)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"preview at http://127.0.0.1:{args.port}/  (watching {build_file.parent})")

    lang_dir = Path(__file__).resolve().parents[1]
    try:
        for changes in watch(build_file.parent, lang_dir):
            if any(Path(p).suffix == ".py" for _, p in changes):
                rebuild(build_file, out_dir)
    except KeyboardInterrupt:
        pass
    server.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
