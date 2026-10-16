"""The inventory written back [Florian, decided in the nesting review,
2026-10-16]: when a nest or a sheet of it is marked as made
(`lang.nesting.pinning`), the pieces on hand it used come out of the
ledger (`inventory.toml`, `lang.nesting.inventory`) and the rests it kept
go in; never on a plain nest run.

The file is Florian's too (he adds the sheets he buys and deletes what is
used elsewhere), so it is rewritten line by line, keeping what it does not
touch as it is, his comments and the order of his entries among it:

- A piece used comes out of the first entry of its material and size: its
  `count` lowered by one, or the entry removed when none is left, with the
  comment lines right above its `[[stock]]` (no blank line between) and
  the blank lines after it. A piece the ledger no longer has (used
  elsewhere and deleted) is noted, not an error.
- A rest kept goes in at the end, as `[[stock]]` with its material, its
  size along the grain first, and a count where a sheet left several of
  one size, under a comment saying where it came from.

A file it cannot read (not TOML, or not the ledger's keys) is refused, and
so is one whose stock is not written as `[[stock]]` tables (an inline
array), which this cannot rewrite line by line. The text written is read
back and must give exactly the stock meant, else nothing is written.
"""
from __future__ import annotations

import re
import tomllib
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from ..core.errors import LangError
from .inventory import NAME, inventory_from
from .workshop import OnHand

_HEADER = re.compile(r"^\s*\[\[\s*stock\s*\]\]\s*(#.*)?$")
_TABLE = re.compile(r"^\s*\[")
_COUNT = re.compile(r"""^(\s*(?:count|"count"|'count')\s*=\s*)(\d+)(\s*(?:#.*)?)$""")
_COMMENT = re.compile(r"^\s*#")
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
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    headers = [k for k, line in enumerate(lines) if _HEADER.match(line)]
    if len(headers) != len(stock) or any(_TABLE.match(line) and not _HEADER.match(line) for line in lines):
        raise LangError(f"{where}: its stock is not written as [[stock]] tables, one per piece; written so, the "
                        "nest can take out the pieces it used and add its rests (it is left as it was).")
    # Each entry's lines: the comments right above its header, the header,
    # and its keys up to the last (comments between them too).
    starts = [_start(lines, k) for k in headers]
    entries: list[tuple[int, int]] = []
    for k, (start, header) in enumerate(zip(starts, headers)):
        limit = starts[k + 1] if k + 1 < len(starts) else len(lines)
        last = max(j for j in range(header, limit) if lines[j].strip() and not _COMMENT.match(lines[j]))
        entries.append((start, last + 1))
    counts = [o.count for o in stock]
    notes: list[str] = []
    for piece in change.taken:
        k = next((k for k, o in enumerate(stock) if counts[k] > 0 and _same(o, piece)), None)
        if k is None:
            notes.append(f"inventory: no {piece.label()} left to take out (used elsewhere?); left as it is")
            continue
        counts[k] -= 1
        notes.append(f"inventory: -1 {piece.label()}")
    gone: set[int] = set()
    for k, (start, end) in enumerate(entries):
        if counts[k] == 0:
            gone.update(range(start, end))
            # One blank line after it goes too where one is left before it.
            if end < len(lines) and not lines[end].strip() and (start == 0 or not lines[start - 1].strip()):
                gone.add(end)
        elif counts[k] != stock[k].count:
            _set_count(lines, headers[k], end, counts[k], where, k)
    out = [line for j, line in enumerate(lines) if j not in gone]
    added = _grouped(change.added)
    if added:
        if not out:
            out.append(NEW_FILE)
        for (piece, note), n in added:
            if out[-1].strip():
                out.append("\n")
            out += ([f"# {note}\n"] if note else []) + ["[[stock]]\n", f'material = "{_escaped(piece.material)}"\n',
                                                        f"size = [{_number(piece.length)}, {_number(piece.width)}]\n"]
            if n > 1:
                out.append(f"count = {n}\n")
            notes.append(f"inventory: +{n} {piece.label()}")
    new = "".join(out)
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


# -- helpers ---------------------------------------------------------------------------------------

def _read(text: str, where: str) -> list[OnHand]:
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise LangError(f"{where}: {error}; the nest writes no ledger it cannot read.") from None
    return inventory_from(data, where)


def _start(lines: Sequence[str], header: int) -> int:
    """Where an entry starts: its header, or the comments right above it."""
    k = header
    while k > 0 and _COMMENT.match(lines[k - 1]) and not _HEADER.match(lines[k - 1]):
        k -= 1
    return k


def _set_count(lines: list[str], header: int, end: int, count: int, where: str, k: int) -> None:
    """Changes an entry's count on its own line (an entry counting more
    than one has one)."""
    for j in range(header, end):
        m = _COUNT.match(lines[j].rstrip("\n"))
        if m is not None:
            lines[j] = f"{m.group(1)}{count}{m.group(3)}\n"
            return
    raise LangError(f"{where}: stock {k + 1}'s count is not on a line of its own; it is left as it was.")


def _same(o: OnHand, piece: Piece) -> bool:
    return (o.material == piece.material and abs(o.length - piece.length) < SAME
            and abs(o.width - piece.width) < SAME)


def _grouped(added: Sequence[tuple[Piece, str]]) -> list[tuple[tuple[Piece, str], int]]:
    groups: dict[tuple[Piece, str], int] = {}
    for key in added:
        groups[key] = groups.get(key, 0) + 1
    return list(groups.items())


def _number(v: float) -> str:
    """A size as the ledger writes it: whole millimetres plain, else to a
    thousandth."""
    text = repr(round(float(v), 3))
    return text[:-2] if text.endswith(".0") else text


def _escaped(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


__all__ = ["Piece", "Change", "rewrite", "write_back", "NEW_FILE"]
