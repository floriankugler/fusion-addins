"""Pinning (`lang.nesting.pinning`, `ledger`): nests marked as made, whole
or by sheets, in the state file; a nest marked frozen, what is not made of
it nested into a second nest beside it, parts gone reported, parts fixed
by hand left alone; and the inventory written back on a mark only,
keeping Florian's comments and order, once per sheet."""
from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

import pytest

from lang import LangError
from lang.nesting.__main__ import main as nest_main
from lang.nesting.inventory import inventory_from, read_inventory
from lang.nesting.ledger import NEW_FILE, Change, Piece, rewrite, write_back
from lang.nesting.nest_types import NEST_VERSION, NestFile
from lang.nesting.pinning import (FIXED, STATE, chain, changes, chosen_sheets, empty, fix, mark, open_name,
                                  read_nest, read_state, second_folder, second_name, standing, write_state)
from lang.nesting.workshop import OnHand

WHEN = "2026-10-16T17:00:00+02:00"
Sheet = tuple[str, str, bool, tuple[float, float], list[tuple[str, str]], list[tuple[float, float, bool]]]


def nest_file(name: str, sheets: list[Sheet], follows: str = "", written: str = "2026-10-16T09:00:00+02:00",
              unplaced: tuple[str, ...] = ()) -> NestFile:
    """A nest file of sheets given as (material, name, bought, size, parts
    as (path, fingerprint), rests as (w, h, kept))."""
    materials: dict[str, dict[str, Any]] = {}
    for material, sheet, bought, size, parts, rests in sheets:
        m = materials.setdefault(material, {"material": material, "thickness": 15.0, "sheets": [], "bought": {},
                                            "on_hand_used": [], "parts_area": 0.0, "stock_area": 0.0,
                                            "kept_area": 0.0, "used_area": 0.0, "unplaced": [], "notes": []})
        m["sheets"].append({
            "name": sheet, "stock": "sheet", "bought": bought, "size": list(size), "cuts": [],
            "blanks": [{"name": f"{sheet}.1", "rect": [0, 0, 100, 100], "own_blank": False,
                        "parts": [{"path": p, "fingerprint": f, "up": "top", "turn": 0.0, "at": [0, 0],
                                   "transform": []} for p, f in parts]}],
            "rests": [{"rect": [0, 0, w, h], "keep": keep} for w, h, keep in rests]})
    if unplaced:
        next(iter(materials.values()))["unplaced"] = list(unplaced)
    return {"version": NEST_VERSION, "name": name, "follows": follows, "reasons": {}, "written": written,
            "source": "", "layout_hash": "", "settings": {}, "materials": list(materials.values()),  # pyright: ignore[reportReturnType]
            "left_out": [], "problems": []}


TWO = nest_file("m.carcass", [
    ("birch 15", "1", False, (1250, 600), [("m.left", "a1"), ("m.right", "b1")], [(400, 300, True), (100, 50, False)]),
    ("birch 15", "2", True, (2500, 1250), [("m.top", "c1"), ("m.bottom", "d1")], [(1200, 600, True)]),
])


# -- the ledger --------------------------------------------------------------------------------------

LEDGER = """# My stock, on the shelf by the door.

[[stock]]
material = "birch 15"   # the good one
size = [1250, 600]
count = 2   # two of them

# A loose note about what follows.

# The offcut from the kitchen
[[stock]]
material = "birch 15"
size = [900, 450]

[[stock]]
material = "birch 9"
# damaged corner
size = [800, 400]
"""


def test_a_piece_used_lowers_its_count_and_keeps_the_comments():
    new, notes = rewrite(LEDGER, Change(taken=(Piece("birch 15", 1250, 600),)))
    assert new == LEDGER.replace("count = 2   # two of them", "count = 1   # two of them")
    assert notes == ["inventory: -1 birch 15 1250x600"]


def test_a_piece_used_up_goes_with_the_comment_above_it_and_the_rest_stays_in_order():
    new, _notes = rewrite(LEDGER, Change(taken=(Piece("birch 15", 900, 450),)))
    assert "# The offcut from the kitchen" not in new and "900, 450" not in new
    assert "# A loose note about what follows." in new and "# damaged corner" in new
    assert new.index("1250, 600") < new.index("# A loose note") < new.index("800, 400")
    assert "\n\n\n" not in new
    assert inventory_from(tomllib.loads(new)) == [OnHand("birch 15", 1250, 600, 2), OnHand("birch 9", 800, 400)]


def test_rests_kept_go_in_at_the_end_with_where_they_came_from():
    note = "kept from m.carcass birch 15 sheet 2, marked made 2026-10-16"
    new, notes = rewrite(LEDGER, Change(added=((Piece("birch 15", 1294.5, 1240), note),
                                               (Piece("birch 15", 400, 300), note), (Piece("birch 15", 400, 300), note))))
    assert new.startswith(LEDGER)
    assert new[len(LEDGER):] == (f"\n# {note}\n[[stock]]\nmaterial = \"birch 15\"\nsize = [1294.5, 1240]\n"
                                 f"\n# {note}\n[[stock]]\nmaterial = \"birch 15\"\nsize = [400, 300]\ncount = 2\n")
    assert notes == ["inventory: +1 birch 15 1294.5x1240", "inventory: +2 birch 15 400x300"]


def test_a_piece_the_ledger_no_longer_has_is_noted_not_an_error():
    new, notes = rewrite(LEDGER, Change(taken=(Piece("oak 20", 500, 500), Piece("birch 9", 800, 400),
                                               Piece("birch 9", 800, 400))))
    assert notes == ["inventory: no oak 20 500x500 left to take out (used elsewhere?); left as it is",
                     "inventory: -1 birch 9 800x400",
                     "inventory: no birch 9 800x400 left to take out (used elsewhere?); left as it is"]
    assert "800, 400" not in new and "# damaged corner" not in new


def test_a_ledger_written_from_nothing_says_what_it_is(tmp_path: Path):
    path = tmp_path / "inventory.toml"
    assert write_back(path, Change()) == [] and not path.exists()
    write_back(path, Change(added=((Piece("birch 15", 600, 400), "kept"),)))
    assert path.read_text().startswith(NEW_FILE) and read_inventory(path) == [OnHand("birch 15", 600, 400)]


@pytest.mark.parametrize("text, message", [
    ("[[stock]\nmaterial = 1", "Expected"),
    ('[[stock]]\nmaterial = "birch 15"\nsize = [1, 2]\ncolour = "red"\n', "unknown key colour"),
    ('stock = [{material = "birch 15", size = [600, 400]}]\n', "not written as \\[\\[stock\\]\\] tables"),
    ('[[stock]]\nmaterial = "birch 15"\nsize = [600, 400]\ncount = 0x2\n', "count is not on a line of its own"),
])
def test_a_ledger_it_cannot_read_or_rewrite_is_refused_and_left_as_it_was(tmp_path: Path, text: str, message: str):
    path = tmp_path / "inventory.toml"
    path.write_text(text)
    with pytest.raises(LangError, match=message):
        write_back(path, Change(taken=(Piece("birch 15", 600, 400),), added=((Piece("birch 15", 300, 300), ""),)))
    assert path.read_text() == text


# -- marks and the state file -----------------------------------------------------------------------

def test_a_mark_records_the_sheets_and_their_parts_and_the_ledger_change_once():
    state = empty()
    marked = mark(state, TWO, [("birch 15", "1")], WHEN)
    assert marked.sheets == [("birch 15", "1")] and marked.before == []
    assert marked.change.taken == (Piece("birch 15", 1250, 600),)            # a piece on hand used
    assert [p for p, _note in marked.change.added] == [Piece("birch 15", 400, 300)]   # its kept rest only
    assert state["nests"]["m.carcass"] == {"follows": "", "written": TWO["written"], "sheets": {"birch 15": ["1"]}}
    assert state["made"]["m.carcass"] == {
        "m.left": {"fingerprint": "a1", "by": "m.carcass birch 15 sheet 1", "when": WHEN},
        "m.right": {"fingerprint": "b1", "by": "m.carcass birch 15 sheet 1", "when": WHEN}}
    again = mark(state, TWO, [("birch 15", "1")], WHEN)
    assert again.sheets == [] and again.before == [("birch 15", "1")] and not again.change
    whole = mark(state, TWO, None, WHEN)                       # the rest of it: sheet 2 only
    assert whole.sheets == [("birch 15", "2")] and whole.before == [("birch 15", "1")]
    assert whole.change.taken == () and [p for p, _n in whole.change.added] == [Piece("birch 15", 1200, 600)]
    assert set(state["made"]["m.carcass"]) == {"m.left", "m.right", "m.top", "m.bottom"}


def test_sheets_are_named_by_number_or_by_material_where_two_have_one():
    two = nest_file("m.all", [("birch 15", "1", True, (2500, 1250), [("m.a", "a")], []),
                              ("birch 9", "1", True, (2500, 1250), [("m.b", "b")], []),
                              ("birch 9", "2", True, (2500, 1250), [("m.c", "c")], [])])
    assert chosen_sheets(two, ["2", "birch 15:1", "birch_9:1", "2"]) == [("birch 9", "2"), ("birch 15", "1"),
                                                                       ("birch 9", "1")]
    with pytest.raises(LangError, match="'1' names two sheets; say which material's .*birch 15:1, birch 9:1"):
        chosen_sheets(two, ["1"])
    with pytest.raises(LangError, match="'3' is no sheet of it"):
        chosen_sheets(two, ["3"])


def test_a_nest_file_written_again_after_its_mark_is_refused():
    state = empty()
    mark(state, TWO, [("birch 15", "1")], WHEN)
    later = dict(TWO, written="2026-10-17T09:00:00+02:00")
    with pytest.raises(LangError, match="its file was written 2026-10-17.*after it was marked"):
        mark(state, later, None, WHEN)  # pyright: ignore[reportArgumentType]


def test_second_nests_are_named_after_the_first_with_a_counter_and_marked_in_order():
    state = empty()
    assert open_name(state, "m.carcass") == "m.carcass" and chain(state, "m.carcass") == []
    mark(state, TWO, [("birch 15", "1")], WHEN)
    assert open_name(state, "m.carcass") == second_name("m.carcass", 2) == "m.carcass-2"
    assert second_folder(Path("out/m/carcass"), 2) == Path("out/m/carcass-2")
    third = nest_file("m.carcass-3", [("birch 15", "1", True, (2500, 1250), [("m.top", "c2")], [])],
                      follows="m.carcass")
    with pytest.raises(LangError, match="m.carcass-3 follows m.carcass, whose nests before it are not all marked"):
        mark(state, third, None, WHEN)
    second = nest_file("m.carcass-2", [("birch 15", "1", True, (2500, 1250), [("m.top", "c2")], [])],
                       follows="m.carcass")
    mark(state, second, None, WHEN)
    assert chain(state, "m.carcass") == ["m.carcass", "m.carcass-2"] and open_name(state, "m.carcass") == "m.carcass-3"
    assert state["made"]["m.carcass"]["m.top"]["by"] == "m.carcass-2 birch 15 sheet 1"   # one chain


def test_the_state_file_reads_back_and_refuses_what_it_is_not(tmp_path: Path):
    assert read_state(tmp_path) == empty()
    state = empty()
    mark(state, TWO, None, WHEN)
    write_state(tmp_path, state)
    assert read_state(tmp_path) == state and json.loads((tmp_path / STATE).read_text())["version"] == 1
    (tmp_path / STATE).write_text('{"version": 7}')
    with pytest.raises(LangError, match="not a state file of version 1"):
        read_state(tmp_path)


def test_a_nest_file_without_fingerprints_cannot_be_marked(tmp_path: Path):
    (tmp_path / "nest.json").write_text(json.dumps(dict(TWO, version=2)))
    with pytest.raises(LangError, match="version 2, without its parts' fingerprints; nest it again"):
        read_nest(tmp_path / "nest.json")


# -- a nest marked against the build --------------------------------------------------------------

def test_a_nest_marked_by_sheets_leaves_out_what_is_made_and_nests_the_rest_anew():
    state = empty()
    mark(state, TWO, [("birch 15", "1")], WHEN)
    now = {"m.left": "a1", "m.right": "b2", "m.top": "c1", "m.bottom": "d1", "m.shelf": "e1"}
    st = standing(state, "m.carcass", now, {"m.carcass": TWO})
    assert st.made == {"m.left": "m.carcass birch 15 sheet 1"}
    assert st.changed == ["m.right"] and st.not_made == ["m.top", "m.bottom"] and st.new == ["m.shelf"]
    assert st.reasons == {"m.right": "changed", "m.top": "not made", "m.bottom": "not made", "m.shelf": "new"}


def test_parts_made_and_gone_from_the_build_are_reported():
    state = empty()
    mark(state, TWO, None, WHEN)
    st = standing(state, "m.carcass", {"m.left": "a1", "m.top": "c1"}, {"m.carcass": TWO})
    assert st.gone == ["m.right", "m.bottom"] and st.reasons == {}


def test_a_part_fixed_by_hand_is_made_as_it_is_now_until_it_changes_again():
    state = empty()
    mark(state, TWO, None, WHEN)
    now = {"m.left": "a2", "m.right": "b1", "m.top": "c1", "m.bottom": "d1"}
    assert standing(state, "m.carcass", now, {"m.carcass": TWO}).changed == ["m.left"]
    assert fix(state, "m.carcass", ["m.left"], now, WHEN) == ["m.left: fixed by hand, made as the build has it now"]
    st = standing(state, "m.carcass", now, {"m.carcass": TWO})
    assert st.made["m.left"] == FIXED and st.reasons == {}
    assert standing(state, "m.carcass", dict(now, **{"m.left": "a3"}), {"m.carcass": TWO}).changed == ["m.left"]
    with pytest.raises(LangError, match="m.right is made and unchanged"):
        fix(state, "m.carcass", ["m.right"], now, WHEN)
    with pytest.raises(LangError, match="m.shelf is not made in m.carcass"):
        fix(state, "m.carcass", ["m.shelf"], dict(now, **{"m.shelf": "e1"}), WHEN)
    with pytest.raises(LangError, match="m.top is no longer in m.carcass"):
        fix(state, "m.carcass", ["m.top"], {"m.left": "a2"}, WHEN)


def test_a_part_made_again_in_a_second_nest_is_made_as_that_one_has_it():
    state = empty()
    mark(state, TWO, None, WHEN)
    second = nest_file("m.carcass-2", [("birch 15", "1", True, (2500, 1250), [("m.left", "a2")], [])],
                       follows="m.carcass")
    mark(state, second, None, WHEN)
    now = {"m.left": "a2", "m.right": "b1", "m.top": "c1", "m.bottom": "d1"}
    assert standing(state, "m.carcass", now, {"m.carcass": TWO, "m.carcass-2": second}).reasons == {}
    # Changed back to what the first nest made: the latest made is the second's.
    assert standing(state, "m.carcass", dict(now, **{"m.left": "a1"}), {}).changed == ["m.left"]


def test_a_nest_not_marked_says_what_changed_since_its_file():
    found = changes(TWO, {"m.left": "a1", "m.right": "b9", "m.top": "c1", "m.shelf": "e1"})
    assert found.changed == ["m.right"] and found.new == ["m.shelf"] and found.gone == ["m.bottom"]
    assert not changes(TWO, {"m.left": "a1", "m.right": "b1", "m.top": "c1", "m.bottom": "d1"})
    left_over = nest_file("m.x", [("birch 15", "1", True, (2500, 1250), [("m.a", "a")], [])], unplaced=("m.b",))
    assert not changes(left_over, {"m.a": "a", "m.b": "b"})


# -- the command line --------------------------------------------------------------------------------

def _shop(extra: str = "", count: int = 3) -> str:
    """A build of `count` panels of 500 x 350 on sheets of 600 x 400: one a
    sheet, so each sheet holds one part."""
    panels = "".join(f"    board('p{k}', ply).on(m.bottom).between(m.front.into(350), m.front, m.left.gap({k * 600}), "
                     f"m.left.gap({k * 600 + 500}))\n" for k in range(count))
    return f"""from lang import *
use(nesting.bed((2000, 1000)), nesting.seconds(0.3), nesting.least_seconds(0.2), nesting.refill(False),
    nesting.spacing(5), nesting.margin(5))
ply = sheet_material('birch', t=15, size=(600, 400))
with module('m', Box.from_size(depth=400, width={count * 600}, height=300)) as m:
    uncheck(no_interference)
{panels}{extra}"""


def _nest(build: Path, *args: str) -> int:
    return nest_main([str(build), "--out", str(build.parent / "out"), "--no-refill", *args])


def _state(build: Path) -> dict[str, Any]:
    return json.loads((build.parent / "out" / STATE).read_text())


def test_the_command_line_marks_a_nest_made_and_nests_only_what_changed_beside_it(
        tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    build = tmp_path / "shop.py"
    build.write_text(_shop())
    (tmp_path / "inventory.toml").write_text('# mine\n\n[[stock]]\nmaterial = "birch 15"\nsize = [600, 400]\n')
    assert _nest(build) == 0
    out = tmp_path / "out" / "m" / "birch_15"
    first = json.loads((out / "nest.json").read_text())
    sheets = {p["path"]: s["name"] for s in first["materials"][0]["sheets"] for b in s["blanks"] for p in b["parts"]}
    assert len(set(sheets.values())) == 3 and [s["bought"] for s in first["materials"][0]["sheets"]] == \
        [False, True, True]
    assert _nest(build, "--made", "m.birch_15") == 0
    assert "inventory: -1 birch 15 600x400" in capsys.readouterr().out
    assert read_inventory(tmp_path / "inventory.toml") == [] and (tmp_path / "inventory.toml").read_text() == \
        "# mine\n"
    frozen = (out / "nest.json").read_bytes()
    # p1 gets a hole, p2 goes, p3 comes.
    build.write_text(_shop("    m['p1'].hole(8, at=m['p1'].inner.center, depth=5)\n", 2)
                     + "    board('p3', ply).on(m.top).between(m.front.into(350), m.front, m.left, m.left.gap(500))\n")
    assert _nest(build) == 0
    said = capsys.readouterr().out
    assert "m.birch_15: marked as made; 1 part(s) made and unchanged; changed since made: m.p1; new: m.p3" in said
    assert "made, gone from the build: m.p2" in said
    assert (out / "nest.json").read_bytes() == frozen                       # frozen: never written again
    second = json.loads((tmp_path / "out" / "m" / "birch_15-2" / "nest.json").read_text())
    assert second["name"] == "m.birch_15-2" and second["follows"] == "m.birch_15"
    assert second["reasons"] == {"m.p1": "changed", "m.p3": "new"}
    assert sorted(p["path"] for s in second["materials"][0]["sheets"] for b in s["blanks"] for p in b["parts"]) == \
        ["m.p1", "m.p3"]
    # p1 fixed by hand instead: the second nest takes p3 only.
    assert _nest(build, "--fixed", "m.birch_15", "m.p1") == 0
    assert _nest(build, "m.birch_15") == 0
    second = json.loads((tmp_path / "out" / "m" / "birch_15-2" / "nest.json").read_text())
    assert second["reasons"] == {"m.p3": "new"}
    # Made too, the second nest leaves nothing; a run says so and nests nothing.
    assert _nest(build, "--made", "m.birch_15-2") == 0
    capsys.readouterr()
    assert _nest(build, "m.birch_15") == 0
    assert "m.birch_15: everything made, nothing to nest" in capsys.readouterr().out
    assert not (tmp_path / "out" / "m" / "birch_15-3").exists()
    assert list(_state(build)["nests"]) == ["m.birch_15", "m.birch_15-2"]


def test_the_command_line_marks_sheets_once_and_their_rests_go_into_the_inventory(
        tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    build = tmp_path / "shop.py"
    build.write_text(_shop(count=2).replace("size=(600, 400)", "size=(2000, 1000)"))
    assert _nest(build) == 0
    nest = json.loads((tmp_path / "out" / "m" / "birch_15" / "nest.json").read_text())
    (sheet,) = nest["materials"][0]["sheets"]
    kept = [r["rect"] for r in sheet["rests"] if r["keep"]]
    assert kept and not (tmp_path / "inventory.toml").exists()
    assert _nest(build, "--made", "m.birch_15", "1") == 0
    ledger = read_inventory(tmp_path / "inventory.toml")
    assert [(o.length, o.width) for o in ledger] == [(r[2], r[3]) for r in kept]
    text = (tmp_path / "inventory.toml").read_text()
    capsys.readouterr()
    assert _nest(build, "--made", "m.birch_15") == 0                     # again: nothing to the ledger
    assert "birch 15 sheet 1 was marked as made before" in capsys.readouterr().out
    assert (tmp_path / "inventory.toml").read_text() == text
    assert _nest(build, "--made", "m.birch_15", "7") == 1
    assert "'7' is no sheet of it" in capsys.readouterr().err


def test_a_nest_marked_by_sheets_nests_its_other_sheets_parts_anew(tmp_path: Path):
    build = tmp_path / "shop.py"
    build.write_text(_shop())
    assert _nest(build) == 0
    out = tmp_path / "out" / "m"
    nest = json.loads((out / "birch_15" / "nest.json").read_text())
    on = {p["path"]: s["name"] for s in nest["materials"][0]["sheets"] for b in s["blanks"] for p in b["parts"]}
    first = next(path for path, sheet in on.items() if sheet == "1")
    assert _nest(build, "--made", "m.birch_15", "1") == 0
    assert _nest(build, "m.birch_15") == 0
    second = json.loads((out / "birch_15-2" / "nest.json").read_text())
    assert second["reasons"] == {path: "not made" for path in on if path != first}


def test_status_says_what_changed_and_writes_nothing(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    build = tmp_path / "shop.py"
    build.write_text(_shop(count=2))
    assert _nest(build, "--status") == 0
    assert "m.birch_15: not nested yet" in capsys.readouterr().out and not (tmp_path / "out").exists()
    assert _nest(build) == 0
    assert _nest(build, "--status") == 0
    assert "m.birch_15: its parts are as nested" in capsys.readouterr().out
    build.write_text(_shop("    m['p0'].hole(8, at=m['p0'].inner.center, depth=5)\n", 2))
    before = {p: p.read_bytes() for p in (tmp_path / "out").rglob("*") if p.is_file()}
    assert _nest(build, "--status") == 0
    assert "m.birch_15: changed since nested: m.p0" in capsys.readouterr().out
    assert {p: p.read_bytes() for p in (tmp_path / "out").rglob("*") if p.is_file()} == before


def test_marking_runs_no_build_and_refuses_a_nest_not_nested(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    build = tmp_path / "shop.py"
    build.write_text(_shop(count=1))
    assert _nest(build) == 0
    build.write_text("raise SystemExit('a build that does not run')\n")
    assert _nest(build, "--made", "m.birch_15") == 0
    assert _nest(build, "--made", "m.other") == 1
    assert "No nest file of m.other under" in capsys.readouterr().err
