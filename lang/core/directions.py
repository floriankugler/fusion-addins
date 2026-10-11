"""Directions: six names bound to world axes, per frame.

The world frame is set once per project and follows the van: front is -x,
toward the vehicle's front; left is -y, the driver's side; top is +z. A
build replaces it with `set_frame(Frame(...))`.

A module is written in its own frame, derived from where it faces when it
is placed (`module(name, box, front=box.right)`): front is where it opens,
top stays up, and left and right are a cabinetmaker's, standing in front
of it. `mirrored=True` swaps left and right. Names resolve against the
frame of the scope they are used in (`current_frame()`); the layout file
carries world names (`frame.name_of(direction)`).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Literal

Axis = Literal["x", "y", "z"]
AXES: tuple[Axis, Axis, Axis] = ("x", "y", "z")
DIRECTION_NAMES = ("front", "back", "left", "right", "top", "bottom")
#: The names of a box's three extents, checked by the type checker where a
#: build file uses them (`split("height", 3)`, `grain("depth")`).
ExtentName = Literal["width", "depth", "height"]
EXTENT_NAMES: tuple[ExtentName, ...] = ("width", "depth", "height")
#: The direction whose axis each extent name measures along.
EXTENT_OF: dict[str, str] = {"depth": "front", "width": "left", "height": "top"}
_OPPOSITES = (("front", "back"), ("left", "right"), ("top", "bottom"))


def as_axis(value: str) -> Axis:
    if value == "x" or value == "y" or value == "z":
        return value
    raise ValueError(f"Unknown axis {value!r}.")


def _code(axis: Axis, sign: int) -> str:
    return f"{'+' if sign > 0 else '-'}{axis}"


def _flip(code: str) -> str:
    """The opposite direction code: `-x` for `+x`."""
    return ("-" if code[0] == "+" else "+") + code[1:]


@dataclass(frozen=True)
class Direction:
    name: str
    axis: Axis
    sign: int
    frame: Frame = field(compare=False, hash=False, repr=False)

    def __neg__(self) -> Direction:
        return self.frame.direction_of(self.axis, -self.sign)

    @property
    def opposite(self) -> Direction:
        return -self

    @property
    def code(self) -> str:
        """The world axis and sign, e.g. `-y`."""
        return _code(self.axis, self.sign)

    @property
    def vector(self) -> tuple[int, int, int]:
        v = [0, 0, 0]
        v[AXES.index(self.axis)] = self.sign
        return (v[0], v[1], v[2])

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Direction({self.name}: {self.code})"


def _cross(a: Direction, b: Direction) -> tuple[Axis, int]:
    """The axis and sign of a x b for perpendicular axis directions."""
    va, vb = a.vector, b.vector
    c = (va[1] * vb[2] - va[2] * vb[1], va[2] * vb[0] - va[0] * vb[2], va[0] * vb[1] - va[1] * vb[0])
    for i, component in enumerate(c):
        if component != 0:
            return AXES[i], (1 if component > 0 else -1)
    raise ValueError(f"{a.name} and {b.name} lie on one axis.")


class Frame:
    """Binds direction names to axes and signs, plus aliases. The extents
    `width`, `depth` and `height` measure along the left, front and top
    axes."""

    def __init__(
        self,
        front: str = "-x", back: str | None = None,
        left: str = "-y", right: str | None = None,
        top: str = "+z", bottom: str | None = None,
        aliases: dict[str, str] | None = None,
    ):
        """Each direction as a world axis with a sign, `Frame(front="-x",
        left="-y", top="+z")`; back, right and bottom default to the
        opposites."""
        spec = {"front": front, "back": back or _flip(front), "left": left, "right": right or _flip(left),
                "top": top, "bottom": bottom or _flip(top)}
        self._by_name: dict[str, Direction] = {}
        self._by_axis: dict[tuple[Axis, int], Direction] = {}
        for name, code in spec.items():
            sign = 1 if code[0] == "+" else -1
            axis = as_axis(code[1])
            direction = Direction(name, axis, sign, self)
            self._by_name[name] = direction
            if (axis, sign) in self._by_axis:
                raise ValueError(f"Two directions bound to {code}.")
            self._by_axis[(axis, sign)] = direction
        if len(self._by_axis) != 6:
            raise ValueError("A frame needs all six directions.")
        for a, b in _OPPOSITES:
            if self._by_name[a].axis != self._by_name[b].axis:
                raise ValueError(f"{a} and {b} must lie on one axis.")
        self._aliases: dict[str, str] = {"up": "top", "down": "bottom"}
        self._aliases.update(aliases or {})
        self.extents: dict[str, Axis] = {
            name: self._by_name[direction].axis for name, direction in EXTENT_OF.items()}

    @classmethod
    def derived(cls, front: Direction, up: Direction, mirrored: bool = False) -> Frame:
        """A module's frame: `front` is where it opens, `up` is the
        parent's top, left is a cabinetmaker's (standing in front of the
        module, so front x up), or the other way round when mirrored."""
        left_axis, left_sign = _cross(front, up)
        if mirrored:
            left_sign = -left_sign
        return cls(front=front.code, back=_code(front.axis, -front.sign),
                   left=_code(left_axis, left_sign), right=_code(left_axis, -left_sign),
                   top=up.code, bottom=_code(up.axis, -up.sign))

    def mirrored(self) -> Frame:
        """This frame with left and right swapped."""
        d = self._by_name
        return Frame(front=d["front"].code, back=d["back"].code, left=d["right"].code,
                     right=d["left"].code, top=d["top"].code, bottom=d["bottom"].code,
                     aliases=dict(self._aliases))

    @property
    def is_mirrored(self) -> bool:
        """Whether the frame is left-handed, i.e. its parts are mirror
        images of what the same code gives in a right-handed frame."""
        axis, sign = _cross(self._by_name["front"], self._by_name["top"])
        left = self._by_name["left"]
        return (left.axis, left.sign) != (axis, sign)

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

    def direction_of(self, axis: Axis, sign: int) -> Direction:
        return self._by_axis[(axis, 1 if sign > 0 else -1)]

    def name_of(self, direction: Direction) -> str:
        """The name this frame gives the direction's axis and sign."""
        return self.direction_of(direction.axis, direction.sign).name

    def directions(self) -> list[Direction]:
        return list(self._by_name.values())

    def axis_of_extent(self, name: ExtentName) -> Axis:
        return self.extents[name]

    def axis_of(self, axis_or_name: str) -> Axis:
        """An axis letter, an extent name or a direction name, as an axis."""
        if axis_or_name in ("x", "y", "z"):
            return as_axis(axis_or_name)
        if axis_or_name in self.extents:
            return self.extents[axis_or_name]
        return self.direction(axis_or_name).axis

    def __repr__(self) -> str:
        return "Frame(" + ", ".join(f"{d.name}={d.code}" for d in self._by_name.values()) + ")"


#: The world frame.
frame = Frame()


def set_frame(new_frame: Frame) -> None:
    """Replaces the world frame. Call before creating any part."""
    global frame
    frame = new_frame


_current_provider: Callable[[], Frame] | None = None


def set_current_frame_provider(provider: Callable[[], Frame]) -> None:
    """Installed by `scope`, so that names resolve against the frame of the
    scope being built."""
    global _current_provider
    _current_provider = provider


def current_frame() -> Frame:
    """The frame names resolve against right now: the current scope's, or
    the world frame outside any scope."""
    return _current_provider() if _current_provider is not None else frame
