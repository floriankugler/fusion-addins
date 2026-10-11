"""The snapshot writer's Fusion-free half and the committed fixture."""
import json
import math
from pathlib import Path

import pytest

from lang.core.snapshot_types import SNAPSHOT_VERSION
from lang.emit import snapshot_format as fmt
from lang.emit.snapshot_format import ChainError, Collector, chain, content_hash, dumps

FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "van_snapshot.json"


# -- chaining curves -------------------------------------------------------------

def test_chain_orders_and_flips_curves():
    a = [(0.0, 0.0, 0.0), (10.0, 0.0, 0.0)]
    b = [(20.0, 5.0, 0.0), (10.0, 0.0, 0.0)]          # runs the other way
    c = [(20.0, 5.0, 0.0), (30.0, 5.0, 0.0)]
    points, closed = chain([c, a, b])
    assert not closed
    # one open end to the other, without repeated points
    assert points[0] in (a[0], c[-1]) and points[-1] in (a[0], c[-1])
    assert len(points) == 4


def test_chain_closes_a_loop_without_repeating_the_start():
    square = [[(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)], [(1.0, 0.0, 0.0), (1.0, 1.0, 0.0)],
              [(0.0, 1.0, 0.0), (1.0, 1.0, 0.0)], [(0.0, 1.0, 0.0), (0.0, 0.0, 0.0)]]
    points, closed = chain(square)
    assert closed and len(points) == 4


def test_chain_takes_a_single_closed_curve():
    circle = [(math.cos(t / 8 * math.tau), math.sin(t / 8 * math.tau), 0.0) for t in range(9)]
    points, closed = chain([circle])
    assert closed and len(points) == 8


def test_chain_joins_ends_within_tolerance():
    points, closed = chain([[(0.0, 0.0, 0.0), (10.0, 0.0, 0.0)], [(10.005, 0.0, 0.0), (10.0, 7.0, 0.0)]])
    assert not closed and len(points) == 3


def test_chain_refuses_two_chains_and_branches():
    with pytest.raises(ChainError, match="2 separate chains"):
        chain([[(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)], [(5.0, 0.0, 0.0), (6.0, 0.0, 0.0)]])
    with pytest.raises(ChainError, match="3 curves meet"):
        chain([[(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)], [(0.0, 0.0, 0.0), (0.0, 1.0, 0.0)],
               [(0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]])
    with pytest.raises(ChainError, match="no curves"):
        chain([])


# -- collecting names --------------------------------------------------------------

def test_collector_skips_double_underscore_and_reports_duplicates():
    c = Collector()
    c.plane("", "Boden", "root", (0, 0, 40), (0, 0, 2))
    c.plane("", "Boden", "root", (0, 0, 50), (0, 0, 1))
    c.plane("", "__Hilfe", "root", (0, 0, 0), (1, 0, 0))
    c.plane("Bett", "__Hilfe", "Bett:1", (0, 0, 0), (1, 0, 0))   # the item's own name counts
    c.box("", "Kueche", "Kueche:1", (0, 0, 0), (1, 2, 3), True)
    c.contour("", "Fenster", "root", [[(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)], [(5.0, 0.0, 0.0), (6.0, 0.0, 0.0)]],
              (0, 0, 0), (0, 1, 0))
    c.problem("boxes", "", "Haut", "root", "a surface body, not a solid")
    s = c.build("master")
    assert c.skipped == 2
    assert s["planes"] == {} and set(s["boxes"]) == {"Kueche"}
    problems = {(p["kind"], p["name"]): p["message"] for p in s["problems"]}
    assert problems[("planes", "Boden")] == "named twice (root, root)"
    assert "separate chains" in problems[("contours", "Fenster")]
    assert problems[("boxes", "Haut")].startswith("a surface body")


def test_items_in_components_are_named_by_their_path():
    c = Collector()
    c.plane("", "Boden", "root", (0, 0, 40), (0, 0, 1))
    c.plane("Bett", "Boden", "Bett:1", (0, 0, 900), (0, 0, 1))          # no clash with the root's
    c.box("Moebel", "Kueche", "Moebel:1+Kueche:1", (0, 0, 0), (1, 1, 1), True)
    c.box("Moebel.Sitzbank", "Sitz", "Moebel:1+Sitzbank:1", (0, 0, 0), (1, 1, 1), True)
    c.parameter("Bodenaufbau", 40, "mm", "40 mm")
    s = c.build("master")
    assert set(s["planes"]) == {"Boden", "Bett.Boden"}
    assert set(s["boxes"]) == {"Moebel.Kueche", "Moebel.Sitzbank.Sitz"}
    assert set(s["parameters"]) == {"Bodenaufbau"}


def test_collector_normalises_and_rounds():
    c = Collector()
    c.plane("", "Boden", "root", (0.123456789, -0.0, 40), (0, 0, 2))
    s = c.build("master")
    assert s["planes"]["Boden"] == {"origin": [0.1235, 0.0, 40.0], "normal": [0.0, 0.0, 1.0]}


def test_hash_covers_the_content_not_the_source_name():
    def snapshot(source: str, z: float):
        c = Collector()
        c.plane("", "Boden", "root", (0, 0, z), (0, 0, 1))
        return c.build(source)
    assert snapshot("a", 40)["hash"] == snapshot("b", 40)["hash"]
    assert snapshot("a", 40)["hash"] != snapshot("a", 41)["hash"]


def test_dumps_is_json_with_one_point_per_line():
    c = Collector()
    c.contour("", "Profil", "root", [[(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 2.0, 0.0)]], (0, 0, 0), (0, 0, 1))
    s = c.build("master")
    text = dumps(s)
    assert json.loads(text) == s
    assert "\n        [1.0, 0.0, 0.0],\n" in text


def test_versions_agree():
    assert fmt.SNAPSHOT_VERSION == SNAPSHOT_VERSION


# -- the committed fixture ------------------------------------------------------------

def test_fixture_is_intact():
    """examples/van_snapshot.json is the snapshot of tools/van_master.py."""
    s = json.loads(FIXTURE.read_text())
    assert s["version"] == SNAPSHOT_VERSION
    assert s["hash"] == content_hash(s)
    assert set(s["planes"]) == {"Bodenniveau", "Boden vorne", "Boden hinten", "Wand FS", "Dach geneigt", "Bett.oben"}
    assert set(s["contours"]) == {"Bodenumriss", "Bodenprofil", "Bett.Kante"}
    assert set(s["boxes"]) == {"Boden", "Moebel.Kueche", "Bett", "Radkasten FS", "Sitzbank.Sitz", "Sitzbank.Lehne"}
    assert [p["name"] for p in s["problems"]] == ["Fenster"]
    # the moved component's items are in world coordinates
    assert s["boxes"]["Bett"]["min"] == [2300.0, -890.0, 900.0]
    assert s["planes"]["Bett.oben"]["origin"][2] == 1000.0
    assert s["contours"]["Bett.Kante"]["points"] == [[2300.0, -890.0, 900.0], [3400.0, -890.0, 900.0]]
    assert not s["boxes"]["Radkasten FS"]["cuboid"] and s["boxes"]["Moebel.Kueche"]["cuboid"]
    assert s["parameters"]["Neigung"]["value"] == pytest.approx(10.0)
