// The selection's references (refs.js): what a click names on a board in
// each orientation, at the tolerance, in both spellings; references read
// back from their spellings; the items the panel lists; the snippets.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { TOLERANCE, MOVE, APART, num, frameAxes, sizeIn, sizeText, indexLayout, kindOf, spell, spellings, parseRef, faceAt, edgeOffsets, pick, anchorPoint, edgeEnds, nameAt, describe, snippets } from '../refs.js';

// The world frame of the examples, and a cabinet in it that opens toward
// world right (+y), as examples/drawer_cabinet.py builds it: its front is
// world right, its left world back (+x).
const frame = { front: '-x', back: '+x', left: '-y', right: '+y', top: '+z', bottom: '-z' };
const cabinet = (inner) => ({ right: ['front'], left: ['back'], back: ['left'], front: ['right'], top: ['top'], bottom: ['bottom'], ...inner });
const board = (path, t, min, max, faces, extra = {}) => ({
  path, kind: 'board', material: 'birch 15', axes: { t, u: t === 'x' ? 'y' : 'x', v: t === 'z' ? 'y' : 'z' },
  box: { min, max }, faces, where: `examples/cab.py:${10 + path.length}`, ...extra });

const left = board('kitchen.left', 'x', [585, 0, 0], [600, 500, 720], cabinet({ back: ['left', 'outer'], front: ['right', 'inner'] }));
const right = board('kitchen.right', 'x', [0, 0, 0], [15, 500, 720], cabinet({ back: ['left', 'inner'], front: ['right', 'outer'] }));
const bottom = board('kitchen.bottom', 'z', [15, 0, 100], [585, 500, 115], cabinet({ top: ['top', 'inner'], bottom: ['bottom', 'outer'] }));
const top = board('kitchen.top', 'z', [15, 0, 705], [585, 500, 720], cabinet({ top: ['top', 'outer'], bottom: ['bottom', 'inner'] }));
const back = board('kitchen.back', 'y', [15, 0, 115], [585, 9, 705], cabinet({ right: ['front', 'inner'], left: ['back', 'outer'] }), { material: 'birch 9' });
const face = board('kitchen.drawer1.face', 'y', [18, 485, 118], [582, 500, 345], cabinet({ right: ['front', 'outer'], left: ['back', 'inner'] }));
const runners = { path: 'kitchen.drawer1.runners', kind: 'hardware', name: 'runners', where: 'examples/cab.py:83',
  bodies: [{ name: 'left', boxes: [{ min: [564, 45, 140], max: [576, 485, 160] }] },
           { name: 'right', boxes: [{ min: [24, 45, 140], max: [36, 485, 160] }] }] };
// A module written mirrored (examples/slats.py's unit): its left is world right.
const unitTop = board('unit.top', 'z', [0, 0, 785], [320, 620, 800],
  { front: ['front'], back: ['back'], right: ['left'], left: ['right'], top: ['top', 'outer'], bottom: ['bottom', 'inner'] });
const rail = { ...board('bed.rail', 'y', [0, 800, 0], [2000, 840, 60],
  { front: ['front'], back: ['back'], left: ['left', 'outer'], right: ['right', 'inner'], top: ['top'], bottom: ['bottom'] }), kind: 'slat', section: [40, 60] };

const layout = {
  version: 10, frame,
  modules: [
    { path: 'kitchen', where: 'examples/cab.py:97', box: { min: [0, 0, 0], max: [600, 500, 720] },
      parts: [left, right, bottom, top, back, face], hardware: [runners] },
    { path: 'unit', where: 'examples/slats.py:20', box: { min: [0, 0, 0], max: [320, 620, 800] }, parts: [unitTop], hardware: [] },
    { path: 'bed', where: 'examples/slats.py:40', box: { min: [0, 800, 0], max: [2000, 2200, 100] }, parts: [rail], hardware: [] },
  ],
};

const texts = (lines) => lines.map((l) => l.text);

test('numbers as a snippet writes them', () => {
  assert.equal(num(37), '37');
  assert.equal(num(227.5), '227.5');
  assert.equal(num(1 / 3), '0.33');
  assert.equal(num(-0.001), '0');
});

test('a part\'s extents in its scope\'s frame, as the build file names them', () => {
  assert.deepEqual(frameAxes(left, frame), { width: 'x', depth: 'y', height: 'z' });
  assert.deepEqual(sizeIn(left.box, frameAxes(left, frame)), [['width', 15], ['depth', 500], ['height', 720]]);
  assert.deepEqual(sizeIn(left.box, frameAxes(left, frame), ['y', 'z']), [['depth', 500], ['height', 720]]);
  assert.equal(sizeText(sizeIn(bottom.box, frameAxes(bottom, frame))), 'width 570, depth 500, height 15');
  // without a part, the world frame's own: world front is -x, so depth runs along x
  assert.deepEqual(frameAxes(null, frame), { width: 'y', depth: 'x', height: 'z' });
  // a mirrored module keeps its width along y
  assert.deepEqual(frameAxes(unitTop, frame), { width: 'y', depth: 'x', height: 'z' });
});

test('the layout\'s things by path, once per layout', () => {
  const idx = indexLayout(layout);
  assert.equal(indexLayout(layout), idx);
  assert.deepEqual([...idx.scopes].sort(), ['kitchen.drawer1']);
  assert.ok(idx.bodies.has('kitchen.drawer1.runners.left'));
  assert.equal(kindOf({ part: 'kitchen.left' }, layout), 'board');
  assert.equal(kindOf({ part: 'bed.rail' }, layout), 'slat');
  assert.equal(kindOf({ part: 'kitchen.drawer1.runners.left' }, layout), 'hardware');
  assert.equal(kindOf({ part: 'kitchen.drawer1.runners' }, layout), 'hardware');
  assert.equal(kindOf({ part: 'kitchen.drawer1' }, layout), 'scope');
  assert.equal(kindOf({ part: 'kitchen' }, layout), 'module');
  assert.equal(kindOf({ part: 'kitchen.gone' }, layout), 'gone');
  assert.equal(kindOf({ part: 'kitchen.gone', face: 'front' }, layout), 'gone');
});

test('a click inside a face names the face, in both spellings, and keeps the point', () => {
  const ref = pick(left, frame, { point: [585, 250, 360], normal: [-1, 0, 0] }, { scale: 1 });
  assert.deepEqual(ref, { part: 'kitchen.left', face: 'front', anchor: [], point: [585, 250, 360] });
  assert.equal(kindOf(ref, layout), 'face');
  assert.deepEqual(spellings(ref, layout), ['kitchen.left.inner', 'kitchen.left.right']);
  // the outer face, and a face without inner or outer
  assert.deepEqual(spellings(pick(left, frame, { point: [600, 250, 360], normal: [1, 0, 0] }, { scale: 1 }), layout),
    ['kitchen.left.outer', 'kitchen.left.left']);
  assert.deepEqual(spellings(pick(left, frame, { point: [592, 250, 720], normal: [0, 0, 1] }, { scale: 1 }), layout),
    ['kitchen.left.top']);
});

test('a board in each orientation names its big faces', () => {
  // lying flat: its top is its inner face
  const flat = pick(bottom, frame, { point: [300, 250, 115], normal: [0, 0, 1] }, { scale: 1 });
  assert.deepEqual(spellings(flat, layout), ['kitchen.bottom.inner', 'kitchen.bottom.top']);
  assert.deepEqual(spellings(pick(top, frame, { point: [300, 250, 705], normal: [0, 0, -1] }, { scale: 1 }), layout),
    ['kitchen.top.inner', 'kitchen.top.bottom']);
  // standing across the depth: its inner face is toward the cabinet's front, world right
  assert.deepEqual(spellings(pick(back, frame, { point: [300, 9, 400], normal: [0, 1, 0] }, { scale: 1 }), layout),
    ['kitchen.back.inner', 'kitchen.back.front']);
  // standing across the width
  assert.deepEqual(spellings(pick(right, frame, { point: [15, 250, 400], normal: [1, 0, 0] }, { scale: 1 }), layout),
    ['kitchen.right.inner', 'kitchen.right.left']);
  // a slat along the width
  assert.deepEqual(spellings(pick(rail, frame, { point: [1000, 840, 30], normal: [0, 1, 0] }, { scale: 1 }), layout),
    ['bed.rail.inner', 'bed.rail.right']);
});

test('near an edge a click names the edge, within the tolerance in screen pixels', () => {
  // 3 mm from the cabinet's front (world +y), at 1 mm a pixel: 3 px
  const ref = pick(left, frame, { point: [585, 497, 360], normal: [-1, 0, 0] }, { scale: 1 });
  assert.deepEqual(ref.anchor, [['right', null]]);
  assert.equal(kindOf(ref, layout), 'edge');
  assert.deepEqual(spellings(ref, layout), ['kitchen.left.inner.front', 'kitchen.left.right.front']);
  // the same 3 mm at 0.4 mm a pixel are 7.5 px: the face
  assert.deepEqual(pick(left, frame, { point: [585, 497, 360], normal: [-1, 0, 0] }, { scale: 0.4 }).anchor, []);
  // exactly at the tolerance, and just past it
  assert.equal(pick(left, frame, { point: [585, 500 - TOLERANCE, 360], normal: [-1, 0, 0] }, { scale: 1 }).anchor.length, 1);
  assert.equal(pick(left, frame, { point: [585, 500 - TOLERANCE - 0.1, 360], normal: [-1, 0, 0] }, { scale: 1 }).anchor.length, 0);
  // a tolerance of its own
  assert.equal(pick(left, frame, { point: [585, 490, 360], normal: [-1, 0, 0] }, { scale: 1, tolerance: 12 }).anchor.length, 1);
});

test('a distance seen at a slant counts as it shows on the screen', () => {
  const point = [585, 481, 360];      // 19 mm from the front edge
  assert.equal(pick(left, frame, { point, normal: [-1, 0, 0] }, { scale: 1 }).anchor.length, 0);
  // looking nearly along the depth, 19 mm show as 19 * 0.31 px
  const view = [Math.sqrt(1 - 0.95 ** 2), -0.95, 0];
  assert.deepEqual(pick(left, frame, { point, normal: [-1, 0, 0] }, { scale: 1, view }).anchor, [['right', null]]);
  // across the line of sight they show whole
  assert.equal(pick(left, frame, { point, normal: [-1, 0, 0] }, { scale: 1, view: [-1, 0, 0] }).anchor.length, 0);
});

test('where two edges are within the tolerance a click names the corner, the nearer edge first', () => {
  const ref = pick(left, frame, { point: [585, 497, 2], normal: [-1, 0, 0] }, { scale: 1 });
  assert.deepEqual(ref.anchor, [['bottom', null], ['right', null]]);
  assert.equal(kindOf(ref, layout), 'corner');
  assert.deepEqual(spellings(ref, layout), ['kitchen.left.inner.bottom.front', 'kitchen.left.right.bottom.front']);
  const other = pick(left, frame, { point: [585, 498, 4], normal: [-1, 0, 0] }, { scale: 1 });
  assert.deepEqual(spellings(other, layout)[0], 'kitchen.left.inner.front.bottom');
  // a narrow face's edge with a big face takes inner or outer too; only the nearer edge of an axis counts
  const narrow = pick(left, frame, { point: [592, 250, 720], normal: [0, 0, 1] }, { scale: 2 });
  assert.deepEqual(narrow.anchor, [['front', null]]);
  assert.deepEqual(spellings(narrow, layout), ['kitchen.left.top.inner', 'kitchen.left.top.right']);
  // in a mirrored module, world right is the module's left
  const mirrored = pick(unitTop, frame, { point: [160, 618, 800], normal: [0, 0, 1] }, { scale: 1 });
  assert.deepEqual(spellings(mirrored, layout), ['unit.top.outer.left', 'unit.top.top.left']);
});

test('a hit off the faces of the part\'s box names the part, with the point', () => {
  // up in a toe kick notch, 50 above the board's bottom
  assert.deepEqual(pick(left, frame, { point: [592, 30, 50], normal: [0, 0, -1] }, { scale: 1 }),
    { part: 'kitchen.left', point: [592, 30, 50] });
  // a slanted face
  assert.equal(faceAt(left, frame, [585, 250, 360], [-0.7, 0.7, 0]), null);
  // without a normal, the nearest plane
  assert.equal(faceAt(left, frame, [590, 250, 360]), 'front');
  // a pocket's floor 2 mm in counts as the face at a coarse zoom only
  assert.equal(faceAt(left, frame, [587, 250, 360], [-1, 0, 0], 0.5), null);
  assert.equal(pick(left, frame, { point: [587, 250, 360], normal: [-1, 0, 0] }, { scale: 2 }).face, 'front');
});

test('a face\'s edges around a point, nearer first, and the point it names', () => {
  assert.deepEqual(edgeOffsets(left, frame, 'front', [585, 463, 120]), [
    { i: 1, near: ['right', 37], far: ['left', 463] },
    { i: 2, near: ['bottom', 120], far: ['top', 600] },
  ]);
  assert.deepEqual(anchorPoint({ part: 'kitchen.left', face: 'front', anchor: [['right', 37], ['bottom', 120]] }, layout), [585, 463, 120]);
  assert.deepEqual(anchorPoint({ part: 'kitchen.left', face: 'front', anchor: [['right', null]] }, layout), [585, 500, 360]);
  assert.deepEqual(anchorPoint({ part: 'kitchen.left', face: 'front', anchor: [] }, layout), [585, 250, 360]);
  assert.deepEqual(edgeEnds({ part: 'kitchen.left', face: 'front', anchor: [['right', null]] }, layout), [[585, 500, 0], [585, 500, 720]]);
  assert.deepEqual(edgeEnds({ part: 'kitchen.bottom', face: 'top', anchor: [['back', null]] }, layout), [[585, 0, 115], [585, 500, 115]]);
  assert.deepEqual(anchorPoint({ part: 'kitchen.left' }, layout), [592.5, 250, 360]);
  assert.deepEqual(anchorPoint({ part: 'kitchen' }, layout), [300, 250, 360]);
  assert.deepEqual(anchorPoint({ part: 'kitchen.drawer1.runners.left' }, layout), [570, 265, 150]);
});

test('references read back from their spellings', () => {
  for (const ref of [
    { part: 'kitchen.left', face: 'front', anchor: [] },
    { part: 'kitchen.left', face: 'front', anchor: [['right', null]] },
    { part: 'kitchen.left', face: 'front', anchor: [['bottom', null], ['right', null]] },
    { part: 'kitchen.left', face: 'front', anchor: [['right', 37], ['bottom', 120.5]] },
    { part: 'kitchen.left', face: 'top', anchor: [['front', null]] },
    { part: 'unit.top', face: 'top', anchor: [['right', null]] },
  ]) {
    for (const text of spellings(ref, layout)) assert.deepEqual(parseRef(text, layout), ref, text);
  }
  assert.deepEqual(parseRef('kitchen.left', layout), { part: 'kitchen.left' });
  assert.deepEqual(parseRef(' kitchen.drawer1 ', layout), { part: 'kitchen.drawer1' });
  assert.deepEqual(parseRef('kitchen.drawer1.runners.left', layout), { part: 'kitchen.drawer1.runners.left' });
  assert.deepEqual(parseRef('kitchen.drawer1.face.outer', layout), { part: 'kitchen.drawer1.face', face: 'right', anchor: [] });
  assert.deepEqual(parseRef('kitchen.left.inner.front(37)', layout), { part: 'kitchen.left', face: 'front', anchor: [['right', 37]] });
  const center = parseRef('kitchen.left.inner.center', layout);
  assert.deepEqual(center, { part: 'kitchen.left', face: 'front', anchor: [], center: true });
  assert.equal(kindOf(center, layout), 'point');
  assert.equal(spell(center, layout), 'kitchen.left.inner.center');
  assert.equal(kindOf(parseRef('kitchen.left.inner.front(37).bottom', layout), layout), 'point');
});

test('a reference that names nothing is refused, saying why', () => {
  assert.throws(() => parseRef('pantry.left', layout), /no part, bought part, scope or module/);
  assert.throws(() => parseRef('kitchen.left.sideways', layout), /no face sideways; its faces are .*inner/);
  assert.throws(() => parseRef('kitchen.left.inner.outer', layout), /not an edge here/);
  assert.throws(() => parseRef('kitchen.left.inner.front.back', layout), /not an edge here/);
  assert.throws(() => parseRef('kitchen.left.inner(3)', layout), /a face takes no distance/);
  assert.throws(() => parseRef('kitchen.left.inner.front(a)', layout), /takes a distance in mm/);
  assert.throws(() => parseRef('kitchen.left.inner.front()', layout), /takes a distance in mm/);
  assert.throws(() => parseRef('kitchen.drawer1.runners.left.top', layout), /is a hardware: it has no faces/);
  assert.throws(() => parseRef('kitchen.drawer1.inner', layout), /is a scope: it has no faces/);
});

test('a world point named: its face, nearest edge and corner, and the anchor with offsets', () => {
  assert.deepEqual(nameAt(layout, [585, 463, 120]), {
    part: 'kitchen.left', point: [585, 463, 120],
    face: ['kitchen.left.inner', 'kitchen.left.right'],
    edge: { spellings: ['kitchen.left.inner.front', 'kitchen.left.right.front'], mm: 37 },
    corner: ['kitchen.left.inner.front.bottom', 'kitchen.left.right.front.bottom'],
    anchor: ['kitchen.left.inner.front(37).bottom(120)', 'kitchen.left.right.front(37).bottom(120)'],
  });
  // inside the board: the nearest face, and how far off its plane the point is
  const inside = nameAt(layout, [590, 463.4, 120]);
  assert.equal(inside.off, 5);
  assert.deepEqual(inside.point, [585, 463.4, 120]);
  assert.equal(inside.anchor[0], 'kitchen.left.inner.front(37).bottom(120)');
  // a part named
  assert.equal(nameAt(layout, [300, 250, 110], 'kitchen.bottom').face[0], 'kitchen.bottom.inner');
  assert.throws(() => nameAt(layout, [5000, 0, 0]), /no part at/);
  assert.throws(() => nameAt(layout, [0, 0, 0], 'kitchen.none'), /no part kitchen.none/);
});

test('the panel\'s items: what each is, its size and line, and what it belongs to', () => {
  const faceItem = describe({ part: 'kitchen.left', face: 'front', anchor: [], point: [585, 463, 120] }, layout);
  assert.equal(faceItem.kind, 'face');
  assert.equal(faceItem.path, 'kitchen.left.inner');
  assert.deepEqual(faceItem.spellings, ['kitchen.left.inner', 'kitchen.left.right']);
  assert.deepEqual(faceItem.size, [['depth', 500], ['height', 720]]);
  assert.deepEqual(faceItem.offsets, [['front', 37], ['bottom', 120]]);
  assert.deepEqual(faceItem.point, [585, 463, 120]);
  assert.deepEqual(faceItem.parents.map((p) => [p.kind, p.path, p.material, sizeText(p.size), p.where]), [
    ['board', 'kitchen.left', 'birch 15', 'width 15, depth 500, height 720', left.where],
    ['module', 'kitchen', null, 'width 600, depth 500, height 720', 'examples/cab.py:97'],
  ]);
  assert.deepEqual(describe({ part: 'kitchen.left', face: 'front', anchor: [['right', null]] }, layout).size, [['height', 720]]);
  assert.deepEqual(describe({ part: 'kitchen.left', face: 'front', anchor: [['right', null]] }, layout).point, [585, 500, 360]);
  assert.deepEqual(describe({ part: 'kitchen.left', face: 'front', anchor: [['right', null], ['bottom', null]] }, layout).size, []);

  const boardItem = describe({ part: 'kitchen.drawer1.face' }, layout);
  assert.deepEqual([boardItem.kind, boardItem.path, boardItem.material, sizeText(boardItem.size), boardItem.where],
    ['board', 'kitchen.drawer1.face', 'birch 15', 'width 564, depth 15, height 227', face.where]);
  assert.deepEqual(boardItem.parents.map((p) => [p.kind, p.path, sizeText(p.size)]), [
    ['scope', 'kitchen.drawer1', 'width 564, depth 455, height 227'],
    ['module', 'kitchen', 'width 600, depth 500, height 720'],
  ]);
  const body = describe({ part: 'kitchen.drawer1.runners.left' }, layout);
  assert.deepEqual([body.kind, body.material, sizeText(body.size), body.where],
    ['hardware', null, 'width 12, depth 440, height 20', runners.where]);
  assert.deepEqual(body.parents.map((p) => [p.kind, p.path]),
    [['hardware', 'kitchen.drawer1.runners'], ['scope', 'kitchen.drawer1'], ['module', 'kitchen']]);
  assert.deepEqual(describe({ part: 'kitchen' }, layout).parents, []);
  assert.equal(describe({ part: 'bed.rail' }, layout).kind, 'slat');
  assert.deepEqual(describe({ part: 'kitchen.gone' }, layout), { kind: 'gone', path: 'kitchen.gone', spellings: ['kitchen.gone'],
    material: null, size: [], where: '', point: null, parents: [] });
});

test('a face\'s snippets: its names, moved, its middle and plane, and the point clicked on it', () => {
  const ref = { part: 'kitchen.left', face: 'front', anchor: [], point: [585, 463, 120] };
  assert.deepEqual(texts(snippets([ref], layout)), [
    'kitchen.left.inner', 'kitchen.left.right',
    `kitchen.left.inner.into(${MOVE})`, `kitchen.left.inner.gap(${MOVE})`, 'kitchen.left.inner.center', 'kitchen.left.inner.position',
    'kitchen.left.inner.front(37).bottom(120)',
    'kitchen.left.inner.back(463).bottom(120)',
    'kitchen.left.inner.front(37).top(600)',
    'kitchen.left.inner.back(463).top(600)',
    'kitchen.left.inner.front.bottom',
    'kitchen.left.inner.front(37).center(kitchen.left.bottom.position + 120)',
    'kitchen.left.inner.bottom(120).center(kitchen.left.front.position - 37)',
  ]);
  // without a point clicked, none of the point's
  assert.equal(snippets([{ part: 'kitchen.left', face: 'front', anchor: [] }], layout).length, 6);
  // the offsets are whole millimetres
  assert.equal(texts(snippets([{ ...ref, point: [585, 463.4, 119.6] }], layout))[6], 'kitchen.left.inner.front(37).bottom(120)');
});

test('an edge\'s snippets: its names, a point a distance from it, the corners at its ends', () => {
  assert.deepEqual(texts(snippets([{ part: 'kitchen.left', face: 'front', anchor: [['right', null]], point: [585, 498, 300] }], layout)), [
    'kitchen.left.inner.front', 'kitchen.left.right.front', `kitchen.left.inner.front(${MOVE})`,
    'kitchen.left.inner.front.bottom', 'kitchen.left.inner.front.top',
  ]);
  assert.deepEqual(snippets([{ part: 'kitchen.left', face: 'front', anchor: [['right', null]] }], layout)[0].label, 'edge');
});

test('a corner\'s snippets, and a point\'s variants', () => {
  assert.deepEqual(texts(snippets([{ part: 'kitchen.left', face: 'front', anchor: [['right', null], ['bottom', null]] }], layout)), [
    'kitchen.left.inner.front.bottom', 'kitchen.left.right.front.bottom', `kitchen.left.inner.front(${MOVE}).bottom(${MOVE})`,
  ]);
  const point = texts(snippets([parseRef('kitchen.left.inner.front(37).bottom(120)', layout)], layout));
  assert.deepEqual(point, [
    'kitchen.left.inner.front(37).bottom(120)', 'kitchen.left.right.front(37).bottom(120)',
    'kitchen.left.inner.back(463).bottom(120)', 'kitchen.left.inner.front(37).top(600)', 'kitchen.left.inner.back(463).top(600)',
    'kitchen.left.inner.front.bottom',
    'kitchen.left.inner.front(37).center(kitchen.left.bottom.position + 120)',
    'kitchen.left.inner.bottom(120).center(kitchen.left.front.position - 37)',
  ]);
  // a point named past its face's edges is taken on them
  assert.deepEqual(texts(snippets([parseRef('kitchen.left.top.inner(20).back(100)', layout)], layout)).slice(2, 4),
    ['kitchen.left.top.outer(0).back(100)', 'kitchen.left.top.inner(15).back(100)']);
  // a part or a bought part: its path
  assert.deepEqual(texts(snippets([{ part: 'kitchen.drawer1.runners.left' }], layout)), ['kitchen.drawer1.runners.left']);
  assert.deepEqual(snippets([], layout), []);
});

test('two parallel faces: the distance, the midpoint, a distance from either side, between()', () => {
  const a = { part: 'kitchen.bottom', face: 'top', anchor: [] }, b = { part: 'kitchen.top', face: 'bottom', anchor: [] };
  const lines = snippets([b, a], layout);
  assert.deepEqual(texts(lines), [
    'kitchen.top.inner - kitchen.bottom.inner', '(kitchen.bottom.inner + kitchen.top.inner) / 2',
    `kitchen.bottom.inner.gap(${APART})`, `kitchen.top.inner.gap(${APART})`,
    '.between(kitchen.bottom.inner, kitchen.top.inner)',
  ]);
  assert.equal(lines[0].note, '590 mm');
  assert.deepEqual(lines.map((l) => l.label), ['distance', 'midpoint', 'from one side', 'from one side', 'between']);
  // facing the same way, the far one moves into its board toward the other
  const c = { part: 'kitchen.top', face: 'top', anchor: [] };
  assert.deepEqual(texts(snippets([a, c], layout)).slice(2, 4), [`kitchen.bottom.inner.gap(${APART})`, `kitchen.top.outer.into(${APART})`]);
  // faces not parallel are said to be so, with nothing to copy
  const across = snippets([a, { part: 'kitchen.left', face: 'front', anchor: [] }], layout);
  assert.deepEqual(across.map((l) => [l.text, l.label]), [[null, 'not parallel']]);
  assert.match(across[0].note, /kitchen.bottom.inner and kitchen.left.inner/);
});

test('two parts: between(), and the gap along each extent with the faces bounding it', () => {
  const lines = snippets([{ part: 'kitchen.left' }, { part: 'kitchen.right' }], layout);
  assert.deepEqual(lines.map((l) => [l.text, l.label, l.note]), [
    ['.between(kitchen.left, kitchen.right)', 'between', null],
    ['kitchen.left.inner - kitchen.right.inner', 'width gap', '570 mm'],
    [null, 'depth', 'they overlap by 500 mm'],
    [null, 'height', 'they overlap by 720 mm'],
  ]);
  const stacked = snippets([{ part: 'kitchen.top' }, { part: 'kitchen.bottom' }], layout);
  assert.deepEqual(stacked[3].text, 'kitchen.top.inner - kitchen.bottom.inner');
  assert.equal(stacked[3].note, '590 mm');
});

test('two edges of one face make a corner; anchors their distances; a face and an anchor the distance from its plane', () => {
  const front = { part: 'kitchen.left', face: 'front', anchor: [['right', null]] };
  const low = { part: 'kitchen.left', face: 'front', anchor: [['bottom', null]] };
  assert.equal(snippets([front, low], layout)[0].text, 'kitchen.left.inner.front.bottom');
  const c1 = { part: 'kitchen.left', face: 'front', anchor: [['right', null], ['bottom', null]] };
  const c2 = parseRef('kitchen.right.inner.back(20).top(30)', layout);
  assert.deepEqual(snippets([c1, c2], layout).map((l) => [l.label, l.text]), [['width', '570'], ['depth', '480'], ['height', '690']]);
  const shelf = { part: 'kitchen.bottom', face: 'top', anchor: [] };
  assert.deepEqual(snippets([shelf, c2], layout).map((l) => [l.text, l.label]), [['575', 'from kitchen.bottom.inner']]);
  // what relates nothing: each one's names
  assert.deepEqual(texts(snippets([front, { part: 'kitchen.top' }], layout)),
    ['kitchen.left.inner.front', 'kitchen.left.right.front', 'kitchen.top']);
  assert.deepEqual(texts(snippets([{ part: 'kitchen.top' }, { part: 'kitchen.left' }, { part: 'kitchen' }], layout)),
    ['kitchen.top', 'kitchen.left', 'kitchen']);
});
