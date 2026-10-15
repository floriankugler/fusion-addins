"""The standard library: building blocks written on the public API only
(`from lang import ...`, nothing from `lang.core`, `lang.joints` or
`lang.hardware`), each with a test and an example (`design/std.md`). A
block that needs an internal shows something the core lacks, and
`tests/test_std.py` holds every module here to the rule.

Build files use them as `from lang.std import carcass, drawer_box`.
"""
from .carcass import Carcass, Front, OpenCarcass, carcass
from .drawers import DrawerBox, drawer_box

__all__ = ["Carcass", "OpenCarcass", "Front", "carcass", "DrawerBox", "drawer_box"]
