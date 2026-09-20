"""Mapping from recognized features to template-based operations.

Holes are handled automatically from the available drill/bore templates
(filtered by the selected cutter variant):
- A hole matching a drill template's tool diameter exactly is drilled with it.
- Through holes larger than BIG_HOLE_LIMIT are machined as inner contours.
- Other holes are bored with the smallest tool that leaves no standing core
  (tool diameter > hole diameter / 2) and is at least TOOL_CLEARANCE smaller
  than the hole; holes too big for that use the largest bore tool. Holes
  smaller than every tool are skipped with a warning.

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
an open chain by the 'dogbone' template's smaller cutter. Because such a corner
is machined separately, it places no demand on the template it came from and is
left out of that template's corner-radius check.

Tabs are opt-in per contour: the tab selection accepts edges or faces of an
outer contour or a cutout, resolved to the owning feature. A second selection
takes tabs away again and wins over both the mode and the tab selection.
"""

import os
import adsk.core, adsk.fusion
from dataclasses import dataclass, field
from . import holding, recognition, tabs, templates

# A hole this close to a drill template's tool diameter is drilled (cm).
DRILL_MATCH_TOL = 0.005
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
    # Single arcs machined as open chains (dogbone reliefs).
    open_chains: list = field(default_factory=list)
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
    bores = _variants_by_tool_diameter(registry['bore'], assignments.cutter, warnings)
    max_bore = max(bores.keys(), default=None)

    # Large through holes become inner contours instead of bores; large blind
    # holes (bigger than 2x the largest bore cutter, which would leave a
    # standing core) become circular pockets.
    small_holes: list[recognition.Hole] = []
    cutouts = list(result.cutouts)
    pockets = list(result.pockets)
    for hole in result.holes:
        if _drill_match(hole.diameter, drills):
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
    sets = _feature_sets(resolver, assignments, tab_policy, warnings)

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
                  tab_policy: TabPolicy, warnings: list[str]) -> _FeatureSets:
    tab_outer, tab_cutouts, _ = _resolve_features(resolver, tab_policy.selection, warnings, 'tab')
    no_tab = _resolve_features(resolver, tab_policy.skip_selection, warnings, 'skip-tab')
    finish = _resolve_features(resolver, assignments.finish_selection, warnings, 'finishing')
    skip = _resolve_features(resolver, assignments.skip_selection, warnings, 'skip')
    no_finish = _resolve_features(
        resolver, assignments.no_finish_selection, warnings, 'skip-finishing')
    return _FeatureSets(
        tab_outer=tab_outer, tab_cutouts=tab_cutouts,
        no_tab_outer=no_tab[0], no_tab_cutouts=no_tab[1],
        finish_outer=finish[0], finish_cutouts=finish[1], finish_pockets=finish[2],
        skip_outer=skip[0], skip_cutouts=skip[1], skip_pockets=skip[2],
        no_finish_outer=no_finish[0], no_finish_cutouts=no_finish[1],
        no_finish_pockets=no_finish[2])


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
        warnings.append('No drill/bore templates found; all holes skipped.')
        return []

    groups: dict[tuple[str, float, bool, float | None], Job] = {}
    for hole in holes:
        required_depth = hole.depth + (overcut if hole.is_through else 0.0)
        picked = _pick_hole_template(hole, required_depth, drills, bores, warnings)
        if not picked:
            warnings.append(
                f'{hole.body.name}: hole ⌀{hole.diameter * 10:.2f}mm has no matching '
                'drill/bore template; skipped.')
            continue
        variant, tool_dia = picked
        # A bore's feedrate follows the hole diameter, so each diameter needs
        # its own operation. A drill's hole is the size of its tool by
        # definition, so its tool diameter already says everything.
        feed_scale = (round(hole.diameter / tool_dia, FEED_SCALE_TOL)
                      if variant.kind == 'bore' and tool_dia else None)
        key = (variant.kind, tool_dia, hole.is_through, feed_scale)
        if key not in groups:
            kind_label = 'through' if hole.is_through else 'blind'
            size = f'⌀{hole.diameter * 10:.1f}mm, ' if feed_scale is not None else ''
            groups[key] = Job(
                variant=variant,
                display_name=f'{variant.kind.capitalize()} ({variant.display_label}, '
                             f'{size}{kind_label})',
                is_through=hole.is_through,
                feed_scale=feed_scale,
            )
        groups[key].holes.append(hole)
    order = lambda key: (0 if key[0] == 'drill' else 1, key[1], key[3] or 0.0, key[2])
    return [groups[key] for key in sorted(groups.keys(), key=order)]


def _pick_hole_template(hole, required_depth, drills, bores, warnings):
    diameter = hole.diameter

    def depth_ok(flute):
        return flute is None or flute >= required_depth - DEPTH_TOL

    for tool_dia, (variant, flute) in drills.items():
        if abs(diameter - tool_dia) < DRILL_MATCH_TOL:
            if depth_ok(flute):
                return variant, tool_dia
            bore_pick = _pick_bore(diameter, required_depth, bores, require_depth=True)
            if bore_pick:
                warnings.append(
                    f'{hole.body.name}: hole ⌀{diameter * 10:.2f}mm is deeper '
                    f'({required_depth * 10:.1f}mm) than the drill tool allows '
                    f'({flute * 10:.1f}mm); boring with "{bore_pick[0].display_label}" instead.')
                return bore_pick
            warnings.append(
                f'{hole.body.name}: hole ⌀{diameter * 10:.2f}mm depth '
                f'{required_depth * 10:.1f}mm exceeds the drill tool\'s maximum '
                f'({flute * 10:.1f}mm) and no bore tool can reach it; check the operation.')
            return variant, tool_dia

    bore_pick = _pick_bore(diameter, required_depth, bores, require_depth=True)
    if bore_pick:
        return bore_pick
    bore_pick = _pick_bore(diameter, required_depth, bores, require_depth=False)
    if bore_pick:
        variant, tool_dia = bore_pick
        flute = bores[tool_dia][1]
        warnings.append(
            f'{hole.body.name}: hole ⌀{diameter * 10:.2f}mm depth '
            f'{required_depth * 10:.1f}mm exceeds every bore tool\'s maximum '
            f'(using "{variant.display_label}", {flute * 10:.1f}mm); check the operation.')
        return bore_pick
    return None


def _pick_bore(diameter, required_depth, bores, require_depth):
    candidates = []
    for tool_dia, (variant, flute) in bores.items():
        if tool_dia > diameter - TOOL_CLEARANCE:
            continue
        if require_depth and flute is not None and flute < required_depth - DEPTH_TOL:
            continue
        candidates.append(tool_dia)
    if not candidates:
        return None
    # Smallest tool that leaves no standing core (tool > hole/2), otherwise the
    # largest tool (core is accepted / falls out on through holes).
    no_core = [t for t in candidates if 2 * t > diameter]
    tool_dia = min(no_core) if no_core else max(candidates)
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

    def full_thickness(loop, position: float, body) -> bool:
        """True if the part carries the full sheet thickness above this stretch
        of the contour (THICKNESS_MARGIN to each side along the loop).

        Where nothing was milled off the top, the boundary of the body's top
        face runs directly above the bottom contour; a pocket, rabbet or
        chamfer reaching the contour makes it detour inward. A tab under such
        thinned material can be taller than what is left above it.
        """
        token = body.entityToken
        if token not in top_outlines:
            top_outlines[token] = _top_face_outlines(body)
        outlines = top_outlines[token]
        if not outlines:
            return False
        for offset in (-THICKNESS_MARGIN, 0.0, THICKNESS_MARGIN):
            point = loop.point_at(position + offset)
            x = point.asVector().dotProduct(frame.x)
            y = point.asVector().dotProduct(frame.y)
            if not any(_near_outline(x, y, outline, FULL_THICKNESS_TOL)
                       for outline in outlines):
                return False
        return True

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
    """Operations with the smallest available dogbone cutter, machining each
    relief along its arc as an open chain.

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
    variant = min(candidates, key=lambda v: tool_limits(v).max_diameter or 0.0)
    limits = tool_limits(variant)

    smallest = min(relief.diameter for relief in reliefs)
    if limits.max_diameter is not None and limits.max_diameter > smallest - RELIEF_TOL:
        warnings.append(
            f'The smallest dogbone (⌀{smallest * 10:.2f}mm) is not wider than the '
            f'"{variant.display_label}" tool (⌀{limits.max_diameter * 10:.2f}mm), which '
            'leaves it nothing to cut; check the operation.')

    # A relief hangs from the top face, so equal depths sit at equal heights.
    levels: dict[tuple[float, bool], list[recognition.Relief]] = {}
    for relief in reliefs:
        levels.setdefault((round(relief.depth, 4), relief.is_through), []).append(relief)

    jobs: list[Job] = []
    for (depth, is_through), group in sorted(levels.items()):
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
