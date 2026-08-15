"""Mapping from recognized features to template-based operations.

Holes are handled automatically from the available drill/bore templates
(filtered by the selected cutter variant):
- A hole matching a drill template's tool diameter exactly is drilled with it.
- Through holes larger than BIG_HOLE_LIMIT are machined as inner contours.
- Other holes are bored with the smallest tool that leaves no standing core
  (tool diameter > hole diameter / 2) and is at least TOOL_CLEARANCE smaller
  than the hole; holes too big for that use the largest bore tool. Holes
  smaller than every tool are skipped with a warning.

Pockets and contours are chosen by label in the UI; the selected cutter
variant (dc / udc) picks the concrete template file (untagged templates are
valid for any cutter). Finishing: a global mode (none / outer contours / all
contours) plus an additive selection of individual contours or pockets that
get the '.finish' template variant regardless of the mode. Two subtractive
selections override those defaults: features that are not machined at all, and
features that keep their operation but lose the finishing pass. Pocket templates
are validated against the pocket's minimum concave corner radius using the
widest tool in the template (which must be TOOL_CLEARANCE smaller than the
corner it has to reach into); on a misfit the best fitting variant is
substituted with a warning.

A contour tool wider than an inside corner relief (a dogbone) of the profile
cannot machine it. Those reliefs are collected across all contours and cutouts
and get extra operations after the contour operations: a relief matching a
drill template's tool diameter exactly is plunged with it (a contour pass would
degenerate to a point), every other one is machined along its arc as an open
chain by the 'dogbone' template's smaller cutter.

Tabs are opt-in per contour: the tab selection accepts edges or faces of an
outer contour or a cutout, resolved to the owning feature.
"""

import os
import adsk.core, adsk.fusion
from dataclasses import dataclass, field
from . import recognition, templates

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
# Extra depth required for through cuts (breakthrough below the stock, cm).
THROUGH_ALLOWANCE = 0.02
# A tool of exactly a relief's diameter machines it (that is what dogbones are
# drawn for), so only reliefs narrower than the tool by more than this need an
# extra operation (cm).
RELIEF_TOL = 0.005

TAB_NONE = 0
TAB_OUTER = 1
TAB_INNER = 2
TAB_ALL = 3

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
    # Single arcs machined as open chains (dogbone reliefs).
    open_chains: list = field(default_factory=list)
    tabbed: bool = False
    # Edge loops to place tabs on, with a label for warnings.
    tab_loops: list[tuple[list, str]] = field(default_factory=list)


@dataclass
class TabPolicy:
    """Tab placement policy from the command UI: a global mode plus an additive
    selection of individual contours (edges/faces of outer contours or cutouts).

    The tab count per contour follows from the contour length with degressive
    density (see tabs.tab_count); min_count is the floor."""
    mode: int = TAB_NONE
    selection: list = field(default_factory=list)  # entities (additive)
    min_count: int = 4


@dataclass
class Assignments:
    """Feature-to-variant choices coming from the command UI."""
    cutter: str | None = None            # 'dc' | 'udc' | None
    pocket_default: str | None = None    # label
    contour_default: str | None = None   # label
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
         assignments: Assignments, tab_policy: TabPolicy | None = None) -> tuple[list[Job], list[str]]:
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
                    min_corner_radius=hole.diameter / 2,
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
    jobs: list[Job] = []
    jobs += _plan_holes(small_holes, drills, bores, warnings)
    jobs += _plan_pockets(pockets, registry, assignments, sets, tool_limits, warnings)
    jobs += _plan_contours(result, cutouts, registry, assignments, tab_policy.mode, sets,
                           outer_overrides, cutout_overrides, drills, tool_limits, warnings)
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
    finish = _resolve_features(resolver, assignments.finish_selection, warnings, 'finishing')
    skip = _resolve_features(resolver, assignments.skip_selection, warnings, 'skip')
    no_finish = _resolve_features(
        resolver, assignments.no_finish_selection, warnings, 'skip-finishing')
    return _FeatureSets(
        tab_outer=tab_outer, tab_cutouts=tab_cutouts,
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


def _plan_holes(holes, drills, bores, warnings: list[str]) -> list[Job]:
    if not holes:
        return []
    if not drills and not bores:
        warnings.append('No drill/bore templates found; all holes skipped.')
        return []

    groups: dict[tuple[str, float, bool], Job] = {}
    for hole in holes:
        required_depth = hole.depth + (THROUGH_ALLOWANCE if hole.is_through else 0.0)
        picked = _pick_hole_template(hole, required_depth, drills, bores, warnings)
        if not picked:
            warnings.append(
                f'{hole.body.name}: hole ⌀{hole.diameter * 10:.2f}mm has no matching '
                'drill/bore template; skipped.')
            continue
        variant, tool_dia = picked
        key = (variant.kind, tool_dia, hole.is_through)
        if key not in groups:
            kind_label = 'through' if hole.is_through else 'blind'
            groups[key] = Job(
                variant=variant,
                display_name=f'{variant.kind.capitalize()} ({variant.display_label}, {kind_label})',
                is_through=hole.is_through,
            )
        groups[key].holes.append(hole)
    order = lambda key: (0 if key[0] == 'drill' else 1, key[1], key[2])
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
                  tool_limits, warnings: list[str]) -> list[Job]:
    if not pockets:
        return []

    def fits_radius(variant: templates.TemplateVariant, pocket: recognition.Pocket) -> bool:
        if pocket.min_corner_radius is None:
            return True
        diameter = tool_limits(variant).max_diameter
        # The tool has to fit into the corner with room to cut: its diameter
        # must stay below the corner's diameter by at least TOOL_CLEARANCE.
        return diameter is None or diameter <= 2 * pocket.min_corner_radius - TOOL_CLEARANCE

    def fits_depth(variant: templates.TemplateVariant, pocket: recognition.Pocket) -> bool:
        flute = tool_limits(variant).min_flute
        return flute is None or flute >= pocket.depth - DEPTH_TOL

    def fits(variant, pocket):
        return fits_radius(variant, pocket) and fits_depth(variant, pocket)

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
            problems.append(f'corner radius {pocket.min_corner_radius * 10:.1f}mm')
        if not fits_depth(variant, pocket):
            problems.append(f'depth {pocket.depth * 10:.1f}mm')
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
        if variant.name not in groups:
            groups[variant.name] = Job(
                variant=variant, display_name=f'Pockets ({variant.display_label})')
        groups[variant.name].pockets.append(pocket)
    return list(groups.values())


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
                         context: str, warnings: list[str]) -> templates.TemplateVariant:
    """Ensure the contour template's tool can cut through the stock; substitute
    a depth-capable variant (same finish flag) or warn."""
    required = feature_depth + THROUGH_ALLOWANCE
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


def _plan_contours(result, cutouts, registry, assignments: Assignments, tab_mode: int,
                   sets: _FeatureSets,
                   outer_overrides: dict[str, str], cutout_overrides: dict[int, str],
                   drills, tool_limits, warnings: list[str]) -> list[Job]:
    if not cutouts and not result.contours:
        return []
    if assignments.contour_default is None and not outer_overrides and not cutout_overrides:
        warnings.append('No contour template available; cutouts and contours skipped.')
        return []

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
            f'{cutout.body.name} cutout', warnings)
        reliefs += _reliefs(variant, cutout.edges, cutout.depth, tool_limits)
        tabbed = tab_mode in (TAB_INNER, TAB_ALL) or index in sets.tab_cutouts
        key = (variant.name, tabbed)
        if key not in cutout_groups:
            suffix = ', tabs' if tabbed else ''
            cutout_groups[key] = Job(
                variant=variant, display_name=f'Cutouts ({variant.display_label}{suffix})',
                tabbed=tabbed)
        cutout_groups[key].cutouts.append(cutout)
        if tabbed:
            cutout_groups[key].tab_loops.append((cutout.edges, f'{cutout.body.name} cutout'))

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
            f'{contour.body.name} outer contour', warnings)
        reliefs += _reliefs(variant, contour.edges, contour.depth, tool_limits)
        tabbed = tab_mode in (TAB_OUTER, TAB_ALL) or body_token in sets.tab_outer
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
            contour_groups[key].tab_loops.append((contour.edges, f'{contour.body.name} outer contour'))

    return (list(cutout_groups.values()) + list(contour_groups.values())
            + _plan_reliefs(reliefs, registry, drills, assignments.cutter, tool_limits, warnings))


def _reliefs(variant: templates.TemplateVariant, edges, depth: float,
             tool_limits) -> list[recognition.Relief]:
    """Inside corner reliefs of one contour that its own tool is too wide for.

    The narrowest tool of the template decides: it is the one that reaches
    furthest into the corners."""
    diameter = tool_limits(variant).min_diameter
    if diameter is None:
        return []
    return recognition.corner_reliefs(edges, diameter - RELIEF_TOL, depth)


def _plan_reliefs(reliefs: list[recognition.Relief], registry, drills, cutter: str | None,
                  tool_limits, warnings: list[str]) -> list[Job]:
    """Extra operations for the reliefs the contour operations left behind:
    plunged with an exactly fitting drill where one exists, milled along the arc
    with the dogbone template otherwise."""
    if not reliefs:
        return []

    drill_groups: dict[str, Job] = {}
    milled: list[recognition.Relief] = []
    for relief in reliefs:
        variant = _drill_for_relief(relief, drills)
        if not variant:
            milled.append(relief)
            continue
        if variant.name not in drill_groups:
            drill_groups[variant.name] = Job(
                variant=variant,
                display_name=f'Dogbones ({variant.display_label})',
                is_through=True,
            )
        # A relief is a partial hole: the drill strategy takes its wall face.
        drill_groups[variant.name].holes.append(recognition.Hole(
            face=relief.face, diameter=relief.diameter, depth=relief.depth,
            is_through=True, body=relief.face.body))

    for job in drill_groups.values():
        flute = tool_limits(job.variant).min_flute
        required = max(hole.depth for hole in job.holes) + THROUGH_ALLOWANCE
        if flute is not None and flute < required - DEPTH_TOL:
            warnings.append(
                f'Dogbone cut depth {required * 10:.1f}mm exceeds the '
                f'"{job.variant.display_label}" tool ({flute * 10:.1f}mm); check the operation.')

    return list(drill_groups.values()) + _plan_milled_reliefs(
        milled, registry, cutter, tool_limits, warnings)


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
                         tool_limits, warnings: list[str]) -> list[Job]:
    """One operation with the smallest available dogbone cutter, machining each
    relief along its arc as an open chain."""
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
    required = max(relief.depth for relief in reliefs) + THROUGH_ALLOWANCE
    if limits.min_flute is not None and limits.min_flute < required - DEPTH_TOL:
        warnings.append(
            f'Dogbone cut depth {required * 10:.1f}mm exceeds the "{variant.display_label}" '
            f'tool ({limits.min_flute * 10:.1f}mm); check the operation.')

    return [Job(
        variant=variant,
        display_name=f'Dogbones ({variant.display_label})',
        open_chains=[relief.edge for relief in reliefs],
    )]


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
