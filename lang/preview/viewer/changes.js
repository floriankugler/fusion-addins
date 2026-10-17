// What a save changed (design/proposals/preview-assist.md, What a save
// changed): the layout a rebuild brings against the one on screen, per path
// (each part, and each body of a bought part, as the scene names them):
// what was added, what is gone and what changed, and for a changed part
// which operations differ, were added or removed, which outline segments
// differ, whether its box changed and what else (material, settings, grain,
// nest). Then where the page glows (`changeMarks`) and what the panel says
// (`changeRows`). Pure, without three.js or the DOM, so `node --test` checks
// it; linear in the parts and operations.
//
// Provenance is no change: a part's or operation's `where` (the build file's
// line) and a setting's `source` (the node that set it) are left out, so a
// line inserted above a board, or a setting moved to another scope with the
// same value, changes nothing.

import { AXIS, opPoint } from './scene-utils.js';

const PROVENANCE = new Set(['where', 'source']);

// Numbers within this (mm) are equal: below it a difference is float noise
// (a part moved and its coordinates added up again), far below the 0.01 mm
// the language cleans geometry at. key() rounds to it.
const TOL = 1e-4;

// A box's extents and a move are equal within this (mm).
const EPS = 1e-6;

/**
 * Whether two values of a layout are the same but for provenance (`where`,
 * `source`) and float noise (numbers within 0.1 µm). `seen.provenance` is
 * set when provenance differed on the way.
 */
export function same(a, b, seen = null) {
  if (a === b) return true;
  if (typeof a !== 'object' || typeof b !== 'object' || a === null || b === null) {
    return typeof a === 'number' && typeof b === 'number' && Math.abs(a - b) <= TOL;
  }
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  if (Array.isArray(a)) {
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) {
      const x = a[i], y = b[i];
      if (x === y) continue;
      if (typeof x === 'number') { if (typeof y !== 'number' || Math.abs(x - y) > TOL) return false; continue; }
      if (Array.isArray(x) && x.length === 2 && typeof x[0] === 'number' && Array.isArray(y) && y.length === 2) {
        // a point [u, v], the bulk of outlines and shapes
        if (!(Math.abs(x[0] - y[0]) <= TOL && Math.abs(x[1] - y[1]) <= TOL)) return false;
        continue;
      }
      if (!same(x, y, seen)) return false;
    }
    return true;
  }
  let keys = 0;
  for (const key in a) {
    if (PROVENANCE.has(key)) {
      if (seen && a[key] !== b[key]) seen.provenance = true;
      continue;
    }
    keys++;
    if (!(key in b) || !same(a[key], b[key], seen)) return false;
  }
  for (const key in b) if (!PROVENANCE.has(key)) keys--;
  return keys === 0;
}

// A value as a string for matching: provenance left out, numbers in units
// of 0.1 µm (TOL), so that a part moved whole matches itself despite float
// noise. Keys are written in the order the layout writes them.
function key(value) {
  if (typeof value === 'number') return String(Math.round(value / TOL));
  if (typeof value !== 'object' || value === null) return JSON.stringify(value) ?? 'null';
  let text;
  if (Array.isArray(value)) {
    text = '[';
    for (const x of value) text += (typeof x === 'number' ? Math.round(x / TOL) : key(x)) + ',';
    return text + ']';
  }
  text = '{';
  for (const k in value) if (!PROVENANCE.has(k)) text += JSON.stringify(k) + ':' + key(value[k]) + ',';
  return text + '}';
}

/** What the diff compares of a layout, by the path the scene names it by: each part as
 * `{part}`, each body of a bought part as `{item, body}`. */
export function layoutIndex(layout) {
  const things = new Map();
  for (const m of layout?.modules ?? []) {
    for (const part of m.parts) things.set(part.path, { part });
    for (const item of m.hardware ?? []) {
      for (const body of item.bodies) things.set(`${item.path}.${body.name}`, { item, body });
    }
  }
  return things;
}

/** An operation's name (an edge operation's is its inner one's), null for none. */
export function opName(op) {
  return (op.kind === 'edge' ? op.op?.name : op.name) ?? null;
}

/** An operation's kind as the diff pairs them: `hole`, `edge pocket`. */
export function opKind(op) {
  return op.kind === 'edge' ? `edge ${op.op?.kind}` : op.kind;
}

/**
 * What changed from the layout `before` to `after`: `{added, gone, changed,
 * problems: {added, gone}, provenance}`. `added` and `gone` are paths; each of
 * `changed` is a part's or bought body's change (`partChange`,
 * `bodyChange`). `provenance` is whether provenance differed somewhere (a
 * line of the build file, a setting's source) where nothing else did.
 */
export function diffLayouts(before, after) {
  const was = layoutIndex(before), now = layoutIndex(after);
  const seen = { provenance: false };
  const diff = { added: [], gone: [], changed: [], problems: problemChanges(before, after), provenance: false };
  for (const [path, thing] of now) {
    const old = was.get(path);
    if (!old || !old.part !== !thing.part) { diff.added.push(path); continue; }
    const change = thing.part ? partChange(old.part, thing.part, after.frame, seen) : bodyChange(old, thing, seen);
    if (change) diff.changed.push(change);
  }
  for (const [path, thing] of was) {
    const now_ = now.get(path);
    if (!now_ || !now_.part !== !thing.part) diff.gone.push(path);
  }
  diff.provenance = seen.provenance;
  return diff;
}

// A problem's text without the build file's lines in it, so a problem
// whose line moved is the same problem.
const LINE = /[^\s:'"()]+\.py:\d+/g;

function problemChanges(before, after) {
  const count = new Map();
  for (const text of before?.problems ?? []) {
    const k = text.replace(LINE, '');
    count.set(k, (count.get(k) ?? 0) + 1);
  }
  const added = [];
  for (const text of after?.problems ?? []) {
    const k = text.replace(LINE, '');
    if (count.get(k)) count.set(k, count.get(k) - 1); else added.push(text);
  }
  const gone = [];
  for (const text of before?.problems ?? []) {
    const k = text.replace(LINE, '');
    if (count.get(k)) { count.set(k, count.get(k) - 1); gone.push(text); }
  }
  return { added, gone };
}

// The keys of a part the diff looks at on their own; the others are its
// `rest`.
const OWN = new Set(['path', 'where', 'ops', 'outline', 'box', 'origin', 'axes', 'settings', 'op_settings']);

/**
 * A part's change, or null when it is the same but for provenance:
 * `{path, kind: 'part', box, moved, resized, turned, ops, outline, rest,
 * values, settings}`.
 *
 * - `box`: its box (or origin) changed; `moved`: the world vector it moved
 *   by when its box moved whole, size and axes kept, else null; `resized`:
 *   its box's extents changed; `turned`: its axes changed (then its
 *   operations and outline are not compared: every coordinate differs).
 * - `ops`: `{changed, added, removed}`, each `{index, name, kind}` (`index`
 *   in the new part's operations, a removed one's in the old part's; a
 *   changed one's old index is `was`). Operations are matched by name, else
 *   (the unnamed ones) by being equal, else by their order among those of
 *   their kind; `where` is left out.
 * - `outline`: `{added, removed}`, the segments of the new outline that the
 *   old has not and those of the old the new has not, each `[u0, v0, u1,
 *   v1]`.
 * - A part that moved whole is compared as it was and as moved, and the
 *   comparison that matches more operations and segments counts: a part
 *   moved with its holes changes no operation.
 * - `rest`: the other keys that differ (material, grain, nest, faces...),
 *   with `values[key] = [was, now]`; `settings`: the settings whose value
 *   differs, `{name, was, now}` (null for none), an operation's own as
 *   `toekick: cam.tabs`.
 */
export function partChange(old, now, frame, seen = null) {
  if (same(old, now, seen)) return null;
  const change = { path: now.path, kind: 'part', box: !same(old.box, now.box) || !same(old.origin, now.origin),
    moved: null, resized: false, turned: !same(old.axes, now.axes), ops: null, outline: null,
    rest: [], values: {}, settings: [] };
  const d = [0, 1, 2].map((i) => now.box.min[i] - old.box.min[i]);
  change.resized = [0, 1, 2].some((i) =>
    Math.abs((now.box.max[i] - now.box.min[i]) - (old.box.max[i] - old.box.min[i])) > EPS);
  if (!change.turned && !change.resized && d.some((x) => Math.abs(x) > EPS)) change.moved = d;
  if (!change.turned) {
    // moved whole with everything on it, as most moves are: no need to compare it as it was
    let best = change.moved ? compareShapes(old, now, frame, change.moved) : null;
    if (!best || !best.whole) {
      const as = compareShapes(old, now, frame, null);
      if (!best || as.score >= best.score) best = as;
    }
    change.ops = best.ops;
    change.outline = best.outline;
  }
  for (const k of new Set([...Object.keys(old), ...Object.keys(now)])) {
    if (OWN.has(k) || same(old[k], now[k])) continue;
    change.rest.push(k);
    change.values[k] = [old[k] ?? null, now[k] ?? null];
  }
  change.settings = settingChanges(old.settings, now.settings, '');
  for (const op of new Set([...Object.keys(old.op_settings ?? {}), ...Object.keys(now.op_settings ?? {})])) {
    change.settings.push(...settingChanges(old.op_settings?.[op], now.op_settings?.[op], `${op}: `));
  }
  return change;
}

function settingChanges(was = {}, now = {}, prefix) {
  const changes = [];
  for (const name of new Set([...Object.keys(was ?? {}), ...Object.keys(now ?? {})])) {
    if (!same(was?.[name]?.value, now?.[name]?.value) || !was?.[name] !== !now?.[name]) {
      changes.push({ name: prefix + name, was: was?.[name]?.value ?? null, now: now?.[name]?.value ?? null });
    }
  }
  return changes;
}

// The operations and outline of a part compared, the old one moved by `d`
// (world mm) or not moved (null); `score` counts what matched.
function compareShapes(old, now, frame, d) {
  const axes = now.axes;
  const shift = (axis) => (d ? d[AXIS[axis]] : 0);
  const du = shift(axes.u), dv = shift(axes.v), dt = shift(axes.t);
  const was = d ? old.ops.map((op) => shiftOp(op, du, dv, dt, axes, frame, d)) : old.ops;
  const ops = matchOps(was, now.ops);
  const outline = compareOutline(old.outline, now.outline, du, dv);
  return { ops: { changed: ops.changed, added: ops.added, removed: ops.removed }, outline: { added: outline.added, removed: outline.removed },
    score: ops.same + outline.same,
    whole: !ops.changed.length && !ops.added.length && !ops.removed.length && !outline.added.length && !outline.removed.length };
}

const shiftPoint = (p, du, dv) => [p[0] + du, p[1] + dv];
const shiftRings = (rings, du, dv) => rings.map((ring) => ring.map((p) => shiftPoint(p, du, dv)));

// An operation as it lies once its part moved by (du, dv) along the part's u
// and v axes (dt along its thickness, `d` the world vector): its points in
// the face's (u, v), an edge operation's place along its face.
function shiftOp(op, du, dv, dt, axes, frame, d) {
  switch (op.kind) {
    case 'hole': return { ...op, u: op.u + du, v: op.v + dv };
    case 'vgroove': return { ...op, start: shiftPoint(op.start, du, dv), end: shiftPoint(op.end, du, dv) };
    case 'cut': case 'pocket': return { ...op, shape: shiftRings(op.shape, du, dv),
      dogbones: op.dogbones?.map((b) => ({ ...b, center: shiftPoint(b.center, du, dv) })),
      ...(op.slot ? { slot: { ...op.slot, start: shiftPoint(op.slot.start, du, dv), end: shiftPoint(op.slot.end, du, dv) } } : {}) };
    case 'edge': {
      const faceAxis = frame?.[op.face]?.[1];
      const along = faceAxis === axes.u ? axes.v : axes.u;
      return { ...op, s: op.s + d[AXIS[along]], t: op.t + dt };
    }
    default: return op;   // a chamfer names what it follows
  }
}

// A multimap of indices that hands each out once, in order.
function push(map, k, i) {
  const entry = map.get(k);
  if (entry) entry.list.push(i); else map.set(k, { list: [i], at: 0 });
}
function take(map, k) {
  const entry = map.get(k);
  return entry && entry.at < entry.list.length ? entry.list[entry.at++] : undefined;
}

// The old operations (moved with their part, where it moved) paired with
// the new: those at the same place in the list that are the same first
// (most of them, without keys), then the rest by the rules partChange
// gives, by keys made for them only.
function matchOps(was, now) {
  const used = new Uint8Array(was.length), matched = new Uint8Array(now.length);
  const result = { same: 0, changed: [], added: [], removed: [] };
  const entry = (op, index) => ({ index, name: opName(op), kind: opKind(op) });
  for (let i = 0; i < Math.min(was.length, now.length); i++) {
    if (opName(was[i]) === opName(now[i]) && same(was[i], now[i])) { used[i] = matched[i] = 1; result.same++; }
  }
  const wasKeys = [], nowKeys = [];
  const wasKey = (i) => (wasKeys[i] ??= key(was[i]));
  const nowKey = (j) => (nowKeys[j] ??= key(now[j]));
  const pair = (i, j) => {
    used[i] = 1; matched[j] = 1;
    if (wasKey(i) === nowKey(j)) result.same++;
    else result.changed.push({ ...entry(now[j], j), was: i });
  };
  // named ones by name, the k-th of a name with the k-th
  const byName = new Map();
  was.forEach((op, i) => { const name = opName(op); if (name !== null && !used[i]) push(byName, name, i); });
  now.forEach((op, j) => {
    const name = opName(op);
    if (name === null || matched[j]) return;
    const i = take(byName, name);
    if (i !== undefined) pair(i, j); else { matched[j] = 1; result.added.push(entry(op, j)); }
  });
  // unnamed ones: an equal one first, then in order among those of their kind
  const equal = new Map(), byKind = new Map();
  was.forEach((op, i) => { if (opName(op) === null && !used[i]) push(equal, wasKey(i), i); });
  now.forEach((op, j) => {
    if (matched[j]) return;
    let i = take(equal, nowKey(j));
    while (i !== undefined && used[i]) i = take(equal, nowKey(j));
    if (i !== undefined) pair(i, j);
  });
  was.forEach((op, i) => { if (!used[i] && opName(op) === null) push(byKind, opKind(op), i); });
  now.forEach((op, j) => {
    if (matched[j]) return;
    const i = take(byKind, opKind(op));
    if (i !== undefined) pair(i, j); else { matched[j] = 1; result.added.push(entry(op, j)); }
  });
  was.forEach((op, i) => { if (!used[i]) result.removed.push(entry(op, i)); });
  result.changed.sort((a, b) => a.index - b.index);
  result.added.sort((a, b) => a.index - b.index);
  return result;
}

// A point's key, rounded as key() rounds.
const pointKey = (u, v) => `${Math.round(u / TOL)},${Math.round(v / TOL)};`;

// An outline's segments, each with a key that is the same whichever way the
// ring runs and wherever it starts.
function segments(rings, du, dv) {
  const list = [];
  for (const ring of rings ?? []) {
    let k = ring.length - 1, ka = ring.length ? pointKey(ring[k][0] + du, ring[k][1] + dv) : '';
    for (let i = 0; i < ring.length; k = i++) {
      const kb = pointKey(ring[i][0] + du, ring[i][1] + dv);
      if (ka !== kb) list.push({ key: ka < kb ? ka + kb : kb + ka, segment: [ring[k][0], ring[k][1], ring[i][0], ring[i][1]] });
      ka = kb;
    }
  }
  return list;
}

// Whether a ring moved by (du, dv) is the ring `now`, point by point.
function ringSame(was, now, du, dv) {
  if (was.length !== now.length) return false;
  for (let i = 0; i < was.length; i++) {
    if (Math.abs(was[i][0] + du - now[i][0]) > TOL || Math.abs(was[i][1] + dv - now[i][1]) > TOL) return false;
  }
  return true;
}

// The outline's segments that differ: the rings the same point by point
// (most of them: a board's exterior when a mortise in it moved) first, the
// others by their segments.
function compareOutline(rings = [], ringsNow = [], du, dv) {
  let same = 0;
  const was = [], now = [];
  for (let r = 0; r < Math.max(rings.length, ringsNow.length); r++) {
    if (r < rings.length && r < ringsNow.length && ringSame(rings[r], ringsNow[r], du, dv)) { same += ringsNow[r].length; continue; }
    if (r < rings.length) was.push(rings[r]);
    if (r < ringsNow.length) now.push(ringsNow[r]);
  }
  if (!was.length && !now.length) return { same, added: [], removed: [] };
  const count = new Map();
  const old = segments(was, du, dv);
  for (const s of old) count.set(s.key, (count.get(s.key) ?? 0) + 1);
  const result = { same, added: [], removed: [] };
  for (const s of segments(now, 0, 0)) {
    if (count.get(s.key)) { count.set(s.key, count.get(s.key) - 1); result.same++; } else result.added.push(s.segment);
  }
  for (const s of old) {
    if (count.get(s.key)) { count.set(s.key, count.get(s.key) - 1); result.removed.push(s.segment); }
  }
  return result;
}

/**
 * A bought part's body's change, or null when it is the same:
 * `{path, kind: 'hardware', box, moved, resized, rest, values}`; `moved` the
 * world vector when all its boxes moved by it.
 */
export function bodyChange(old, now, seen = null) {
  const sameBody = same(old.body, now.body, seen);
  const rest = [], values = {};
  for (const k of new Set([...Object.keys(old.item), ...Object.keys(now.item)])) {
    if (k === 'path' || k === 'bodies' || PROVENANCE.has(k)) {
      if (seen && k === 'where' && old.item.where !== now.item.where) seen.provenance = true;
      continue;
    }
    if (!same(old.item[k], now.item[k])) { rest.push(k); values[k] = [old.item[k] ?? null, now.item[k] ?? null]; }
  }
  if (sameBody && !rest.length) return null;
  const change = { path: `${now.item.path}.${now.body.name}`, kind: 'hardware', box: !sameBody, moved: null,
    resized: !sameBody, rest, values };
  const a = old.body.boxes, b = now.body.boxes;
  if (!sameBody && a.length === b.length && a.length) {
    const d = [0, 1, 2].map((i) => b[0].min[i] - a[0].min[i]);
    const whole = a.every((box, k) => [0, 1, 2].every((i) =>
      Math.abs(b[k].min[i] - box.min[i] - d[i]) <= EPS && Math.abs(b[k].max[i] - box.max[i] - d[i]) <= EPS));
    if (whole && d.some((x) => Math.abs(x) > EPS)) { change.moved = d; change.resized = false; }
  }
  return change;
}

// -- where the page glows ------------------------------------------------------

/**
 * Where an operation is, in world mm, for the glow: `{points, lines}` (a
 * line `[[x, y, z], [x, y, z]]`), or null when the page cannot place it. A
 * hole, pocket, cut, V-groove or edge operation is its point (`opPoint`,
 * where `preview.look` aims); a chamfer runs along what it names: the
 * outline on its face, a named operation, or the box edge where two faces
 * meet (`front.top`).
 */
export function opMarks(frame, part, op) {
  if (op.kind === 'chamfer') {
    if (op.what === 'outline') {
      const code = frame[op.face];
      if (!code || code[1] !== part.axes.t) return null;
      const t = code[0] === '+' ? part.box.max[AXIS[part.axes.t]] : part.box.min[AXIS[part.axes.t]];
      return { points: [], lines: part.outline.flatMap((ring) => ring.map((p, i) =>
        [world(part, ring[(i || ring.length) - 1], t), world(part, p, t)])) };
    }
    const named = part.ops.find((o) => o !== op && opName(o) === op.what);
    if (named) return opMarks(frame, part, named);
    const names = op.what.split('.');
    const codes = names.map((n) => frame[n]);
    if (names.length !== 2 || codes.some((c) => !c) || codes[0][1] === codes[1][1]) return null;
    const b = part.box;
    const from = [0, 0, 0], to = [0, 0, 0];
    for (const code of codes) {
      const i = AXIS[code[1]];
      from[i] = to[i] = code[0] === '+' ? b.max[i] : b.min[i];
    }
    const k = [0, 1, 2].find((i) => !codes.some((c) => AXIS[c[1]] === i));
    from[k] = b.min[k]; to[k] = b.max[k];
    return { points: [], lines: [[from, to]] };
  }
  try {
    return { points: [opPoint(frame, part, op)], lines: [] };
  } catch (e) {
    return null;
  }
}

// A point of a part's outline, (u, v), at `t` along its thickness axis, in world mm.
function world(part, [u, v], t) {
  const p = [0, 0, 0];
  p[AXIS[part.axes.u]] = u; p[AXIS[part.axes.v]] = v; p[AXIS[part.axes.t]] = t;
  return p;
}

/**
 * Where the page glows for a diff: `marks`, each `{at, kind, path, op}` (a
 * halo at a point: `changed`, `added`, `removed`, or `was`, a changed
 * operation's old point where it moved), `lines`, each `{from, to, kind,
 * path, op?}` (a glow along a chamfer's edge, or along an outline segment
 * that differs, kind `outline`, at mid thickness), and `unplaced`, the
 * operations it cannot place, as `path: label`.
 */
export function changeMarks(diff, before, after) {
  const was = layoutIndex(before), now = layoutIndex(after);
  const marks = [], lines = [], unplaced = [];
  for (const change of diff.changed) {
    if (change.kind !== 'part') continue;
    const old = was.get(change.path).part, part = now.get(change.path).part;
    const place = (frame, p, entry, kind) => {
      const op = p.ops[entry.index], label = opLabel(entry);
      const found = opMarks(frame, p, op);
      if (!found) { unplaced.push(`${change.path}: ${label}`); return null; }
      for (const at of found.points) marks.push({ at, kind, path: change.path, op: label });
      for (const [from, to] of found.lines) lines.push({ from, to, kind, path: change.path, op: label });
      return found;
    };
    for (const entry of change.ops?.changed ?? []) {
      const found = place(after.frame, part, entry, 'changed');
      const before_ = found && opMarks(before.frame, old, old.ops[entry.was]);
      const at = found?.points[0], then = before_?.points[0];
      if (at && then && Math.hypot(at[0] - then[0], at[1] - then[1], at[2] - then[2]) > 0.01) {
        marks.push({ at: then, kind: 'was', path: change.path, op: opLabel(entry) });
      }
    }
    for (const entry of change.ops?.added ?? []) place(after.frame, part, entry, 'added');
    for (const entry of change.ops?.removed ?? []) place(before.frame, old, entry, 'removed');
    // at mid thickness: the glow is drawn through the parts
    const ti = AXIS[part.axes.t], t = (part.box.min[ti] + part.box.max[ti]) / 2;
    for (const [u0, v0, u1, v1] of change.outline?.added ?? []) {
      lines.push({ from: world(part, [u0, v0], t), to: world(part, [u1, v1], t), kind: 'outline', path: change.path });
    }
  }
  return { marks, lines, unplaced };
}

/**
 * A diff and its glows as `preview.changes()` gives them, short enough to
 * read: each change with its outline as `{added, removed, at}` (how many
 * segments differ, and the world point in the middle of those that glow,
 * null for none) instead of the segments, the halos as they are (`marks`,
 * each with its point), the glowing lines counted (`lines`).
 */
export function changeReport(diff, glows) {
  const middle = new Map();
  for (const line of glows.lines) {
    if (line.kind !== 'outline') continue;
    let box = middle.get(line.path);
    if (!box) middle.set(line.path, box = { min: [Infinity, Infinity, Infinity], max: [-Infinity, -Infinity, -Infinity] });
    for (const p of [line.from, line.to]) {
      for (let i = 0; i < 3; i++) { box.min[i] = Math.min(box.min[i], p[i]); box.max[i] = Math.max(box.max[i], p[i]); }
    }
  }
  const round = (x) => Math.round(x * 100) / 100;
  return {
    added: diff.added, gone: diff.gone, problems: diff.problems, provenance: diff.provenance,
    changed: diff.changed.map((change) => {
      if (!change.outline) return change;
      const box = middle.get(change.path);
      return { ...change, outline: { added: change.outline.added.length, removed: change.outline.removed.length,
        at: box ? box.min.map((x, i) => round((x + box.max[i]) / 2)) : null } };
    }),
    marks: glows.marks, lines: glows.lines.length, unplaced: glows.unplaced,
  };
}

/** An operation of a diff as the panel names it: its name, else its kind and index (`hole 3`). */
export function opLabel(entry) {
  return entry.name ?? `${entry.kind} ${entry.index}`;
}

// -- what the panel says ---------------------------------------------------------

/** A length in mm as the panel writes it: 20, 0.5, 2.25, 0.004. */
export function mm(x) {
  const r = Math.round(x * 100) / 100;
  return String(r !== 0 ? r : Number(x.toPrecision(2)));
}

/** A move as the layout's directions name it: `right 20 mm, back 2 mm`. */
export function moveText(d, frame) {
  const parts = [];
  d.forEach((x, i) => {
    if (Math.abs(x) <= EPS) return;
    const code = (x > 0 ? '+' : '-') + 'xyz'[i];
    const name = Object.keys(frame ?? {}).find((n) => frame[n] === code) ?? code;
    parts.push(`${name} ${mm(Math.abs(x))} mm`);
  });
  return parts.join(', ');
}

function valueText(value) {
  if (value === null || value === undefined) return 'none';
  if (typeof value === 'number') return mm(value);
  if (typeof value === 'string') return value;
  return JSON.stringify(value);
}

/** What changed of one part, in a few words: `moved right 20 mm, 2 ops, material`. */
export function changeSummary(change, frame) {
  const words = [];
  if (change.kind === 'hardware') words.push('hardware');
  if (change.moved) words.push('moved ' + moveText(change.moved, frame));
  else if (change.turned) words.push('turned');
  else if (change.resized) words.push(change.kind === 'hardware' ? 'reshaped' : 'resized');
  const ops = change.ops ? change.ops.changed.length + change.ops.added.length + change.ops.removed.length : 0;
  if (ops) words.push(`${ops} op${ops === 1 ? '' : 's'}`);
  if (change.outline?.added.length || change.outline?.removed.length) words.push('outline');
  words.push(...change.rest);
  if (change.settings?.length) words.push(change.settings.length === 1 ? 'a setting' : `${change.settings.length} settings`);
  if (!words.length || (words.length === 1 && change.kind === 'hardware')) words.push(change.box ? 'its box' : 'the order of its ops');
  return words.join(', ');
}

/**
 * What the panel says about a diff, as rows of pieces (`{text}`, or `{text,
 * path}` for a path the page makes a link that selects it): a line each for
 * the parts changed, added and gone (the first `most` of each named), then
 * the values the glow cannot show (material, settings...), the operations
 * it could not place (`unplaced`) and the problems that came and went.
 */
export function changeRows(diff, frame, unplaced = [], most = 8) {
  const rows = [];
  const count = (n, what) => `${n} ${what}${n === 1 ? '' : 's'}`;
  const listed = (head, items) => {
    const row = [{ text: head + ': ' }];
    items.slice(0, most).forEach((item, k) => {
      if (k) row.push({ text: ', ' });
      row.push({ text: item.path, path: item.path });
      if (item.note) row.push({ text: ` (${item.note})` });
    });
    if (items.length > most) row.push({ text: `, and ${items.length - most} more` });
    rows.push(row);
  };
  if (diff.changed.length) {
    listed(`${count(diff.changed.length, 'part')} changed`,
      diff.changed.map((c) => ({ path: c.path, note: changeSummary(c, frame) })));
  }
  if (diff.added.length) listed(`${count(diff.added.length, 'part')} added`, diff.added.map((path) => ({ path })));
  if (diff.gone.length) listed(`${count(diff.gone.length, 'part')} gone`, diff.gone.map((path) => ({ path })));
  if (!rows.length) {
    rows.push([{ text: diff.provenance ? 'no part changed, only lines of the build file' : 'no part changed' }]);
  }
  const details = [];
  for (const change of diff.changed) {
    const at = { text: change.path, path: change.path };
    for (const k of change.rest) {
      const [was, now] = change.values[k];
      details.push(typeof was === 'object' && was !== null || typeof now === 'object' && now !== null
        ? [at, { text: `: ${k} changed` }]
        : [at, { text: `: ${k} ${valueText(was)} → ${valueText(now)}` }]);
    }
    for (const s of change.settings ?? []) details.push([at, { text: `: ${s.name} ${valueText(s.was)} → ${valueText(s.now)}` }]);
  }
  rows.push(...details.slice(0, most * 2));
  if (details.length > most * 2) rows.push([{ text: `and ${details.length - most * 2} more values` }]);
  if (unplaced.length) rows.push([{ text: `not placed in the scene: ${unplaced.slice(0, most).join(', ')}` +
    (unplaced.length > most ? `, and ${unplaced.length - most} more` : '') }]);
  for (const text of diff.problems.added) rows.push([{ text: `new problem: ${text}` }]);
  if (diff.problems.gone.length) rows.push([{ text: `${count(diff.problems.gone.length, 'problem')} gone` }]);
  return rows;
}
