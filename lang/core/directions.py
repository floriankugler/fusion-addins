"""Directions: six names bound once per project to world axes.

The default frame follows the existing van documents: x runs along the
vehicle (positive toward the rear), y across it (positive toward the
driver's side), z up. A build replaces it with `set_frame(Frame(...))`.
"""
from __future__ import annotations

from dataclasses import dataclass

AXES = ("x", "y", "z")


@dataclass(frozen=True)
class Direction:
    name: str
    axis: str
    sign: int

    def __neg__(self) -> "Direction":
        return frame.direction_of(self.axis, -self.sign)

    @property
    def opposite(self) -> "Direction":
        return -self

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Direction({self.name}: {'+' if self.sign > 0 else '-'}{self.axis})"


class Frame:
    """Binds direction names to axes and signs, plus aliases and the names
    of the three extents (width, depth, height)."""

    def __init__(
        self,
        front: str = "-x", back: str = "+x",
        left: str = "+y", right: str = "-y",
        top: str = "+z", bottom: str = "-z",
        width: str = "y", depth: str = "x", height: str = "z",
        aliases: dict[str, str] | None = None,
    ):
        spec = {"front": front, "back": back, "left": left, "right": right,
                "top": top, "bottom": bottom}
        self._by_name: dict[str, Direction] = {}
        self._by_axis: dict[tuple[str, int], Direction] = {}
        for name, code in spec.items():
            sign = 1 if code[0] == "+" else -1
            axis = code[1]
            if axis not in AXES:
                raise ValueError(f"Direction {name}: unknown axis {axis!r}.")
            direction = Direction(name, axis, sign)
            self._by_name[name] = direction
            if (axis, sign) in self._by_axis:
                raise ValueError(f"Two directions bound to {code}.")
            self._by_axis[(axis, sign)] = direction
        if len(self._by_axis) != 6:
            raise ValueError("A frame needs all six directions.")
        self._aliases = {"up": "top", "down": "bottom"}
        self._aliases.update(aliases or {})
        self.extents = {"width": width, "depth": depth, "height": height}

    def alias(self, name: str, of: str) -> None:
        self._aliases[name] = of

    def direction(self, name: str | Direction) -> Direction:
        if isinstance(name, Direction):
            return name
        key = self._aliases.get(name, name)
        try:
            return self._by_name[key]
        except KeyError:
            raise ValueError(
                f"Unknown direction {name!r}; expected one of "
                f"{', '.join(self._by_name)} or an alias."
            ) from None

    def is_direction(self, name: str) -> bool:
        return name in self._by_name or name in self._aliases

    def direction_of(self, axis: str, sign: int) -> Direction:
        return self._by_axis[(axis, 1 if sign > 0 else -1)]

    def directions(self) -> list[Direction]:
        return list(self._by_name.values())

    def axis_of_extent(self, name: str) -> str:
        return self.extents[name]


frame = Frame()


def set_frame(new_frame: Frame) -> None:
    """Replaces the project frame. Call before creating any part."""
    global frame
    frame = new_frame
