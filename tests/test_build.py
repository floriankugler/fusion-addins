"""Errors of a build as `python -m lang.build` prints them: the message and
the build files' own lines, without runpy's, lang.build's or the language's
frames."""
from pathlib import Path

import pytest

from lang.build import main

HEAD = """from lang import *
ply = sheet_material("birch", t=15)
with module("m", Box.from_size(width=400, depth=300, height=100)) as m:
    with board("panel", ply).on(m.bottom).show(m.top) as panel:
"""


def build_error(tmp_path: Path, capsys: pytest.CaptureFixture[str], body: str, name: str = "bad.py") -> list[str]:
    (tmp_path / name).write_text(HEAD + body)
    assert main([str(tmp_path / name), "--out", str(tmp_path / "out"), "--no-scene"]) == 1
    return capsys.readouterr().err.splitlines()


def test_language_error_names_the_line(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    lines = build_error(tmp_path, capsys, '        panel.hole(d=5, at=panel.top.center, depth=through, name="a")\n'
                                          '        panel.hole(d=5, at=panel.top.center, depth=through, name="a")\n')
    assert lines[0] == "error: m.panel: operation name 'a' used twice."
    assert lines[1].endswith('bad.py:6: panel.hole(d=5, at=panel.top.center, depth=through, name="a")')
    assert len(lines) == 2


def test_python_error_in_the_build_keeps_its_hint(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    lines = build_error(tmp_path, capsys, '        panel.hole(d=5, at=panel.top.center, nme="a")\n')
    assert lines[0].startswith("TypeError: ") and "Did you mean 'name'?" in lines[0]
    assert lines[1].endswith('bad.py:5: panel.hole(d=5, at=panel.top.center, nme="a")')
    assert len(lines) == 2
    assert not any("runpy" in line or "lang/build.py" in line for line in lines)


def test_error_raised_inside_the_language_names_where(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    lines = build_error(tmp_path, capsys, '        panel.cut(circle("x"), at=panel.top.center)\n')
    assert lines[0].startswith("TypeError: ")
    assert lines[1].endswith('bad.py:5: panel.cut(circle("x"), at=panel.top.center)')
    assert lines[2].startswith("  raised in ") and "lang/core/shapes.py:" in lines[2] and "(circle)" in lines[2]


def test_lines_of_every_build_file_on_the_way(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    (tmp_path / "build_helper_a.py").write_text(
        "from lang import through\n"
        "def holes(panel):\n"
        "    for _ in range(2):\n"
        "        panel.hole(d=5, at=panel.top.center, depth=through, name=\"x\")\n")
    lines = build_error(tmp_path, capsys, "        from build_helper_a import holes\n        holes(panel)\n")
    assert lines[0] == "error: m.panel: operation name 'x' used twice."
    assert lines[1].endswith("bad.py:6: holes(panel)")
    assert lines[2].endswith('build_helper_a.py:4: panel.hole(d=5, at=panel.top.center, depth=through, name="x")')
    assert len(lines) == 3


def test_syntax_error(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    lines = build_error(tmp_path, capsys, "        x = (\n")
    assert lines[0] == "SyntaxError: '(' was never closed"
    assert lines[1].endswith("bad.py:5: x = (")
    assert len(lines) == 2


def test_an_error_in_a_lazy_body_names_the_bodys_line(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    """A module type's body runs when its parts are first needed, at the
    latest after the build file ran; its error names its own lines."""
    (tmp_path / "lazy.py").write_text(
        "from lang import *\n"
        "@module\n"
        "def shelf(cab: Scope) -> None:\n"
        "    panel = board(\"panel\", sheet_material(\"birch\", t=15)).on(cab.bottom)\n"
        "    panel.chamfer(panel.top.front)\n"
        "shelf(Box.from_size(width=400, depth=300, height=100))\n")
    assert main([str(tmp_path / "lazy.py"), "--out", str(tmp_path / "out"), "--no-scene"]) == 1
    lines = capsys.readouterr().err.splitlines()
    assert lines[0].startswith("error: the chamfer of shelf.panel reads chamfer_size, which has no default")
    assert lines[1].endswith("lazy.py:5: panel.chamfer(panel.top.front)")
    assert len(lines) == 2


def _lazy_error(tmp_path: Path, capsys: pytest.CaptureFixture[str], text: str) -> list[str]:
    (tmp_path / "lazy.py").write_text(text)
    assert main([str(tmp_path / "lazy.py"), "--out", str(tmp_path / "out"), "--no-scene"]) == 1
    return capsys.readouterr().err.splitlines()


def test_a_board_without_material_found_at_the_layout_names_its_line(tmp_path: Path,
                                                                     capsys: pytest.CaptureFixture[str]):
    """A board resolves lazily, so a material missing along its chain is
    found at the layout, where no line of the build file is on the stack:
    the error starts with the board's line, a loop's line for its boards."""
    lines = _lazy_error(tmp_path, capsys,
                        "from lang import *\n"
                        "with module('floor', Box.from_size(width=1000, depth=600, height=100)) as floor:\n"
                        "    for i in range(3):\n"
                        "        board(f'batten{i}').on(floor.bottom).between(floor.left.into(100 * i),\n"
                        "                                                     floor.left.into(100 * i + 40))\n")
    assert lines[0].startswith("error: ") and lines[0].endswith(
        "lazy.py:4: floor.batten0 reads material, which has no default and is set nowhere above it; "
        "board(name, material) gives a board its own, or use(material(...)) in a scope above sets it for "
        "everything in it.")
    assert len(lines) == 1


def test_a_board_found_wrong_on_its_own_line_names_it_once(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    """Where the board is found wrong on the line that made it, that line
    is the message's and not repeated below it; found on a later line, the
    message names the board's line and the stack the later one."""
    lines = _lazy_error(tmp_path, capsys,
                        "from lang import *\n"
                        "with module('m', Box.from_size(width=400, depth=300, height=100)) as m:\n"
                        "    board('shelf').on(m.bottom).hole(5, depth=through)\n")
    assert lines[0].startswith("error: ") and "lazy.py:3: m.shelf reads material" in lines[0]
    assert len(lines) == 1
    lines = _lazy_error(tmp_path, capsys,
                        "from lang import *\n"
                        "with module('m', Box.from_size(width=400, depth=300, height=100)) as m:\n"
                        "    shelf = board('shelf', sheet_material('birch', t=15))\n"
                        "    shelf.hole(5, depth=through)\n")
    assert lines[0].startswith("error: ") and lines[0].endswith("lazy.py:3: m.shelf: no placement: give on() or "
                                                                 "center().")
    assert lines[1].endswith("lazy.py:4: shelf.hole(5, depth=through)") and len(lines) == 2


def test_an_inherited_grain_along_the_thickness_names_the_boards_line(tmp_path: Path,
                                                                      capsys: pytest.CaptureFixture[str]):
    lines = _lazy_error(tmp_path, capsys,
                        "from lang import *\n"
                        "use(grain('height'))\n"
                        "with module('m', Box.from_size(width=400, depth=300, height=100)) as m:\n"
                        "    board('bottom', sheet_material('birch', t=15)).on(m.bottom)\n")
    assert lines[0].startswith("error: ") and lines[0].endswith(
        "lazy.py:4: m.bottom: grain z from root is the thickness axis of this board; give it a grain() of its "
        "own.")
    assert len(lines) == 1
