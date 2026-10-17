"""The preview server's bookkeeping (`lang.preview.__main__`): which files
of a folder are build files, which designs a change makes stale, which
ones it builds, a build that fails or runs too long keeping the last good
one, and the files it serves."""
import os
from pathlib import Path
from typing import Any

import pytest

from lang.preview.__main__ import VIEWER_DIR, Designs, _Handler, nest_state, rebuild, renest, scan  # type: ignore[reportPrivateUsage]

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"

CABINET = '''from lang import *

def cabinet(name: str) -> None:
    with module(name, Box.from_size(width=300, depth=200, height=400)) as m:
        board("left", sheet_material("birch", t=15)).on(m.left)

if __name__ == "__build__":   # run as the build file, not imported
    cabinet("cabinet")
'''


def write(folder: Path, name: str, text: str) -> Path:
    path = folder / name
    path.write_text(text)
    return path


def folder_of_files(tmp_path: Path) -> Path:
    write(tmp_path, "cabinet.py", CABINET)
    write(tmp_path, "van.py", "from lang import *\nfrom cabinet import cabinet\nfrom parts import ply\n\ncabinet('kitchen')\n")
    write(tmp_path, "parts.py", "from lang import *\n\nply = sheet_material('birch', t=15)\n")
    write(tmp_path, "shelf.py", "from lang import *\nfrom lang.core import scope\n\nwith module(\n")    # mid-edit
    write(tmp_path, "notes.py", "print('no lang here')\n")
    write(tmp_path, "__init__.py", "from lang import *\n")
    write(tmp_path, "_scratch.py", "from lang import *\n")
    write(tmp_path, "van_snapshot.json", "{}\n")
    return tmp_path


def stale(designs: Designs) -> set[str]:
    return {name for name, design in designs.designs.items() if design.stale}


def fresh(designs: Designs) -> None:
    for design in designs.designs.values():
        design.stale = False


def test_build_files_import_lang_and_libraries_are_not_listed(tmp_path: Path):
    files, imported = scan(folder_of_files(tmp_path))
    # parts.py is imported and builds nothing of its own; cabinet.py is
    # imported too but keeps a build of its own; shelf.py does not parse.
    assert [path.name for path in files] == ["cabinet.py", "shelf.py", "van.py"]
    assert imported == {"cabinet", "parts"}


def test_the_examples_are_build_files():
    files, _ = scan(EXAMPLES)
    names = {path.stem for path in files}
    assert {"drawer_cabinet", "van", "shelf", "cutouts"} <= names
    assert "stock" not in names          # a library the build files import


def test_a_save_makes_its_own_design_stale_and_a_shared_module_all(tmp_path: Path):
    folder = folder_of_files(tmp_path)
    designs = Designs(folder, tmp_path / "out")
    assert set(designs.designs) == {"cabinet", "shelf", "van"}
    fresh(designs)
    designs.changed({folder / "shelf.py"})
    assert stale(designs) == {"shelf"}
    for shared in (folder / "cabinet.py", folder / "parts.py", folder / "van_snapshot.json",
                   Path(__file__).resolve().parents[1] / "lang" / "build.py"):
        fresh(designs)
        designs.changed({shared})
        assert stale(designs) == {"cabinet", "shelf", "van"}, shared


def test_new_build_files_show_up_and_deleted_ones_go(tmp_path: Path):
    folder = folder_of_files(tmp_path)
    designs = Designs(folder, tmp_path / "out")
    fresh(designs)
    door = write(folder, "door.py", "from lang import *\n")
    designs.changed({door})
    assert list(designs.designs) == ["cabinet", "door", "shelf", "van"]
    assert stale(designs) == {"door"}
    assert designs.designs["door"].out == tmp_path / "out" / "door"
    door.unlink()
    designs.changed({door})
    assert list(designs.designs) == ["cabinet", "shelf", "van"]


def test_what_counts_as_a_change(tmp_path: Path):
    folder = folder_of_files(tmp_path)
    designs = Designs(folder, folder / "out")
    assert designs.counts(folder / "van.py")
    assert designs.counts(folder / "van_snapshot.json")
    assert not designs.counts(folder / "__pycache__" / "cabinet.cpython-313.pyc")
    assert not designs.counts(folder / "out" / "van" / "layout.json")


def test_only_the_designs_pages_show_are_built(tmp_path: Path):
    designs = Designs(folder_of_files(tmp_path), tmp_path / "out")
    assert designs.next_build() is None                  # no page open
    state = designs.status("van", page="a")
    assert state["designs"] == ["cabinet", "shelf", "van"]
    assert state["design"] == {"name": "van", "url": "out/van/", "version": None, "built": None, "level": "normal",
                               "builds": 0, "state": "building", "nests": []}
    assert designs.next_build() is designs.designs["van"]
    designs.status("cabinet", page="a")                  # the page switched
    assert designs.next_build() is designs.designs["cabinet"]
    designs.designs["cabinet"].stale = False
    assert designs.next_build() is None
    assert designs.status("gone", page="a")["design"] is None


def test_a_single_build_file_builds_without_a_page(tmp_path: Path):
    path = write(tmp_path, "cabinet.py", CABINET)
    designs = Designs(path, tmp_path / "out")
    assert designs.next_build() is designs.designs["cabinet"]
    assert designs.designs["cabinet"].url == "out/"
    designs.designs["cabinet"].stale = False
    designs.changed({tmp_path / "other.py"})
    assert stale(designs) == {"cabinet"}


def test_a_level_asked_for_is_kept_per_design_and_builds_it_again(tmp_path: Path):
    designs = Designs(folder_of_files(tmp_path), tmp_path / "out")
    fresh(designs)
    van = designs.designs["van"]
    assert designs.status("van", page="a")["design"]["level"] == "normal"
    designs.status("van", page="a", level="rough")       # no such level
    assert van.level == "normal" and stale(designs) == set()
    state = designs.status("van", page="a", level="fine")["design"]
    assert (state["level"], state["state"], state["built"]) == ("fine", "building", None)
    assert stale(designs) == {"van"} and designs.designs["cabinet"].level == "normal"
    fresh(designs)
    designs.status("van", page="b", level="fine")         # the level it has: nothing to build
    assert stale(designs) == set()
    assert designs.status("van", page="a")["design"]["level"] == "fine"      # kept, for every page
    assert rebuild(van.file, van.out, level=van.level)
    assert designs.status("van", page="a")["design"]["built"] == "fine"
    assert (van.out / "level.txt").read_text() == "fine"


def test_a_failed_build_keeps_the_last_good_one(tmp_path: Path):
    path = write(tmp_path, "cabinet.py", CABINET)
    out = tmp_path / "out"
    assert rebuild(path, out)
    version = (out / "version.txt").read_text()
    assert {p.name for p in out.iterdir()} == {".mesh", "build.log", "layout.json", "scene.glb", "level.txt", "version.txt"}
    assert "1 parts" in (out / "build.log").read_text()
    path.write_text(CABINET + "    undefined_name()\n")
    assert not rebuild(path, out)
    assert (out / "version.txt").read_text() == version
    assert "NameError" in (out / "build.log").read_text()
    assert not (out / ".build").exists()


def test_a_build_that_runs_too_long_is_stopped_and_keeps_the_last_good_one(tmp_path: Path):
    build = write(tmp_path, "cabinet.py", CABINET)
    out = tmp_path / "out"
    assert rebuild(build, out)
    good = (out / "version.txt").read_text()
    write(tmp_path, "cabinet.py", "from lang import *\nwhile True:\n    pass\n")
    assert not rebuild(build, out, timeout=1.0)
    assert (out / "version.txt").read_text() == good
    assert "took longer than 1 s and was stopped" in (out / "build.log").read_text()


NESTED = """from lang import *
ply = sheet_material('birch', t=15, size=(2470, 1240))
use(nesting.bed((2000, 1000)), nesting.seconds(0.3), nesting.refill(False))
with module('cabinet', Box.from_size(width=300, depth=200, height=400)) as m:
    board('left', ply).on(m.left)
    board('right', ply).on(m.right)
    m.nest('sides', [m['left']])
"""


def _entry(path: str, folder: str, state: str = "none") -> dict[str, object]:
    return {"path": path, "dir": folder, "follows": "", "state": state, "sheets": [], "made": [], "changed": [],
            "new": [], "gone": []}


def test_the_nests_listed_say_what_changed_since_by_their_parts(tmp_path: Path):
    path = write(tmp_path, "cabinet.py", NESTED)
    designs = Designs(path, tmp_path / "out")
    design = designs.designs["cabinet"]
    assert nest_state(design) == []                                # not built yet
    assert rebuild(path, design.out)
    assert nest_state(design) == [_entry("cabinet.sides", "cabinet/sides/"),
                                  _entry("cabinet.birch_15", "cabinet/birch_15/")]
    assert designs.ask_nest("cabinet", "cabinet.sides")
    assert not designs.ask_nest("gone", "cabinet.sides") and not designs.ask_nest("cabinet", "cabinet.oak")
    assert nest_state(design)[0]["state"] == "running" and nest_state(design)[1]["state"] == "none"
    assert renest(path, design.out, "cabinet.sides", "cabinet/sides")
    design.nesting.clear()
    state = nest_state(design)[0]
    assert state["state"] == "ok" and state["version"] and state["sheets"] == [["birch 15", "1"]]
    folder = design.out / "cabinet" / "sides"
    assert {"nest.json", "nest.svg", "nest.layout.json", "nest.log"} <= {p.name for p in folder.iterdir()}
    assert not (design.out / "cabinet" / "birch_15").exists()           # only the nest asked for
    # Another part changed: the nest still holds, by its parts' fingerprints.
    write(tmp_path, "cabinet.py", NESTED.replace("board('right', ply).on(m.right)",
                                                 "board('right', ply).on(m.right).hole(8, depth=5)"))
    assert rebuild(path, design.out)
    assert nest_state(design)[0]["state"] == "ok"
    write(tmp_path, "cabinet.py", NESTED.replace("board('left', ply).on(m.left)",
                                                 "board('left', ply).on(m.left).hole(8, depth=5)"))
    assert rebuild(path, design.out)
    state = nest_state(design)[0]
    assert state["state"] == "changed" and state["changed"] == ["cabinet.left"]


def test_the_status_reads_a_built_layout_once_however_often_the_page_asks(tmp_path: Path,
                                                                          monkeypatch: pytest.MonkeyPatch):
    path = write(tmp_path, "cabinet.py", NESTED)
    designs = Designs(path, tmp_path / "out")
    design = designs.designs["cabinet"]
    assert rebuild(path, design.out)
    reads: list[Path] = []
    read_text = Path.read_text

    def counted(self: Path, *args: Any, **kwargs: Any) -> str:
        if self.name == "layout.json":
            reads.append(self)
        return read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", counted)
    for _ in range(3):
        status = designs.status("cabinet")["design"]
        assert [n["path"] for n in status["nests"]] == ["cabinet.sides", "cabinet.birch_15"]
    assert len(reads) == 1
    assert rebuild(path, design.out)        # the same layout written again is read again
    assert len(designs.status("cabinet")["design"]["nests"]) == 2 and len(reads) == 2


def test_marks_go_through_the_server_and_the_nests_say_what_is_made(tmp_path: Path):
    path = write(tmp_path, "cabinet.py", NESTED)
    designs = Designs(path, tmp_path / "out")
    design = designs.designs["cabinet"]
    assert rebuild(path, design.out) and renest(path, design.out, "cabinet.sides", "cabinet/sides")
    assert designs.pin("cabinet", ["--made", "cabinet.oak"])[0] == 400
    status, text = designs.pin("cabinet", ["--made", "cabinet.sides"])
    assert status == 200 and "marked as made: birch 15 sheet 1" in text
    (sides, _default) = nest_state(design)
    assert sides["state"] == "made" and sides["made"] == [["birch 15", "1"]]
    assert sides["changed"] == [] and sides["not_made"] == [] and sides["made_parts"] == {
        "cabinet.left": "cabinet.sides birch 15 sheet 1"}
    write(tmp_path, "cabinet.py", NESTED.replace("board('left', ply).on(m.left)",
                                                 "board('left', ply).on(m.left).hole(8, depth=5)"))
    assert rebuild(path, design.out)
    sides, second, _default = nest_state(design)
    assert sides["state"] == "made" and sides["changed"] == ["cabinet.left"]
    assert second == {**_entry("cabinet.sides-2", "cabinet/sides-2/"), "follows": "cabinet.sides"}
    assert designs.ask_nest("cabinet", "cabinet.sides-2") and design.nesting == ["cabinet.sides"]
    assert designs.pin("cabinet", ["--made", "cabinet.sides"])[0] == 409          # while it nests
    design.nesting.clear()
    status, text = designs.pin("cabinet", ["--fixed", "cabinet.sides", "cabinet.left"])
    assert status == 200 and "fixed by hand" in text
    sides, _default = nest_state(design)
    assert sides["changed"] == [] and sides["made_parts"] == {"cabinet.left": "fixed"}


def test_a_failed_nest_says_why(tmp_path: Path):
    path = write(tmp_path, "cabinet.py", CABINET)
    out = tmp_path / "out"
    designs = Designs(path, out)
    design = designs.designs["cabinet"]
    assert rebuild(path, out)
    assert not renest(path, out, "cabinet.birch_15", "cabinet/birch_15")       # no bed set anywhere
    design.nest_failed.add("cabinet.birch_15")
    (state,) = nest_state(design)
    assert state["state"] == "failed" and "no nesting.bed is used for it" in state["log"]


def _handler(out: Path) -> _Handler:
    """A request handler without a request, for its path translation."""
    handler = _Handler.__new__(_Handler)
    handler.designs = Designs(write(out.parent, "cabinet.py", CABINET), out)
    handler.directory = str(VIEWER_DIR)
    return handler


def test_the_server_serves_nothing_outside_out(tmp_path: Path):
    real = tmp_path / "real"
    real.mkdir()
    os.symlink(real, tmp_path / "out")          # --out given through a symlink
    out = tmp_path / "out"
    (out / "cabinet").mkdir(parents=True)
    (out / "cabinet" / "layout.json").write_text("{}")
    (tmp_path / "secret.txt").write_text("no")
    os.symlink(tmp_path / "secret.txt", out / "link.txt")
    handler = _handler(out)
    assert handler.translate_path("/out/cabinet/layout.json?v=3") == str((out / "cabinet" / "layout.json").resolve())
    for escape in ("/out/../secret.txt", "/out/%2e%2e/secret.txt", "/out/cabinet/../../secret.txt", "/out/link.txt"):
        assert handler.translate_path(escape) == str(out.resolve() / "missing"), escape
    assert handler.translate_path("/index.html") == str(VIEWER_DIR / "index.html")
