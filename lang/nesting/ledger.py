"""The inventory written back [Florian, decided in the nesting review,
2026-10-16]: when a nest or a sheet of it is marked as made
(`lang.nesting.pinning`), the pieces on hand it used come out of the
ledger (`inventory.toml`, `lang.nesting.inventory`) and the rests it kept
go in; never on a plain nest run.

The file is Florian's too (he adds the sheets he buys and deletes what is
used elsewhere), so it goes through tomlkit, which keeps what is not
touched as it was written: his comments, blank lines and spellings, and
the order of his entries:

- A piece used comes out of the first entry of its material and size: its
  `count` lowered by one, or the entry removed when none is left, with the
  comment lines right above its `[[stock]]` (no blank line between) and
  one blank line around it. A piece the ledger no longer has (used
  elsewhere and deleted) is noted, not an error.
- A rest kept goes in at the end, as `[[stock]]` with its material, its
  size along the grain first, and a count where a sheet left several of
  one size, under a comment saying where it came from. Where the stock is
  written as an inline array (`stock = [{material = ..., size = ...}]`),
  the rest is appended to the array, its comment beside it where the array
  spans lines.

A file it cannot read (not TOML, or not the ledger's keys) is refused. The
text written is read back and must give exactly the stock meant, else
nothing is written. tomlkit (0.15.2 tried) writes a header spelt
`[[ stock ]]` as `[[stock]]`.
"""
from __future__ import annotations

import tomllib
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomlkit
from tomlkit.container import Container
from tomlkit.exceptions import TOMLKitError
from tomlkit.items import AoT, Array, Comment, Item, Null, Table, Trivia, Whitespace
from tomlkit.toml_document import TOMLDocument

from ..core.errors import LangError
from .inventory import NAME, inventory_from
from .workshop import OnHand

#: How close two sizes (mm) are the same piece.
SAME = 1e-6
#: The first lines of a ledger this writes from nothing.
NEW_FILE = ("# The stock on hand (lang/nesting/inventory.py): full sheets and offcuts alike, by material as\n"
            "# the layout labels it, the size along the grain first (mm), and how many (1 if not given).\n")


@dataclass(frozen=True)
class Piece:
    """A piece of stock: its material and size, along the grain first."""
    material: str
    length: float
    width: float

    def label(self) -> str:
        return f"{self.material} {_number(self.length)}x{_number(self.width)}"


@dataclass(frozen=True)
class Change:
    """What a mark does to the ledger: pieces on hand used, rests kept
    (with a note on where they came from, the comment above them)."""
    taken: tuple[Piece, ...] = ()
    added: tuple[tuple[Piece, str], ...] = ()

    def __bool__(self) -> bool:
        return bool(self.taken or self.added)


def rewrite(text: str, change: Change, where: str = NAME) -> tuple[str, list[str]]:
    """The ledger's text with `change` made (see the module's doc), and
    notes: each piece taken out or not found, each rest added."""
    stock = _read(text, where)
    try:
        doc = tomlkit.parse(text)
    except TOMLKitError as error:
        raise LangError(f"{where}: {error}; the nest writes no ledger it cannot read.") from None
    counts = [o.count for o in stock]
    notes: list[str] = []
    for piece in change.taken:
        k = next((k for k, o in enumerate(stock) if counts[k] > 0 and _same(o, piece)), None)
        if k is None:
            notes.append(f"inventory: no {piece.label()} left to take out (used elsewhere?); left as it is")
            continue
        counts[k] -= 1
        notes.append(f"inventory: -1 {piece.label()}")
    added = _grouped(change.added)
    entries = doc.get("stock")
    if isinstance(entries, Array):
        _edit_array(entries, stock, counts, added)
    else:
        _edit_tables(doc, entries if isinstance(entries, AoT) else None, stock, counts, added)
    notes += [f"inventory: +{n} {piece.label()}" for (piece, _note), n in added]
    new = tomlkit.dumps(doc)
    # Read back: the stock must be what was meant.
    want = [OnHand(o.material, o.length, o.width, n) for o, n in zip(stock, counts) if n > 0]
    want += [OnHand(piece.material, piece.length, piece.width, n) for (piece, _note), n in added]
    if _read(new, where) != want:
        raise LangError(f"{where}: rewriting it would not give the stock meant; it is left as it was.")
    return new, notes


def write_back(path: Path, change: Change) -> list[str]:
    """Rewrites the ledger at `path` with `change` (a new file where there
    is none and something to add); returns the notes."""
    if not change:
        return []
    try:
        text = path.read_text() if path.exists() else ""
    except OSError as error:
        raise LangError(f"{path}: {error.strerror or error}") from None
    new, notes = rewrite(text, change, str(path))
    if new != text:
        scratch = path.with_name(path.name + ".writing")
        scratch.write_text(new)
        scratch.replace(path)
    return notes


# -- [[stock]] tables ---------------------------------------------------------------------------------
#
# tomlkit keeps the comments and blank lines between two tables at the end
# of the first one's body, and those above the first table in the
# document's body before the array; a table's `trivia.indent` is written
# before its header. Items are taken out as tomlkit takes them out, by
# putting a Null in their place, so that the containers' indices hold.

Body = list[tuple[Any, Item]]


def _edit_tables(doc: TOMLDocument, aot: AoT | None, stock: list[OnHand], counts: list[int],
                 added: list[tuple[tuple[Piece, str], int]]) -> None:
    for k in reversed(range(len(stock))):
        assert aot is not None
        if counts[k] == 0:
            _remove_table(doc, aot, k)
        elif counts[k] != stock[k].count:
            aot[k]["count"] = counts[k]
    if aot is not None and not len(aot):
        if "stock" in doc:
            doc.remove("stock")
        aot = None
    for (piece, note), n in added:
        last: Container = aot[-1].value if aot is not None else doc
        if not tomlkit.dumps(doc).strip():
            last.append(None, _comment_lines(NEW_FILE))
        elif not tomlkit.dumps(doc).endswith("\n"):
            last.append(None, Whitespace("\n"))
        if tomlkit.dumps(doc).strip() and not tomlkit.dumps(doc).endswith("\n\n"):
            last.append(None, Whitespace("\n"))
        if note:
            last.append(None, Comment(Trivia(comment=f"# {note}", trail="\n")))
        table = tomlkit.table()
        for key, value in _entry(piece, n).items():
            table[key] = value
        if aot is None:
            aot = tomlkit.aot()
            doc.append("stock", aot)
        aot.append(table)
        table.trivia.indent = ""        # right under its comment


def _remove_table(doc: TOMLDocument, aot: AoT, k: int) -> None:
    """Takes the k-th table out with the comment lines right above it; the
    lines after its keys (loose comments, the next table's) stay where
    they were, one blank line around it less."""
    tables: list[Table] = aot.body
    # The lines above it: at the end of the table before's body, or in the document's before the array.
    before: Body = tables[k - 1].value.body if k else doc.body
    end = len(before) if k else next(j for j, (key, _item) in enumerate(before)
                                     if key is not None and key.key == "stock")
    j = end
    while j > 0 and before[j - 1][0] is None and isinstance(before[j - 1][1], (Comment, Null)):
        j -= 1
    for i in range(j, end):
        before[i] = (None, Null())
    body: Body = tables[k].value.body
    last_key = max(i for i, (key, _item) in enumerate(body) if key is not None)
    tail = [item for _key, item in body[last_key + 1:] if not isinstance(item, Null)]
    above = [item for _key, item in before[:end] if not isinstance(item, Null)]
    if tail and isinstance(tail[0], Whitespace) and (not above or _blank(above[-1])):
        tail[0:1] = _less_one_line(tail[0])
    last = k == len(tables) - 1
    del aot[k]
    if last and all(isinstance(item, Whitespace) for item in tail):
        # The last one: the blank lines before it go too.
        for i in reversed(range(end)):
            key, item = before[i]
            if isinstance(item, Null):
                continue
            if key is not None or not isinstance(item, Whitespace):
                break
            before[i] = (None, Null())
        return
    if k:
        container: Container = tables[k - 1].value
        for item in tail:
            container.append(None, item)
    elif not last:
        nxt = aot.body[0]
        nxt.trivia.indent = "".join(item.as_string() for item in tail) + nxt.trivia.indent
    else:
        doc.remove("stock")
        for item in tail:
            doc.append(None, item)


def _blank(item: Item) -> bool:
    return isinstance(item, Whitespace) and "\n" in item.as_string()


def _less_one_line(item: Whitespace) -> list[Item]:
    text = item.as_string().replace("\n", "", 1)
    return [Whitespace(text)] if "\n" in text else []


def _comment_lines(text: str) -> Comment:
    """Comment lines as one item, written as they are."""
    return Comment(Trivia(comment=text.rstrip("\n"), trail="\n"))


# -- an inline array -------------------------------------------------------------------------------

def _edit_array(array: Array, stock: list[OnHand], counts: list[int],
                added: list[tuple[tuple[Piece, str], int]]) -> None:
    for k in reversed(range(len(stock))):
        if counts[k] == 0:
            del array[k]
        elif counts[k] != stock[k].count:
            array[k]["count"] = counts[k]
    lines = "\n" in array.as_string()
    for (piece, note), n in added:
        table = tomlkit.inline_table()
        table.update(_entry(piece, n))
        if lines:
            array.add_line(table, indent=_indent(array), comment=note or None)
        else:
            array.append(table)


def _indent(array: Array) -> str:
    """The indent of an array's lines, as its first line that holds an item has it."""
    for line in array.as_string().split("\n")[1:]:
        stripped = line.lstrip(" \t")
        if stripped and not stripped.startswith("]"):
            return line[:len(line) - len(stripped)]
    return "  "


# -- helpers ---------------------------------------------------------------------------------------

def _entry(piece: Piece, n: int) -> dict[str, Any]:
    out: dict[str, Any] = {"material": piece.material, "size": [_value(piece.length), _value(piece.width)]}
    if n > 1:
        out["count"] = n
    return out


def _read(text: str, where: str) -> list[OnHand]:
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise LangError(f"{where}: {error}; the nest writes no ledger it cannot read.") from None
    return inventory_from(data, where)


def _same(o: OnHand, piece: Piece) -> bool:
    return (o.material == piece.material and abs(o.length - piece.length) < SAME
            and abs(o.width - piece.width) < SAME)


def _grouped(added: Sequence[tuple[Piece, str]]) -> list[tuple[tuple[Piece, str], int]]:
    groups: dict[tuple[Piece, str], int] = {}
    for key in added:
        groups[key] = groups.get(key, 0) + 1
    return list(groups.items())


def _value(v: float) -> int | float:
    """A size as the ledger writes it: whole millimetres as a whole number,
    else to a thousandth."""
    v = round(float(v), 3)
    return int(v) if v.is_integer() else v


def _number(v: float) -> str:
    return str(_value(v))


__all__ = ["Piece", "Change", "rewrite", "write_back", "NEW_FILE"]
