"""Florian's CAM templates read outside Fusion: the `.f3dhsm-template`
files Auto Setup exports (`lib/auto_setup/templates.py`), each an XML file
with one `<template>` per operation, its `<tool>` inside and the
operation's parameters as expressions.

A file is named `<kind>[.<tag>...]_<label>.f3dhsm-template`, the kinds
`pocket`, `contour`, `drill`, `bore`, `dogbone`, `chamfer` and `groove`, the
tags `dc` and `udc` (the cutter variant it is for; none: either) and
`finish` (it has a finishing pass); the label names it in the settings
(`cam.contour_template("Kontur 6mm")`). A template's widest tool is its
cutter [decided]: what the plan sorts by and names it after; its
narrowest decides what it reaches (an adaptive pocket's 6 mm clean-up
after the 8 mm); its shortest flute how deep it cuts.

Lengths in mm (a tool given in inches is converted). A parameter's
expression is evaluated where it is plain arithmetic of lengths, numbers
and the tool's diameter and flute length (`6.4mm`, `(-0.2) * 1mm`,
`Math.min(tool_fluteLength * 0.75; tool_diameter)`), else it is None.
"""
from __future__ import annotations

import math
import re
import xml.etree.ElementTree as ET
from collections.abc import Sequence
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Literal

from ..core.errors import LangError

Kind = Literal["pocket", "contour", "drill", "bore", "dogbone", "chamfer", "groove"]
KINDS: tuple[Kind, ...] = ("pocket", "contour", "drill", "bore", "dogbone", "chamfer", "groove")
CUTTER_TAGS = ("dc", "udc")
VALID_TAGS = ("dc", "udc", "finish")
EXT = ".f3dhsm-template"
_NS = "{http://www.hsmworks.com/namespace/hsmworks/document/template}"
_UNITS = {"mm": 1.0, "cm": 10.0, "m": 1000.0, "in": 25.4, "inch": 25.4}
#: Units that are not lengths, whose numbers are taken as they are.
_PLAIN = {"deg", "degrees", "rpm", "mmpm", "ipm", "s"}


@dataclass(frozen=True)
class Tool:
    """A template operation's tool (mm, degrees)."""
    #: Fusion's tool type: "flat end mill", "chamfer mill" ...
    type: str
    diameter: float
    flute: float | None
    #: The flank's angle against the tool's axis (45 for a 90 degree V-bit).
    taper: float | None
    #: The tip's diameter: 0 for a pointed V-bit.
    tip: float


@dataclass(frozen=True)
class TemplateOp:
    strategy: str
    tool: Tool
    #: The operation's parameters by name, as expressions.
    params: dict[str, str]

    def value(self, name: str) -> float | bool | str | None:
        """A parameter's value: a number (lengths in mm), a flag, a word, or
        None where the expression is not plain enough to evaluate."""
        text = self.params.get(name)
        return None if text is None else evaluate(text, self.tool)


@dataclass(frozen=True)
class Template:
    kind: Kind
    tags: tuple[str, ...]
    label: str
    path: str
    ops: tuple[TemplateOp, ...] = field(default=())

    @property
    def stem(self) -> str:
        """The file's name without its extension: `contour.dc_Kontur 6mm`."""
        return f"{'.'.join((self.kind, *self.tags))}_{self.label}"

    @property
    def cutter_tag(self) -> str | None:
        return next((t for t in self.tags if t in CUTTER_TAGS), None)

    @property
    def finish(self) -> bool:
        return "finish" in self.tags

    def matches(self, cutter: str) -> bool:
        """For the cutter variant: tagged so, or untagged."""
        return self.cutter_tag is None or self.cutter_tag == cutter

    @property
    def tool(self) -> Tool:
        """Its cutter: the widest of its tools."""
        return max((op.tool for op in self.ops), key=lambda t: t.diameter)

    @property
    def diameter(self) -> float:
        return self.tool.diameter

    @property
    def narrowest(self) -> float:
        return min(op.tool.diameter for op in self.ops)

    @property
    def flute(self) -> float | None:
        """The shortest flute of its tools, how deep it cuts."""
        flutes = [op.tool.flute for op in self.ops if op.tool.flute is not None]
        return min(flutes) if flutes else None

    @property
    def adaptive(self) -> bool:
        return any("adaptive" in op.strategy.lower() for op in self.ops)

    def value(self, name: str) -> float | bool | str | None:
        """A parameter of its first operation that has it."""
        for op in self.ops:
            if name in op.params:
                return op.value(name)
        return None

    def number(self, name: str) -> float | None:
        v = self.value(name)
        return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None

    @property
    def stepdown(self) -> float | None:
        """Its first operation's largest stepdown where it cuts in several
        depths, else None (one pass)."""
        if not self.ops:
            return None
        op = self.ops[0]
        step = op.value("maximumStepdown")
        if op.value("doMultipleDepths") is not True or not isinstance(step, float) or step <= 0:
            return None
        return step

    @property
    def reach(self) -> float | None:
        """How deep a V-bit's flank cuts from its tip: the cone's height,
        capped by the flute (`lib.auto_setup.templates.VBit.reach`)."""
        tool = self.ops[0].tool if self.ops else None
        if tool is None or not tool.taper:
            return None
        height = (tool.diameter - tool.tip) / 2 / math.tan(math.radians(tool.taper))
        return height if tool.flute is None else min(height, tool.flute)


def parse_stem(stem: str) -> tuple[Kind, tuple[str, ...], str] | None:
    """'<kind>[.<tag>...]_<label>' as (kind, tags, label), or None."""
    head, sep, label = stem.partition("_")
    if not sep or not label:
        return None
    parts = head.split(".")
    kind, tags = parts[0], tuple(parts[1:])
    if kind not in KINDS or any(t not in VALID_TAGS for t in tags):
        return None
    return next(k for k in KINDS if k == kind), tags, label


def read_template(path: Path) -> Template:
    """One template file, its operations and their tools."""
    parsed = parse_stem(path.name[:-len(EXT)] if path.name.endswith(EXT) else path.stem)
    if parsed is None:
        raise LangError(f"{path.name}: not a template's name (<kind>[.<tag>...]_<label>{EXT}).")
    kind, tags, label = parsed
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as error:
        raise LangError(f"{path}: {error}") from None
    ops: list[TemplateOp] = []
    for element in root.iter(f"{_NS}template"):
        tool_element = element.find(f"{_NS}tool")
        body = tool_element.find(f"{_NS}body") if tool_element is not None else None
        if tool_element is None or body is None or body.get("diameter") is None:
            raise LangError(f"{path.name}: an operation without a tool.")
        scale = 25.4 if (tool_element.get("unit") or "").startswith("inch") else 1.0

        def length(name: str, body: ET.Element = body, scale: float = scale) -> float | None:
            text = body.get(name)
            return None if text is None else float(text) * scale

        diameter = length("diameter")
        assert diameter is not None
        taper = body.get("taper-angle")
        tool = Tool(tool_element.get("type") or "", diameter, length("flute-length"),
                    float(taper) if taper is not None else None, length("tip-diameter") or 0.0)
        params = {p.get("name") or "": p.get("expression") or "" for p in element.findall(f"{_NS}parameter")
                  if p.get("name")}
        ops.append(TemplateOp(element.get("strategy") or "", tool, params))
    if not ops:
        raise LangError(f"{path.name}: no operation in it.")
    return Template(kind, tags, label, str(path), tuple(ops))


@dataclass(frozen=True)
class Registry:
    """The templates of a folder, by kind."""
    folder: str
    by_kind: dict[str, tuple[Template, ...]]
    #: The files whose names are no templates' (a typo in a tag).
    skipped: tuple[str, ...] = ()

    def of(self, kind: Kind, cutter: str, labels: Sequence[str] | None = None) -> list[Template]:
        """The templates of a kind for the cutter, those labelled so where
        `labels` are given."""
        return [t for t in self.by_kind.get(kind, ()) if t.matches(cutter) and (labels is None or t.label in labels)]

    def resolve(self, kind: Kind, label: str, finish: bool, cutter: str) -> tuple[Template | None, list[str]]:
        """The template of a label with (or without) its finishing pass for
        the cutter variant, as Auto Setup resolves it: the one tagged for the
        cutter, else an untagged one, else the other cutter's with a note;
        without the finishing pass asked for, the other with a note."""
        notes: list[str] = []
        for want in (finish, not finish):
            candidates = [t for t in self.by_kind.get(kind, ()) if t.label == label and t.finish == want]
            exact = [t for t in candidates if t.cutter_tag == cutter]
            untagged = [t for t in candidates if t.cutter_tag is None]
            chosen = (exact or untagged or candidates or [None])[0]
            if chosen is None:
                continue
            if not exact and not untagged:
                notes.append(f"no {kind} template {label!r} for the {cutter} cutter; {chosen.stem} is taken")
            if want != finish:
                notes.append(f"no {kind} template {label!r} {'with' if finish else 'without'} a finishing pass; "
                             f"{chosen.stem} is taken")
            return chosen, notes
        return None, notes

    def labels(self, kind: Kind) -> list[str]:
        return sorted({t.label for t in self.by_kind.get(kind, ())})


def scan(folder: Path) -> Registry:
    """Every template file in a folder."""
    if not folder.is_dir():
        raise LangError(f"No templates' folder {folder} (cam.templates).")
    found: dict[str, list[Template]] = {k: [] for k in KINDS}
    skipped: list[str] = []
    for path in sorted(folder.iterdir()):
        if not path.name.endswith(EXT):
            continue
        if parse_stem(path.name[:-len(EXT)]) is None:
            skipped.append(path.name)
            continue
        template = read_template(path)
        found[template.kind].append(template)
    return Registry(str(folder), {k: tuple(v) for k, v in found.items()}, tuple(skipped))


@cache
def registry_of(folder: str) -> Registry:
    """`scan`, once per folder and run."""
    return scan(Path(folder))


# -- expressions -------------------------------------------------------------------------------

_TOKEN = re.compile(r"\s*(?:(?P<num>\d+(?:\.\d*)?|\.\d+)(?:\s*(?P<unit>[a-zA-Z]+))?|(?P<name>[A-Za-z_][\w.]*)"
                    r"|(?P<str>'[^']*')|(?P<op>[-+*/();]))")


class _Unplain(Exception):
    pass


def evaluate(text: str, tool: Tool | None = None) -> float | bool | str | None:
    """A template expression's value, or None where it is more than
    arithmetic of numbers, lengths (in mm), `tool_diameter`,
    `tool_fluteLength`, `Math.min` and `Math.max`: `true`, `false` and a
    quoted word are taken as they are."""
    s = text.strip()
    if s in ("true", "false"):
        return s == "true"
    if len(s) >= 2 and s[0] == s[-1] == "'" and "'" not in s[1:-1]:
        return s[1:-1]
    tokens: list[tuple[str, str]] = []
    pos = 0
    while pos < len(s):
        m = _TOKEN.match(s, pos)
        if m is None or m.end() == pos:
            return None
        pos = m.end()
        if m.group("num") is not None:
            unit = m.group("unit")
            if unit is not None and unit not in _UNITS and unit not in _PLAIN:
                return None
            tokens.append(("num", str(float(m.group("num")) * _UNITS.get(unit or "", 1.0))))
        elif m.group("name") is not None:
            tokens.append(("name", m.group("name")))
        elif m.group("op") is not None:
            tokens.append(("op", m.group("op")))
        else:
            return None
    names = {"tool_diameter": tool.diameter if tool else None, "tool_fluteLength": tool.flute if tool else None}
    k = 0

    def peek() -> tuple[str, str] | None:
        return tokens[k] if k < len(tokens) else None

    def take() -> tuple[str, str]:
        nonlocal k
        if k >= len(tokens):
            raise _Unplain
        k += 1
        return tokens[k - 1]

    def expr() -> float:
        value = term()
        while (t := peek()) is not None and t in (("op", "+"), ("op", "-")):
            take()
            value = value + term() if t[1] == "+" else value - term()
        return value

    def term() -> float:
        value = factor()
        while (t := peek()) is not None and t in (("op", "*"), ("op", "/")):
            take()
            other = factor()
            if t[1] == "/" and other == 0:
                raise _Unplain
            value = value * other if t[1] == "*" else value / other
        return value

    def factor() -> float:
        kind, text_ = take()
        if (kind, text_) == ("op", "-"):
            return -factor()
        if (kind, text_) == ("op", "+"):
            return factor()
        if (kind, text_) == ("op", "("):
            value = expr()
            if take() != ("op", ")"):
                raise _Unplain
            return value
        if kind == "num":
            return float(text_)
        if kind == "name" and text_ in ("Math.min", "Math.max"):
            if take() != ("op", "("):
                raise _Unplain
            values = [expr()]
            while peek() == ("op", ";"):
                take()
                values.append(expr())
            if take() != ("op", ")"):
                raise _Unplain
            return min(values) if text_ == "Math.min" else max(values)
        if kind == "name" and names.get(text_) is not None:
            v = names[text_]
            assert v is not None
            return v
        raise _Unplain

    try:
        value = expr()
    except _Unplain:
        return None
    return value if k == len(tokens) else None
