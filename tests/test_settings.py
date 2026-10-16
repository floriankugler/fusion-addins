"""Settings (`lang.core.settings`, `design/api.md`, Settings): keys and
bindings, the chain from an operation up to the root, set once per node,
freezing, the core's keys (`material`, `grain`, `nest`, `chamfer_size`),
provenance in the layout, the master's parameters as settings, and lazy
modules made with `@module`."""
from pathlib import Path

import pytest

from lang import *
from lang.core.layout import build_layout
from lang.core.layout_types import PartLayout
from helpers import ply9, ply12, ply15, ply18

BOX = Box.from_size(width=600, depth=500, height=720)
FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "van_snapshot.json"
#: A key with a default and one without, as a build defines its own.
gap = setting(3.0, "gap")
reveal: Setting[float] = setting(..., "reveal")


def part_layout(path: str) -> PartLayout:
    return next(p for m in build_layout()["modules"] for p in m["parts"] if p["path"] == path)


# -- keys and the chain -----------------------------------------------------------------------

def test_a_key_reads_its_default_where_nothing_uses_it():
    assert value(gap) == 3.0
    with module("m", BOX) as m:
        assert value(gap) == 3.0 and m.value(gap) == 3.0
        b = board("b", ply15).on(m.left)
        assert b.value(gap) == 3.0
    assert repr(gap) == "setting('gap')" and repr(gap(2.5)) == "gap(2.5)"


def test_the_nearest_node_wins():
    """Operation, part, scopes innermost first, root, default."""
    use(gap(1.0))
    with module("m", BOX) as m:
        use(gap(2.0))
        with scope("inner"):
            use(gap(3.0))
            b = board("b", ply15).on(m.left)
            b.cut(rect(depth=60, height=100), at=b.outer.bottom.front, name="notch")
            c = board("c", ply15).on(m.right).use(gap(4.0))
            c.cut(rect(depth=60, height=100), at=c.outer.bottom.front, name="notch")
            c.notch.use(gap(5.0))
            assert value(gap) == 3.0 and b.value(gap) == 3.0 and b.notch.value(gap) == 3.0
            assert c.value(gap) == 4.0 and c.notch.value(gap) == 5.0
        assert m.value(gap) == 2.0
    with module("n", BOX) as n:
        assert n.value(gap) == 1.0                                 # the root's
    assert value(gap) == 1.0


def test_a_key_without_a_default_must_be_used_above_its_reader():
    with module("m", BOX):
        with pytest.raises(LangError, match=r"^m reads reveal, which has no default and is set nowhere above it; "
                                            r"use\(reveal\(\.\.\.\)\) in a scope above sets it for everything in it"):
            value(reveal)
        use(reveal(2.0))
        assert value(reveal) == 2.0
    with pytest.raises(LangError, match="has no default"):
        _ = reveal.default


def test_a_node_uses_a_key_once():
    with module("m", BOX):
        use(gap(1.0))
        with pytest.raises(LangError, match=r"gap used twice on m \(first at tests/test_settings\.py:\d+: "
                                            r"use\(gap\(1\.0\)\)\); a node uses a setting once"):
            use(gap(2.0))
        with scope("s"):
            use(gap(2.0))                                          # another node
    with pytest.raises(LangError, match="gap used twice on root"):
        use(gap(1.0), gap(2.0))
    assert value(gap) == 3.0


def test_use_is_all_or_nothing():
    """A refused use() uses none of its bindings."""
    with module("m", BOX) as m:
        with pytest.raises(LangError, match="reveal used twice"):
            use(gap(1.0), reveal(1.0), reveal(2.0))
        assert not m.settings.uses(gap) and not m.settings.uses(reveal)
        use(gap(1.0))
        assert value(gap) == 1.0


def test_a_binding_is_checked_when_it_is_made():
    with pytest.raises(LangError, match=r"nest\(\) takes True or False, not 'no'"):
        nest("no")                                                 # type: ignore[arg-type]
    with pytest.raises(LangError, match=r"grain\(\): expected 'width', 'depth' or 'height', not 'hieght'"):
        grain("hieght")                                            # type: ignore[arg-type]
    with pytest.raises(LangError, match=r"material\(\): oak is a slat material"):
        material(slat_material("oak"))                             # type: ignore[arg-type]
    with pytest.raises(LangError, match=r"chamfer_size\(\) takes a size in mm, not '1'"):
        chamfer_size("1")                                          # type: ignore[arg-type]
    with pytest.raises(LangError, match="use.. takes bindings"):
        use(gap)                                                   # type: ignore[arg-type]


# -- freezing ----------------------------------------------------------------------------------

def test_a_key_read_freezes_for_the_nodes_the_read_passed():
    """A use() above a reader after the read is an error naming the reader
    and its line; one before is not."""
    with module("m", BOX) as m:
        with scope("inner"):
            b = board("b", ply15).on(m.left)
            assert b.value(gap) == 3.0                             # read from the default
        with pytest.raises(LangError, match=r"^gap\(2\.0\) on m comes after m\.inner\.b read gap, at "
                                            r"tests/test_settings\.py:\d+: assert b\.value\(gap\) == 3\.0 .*; what "
                                            r"was read there would no longer hold\. Use it before that line\.$"):
            use(gap(2.0))
        with pytest.raises(LangError, match=r"on m\.inner\.b comes after m\.inner\.b read gap"):
            b.use(gap(2.0))
    with pytest.raises(LangError, match="on root comes after m.inner.b read gap"):
        use(gap(2.0))


def test_a_use_the_reader_never_saw_is_not_frozen():
    """Above the node a read found its value at, a key may still be used:
    the reader would not see it."""
    with module("m", BOX) as m:
        with scope("inner"):
            use(gap(1.0))
            b = board("b", ply15).on(m.left)
            assert b.value(gap) == 1.0
        use(gap(2.0))                                              # shadowed by inner's for b
        assert m.value(gap) == 2.0 and b.value(gap) == 1.0


def test_a_chamfer_without_a_size_reads_the_key_where_it_is_written():
    with module("m", BOX) as m:
        use(chamfer_size(1.0))
        b = board("b", ply15).on(m.left)
        b.chamfer(b.outer.front)
        with pytest.raises(LangError, match=r"chamfer_size\(0\.5\) on m\.b comes after the chamfer of m\.b read "
                                            r"chamfer_size, at tests/test_settings\.py:\d+: b\.chamfer\(b\.outer\.front\)"):
            b.use(chamfer_size(0.5))


def test_keys_nothing_reads_during_the_build_are_never_frozen():
    """nest and grain are read by the layout, so a scope takes them at any
    time, after its boards are placed and machined."""
    with module("m", BOX) as m:
        b = board("b", ply15).on(m.left)
        b.cut(rect(depth=60, height=100), at=b.outer.bottom.front)
        use(nest(False), grain("height"))
    layout = part_layout("m.b")
    assert layout["nest"] is False and layout["grain"] == "z"


# -- the core's keys ---------------------------------------------------------------------------

def test_a_board_takes_the_material_its_scopes_use():
    use(material(ply15))
    with module("m", BOX) as m:
        side = board("side").on(m.left)
        back = board("back", ply9).on(m.back).between(side, m.right)
        with scope("drawers"):
            use(material(ply12))
            front = board("front").on(m.front).between(side, m.right)
    assert side.thickness == 15 and back.thickness == 9 and front.thickness == 12
    assert part_layout("m.side")["settings"]["material"] == {"value": "birch 15", "source": "root"}
    assert part_layout("m.back")["settings"]["material"] == {"value": "birch 9", "source": "m.back"}
    assert part_layout("m.drawers.front")["settings"]["material"] == {"value": "birch 12", "source": "m.drawers"}


def test_a_board_without_material_in_a_chain_that_uses_none_is_an_error():
    with module("m", BOX) as m:
        side = board("side").on(m.left)
        with pytest.raises(LangError, match=r"^m\.side reads material, which has no default and is set nowhere above "
                                            r"it; board\(name, material\) gives a board its own, or "
                                            r"use\(material\(\.\.\.\)\) in a scope above sets it"):
            _ = side.inner
    with pytest.raises(LangError, match="m.side reads material"):
        build_layout()


def test_a_material_used_after_the_board_is_made_applies_until_it_is_read():
    """Boards resolve lazily: the material is read when the placement is,
    and then it is frozen for the scopes the read passed."""
    use(material(ply15))
    with module("m", BOX) as m:
        side = board("side").on(m.left)
        with scope("s"):
            shelf = board("shelf").on(m.bottom).between(side, m.right)
            use(material(ply18))                                   # after the board, before its placement
        assert side.thickness == 15 and shelf.thickness == 18
        with pytest.raises(LangError, match=r"^material\(SheetMaterial.*\) on m comes after m\.side read material, "
                                            r"at tests/test_settings\.py:\d+: assert side\.thickness == 15"):
            use(material(ply12))


def test_a_board_says_material_grain_and_nest_through_its_own_spelling():
    """One spelling per key per node [decided 2026-10-16]."""
    with module("m", BOX) as m:
        b = board("b", ply15).on(m.left)
        for binding, spelling in ((material(ply9), r"board\(name, material\)"), (grain("height"), r"grain\(\)"),
                                  (nest(False), r"nest\(\)")):
            with pytest.raises(LangError, match=rf"m\.b: use\(.*\) on a board: a board says \w+ with {spelling}"):
                b.use(binding)
        b.use(gap(1.0))
        oak = slat_material("oak")
        s = slat("cleat", oak, section=(20, 40))
        with pytest.raises(LangError, match="on a slat: a slat's material is its own"):
            s.use(nest(False))


def test_a_scope_unnests_every_board_in_it():
    with module("m", BOX) as m:
        with scope("floor"):
            use(nest(False))
            a = board("a", ply15).on(m.bottom)
            b = board("b", ply15).on(m.top).nest(True)
        c = board("c", ply15).on(m.left)
    assert not a.nested and b.nested and c.nested
    assert part_layout("m.floor.a")["nest"] is False and part_layout("m.floor.b")["nest"] is True
    assert part_layout("m.floor.a")["settings"]["nest"] == {"value": False, "source": "m.floor"}
    assert part_layout("m.floor.b")["settings"]["nest"] == {"value": True, "source": "m.floor.b"}
    assert "nest" not in part_layout("m.c")["settings"]


def test_a_scope_grain_is_read_in_its_own_frame():
    """An extent names the axis in the frame of the node that uses it: the
    kitchen's depth, also for a child scope and when it is used from
    outside."""
    van = Box.from_size(width=2000, depth=1000, height=1000)
    with module("k", van, front=van.right) as k:              # front +y: the kitchen's depth is y
        use(grain("depth"))
        top = board("top", ply15).on(k.top)
        with scope("inner"):
            shelf = board("shelf", ply15).on(k.bottom)
    outer = module("o", van, front=van.right).use(grain("width"))  # its width is x
    with outer:
        back = board("back", ply15).on(outer.bottom)
    assert part_layout("k.top")["grain"] == "y" and part_layout("k.inner.shelf")["grain"] == "y"
    assert part_layout("o.back")["grain"] == "x"
    assert part_layout("k.top")["settings"]["grain"] == {"value": "y", "source": "k"}
    assert top.grain_axis() == "y" and shelf.grain_axis() == "y" and back.grain_axis() == "x"


def test_an_inherited_grain_along_the_thickness_is_an_error():
    with module("m", BOX) as m:
        use(grain("height"))
        side = board("side", ply15).on(m.left)
        bottom = board("bottom", ply15).on(m.bottom)
    assert side.grain_axis() == "z"
    with pytest.raises(LangError, match=r"m\.bottom: grain z from m is the thickness axis of this board; give it a "
                                        r"grain\(\) of its own"):
        bottom.grain_axis()
    bottom.grain("depth")                                          # after placement: grain() is order-free now
    assert bottom.grain_axis() == "x"
    with pytest.raises(LangError, match=r"grain\(\) given twice"):
        bottom.grain("width")
    with pytest.raises(LangError, match=r"m\.side: grain y is the thickness axis"):
        side.grain(m.left)                                         # placed: refused at once
    with m:
        other = board("other", ply15).on(m.left).grain(m.left)
    with pytest.raises(LangError, match=r"m\.other: grain y is the thickness axis"):
        _ = other.inner                                            # else when it is placed


def test_a_material_without_grain_takes_no_inherited_grain():
    mdf = sheet_material("mdf", t=16, grain=False)
    with module("m", BOX) as m:
        use(grain("height"))
        board("panel", mdf).on(m.left)
        board("own", mdf).on(m.right).grain("depth")
    assert part_layout("m.panel")["grain"] is None and "grain" not in part_layout("m.panel")["settings"]
    assert part_layout("m.own")["grain"] == "x" and part_layout("m.own")["settings"]["grain"]["source"] == "m.own"


def test_a_slat_takes_none_of_the_boards_keys():
    oak = slat_material("oak")
    with module("m", BOX) as m:
        use(nest(False), grain("depth"), material(ply15), gap(1.0))
        cleat = slat("cleat", oak, section=(20, 40)).on(m.left).edge_on(m.bottom)
    layout = part_layout("m.cleat")
    assert layout["grain"] == "x" == cleat.grain_axis()             # along its length, whatever the scope says
    assert layout["material"] == "oak" and layout["nest"] is False
    assert set(layout["settings"]) == {"gap"}


def test_chamfer_size_comes_from_the_chamfer_or_the_chain():
    with module("m", BOX) as m:
        a = board("a", ply15).on(m.left)
        with pytest.raises(LangError, match=r"^the chamfer of m\.a reads chamfer_size, which has no default and is "
                                            r"set nowhere above it; chamfer\(what, size\) gives a chamfer its own, "
                                            r"or use\(chamfer_size\(\.\.\.\)\)"):
            a.chamfer(a.outer.front)
        assert a.ops == []
        a.chamfer(a.outer.front, 2)                                # its own
        b = board("b", ply15).on(m.right).use(chamfer_size(0.5))
        b.chamfer([b.outer.front, b.outer.back])
        use(chamfer_size(1.5))
        c = board("c", ply15).on(m.back).between(a, b)
        c.chamfer(c.outer.top)
    sizes = {p: [op["size"] for op in part_layout(p)["ops"] if op["kind"] == "chamfer"] for p in ("m.a", "m.b", "m.c")}
    assert sizes == {"m.a": [2.0], "m.b": [0.5, 0.5], "m.c": [1.5]}
    assert part_layout("m.c")["settings"]["chamfer_size"] == {"value": 1.5, "source": "m"}
    # what holds for the board, set along its chain, whatever its own chamfer said
    assert part_layout("m.a")["settings"]["chamfer_size"] == {"value": 1.5, "source": "m"}


def test_a_corner_chamfer_reads_the_key_too():
    with module("m", BOX) as m:
        use(chamfer_size(10))
        panel = board("panel", ply15).on(m.bottom)
        panel.chamfer(panel.front.left)
    assert panel.outline.area == pytest.approx(600 * 500 - 10 * 10 / 2)     # one corner cut off


# -- provenance --------------------------------------------------------------------------------

def test_the_layout_carries_the_settings_set_along_each_parts_chain():
    big = setting({"a": [1, 2]}, "big")
    shape = setting(rect(depth=10, height=10), "shape")       # not JSON data: left out
    use(gap(1.0), shape(rect(depth=20, height=20)))
    with module("m", BOX) as m:
        use(big({"a": [3]}))
        b = board("b", ply15).on(m.left)
        b.cut(rect(depth=60, height=100), at=b.outer.bottom.front, name="notch")
        b.notch.use(gap(4.0))
        assert b.value(gap) == 1.0
        c = board("c", ply15).on(m.right)
        assert c.value(setting(7, "unused")) == 7                 # a default read: listed as such
    layout = part_layout("m.b")
    assert layout["settings"] == {"big": {"value": {"a": [3]}, "source": "m"},
                                  "gap": {"value": 1.0, "source": "root"},
                                  "material": {"value": "birch 15", "source": "m.b"}}
    assert layout["op_settings"] == {"notch": {"gap": {"value": 4.0, "source": "m.b.notch"}}}
    assert "unused" not in part_layout("m.c")["settings"]           # its default is no one's setting
    assert part_layout("m.c")["op_settings"] == {}


def test_the_masters_parameters_are_settings():
    van = master(FIXTURE)
    height = van.setting("Kuechenhoehe")
    assert van.setting("Kuechenhoehe") is height and height.default == van.param("Kuechenhoehe") == 720
    with module("m", BOX) as m:
        a = board("a", ply15).on(m.left)
        assert a.value(height) == 720
        with scope("low"):
            use(height(700))
            b = board("b", ply15).on(m.right)
            assert b.value(height) == 700
    assert part_layout("m.a")["settings"]["Kuechenhoehe"] == {"value": 720.0, "source": "master: Kuechenhoehe"}
    assert part_layout("m.low.b")["settings"]["Kuechenhoehe"] == {"value": 700.0, "source": "m.low"}
    with pytest.raises(LangError, match="has no parameter 'Kuechenhohe'; did you mean 'Kuechenhoehe'"):
        van.setting("Kuechenhohe")


def test_the_nest_key_survives_importing_the_nesting_package():
    """`lang.nest` is the setting; importing the subpackage lang.nest must
    not put the package in its place."""
    import importlib

    import lang
    importlib.import_module("lang.nest.sawing")
    from lang import nest as key
    assert key is nest and lang.nest is nest
    from lang.nest import nest_layout
    assert callable(nest_layout)


# -- modules -----------------------------------------------------------------------------------

ran: list[str] = []


@module
def cupboard(cab: Scope, *, shelves: int = 1) -> None:
    """A cupboard with `shelves` shelves."""
    ran.append(cab.path)
    left = board("left").on(cab.left)
    right = board("right").on(cab.right)
    for i in range(shelves):
        board(f"shelf{i}").on(cab.bottom.into(100 * (i + 1))).between(left, right)
    left.chamfer(left.outer.front)
    cab.export("count", shelves)


@pytest.fixture(autouse=True)
def forget_runs():
    ran.clear()


def test_a_module_type_is_named_after_its_body():
    assert cupboard.__name__ == "cupboard" and cupboard.__doc__ == "A cupboard with `shelves` shelves."
    assert repr(cupboard) == "module(cupboard)"
    use(material(ply15), chamfer_size(1))
    a = cupboard(BOX)
    b = cupboard(BOX, name="second", shelves=2)
    assert a.path == "cupboard" and b.path == "second" and a.is_module
    assert [p["path"] for m in build_layout()["modules"] for p in m["parts"]] == [
        "cupboard.left", "cupboard.right", "cupboard.shelf0",
        "second.left", "second.right", "second.shelf0", "second.shelf1"]


def test_a_lazy_body_runs_once_on_first_use():
    use(material(ply15), chamfer_size(1))
    with module("van", BOX.grown(1000)):
        c = cupboard(BOX, shelves=2)
        assert ran == []                                           # not at the call
        assert c.left.value == BOX.side("left").value and ran == []   # the box's sides need no body
        assert c.count == 2 and ran == ["van.cupboard"]            # an export: the body runs
        assert c["left"].thickness == 15 and c.shelf1.thickness == 15
    build_layout()
    assert ran == ["van.cupboard"]


@pytest.mark.parametrize("first_use", ["part", "item", "parts", "child", "check", "layout", "interior", "with"])
def test_a_lazy_body_runs_at_any_first_use(first_use: str):
    use(material(ply15), chamfer_size(1))
    c = cupboard(BOX)
    assert ran == []
    if first_use == "part":
        c.part("left")
    elif first_use == "item":
        _ = c["left"]
    elif first_use == "parts":
        assert set(c.parts) == {"left", "right", "shelf0"}
    elif first_use == "child":
        with pytest.raises(LangError, match="no scope named 'x'"):
            c.child("x")
    elif first_use == "check":
        assert c.run_checks() == []
    elif first_use == "layout":
        build_layout()
    elif first_use == "interior":
        assert c.interior.width == 570
    else:
        with c:
            board("extra").on(c.top).between(c["left"], c["right"])
    assert ran == ["cupboard"]


def test_use_on_a_lazy_module_applies_to_its_body():
    use(material(ply15), chamfer_size(1))
    c = cupboard(BOX).use(chamfer_size(0.5), material(ply18))
    d = cupboard(BOX, name="d")
    use(nest(False))                                               # after the call, before the body: applies
    assert c["left"].thickness == 18 and d["left"].thickness == 15
    sizes = [op["size"] for op in part_layout("cupboard.left")["ops"] if op["kind"] == "chamfer"]
    assert sizes == [0.5]
    assert part_layout("d.left")["nest"] is False
    assert part_layout("cupboard.left")["settings"]["chamfer_size"]["source"] == "cupboard"
    with pytest.raises(LangError, match=r"chamfer_size\(2\.0\) on d comes after the chamfer of d\.left read "
                                        r"chamfer_size, at tests/test_settings\.py:\d+: left\.chamfer"):
        d.use(chamfer_size(2.0))


def test_a_lazy_modules_parent_is_the_scope_current_at_the_call():
    use(material(ply15), chamfer_size(1))
    with module("van", BOX.grown(1000)):
        with scope("left_wall"):
            c = cupboard(BOX)
    with module("other", BOX.grown(1000)):
        _ = c["left"]                                              # the body runs here, but belongs there
        board("x", ply15).on(BOX.side("top"))
    assert c.path == "van.left_wall.cupboard" and c["left"].path == "van.left_wall.cupboard.left"
    assert [p["path"] for p in build_layout()["modules"][1]["parts"]] == ["other.x"]


def test_a_lazy_module_with_front_is_written_in_its_own_frame():
    """The same layout as the body written in place with `with module(...)`."""
    van = Box.from_size(width=2000, depth=1000, height=1000)
    use(material(ply15), chamfer_size(1))
    cupboard(van, front=van.right, name="lazy", shelves=2)
    with module("eager", van, front=van.right) as cab:
        cupboard._body(cab, shelves=2)                             # pyright: ignore[reportPrivateUsage]
    layout = build_layout()
    lazy, eager = ([{k: v for k, v in p.items() if k not in ("path", "settings")} for p in m["parts"]]
                   for m in layout["modules"])
    assert lazy == eager
    with pytest.raises(LangError, match=r"module\('up'\): front= must face sideways; top is up or down"):
        cupboard(van, front=van.top, name="up")


def test_a_lazy_body_named_twice_in_one_scope_is_refused_at_the_call():
    use(material(ply15), chamfer_size(1))
    with module("van", BOX.grown(1000)):
        cupboard(BOX)
        with pytest.raises(LangError, match="name 'cupboard' already used in this scope"):
            cupboard(BOX)
    assert ran == []


def test_a_module_body_takes_its_scope_and_keywords_only():
    with pytest.raises(LangError, match=r"@module 'two': a module body takes its scope, then keywords of its own "
                                        r"only: def kitchen\(cab: Scope, \*, drawers: int = 3\)"):
        @module
        def two(cab: Scope, n: int) -> None:                       # pyright: ignore[reportUnusedFunction]
            pass
    with pytest.raises(LangError, match=r"@module 'named': the keyword 'name' is the module call's own"):
        @module
        def named(cab: Scope, *, name: str = "") -> None:          # pyright: ignore[reportUnusedFunction]
            pass

    @module
    def returns(cab: Scope) -> None:
        return 3                                                   # type: ignore[return-value]
    r = returns(BOX)
    with pytest.raises(LangError, match="the body of the module 'returns' returned 3; a module body returns nothing"):
        _ = r.parts


def test_a_body_reads_values_with_value():
    seen: list[float] = []

    @module
    def spaced(cab: Scope) -> None:
        seen.append(value(gap))

    with module("van", BOX.grown(1000)):
        use(gap(2.0))
        s = spaced(BOX).use(gap(1.0))
        t = spaced(BOX, name="t")
    build_layout()
    assert seen == [1.0, 2.0]
    with pytest.raises(LangError, match="gap.1.0. on van.t comes after van.t read gap"):
        t.use(gap(1.0))
    assert s.value(gap) == 1.0
