"""Draws a nest as SVG: its name, then per material each piece of stock
with its saw cuts (numbered in the order they are made), its blanks with
their parts (labelled, the grain marked; a `nest(False)` board's own blank
hatched), the rests kept as stock and the waste, and a line saying what it
uses. The preview shows it in its nest view; each part
is a group with `data-path`, which the page selects in the scene.
"""
from __future__ import annotations

import html
import math
from collections.abc import Callable, Sequence

from shapely import Polygon

from .items import Item
from .nest_types import MaterialOut, NestFile, SheetOut

PAD = 80.0          # mm around and between the sheets
TITLE = 70.0        # mm of room for a material's title


def draw_nest(nest: NestFile, items: dict[str, Item]) -> str:
    """The SVG text: every material, one sheet under the other."""
    widths = [s["size"][0] for m in nest["materials"] for s in m["sheets"]] or [1000.0]
    width = max(widths) + 2 * PAD
    out: list[str] = []
    y = PAD
    if nest["name"]:
        out.append(_text(PAD, y + 40, f"{nest['name']} (written {nest['written']})", 48, "title"))
        y += TITLE + 10
    for m in nest["materials"]:
        out.append(_text(PAD, y + 40, _material_line(m), 44, "title"))
        y += TITLE
        for sheet in m["sheets"]:
            out.append(_sheet(sheet, items, PAD, y))
            y += sheet["size"][1] + 60 + PAD
    if nest["left_out"]:
        out.append(_text(PAD, y + 30, "Not nested: " + ", ".join(f"{p['path']} ({p['why']})" for p in nest["left_out"]),
                         30, "note"))
        y += 60
    for problem in nest["problems"]:
        out.append(_text(PAD, y + 30, "Problem: " + problem, 30, "problem"))
        y += 45
    height = y + PAD
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" '
            f'width="{width / 5:.0f}" height="{height / 5:.0f}" font-family="sans-serif">\n'
            f'<style>{_STYLE}</style>\n{_DEFS}\n' + "\n".join(out) + "\n</svg>\n")


_DEFS = ('<defs><pattern id="own" width="24" height="24" patternUnits="userSpaceOnUse" '
         'patternTransform="rotate(45)"><rect width="24" height="24" fill="#f6f1e6"/>'
         '<line x1="0" y1="0" x2="0" y2="24" stroke="#d8cdb4" stroke-width="6"/></pattern></defs>')


_STYLE = """
.sheet { fill: #e9e4d8; stroke: #333; stroke-width: 3; }
.blank { fill: #f6f1e6; stroke: #7a6a4a; stroke-width: 2; }
.blank.own { fill: url(#own); stroke-dasharray: 12 6; }
.kept { fill: #cfe8c4; stroke: #4c7a3c; stroke-width: 2; }
.waste { fill: #c9c9c9; stroke: #888; stroke-width: 1.5; }
.cut { stroke: #c0392b; stroke-width: 4; stroke-dasharray: 24 10; }
.cutno { fill: #c0392b; font-weight: bold; }
.part path { fill: #7aa6d8; fill-opacity: 0.85; fill-rule: evenodd; stroke: #1d4f8a; stroke-width: 1.5; }
.part:hover path { fill: #f0a830; }
.part text { fill: #102a4a; pointer-events: none; }
.grain { stroke: #8a5a1d; stroke-width: 3; stroke-dasharray: 16 8; }
.title { fill: #222; font-weight: bold; }
.label { fill: #555; }
.blankname { fill: #7a6a4a; font-weight: bold; paint-order: stroke; stroke: #f6f1e6; stroke-width: 5; }
.note { fill: #555; }
.problem { fill: #c0392b; }
"""


def _material_line(m: MaterialOut) -> str:
    bought = ", ".join(f"{n} x {size}" for size, n in m["bought"].items()) or "nothing"
    on_hand = f", on hand {', '.join(m['on_hand_used'])}" if m["on_hand_used"] else ""
    return (f"{m['material']}: bought {bought}{on_hand}; parts {m['parts_area']:.2f} m², used {m['used_area']:.2f} m², "
            f"kept {m['kept_area']:.2f} m²" + (f"; left over {len(m['unplaced'])}" if m["unplaced"] else ""))


def _sheet(sheet: SheetOut, items: dict[str, Item], left: float, top: float) -> str:
    length, width = sheet["size"]

    def sy(y: float) -> float:          # sheet y (up) to SVG y (down)
        return top + width - y

    parts_area = sum(items[p["path"]].area for b in sheet["blanks"] for p in b["parts"] if p["path"] in items)
    kept = sum(r["rect"][2] * r["rect"][3] for r in sheet["rests"] if r["keep"])
    waste = length * width - parts_area - kept
    kind = f"{sheet['stock']} {'bought' if sheet['bought'] else 'on hand'}"
    out = [f'<g class="stock" data-sheet="{sheet["name"]}">',
           f'<rect class="sheet" x="{left:.1f}" y="{top:.1f}" width="{length:.1f}" height="{width:.1f}"/>']
    for r in sheet["rests"]:
        x, y, w, h = r["rect"]
        out.append(f'<rect class="{"kept" if r["keep"] else "waste"}" x="{left + x:.1f}" y="{sy(y + h):.1f}" '
                   f'width="{w:.1f}" height="{h:.1f}"><title>{"kept" if r["keep"] else "waste"} '
                   f'{w:.0f} x {h:.0f}</title></rect>')
        if r["keep"]:
            out.append(_text(left + x + 10, sy(y + h) + 34, f"{w:.0f} x {h:.0f}", 26, "label"))
    for b in sheet["blanks"]:
        x, y, w, h = b["rect"]
        own = " own" if b["own_blank"] else ""
        out.append(f'<rect class="blank{own}" x="{left + x:.1f}" y="{sy(y + h):.1f}" width="{w:.1f}" '
                   f'height="{h:.1f}"><title>{"own " if own else ""}blank {b["name"]}: {w:.0f} x {h:.0f}</title></rect>')
        for p in b["parts"]:
            item = items.get(p["path"])
            if item is None:
                continue
            shape = item.placed(p["turn"], (x + p["at"][0], y + p["at"][1]))
            out.append(_part(shape, p["path"], item, left, sy))
        # Over its parts, which come up to its margin.
        out.append(_text(left + x + 6, sy(y + h) + 14, f"{b['name']}  {w:.0f} x {h:.0f}" +
                         (" sawn to size" if own else ""), 22, "blankname"))
    for k, cut in enumerate(sheet["cuts"], 1):
        x0, y0, x1, y1 = cut["line"]
        out.append(f'<line class="cut" x1="{left + x0:.1f}" y1="{sy(y0):.1f}" x2="{left + x1:.1f}" y2="{sy(y1):.1f}"/>')
        out.append(_text(left + (x0 + x1) / 2 + 8, sy((y0 + y1) / 2) - 8, str(k), 34, "cutno"))
    # The sheet's grain: along its length.
    out.append(f'<line class="grain" x1="{left + 20:.1f}" y1="{top + width + 30:.1f}" x2="{left + 320:.1f}" '
               f'y2="{top + width + 30:.1f}"/>')
    out.append(_text(left + 340, top + width + 42, f"{sheet['name']}: {kind} {length:g} x {width:g}, "
                     f"{len(sheet['cuts'])} cuts, waste {waste / 1e6:.2f} m², kept {kept / 1e6:.2f} m² "
                     "(the grain along the dashes)", 30, "label"))
    out.append("</g>")
    return "\n".join(out)


def _part(shape: Polygon, path: str, item: Item, left: float, to_y: Callable[[float], float]) -> str:
    def ring(coords: Sequence[tuple[float, ...]]) -> str:
        pts = list(coords)[:-1]
        return "M " + " L ".join(f"{left + p[0]:.1f} {to_y(p[1]):.1f}" for p in pts) + " Z"
    d = " ".join([ring(list(shape.exterior.coords))] + [ring(list(r.coords)) for r in shape.interiors])
    c = shape.representative_point()
    x0, _y0, x1, _y1 = shape.bounds
    size = max(12.0, min(40.0, math.sqrt(shape.area) / 7))
    name = path.rsplit(".", 1)[-1]
    out = [f'<g class="part" data-path="{html.escape(path)}"><title>{html.escape(path)}</title>',
           f'<path d="{d}"/>']
    if item.grained:
        length = min(0.5 * (x1 - x0), 240.0)
        gy = to_y(c.y) + size
        out.append(f'<line class="grain" x1="{left + c.x - length / 2:.1f}" y1="{gy:.1f}" '
                   f'x2="{left + c.x + length / 2:.1f}" y2="{gy:.1f}"/>')
    out.append(_text(left + c.x, to_y(c.y), name, size, "", anchor="middle"))
    out.append("</g>")
    return "\n".join(out)


def _text(x: float, y: float, text: str, size: float, cls: str, anchor: str = "start") -> str:
    c = f' class="{cls}"' if cls else ""
    return (f'<text{c} x="{x:.1f}" y="{y:.1f}" font-size="{size:.0f}" text-anchor="{anchor}" '
            f'dominant-baseline="middle">{html.escape(text)}</text>')
