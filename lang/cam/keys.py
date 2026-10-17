"""The CAM plan's settings (`lang.core.settings`, `design/cam.md`, Keys):
the templates per kind, the cutter, finishing, tabs, the skin and the
release, used where they hold, as the nesting keys are:

    use(cam.cutter("udc"), cam.breakthrough(0.3))           # the root: the workshop
    drawers.use(cam.finish_outer(True))                     # a module
    front.use(cam.tabs("none"))                             # a part
    left.toekick.use(cam.pocket_template("Tasche 6mm"))     # a named operation
    carcass.use(cam.tab_margin(8))                          # a nest (`Scope.nest`)

Nothing reads them during the build, so they are never frozen; the layout
carries them (the parts' with their sources, each nest's own, a named
operation's own) and the plan reads them from there (`resolve`). A key the
plan needs one value of for a nest (`JOINS` "agree": the templates' folder,
the breakthrough, the skin, the smallest cutter) is the nest's own, else
its parts', which must agree, else its default. Every other key is read
per part, nearest first: the operation's own, the nest's, the part's along
its chain, the default [`proposals/settings.md`, The chain]. Operations of
parts with different values are kept apart: one Fusion operation per tool,
kind, template and parameters.

Millimetres unless a key says otherwise. Plain Python without shapely, so a
build file imports them without the plan (`from lang import cam`). A
module of this package must not be named like one of its keys (importing
it would replace the key on the package): the template files are read by
`tooling`, the tabs placed by `tabbing`.
"""
from __future__ import annotations

import math
from typing import Any, Literal, cast

from ..core.errors import LangError
from ..core.layout_types import JsonValue
from ..core.settings import Setting

Join = Literal["agree", "part"]
Cutter = Literal["dc", "udc"]
Tabs = Literal["none", "auto", "forced"]


def _number(value: object, what: str, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise LangError(f"{what} takes a number, not {value!r}.")
    if value < 0 or (positive and value == 0):
        raise LangError(f"{what}: {value!r} must be {'more than 0' if positive else '0 or more'}.")
    return float(value)


def _mm(value: object, what: str) -> float:
    return _number(value, what)


def _positive(value: object, what: str) -> float:
    return _number(value, what, positive=True)


def _positive_or_none(value: object, what: str) -> float | None:
    return None if value is None else _positive(value, what)


def _count(value: object, what: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise LangError(f"{what} takes a whole number, 1 or more, not {value!r}.")
    return value


def _flag(value: object, what: str) -> bool:
    if not isinstance(value, bool):
        raise LangError(f"{what} takes True or False, not {value!r}.")
    return value


def _label(value: object, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LangError(f"{what} takes a template's label, as its file names it after the kind and tags "
                        f"('Kontur 6mm' for contour.dc_Kontur 6mm.f3dhsm-template), not {value!r}.")
    return value


def _label_or_none(value: object, what: str) -> str | None:
    return None if value is None else _label(value, what)


def _labels(value: object, what: str) -> str | tuple[str, ...] | None:
    """None (every template of the kind), a label, or several."""
    if value is None:
        return None
    if isinstance(value, str):
        return (_label(value, what),)
    if isinstance(value, (list, tuple)) and value:
        return tuple(_label(v, what) for v in cast("list[object]", value))
    raise LangError(f"{what} takes None (every template of the kind), a label or a list of labels, not {value!r}.")


def _cutter(value: object, what: str) -> Cutter:
    if value in ("dc", "udc"):
        return value
    raise LangError(f"{what} takes 'dc' (down-cut) or 'udc' (up/down-cut), not {value!r}.")


def _tabs(value: object, what: str) -> Tabs:
    if value in ("none", "auto", "forced"):
        return value
    raise LangError(f"{what} takes 'none', 'auto' or 'forced', not {value!r}.")


def _folder(value: object, what: str) -> str:
    if not isinstance(value, str) or not value:
        raise LangError(f"{what} takes a folder's path, not {value!r}.")
    return value


def _list_or_none(value: str | tuple[str, ...] | None, _frame: object) -> JsonValue:
    return None if value is None else [value] if isinstance(value, str) else [v for v in value]


# -- the templates ------------------------------------------------------------------------------

#: The folder of the `.f3dhsm-template` files, relative to the repository
#: (the folder `lang` is in) unless absolute: Auto Setup's.
templates: Setting[str] = Setting("addins-src/auto_setup/templates", "cam.templates", check=_folder)
#: The cutter variant the templates are taken for: a template tagged `dc`
#: or `udc` is for that cutter only, one without either tag for both.
cutter: Setting[Cutter] = Setting("dc", "cam.cutter", check=_cutter)
#: The contour template, by label: the outer contours and the inner ones
#: whose waste survives (Auto Setup's dialog default). Where its cutter
#: cannot reach all of a contour, the widest one that can is taken.
contour_template: Setting[str] = Setting("Kontur 6mm", "cam.contour_template", check=_label)
#: The pocket template, by label (Auto Setup's dialog default); the widest
#: cutter that reaches a pocket where it does not.
pocket_template: Setting[str] = Setting("Tasche adaptiv 8mm", "cam.pocket_template", check=_label)
#: The bore, drill and dog bone templates the plan may take, by label: None
#: for every template of the kind, the fitting one chosen by its cutter.
bore_template: Setting[str | tuple[str, ...] | None] = Setting(None, "cam.bore_template", check=_labels,
                                                               to_layout=_list_or_none)
drill_template: Setting[str | tuple[str, ...] | None] = Setting(None, "cam.drill_template", check=_labels,
                                                                to_layout=_list_or_none)
dogbone_template: Setting[str | tuple[str, ...] | None] = Setting(None, "cam.dogbone_template", check=_labels,
                                                                  to_layout=_list_or_none)
#: The V-bit's templates, for the chamfers and for the V-grooves, by
#: label: None for the 90 degree bit that reaches deepest.
chamfer_template: Setting[str | None] = Setting(None, "cam.chamfer_template", check=_label_or_none)
groove_template: Setting[str | None] = Setting(None, "cam.groove_template", check=_label_or_none)

# -- finishing ----------------------------------------------------------------------------------

#: Whether outer contours, inner contours and pockets take the template
#: with a finishing pass (tag `finish`), Auto Setup's checkboxes.
finish_outer: Setting[bool] = Setting(False, "cam.finish_outer", check=_flag)
finish_inner: Setting[bool] = Setting(False, "cam.finish_inner", check=_flag)
finish_pockets: Setting[bool] = Setting(False, "cam.finish_pockets", check=_flag)

# -- holding: skin, release, tabs ------------------------------------------------------------

#: How far through cuts go past the stock's bottom (mm), the release
#: contours' bottom.
breakthrough: Setting[float] = Setting(0.2, "cam.breakthrough", check=_mm)
#: The skin the roughing contours leave above the stock's bottom (mm), which
#: the release contours cut [decided 2026-10-17].
skin: Setting[float] = Setting(0.2, "cam.skin", check=_mm)
#: Tabs on a part's outer contour: "auto", none but for a part that holds
#: too little (`tab_margin`, `tab_area`), "forced" or "none" [decided
#: 2026-10-17: none by default, with a safety net for very small and very
#: skinny parts].
tabs: Setting[Tabs] = Setting("auto", "cam.tabs", check=_tabs)
#: The rim of a part's footprint that holds next to nothing on the vacuum
#: bed (mm): a part whose footprint shrunk by it keeps less than
#: `tab_area`, or nothing, gets tabs.
tab_margin: Setting[float] = Setting(6.0, "cam.tab_margin", check=_mm)
#: ... that much (cm²).
tab_area: Setting[float] = Setting(10.0, "cam.tab_area", check=_mm)
#: The fewest tabs a tabbed part gets; more on a long contour.
tab_min_count: Setting[int] = Setting(3, "cam.tab_min_count", check=_count)
#: The tabs' width and height (mm); None: the contour template's.
tab_width: Setting[float | None] = Setting(None, "cam.tab_width", check=_positive_or_none)
tab_height: Setting[float | None] = Setting(None, "cam.tab_height", check=_positive_or_none)
#: The waste inside an inner contour that survives the cut is pocketed
#: away, not released, where its footprint shrunk by `tab_margin` keeps
#: less than this (cm²): the measure and value of the tabs' threshold, so
#: waste that would need tabs as a part does not fly [chosen 2026-10-17;
#: `proposals/cam.md` left the threshold open].
waste_area: Setting[float] = Setting(10.0, "cam.waste_area", check=_mm)
#: The smallest cutter (mm) the nest's manufacturing groups and the checks
#: may count on; None: the narrowest of the templates.
smallest_cutter: Setting[float | None] = Setting(None, "cam.smallest_cutter", check=_positive_or_none)

#: Every CAM key, in the order the plan file lists them.
KEYS: tuple[Setting[Any], ...] = (
    templates, cutter, contour_template, pocket_template, bore_template, drill_template, dogbone_template,
    chamfer_template, groove_template, finish_outer, finish_inner, finish_pockets, breakthrough, skin, tabs,
    tab_margin, tab_area, tab_min_count, tab_width, tab_height, waste_area, smallest_cutter)
#: How the plan takes a key: one value for the nest ("agree"), or per part
#: and operation ("part").
JOINS: dict[str, Join] = {key.name: "agree" if key in (templates, breakthrough, skin, smallest_cutter) else "part"
                          for key in KEYS}
