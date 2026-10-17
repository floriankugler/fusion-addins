// The nest view's CAM layer without the DOM, so that `node --test
// lang/preview/viewer/tests/` can check it: what the page lists of a nest's
// CAM plan (cam.json, lang/cam/plan_types.py) and what it draws of it on
// the nest's drawing (nest.svg, lang/nesting/draw.py).
//
// A setup is a blank; its frame is the blank's (x along its length, y
// across, from its corner), and the drawing puts a blank at its `rect` on
// its sheet, a sheet with y down. What is drawn is given as SVG elements
// ({tag, attrs, text}) in the drawing's coordinates, millimetres.

// The plan file version this page draws (lang/cam/plan_types.py CAM_VERSION).
export const CAM_VERSION = 1;

/** Why the page cannot draw `plan`, or null when it can. */
export function planVersionProblem(plan) {
  const version = plan?.version;
  if (version === CAM_VERSION) return null;
  return `plan version ${version ?? 'missing'}, this viewer reads ${CAM_VERSION}`;
}

/** When a file was written (ISO 8601) as the panel says it: `2026-10-17 11:31:04`. */
export function when(iso) {
  return (iso ?? '').replace('T', ' ').replace(/[+-]\d\d:\d\d$|Z$/, '');
}

/** A nest's plan as the side panel says it (the `plan` of a nest's entry in status.json). */
export function planStatusText(plan) {
  switch (plan?.state) {
    case 'ok': return `planned ${when(plan.written)}, for this nest`;
    case 'stale': return `stale: ${plan.why}: plan again`;
    case 'running': return 'planning…';
    case 'failed': return 'the plan failed:\n' + (plan.log ?? '').trim();
    default: return 'not planned yet: plan again, or python -m lang.cam';
  }
}

// -- tools -----------------------------------------------------------------

const PALETTE = ['#d1495b', '#2e86ab', '#3c9d4e', '#8e5ec5', '#e08a1e', '#1b998b', '#b5446e', '#6b7a8f'];

/** The tool an operation cuts with, as the legend names it: `6 mm`, `3.175 mm`, `V-bit 90°`. */
export function toolName(op) {
  const { type, diameter, taper } = op.tool;
  if (type === 'chamfer mill' || taper) return `V-bit ${round(2 * (taper ?? 45))}°`;
  return type === 'flat end mill' ? `${round(diameter)} mm` : `${type} ${round(diameter)} mm`;
}

/** Each tool of the plan (by `toolName`) and its colour: the widest first, the V-bits last. */
export function toolColors(plan) {
  const tools = new Map();
  for (const setup of plan?.setups ?? []) {
    for (const op of setup.operations) {
      const vbit = op.tool.type === 'chamfer mill' || !!op.tool.taper;
      tools.set(toolName(op), vbit ? -1 : op.tool.diameter);
    }
  }
  const order = [...tools].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  return new Map(order.map(([name], k) => [name, PALETTE[k % PALETTE.length]]));
}

// -- the legend --------------------------------------------------------------

/** The setup's name without its nest's: `birch 15 1.1`. */
export function setupLabel(plan, setup) {
  const head = `${plan?.nest ?? ''} `;
  return setup.name.startsWith(head) ? setup.name.slice(head.length) : setup.name;
}

/** The legend: per setup, in the plan's order, its operations in the order they run, each with its tool
 * and colour, how many features it machines and how many tabs it leaves. */
export function legend(plan) {
  const colors = toolColors(plan);
  return (plan?.setups ?? []).map((setup) => ({
    setup: setup.name,
    label: setupLabel(plan, setup),
    parts: setup.parts.length,
    operations: setup.operations.map((op, index) => ({
      index, name: op.name, kind: op.kind, tool: toolName(op), color: colors.get(toolName(op)),
      features: op.features.length, tabs: op.params.tabs?.positions.length ?? 0,
    })),
  }));
}

/** The operation chosen, as the page keeps it: {setup, index}, the index an operation's in the setup or
 * 'all' for every one of it; the choice when the plan has it, else null. */
export function chosenOperation(plan, wanted) {
  if (!wanted) return null;
  const setup = plan?.setups?.find((s) => s.name === wanted.setup);
  if (!setup) return null;
  if (wanted.index === 'all') return { setup: setup.name, index: 'all' };
  return Number.isInteger(wanted.index) && wanted.index >= 0 && wanted.index < setup.operations.length
    ? { setup: setup.name, index: wanted.index } : null;
}

/** The operations of a setup a choice highlights, by index. */
export function highlighted(setup, choice) {
  if (!choice || choice.setup !== setup.name) return [];
  return choice.index === 'all' ? setup.operations.map((_op, k) => k) : [choice.index];
}

// -- parts and their release -------------------------------------------------

/** Each part's place in the release order, from 1: the order its outer contour is cut free (smallest
 * hold first, the widest cutter's releases before a narrower one's). A part with no release (an own
 * blank's) has none. */
export function releaseRanks(setup) {
  const ranks = new Map();
  for (const r of setup.release_order ?? []) {
    if (r.what === 'outer' && !ranks.has(r.part)) ranks.set(r.part, ranks.size + 1);
  }
  return ranks;
}

/** The setup's parts in their release order, those with none last: {path, rank, hold, tabs, policy}. */
export function releaseList(setup) {
  const ranks = releaseRanks(setup);
  return setup.parts.map((p) => ({ path: p.path, rank: ranks.get(p.path) ?? null, hold: p.hold, tabs: p.tabs,
    policy: p.tab_policy }))
    .sort((a, b) => (a.rank ?? Infinity) - (b.rank ?? Infinity));
}

/** A hold as the page writes it: cm², a decimal under 100. */
export function holdText(hold) {
  return `${hold < 100 ? hold.toFixed(1) : Math.round(hold)} cm²`;
}

/** A part's line in its tooltip and the selection's info. */
export function partText(part, of) {
  const tabs = `${part.tabs} tab${part.tabs === 1 ? '' : 's'}`;
  const release = part.rank === null ? 'no release (its own blank)' : `released ${part.rank} of ${of}`;
  return `${release}: hold ${holdText(part.hold)}, ${tabs} (cam.tabs ${part.policy})`;
}

/** Each released part's colour by its rank: light the first, dark the last. */
export function releaseColors(setup) {
  const ranks = releaseRanks(setup);
  const n = ranks.size;
  return new Map([...ranks].map(([path, rank]) => [path, ramp(n > 1 ? (rank - 1) / (n - 1) : 0)]));
}

// From a pale to a deep blue, the parts' own hue, light enough for their names.
const RAMP = [[214, 233, 248], [124, 172, 222], [62, 116, 186]];

function ramp(t) {
  const x = Math.min(1, Math.max(0, t)) * (RAMP.length - 1);
  const k = Math.min(RAMP.length - 2, Math.floor(x));
  const f = x - k;
  const c = RAMP[k].map((v, i) => Math.round(v + (RAMP[k + 1][i] - v) * f));
  return `rgb(${c.join(', ')})`;
}

// -- what is drawn -----------------------------------------------------------

/** A feature's geometry in its setup's frame: `region` (rings, a pocket's piece or a rest), `outline`
 * (points, closed or open: a contour, a dog bone's wall, a chamfer's edge, a V-groove) and `circle`
 * (centre and radius: a hole, a dog bone). */
export function featureShapes(feature) {
  switch (feature.what) {
    case 'outer': case 'inner': return [{ shape: 'outline', points: feature.ring, closed: true }];
    case 'pocket': case 'rest': return [{ shape: 'region', rings: feature.rings, rest: feature.what === 'rest' }];
    case 'hole': return [{ shape: 'circle', center: feature.center, r: feature.d / 2 }];
    case 'dogbone': return [{ shape: 'circle', center: feature.center, r: feature.d / 2 },
      ...(feature.arc.length > 1 ? [{ shape: 'outline', points: feature.arc, closed: false }] : [])];
    case 'chamfer': return feature.paths.length
      ? feature.paths.map((p) => ({ shape: 'outline', points: p.points, closed: p.closed }))
      : feature.hole ? [{ shape: 'circle', center: feature.hole.center, r: feature.hole.d / 2 }] : [];
    case 'vgroove': return [{ shape: 'outline', points: [feature.start, feature.end], closed: false }];
    default: return [];
  }
}

/** Maps a point of a setup's frame onto the drawing: the blank at `rect` ([x, y, w, h]) on its sheet,
 * the sheet drawn at `sheet` ({x, y, height}: its rect in the drawing, y down). */
export function toDrawing(sheet, rect) {
  return ([x, y]) => [sheet.x + rect[0] + x, sheet.y + sheet.height - (rect[1] + y)];
}

/** The tab positions of a setup, once each (a roughing and its release leave the same), in its frame. */
export function tabPositions(setup) {
  const seen = new Map();
  for (const op of setup.operations) {
    for (const p of op.params.tabs?.positions ?? []) {
      const key = `${p[0].toFixed(3)} ${p[1].toFixed(3)}`;
      if (!seen.has(key)) seen.set(key, p);
    }
  }
  return [...seen.values()];
}

/** What the CAM layer draws on one setup's blank, in the drawing's coordinates: the highlighted
 * operations' features in their tools' colours, the tabs as marks on the contours, and by each part's
 * name (`labels`: per path {x, y, size}, where the drawing writes it) its place in the release order, its
 * hold and its tabs. `chosen`: the choice (`chosenOperation`). */
export function setupOverlay(setup, { sheet, chosen = null, colors = new Map(), labels = {} }) {
  const at = toDrawing(sheet, setup.stock.rect);
  const out = [];
  for (const k of highlighted(setup, chosen)) {
    const op = setup.operations[k];
    const color = colors.get(toolName(op)) ?? PALETTE[0];
    for (const feature of op.features) {
      for (const s of featureShapes(feature)) out.push(...shapeElements(s, feature.what, color, at));
    }
  }
  for (const p of tabPositions(setup)) {
    const [cx, cy] = at(p);
    out.push({ tag: 'circle', attrs: { class: 'cam-tab', cx: fix(cx), cy: fix(cy), r: 7 } });
  }
  const ranks = releaseRanks(setup);
  for (const part of setup.parts) {
    const label = labels[part.path];
    if (!label) continue;
    const rank = ranks.get(part.path);
    const text = (rank ? `${rank}. ` : '') + holdText(part.hold) + (part.tabs ? `, ${part.tabs} tabs` : '');
    out.push({ tag: 'text', attrs: { class: 'cam-release', x: fix(label.x), y: fix(label.y - 1.15 * label.size),
      'font-size': fix(Math.max(10, 0.7 * label.size)), 'text-anchor': 'middle', 'dominant-baseline': 'middle',
      'data-path': part.path }, text });
  }
  return out;
}

function shapeElements(s, what, color, at) {
  const cls = `cam-feature cam-${what}`;
  if (s.shape === 'region') {
    return [{ tag: 'path', attrs: { class: cls + (s.rest ? ' rest' : ''), d: s.rings.map((r) => pathOf(r, true, at)).join(' '),
      fill: color, stroke: color } }];
  }
  if (s.shape === 'outline') {
    return [{ tag: 'path', attrs: { class: cls, d: pathOf(s.points, s.closed, at), fill: 'none', stroke: color } }];
  }
  const [cx, cy] = at(s.center);
  return [{ tag: 'circle', attrs: { class: cls, cx: fix(cx), cy: fix(cy), r: fix(s.r), fill: color, stroke: 'none' } },
    // a ring around it, as a hole of a few millimetres is a dot at the scale of a sheet
    { tag: 'circle', attrs: { class: cls + ' halo', cx: fix(cx), cy: fix(cy), r: fix(Math.max(s.r + 3, 6)),
      fill: 'none', stroke: color } }];
}

function pathOf(points, closed, at) {
  return 'M ' + points.map((p) => at(p).map(fix).join(' ')).join(' L ') + (closed ? ' Z' : '');
}

const fix = (v) => Math.round(v * 100) / 100;
const round = (v) => Math.round(v * 1000) / 1000;

// -- what is listed ----------------------------------------------------------

/** The plan's text beside the drawing: per setup what it leaves out (an operation a line, with its
 * chamfer and dog bones; what is in a narrow face is taken care of and not listed) and its problems, then
 * the plan's own problems that no setup has (its check's). */
export function planNotes(plan) {
  const lines = [];
  const listed = new Set();
  for (const setup of plan?.setups ?? []) {
    const own = [];
    const groups = new Map();
    for (const left of setup.left_out) {
      if (left.why === 'narrow face') continue;
      const key = `${left.part}\n${left.op.index}\n${left.why}`;
      if (!groups.has(key)) groups.set(key, { left, aspects: [], note: '' });
      const g = groups.get(key);
      g.aspects.push(left.op.aspect);
      if (left.note && !g.note) g.note = left.note;
    }
    for (const { left, aspects, note } of groups.values()) {
      const r = left.op;
      const what = r.index >= 0 ? (r.name || r.kind) : 'the outline';
      const reliefs = aspects.filter((a) => a.startsWith('relief')).length;
      const extra = aspects.filter((a) => a !== 'op' && !a.startsWith('relief'));
      const more = [...extra, ...(reliefs ? [`${reliefs} dog bone${reliefs === 1 ? '' : 's'}`] : [])].join(', ');
      own.push(`left out: ${left.part} ${what}${more ? ` (${more})` : ''}: ${left.why}${note ? `, ${note}` : ''}`);
    }
    for (const problem of setup.problems) {
      own.push(`problem: ${problem}`);
      listed.add(`${setup.name}: ${problem}`);
    }
    if (own.length) lines.push(`${setupLabel(plan, setup)}:`, ...own.map((line) => '  ' + line));
  }
  for (const problem of plan?.problems ?? []) if (!listed.has(problem)) lines.push(`problem: ${problem}`);
  return lines.join('\n');
}
