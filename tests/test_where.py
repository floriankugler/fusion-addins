"""The build file's lines (`lang.core.where`): every part, module, hardware
item and operation names the line that made it, the innermost one outside
the language, and the layout carries it as `where`."""
from __future__ import annotations

import copy
import linecache
import re
from pathlib import Path

import pytest

from lang import Box, LangError, Scope, board, cabineo, domino, grain, hinge, module, rect, use
from lang.build import layout_of
from lang.core.layout import build_layout
from lang.core.layout_types import OpLayout
from lang.core.where import build_line, shown, where
from lang.preview.levels import NORMAL
from lang.preview.mesh import part_key
from lang.std import carcass

from helpers import EXAMPLES, ply9, ply12, ply15

HERE = shown(__file__)
BOX = Box.from_size(width=600, depth=500, height=720)
TEXT = Path(__file__).read_text().splitlines()


def at(mark: str) -> str:
    """The line of this file marked `# @mark`, as `where` names it."""
    (n,) = [i for i, line in enumerate(TEXT, 1) if line.rstrip().endswith(f"# @{mark}")]
    return f"{HERE}:{n}"


def _made_here() -> str:
    return where()


def test_a_line_is_the_innermost_frame_outside_the_language():
    """A function of the build's own counts as the build's: the line is
    the one in it, not its caller's."""
    assert where() == at("here")                                          # @here
    assert _made_here() == f"{HERE}:{TEXT.index('    return where()') + 1}"


def test_build_line_keeps_the_code():
    line = build_line()                                                   # @build_line
    assert line == f"{at('build_line')}: line = build_line()" + " " * 51 + "# @build_line"


def test_a_board_names_the_line_that_made_it():
    with module("m", BOX) as m:                                           # @module
        side = board("side", ply15).on(m.left)                            # @board
        side.hole(8, at=side.inner.center, depth=5)                       # @hole
        side.chamfer(side.inner.front, 1)                                 # @chamfer
    assert m.where == at("module")
    assert side.where == at("board")
    assert [op.where for op in side.ops] == [at("hole"), at("chamfer")]


def test_a_loops_boards_share_its_line():
    with module("m", BOX) as m:
        boards = [board(f"shelf{i}", ply15).on(m.bottom.into(100 * i)) for i in range(3)]     # @loop
        for b in boards:
            b.cut(rect(width=50, depth=50), at=b.top.front.left)          # @loop_cut
    assert {b.where for b in boards} == {at("loop")}
    assert {op.where for b in boards for op in b.ops} == {at("loop_cut")}


def test_a_join_names_its_line_in_both_boards():
    with module("m", BOX) as m:
        left = board("left", ply15).on(m.left)                            # @left
        right = board("right", ply15).on(m.right)
        bottom = board("bottom", ply15).on(m.bottom).between(left, right)
        bottom.join(left, right, using=cabineo(count=2))                  # @join
    joined = [op for b in (left, right, bottom) for op in b.ops]
    assert all(b.ops for b in (left, right, bottom)) and {op.where for op in joined} == {at("join")}
    assert left.where == at("left")


def test_the_standard_library_names_the_build_files_call():
    """A board `carcass()` makes, and every operation its joins make, has
    the line of the `carcass(...)` call, not the library's own."""
    with module("cab", BOX, front=BOX.right) as cab:
        c = carcass(cab, ply15, back=ply9, toekick=(60, 100), joins=domino("4x20", count=2))      # @carcass
    assert [b.where for b in c] == [at("carcass")] * 5
    assert {op.where for b in c for op in b.ops} == {at("carcass")}


def test_hardware_names_the_mount_line():
    with module("cab", Box.from_size(width=500, depth=350, height=700)) as cab:
        behind = cab.front.into(12)
        side = board("side", ply15).on(cab.left).between(behind)
        door = board("door", ply12).on(cab.front).inset(1.5)
        cab.mount(hinge(), door=door, carcass=side)                       # @mount
    (item,) = cab.hardware
    assert item["where"] == at("mount")
    assert {op.where for b in (side, door) for op in b.ops} == {at("mount")}


def test_a_lazy_module_names_the_call_that_made_it():
    @module
    def shelf(s: Scope) -> None:
        board("panel", ply15).on(s.bottom)                                # @body
    made = shelf(BOX)                                                     # @call
    assert made.where == at("call")
    assert made.part("panel").where == at("body")


def test_an_edge_operation_and_its_inner_one_share_the_line():
    with module("m", BOX) as m:
        side = board("side", ply15).on(m.left)
        side.hole(5, at=side.top.center, depth=20)                        # @edge
    layout = build_layout()
    (op,) = layout["modules"][0]["parts"][0]["ops"]
    assert op["kind"] == "edge" and op["where"] == op["op"]["where"] == at("edge")


def test_the_layout_names_the_line_of_everything_in_the_examples():
    """Every module, part, hardware item and operation of the examples
    carries the build file's line, a line of code in one of the example
    files, of every kind of operation."""
    kinds: set[str] = set()
    for path in sorted(EXAMPLES.glob("*.py")):
        if path.name.startswith("_") or "import" not in path.read_text() or path.stem == "stock":
            continue
        layout = layout_of(path)
        for module_ in layout["modules"]:
            things: list[tuple[str, str]] = [] if module_["path"] == "" else [(module_["path"], module_["where"])]
            things += [(p["path"], p["where"]) for p in module_["parts"]]
            things += [(h["path"], h["where"]) for h in module_["hardware"]]
            for part in module_["parts"]:
                for op in part["ops"]:
                    kinds.add(op["kind"])
                    things.append((f"{part['path']}#{op['kind']}", op["where"]))
                    if op["kind"] == "edge":
                        things.append((f"{part['path']}#edge.op", op["op"]["where"]))
            for what, line in things:
                assert re.fullmatch(r"(.*/)?examples/\w+\.py:\d+", line), f"{path.name}: {what} names {line!r}"
                file, number = line.rsplit(":", 1)
                assert linecache.getline(file, int(number)).strip(), f"{path.name}: {what} names an empty line"
    assert kinds == {"cut", "pocket", "hole", "chamfer", "vgroove", "edge"}


def test_a_line_moved_meshes_nothing_again():
    """The mesh cache's key leaves the lines out: a line inserted above a
    part in the build file changes every `where` below it, not its mesh."""
    with module("m", BOX) as m:
        side = board("side", ply15).on(m.left)
        side.hole(5, at=side.top.center, depth=20)
        side.cut(rect(depth=50, height=50), at=side.inner.front.bottom)
    part = build_layout()["modules"][0]["parts"][0]
    moved = copy.deepcopy(part)
    moved["where"] = "examples/van.py:99"
    for op in moved["ops"]:
        op["where"] = "examples/van.py:100"
        if op["kind"] == "edge":
            op["op"]["where"] = "examples/van.py:100"
    frame = {"front": "-x"}
    assert part_key(moved, frame, NORMAL) == part_key(part, frame, NORMAL)
    fewer: list[OpLayout] = moved["ops"][1:]
    moved["ops"] = fewer
    assert part_key(moved, frame, NORMAL) != part_key(part, frame, NORMAL)


# -- errors -------------------------------------------------------------------------------------

def test_an_error_found_resolving_a_board_starts_with_its_line():
    """Placement, material and an inherited grain are found when the board
    resolves, at the layout as likely as at a later line; the error names
    the board's own line."""
    with module("m", BOX) as m:
        loose = board("loose", ply15)                                     # @no_placement
        bare = board("bare").on(m.left)                                   # @no_material
    with pytest.raises(LangError, match=rf"^{re.escape(at('no_placement'))}: m\.loose: no placement"):
        loose.box()
    with pytest.raises(LangError, match=rf"^{re.escape(at('no_material'))}: m\.bare reads material"):
        _ = bare.inner
    with module("g", BOX) as g:
        use(grain("height"))
        flat = board("flat", ply15).on(g.bottom)                          # @grain
    with pytest.raises(LangError, match=rf"^{re.escape(at('grain'))}: g\.flat: grain z from g is the thickness"):
        flat.to_layout()


def test_the_innermost_board_found_wrong_names_its_line():
    """A board limited by another that cannot resolve names the other's
    line: the error is about that one."""
    with module("m", BOX) as m:
        left = board("left", ply15)                                       # @unplaced
        shelf = board("shelf", ply15).on(m.bottom).between(left, m.right)
    with pytest.raises(LangError, match=rf"^{re.escape(at('unplaced'))}: m\.left: no placement"):
        shelf.box()


def test_locate_keeps_the_first_line_and_the_traceback():
    error = LangError("no placement: give on() or center().", "m.b")
    assert str(error) == "m.b: no placement: give on() or center()."
    error.locate("examples/van.py:45")
    error.locate("examples/van.py:50")
    assert error.where == "examples/van.py:45"
    assert str(error) == "examples/van.py:45: m.b: no placement: give on() or center()."
    error.locate("")
    assert str(error).startswith("examples/van.py:45: ")

