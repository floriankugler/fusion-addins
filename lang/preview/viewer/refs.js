// The selection's references: what a click in the scene names (a part's
// face, an edge, a corner, a point on a face), spelled as the build file
// writes it, the items the selection panel lists, and the snippets it
// offers for them (design/proposals/preview-assist.md, The selection
// panel, Click to select, click to copy, Snippets to copy). Plain data in
// and out, no three.js and no DOM, so that `node --test
// lang/preview/viewer/tests/` checks it.
//
// A reference is `{part, face, anchor, center, point}`: `part` a part's,
// a bought part's (a body or the item), a scope's or a module's path;
// `face` the world name of one of the part's faces (`front`, as the
// layout's `frame` and the part's `faces` key it), or none; `anchor` the
// edges named on that face, each `[world name, mm or null]`: one is an
// edge (`left.inner.front`), two a corner (`left.inner.front.bottom`), and
// a number measures from its edge (`left.inner.front(37).bottom(120)`);
// `center` the face's middle (`left.inner.center`); `point` the world
// point in mm a click fell on, kept with the reference. The build file's
// names come from the part's `faces`: the direction in its scope's frame,
// then `inner` or `outer` where it resolves.

import { AXIS } from './scene-utils.js';

/** How near an edge a click selects it, in screen pixels; two edges this near make a corner. */
export const TOLERANCE = 6;

/** The value a snippet offers to adjust: `.into(15)`, `.gap(15)`, `front(15)`. */
export const MOVE = 15;

/** The distance from either of two parallel faces a snippet offers: `bottom.top.gap(100)`. */
export const APART = 100;

const AXES = ['x', 'y', 'z'];

// The extent each direction of a frame measures along, as a box names it (design/placement.md).
const EXTENT = { left: 'width', right: 'width', front: 'depth', back: 'depth', top: 'height', bottom: 'height' };
const EXTENTS = ['width', 'depth', 'height'];

/** A length or a position as a snippet writes it: whole where it is, else to a hundredth. */
export function num(value) {
  const r = Math.round(value * 100) / 100;
  return String(Object.is(r, -0) ? 0 : r);
}

// -- frames ------------------------------------------------------------------

// A world face name's axis, its index and its sign: frame.front === '-x'.
function dir(frame, world) {
  const code = frame[world];
  if (!code) throw new Error(`no direction ${JSON.stringify(world)} in the layout's frame`);
  return { axis: code[1], i: AXIS[code[1]], sign: code[0] === '+' ? 1 : -1 };
}

// The world face name of an axis and a sign.
function worldName(frame, axis, sign) {
  const code = (sign > 0 ? '+' : '-') + axis;
  return Object.keys(frame).find((name) => frame[name] === code);
}

// The plane of a box's face, as a value on its axis.
function plane(box, d) {
  return d.sign > 0 ? box.max[d.i] : box.min[d.i];
}

/**
 * The world axis of each extent of a part's scope frame, as the build file
 * names them (`{width: 'y', depth: 'x', height: 'z'}`), read from the
 * part's `faces`: the direction each world face has in its scope. Without
 * a part, the world frame's own.
 */
export function frameAxes(part, frame) {
  const axes = {};
  for (const world of Object.keys(frame)) {
    const name = part ? part.faces?.[world]?.[0] : world;
    if (EXTENT[name]) axes[EXTENT[name]] = frame[world][1];
  }
  return axes;
}

/** A box's extents in a frame, `[[width, 570], [depth, 500], [height, 15]]` (mm, to a hundredth), those on
 *  `only` (world axes) alone when given. */
export function sizeIn(box, axes, only = null) {
  return EXTENTS.filter((e) => axes[e] && (!only || only.includes(axes[e])))
    .map((e) => [e, Math.round((box.max[AXIS[axes[e]]] - box.min[AXIS[axes[e]]]) * 100) / 100]);
}

/** A size as the panel says it: `width 570, depth 500, height 15`. */
export function sizeText(size) {
  return size.map(([name, mm]) => `${name} ${num(mm)}`).join(', ');
}

// -- the layout's things, by path ---------------------------------------------

const indexes = new WeakMap();

/**
 * The layout's things by path, made once per layout: `parts`, the bought
 * parts' `bodies` and `items`, the `modules`, the `scopes` (the path
 * prefixes of parts that are neither a part nor a module), and the module
 * of each part and item (`moduleOf`).
 */
export function indexLayout(layout) {
  let idx = indexes.get(layout);
  if (idx) return idx;
  idx = { frame: layout.frame, parts: new Map(), bodies: new Map(), items: new Map(), modules: new Map(),
          scopes: new Set(), moduleOf: new Map() };
  const prefixes = [];
  for (const m of layout.modules ?? []) {
    idx.modules.set(m.path, m);
    for (const part of m.parts) {
      idx.parts.set(part.path, part);
      idx.moduleOf.set(part.path, m);
      prefixes.push(part.path);
    }
    for (const item of m.hardware ?? []) {
      idx.items.set(item.path, item);
      idx.moduleOf.set(item.path, m);
      prefixes.push(item.path);
      for (const body of item.bodies) idx.bodies.set(`${item.path}.${body.name}`, { item, body });
    }
  }
  for (const path of prefixes) {
    const segments = path.split('.');
    for (let k = 1; k < segments.length; k++) {
      const scope = segments.slice(0, k).join('.');
      if (!idx.modules.has(scope) && !idx.parts.has(scope)) idx.scopes.add(scope);
    }
  }
  indexes.set(layout, idx);
  return idx;
}

// The boxes under a path: a part's, a body's, every part and body below a scope or module.
function boxesUnder(idx, path) {
  const boxes = [];
  const under = (p) => p === path || p.startsWith(path + '.');
  for (const [p, part] of idx.parts) if (under(p)) boxes.push(part.box);
  for (const [p, { body }] of idx.bodies) if (under(p)) boxes.push(...body.boxes);
  return boxes;
}

function union(boxes) {
  if (!boxes.length) return null;
  const min = [0, 1, 2].map((i) => Math.min(...boxes.map((b) => b.min[i])));
  const max = [0, 1, 2].map((i) => Math.max(...boxes.map((b) => b.max[i])));
  return { min, max };
}

// The module a path lies in: a part's or item's own, else the longest module path above it.
function moduleAt(idx, path) {
  const own = idx.moduleOf.get(path) ?? idx.moduleOf.get(idx.bodies.get(path)?.item.path);
  if (own) return own;
  let found = null;
  for (const [p, m] of idx.modules) {
    if ((p === path || path.startsWith(p + '.') || p === '') && (!found || p.length > found.path.length)) found = m;
  }
  return found;
}

// The frame a path's sizes are given in: its own part's, else the first part of its module's.
function axesAt(idx, path) {
  const part = idx.parts.get(path) ?? moduleAt(idx, path)?.parts[0];
  return frameAxes(part ?? null, idx.frame);
}

/** What a reference is: `board`, `slat`, `hardware`, `module`, `scope`, `face`, `edge`, `corner`,
 *  `point`, or `gone` (its part is not in the layout). */
export function kindOf(ref, layout) {
  const idx = indexLayout(layout);
  const part = idx.parts.get(ref.part);
  if (ref.face && part) {
    const anchor = ref.anchor ?? [];
    if (ref.center || anchor.some(([, v]) => v !== null && v !== undefined)) return 'point';
    return ['face', 'edge', 'corner'][anchor.length];
  }
  if (part) return part.kind === 'slat' ? 'slat' : 'board';
  if (idx.bodies.has(ref.part) || idx.items.has(ref.part)) return 'hardware';
  if (idx.modules.has(ref.part)) return 'module';
  if (idx.scopes.has(ref.part)) return 'scope';
  return 'gone';
}

// -- spelling ----------------------------------------------------------------

// A face's name as the build file writes it: `inner` or `outer` where it
// resolves (`aliases`), else the direction in the scope's frame.
function faceName(part, world, aliases = true) {
  const names = part.faces?.[world];
  if (!names?.length) throw new Error(`${part.path} has no face ${world}`);
  return aliases ? names[names.length - 1] : names[0];
}

/** A reference as the build file writes it, with `inner`/`outer` where they resolve, or with
 *  directions only (`aliases: false`). */
export function spell(ref, layout, { aliases = true } = {}) {
  if (!ref.face) return ref.part;
  const part = indexLayout(layout).parts.get(ref.part);
  if (!part) return ref.part;
  let text = `${ref.part}.${faceName(part, ref.face, aliases)}`;
  for (const [world, value] of ref.anchor ?? []) {
    text += '.' + faceName(part, world, aliases) + (value === null || value === undefined ? '' : `(${num(value)})`);
  }
  if (ref.center) text += '.center';
  return text;
}

/** A reference's spellings: with `inner`/`outer` first, then with directions only where that differs. */
export function spellings(ref, layout) {
  const a = spell(ref, layout), b = spell(ref, layout, { aliases: false });
  return a === b ? [a] : [a, b];
}

// -- reading a reference ---------------------------------------------------------

/**
 * A reference from its spelling: a part's, a bought part's, a scope's or a
 * module's path, followed for a part by a face (`kitchen.left.inner`), one
 * or two of the face's edges (`.front`, `.front.bottom`), each with a
 * distance from it or not (`.front(37).bottom(120)`), or `.center`. The
 * names are the build file's, as the part's `faces` list them. Throws,
 * saying what it can read, for anything else.
 */
export function parseRef(text, layout) {
  const idx = indexLayout(layout);
  const source = String(text).trim();
  const tokens = [];
  const re = /([^.()\s]+)(?:\(([^)]*)\))?(?:\.|$)/y;
  while (re.lastIndex < source.length) {
    const at = re.lastIndex;
    const found = re.exec(source);
    if (!found || re.lastIndex === at) throw new Error(`cannot read ${JSON.stringify(source)} at ${JSON.stringify(source.slice(at))}`);
    tokens.push({ name: found[1], value: found[2] });
  }
  let k = tokens.length;
  const known = (p) => idx.parts.has(p) || idx.bodies.has(p) || idx.items.has(p) || idx.modules.has(p) || idx.scopes.has(p);
  for (; k > 0; k--) {
    if (tokens.slice(0, k).some((t) => t.value !== undefined)) continue;
    if (known(tokens.slice(0, k).map((t) => t.name).join('.'))) break;
  }
  if (k === 0) throw new Error(`no part, bought part, scope or module in ${JSON.stringify(source)}`);
  const path = tokens.slice(0, k).map((t) => t.name).join('.');
  const rest = tokens.slice(k);
  if (!rest.length) return { part: path };
  const part = idx.parts.get(path);
  if (!part) throw new Error(`${path} is a ${kindOf({ part: path }, layout)}: it has no faces to name (${source})`);
  const worldOf = new Map();
  for (const [world, names] of Object.entries(part.faces)) for (const name of names) worldOf.set(name, world);
  const options = () => [...worldOf.keys()].join(', ');
  const [first, ...more] = rest;
  const face = worldOf.get(first.name);
  if (!face) throw new Error(`${path} has no face ${first.name}; its faces are ${options()}`);
  if (first.value !== undefined) throw new Error(`${path}.${first.name}(${first.value}): a face takes no distance; name an edge, ${path}.${first.name}.front(37)`);
  const ref = { part: path, face, anchor: [] };
  const axes = [dir(idx.frame, face).axis];
  for (const [n, token] of more.entries()) {
    if (token.name === 'center' && token.value === undefined && n === 0 && more.length === 1) { ref.center = true; break; }
    const world = worldOf.get(token.name);
    if (!world) throw new Error(`${source}: ${token.name} is no face of ${path}; its faces are ${options()}`);
    const axis = dir(idx.frame, world).axis;
    if (axes.includes(axis)) throw new Error(`${source}: ${token.name} is not an edge here: it lies on the axis of a face named before it`);
    if (ref.anchor.length === 2) throw new Error(`${source}: a face has two axes to name an edge on`);
    let value = null;
    if (token.value !== undefined) {
      value = Number(token.value);
      if (token.value.trim() === '' || !Number.isFinite(value)) throw new Error(`${source}: ${token.name}(${token.value}) takes a distance in mm`);
    }
    axes.push(axis);
    ref.anchor.push([world, value]);
  }
  return ref;
}

// -- picking -----------------------------------------------------------------------

/**
 * The face of a part a point lies on, as its world name: the face of the
 * part's box whose outward direction is the hit's `normal` (within about
 * 25 degrees) and whose plane lies within `slack` mm of the point; without
 * a normal, the face whose plane is nearest. Null where the point lies on
 * no face of the box: in a notch, a pocket, a hole, on a slanted edge.
 */
export function faceAt(part, frame, point, normal = null, slack = 0.5) {
  let best = null, score = -Infinity;
  for (const world of Object.keys(part.faces ?? {})) {
    const d = dir(frame, world);
    const off = Math.abs(point[d.i] - plane(part.box, d));
    if (normal) {
      const along = d.sign * normal[d.i];
      if (off > slack || along < 0.9 || along <= score) continue;
      best = world; score = along;
    } else if (-off > score) {
      best = world; score = -off;
    }
  }
  return best;
}

/**
 * The edges of a face around a point, per axis of the face's plane: the
 * nearer edge and the farther one, each `[world name, mm from the point]`,
 * the axis with the nearer edge first.
 */
export function edgeOffsets(part, frame, face, point) {
  const fi = dir(frame, face).i;
  return [0, 1, 2].filter((i) => i !== fi).map((i) => {
    const lo = [worldName(frame, AXES[i], -1), point[i] - part.box.min[i]];
    const hi = [worldName(frame, AXES[i], 1), part.box.max[i] - point[i]];
    return lo[1] <= hi[1] ? { i, near: lo, far: hi } : { i, near: hi, far: lo };
  }).sort((a, b) => a.near[1] - b.near[1]);
}

/**
 * What a click on a part names: the finest thing under the pointer. Of the
 * hit face's box edges, those within `tolerance` screen pixels of the hit
 * point (`scale`: mm per pixel at the hit; `view`: the ray's unit
 * direction, which shortens a distance seen at a slant): two make a
 * corner, one an edge, none leaves the face. The hit point is kept, on the
 * face's plane. A hit on no face of the part's box (`faceAt`) names the
 * part, with its point.
 */
export function pick(part, frame, { point, normal = null }, { scale = 0, view = null, tolerance = TOLERANCE, slack } = {}) {
  const face = faceAt(part, frame, point, normal, slack ?? Math.max(0.5, 2 * scale));
  if (!face) return { part: part.path, point: [...point] };
  const d = dir(frame, face);
  const at = [...point];
  at[d.i] = plane(part.box, d);
  for (let i = 0; i < 3; i++) if (i !== d.i) at[i] = Math.min(part.box.max[i], Math.max(part.box.min[i], at[i]));
  const seen = (e) => e.near[1] * Math.sqrt(Math.max(0, 1 - (view ? view[e.i] ** 2 : 0)));
  const near = edgeOffsets(part, frame, face, at).filter((e) => seen(e) <= tolerance * scale)
    .sort((a, b) => seen(a) - seen(b));
  return { part: part.path, face, anchor: near.map((e) => [e.near[0], null]), point: at };
}

/** The world point a reference names on its part: its anchor's (a face's middle, an edge's, a
 *  corner, a point measured from edges), or a part's, a scope's or a module's middle. */
export function anchorPoint(ref, layout) {
  const idx = indexLayout(layout);
  const part = idx.parts.get(ref.part);
  const box = part?.box ?? idx.modules.get(ref.part)?.box ?? union(boxesUnder(idx, ref.part));
  if (!box) return null;
  const p = [0, 1, 2].map((i) => (box.min[i] + box.max[i]) / 2);
  if (!part || !ref.face) return p;
  const d = dir(idx.frame, ref.face);
  p[d.i] = plane(box, d);
  for (const [world, value] of ref.anchor ?? []) {
    const e = dir(idx.frame, world);
    p[e.i] = plane(box, e) - e.sign * (value ?? 0);
  }
  return p;
}

/** An edge's ends, the corners of its face at either end of it, as world points (the reference names
 *  an edge: a face and one edge of it). */
export function edgeEnds(ref, layout) {
  const frame = indexLayout(layout).frame;
  const [edge] = ref.anchor;
  const k = AXES.find((a) => a !== dir(frame, ref.face).axis && a !== dir(frame, edge[0]).axis);
  return [-1, 1].map((sign) => anchorPoint({ ...ref, anchor: [[edge[0], null], [worldName(frame, k, sign), null]] }, layout));
}

/**
 * A world point on a part named (`preview.name(point)`): the face whose
 * plane is nearest (`off`, mm from it, where it is not on it), the nearest
 * edge with its distance, the nearest corner, and the anchor with the
 * whole-millimetre distances from the two nearest edges, each in its
 * spellings. Without a part given, the part whose box holds the point and
 * has a face plane nearest to it.
 */
export function nameAt(layout, point, path = null) {
  const idx = indexLayout(layout);
  let part = null, best = Infinity;
  if (path !== null) {
    part = idx.parts.get(path);
    if (!part) throw new Error(`no part ${path}`);
  } else {
    for (const candidate of idx.parts.values()) {
      const b = candidate.box;
      const outside = Math.max(...[0, 1, 2].map((i) => Math.max(b.min[i] - point[i], point[i] - b.max[i], 0)));
      if (outside > 0.5) continue;
      const face = faceAt(candidate, idx.frame, point);
      const off = Math.abs(point[dir(idx.frame, face).i] - plane(b, dir(idx.frame, face))) + outside;
      if (off < best) { best = off; part = candidate; }
    }
    if (!part) throw new Error(`no part at [${point.map(num).join(', ')}]`);
  }
  const ref = pick(part, idx.frame, { point }, { scale: 1, tolerance: Infinity, slack: Infinity });
  const d = dir(idx.frame, ref.face);
  const off = Math.abs(point[d.i] - plane(part.box, d));
  const edges = edgeOffsets(part, idx.frame, ref.face, ref.point);
  const round = (e) => [e[0], Math.round(e[1])];
  return {
    part: part.path,
    point: ref.point,
    ...(off > 0.01 ? { off: Math.round(off * 100) / 100 } : {}),
    face: spellings({ part: part.path, face: ref.face }, layout),
    edge: { spellings: spellings({ part: part.path, face: ref.face, anchor: [ref.anchor[0]] }, layout),
            mm: Math.round(edges[0].near[1] * 100) / 100 },
    corner: spellings({ part: part.path, face: ref.face, anchor: ref.anchor }, layout),
    anchor: spellings({ part: part.path, face: ref.face, anchor: [round(edges[0].near), round(edges[1].near)] }, layout),
  };
}

// -- the items the panel lists ------------------------------------------------------

// The scopes and modules above a path, nearest first, each {kind, path}.
function ancestors(idx, path) {
  const segments = path.split('.');
  const found = [];
  for (let k = segments.length - 1; k > 0; k--) {
    const p = segments.slice(0, k).join('.');
    if (idx.modules.has(p)) found.push({ kind: 'module', path: p });
    else if (idx.scopes.has(p)) found.push({ kind: 'scope', path: p });
  }
  return found;
}

// A part, item, scope or module as an item's line: {kind, path, material, size, where}.
function entry(idx, kind, path) {
  const part = idx.parts.get(path);
  const axes = axesAt(idx, path);
  if (part) return { kind, path, material: part.material, size: sizeIn(part.box, axes), where: part.where ?? '' };
  const item = idx.items.get(path) ?? idx.bodies.get(path)?.item;
  const m = idx.modules.get(path);
  const box = m?.box ?? union(boxesUnder(idx, path));
  return { kind, path, material: null, size: box ? sizeIn(box, axes) : [], where: item?.where ?? m?.where ?? '' };
}

/**
 * A reference as the panel lists it: what it is, its spellings, the
 * material, the size in its scope's frame (a part's three extents as
 * width, depth and height, a face's two, an edge's length), the line that
 * made it (`where`), its world point, the distances from the two nearest
 * edges for a point on a face, and what it belongs to, nearest first: a
 * face's board, a body's bought part, then the scopes and the module.
 */
export function describe(ref, layout) {
  const idx = indexLayout(layout);
  const kind = kindOf(ref, layout);
  const point = ref.point ?? anchorPoint(ref, layout);
  if (kind === 'gone') return { kind, path: ref.part, spellings: [ref.part], material: null, size: [], where: '', point, parents: [] };
  const item = { ...entry(idx, kind, ref.part), spellings: spellings(ref, layout), point };
  item.path = item.spellings[0];
  const parents = [];
  if (ref.face) {
    const part = idx.parts.get(ref.part);
    const axes = frameAxes(part, idx.frame);
    const fi = dir(idx.frame, ref.face).axis;
    const named = (ref.anchor ?? []).map(([w]) => dir(idx.frame, w).axis);
    item.size = kind === 'face' ? sizeIn(part.box, axes, AXES.filter((a) => a !== fi))
      : kind === 'edge' ? sizeIn(part.box, axes, AXES.filter((a) => a !== fi && !named.includes(a)))
      : [];
    if (kind === 'face' && ref.point) {
      item.offsets = edgeOffsets(part, idx.frame, ref.face, ref.point)
        .map((e) => [faceName(part, e.near[0]), Math.round(e.near[1])]);
    }
    parents.push(entry(idx, part.kind === 'slat' ? 'slat' : 'board', ref.part));
  } else if (idx.bodies.has(ref.part)) {
    parents.push(entry(idx, 'hardware', idx.bodies.get(ref.part).item.path));
  }
  const top = parents.length ? (idx.bodies.get(ref.part)?.item.path ?? ref.part) : ref.part;
  for (const a of ancestors(idx, top)) parents.push(entry(idx, a.kind, a.path));
  item.parents = parents;
  return item;
}

// -- snippets ------------------------------------------------------------------------

// A snippet: `text` is what a click copies (null for a note alone), `label`
// what it is, `note` a value it stands for.
const line = (text, label = null, note = null) => ({ text, label, note });

// A position on an axis inward from a face's plane, as a bare position: `left.bottom.position + 120`.
function inward(part, frame, world, mm) {
  const d = dir(frame, world);
  const base = `${part.path}.${faceName(part, world)}.position`;
  return mm === 0 ? base : `${base} ${d.sign > 0 ? '-' : '+'} ${num(mm)}`;
}

// What a point on a face can be written as: the anchor with its whole-millimetre distances from the
// two nearest edges, the same from the other edges, the corner of the two nearest, and with one axis
// centred on a position. A point named past the face's edges is taken on them.
function pointSnippets(part, layout, face, point) {
  const frame = indexLayout(layout).frame;
  const on = point.map((x, i) => Math.min(part.box.max[i], Math.max(part.box.min[i], x)));
  const [a, b] = edgeOffsets(part, frame, face, on);
  const r = (e) => [e[0], Math.round(e[1])];
  const at = (anchor) => spell({ part: part.path, face, anchor }, layout);
  return [
    line(at([r(a.near), r(b.near)]), 'point'),
    line(at([r(a.far), r(b.near)]), 'other edges'),
    line(at([r(a.near), r(b.far)]), 'other edges'),
    line(at([r(a.far), r(b.far)]), 'other edges'),
    line(at([[a.near[0], null], [b.near[0], null]]), 'nearest corner'),
    line(`${at([r(a.near)])}.center(${inward(part, frame, b.near[0], Math.round(b.near[1]))})`, 'centred on'),
    line(`${at([r(b.near)])}.center(${inward(part, frame, a.near[0], Math.round(a.near[1]))})`, 'centred on'),
  ];
}

// The snippets of one reference.
function ownSnippets(ref, layout) {
  const idx = indexLayout(layout);
  const kind = kindOf(ref, layout);
  const names = spellings(ref, layout).map((text) => line(text, kind));
  const part = idx.parts.get(ref.part);
  if (!part || !ref.face) return names;
  const frame = idx.frame;
  const name = names[0].text;
  const with_ = (anchor) => spell({ part: ref.part, face: ref.face, anchor }, layout);
  if (kind === 'face') {
    const out = [...names, line(`${name}.into(${MOVE})`, 'moved in'), line(`${name}.gap(${MOVE})`, 'moved out'),
      line(`${name}.center`, 'its middle'), line(`${name}.position`, 'its plane')];
    return ref.point ? [...out, ...pointSnippets(part, layout, ref.face, ref.point)] : out;
  }
  if (kind === 'edge') {
    const [edge] = ref.anchor;
    const k = AXES.find((a) => a !== dir(frame, ref.face).axis && a !== dir(frame, edge[0]).axis);
    return [...names, line(with_([[edge[0], MOVE]]), 'from it'),
      line(with_([edge, [worldName(frame, k, -1), null]]), 'corner'),
      line(with_([edge, [worldName(frame, k, 1), null]]), 'corner')];
  }
  if (kind === 'corner') {
    return [...names, line(with_(ref.anchor.map(([w]) => [w, MOVE])), 'from both')];
  }
  // a point: its names, then the variants of the point it names, but its own spelling
  const own = new Set(names.map((n) => n.text));
  return [...names, ...pointSnippets(part, layout, ref.face, anchorPoint(ref, layout)).filter((n) => !own.has(n.text))];
}

// A face's plane and the spelling it is written with.
function facePlane(ref, layout) {
  const idx = indexLayout(layout);
  const part = idx.parts.get(ref.part);
  const d = dir(idx.frame, ref.face);
  return { ...d, value: plane(part.box, d), name: spell({ part: ref.part, face: ref.face }, layout) };
}

// Two faces: on one axis, the distance, the midpoint, a distance from either side toward the other,
// and between(); else that they are not parallel.
function faceSnippets(a, b, layout) {
  const fa = facePlane(a, layout), fb = facePlane(b, layout);
  if (fa.axis !== fb.axis) return [line(null, 'not parallel', `${fa.name} and ${fb.name}: no distance between them`)];
  const [lo, hi] = fa.value <= fb.value ? [fa, fb] : [fb, fa];
  const toward = (f, other) => {
    if (other.value === f.value) return [];
    const out = (other.value - f.value) * f.sign > 0;
    return [line(`${f.name}.${out ? 'gap' : 'into'}(${APART})`, 'from one side')];
  };
  return [
    line(`${hi.name} - ${lo.name}`, 'distance', `${num(hi.value - lo.value)} mm`),
    line(`(${lo.name} + ${hi.name}) / 2`, 'midpoint'),
    ...toward(lo, hi), ...toward(hi, lo),
    line(`.between(${lo.name}, ${hi.name})`, 'between'),
  ];
}

// Two parts: between(), and per extent of the first's frame the gap between their boxes with the faces
// bounding it, or how far they overlap.
function partSnippets(a, b, layout) {
  const idx = indexLayout(layout);
  const pa = idx.parts.get(a.part), pb = idx.parts.get(b.part);
  const axes = frameAxes(pa, idx.frame);
  const out = [line(`.between(${a.part}, ${b.part})`, 'between')];
  for (const extent of EXTENTS) {
    const axis = axes[extent];
    if (!axis) continue;
    const i = AXIS[axis];
    const [first, second] = pa.box.max[i] <= pb.box.min[i] + 1e-9 ? [pa, pb] : pb.box.max[i] <= pa.box.min[i] + 1e-9 ? [pb, pa] : [null, null];
    if (!first) {
      const overlap = Math.min(pa.box.max[i], pb.box.max[i]) - Math.max(pa.box.min[i], pb.box.min[i]);
      out.push(line(null, extent, `they overlap by ${num(overlap)} mm`));
      continue;
    }
    const hiFace = spell({ part: second.path, face: worldName(idx.frame, axis, -1) }, layout);
    const loFace = spell({ part: first.path, face: worldName(idx.frame, axis, 1) }, layout);
    out.push(line(`${hiFace} - ${loFace}`, `${extent} gap`, `${num(second.box.min[i] - first.box.max[i])} mm`));
  }
  return out;
}

// Two points: their distances along each extent of the first's frame.
function pointDistances(a, b, layout) {
  const idx = indexLayout(layout);
  const p = a.point ?? anchorPoint(a, layout), q = b.point ?? anchorPoint(b, layout);
  const axes = axesAt(idx, a.part);
  return EXTENTS.filter((e) => axes[e]).map((e) => line(num(Math.abs(q[AXIS[axes[e]]] - p[AXIS[axes[e]]])), e, 'mm apart'));
}

const ANCHORS = ['corner', 'point'];
const PARTS = ['board', 'slat'];

/**
 * The snippets the panel offers for a selection (a list of references),
 * each `{text, label, note}`: `text` the code a click copies (null for a
 * note), `label` what it is, `note` the value it stands for. One item: its
 * names, and for a face moved in and out, its middle and plane and the
 * point clicked on it as anchors; for an edge a point a distance from it
 * and the corners at its ends; for a corner the distances from both edges;
 * for a point the variants. Two items: two faces' distance, midpoint,
 * distances from either side and between(), or that they are not
 * parallel; two parts' between() and gaps; two edges of one face the
 * corner; two corners or points their distances along each axis; a face
 * and a corner or point the distance from the face's plane. Several:
 * each one's names.
 */
export function snippets(refs, layout) {
  if (!refs.length) return [];
  if (refs.length === 1) return ownSnippets(refs[0], layout);
  const kinds = refs.map((r) => kindOf(r, layout));
  const names = () => refs.flatMap((r, k) => spellings(r, layout).map((text) => line(text, kinds[k])));
  if (refs.length > 2 || kinds.includes('gone')) return names();
  const [a, b] = refs, [ka, kb] = kinds;
  if (ka === 'face' && kb === 'face') return faceSnippets(a, b, layout);
  if (PARTS.includes(ka) && PARTS.includes(kb)) return partSnippets(a, b, layout);
  if (ka === 'edge' && kb === 'edge' && a.part === b.part && a.face === b.face) {
    const frame = indexLayout(layout).frame;
    if (dir(frame, a.anchor[0][0]).axis !== dir(frame, b.anchor[0][0]).axis) {
      return ownSnippets({ part: a.part, face: a.face, anchor: [a.anchor[0], b.anchor[0]] }, layout);
    }
  }
  if (ANCHORS.includes(ka) && ANCHORS.includes(kb)) return pointDistances(a, b, layout);
  if ((ka === 'face' && ANCHORS.includes(kb)) || (kb === 'face' && ANCHORS.includes(ka))) {
    const [face, anchor] = ka === 'face' ? [a, b] : [b, a];
    const f = facePlane(face, layout);
    const p = anchor.point ?? anchorPoint(anchor, layout);
    return [line(num(Math.abs(p[f.i] - f.value)), `from ${f.name}`, 'mm from its plane')];
  }
  return names();
}
