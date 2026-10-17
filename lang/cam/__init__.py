"""The CAM plan: a nest's blanks as setups for Fusion, each with its
operations in order, their templates and tools, the features they machine
and the tabs (`design/cam.md`).

    python -m lang.cam examples/drawer_cabinet.py                 # every nest nested
    python -m lang.cam examples/drawer_cabinet.py drawercab.birch_15

After the nest, Fusion-free, like it: `tooling` reads the
`.f3dhsm-template` files, `resolve` the plan's settings from the layout,
`regions` the parts as they lie on their blank, `rules` chooses templates
for holes, pockets, contours, dog bones and the V-bit, `holding` the
release order and which parts get tabs, `tabbing` where, `plan` makes the
setups, `verify` checks them; the plan file's shape is in `plan_types`.
A build file imports only the keys from here (`from lang import cam`),
which load none of that.
"""
from .keys import (breakthrough, chamfer_template, contour_template, cutter, dogbone_template, drill_template,
                   finish_inner, finish_outer, finish_pockets, groove_template, pocket_template, bore_template, skin,
                   smallest_cutter, tab_area, tab_height, tab_margin, tab_min_count, tab_width, tabs, templates,
                   waste_area)

__all__ = ["templates", "cutter", "contour_template", "pocket_template", "bore_template", "drill_template",
           "dogbone_template", "chamfer_template", "groove_template", "finish_outer", "finish_inner",
           "finish_pockets", "breakthrough", "skin", "tabs", "tab_margin", "tab_area", "tab_min_count", "tab_width",
           "tab_height", "waste_area", "smallest_cutter"]
