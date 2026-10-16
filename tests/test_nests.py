"""Nests declared in the build (`Scope.nest`, `lang.core.nests`): what a
nest by material or by boards named takes, the names and the errors, the
default nests per module and material, and what the layout carries of
them (version 8: each module's nests with their own settings, the sheet
materials with their sizes)."""
import pytest

from lang import *
from lang.core.layout import build_layout
from lang.core.layout_types import Layout, NestLayout
from lang.core.nests import file_safe
from helpers import ply9, ply12, ply15

BOX = Box.from_size(width=600, depth=500, height=720)


def nests(layout: Layout | None = None) -> dict[str, NestLayout]:
    layout = layout or build_layout()
    return {n["path"]: n for m in layout["modules"] for n in m["nests"]}


def shelf_unit(name: str = "unit", box: Box = BOX) -> Scope:
    """Sides and a back of 15 mm, a 12 mm shelf, a 9 mm drawer bottom in a
    scope of its own."""
    with module(name, box) as m:
        board("left", ply15).on(m.left)
        board("right", ply15).on(m.right)
        board("back", ply15).on(m.back).between(m["left"], m["right"])
        board("shelf", ply12).on(m.bottom).between(m["left"], m["right"], m["back"])
        with scope("drawer"):
            board("bottom", ply9).on(m.top).between(m["left"], m["right"], m["back"])
    return m


# -- declaring --------------------------------------------------------------------------------

def test_a_nest_by_material_takes_the_nested_boards_of_it_in_its_scope_made_before_or_after():
    with module("unit", BOX) as m:
        carcass = m.nest("carcass", material=ply15)
        board("left", ply15).on(m.left)
        board("right", ply15).on(m.right).nest(False)
        board("hand", ply15).on(m.bottom).between(m["left"], m["right"]).manual()
        with scope("inner"):
            board("back", ply15).on(m.back).between(m["left"], m["right"])
        board("shelf", ply12).on(m.top).between(m["left"], m["right"])
    assert [b.path for b in carcass.parts] == ["unit.left", "unit.inner.back"]
    n = nests()
    assert n["unit.carcass"] == {"path": "unit.carcass", "module": "unit", "by": "material", "material": "birch 15",
                                 "parts": ["unit.left", "unit.inner.back"], "left_out": ["unit.right", "unit.hand"],
                                 "settings": {}}
    assert n["unit.birch_12"]["parts"] == ["unit.shelf"] and n["unit.birch_12"]["by"] == "default"


def test_a_nest_names_boards_anywhere_in_its_scope_and_a_root_module_those_of_its_modules():
    with module("van", BOX) as van:
        a = shelf_unit("a", BOX)
        b = shelf_unit("b", BOX)
        remake = van.nest("remake", [a["left"], b["shelf"]])
        strips = van.nest("strips", [a["right"].nest(False)])
    assert remake.parts == [a["left"], b["shelf"]] and strips.path == "van.strips"
    n = nests()
    assert n["van.remake"]["by"] == "parts" and n["van.remake"]["material"] is None
    assert n["van.remake"]["parts"] == ["van.a.left", "van.b.shelf"] and n["van.remake"]["module"] == "van"
    assert n["van.strips"]["parts"] == ["van.a.right"]              # a nest(False) board: its own blank
    # Named by a nest, a board is in no default nest.
    assert n["van.a.birch_15"]["parts"] == ["van.a.back"] and "van.b.birch_12" not in n
    assert n["van.b.birch_15"]["parts"] == ["van.b.left", "van.b.right", "van.b.back"]


def test_a_nest_by_material_leaves_the_boards_of_a_module_inside_it_to_that_module():
    with module("van", BOX) as van:
        shelf_unit("unit", BOX)
        board("floor", ply15).on(van.bottom)
        van.nest("all15", material=ply15)
    n = nests()
    assert n["van.all15"]["parts"] == ["van.floor"]
    assert n["van.unit.birch_15"]["parts"] == ["van.unit.left", "van.unit.right", "van.unit.back"]


@pytest.mark.parametrize("name", ["", " carcass", "a.b", "a/b", "a\\b", 3])
def test_a_nest_s_name_is_a_word_for_a_folder(name: object):
    with module("m", BOX) as m:
        with pytest.raises(LangError, match="a nest's name is a word for a folder"):
            m.nest(name, material=ply15)  # pyright: ignore[reportArgumentType, reportCallIssue]


def test_a_nest_takes_a_material_or_boards_once_each():
    with module("m", BOX) as m:
        left = board("left", ply15).on(m.left)
        rail = slat("rail", slat_material("oak"), section=(20, 40)).on(m.bottom).edge_on(m.front) \
            .between(m.left, m.right)
        with pytest.raises(LangError, match="either its material .* or its boards .*, not both"):
            m.nest("a", [left], material=ply15)  # pyright: ignore[reportCallIssue]
        with pytest.raises(LangError, match="one of them"):
            m.nest("a")  # pyright: ignore[reportCallIssue]
        with pytest.raises(LangError, match="is not a material"):
            m.nest("a", material="birch 15")  # pyright: ignore[reportArgumentType]
        with pytest.raises(LangError, match="slat material"):
            m.nest("a", material=slat_material("oak"))  # pyright: ignore[reportArgumentType]
        with pytest.raises(LangError, match="as a list"):
            m.nest("a", left)  # pyright: ignore[reportArgumentType, reportCallIssue]
        with pytest.raises(LangError, match="m.rail is a slat"):
            m.nest("a", [rail])
        with pytest.raises(LangError, match="m.left is named twice"):
            m.nest("a", [left, left])
        with pytest.raises(LangError, match="name at least one board"):
            m.nest("a", [])
        with pytest.raises(LangError, match="is not a board"):
            m.nest("a", [m])  # pyright: ignore[reportArgumentType]
        m.nest("a", [left])
        with pytest.raises(LangError, match="m has a nest of that name already"):
            m.nest("a", material=ply15)
    with module("n", BOX) as n:
        with pytest.raises(LangError, match="m.left is not in n"):
            n.nest("b", [left])


def test_a_board_is_in_one_nest_of_its_module():
    with module("m", BOX) as m:
        left = board("left", ply15).on(m.left)
        m.nest("carcass", material=ply15)
        m.nest("fronts", [left])
    with pytest.raises(LangError, match="m.left is in two nests of m, m.carcass and m.fronts"):
        build_layout()


def test_a_board_may_be_in_a_nest_of_its_module_and_one_around_it():
    with module("van", BOX) as van:
        unit = shelf_unit("unit", BOX)
        unit.nest("carcass", material=ply15)
        van.nest("remake", [unit["left"]])
    n = nests()
    assert "van.unit.left" in n["van.unit.carcass"]["parts"] and n["van.remake"]["parts"] == ["van.unit.left"]


def test_a_manual_board_named_in_a_nest_is_refused():
    with module("m", BOX) as m:
        hand = board("hand", ply15).on(m.left).manual()
        m.nest("a", [hand])
    with pytest.raises(LangError, match="m.a names m.hand, which is made by hand"):
        build_layout()


def test_a_default_nest_s_name_taken_by_a_declared_nest_is_an_error():
    with module("m", BOX) as m:
        left = board("left", ply15).on(m.left)
        board("right", ply15).on(m.right)
        m.nest("birch_15", [left])
    with pytest.raises(LangError, match="m.birch_15 is the name of the nest of m's birch 15 boards that no nest "
                                        "names, and of a nest declared"):
        build_layout()


def test_a_declared_nest_that_takes_nothing_is_a_problem():
    with module("m", BOX) as m:
        board("left", ply15).on(m.left)
        m.nest("thin", material=ply9)
    layout = build_layout()
    assert "m.thin: no board to nest" in layout["problems"]
    assert nests(layout)["m.thin"]["parts"] == []


# -- default nests ---------------------------------------------------------------------------------

def test_what_no_nest_names_makes_a_nest_per_module_and_material():
    shelf_unit("unit")
    with module("other", Box.from_size(width=600, depth=500, height=720, origin=(1000, 0, 0))) as o:
        board("top", ply15).on(o.top)
    with scope("loose", Box.from_size(width=600, depth=500, height=720, origin=(2000, 0, 0))) as s:
        board("side", ply12).on(s.left)                 # a top-level scope counts as a module
    free = Box.from_size(width=400, depth=200, height=12, origin=(3000, 0, 0))
    board("plank", ply12).on(free.bottom).between(free.front, free.back, free.left, free.right)
    n = nests()
    assert {p: (v["module"], v["material"], v["parts"]) for p, v in n.items()} == {
        "unit.birch_15": ("unit", "birch 15", ["unit.left", "unit.right", "unit.back"]),
        "unit.birch_12": ("unit", "birch 12", ["unit.shelf"]),
        "unit.birch_9": ("unit", "birch 9", ["unit.drawer.bottom"]),
        "other.birch_15": ("other", "birch 15", ["other.top"]),
        "loose.birch_12": ("loose", "birch 12", ["loose.side"]),
        "birch_12": ("", "birch 12", ["plank"]),
    }
    assert all(v["by"] == "default" and v["settings"] == {} for v in n.values())


def test_a_material_s_label_is_made_file_safe():
    assert file_safe("birch 15") == "birch_15" and file_safe("birch 1.5") == "birch_1_5"
    assert file_safe("Multiplex/Birke 18") == "Multiplex_Birke_18" and file_safe("...") == "material"


def test_a_module_whose_boards_are_not_nested_has_no_nest_and_lists_them_where_one_is():
    with module("floor", BOX) as f:
        board("panel", ply12).on(f.top).nest(False)
        board("batten", ply15).on(f.bottom).between(f.front, f.front.into(60))
        board("long", ply15).on(f.bottom).between(f.back.into(60), f.back).nest(False)
    n = nests()
    assert list(n) == ["floor.birch_15"] and n["floor.birch_15"]["left_out"] == ["floor.long"]


def test_use_nest_false_on_a_module_keeps_its_boards_out_of_the_default_nests():
    with module("floor", BOX) as f:
        use(nest(False))
        board("panel", ply12).on(f.top)
        board("batten", ply15).on(f.bottom).nest(True)
    assert list(nests()) == ["floor.birch_15"]


# -- a nest's settings ----------------------------------------------------------------------------

def test_a_nest_is_a_node_of_the_chain_under_its_scope():
    use(nesting.bed((2000, 1000)))
    with module("m", BOX) as m:
        use(nesting.margin(12))
        board("left", ply15).on(m.left)
        carcass = m.nest("carcass", material=ply15).use(nesting.spacing(20), nesting.seconds(90))
        assert carcass.value(nesting.spacing) == 20 and carcass.value(nesting.margin) == 12
        assert carcass.value(nesting.bed) == (2000, 1000) and carcass.value(nesting.kerf) == 4
        with pytest.raises(LangError, match="nesting.spacing used twice on m.carcass"):
            carcass.use(nesting.spacing(5))
        for binding, spelling in ((material(ply12), "board"), (grain("width"), "grain"), (nest(False), "nest")):
            with pytest.raises(LangError, match=f"on a nest: {binding.key.name} is a board's.*{spelling}"):
                carcass.use(binding)
    n = nests()
    assert n["m.carcass"]["settings"] == {"nesting.spacing": {"value": 20.0, "source": "m.carcass"},
                                          "nesting.seconds": {"value": 90.0, "source": "m.carcass"}}
    layout = build_layout()
    left = layout["modules"][0]["parts"][0]
    assert left["settings"]["nesting.margin"] == {"value": 12.0, "source": "m"}
    assert left["settings"]["nesting.bed"] == {"value": [2000.0, 1000.0], "source": "root"}


@pytest.mark.parametrize("binding, message", [
    (lambda: nesting.bed((2000,)), "takes a size"),  # pyright: ignore[reportArgumentType]
    (lambda: nesting.bed((2000, 0)), "must be more than 0"),
    (lambda: nesting.kerf(-1), "0 or more"),
    (lambda: nesting.max_cuts(2.5), "whole number"),  # pyright: ignore[reportArgumentType]
    (lambda: nesting.seconds(0), "more than 0"),
    (lambda: nesting.refill("yes"), "True or False"),  # pyright: ignore[reportArgumentType]
    (lambda: nesting.spacing("ten"), "takes a number"),  # pyright: ignore[reportArgumentType]
])
def test_the_nesting_keys_check_their_values(binding: object, message: str):
    with pytest.raises(LangError, match=message):
        binding()  # pyright: ignore[reportCallIssue]


# -- the sheet materials -----------------------------------------------------------------------------

def test_the_layout_carries_the_sheet_materials_and_their_sizes():
    sized = sheet_material("birch", t=15, size=(2500, 1250))
    with module("m", BOX) as m:
        board("left", sized).on(m.left)
        board("right", ply12).on(m.right)
        slat("rail", slat_material("oak"), section=(20, 40)).on(m.bottom).edge_on(m.front).between(m.left, m.right)
    assert build_layout()["sheet_materials"] == {
        "birch 12": {"thickness": 12.0, "grain": True, "size": None},
        "birch 15": {"thickness": 15.0, "grain": True, "size": [2500.0, 1250.0]}}


def test_two_materials_of_one_label_are_an_error():
    with module("m", BOX) as m:
        board("left", ply15).on(m.left)
        board("right", sheet_material("birch", t=15, size=(2500, 1250))).on(m.right)
    with pytest.raises(LangError, match="two materials are called birch 15"):
        build_layout()


def test_the_nesting_keys_are_not_shadowed_by_the_package_s_modules():
    """Importing a submodule of `lang.nesting` sets an attribute of the
    package: a module named like a key would replace it (`refill` did)."""
    import importlib
    import pkgutil

    import lang.nesting as package
    from lang.nesting.keys import KEYS
    for info in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"lang.nesting.{info.name}")
    for key in KEYS:
        assert getattr(package, key.name.split(".", 1)[1]) is key
