"""Vacuum holding analysis for tab planning.

Once its contour is cut, a piece lies on the vacuum bed held only by the
suction under its own footprint. Three quantities decide whether it stays put:

- Hold-down force: pressure times EFFECTIVE area. On a bleed-through MDF
  spoilboard air feeds in around every free edge, so a rim strip of the
  footprint holds next to nothing; the effective area is the footprint eroded
  inward by a leak margin. This is what makes a long narrow part weak despite
  a respectable nominal area.
- Sliding: friction * hold-down against the cutting force.
- Twisting: the cutter pushing at the contour point farthest from the pressure
  centroid applies the torque force * lever; distributed friction resists with
  friction * pressure * J, where J = integral |r - c| dA over the effective
  footprint. Long pieces have long levers but thin J - the leverage failure.

The sheet is analyzed as a whole: the stock is rasterized into a grid, every
machined band (each contour swept by its tool diameter) is removed, and the
remaining cells decompose into pieces - the parts, the waste inside cutouts,
loose offcuts, and the outer skeleton. Every piece is scored the same way;
nothing is anchored: the skeleton is just another piece lying on the bed, and
a narrow one erodes to nothing exactly like a narrow part does.

All lengths in cm, forces in N, pressure in N/cm^2. Pure geometry and
arithmetic - the Fusion-facing adapter at the bottom imports its dependencies
lazily, so the physics can be exercised and calibrated outside Fusion.
"""

import math
from collections import deque
from dataclasses import dataclass, field

# Cell labels (piece indices are >= 0).
_WASTE = -1
_CUT = -2

# Chamfer distance-transform weights (straight / diagonal step, in cells).
_CHAMFER_STRAIGHT = 1.0
_CHAMFER_DIAGONAL = 1.4

# Shear capacity of one tab (N). An 8 x 0.5mm plywood tab is good for roughly
# tab width * thickness * shear strength; calibratable like everything else.
TAB_STRENGTH = 50.0
# How far a tab can bridge across machined kerf to reach its anchor, in tool
# diameters - matches the builder's TAB_REACH_FACTOR, which guarantees every
# operation within that reach keeps the tab standing.
BRIDGE_FACTOR = 2.0


@dataclass(frozen=True)
class HoldingParams:
    """Calibration of the bed and the cut. pressure, friction and cutting_force
    only ever appear as the ratio friction*pressure/cutting_force, so the test
    cuts calibrate that lump plus leak_margin - absolute values of the three
    need not be known individually."""
    pressure: float = 0.5        # holding pressure under sealed footprint (N/cm^2)
    friction: float = 0.5        # piece against spoilboard
    cutting_force: float = 20.0  # lateral force at the cutter (N)
    safety: float = 1.5          # margins must beat the load by this factor
    leak_margin: float = 1.2     # rim width that holds nothing (cm)
    cell: float = 0.3            # grid resolution (cm)
    # How far the physical sheet extends beyond the stock box on each side.
    # The cutter never goes there, but the skeleton does - a sheet cut from
    # generous material is anchored by all that extra footprint.
    sheet_oversize: float = 0.0


@dataclass
class Footprint:
    """One part's bottom footprint in machining-frame XY."""
    name: str
    outer: list  # [(x, y), ...] closed polygon, implicit last->first edge
    cutouts: list = field(default_factory=list)  # list of polygons
    kerf: float = 0.6  # tool diameter of its contour operations


@dataclass
class Piece:
    """One piece of the fully cut sheet, with its holding verdict.

    Margins are ratios of holding over required (load times safety); a piece
    holds when both are >= 1. J and lever are reported for calibration work.
    """
    kind: str   # 'part' | 'cutout' | 'offcut' | 'skeleton'
    name: str
    area: float
    effective_area: float
    centroid: tuple | None  # of the effective footprint; None if it eroded away
    twist_j: float          # integral |r - c| dA (cm^3)
    lever: float            # farthest machined point from the centroid (cm)
    slide_margin: float
    twist_margin: float

    @property
    def holds(self) -> bool:
        return min(self.slide_margin, self.twist_margin) >= 1.0

    # Internals for assembly math and tab planning (not part of the report).
    index: int = -1          # position in Sheet.pieces
    hull: list = field(default_factory=list)  # convex hull of machined boundary


@dataclass
class Sheet:
    """The decomposed sheet: the pieces plus the grid they were cut from, so
    the tab planner can resolve anchors and merge footprints."""
    params: HoldingParams
    cell: float
    ox: float
    oy: float
    nx: int
    ny: int
    piece_at_cell: list   # cell -> piece index, or _CUT / _WASTE(none)
    pieces: list          # parts first (footprint order), then waste by size

    def piece_at(self, x: float, y: float):
        """Piece index under a point, or None over machined kerf / off-grid."""
        i, j = int((x - self.ox) / self.cell), int((y - self.oy) / self.cell)
        if not (0 <= i < self.nx and 0 <= j < self.ny):
            return None
        piece = self.piece_at_cell[j * self.nx + i]
        return piece if piece >= 0 else None

    def anchor_for(self, piece: int, x: float, y: float, limit: float):
        """The nearest piece other than `piece` within `limit` of a contour
        point: what a tab bridging the kerf there would connect to. Within
        bridge reach of a contour, the only things present are the piece
        itself, the cut band, and whatever lies across it."""
        best = None
        best_d2 = limit * limit
        r = int(limit / self.cell) + 1
        ci, cj = int((x - self.ox) / self.cell), int((y - self.oy) / self.cell)
        for dj in range(-r, r + 1):
            j = cj + dj
            if not 0 <= j < self.ny:
                continue
            for di in range(-r, r + 1):
                i = ci + di
                if not 0 <= i < self.nx:
                    continue
                other = self.piece_at_cell[j * self.nx + i]
                if other < 0 or other == piece:
                    continue
                px = self.ox + (i + 0.5) * self.cell - x
                py = self.oy + (j + 0.5) * self.cell - y
                d2 = px * px + py * py
                if d2 < best_d2:
                    best, best_d2 = other, d2
        return best


def analyze(footprints: list, params: HoldingParams,
            side_offset: float = 0.7) -> list:
    """Decompose the sheet and score every piece (see decompose)."""
    return decompose(footprints, params, side_offset).pieces if footprints else []


def decompose(footprints: list, params: HoldingParams,
              side_offset: float = 0.7) -> Sheet:
    """Rasterize the stock, remove the machined bands, and score the pieces.

    The stock rectangle is the parts' extent plus side_offset on each side,
    matching the relative box stock the builder configures. Pieces come parts
    first (in footprint order), then waste largest first.
    """
    xs = [x for fp in footprints for x, _ in fp.outer]
    ys = [y for fp in footprints for _, y in fp.outer]
    rim = side_offset + params.sheet_oversize
    ox, oy = min(xs) - rim, min(ys) - rim
    cell = params.cell
    nx = max(1, math.ceil((max(xs) + rim - ox) / cell))
    ny = max(1, math.ceil((max(ys) + rim - oy) / cell))

    label = [_WASTE] * (nx * ny)
    owner = [-1] * (nx * ny)  # part whose outer loop encloses the cell
    part_cells: list[list[int]] = [[] for _ in footprints]

    for index, fp in enumerate(footprints):
        for k in _polygon_cells(fp.outer, ox, oy, cell, nx, ny):
            label[k] = index
            owner[k] = index
        for hole in fp.cutouts:
            for k in _polygon_cells(hole, ox, oy, cell, nx, ny):
                if label[k] == index:
                    label[k] = _WASTE
    # The machined band: every contour swept by its tool diameter. Stamped
    # after all parts are filled so a band never eats a neighboring part
    # (parts nested closer than the tool would collide on the machine anyway).
    for fp in footprints:
        disc = _disc_offsets(fp.kerf / cell)
        for loop in [fp.outer] + fp.cutouts:
            for px, py in _walk(loop, cell * 0.5):
                ci, cj = int((px - ox) / cell), int((py - oy) / cell)
                for di, dj in disc:
                    i, j = ci + di, cj + dj
                    if 0 <= i < nx and 0 <= j < ny and label[j * nx + i] == _WASTE:
                        label[j * nx + i] = _CUT
    for k, lab in enumerate(label):
        if lab >= 0:
            part_cells[lab].append(k)

    pieces: list[Piece] = []
    for index, fp in enumerate(footprints):
        boundary = list(fp.outer) + [p for hole in fp.cutouts for p in hole]
        pieces.append(_score(
            'part', fp.name, part_cells[index], boundary, nx, ny, cell, ox, oy, params))

    waste_cells: list[list[int]] = []
    for cells, touches_border, inside in _waste_components(label, owner, nx, ny):
        if inside is not None:
            kind, name = 'cutout', f'{footprints[inside].name} cutout waste'
        else:
            kind, name = ('skeleton', '') if touches_border else ('offcut', '')
        machined = _machined_boundary(cells, label, nx, ny, cell, ox, oy)
        pieces.append(_score(kind, name, cells, machined, nx, ny, cell, ox, oy, params))
        waste_cells.append(cells)
    # Parts in input order, then waste pieces largest first; skeletons and
    # offcuts are numbered in that order so 'skeleton' is always the big one.
    order = sorted(range(len(waste_cells)), key=lambda w: -pieces[len(footprints) + w].area)
    waste = [pieces[len(footprints) + w] for w in order]
    counts = {'skeleton': 0, 'offcut': 0}
    for piece in waste:
        if piece.name == '':
            counts[piece.kind] += 1
            n = counts[piece.kind]
            piece.name = piece.kind if n == 1 else f'{piece.kind} {n}'
    pieces = pieces[:len(footprints)] + waste

    piece_at_cell = label[:]  # part labels already match their piece index
    for rank, w in enumerate(order):
        for k in waste_cells[w]:
            piece_at_cell[k] = len(footprints) + rank
    for index, piece in enumerate(pieces):
        piece.index = index
    return Sheet(params=params, cell=cell, ox=ox, oy=oy, nx=nx, ny=ny,
                 piece_at_cell=piece_at_cell, pieces=pieces)


# Waste fragments below this area are not worth a report line - typically the
# millimeter of stock rim the kerf leaves standing along the border (cm^2).
SLIVER_AREA = 2.0


def format_report(pieces: list) -> list[str]:
    """One line per piece for the report message box; slivers summarized."""
    lines = []
    slivers = 0
    for p in pieces:
        if p.kind != 'part' and p.area < SLIVER_AREA:
            slivers += 1
            continue
        if p.holds:
            verdict = 'holds'
        elif p.kind == 'part':
            verdict = 'NEEDS TABS'
        else:
            # Waste is allowed to shift once free; its margins only say what
            # it is worth as an anchor.
            verdict = 'loose waste (no anchor value)'
        worst = ('slide' if p.slide_margin <= p.twist_margin else 'twist')
        lines.append(
            f'{p.name}: {verdict} — area {p.area:.0f}→{p.effective_area:.0f}cm², '
            f'slide ×{p.slide_margin:.2f}, twist ×{p.twist_margin:.2f} (worst: {worst})')
    if slivers:
        lines.append(f'({slivers} waste sliver(s) under {SLIVER_AREA:.0f}cm² ignored)')
    return lines


# --- Tab planning -------------------------------------------------------------

@dataclass
class TabRequest:
    """Where tabs may go for one piece: candidate positions along its machined
    contours (each with an opaque key the caller uses to map a chosen position
    back to its loop), and the placement policy for it."""
    piece: int
    candidates: list           # [(x, y, key)]
    bridge: float              # widest machined span a tab can cross (cm)
    min_count: int = 0         # floor once the piece gets tabs at all
    min_separation: float = 0.0
    forced: bool = False       # tab it even when the physics says it holds

@dataclass
class PlannedTabs:
    piece: int
    chosen: list = field(default_factory=list)  # [(x, y, key, anchor piece)]
    margin_before: float = 0.0
    margin: float = 0.0
    holdable: bool = True

# Never place more than this many physics tabs on one piece; past that the
# model is asking for clamps, not tabs.
_MAX_TABS = 12


def plan_tabs(sheet: Sheet, requests: list) -> tuple:
    """Greedy physics-driven tab placement.

    Tabs merge pieces into assemblies (union-find): the load on an assembly is
    ONE cutter at its worst lever, while the holding pools over every member -
    so a raft of marginal pieces can pass where each fails alone. A piece that
    holds by itself gets no tabs (unless forced). Each added tab is the one
    that most improves the failing piece's worst margin, which prefers strong
    anchors and spread positions on its own; when nothing improves a still-
    failing piece, it is declared unholdable with a warning.

    Returns (plans, report_lines, warnings).
    """
    params = sheet.params
    hold = params.friction * params.pressure
    required = params.safety * params.cutting_force

    parent = list(range(len(sheet.pieces)))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def component(piece: int, extra: int | None = None) -> list:
        roots = {find(piece)}
        if extra is not None:
            roots.add(find(extra))
        return [i for i in range(len(sheet.pieces)) if find(i) in roots]

    def assembly_margin(members: list) -> float:
        """Pooled margins of a rigid assembly. Each member seals on its own
        (the kerf between them still leaks), so effective areas add. The
        combined J uses the conservative bound max(J_i, A_i*d_i - J_i) per
        member, exact for the piece at the centroid and a slight underestimate
        in between."""
        total = sum(sheet.pieces[i].effective_area for i in members)
        if total <= 0.0:
            return 0.0
        cx = sum(sheet.pieces[i].effective_area * sheet.pieces[i].centroid[0]
                 for i in members if sheet.pieces[i].centroid) / total
        cy = sum(sheet.pieces[i].effective_area * sheet.pieces[i].centroid[1]
                 for i in members if sheet.pieces[i].centroid) / total
        j_bound = 0.0
        lever = 0.0
        for i in members:
            piece = sheet.pieces[i]
            if piece.centroid:
                d = math.hypot(piece.centroid[0] - cx, piece.centroid[1] - cy)
                j_bound += max(piece.twist_j, piece.effective_area * d - piece.twist_j)
            lever = max(lever, _lever(piece.hull, (cx, cy)))
        slide = hold * total / required
        twist = hold * j_bound / (required * lever) if lever > 0 else math.inf
        return min(slide, twist)

    def joint_margin(piece: Piece, tabs: list) -> float:
        """Can the piece's connection carry its own deficit? Tabs add shear
        capacity against sliding; against twisting they act as a force couple,
        so one tab is a pin (zero moment capacity) and spread is what counts."""
        slide = (hold * piece.effective_area + len(tabs) * TAB_STRENGTH) / required
        spread = 0.0
        for a in range(len(tabs)):
            for b in range(a + 1, len(tabs)):
                spread = max(spread, math.hypot(tabs[a][0] - tabs[b][0],
                                                tabs[a][1] - tabs[b][1]))
        lever = piece.lever
        if piece.centroid is None:
            # Fully eroded piece: no pressure centroid to pivot about; measure
            # the lever across its machined outline instead.
            lever = max((math.hypot(p[0] - q[0], p[1] - q[1])
                         for p in piece.hull for q in piece.hull), default=0.0) / 2
        moment = hold * piece.twist_j + TAB_STRENGTH * spread
        twist = moment / (required * lever) if lever > 0 else math.inf
        return min(slide, twist)

    plans = {req.piece: PlannedTabs(piece=req.piece) for req in requests}
    anchored: dict[int, list] = {}
    for req in requests:
        entries = []
        for x, y, key in req.candidates:
            anchor = sheet.anchor_for(req.piece, x, y, req.bridge)
            if anchor is not None:
                entries.append((x, y, key, anchor))
        anchored[req.piece] = entries

    def clear_of_chosen(req: TabRequest, x: float, y: float) -> bool:
        return all(math.hypot(x - t[0], y - t[1]) >= req.min_separation
                   for t in plans[req.piece].chosen)

    def current_margin(req: TabRequest) -> float:
        piece = sheet.pieces[req.piece]
        alone = min(piece.slide_margin, piece.twist_margin)
        if alone >= 1.0 and not plans[req.piece].chosen:
            return alone
        return min(assembly_margin(component(req.piece)),
                   joint_margin(piece, plans[req.piece].chosen))

    for req in requests:
        plans[req.piece].margin_before = min(sheet.pieces[req.piece].slide_margin,
                                             sheet.pieces[req.piece].twist_margin)

    warnings: list[str] = []
    given_up: set[int] = set()
    while True:
        failing = [(current_margin(req), req.piece, req) for req in requests
                   if req.piece not in given_up and current_margin(req) < 1.0]
        if not failing:
            break
        _, _, req = min(failing, key=lambda f: (f[0], f[1]))
        plan = plans[req.piece]
        margin = current_margin(req)
        piece = sheet.pieces[req.piece]
        best = None
        best_key = None
        if len(plan.chosen) < _MAX_TABS:
            taken = {t[2] for t in plan.chosen}
            for x, y, key, anchor in anchored[req.piece]:
                if key in taken or not clear_of_chosen(req, x, y):
                    continue
                tentative = plan.chosen + [(x, y, key, anchor)]
                m = min(assembly_margin(component(req.piece, extra=anchor)),
                        joint_margin(piece, tentative))
                # Tie-breaks: spread (distance to the tabs already placed, or
                # to the centroid for the first one - an extremity now is what
                # gives the next tab its moment arm), then anchor strength.
                if plan.chosen:
                    aux = min(math.hypot(x - t[0], y - t[1]) for t in plan.chosen)
                elif piece.centroid:
                    aux = math.hypot(x - piece.centroid[0], y - piece.centroid[1])
                else:
                    aux = 0.0
                score = (m, aux, sheet.pieces[anchor].effective_area)
                if best_key is None or score > best_key:
                    best_key, best = score, (x, y, key, anchor)
        # A single tab is a pin: it cannot improve a twist deficit, only the
        # second one creates spread. Tabs up to the floor count are therefore
        # committed on the tie-breaks alone; beyond it, every further tab has
        # to actually raise the margin.
        improves = best is not None and best_key[0] > margin + 1e-9
        if best is None or (not improves
                            and len(plan.chosen) >= max(2, req.min_count)):
            given_up.add(req.piece)
            warnings.append(
                f'{piece.name}: cannot be held (×{margin:.2f} with '
                f'{len(plan.chosen)} tab(s)); clamp it, nest it closer to other '
                'parts, or increase the sheet oversize.')
            plan.holdable = False
            continue
        plan.chosen.append(best)
        parent[find(req.piece)] = find(best[3])

    # Floor: forced pieces and every tabbed piece get at least min_count tabs,
    # padded for maximum spread among the anchored candidates.
    for req in requests:
        plan = plans[req.piece]
        if not (req.forced or plan.chosen):
            continue
        taken = {t[2] for t in plan.chosen}
        while len(plan.chosen) < req.min_count:
            candidates = [(x, y, key, anchor) for x, y, key, anchor in anchored[req.piece]
                          if key not in taken and clear_of_chosen(req, x, y)]
            if not candidates:
                break
            if plan.chosen:
                pick = max(candidates, key=lambda c: min(
                    math.hypot(c[0] - t[0], c[1] - t[1]) for t in plan.chosen))
            else:
                pick = candidates[0]
            plan.chosen.append(pick)
            taken.add(pick[2])
            parent[find(req.piece)] = find(pick[3])

    lines: list[str] = []
    for req in requests:
        plan = plans[req.piece]
        plan.margin = current_margin(req)
        if not plan.chosen:
            continue
        anchors: dict[str, int] = {}
        for _, _, _, anchor in plan.chosen:
            name = sheet.pieces[anchor].name
            anchors[name] = anchors.get(name, 0) + 1
        into = ', '.join(f'{n}→{name}' for name, n in anchors.items())
        lines.append(
            f'{sheet.pieces[req.piece].name}: {len(plan.chosen)} tab(s) ({into}), '
            f'×{plan.margin_before:.2f} → ×{plan.margin:.2f}')
    return [plans[req.piece] for req in requests], lines, warnings


def _convex_hull(points: list) -> list:
    """Andrew monotone chain; collapses the machined boundary to the few
    points that can carry the maximum lever."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def half(iterable):
        chain = []
        for p in iterable:
            while len(chain) >= 2 and (
                    (chain[-1][0] - chain[-2][0]) * (p[1] - chain[-2][1])
                    - (chain[-1][1] - chain[-2][1]) * (p[0] - chain[-2][0])) <= 0:
                chain.pop()
            chain.append(p)
        return chain[:-1]

    return half(pts) + half(reversed(pts))


def _score(kind: str, name: str, cells: list, boundary_points: list,
           nx: int, ny: int, cell: float, ox: float, oy: float,
           params: HoldingParams) -> Piece:
    """Holding metrics of one piece from its grid cells.

    boundary_points are the machined points the cutter can push at (a part's
    own contours; for waste, its cells along the cut bands) - the lever of the
    twist check is the farthest of them from the pressure centroid.
    """
    area = len(cells) * cell * cell
    hull = _convex_hull(boundary_points)
    effective = _effective_cells(cells, nx, ny, cell, params.leak_margin)
    if not effective:
        return Piece(kind, name, area, 0.0, None, 0.0, _lever(boundary_points, None),
                     0.0, 0.0, hull=hull)
    inv = 1.0 / len(effective)
    cx = sum(ox + (k % nx + 0.5) * cell for k in effective) * inv
    cy = sum(oy + (k // nx + 0.5) * cell for k in effective) * inv
    twist_j = sum(
        math.hypot(ox + (k % nx + 0.5) * cell - cx, oy + (k // nx + 0.5) * cell - cy)
        for k in effective) * cell * cell
    lever = _lever(hull, (cx, cy))

    hold = params.friction * params.pressure
    required = params.safety * params.cutting_force
    slide = hold * len(effective) * cell * cell / required
    twist = (hold * twist_j / (required * lever)) if lever > 0 else float('inf')
    return Piece(kind, name, area, len(effective) * cell * cell, (cx, cy),
                 twist_j, lever, slide, twist, hull=hull)


def _lever(points: list, centroid) -> float:
    if not points or centroid is None:
        return 0.0
    cx, cy = centroid
    return max(math.hypot(x - cx, y - cy) for x, y in points)


def _effective_cells(cells: list, nx: int, ny: int, cell: float,
                     leak_margin: float) -> list:
    """The cells deeper than the leak margin inside the piece: a two-pass
    chamfer distance transform over the piece's bounding box, with everything
    outside the piece (including beyond the grid: the sheet edge leaks too) at
    distance zero."""
    if not cells:
        return []
    is_ = [k % nx for k in cells]
    js = [k // nx for k in cells]
    bx0, by0 = min(is_), min(js)
    bw, bh = max(is_) - bx0 + 1, max(js) - by0 + 1
    dist = [0.0] * (bw * bh)
    for k in cells:
        dist[(k // nx - by0) * bw + (k % nx - bx0)] = math.inf

    for j in range(bh):
        base = j * bw
        for i in range(bw):
            k = base + i
            d = dist[k]
            if d == 0.0:
                continue
            d = min(d, (dist[k - 1] if i > 0 else 0.0) + _CHAMFER_STRAIGHT)
            if j > 0:
                d = min(d, dist[k - bw] + _CHAMFER_STRAIGHT)
                d = min(d, (dist[k - bw - 1] if i > 0 else 0.0) + _CHAMFER_DIAGONAL)
                d = min(d, (dist[k - bw + 1] if i < bw - 1 else 0.0) + _CHAMFER_DIAGONAL)
            else:
                d = min(d, _CHAMFER_STRAIGHT)
            dist[k] = d
    for j in range(bh - 1, -1, -1):
        base = j * bw
        for i in range(bw - 1, -1, -1):
            k = base + i
            d = dist[k]
            if d == 0.0:
                continue
            d = min(d, (dist[k + 1] if i < bw - 1 else 0.0) + _CHAMFER_STRAIGHT)
            if j < bh - 1:
                d = min(d, dist[k + bw] + _CHAMFER_STRAIGHT)
                d = min(d, (dist[k + bw - 1] if i > 0 else 0.0) + _CHAMFER_DIAGONAL)
                d = min(d, (dist[k + bw + 1] if i < bw - 1 else 0.0) + _CHAMFER_DIAGONAL)
            else:
                d = min(d, _CHAMFER_STRAIGHT)
            dist[k] = d

    # Cell centers sit half a cell in from the piece edge already.
    threshold = leak_margin / cell + 0.5
    return [k for k in cells
            if dist[(k // nx - by0) * bw + (k % nx - bx0)] >= threshold]


def _waste_components(label: list, owner: list, nx: int, ny: int):
    """Connected components of the un-machined waste: (cells, touches the
    stock border, enclosing part index or None). A component inside a part's
    outer loop is that part's cutout waste."""
    seen = [False] * len(label)
    for start, lab in enumerate(label):
        if lab != _WASTE or seen[start]:
            continue
        cells, queue = [], deque([start])
        seen[start] = True
        touches = False
        while queue:
            k = queue.popleft()
            cells.append(k)
            i, j = k % nx, k // nx
            if i == 0 or i == nx - 1 or j == 0 or j == ny - 1:
                touches = True
            for n in _neighbors(k, i, j, nx, ny):
                if not seen[n] and label[n] == _WASTE:
                    seen[n] = True
                    queue.append(n)
        inside = owner[cells[0]]
        yield cells, touches, (inside if inside >= 0 else None)


def _neighbors(k: int, i: int, j: int, nx: int, ny: int):
    if i > 0:
        yield k - 1
    if i < nx - 1:
        yield k + 1
    if j > 0:
        yield k - nx
    if j < ny - 1:
        yield k + nx


def _machined_boundary(cells: list, label: list, nx: int, ny: int,
                       cell: float, ox: float, oy: float) -> list:
    """Centers of the piece's cells that border a cut band - where the cutter
    actually pushes on this piece."""
    points = []
    for k in cells:
        i, j = k % nx, k // nx
        if any(label[n] == _CUT for n in _neighbors(k, i, j, nx, ny)):
            points.append((ox + (i + 0.5) * cell, oy + (j + 0.5) * cell))
    return points


def _polygon_cells(poly: list, ox: float, oy: float, cell: float,
                   nx: int, ny: int):
    """Grid indices whose cell center lies inside the polygon (even-odd,
    scanline per row)."""
    if len(poly) < 3:
        return
    poly_ys = [p[1] for p in poly]
    j0 = max(0, int((min(poly_ys) - oy) / cell) - 1)
    j1 = min(ny - 1, int((max(poly_ys) - oy) / cell) + 1)
    count = len(poly)
    for j in range(j0, j1 + 1):
        y = oy + (j + 0.5) * cell
        crossings = []
        for a in range(count):
            x1, y1 = poly[a]
            x2, y2 = poly[(a + 1) % count]
            if (y1 > y) != (y2 > y):
                crossings.append(x1 + (y - y1) / (y2 - y1) * (x2 - x1))
        crossings.sort()
        for a in range(0, len(crossings) - 1, 2):
            i0 = max(0, math.ceil((crossings[a] - ox) / cell - 0.5))
            i1 = min(nx - 1, math.floor((crossings[a + 1] - ox) / cell - 0.5))
            for i in range(i0, i1 + 1):
                yield j * nx + i


def _walk(poly: list, step: float):
    """Points along the polygon boundary, at most `step` apart."""
    count = len(poly)
    for a in range(count):
        x1, y1 = poly[a]
        x2, y2 = poly[(a + 1) % count]
        samples = max(1, int(math.hypot(x2 - x1, y2 - y1) / step))
        for t in range(samples):
            f = t / samples
            yield x1 + (x2 - x1) * f, y1 + (y2 - y1) * f


_disc_cache: dict[int, list] = {}


def _disc_offsets(radius_cells: float) -> list:
    key = int(radius_cells * 8)
    if key not in _disc_cache:
        limit = int(radius_cells) + 1
        r2 = radius_cells * radius_cells
        _disc_cache[key] = [(di, dj)
                            for dj in range(-limit, limit + 1)
                            for di in range(-limit, limit + 1)
                            if di * di + dj * dj <= r2]
    return _disc_cache[key]


# --- Fusion adapter -----------------------------------------------------------

@dataclass
class SetupSheet:
    """The decomposition of a recognition result, with the maps back into it:
    part pieces by body entityToken, cutout waste pieces by index into
    result.cutouts (missing when the waste was milled away entirely)."""
    sheet: Sheet
    part_pieces: dict     # body entityToken -> piece index
    cutout_pieces: dict   # index into result.cutouts -> piece index
    notes: list


def decompose_setup(result, frame, params: HoldingParams,
                    kerfs: dict | None = None, side_offset: float = 0.7,
                    cutouts_override: list | None = None) -> SetupSheet:
    """Sample every contour and cutout loop into a frame-XY polygon and
    decompose the sheet. kerfs maps a body entityToken to the tool diameter of
    its contour operations (default 0.6cm). cutouts_override replaces
    result.cutouts - the planner passes its extended list, where big through
    holes have become circular cutouts."""
    from . import tabs  # deferred: keeps this module importable outside Fusion

    def project(edges):
        return [(p.asVector().dotProduct(frame.x), p.asVector().dotProduct(frame.y))
                for p in tabs.loop_outline(edges).points]

    notes: list[str] = []
    footprints: list[Footprint] = []
    part_pieces: dict = {}
    cutout_polys: list = []
    for contour in result.contours:
        if not contour.edges:
            notes.append(f'{contour.body.name}: no planar bottom face; '
                         'left out of the holding analysis.')
            continue
        token = contour.body.entityToken
        part_pieces[token] = len(footprints)
        footprints.append(Footprint(
            name=contour.body.name, outer=project(contour.edges),
            kerf=(kerfs or {}).get(token, 0.6)))
    cutout_list = result.cutouts if cutouts_override is None else cutouts_override
    for index, cutout in enumerate(cutout_list):
        piece = part_pieces.get(cutout.body.entityToken)
        if piece is None:
            continue
        poly = project(cutout.edges)
        footprints[piece].cutouts.append(poly)
        cutout_polys.append((index, poly))
    if not footprints:
        raise ValueError('No footprints to analyze.')
    sheet = decompose(footprints, params, side_offset)

    cutout_pieces: dict = {}
    for index, poly in cutout_polys:
        for k in _polygon_cells(poly, sheet.ox, sheet.oy, sheet.cell,
                                sheet.nx, sheet.ny):
            piece = sheet.piece_at_cell[k]
            if piece >= 0 and sheet.pieces[piece].kind == 'cutout':
                cutout_pieces[index] = piece
                break
    return SetupSheet(sheet=sheet, part_pieces=part_pieces,
                      cutout_pieces=cutout_pieces, notes=notes)


def analyze_setup(result, frame, params: HoldingParams,
                  kerf: float = 0.6, side_offset: float = 0.7) -> tuple:
    """Score a recognition result; returns (pieces, notes)."""
    try:
        setup = decompose_setup(result, frame, params, side_offset=side_offset)
    except ValueError:
        return [], ['No footprints to analyze.']
    return setup.sheet.pieces, setup.notes
