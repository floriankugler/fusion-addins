// The nest view's CAM layer (cam.js): the plan's state, the legend and its
// order, the operation chosen, the release order and what is drawn.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { CAM_VERSION, planVersionProblem, when, planStatusText, toolName, toolColors, setupLabel, legend, chosenOperation,
  highlighted, releaseRanks, releaseList, holdText, partText, releaseColors, featureShapes, toDrawing, tabPositions,
  setupOverlay, planNotes } from '../cam.js';

const mill = (diameter) => ({ type: 'flat end mill', diameter, flute: 20, taper: null, tip: 0 });
const vbit = { type: 'chamfer mill', diameter: 6, flute: 4.24, taper: 45, tip: 0 };
const params = (tabs = null) => ({ top: { mode: 'from stock top', offset: 0 }, bottom: { mode: 'from stock bottom', offset: 0.2 },
  multiple_depths: null, stepdowns: null, preserve_order: false, feed_scale: null, tabs });
const ref = (index, aspect = 'op', name = null, kind = 'hole') => ({ index, name, kind, aspect });
const op = (name, kind, tool, features, tabs = null) => ({ name, kind, template: 't', label: 'l', tool, params: params(tabs), features });

const square = (x, y, s) => [[x, y], [x + s, y], [x + s, y + s], [x, y + s]];
const TABS = { width: 5, height: 2, positions: [[10, 50], [110, 50]] };

// Two setups: a blank with a part A (an inner contour, tabs) and a part B, on sheet 1; an own blank on sheet 2.
const PLAN = {
  version: 1, nest: 'm.ply', nest_written: '2026-10-17T11:30:50+02:00', layout_hash: 'h', written: '2026-10-17T11:31:04+02:00',
  settings: {}, problems: ['m.ply birch 15 1.1: m.a: a 2 mm hole is drilled', 'check: m.b: a ring is cut twice'],
  setups: [
    {
      name: 'm.ply birch 15 1.1',
      stock: { material: 'birch 15', sheet: '1', blank: '1.1', rect: [20, 30, 600, 400], thickness: 15, own_blank: false },
      parts: [{ path: 'm.a', hold: 950.4, tab_policy: 'auto', tabs: 2 }, { path: 'm.b', hold: 42.25, tab_policy: 'forced', tabs: 0 }],
      operations: [
        op('8 mm: pockets (Tasche adaptiv 8mm)', 'pocket', mill(8), [
          { what: 'pocket', part: 'm.a', ops: [ref(2, 'op', 'recess', 'pocket')], rings: [square(20, 20, 60), square(40, 40, 10)], depth: 5, slot: null },
          { what: 'rest', part: 'm.a', ops: [ref(2, 'op', 'recess', 'pocket')], rings: [square(20, 20, 4)], depth: 5, slot: null }]),
        op('6 mm: contours, roughing (Kontur 6mm)', 'contour', mill(6), [
          { what: 'inner', part: 'm.a', ops: [ref(-1, 'ring 1', null, 'outline')], ring: square(60, 60, 20).reverse() },
          { what: 'outer', part: 'm.a', ops: [ref(-1, 'ring 0', null, 'outline')], ring: square(10, 10, 100) }], TABS),
        op('6 mm: contours, roughing (Kontur 6mm)', 'contour', mill(6), [
          { what: 'outer', part: 'm.b', ops: [ref(-1, 'ring 0', null, 'outline')], ring: square(200, 10, 50) }]),
        op('3.175 mm: dog bones (Dogbone 3.175mm)', 'dogbone', mill(3.175), [
          { what: 'dogbone', part: 'm.a', ops: [ref(3, 'relief 0', 'slot', 'cut')], center: [30, 30], d: 3.3, tool: 3.175, depth: null,
            arc: [[31.65, 30], [30, 31.65], [28.35, 30]] }]),
        op('2 mm: drills (Bohrung exakt 2mm)', 'drill', mill(2), [
          { what: 'hole', part: 'm.a', ops: [ref(1)], center: [90, 90], d: 2, depth: 4 }]),
        op('chamfers (Fase 90°)', 'chamfer', vbit, [
          { what: 'chamfer', part: 'm.b', ops: [ref(-1, 'chamfer', null, 'outline')], size: 1,
            paths: [{ points: square(200, 10, 50), closed: true }, { points: [[200, 10], [250, 10]], closed: false }], hole: null },
          { what: 'chamfer', part: 'm.b', ops: [ref(4, 'chamfer')], size: 0.5, paths: [], hole: { center: [225, 35], d: 8 } }]),
        op('V-grooves (Gravur 90°)', 'groove', vbit, [
          { what: 'vgroove', part: 'm.b', ops: [ref(5, 'op', 'mark', 'vgroove')], start: [210, 61], end: [210, 56], depth: 0.3 }]),
        op('6 mm: release (Kontur 6mm)', 'release', mill(6), [
          { what: 'outer', part: 'm.b', ops: [ref(-1, 'ring 0', null, 'outline')], ring: square(200, 10, 50) },
          { what: 'inner', part: 'm.a', ops: [ref(-1, 'ring 1', null, 'outline')], ring: square(60, 60, 20).reverse() },
          { what: 'outer', part: 'm.a', ops: [ref(-1, 'ring 0', null, 'outline')], ring: square(10, 10, 100) }], TABS),
      ],
      release_order: [{ part: 'm.b', what: 'outer', ring: 0, tool: 6 }, { part: 'm.a', what: 'inner', ring: 1, tool: 6 },
        { part: 'm.a', what: 'outer', ring: 0, tool: 6 }],
      left_out: [
        { part: 'm.a', op: ref(6, 'op', 'groove_floor', 'pocket'), why: 'other face', note: '' },
        { part: 'm.a', op: ref(6, 'relief 0', 'groove_floor', 'pocket'), why: 'other face', note: '' },
        { part: 'm.a', op: ref(6, 'relief 1', 'groove_floor', 'pocket'), why: 'other face', note: '' },
        { part: 'm.a', op: ref(7, 'op', null, 'edge'), why: 'narrow face', note: '' },
        { part: 'm.b', op: ref(8, 'op', 'pilot', 'hole'), why: 'nothing fits', note: 'no drill of 1.5 mm' }],
      problems: ['m.a: a 2 mm hole is drilled'],
    },
    {
      name: 'm.ply birch 15 2.1',
      stock: { material: 'birch 15', sheet: '2', blank: '2.1', rect: [0, 0, 300, 200], thickness: 15, own_blank: true },
      parts: [{ path: 'm.top', hold: 3000, tab_policy: 'auto', tabs: 0 }],
      operations: [op('5 mm: bores (Bohrung 5mm)', 'bore', mill(5), [
        { what: 'hole', part: 'm.top', ops: [ref(0)], center: [50, 50], d: 8, depth: null }])],
      release_order: [],
      left_out: [{ part: 'm.top', op: ref(-1, 'ring 0', null, 'outline'), why: 'hand work', note: '' }],
      problems: [],
    },
  ],
};

test('the plan version the page reads', () => {
  assert.equal(CAM_VERSION, 1);
  assert.equal(planVersionProblem(PLAN), null);
  assert.equal(planVersionProblem({ version: 2 }), 'plan version 2, this viewer reads 1');
  assert.equal(planVersionProblem(null), 'plan version missing, this viewer reads 1');
});

test('the plan state as the side panel says it', () => {
  assert.equal(when('2026-10-17T11:31:04+02:00'), '2026-10-17 11:31:04');
  assert.equal(when('2026-10-17T09:31:04Z'), '2026-10-17 09:31:04');
  assert.equal(planStatusText({ state: 'ok', written: '2026-10-17T11:31:04+02:00', nest_written: '2026-10-17T11:30:50+02:00' }),
    'planned 2026-10-17 11:31:04, for this nest');
  assert.equal(planStatusText({ state: 'stale', why: 'planned for the nest written x, the nest beside it was written y' }),
    'stale: planned for the nest written x, the nest beside it was written y: plan again');
  assert.equal(planStatusText({ state: 'running' }), 'planning…');
  assert.equal(planStatusText({ state: 'failed', log: 'error: boom\n' }), 'the plan failed:\nerror: boom');
  assert.match(planStatusText({ state: 'none' }), /not planned yet/);
  assert.match(planStatusText(undefined), /not planned yet/);
});

test('tools by name and colour, the widest first and the V-bit last', () => {
  assert.equal(toolName({ tool: mill(6) }), '6 mm');
  assert.equal(toolName({ tool: mill(3.175) }), '3.175 mm');
  assert.equal(toolName({ tool: vbit }), 'V-bit 90°');
  assert.equal(toolName({ tool: { type: 'drill', diameter: 2, taper: null } }), 'drill 2 mm');
  const colors = toolColors(PLAN);
  assert.deepEqual([...colors.keys()], ['8 mm', '6 mm', '5 mm', '3.175 mm', '2 mm', 'V-bit 90°']);
  assert.equal(new Set(colors.values()).size, 6);
  assert.deepEqual([...toolColors({ setups: [] })], []);
});

test('the legend lists each setup\'s operations in the order they run', () => {
  const [first, second] = legend(PLAN);
  assert.equal(first.setup, 'm.ply birch 15 1.1');
  assert.equal(first.label, 'birch 15 1.1');
  assert.equal(setupLabel({ nest: 'other' }, PLAN.setups[0]), 'm.ply birch 15 1.1');
  assert.equal(first.parts, 2);
  assert.deepEqual(first.operations.map((o) => [o.index, o.kind, o.tool, o.features, o.tabs]), [
    [0, 'pocket', '8 mm', 2, 0], [1, 'contour', '6 mm', 2, 2], [2, 'contour', '6 mm', 1, 0],
    [3, 'dogbone', '3.175 mm', 1, 0], [4, 'drill', '2 mm', 1, 0], [5, 'chamfer', 'V-bit 90°', 2, 0],
    [6, 'groove', 'V-bit 90°', 1, 0], [7, 'release', '6 mm', 3, 2]]);
  assert.equal(first.operations[1].color, first.operations[7].color, 'one tool, one colour');
  assert.notEqual(first.operations[0].color, first.operations[1].color);
  assert.deepEqual(second.operations.map((o) => o.name), ['5 mm: bores (Bohrung 5mm)']);
  assert.deepEqual(legend(null), []);
});

test('the operation chosen is the plan\'s, or none', () => {
  assert.deepEqual(chosenOperation(PLAN, { setup: 'm.ply birch 15 1.1', index: 3 }), { setup: 'm.ply birch 15 1.1', index: 3 });
  assert.deepEqual(chosenOperation(PLAN, { setup: 'm.ply birch 15 2.1', index: 'all' }), { setup: 'm.ply birch 15 2.1', index: 'all' });
  assert.equal(chosenOperation(PLAN, { setup: 'm.ply birch 15 2.1', index: 1 }), null);      // it has one
  assert.equal(chosenOperation(PLAN, { setup: 'm.ply birch 15 1.1', index: -1 }), null);
  assert.equal(chosenOperation(PLAN, { setup: 'm.ply birch 15 1.1', index: '2' }), null);
  assert.equal(chosenOperation(PLAN, { setup: 'gone', index: 0 }), null);
  assert.equal(chosenOperation(PLAN, null), null);
  assert.equal(chosenOperation(null, { setup: 'm.ply birch 15 1.1', index: 0 }), null);
});

test('the highlight set: the operation chosen, or all of the setup\'s, on its own setup only', () => {
  const [one, two] = PLAN.setups;
  assert.deepEqual(highlighted(one, { setup: one.name, index: 4 }), [4]);
  assert.deepEqual(highlighted(one, { setup: one.name, index: 'all' }), [0, 1, 2, 3, 4, 5, 6, 7]);
  assert.deepEqual(highlighted(two, { setup: one.name, index: 4 }), []);
  assert.deepEqual(highlighted(one, null), []);
});

test('the parts by their release order, smallest hold first, an own blank\'s without one', () => {
  const [one, two] = PLAN.setups;
  assert.deepEqual([...releaseRanks(one)], [['m.b', 1], ['m.a', 2]]);       // a part's inner contour first, then its outer
  assert.deepEqual(releaseList(one).map((p) => [p.path, p.rank, p.tabs, p.policy]), [['m.b', 1, 0, 'forced'], ['m.a', 2, 2, 'auto']]);
  assert.deepEqual(releaseList(two).map((p) => [p.path, p.rank]), [['m.top', null]]);
  assert.equal(holdText(950.4), '950 cm²');
  assert.equal(holdText(42.25), '42.3 cm²');
  assert.equal(partText(releaseList(one)[1], 2), 'released 2 of 2: hold 950 cm², 2 tabs (cam.tabs auto)');
  assert.equal(partText({ path: 'x', rank: 1, hold: 7, tabs: 1, policy: 'forced' }, 1), 'released 1 of 1: hold 7.0 cm², 1 tab (cam.tabs forced)');
  assert.equal(partText(releaseList(two)[0], 0), 'no release (its own blank): hold 3000 cm², 0 tabs (cam.tabs auto)');
  const colors = releaseColors(one);
  assert.deepEqual([...colors.keys()], ['m.b', 'm.a']);
  assert.equal(colors.get('m.b'), 'rgb(214, 233, 248)');            // the first released the palest
  assert.equal(colors.get('m.a'), 'rgb(62, 116, 186)');
  assert.deepEqual([...releaseColors(two)], []);
});

test('each feature\'s shapes by its kind', () => {
  const kinds = (k, j = 0) => featureShapes(PLAN.setups[0].operations[k].features[j]).map((s) => s.shape);
  assert.deepEqual(kinds(0), ['region']);
  assert.equal(featureShapes(PLAN.setups[0].operations[0].features[1])[0].rest, true);
  assert.deepEqual(kinds(1), ['outline']);
  assert.deepEqual(kinds(3), ['circle', 'outline']);
  assert.deepEqual(kinds(4), ['circle']);
  assert.deepEqual(featureShapes(PLAN.setups[0].operations[5].features[0]).map((s) => s.closed), [true, false]);
  assert.deepEqual(featureShapes(PLAN.setups[0].operations[5].features[1]), [{ shape: 'circle', center: [225, 35], r: 4 }]);
  assert.deepEqual(featureShapes(PLAN.setups[0].operations[6].features[0]),
    [{ shape: 'outline', points: [[210, 61], [210, 56]], closed: false }]);
  assert.deepEqual(featureShapes({ what: 'dogbone', center: [0, 0], d: 3, arc: [] }), [{ shape: 'circle', center: [0, 0], r: 1.5 }]);
});

test('a setup\'s point lands on its blank in the drawing, y down', () => {
  const at = toDrawing({ x: 80, y: 230, height: 600 }, [20, 30, 600, 400]);
  assert.deepEqual(at([0, 0]), [100, 800]);
  assert.deepEqual(at([10.375, 510.375]), [110.375, 289.625]);
});

test('the tabs once each, though a roughing and its release both leave them', () => {
  assert.deepEqual(tabPositions(PLAN.setups[0]), [[10, 50], [110, 50]]);
  assert.deepEqual(tabPositions(PLAN.setups[1]), []);
});

test('what is drawn on a setup\'s blank', () => {
  const setup = PLAN.setups[0];
  const sheet = { x: 80, y: 230, height: 600 };
  const labels = { 'm.a': { x: 160, y: 700, size: 40 }, 'm.b': { x: 325, y: 765, size: 20 } };
  const colors = toolColors(PLAN);
  // nothing chosen: the tabs and the parts' release
  const plain = setupOverlay(setup, { sheet, colors, labels });
  assert.deepEqual(plain.map((e) => e.attrs.class), ['cam-tab', 'cam-tab', 'cam-release', 'cam-release']);
  assert.deepEqual(plain.slice(0, 2).map((e) => [e.attrs.cx, e.attrs.cy]), [[110, 750], [210, 750]]);
  assert.deepEqual(plain.slice(2).map((e) => [e.attrs['data-path'], e.text, e.attrs.y]),
    [['m.a', '2. 950 cm², 2 tabs', 654], ['m.b', '1. 42.3 cm²', 742]]);
  // the pockets as filled regions in their tool's colour, a rest apart
  const pockets = setupOverlay(setup, { sheet, chosen: { setup: setup.name, index: 0 }, colors, labels })
    .filter((e) => e.attrs.class.startsWith('cam-feature'));
  assert.deepEqual(pockets.map((e) => [e.tag, e.attrs.class, e.attrs.fill]),
    [['path', 'cam-feature cam-pocket', colors.get('8 mm')], ['path', 'cam-feature cam-rest rest', colors.get('8 mm')]]);
  assert.equal(pockets[0].attrs.d, 'M 120 780 L 180 780 L 180 720 L 120 720 Z M 140 760 L 150 760 L 150 750 L 140 750 Z');
  // a contour as an outline, a hole as a circle with a ring around it
  const contour = setupOverlay(setup, { sheet, chosen: { setup: setup.name, index: 2 }, colors, labels })[0];
  assert.deepEqual([contour.attrs.fill, contour.attrs.stroke], ['none', colors.get('6 mm')]);
  assert.match(contour.attrs.d, /^M 300 790 L 350 790 .* Z$/);
  const hole = setupOverlay(setup, { sheet, chosen: { setup: setup.name, index: 4 }, colors });
  assert.deepEqual(hole.map((e) => [e.tag, e.attrs.cx, e.attrs.cy, e.attrs.r]).slice(0, 2), [['circle', 190, 710, 1], ['circle', 190, 710, 6]]);
  // a V-groove as an open line, the dog bone as its circle and wall
  const groove = setupOverlay(setup, { sheet, chosen: { setup: setup.name, index: 6 }, colors })[0];
  assert.equal(groove.attrs.d, 'M 310 739 L 310 744');
  const bone = setupOverlay(setup, { sheet, chosen: { setup: setup.name, index: 3 }, colors });
  assert.deepEqual(bone.slice(0, 3).map((e) => e.tag), ['circle', 'circle', 'path']);
  // every operation of the setup, none on another's
  const all = setupOverlay(setup, { sheet, chosen: { setup: setup.name, index: 'all' }, colors });
  assert.equal(all.filter((e) => e.attrs.class.startsWith('cam-feature')).length, 2 + 2 + 1 + 3 + 2 + 2 + 2 + 1 + 3);
  assert.equal(setupOverlay(PLAN.setups[1], { sheet, chosen: { setup: setup.name, index: 'all' }, colors }).length, 0);
});

test('what the plan leaves out and its problems, as listed beside the drawing', () => {
  assert.equal(planNotes(PLAN), [
    'birch 15 1.1:',
    '  left out: m.a groove_floor (2 dog bones): other face',
    '  left out: m.b pilot: nothing fits, no drill of 1.5 mm',
    '  problem: m.a: a 2 mm hole is drilled',
    'birch 15 2.1:',
    '  left out: m.top the outline (ring 0): hand work',
    'problem: check: m.b: a ring is cut twice'].join('\n'));
  assert.equal(planNotes(null), '');
});
