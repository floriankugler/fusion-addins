"""Errors of a build as `python -m lang.build` prints them: the message and
the build files' own lines, without runpy's, lang.build's or the language's
frames."""
from pathlib import Path

import pytest

from lang.build import main

HEAD = """from lang import *
ply = material("birch", t=15)
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
