"""Mapping from recognized features to template-based operations.

Holes are handled automatically from the available bore templates (filtered by
the selected cutter variant):
- Through holes larger than BIG_HOLE_LIMIT are machined as inner contours.
- Other holes are bored with the widest cutter that is at least BORE_CLEARANCE
  smaller than the hole. A cutter with less room than that cannot clear its
  chips and burns the wall. In a blind hole the cutter also has to reach the
  centre (hole diameter <= 2 x cutter diameter), or it leaves a core standing;
  in a through hole the core drops out.
- A hole that leaves no cutter that much room is bored with the widest cutter
  that fits into it at all, but only TIGHT_CUT_DEPTH deep, which is as far as
  such a tight cut goes without burn marks.
- A hole no bore cutter fits into at all is drilled - plunged with a cutter of
  exactly its diameter - if a drill template has that cutter, again only
  TIGHT_CUT_DEPTH deep. That is the tightest cut there is.
- Every other hole is skipped with a warning.
Drilling is the last resort only (PREFER_DRILLING is off for now): a hole that
matches a drill template but can be bored is bored. The drill templates still
plunge the corner reliefs that match their tool.

Bores are grouped per hole diameter rather than per tool, because their
feedrate is scaled with the hole: a bore template's feedrate is the one for a
hole the size of the tool, and it grows in proportion from there (see
builder._scale_bore_feed). A feedrate is an operation-wide setting, so two hole
diameters cannot share an operation.

Pockets and contours are chosen by label in the UI; the selected cutter
variant (dc / udc) picks the concrete template file (untagged templates are
valid for any cutter). Finishing: a global mode (none / outer contours / all
contours) plus an additive selection of individual contours or pockets that
get the '.finish' template variant regardless of the mode. Two subtractive
selections override those defaults: features that are not machined at all, and
features that keep their operation but lose the finishing pass. Pocket templates
are validated against the pocket: the widest tool in the template must be
TOOL_CLEARANCE smaller than the corners it has to reach into, its shortest
flute must reach the floor, and a template that clears adaptively is only used
on a floor of at least SMALL_POCKET_AREA. On a misfit the best fitting variant
is substituted with a warning.

A tool wider than an inside corner relief (a dogbone) of the profile cannot
machine it. Those reliefs are collected across all contours, cutouts and pocket
floors and get extra operations after the ones they belong to: a relief
matching a drill template's tool diameter exactly is plunged with it (a contour
pass would degenerate to a point), every other one is machined along its arc as
an open chain by a 'dogbone' template - the one with the widest cutter that
still fits the relief. Because such a corner is machined separately, it places
no demand on the template it came from and is left out of that template's
corner-radius check.

The 45 degree chamfers at the top face (hole, pocket and cutout rims, the outer
contour) and pointed 90 degree grooves belong to the V-bit of the 'chamfer' and
'groove' templates. They are machined whenever they are found, unless the
command switches them off or the skip selection names them. The V-bit is always
the last tool of the setup, whatever its diameter.

Tabs are opt-in per contour: the tab selection accepts edges or faces of an
outer contour or a cutout, resolved to the owning feature. A second selection
takes tabs away again and wins over both the mode and the tab selection.
"""

import math
import os
import adsk.core, adsk.fusion
from dataclasses import dataclass, field
from . import holding, recognition, tabs, templates

# Whether a hole that matches a drill template's tool is drilled rather than
# bored. Off for now: plunging a cutter of exactly the hole's diameter through
# the sheet burns, so a hole is bored whenever a bore cutter fits into it, and
# drilled only when none does (and then only TIGHT_CUT_DEPTH deep). Corner
# reliefs are not affected, they are plunged as before.
PREFER_DRILLING = False
# A hole this close to a drill template's tool diameter is drilled (cm).
DRILL_MATCH_TOL = 0.005
# A cutter needs this much less diameter than the hole it bores (cm).
BORE_CLEARANCE = 0.1
# How deep a hole is machined, measured from the top face, when the cutter has
# less than BORE_CLEARANCE in it - down to none at all for a drilled hole (cm).
TIGHT_CUT_DEPTH = 0.4
# Slack for comparing a cutter with the room a hole leaves it (cm): a 3.175mm
# cutter in a 4.175mm hole has its 1mm, whatever the floats say.
FIT_TOL = 1e-6
# A tool must be at least this much smaller than the narrowest part of the
# feature it machines (cm): a 6mm cutter cannot machine a 6mm wide pocket
# corner or bore a 6mm hole, it has to leave material to remove.
TOOL_CLEARANCE = 0.01
# Through holes larger than this are machined as inner contours, not bores (cm).
BIG_HOLE_LIMIT = 3.0
# Tolerance when checking a tool's flute length against a feature depth (cm).
DEPTH_TOL = 0.005
# Default overcut: how far a through cut reaches past the bottom of the part so
# it breaks through cleanly (cm). The command asks for it; this is the fallback
# for callers that do not, and it is what the templates are authored with.
THROUGH_ALLOWANCE = 0.02
# A tool of exactly a relief's diameter machines it (that is what dogbones are
# drawn for), so only reliefs narrower than the tool by more than this need an
# extra operation (cm).
RELIEF_TOL = 0.005
# Ceiling for the diameter-scaled boring feedrate (mm/min).
MAX_BORE_FEED = 3000.0
# Floor area an adaptive pocket template needs to be worth its while (cm²).
# Below it the clearing passes are all lead-in and corner, and a plain pocket
# template does the job.
SMALL_POCKET_AREA = 25.0
# Resolution of the boring feed scale. Holes whose diameters agree to this much
# share an operation, so modelling noise does not split one into several.
FEED_SCALE_TOL = 3  # decimal places

TAB_NONE = 0
TAB_OUTER = 1
TAB_INNER = 2
TAB_ALL = 3
# Physics-driven: tab exactly the pieces that cannot hold themselves on the
# vacuum bed, at positions chosen by the holding model (see lib.auto_setup.holding).
TAB_AUTO = 4

# Operation order within one tool diameter: holes first (they are drilled into
# solid material), then pockets, then the contours that free the part, and
# finally the corner reliefs left over by a contour tool.
KIND_ORDER = {'drill': 0, 'bore': 1, 'pocket': 2, 'contour': 3, 'dogbone': 4}
# The kinds machined by the V-bit. Their operations are not sorted by tool size
# with the others: the V-bit is the last tool of the setup.
V_BIT_KINDS = ('chamfer', 'groove')
# The flank angle of the V-bit against its axis (degrees), and how far a tool
# may deviate from it.
V_BIT_TAPER = 45.0
V_BIT_TAPER_TOL = 0.1
# A tab can sit below a rim chamfer as long as the chamfer takes no more than
# this share of the sheet thickness; a deeper one counts as thinned material.
TAB_CHAMFER_SHARE = 1 / 3


class RulesError(Exception):
    pass


@dataclass
class Job:
    """One template insertion with the geometry it should be bound to."""
    variant: templates.TemplateVariant
    display_name: str
    holes: list[recognition.Hole] = field(default_factory=list)
    pockets: list[recognition.Pocket] = field(default_factory=list)
    cutouts: list[recognition.Cutout] = field(default_factory=list)
    contours: list[recognition.Contour] = field(default_factory=list)
    is_through: bool | None = None  # holes only
    # Hole diameter in tool diameters, used to scale the boring feedrate; None
    # for everything that is not a bore.
    feed_scale: float | None = None
    # Holes only: stop this far below the top face instead of at the hole
    # bottom (see TIGHT_CUT_DEPTH), with the height of the holes' rim.
    depth_limit: float | None = None
    rim: float = 0.0
    # Single arcs machined as open chains (dogbone reliefs).
    open_chains: list = field(default_factory=list)
    chamfers: list[recognition.Chamfer] = field(default_factory=list)
    grooves: list[recognition.Groove] = field(default_factory=list)
    # Grooves only: how many passes the tool takes above the final one at the
    # groove bottom. None leaves the template as it is (a single pass).
    extra_passes: int | None = None
    tabbed: bool = False
    # Edge loops to place tabs on: (edges, label for warnings, explicit tab
    # points or None for the length-based automatic placement).
    tab_loops: list[tuple[list, str, list | None]] = field(default_factory=list)


@dataclass
class TabPolicy:
    """Tab placement policy from the command UI: a global mode plus an additive
    selection of individual contours (edges/faces of outer contours or cutouts),
    and a subtractive selection that beats both.

    The tab count per contour follows from the contour length with degressive
    density (see tabs.tab_count); min_count is the floor. Mode TAB_AUTO plans
    tabs from the vacuum holding model instead and needs `holding` set."""
    mode: int = TAB_NONE
    selection: list = field(default_factory=list)       # entities (additive)
    skip_selection: list = field(default_factory=list)  # entities (wins)
    min_count: int = 4
    holding: holding.HoldingParams | None = None        # TAB_AUTO calibration


@dataclass
class Assignments:
    """Feature-to-variant choices coming from the command UI."""
    cutter: str | None = None            # 'dc' | 'udc' | None
    pocket_default: str | None = None    # label
    contour_default: str | None = None   # label
    # How far a through cut reaches past the bottom of the part (cm). Decides
    # here how long a tool has to be to cut a feature through; the builder
    # writes it into the operations.
    overcut: float = THROUGH_ALLOWANCE
    finish_outer_all: bool = False       # finishing pass on all outer contours
    finish_cutouts_all: bool = False     # ... on all inner contours (cutouts)
    finish_pockets_all: bool = False     # ... on all pockets
    finish_selection: list = field(default_factory=list)  # entities (additive)
    # Features not to machine at all, and features that keep their roughing
    # operation but lose the finishing pass (wins over finish_selection).
    skip_selection: list = field(default_factory=list)
    no_finish_selection: list = field(default_factory=list)
    # Whether chamfers and V-grooves are machined at all.
    chamfers_enabled: bool = True
    # entityToken of a pocket bottom face -> label
    pocket_overrides: dict[str, str] = field(default_factory=dict)
    # (picked contour entity, label) pairs; resolved to features during planning
    contour_overrides: list[tuple[object, str]] = field(default_factory=list)


@dataclass
class _FeatureSets:
    """The UI selections resolved to features: outer contours by body
    entityToken, cutouts and pockets by index."""
    tab_outer: set[str] = field(default_factory=set)
    tab_cutouts: set[int] = field(default_factory=set)
    no_tab_outer: set[str] = field(default_factory=set)
    no_tab_cutouts: set[int] = field(default_factory=set)
    finish_outer: set[str] = field(default_factory=set)
    finish_cutouts: set[int] = field(default_factory=set)
    finish_pockets: set[int] = field(default_factory=set)
    skip_outer: set[str] = field(default_factory=set)
    skip_cutouts: set[int] = field(default_factory=set)
    skip_pockets: set[int] = field(default_factory=set)
    no_finish_outer: set[str] = field(default_factory=set)
    no_finish_cutouts: set[int] = field(default_factory=set)
    no_finish_pockets: set[int] = field(default_factory=set)


# ---- UI option enumeration ---------------------------------------------------

def pocket_options(registry: dict[str, list[templates.TemplateVariant]]) -> list[str]:
    """Unique pocket labels (finishing is handled by the finish selection)."""
    seen: list[str] = []
    for variant in registry['pocket']:
        if variant.label not in seen:
            seen.append(variant.label)
    return sorted(seen)


def contour_options(registry: dict[str, list[templates.TemplateVariant]]) -> list[str]:
    """Unique contour labels (finishing handled by the finishing mode)."""
    seen: list[str] = []
    for variant in registry['contour']:
        if variant.label not in seen:
            seen.append(variant.label)
    return sorted(seen)


# ---- Selection resolution ----------------------------------------------------

class SelectionResolver:
    """Resolves picked edges/faces to the owning machinable feature.

    Wall faces and boundary edges map to their feature; entities touching
    several features (e.g. the body's bottom face) are treated as ambiguous
    and match nothing.
    """

    def __init__(self, result: recognition.RecognitionResult,
                 cutouts: list[recognition.Cutout],
                 pockets: list[recognition.Pocket]):
        self._map: dict[str, tuple] = {}
        self._ambiguous: set[str] = set()
        for index, cutout in enumerate(cutouts):
            self._add_loop(cutout.edges, ('cutout', index))
        for contour in result.contours:
            self._add_loop(contour.edges, ('outer', contour.body.entityToken))
        for index, pocket in enumerate(pockets):
            bottom = pocket.bottom_face
            self._add(bottom.entityToken, ('pocket', index))
            for edge in bottom.edges:
                self._add(edge.entityToken, ('pocket', index))
                for face in edge.faces:
                    if face.entityToken != bottom.entityToken:
                        self._add(face.entityToken, ('pocket', index))

    def _add_loop(self, edges, feature):
        for edge in edges:
            self._add(edge.entityToken, feature)
            for face in edge.faces:
                self._add(face.entityToken, feature)

    def _add(self, token: str, feature: tuple):
        if token in self._ambiguous:
            return
        existing = self._map.get(token)
        if existing is not None and existing != feature:
            del self._map[token]
            self._ambiguous.add(token)
            return
        self._map[token] = feature

    def resolve(self, entity) -> tuple | None:
        token = entity.entityToken
        if token in self._map:
            return self._map[token]
        edge = adsk.fusion.BRepEdge.cast(entity)
        if edge:
            features = {self._map[f.entityToken] for f in edge.faces if f.entityToken in self._map}
            if len(features) == 1:
                return features.pop()
        return None


# ---- Template resolution -----------------------------------------------------

def _resolve(registry, kind: str, label: str, has_finish: bool, cutter: str | None,
             warnings: list[str]) -> templates.TemplateVariant | None:
    """Pick the concrete template for (label, finish) under the cutter selection."""
    candidates = [v for v in registry[kind] if v.label == label and v.has_finish == has_finish]
    exact = [v for v in candidates if v.cutter == cutter and cutter is not None]
    untagged = [v for v in candidates if v.cutter is None]
    if exact:
        return exact[0]
    if untagged:
        return untagged[0]
    if candidates:
        warnings.append(
            f'No "{label}" {kind} template for the selected cutter; using "{candidates[0].name}".')
        return candidates[0]
    return None


def _resolve_with_finish_fallback(registry, kind: str, label: str, finish_wanted: bool,
                                  cutter: str | None,
                                  warnings: list[str]) -> templates.TemplateVariant | None:
    variant = _resolve(registry, kind, label, finish_wanted, cutter, warnings)
    if variant:
        return variant
    fallback = _resolve(registry, kind, label, not finish_wanted, cutter, warnings)
    if fallback:
        wanted = 'with' if finish_wanted else 'without'
        warnings.append(
            f'No "{label}" {kind} template {wanted} finishing pass; using "{fallback.name}".')
    return fallback


# ---- Planning ----------------------------------------------------------------

def plan(result: recognition.RecognitionResult, registry: dict[str, list[templates.TemplateVariant]],
         assignments: Assignments, tab_policy: TabPolicy | None = None,
         frame: recognition.Frame | None = None) -> tuple[list[Job], list[str]]:
    warnings = list(result.warnings)
    tab_policy = tab_policy or TabPolicy()

    drills = _variants_by_tool_diameter(registry['drill'], assignments.cutter, warnings)
    preferred_drills = drills if PREFER_DRILLING else {}
    bores = _variants_by_tool_diameter(registry['bore'], assignments.cutter, warnings)
    max_bore = max(bores.keys(), default=None)

    # Large through holes become inner contours instead of bores; large blind
    # holes (bigger than 2x the largest bore cutter, which would leave a
    # standing core) become circular pockets.
    small_holes: list[recognition.Hole] = []
    cutouts = list(result.cutouts)
    pockets = list(result.pockets)
    for hole in result.holes:
        if _drill_match(hole.diameter, preferred_drills):
            small_holes.append(hole)
        elif hole.is_through and hole.diameter > BIG_HOLE_LIMIT:
            if hole.bottom_edge:
                cutouts.append(recognition.Cutout(edges=[hole.bottom_edge], body=hole.body,
                                                  depth=hole.depth))
            else:
                warnings.append(
                    f'{hole.body.name}: large hole ⌀{hole.diameter * 10:.1f}mm has no bottom edge; skipped.')
        elif not hole.is_through and max_bore is not None and hole.diameter > 2 * max_bore:
            bottom_face = _blind_hole_bottom_face(hole)
            if bottom_face:
                pockets.append(recognition.Pocket(
                    bottom_face=bottom_face,
                    depth=hole.depth,
                    body=hole.body,
                    corner_radii=[hole.diameter / 2],
                    area=bottom_face.area,
                ))
            else:
                warnings.append(
                    f'{hole.body.name}: large blind hole ⌀{hole.diameter * 10:.1f}mm has no flat '
                    'bottom face; skipped.')
        else:
            small_holes.append(hole)

    resolver = SelectionResolver(result, cutouts, pockets)
    skipped_bevels, skip_selection = _split_bevel_selection(
        result, resolver, assignments.skip_selection)
    sets = _feature_sets(resolver, assignments, tab_policy, skip_selection, warnings)

    outer_overrides: dict[str, str] = {}
    cutout_overrides: dict[int, str] = {}
    for entity, label in assignments.contour_overrides:
        feature = resolver.resolve(entity)
        if feature is None or feature[0] == 'pocket':
            warnings.append(f'A "{label}" contour selection could not be matched to a contour; ignored.')
        elif feature[0] == 'outer':
            outer_overrides[feature[1]] = label
        else:
            cutout_overrides[feature[1]] = label

    tool_limits = _tool_limits_cache()
    auto_positions = None
    if tab_policy.mode == TAB_AUTO:
        auto_positions = _plan_auto_tabs(
            result, cutouts, frame, tab_policy, assignments, registry,
            tool_limits, sets, warnings)
    jobs: list[Job] = []
    jobs += _plan_holes(small_holes, drills, bores, assignments.overcut, warnings)
    pocket_jobs, pocket_reliefs = _plan_pockets(
        pockets, registry, assignments, sets, tool_limits, warnings)
    contour_jobs, contour_reliefs = _plan_contours(
        result, cutouts, registry, assignments, tab_policy.mode, sets,
        outer_overrides, cutout_overrides, drills, tool_limits, warnings,
        auto_positions)
    jobs += pocket_jobs + contour_jobs
    # Reliefs from both sources go into the same pass: one operation per cutter
    # and cut depth, rather than one per feature that happened to have corners.
    jobs += _plan_reliefs(pocket_reliefs + contour_reliefs, registry, drills,
                          assignments.cutter, tool_limits, assignments.overcut, warnings)
    jobs.sort(key=lambda job: _job_order(job, tool_limits))
    # Operations are grouped by tool, widest first, to keep tool changes down;
    # the V-bit comes after all of them.
    jobs += _plan_bevels(result, registry, assignments, sets, resolver,
                         skipped_bevels, warnings)
    return jobs, warnings


def _job_order(job: Job, tool_limits) -> tuple:
    """Widest tool first, so the machine works its way down the tool sizes; per
    diameter by feature kind, and tabbed contours before untabbed ones - a part
    that is already free would move under the next cut."""
    diameter = tool_limits(job.variant).max_diameter or 0.0
    return (-round(diameter, 4),
            KIND_ORDER.get(job.variant.kind, len(KIND_ORDER)),
            0 if job.tabbed else 1)


def _feature_sets(resolver: SelectionResolver, assignments: Assignments,
                  tab_policy: TabPolicy, skip_selection: list,
                  warnings: list[str]) -> _FeatureSets:
    tab_outer, tab_cutouts, _ = _resolve_features(resolver, tab_policy.selection, warnings, 'tab')
    no_tab = _resolve_features(resolver, tab_policy.skip_selection, warnings, 'skip-tab')
    finish = _resolve_features(resolver, assignments.finish_selection, warnings, 'finishing')
    skip = _resolve_features(resolver, skip_selection, warnings, 'skip')
    no_finish = _resolve_features(
        resolver, assignments.no_finish_selection, warnings, 'skip-finishing')
    return _FeatureSets(
        tab_outer=tab_outer, tab_cutouts=tab_cutouts,
        no_tab_outer=no_tab[0], no_tab_cutouts=no_tab[1],
        finish_outer=finish[0], finish_cutouts=finish[1], finish_pockets=finish[2],
        skip_outer=skip[0], skip_cutouts=skip[1], skip_pockets=skip[2],
        no_finish_outer=no_finish[0], no_finish_cutouts=no_finish[1],
        no_finish_pockets=no_finish[2])


def _split_bevel_selection(result: recognition.RecognitionResult,
                           resolver: SelectionResolver,
                           selection: list) -> tuple[set[tuple], list]:
    """Take the chamfers and grooves out of the skip selection.

    A chamfer or a groove is picked by one of its faces, or by an edge that
    belongs to nothing else. Its lower edge is also the top of the wall below
    it, and that stays what it always was: a pick of the contour, cutout or
    pocket the wall belongs to. Returns the picked ('chamfer' | 'groove',
    index) features and the rest of the selection.
    """
    features: dict[str, tuple] = {}
    for index, chamfer in enumerate(result.chamfers):
        for face in chamfer.faces:
            features[face.entityToken] = ('chamfer', index)
    for index, groove in enumerate(result.grooves):
        for entity in groove.faces + groove.edges:
            features[entity.entityToken] = ('groove', index)
    if not features:
        return set(), list(selection)

    picked: set[tuple] = set()
    rest: list = []
    for entity in selection:
        feature = features.get(entity.entityToken)
        edge = adsk.fusion.BRepEdge.cast(entity)
        if feature is None and edge and resolver.resolve(entity) is None:
            feature = next((features[face.entityToken] for face in edge.faces
                            if face.entityToken in features), None)
        if feature is None:
            rest.append(entity)
        else:
            picked.add(feature)
    return picked, rest


def _plan_bevels(result: recognition.RecognitionResult, registry, assignments: Assignments,
                 sets: _FeatureSets, resolver: SelectionResolver,
                 skipped: set[tuple], warnings: list[str]) -> list[Job]:
    """The V-bit operations: one for all chamfers, and one for the grooves per
    number of passes they take. Each chamfer is cut at its own depth and each
    groove along its own bottom edge, so neither has to be split up by size as
    such.

    A groove template that cuts in multiple depths names its maximum stepdown,
    but the Trace operation behind it only takes a fixed number of passes, the
    last one on the groove bottom and the others a stepdown apart above it. The
    number is therefore worked out here, from the groove depth - and grooves
    that need a different number get an operation of their own, or the shallow
    ones would be traced through the air above them first.
    """
    if not assignments.chamfers_enabled:
        return []

    def owner_skipped(chamfer: recognition.Chamfer) -> bool:
        """A feature that is not machined keeps its rim as it is."""
        for wall in chamfer.walls:
            feature = resolver.resolve(wall)
            if feature and feature[1] in {'outer': sets.skip_outer,
                                          'cutout': sets.skip_cutouts,
                                          'pocket': sets.skip_pockets}[feature[0]]:
                return True
        return False

    chamfers = [chamfer for index, chamfer in enumerate(result.chamfers)
                if ('chamfer', index) not in skipped and not owner_skipped(chamfer)]
    grooves = [groove for index, groove in enumerate(result.grooves)
               if ('groove', index) not in skipped]
    jobs: list[Job] = []

    if chamfers:
        picked = _v_bit_variant(registry, 'chamfer', assignments.cutter,
                                f'{len(chamfers)} chamfer(s)', warnings)
        if picked:
            variant, bit = picked
            chamfers = [chamfer for chamfer in chamfers
                        if _chamfer_fits(chamfer, variant, bit, warnings)]
            if chamfers:
                jobs.append(Job(variant=variant,
                                display_name=f'Chamfers ({variant.display_label})',
                                chamfers=chamfers))
    if grooves:
        picked = _v_bit_variant(registry, 'groove', assignments.cutter,
                                f'{len(grooves)} V-groove(s)', warnings)
        if picked:
            variant, bit = picked
            if bit.tip_diameter > TOOL_CLEARANCE:
                warnings.append(
                    f'The "{variant.display_label}" tool has a flat tip of '
                    f'{bit.tip_diameter * 10:.2f}mm and leaves a groove with a flat bottom '
                    'that wide instead of a pointed one; check the operation.')
            deepest = max(groove.depth for groove in grooves)
            if bit.reach is not None and deepest > bit.reach + DEPTH_TOL:
                warnings.append(
                    f'V-groove depth {deepest * 10:.1f}mm exceeds what the '
                    f'"{variant.display_label}" tool can cut ({bit.reach * 10:.1f}mm); '
                    'check the operation.')
            step = templates.stepdown(variant)
            if step is None:
                jobs.append(Job(variant=variant,
                                display_name=f'V-grooves ({variant.display_label})',
                                grooves=grooves))
            else:
                by_passes: dict[int, list[recognition.Groove]] = {}
                for groove in grooves:
                    passes = max(1, math.ceil((groove.depth - DEPTH_TOL) / step))
                    by_passes.setdefault(passes, []).append(groove)
                for passes, group in sorted(by_passes.items()):
                    count = '1 pass' if passes == 1 else f'{passes} passes'
                    jobs.append(Job(
                        variant=variant,
                        display_name=f'V-grooves ({variant.display_label}, {count})',
                        grooves=group, extra_passes=passes - 1))
    return jobs


def _v_bit_variant(registry, kind: str, cutter: str | None, what: str,
                   warnings: list[str]) -> tuple[templates.TemplateVariant, templates.VBit] | None:
    """The template for the chamfers or the grooves with its tool: a 90 degree
    bit if there is one, and among those the one that reaches deepest."""
    candidates = [(variant, templates.v_bit(variant)) for variant in registry[kind]
                  if variant.matches_cutter(cutter)]
    if not candidates:
        warnings.append(
            f'{what} found, but no {kind} template is available; not machined.')
        return None

    def is_right_angle(bit: templates.VBit) -> bool:
        return (bit.taper_angle is not None
                and abs(bit.taper_angle - V_BIT_TAPER) <= V_BIT_TAPER_TOL)

    variant, bit = max(candidates,
                       key=lambda entry: (is_right_angle(entry[1]), entry[1].reach or 0.0))
    if not is_right_angle(bit):
        angle = 'an unknown angle' if bit.taper_angle is None else f'{2 * bit.taper_angle:g}°'
        warnings.append(
            f'The "{variant.display_label}" tool is not a 90° bit ({angle}); it does not '
            f'cut the modelled {kind}s to shape, check the operation.')
    return variant, bit


def _chamfer_fits(chamfer: recognition.Chamfer, variant: templates.TemplateVariant,
                  bit: templates.VBit, warnings: list[str]) -> bool:
    """Whether the tool can cut this chamfer. A chamfer that is merely too
    wide is kept with a warning; the rim of a hole too narrow for the tool
    path is left out, because there is no path to cut it on.

    The tip runs past the lower chamfer edge by the template's tip offset, so
    the flank has to cover the chamfer and the offset, and around a hole the
    tool centre circles that much inside the wall.
    """
    size = f'{chamfer.body.name}: chamfer {chamfer.height * 10:.1f}mm'
    if chamfer.hole_radius is not None:
        path_radius = chamfer.hole_radius - bit.tip_offset - bit.tip_diameter / 2
        if path_radius < TOOL_CLEARANCE:
            _warn_once(
                warnings,
                f'{size} on a ⌀{chamfer.hole_radius * 20:.1f}mm hole is too narrow for the '
                f'"{variant.display_label}" tool with its tip offset of '
                f'{bit.tip_offset * 10:.1f}mm; not machined.')
            return False
    required = chamfer.height + bit.tip_offset
    if bit.reach is not None and required > bit.reach + DEPTH_TOL:
        _warn_once(
            warnings,
            f'{size} needs {required * 10:.1f}mm of cutting flank including the tip '
            f'offset, the "{variant.display_label}" tool has {bit.reach * 10:.1f}mm; '
            'check the operation.')
    return True


def _warn_once(warnings: list[str], message: str):
    """A body with twenty identical holes should not raise twenty warnings."""
    if message not in warnings:
        warnings.append(message)


def _tool_limits_cache():
    """Cached tool limits lookup per template variant (each miss loads a file)."""
    cache: dict[str, templates.ToolLimits] = {}

    def tool_limits(variant: templates.TemplateVariant) -> templates.ToolLimits:
        if variant.name not in cache:
            cache[variant.name] = templates.tool_limits(variant)
        return cache[variant.name]

    return tool_limits


def _drill_match(diameter: float, drills: dict[float, templates.TemplateVariant]) -> bool:
    return any(abs(diameter - tool_dia) < DRILL_MATCH_TOL for tool_dia in drills)


def _blind_hole_bottom_face(hole: recognition.Hole) -> adsk.fusion.BRepFace | None:
    if not hole.bottom_edge:
        return None
    for face in hole.bottom_edge.faces:
        if face.entityToken != hole.face.entityToken and adsk.core.Plane.cast(face.geometry):
            return face
    return None


def _resolve_features(resolver: SelectionResolver, selection, warnings: list[str],
                      purpose: str) -> tuple[set[str], set[int], set[int]]:
    outer_tokens: set[str] = set()
    cutout_ids: set[int] = set()
    pocket_ids: set[int] = set()
    for entity in selection:
        feature = resolver.resolve(entity)
        if feature is None:
            warnings.append(f'A {purpose} selection could not be matched to a contour; ignored.')
        elif feature[0] == 'outer':
            outer_tokens.add(feature[1])
        elif feature[0] == 'cutout':
            cutout_ids.add(feature[1])
        elif feature[0] == 'pocket':
            if purpose == 'tab':
                warnings.append('A tab selection points to a pocket; ignored.')
            else:
                pocket_ids.add(feature[1])
    return outer_tokens, cutout_ids, pocket_ids


def _plan_holes(holes, drills, bores, overcut: float, warnings: list[str]) -> list[Job]:
    if not holes:
        return []
    if not drills and not bores:
        warnings.append('No bore templates found; all holes skipped.')
        return []

    groups: dict[tuple, Job] = {}
    for hole in holes:
        picked = _pick_hole_template(hole, overcut, drills, bores, warnings)
        if not picked:
            warnings.append(
                f'{hole.body.name}: hole ⌀{hole.diameter * 10:.2f}mm is too small for '
                'every bore cutter and matches no drill template; skipped.')
            continue
        variant, tool_dia, depth_limit = picked
        # A bore's feedrate follows the hole diameter, so each diameter needs
        # its own operation. A drill's hole is the size of its tool by
        # definition, so its tool diameter already says everything.
        feed_scale = (round(hole.diameter / tool_dia, FEED_SCALE_TOL)
                      if variant.kind == 'bore' and tool_dia else None)
        # A depth-limited hole is measured from the top face but set from the
        # top of the hole wall, so holes with different rims cannot share one.
        rim = round(hole.rim, 4) if depth_limit is not None else 0.0
        key = (variant.kind, tool_dia, hole.is_through, feed_scale, depth_limit, rim)
        if key not in groups:
            if depth_limit is not None:
                kind_label = f'{depth_limit * 10:g}mm deep'
                if rim:
                    kind_label += f', {rim * 10:g}mm rim'
            else:
                kind_label = 'through' if hole.is_through else 'blind'
            size = f'⌀{hole.diameter * 10:.1f}mm, ' if feed_scale is not None else ''
            groups[key] = Job(
                variant=variant,
                display_name=f'{variant.kind.capitalize()} ({variant.display_label}, '
                             f'{size}{kind_label})',
                is_through=hole.is_through,
                feed_scale=feed_scale,
                depth_limit=depth_limit,
                rim=rim,
            )
        groups[key].holes.append(hole)
    order = lambda key: (0 if key[0] == 'drill' else 1, key[1], key[3] or 0.0, key[2],
                         key[4] or 0.0, key[5])
    return [groups[key] for key in sorted(groups.keys(), key=order)]


def _pick_hole_template(hole, overcut: float, drills, bores, warnings):
    """(template, tool diameter, depth limit or None) for a hole, None if no
    cutter fits into it."""
    diameter = hole.diameter
    required_depth = hole.depth + (overcut if hole.is_through else 0.0)

    def depth_ok(flute):
        return flute is None or flute >= required_depth - DEPTH_TOL

    # A core left in a through hole drops out; in a blind hole it stays.
    no_core = not hole.is_through

    for tool_dia, (variant, flute) in (drills if PREFER_DRILLING else {}).items():
        if abs(diameter - tool_dia) < DRILL_MATCH_TOL:
            if depth_ok(flute):
                return variant, tool_dia, None
            bore_pick = _pick_bore(diameter, BORE_CLEARANCE, required_depth, bores,
                                   require_depth=True, no_core=no_core)
            if bore_pick:
                warnings.append(
                    f'{hole.body.name}: hole ⌀{diameter * 10:.2f}mm is deeper '
                    f'({required_depth * 10:.1f}mm) than the drill tool allows '
                    f'({flute * 10:.1f}mm); boring with "{bore_pick[0].display_label}" instead.')
                return *bore_pick, None
            warnings.append(
                f'{hole.body.name}: hole ⌀{diameter * 10:.2f}mm depth '
                f'{required_depth * 10:.1f}mm exceeds the drill tool\'s maximum '
                f'({flute * 10:.1f}mm) and no bore tool can reach it; check the operation.')
            return variant, tool_dia, None

    bore_pick = _pick_bore(diameter, BORE_CLEARANCE, required_depth, bores,
                           require_depth=True, no_core=no_core)
    if bore_pick:
        return *bore_pick, None
    bore_pick = _pick_bore(diameter, BORE_CLEARANCE, required_depth, bores,
                           require_depth=False, no_core=no_core)
    if bore_pick:
        variant, tool_dia = bore_pick
        flute = bores[tool_dia][1]
        warnings.append(
            f'{hole.body.name}: hole ⌀{diameter * 10:.2f}mm depth '
            f'{required_depth * 10:.1f}mm exceeds every bore tool\'s maximum '
            f'(using "{variant.display_label}", {flute * 10:.1f}mm); check the operation.')
        return *bore_pick, None

    # No cutter has room in this hole - or, in a blind hole, none of those that
    # have also reaches the centre. One that fits at all still opens it up, as
    # deep as a tight cut goes without burning.
    bore_pick = _pick_bore(diameter, TOOL_CLEARANCE, 0.0, bores, require_depth=False)
    if bore_pick:
        variant, tool_dia = bore_pick
        if hole.depth <= TIGHT_CUT_DEPTH + DEPTH_TOL:
            return variant, tool_dia, None  # no deeper than that anyway
        _warn_once(
            warnings,
            f'{hole.body.name}: hole ⌀{diameter * 10:.2f}mm leaves the '
            f'"{variant.display_label}" cutter less than {BORE_CLEARANCE * 10:g}mm of room; '
            f'bored only {TIGHT_CUT_DEPTH * 10:g}mm deep to avoid burn marks.')
        return variant, tool_dia, TIGHT_CUT_DEPTH

    # No bore cutter fits into the hole at all. A cutter of exactly its
    # diameter can still plunge it - the tightest cut of all.
    for tool_dia, (variant, _) in drills.items():
        if abs(diameter - tool_dia) < DRILL_MATCH_TOL:
            if hole.depth <= TIGHT_CUT_DEPTH + DEPTH_TOL:
                return variant, tool_dia, None
            _warn_once(
                warnings,
                f'{hole.body.name}: hole ⌀{diameter * 10:.2f}mm is drilled with '
                f'"{variant.display_label}", a cutter of its own diameter; only '
                f'{TIGHT_CUT_DEPTH * 10:g}mm deep to avoid burn marks.')
            return variant, tool_dia, TIGHT_CUT_DEPTH
    return None


def _pick_bore(diameter, clearance, required_depth, bores, require_depth, no_core=False):
    """The widest bore cutter that is at least `clearance` smaller than the
    hole: (template, tool diameter), or None. With no_core the cutter also has
    to reach the centre of the hole, so that nothing is left standing in it."""
    candidates = []
    for tool_dia, (variant, flute) in bores.items():
        if tool_dia > diameter - clearance + FIT_TOL:
            continue
        if no_core and 2 * tool_dia < diameter - FIT_TOL:
            continue
        if require_depth and flute is not None and flute < required_depth - DEPTH_TOL:
            continue
        candidates.append(tool_dia)
    if not candidates:
        return None
    tool_dia = max(candidates)
    return bores[tool_dia][0], tool_dia


def _plan_pockets(pockets, registry, assignments: Assignments, sets: _FeatureSets,
                  tool_limits, warnings: list[str]) -> tuple[list[Job], list[recognition.Relief]]:
    if not pockets:
        return [], []

    def binding_radius(variant: templates.TemplateVariant,
                       pocket: recognition.Pocket) -> float | None:
        """The tightest corner the template's own tool has to reach into.

        Corners narrower than its finest tool are corner reliefs - dogbones -
        and are cut by a separate operation (see _reliefs), so they place no
        demand on this template and are left out.
        """
        relieved = tool_limits(variant).min_diameter
        radii = [r for r in pocket.corner_radii
                 if relieved is None or 2 * r >= relieved - RELIEF_TOL]
        return min(radii, default=None)

    def fits_radius(variant: templates.TemplateVariant, pocket: recognition.Pocket) -> bool:
        radius = binding_radius(variant, pocket)
        if radius is None:
            return True
        diameter = tool_limits(variant).max_diameter
        # The tool has to fit into the corner with room to cut: its diameter
        # must stay below the corner's diameter by at least TOOL_CLEARANCE.
        return diameter is None or diameter <= 2 * radius - TOOL_CLEARANCE

    def fits_depth(variant: templates.TemplateVariant, pocket: recognition.Pocket) -> bool:
        flute = tool_limits(variant).min_flute
        return flute is None or flute >= pocket.depth - DEPTH_TOL

    # Each miss loads a template file, and the same variant is asked about once
    # per pocket and again for every substitution candidate.
    adaptive: dict[str, bool] = {}

    def is_adaptive(variant: templates.TemplateVariant) -> bool:
        if variant.name not in adaptive:
            adaptive[variant.name] = templates.is_adaptive(variant)
        return adaptive[variant.name]

    def fits_area(variant: templates.TemplateVariant, pocket: recognition.Pocket) -> bool:
        return not is_adaptive(variant) or pocket.area >= SMALL_POCKET_AREA

    def fits(variant, pocket):
        return (fits_radius(variant, pocket) and fits_depth(variant, pocket)
                and fits_area(variant, pocket))

    reliefs: list[recognition.Relief] = []
    groups: dict[str, Job] = {}
    for index, pocket in enumerate(pockets):
        if index in sets.skip_pockets:
            continue
        token = pocket.bottom_face.entityToken
        is_override = token in assignments.pocket_overrides
        label = assignments.pocket_overrides.get(token, assignments.pocket_default)
        if label is None:
            warnings.append('No pocket template available; pockets skipped.')
            return []
        finish = ((assignments.finish_pockets_all or index in sets.finish_pockets)
                  and index not in sets.no_finish_pockets)
        variant = _resolve_with_finish_fallback(
            registry, 'pocket', label, finish, assignments.cutter, warnings)
        if variant is None:
            warnings.append(f'No pocket template found for "{label}"; pocket skipped.')
            continue

        problems = []
        if not fits_radius(variant, pocket):
            problems.append(f'corner radius {binding_radius(variant, pocket) * 10:.1f}mm')
        if not fits_depth(variant, pocket):
            problems.append(f'depth {pocket.depth * 10:.1f}mm')
        if not fits_area(variant, pocket):
            problems.append(f'area {pocket.area:.1f}cm²')
        if problems:
            reason = ' and '.join(problems)
            if is_override:
                warnings.append(
                    f'{pocket.body.name}: pocket {reason} does not suit the assigned '
                    f'"{variant.display_label}" tool; check the operation.')
            else:
                eligible = [v for v in registry['pocket'] if v.matches_cutter(assignments.cutter)]
                replacement = _best_fitting_variant(eligible, variant, pocket, fits, tool_limits)
                if replacement:
                    warnings.append(
                        f'{pocket.body.name}: pocket {reason} does not suit '
                        f'"{variant.display_label}"; using "{replacement.display_label}" instead.')
                    variant = replacement
                else:
                    warnings.append(
                        f'{pocket.body.name}: pocket {reason} does not suit any pocket '
                        f'template; keeping "{variant.display_label}", check the operation.')
        reliefs += _reliefs(variant, _pocket_edges(pocket), pocket.depth, tool_limits,
                            is_through=False)
        if variant.name not in groups:
            groups[variant.name] = Job(
                variant=variant, display_name=f'Pockets ({variant.display_label})')
        groups[variant.name].pockets.append(pocket)
    return list(groups.values()), reliefs


def _pocket_edges(pocket: recognition.Pocket) -> list[adsk.fusion.BRepEdge]:
    """Every boundary edge of the pocket floor. Islands come along: their walls
    are convex, so corner_reliefs discards them by itself."""
    return [edge for loop in pocket.bottom_face.loops for edge in loop.edges]


def _best_fitting_variant(variants, chosen, pocket, fits, tool_limits):
    """Among fitting variants prefer the chosen finishing flag and similar labels,
    then the largest tool."""
    candidates = [v for v in variants if fits(v, pocket)]
    if not candidates:
        return None
    def rank(variant):
        prefix = len(os.path.commonprefix([variant.label, chosen.label]))
        return (variant.has_finish == chosen.has_finish, prefix,
                tool_limits(variant).max_diameter or 0.0)
    return max(candidates, key=rank)


def _contour_depth_check(registry, variant, feature_depth, cutter, tool_limits,
                         overcut: float, context: str,
                         warnings: list[str]) -> templates.TemplateVariant:
    """Ensure the contour template's tool can cut through the stock; substitute
    a depth-capable variant (same finish flag) or warn."""
    required = feature_depth + overcut
    flute = tool_limits(variant).min_flute
    if flute is None or flute >= required - DEPTH_TOL:
        return variant
    candidates = [
        v for v in registry['contour']
        if v.matches_cutter(cutter) and v.has_finish == variant.has_finish
        and (tool_limits(v).min_flute is None
             or tool_limits(v).min_flute >= required - DEPTH_TOL)
    ]
    if candidates:
        def rank(v):
            prefix = len(os.path.commonprefix([v.label, variant.label]))
            return (prefix, tool_limits(v).max_diameter or 0.0)
        replacement = max(candidates, key=rank)
        warnings.append(
            f'{context}: cut depth {required * 10:.1f}mm exceeds the "{variant.display_label}" '
            f'tool ({flute * 10:.1f}mm); using "{replacement.display_label}" instead.')
        return replacement
    warnings.append(
        f'{context}: cut depth {required * 10:.1f}mm exceeds every contour template '
        f'(keeping "{variant.display_label}", {flute * 10:.1f}mm); check the operation.')
    return variant


# A tab needs the full sheet thickness above it: no tabs where material was
# milled off the top, nor within this distance of such a stretch, measured
# along the contour (cm).
THICKNESS_MARGIN = 1.0
# The top face boundary counts as running "directly above" the bottom contour
# within this XY deviation (cm) - covers outline sampling error, nothing more.
FULL_THICKNESS_TOL = 0.1


def _near_outline(x: float, y: float, outline: list, tolerance: float) -> bool:
    """Whether an XY point lies within tolerance of a closed polyline."""
    limit = tolerance * tolerance
    count = len(outline)
    for i in range(count):
        x1, y1 = outline[i]
        x2, y2 = outline[(i + 1) % count]
        dx, dy = x2 - x1, y2 - y1
        squared = dx * dx + dy * dy
        t = 0.0 if squared < 1e-18 else max(
            0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / squared))
        px, py = x - x1 - t * dx, y - y1 - t * dy
        if px * px + py * py <= limit:
            return True
    return False


def _plan_auto_tabs(result, cutouts, frame, tab_policy: TabPolicy,
                    assignments: Assignments, registry, tool_limits,
                    sets: _FeatureSets, warnings: list[str]) -> dict | None:
    """Physics-driven tab planning (TAB_AUTO).

    Decomposes the sheet with the holding model, asks the planner which parts
    cannot hold themselves, and where tabs must go to merge them into
    assemblies that do (see holding.plan_tabs). Only the setup's actual parts
    have to be held: waste - offcuts, the skeleton, cutout waste - may shift
    once it is free, so it never gets a requirement of its own (unless the
    user selects it), but it serves as anchorage. A part offers tab sites on
    its outer contour AND on its cutout loops - a tab there ties the part to
    its own cutout waste, whose footprint then counts towards the holding.

    Marks the tabbed features in `sets` - the ordinary selection machinery
    then gives them tabbed operations - and returns the planned positions
    keyed by id(edge loop). None disables tabs entirely.

    The kerf raster and the tab width come from the default contour template;
    a per-feature override with a different tool is close enough for holding
    purposes.
    """
    if frame is None or tab_policy.holding is None:
        warnings.append('Automatic tabs need the machining frame and holding '
                        'calibration; no tabs placed.')
        return None
    variant = None
    if assignments.contour_default:
        variant = _resolve_with_finish_fallback(
            registry, 'contour', assignments.contour_default, False,
            assignments.cutter, warnings)
    kerf = (tool_limits(variant).max_diameter if variant else None) or 0.6
    width = (templates.tab_width(variant) if variant else None) or 0.8

    try:
        setup_sheet = holding.decompose_setup(
            result, frame, tab_policy.holding,
            kerfs={c.body.entityToken: kerf for c in result.contours},
            cutouts_override=cutouts)
    except ValueError:
        warnings.append('Automatic tabs: nothing to analyze; no tabs placed.')
        return None
    sheet = setup_sheet.sheet

    requests: list[holding.TabRequest] = []
    loop_feature: dict[int, tuple] = {}  # id(edges) -> ('outer', token) | ('cutout', index)
    points: dict[tuple, adsk.core.Point3D] = {}
    top_outlines: dict[str, list] = {}   # body entityToken -> full-height top outlines
    rim_chamfers: dict[str, float] = {}  # body entityToken -> widest shallow rim chamfer

    def full_thickness(loop, position: float, body) -> bool:
        """True if the part carries the full sheet thickness above this stretch
        of the contour (THICKNESS_MARGIN to each side along the loop).

        Where nothing was milled off the top, the boundary of the body's top
        face runs directly above the bottom contour; a pocket or rabbet
        reaching the contour makes it detour inward. A tab under such thinned
        material can be taller than what is left above it. A shallow rim
        chamfer sets the boundary back as well, by its own width, and that
        much is allowed for (see rim_chamfer).
        """
        token = body.entityToken
        if token not in top_outlines:
            top_outlines[token] = _top_face_outlines(body)
        outlines = top_outlines[token]
        if not outlines:
            return False
        tolerance = FULL_THICKNESS_TOL + rim_chamfer(body)
        for offset in (-THICKNESS_MARGIN, 0.0, THICKNESS_MARGIN):
            point = loop.point_at(position + offset)
            x = point.asVector().dotProduct(frame.x)
            y = point.asVector().dotProduct(frame.y)
            if not any(_near_outline(x, y, outline, tolerance)
                       for outline in outlines):
                return False
        return True

    def rim_chamfer(body) -> float:
        """How far a rim chamfer sets the top face boundary back from the
        contour below it. A chamfer only takes the top corner off, which a tab
        does not need - unless it is so deep that it thins the sheet out like
        a rabbet would (TAB_CHAMFER_SHARE)."""
        token = body.entityToken
        if token not in rim_chamfers:
            z_low, z_high = [f(frame.height(v.geometry) for v in body.vertices)
                             for f in (min, max)]
            limit = (z_high - z_low) * TAB_CHAMFER_SHARE
            rim_chamfers[token] = max(
                (chamfer.height for chamfer in result.chamfers
                 if chamfer.body.entityToken == token and chamfer.height <= limit),
                default=0.0)
        return rim_chamfers[token]

    def _top_face_outlines(body) -> list:
        """Every loop of the body's full-height top faces, projected to frame
        XY: the outer loops trace the contour where it is full thickness, the
        inner ones do the same above cutouts."""
        z_max = max(frame.height(v.geometry) for v in body.vertices)
        outlines = []
        for face in body.faces:
            if not adsk.core.Plane.cast(face.geometry):
                continue
            _, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
            if normal.dotProduct(frame.z) < 1 - recognition.DIRECTION_TOL:
                continue
            if frame.height(face.pointOnFace) < z_max - recognition.HEIGHT_TOL:
                continue
            for face_loop in face.loops:
                outlines.append(
                    [(p.asVector().dotProduct(frame.x), p.asVector().dotProduct(frame.y))
                     for p in tabs.loop_outline(list(face_loop.edges)).points])
        return outlines

    def loop_candidates(edges: list, feature: tuple, body) -> list:
        loop_feature[id(edges)] = feature
        loop, sites = tabs.candidate_positions(edges, width)
        entries = []
        for n, (position, point) in enumerate(sites):
            if not full_thickness(loop, position, body):
                continue
            key = (id(edges), n)
            points[key] = point
            entries.append((point.asVector().dotProduct(frame.x),
                            point.asVector().dotProduct(frame.y), key))
        return entries

    def add_request(piece: int, candidates: list, forced: bool):
        requests.append(holding.TabRequest(
            piece=piece, candidates=candidates,
            bridge=holding.BRIDGE_FACTOR * kerf,
            min_count=tab_policy.min_count,
            min_separation=tabs.MIN_SEPARATION_FACTOR * width,
            forced=forced))

    part_cutouts: dict[str, list] = {}
    for index, cutout in enumerate(cutouts):
        part_cutouts.setdefault(cutout.body.entityToken, []).append((index, cutout))

    for contour in result.contours:
        token = contour.body.entityToken
        piece = setup_sheet.part_pieces.get(token)
        if (piece is None or not contour.edges or token in sets.skip_outer
                or token in sets.no_tab_outer):
            continue
        candidates = loop_candidates(contour.edges, ('outer', token), contour.body)
        for index, cutout in part_cutouts.get(token, []):
            if index in sets.skip_cutouts or index in sets.no_tab_cutouts:
                continue
            candidates += loop_candidates(cutout.edges, ('cutout', index), cutout.body)
        add_request(piece, candidates, token in sets.tab_outer)
    # Waste never has to be held - it may shift once free - so only cutout
    # waste the user explicitly selected gets a requirement of its own.
    for index, cutout in enumerate(cutouts):
        if (index not in sets.tab_cutouts or index in sets.skip_cutouts
                or index in sets.no_tab_cutouts):
            continue
        piece = setup_sheet.cutout_pieces.get(index)
        if piece is None:
            continue  # milled away entirely; nothing left to hold
        add_request(piece, loop_candidates(cutout.edges, ('cutout', index), cutout.body),
                    True)

    plans, lines, plan_warnings = holding.plan_tabs(sheet, requests)
    warnings += plan_warnings
    warnings += [f'Tabs — {line}' for line in lines]

    positions: dict[int, list] = {}
    placed: set[tuple] = set()
    for plan in plans:
        for _, _, key, _ in plan.chosen:
            if key in placed:
                continue  # the same site chosen through two requests
            placed.add(key)
            kind, feature = loop_feature[key[0]]
            if kind == 'outer':
                sets.tab_outer.add(feature)
            else:
                sets.tab_cutouts.add(feature)
            positions.setdefault(key[0], []).append(points[key])
    return positions


def _plan_contours(result, cutouts, registry, assignments: Assignments, tab_mode: int,
                   sets: _FeatureSets,
                   outer_overrides: dict[str, str], cutout_overrides: dict[int, str],
                   drills, tool_limits, warnings: list[str],
                   auto_positions: dict | None = None,
                   ) -> tuple[list[Job], list[recognition.Relief]]:
    if not cutouts and not result.contours:
        return [], []

    def planned_positions(edges: list) -> list | None:
        """Explicit tab points for a loop (TAB_AUTO), or None for the density
        placement. An empty list means the planner could not place any."""
        if auto_positions is None:
            return None
        return auto_positions.get(id(edges), [])
    if assignments.contour_default is None and not outer_overrides and not cutout_overrides:
        warnings.append('No contour template available; cutouts and contours skipped.')
        return [], []

    def finish_wanted(is_outer: bool, selected: bool, excluded: bool) -> bool:
        if excluded:
            return False
        if selected:
            return True
        return assignments.finish_outer_all if is_outer else assignments.finish_cutouts_all

    # Inside corner reliefs left over by the contour tools.
    reliefs: list[recognition.Relief] = []

    # Tabbed and untabbed features get separate operations so the tabbed ones
    # can run first (see _job_order): a part that is already free would move
    # under the next cut. Mixing them would be safe as far as tabs go - the
    # builder pins the automatic tab count to zero, so only contours with an
    # explicit position are tabbed.
    cutout_groups: dict[tuple[str, bool], Job] = {}
    for index, cutout in enumerate(cutouts):
        if index in sets.skip_cutouts:
            continue
        label = cutout_overrides.get(index, assignments.contour_default)
        if label is None:
            warnings.append(f'{cutout.body.name}: cutout has no contour template; skipped.')
            continue
        finish = finish_wanted(False, index in sets.finish_cutouts,
                               index in sets.no_finish_cutouts)
        variant = _resolve_with_finish_fallback(
            registry, 'contour', label, finish, assignments.cutter, warnings)
        if variant is None:
            warnings.append(f'No contour template found for "{label}"; cutout skipped.')
            continue
        variant = _contour_depth_check(
            registry, variant, cutout.depth, assignments.cutter, tool_limits,
            assignments.overcut, f'{cutout.body.name} cutout', warnings)
        reliefs += _reliefs(variant, cutout.edges, cutout.depth, tool_limits)
        tabbed = ((tab_mode in (TAB_INNER, TAB_ALL) or index in sets.tab_cutouts)
                  and index not in sets.no_tab_cutouts)
        key = (variant.name, tabbed)
        if key not in cutout_groups:
            suffix = ', tabs' if tabbed else ''
            cutout_groups[key] = Job(
                variant=variant, display_name=f'Cutouts ({variant.display_label}{suffix})',
                tabbed=tabbed)
        cutout_groups[key].cutouts.append(cutout)
        if tabbed:
            cutout_groups[key].tab_loops.append(
                (cutout.edges, f'{cutout.body.name} cutout',
                 planned_positions(cutout.edges)))

    contour_groups: dict[tuple[str, bool], Job] = {}
    for contour in result.contours:
        body_token = contour.body.entityToken
        if body_token in sets.skip_outer:
            continue
        label = outer_overrides.get(body_token, assignments.contour_default)
        if label is None:
            warnings.append(f'{contour.body.name}: outer contour has no template; skipped.')
            continue
        finish = finish_wanted(True, body_token in sets.finish_outer,
                               body_token in sets.no_finish_outer)
        variant = _resolve_with_finish_fallback(
            registry, 'contour', label, finish, assignments.cutter, warnings)
        if variant is None:
            warnings.append(f'No contour template found for "{label}"; outer contour skipped.')
            continue
        variant = _contour_depth_check(
            registry, variant, contour.depth, assignments.cutter, tool_limits,
            assignments.overcut, f'{contour.body.name} outer contour', warnings)
        reliefs += _reliefs(variant, contour.edges, contour.depth, tool_limits)
        tabbed = ((tab_mode in (TAB_OUTER, TAB_ALL) or body_token in sets.tab_outer)
                  and body_token not in sets.no_tab_outer)
        if tabbed and not contour.edges:
            warnings.append(
                f'{contour.body.name}: no planar bottom face; cannot place tabs on the outer contour.')
            tabbed = False
        key = (variant.name, tabbed)
        if key not in contour_groups:
            suffix = ', tabs' if tabbed else ''
            contour_groups[key] = Job(
                variant=variant, display_name=f'Outer contours ({variant.display_label}{suffix})',
                tabbed=tabbed)
        contour_groups[key].contours.append(contour)
        if tabbed:
            contour_groups[key].tab_loops.append(
                (contour.edges, f'{contour.body.name} outer contour',
                 planned_positions(contour.edges)))

    return list(cutout_groups.values()) + list(contour_groups.values()), reliefs


def _reliefs(variant: templates.TemplateVariant, edges, depth: float,
             tool_limits, is_through: bool = True) -> list[recognition.Relief]:
    """Inside corner reliefs of one contour or pocket floor that its own tool is
    too wide for.

    The narrowest tool of the template decides: it is the one that reaches
    furthest into the corners."""
    diameter = tool_limits(variant).min_diameter
    if diameter is None:
        return []
    return recognition.corner_reliefs(edges, diameter - RELIEF_TOL, depth, is_through)


def _plan_reliefs(reliefs: list[recognition.Relief], registry, drills, cutter: str | None,
                  tool_limits, overcut: float, warnings: list[str]) -> list[Job]:
    """Extra operations for the reliefs the contour operations left behind:
    plunged with an exactly fitting drill where one exists, milled along the arc
    with the dogbone template otherwise."""
    if not reliefs:
        return []

    # A relief on a pocket floor is cut to that floor, one through the stock is
    # cut past the bottom, so the two cannot share an operation.
    drill_groups: dict[tuple[str, bool], Job] = {}
    milled: list[recognition.Relief] = []
    for relief in reliefs:
        variant = _drill_for_relief(relief, drills)
        if not variant:
            milled.append(relief)
            continue
        key = (variant.name, relief.is_through)
        if key not in drill_groups:
            suffix = '' if relief.is_through else ', pocket'
            drill_groups[key] = Job(
                variant=variant,
                display_name=f'Dogbones ({variant.display_label}{suffix})',
                is_through=relief.is_through,
            )
        # A relief is a partial hole: the drill strategy takes its wall face.
        drill_groups[key].holes.append(recognition.Hole(
            face=relief.face, diameter=relief.diameter, depth=relief.depth,
            is_through=relief.is_through, body=relief.face.body))

    for job in drill_groups.values():
        flute = tool_limits(job.variant).min_flute
        required = max(hole.depth for hole in job.holes)
        if job.is_through:
            required += overcut
        if flute is not None and flute < required - DEPTH_TOL:
            warnings.append(
                f'Dogbone cut depth {required * 10:.1f}mm exceeds the '
                f'"{job.variant.display_label}" tool ({flute * 10:.1f}mm); check the operation.')

    return list(drill_groups.values()) + _plan_milled_reliefs(
        milled, registry, cutter, tool_limits, overcut, warnings)


def _drill_for_relief(relief: recognition.Relief,
                      drills) -> templates.TemplateVariant | None:
    """The drill template whose tool has exactly the relief's diameter, if any:
    such a relief is removed by a single plunge at its centre, while a contour
    pass along it would degenerate to a point."""
    for tool_dia, (variant, _) in drills.items():
        if abs(relief.diameter - tool_dia) < DRILL_MATCH_TOL:
            return variant
    return None


def _plan_milled_reliefs(reliefs: list[recognition.Relief], registry, cutter: str | None,
                         tool_limits, overcut: float, warnings: list[str]) -> list[Job]:
    """Operations with the dogbone cutters, machining each relief along its arc
    as an open chain.

    Each relief gets the widest dogbone cutter that still fits it: a small
    cutter is slow and fragile, so it only takes the reliefs the next bigger
    one cannot get into.

    One operation per cut depth: the dogbone template takes its bottom height
    from the selected contour, which is a single height for the whole
    operation, so reliefs sitting at different levels - the stock bottom, and
    the floor of every pocket depth - have to be kept apart.
    """
    if not reliefs:
        return []
    candidates = [v for v in registry['dogbone'] if v.matches_cutter(cutter)]
    if not candidates:
        warnings.append(
            f'{len(reliefs)} dogbone(s) are too small for the contour tool, but no dogbone '
            'template is available; they are not machined.')
        return []
    candidates.sort(key=lambda v: tool_limits(v).max_diameter or 0.0)
    smallest_variant = candidates[0]

    def cutter_for(relief: recognition.Relief) -> templates.TemplateVariant:
        fitting = [v for v in candidates
                   if (tool_limits(v).max_diameter or 0.0) <= relief.diameter - RELIEF_TOL]
        return fitting[-1] if fitting else smallest_variant

    smallest = min(relief.diameter for relief in reliefs)
    limits = tool_limits(smallest_variant)
    if limits.max_diameter is not None and limits.max_diameter > smallest - RELIEF_TOL:
        warnings.append(
            f'The smallest dogbone (⌀{smallest * 10:.2f}mm) is not wider than the '
            f'"{smallest_variant.display_label}" tool (⌀{limits.max_diameter * 10:.2f}mm), '
            'which leaves it nothing to cut; check the operation.')

    # A relief hangs from the top face, so equal depths sit at equal heights.
    levels: dict[tuple[float, str, float, bool], list[recognition.Relief]] = {}
    variants: dict[str, templates.TemplateVariant] = {}
    for relief in reliefs:
        variant = cutter_for(relief)
        variants[variant.name] = variant
        # Keyed by tool diameter first, so the operations come out widest
        # cutter first like everything else.
        key = (-(tool_limits(variant).max_diameter or 0.0), variant.name,
               round(relief.depth, 4), relief.is_through)
        levels.setdefault(key, []).append(relief)

    jobs: list[Job] = []
    for (_, name, depth, is_through), group in sorted(levels.items()):
        variant = variants[name]
        limits = tool_limits(variant)
        required = depth + (overcut if is_through else 0.0)
        if limits.min_flute is not None and limits.min_flute < required - DEPTH_TOL:
            warnings.append(
                f'Dogbone cut depth {required * 10:.1f}mm exceeds the "{variant.display_label}" '
                f'tool ({limits.min_flute * 10:.1f}mm); check the operation.')
        suffix = '' if is_through else f', pocket {depth * 10:.1f}mm'
        jobs.append(Job(
            variant=variant,
            display_name=f'Dogbones ({variant.display_label}{suffix})',
            open_chains=[relief.edge for relief in group],
            is_through=is_through,
        ))
    return jobs


def _variants_by_tool_diameter(
        variants: list[templates.TemplateVariant], cutter: str | None,
        warnings: list[str]) -> dict[float, tuple[templates.TemplateVariant, float | None]]:
    """Diameter -> (variant, flute length) for the eligible hole templates."""
    eligible = [v for v in variants if v.matches_cutter(cutter)]
    # Prefer cutter-tagged templates over untagged ones at the same diameter.
    eligible.sort(key=lambda v: v.cutter is None)
    result: dict[float, tuple[templates.TemplateVariant, float | None]] = {}
    for variant in eligible:
        diameter, flute = templates.primary_tool(variant)
        if diameter is None:
            continue
        existing = result.get(diameter)
        if existing:
            if existing[0].cutter is not None and variant.cutter is not None:
                warnings.append(
                    f'Multiple {variant.kind} templates share tool diameter {diameter * 10:.2f}mm; '
                    f'using "{existing[0].display_label}", ignoring "{variant.display_label}".')
            continue
        result[diameter] = (variant, flute)
    return result
