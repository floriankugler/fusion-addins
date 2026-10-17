// What a save changed (changes.js): the diff of two layouts, where the page
// glows for it and what the panel says.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { same, diffLayouts, partChange, changeMarks, changeRows, changeSummary, changeReport, opMarks, opLabel, mm, moveText } from '../changes.js';

const frame = { front: '-y', back: '+y', left: '-x', right: '+x', top: '+z', bottom: '-z' };

// A board lying flat, `size` along x, y and z from `at`; its operations in world (u, v) = (x, y).
function board(path, { at = [0, 0, 0], size = [600, 300, 18], ops = [], ...rest } = {}) {
  const [x, y, z] = at, [w, d, t] = size;
  return { path, where: 'examples/a.py:1', kind: 'board', section: null, material: 'birch 18', thickness: t,
    axes: { t: 'z', u: 'x', v: 'y' }, box: { min: [x, y, z], max: [x + w, y + d, z + t] }, origin: [x, y, z],
    outline: [[[x, y], [x + w, y], [x + w, y + d], [x, y + d]]], grain: null, show: 'top', machine: 'top',
    grained: false, manual: false, nest: true, ops, faces: { top: ['top'], bottom: ['bottom'] },
    settings: { chamfer_size: { value: 0.5, source: 'm' } }, op_settings: {}, ...rest };
}
const hole = (u, v, extra = {}) => ({ kind: 'hole', name: null, face: 'top', u, v, d: 5, depth: 10, depth_spec: '10',
  through: false, chamfer: 0, where: 'examples/a.py:2', ...extra });
const pocket = (rings, extra = {}) => ({ kind: 'pocket', name: null, face: 'top', depth: 5, depth_spec: '5', chamfer: 0,
  shape: rings, slot: null, dogbones: [], where: 'examples/a.py:3', ...extra });
const box = (x, y, z, w = 10, d = 10, h = 10) => ({ min: [x, y, z], max: [x + w, y + d, z + h] });
function layout(parts, { hardware = [], problems = [] } = {}) {
  return { version: 10, units: 'mm', frame, problems, snapshots: [], sheet_materials: {},
    modules: [{ path: 'm', where: '', box: null, parts, hardware, exports: {}, problems, nests: [] }] };
}
const runner = (at, where = 'examples/a.py:9') => ({ path: 'm.runners', where, kind: 'hardware', name: 'runners',
  bodies: [{ name: 'left', boxes: [box(...at), box(at[0], at[1] + 10, at[2], 5, 5, 5)] }] });

test('two values are the same but for the lines that made them and the nodes that set them', () => {
  const a = board('m.shelf', { ops: [hole(50, 50)] });
  const b = board('m.shelf', { ops: [hole(50, 50, { where: 'examples/a.py:20' })], where: 'examples/a.py:19',
    settings: { chamfer_size: { value: 0.5, source: 'm.shelf' } } });
  const seen = { provenance: false };
  assert.ok(same(a, b, seen));
  assert.ok(seen.provenance);
  assert.ok(!same(a, board('m.shelf', { ops: [hole(50, 50.5)] })));
  assert.ok(!same({ a: 1 }, { a: 1, b: 2 }));
  assert.ok(!same([1, 2], { 0: 1, 1: 2 }));
});

test('a layout as before changes nothing; its lines alone say so', () => {
  const before = layout([board('m.shelf', { ops: [hole(50, 50)] })]);
  assert.deepEqual(diffLayouts(before, before),
    { added: [], gone: [], changed: [], problems: { added: [], gone: [] }, provenance: false });
  const moved = layout([board('m.shelf', { ops: [hole(50, 50, { where: 'examples/a.py:30' })], where: 'examples/a.py:29' })]);
  const diff = diffLayouts(before, moved);
  assert.deepEqual(diff.changed, []);
  assert.equal(diff.provenance, true);
  assert.deepEqual(changeRows(diff, frame), [[{ text: 'no part changed, only lines of the build file' }]]);
  assert.deepEqual(changeRows(diffLayouts(before, before), frame), [[{ text: 'no part changed' }]]);
});

test('parts added and gone, by path', () => {
  const diff = diffLayouts(layout([board('m.a'), board('m.b')]), layout([board('m.b'), board('m.c')]));
  assert.deepEqual(diff.added, ['m.c']);
  assert.deepEqual(diff.gone, ['m.a']);
  assert.deepEqual(diff.changed, []);
  assert.deepEqual(changeRows(diff, frame).map((row) => row.map((p) => p.text).join('')),
    ['1 part added: m.c', '1 part gone: m.a']);
  assert.deepEqual(changeRows(diff, frame)[0][1], { text: 'm.c', path: 'm.c' });
});

test('a hole moved by 2 mm is one operation changed, glowing where it is and fainter where it was', () => {
  const before = layout([board('m.shelf', { ops: [hole(50, 50), hole(550, 50), hole(50, 250)] })]);
  const after = layout([board('m.shelf', { ops: [hole(50, 50), hole(552, 50), hole(50, 250)] })]);
  const diff = diffLayouts(before, after);
  assert.equal(diff.changed.length, 1);
  const change = diff.changed[0];
  assert.equal(change.path, 'm.shelf');
  assert.equal(change.box, false);
  assert.equal(change.moved, null);
  assert.deepEqual(change.ops, { changed: [{ index: 1, name: null, kind: 'hole', was: 1 }], added: [], removed: [] });
  assert.deepEqual(change.outline, { added: [], removed: [] });
  assert.deepEqual(change.rest, []);
  const { marks, lines, unplaced } = changeMarks(diff, before, after);
  assert.deepEqual(marks, [
    { at: [552, 50, 18], kind: 'changed', path: 'm.shelf', op: 'hole 1' },
    { at: [550, 50, 18], kind: 'was', path: 'm.shelf', op: 'hole 1' },
  ]);
  assert.deepEqual(lines, []);
  assert.deepEqual(unplaced, []);
  assert.deepEqual(changeRows(diff, frame).map((row) => row.map((p) => p.text).join('')), ['1 part changed: m.shelf (1 op)']);
});

test('half a millimetre is a change, and a thousandth; float noise below 0.1 µm is not', () => {
  const before = layout([board('m.shelf', { ops: [hole(50, 50)] })]);
  assert.equal(diffLayouts(before, layout([board('m.shelf', { ops: [hole(50.5, 50)] })])).changed[0].ops.changed.length, 1);
  assert.equal(diffLayouts(before, layout([board('m.shelf', { ops: [hole(50.001, 50)] })])).changed[0].ops.changed.length, 1);
  assert.deepEqual(diffLayouts(before, layout([board('m.shelf', { at: [1e-9, 0, 0], ops: [hole(50 + 1e-9, 50)] })])).changed, []);
  assert.ok(same(0.1 + 0.2, 0.3));
  assert.ok(!same(0.1, 0.1002));
});

test('a part moved whole moved, its operations and outline with it', () => {
  const ops = (dx) => [hole(50 + dx, 50), pocket([[[100 + dx, 100], [200 + dx, 100], [200 + dx, 200], [100 + dx, 200]]]),
    { kind: 'vgroove', name: null, face: 'top', start: [10 + dx, 10], end: [300 + dx, 10], depth: 2, where: '' }];
  const before = layout([board('m.shelf', { ops: ops(0) })]);
  const after = layout([board('m.shelf', { at: [20.1, 0, 0], ops: ops(20.1) })]);
  const diff = diffLayouts(before, after);
  const change = diff.changed[0];
  assert.equal(change.box, true);
  assert.deepEqual(change.moved.map((x) => +x.toFixed(9)), [20.1, 0, 0]);
  assert.equal(change.resized, false);
  assert.deepEqual(change.ops, { changed: [], added: [], removed: [] });
  assert.deepEqual(change.outline, { added: [], removed: [] });
  assert.deepEqual(changeMarks(diff, before, after), { marks: [], lines: [], unplaced: [] });
  assert.equal(changeSummary(change, frame), 'moved right 20.1 mm');
});

test('a part moved and given a hole: the move, and the hole added', () => {
  const before = layout([board('m.shelf', { ops: [hole(50, 50), hole(60, 50)] })]);
  const after = layout([board('m.shelf', { at: [0, -30, 5], ops: [hole(50, 20), hole(60, 20), hole(70, 20)] })]);
  const change = diffLayouts(before, after).changed[0];
  assert.deepEqual(change.moved, [0, -30, 5]);
  assert.deepEqual(change.ops, { changed: [], added: [{ index: 2, name: null, kind: 'hole' }], removed: [] });
  assert.equal(changeSummary(change, frame), 'moved front 30 mm, top 5 mm, 1 op');
});

test('a part moved while its holes stayed where they were: compared as it was or as moved, whichever matches more', () => {
  const holes = [50, 150, 250, 350, 450, 550].map((u) => hole(u, 50));
  const before = layout([board('m.shelf', { ops: holes })]);
  const after = layout([board('m.shelf', { at: [10, 0, 0], ops: holes })]);
  const change = diffLayouts(before, after).changed[0];
  assert.deepEqual(change.moved, [10, 0, 0]);
  // as it was, the six holes match and the four outline segments do not; as moved, only the outline would
  assert.deepEqual(change.ops, { changed: [], added: [], removed: [] });
  assert.equal(change.outline.added.length, 4);
  // two holes: as moved, the outline and one hole (50 moved to 60) match
  const two = diffLayouts(layout([board('m.shelf', { ops: [hole(50, 50), hole(60, 50)] })]),
    layout([board('m.shelf', { at: [10, 0, 0], ops: [hole(50, 50), hole(60, 50)] })])).changed[0];
  assert.deepEqual(two.outline, { added: [], removed: [] });
  assert.deepEqual(two.ops.changed, [{ index: 0, name: null, kind: 'hole', was: 1 }]);
});

test('an unnamed hole inserted before others is the one hole added', () => {
  const before = layout([board('m.shelf', { ops: [hole(50, 50), hole(100, 50), hole(150, 50)] })]);
  const after = layout([board('m.shelf', { ops: [hole(10, 50), hole(50, 50), hole(100, 50), hole(150, 50)] })]);
  assert.deepEqual(diffLayouts(before, after).changed[0].ops,
    { changed: [], added: [{ index: 0, name: null, kind: 'hole' }], removed: [] });
});

test('named operations match by name, whatever their order; a renamed one is removed and added', () => {
  const before = layout([board('m.shelf', { ops: [hole(50, 50, { name: 'pin_a' }), hole(100, 50, { name: 'pin_b' })] })]);
  const swapped = layout([board('m.shelf', { ops: [hole(100, 50, { name: 'pin_b' }), hole(50, 52, { name: 'pin_a' })] })]);
  assert.deepEqual(diffLayouts(before, swapped).changed[0].ops,
    { changed: [{ index: 1, name: 'pin_a', kind: 'hole', was: 0 }], added: [], removed: [] });
  const renamed = layout([board('m.shelf', { ops: [hole(50, 50, { name: 'pin_c' }), hole(100, 50, { name: 'pin_b' })] })]);
  assert.deepEqual(diffLayouts(before, renamed).changed[0].ops, {
    changed: [], added: [{ index: 0, name: 'pin_c', kind: 'hole' }], removed: [{ index: 0, name: 'pin_a', kind: 'hole' }] });
  const reordered = diffLayouts(before, layout([board('m.shelf', { ops: [hole(100, 50, { name: 'pin_b' }), hole(50, 50, { name: 'pin_a' })] })]));
  assert.deepEqual(reordered.changed[0].ops, { changed: [], added: [], removed: [] });
  assert.equal(changeSummary(reordered.changed[0], frame), 'the order of its ops');
});

test('unnamed operations left over pair by their order among those of their kind', () => {
  const before = layout([board('m.shelf', { ops: [hole(50, 50), pocket([[[0, 0], [10, 0], [10, 10]]]), hole(100, 50)] })]);
  const after = layout([board('m.shelf', { ops: [hole(51, 50), pocket([[[0, 0], [12, 0], [12, 10]]]), hole(101, 50), hole(300, 50)] })]);
  assert.deepEqual(diffLayouts(before, after).changed[0].ops, {
    changed: [{ index: 0, name: null, kind: 'hole', was: 0 }, { index: 1, name: null, kind: 'pocket', was: 1 },
      { index: 2, name: null, kind: 'hole', was: 2 }],
    added: [{ index: 3, name: null, kind: 'hole' }], removed: [] });
});

test('a removed operation glows where it was', () => {
  const before = layout([board('m.shelf', { ops: [hole(50, 50), hole(100, 60)] })]);
  const after = layout([board('m.shelf', { ops: [hole(50, 50)] })]);
  const diff = diffLayouts(before, after);
  assert.deepEqual(diff.changed[0].ops.removed, [{ index: 1, name: null, kind: 'hole' }]);
  assert.deepEqual(changeMarks(diff, before, after).marks, [{ at: [100, 60, 18], kind: 'removed', path: 'm.shelf', op: 'hole 1' }]);
});

test('an outline changed glows along the segments that differ, at mid thickness', () => {
  const before = layout([board('m.shelf')]);
  const notched = board('m.shelf');
  notched.outline = [[[0, 0], [600, 0], [600, 300], [100, 300], [100, 280], [0, 280]]];
  const after = layout([notched]);
  const diff = diffLayouts(before, after);
  const change = diff.changed[0];
  assert.equal(change.box, false);
  assert.deepEqual(change.outline.added, [[0, 280, 0, 0], [600, 300, 100, 300], [100, 300, 100, 280], [100, 280, 0, 280]]);
  assert.deepEqual(change.outline.removed, [[0, 300, 0, 0], [600, 300, 0, 300]]);
  const { lines } = changeMarks(diff, before, after);
  assert.equal(lines.length, 4);
  assert.deepEqual(lines.slice(0, 2), [
    { from: [0, 280, 9], to: [0, 0, 9], kind: 'outline', path: 'm.shelf' },
    { from: [600, 300, 9], to: [100, 300, 9], kind: 'outline', path: 'm.shelf' },
  ]);
  assert.equal(changeSummary(change, frame), 'outline');
});

test('the report counts the outline segments and glowing lines, and says where they are', () => {
  const before = layout([board('m.shelf', { ops: [hole(10, 10)] })]);
  const notched = board('m.shelf', { ops: [hole(12, 10)] });
  notched.outline = [[[0, 0], [600, 0], [600, 300], [100, 300], [100, 280], [0, 280]]];
  const after = layout([notched]);
  const diff = diffLayouts(before, after);
  const report = changeReport(diff, changeMarks(diff, before, after));
  assert.deepEqual(report.changed[0].outline, { added: 4, removed: 2, at: [300, 150, 9] });
  assert.deepEqual(report.changed[0].ops.changed, [{ index: 0, name: null, kind: 'hole', was: 0 }]);
  assert.equal(report.lines, 4);
  assert.deepEqual(report.marks.map((m) => m.kind), ['changed', 'was']);
  assert.deepEqual(diff.changed[0].outline.added.length, 4, 'the diff itself keeps the segments');
  assert.doesNotThrow(() => JSON.stringify(report));
});

test('an outline that starts elsewhere or runs the other way is the same', () => {
  const before = layout([board('m.shelf')]);
  const turned = board('m.shelf');
  turned.outline = [[[600, 300], [600, 0], [0, 0], [0, 300]]];
  assert.deepEqual(diffLayouts(before, layout([turned])).changed[0].outline, { added: [], removed: [] });
});

test('a part longer is resized, not moved; one turned is not compared operation by operation', () => {
  const before = layout([board('m.shelf', { ops: [hole(50, 50)] })]);
  const longer = diffLayouts(before, layout([board('m.shelf', { size: [620, 300, 18], ops: [hole(50, 50)] })])).changed[0];
  assert.equal(longer.resized, true);
  assert.equal(longer.moved, null);
  assert.deepEqual(longer.ops, { changed: [], added: [], removed: [] });
  assert.equal(changeSummary(longer, frame), 'resized, outline');
  const turned = diffLayouts(before, layout([board('m.shelf', { axes: { t: 'z', u: 'y', v: 'x' }, ops: [hole(50, 50)] })])).changed[0];
  assert.equal(turned.turned, true);
  assert.equal(turned.ops, null);
  assert.equal(changeSummary(turned, frame), 'turned');
});

test('what the glow cannot show is said: material, grain, settings, an operation\'s own', () => {
  const before = layout([board('m.shelf', { op_settings: { pin: { 'cam.tabs': { value: 2, source: 'm' } } } })]);
  const after = layout([board('m.shelf', { material: 'oak 18', grain: 'x', nest: false,
    settings: { chamfer_size: { value: 1, source: 'm' }, tool: { value: 6, source: 'default' } },
    op_settings: { pin: { 'cam.tabs': { value: 3, source: 'm' } } } })]);
  const change = diffLayouts(before, after).changed[0];
  assert.deepEqual(change.rest, ['material', 'grain', 'nest']);
  assert.deepEqual(change.values, { material: ['birch 18', 'oak 18'], grain: [null, 'x'], nest: [true, false] });
  assert.deepEqual(change.settings, [{ name: 'chamfer_size', was: 0.5, now: 1 }, { name: 'tool', was: null, now: 6 },
    { name: 'pin: cam.tabs', was: 2, now: 3 }]);
  assert.deepEqual(changeRows(diffLayouts(before, after), frame).map((row) => row.map((p) => p.text).join('')), [
    '1 part changed: m.shelf (material, grain, nest, 3 settings)',
    'm.shelf: material birch 18 → oak 18',
    'm.shelf: grain none → x',
    'm.shelf: nest true → false',
    'm.shelf: chamfer_size 0.5 → 1',
    'm.shelf: tool none → 6',
    'm.shelf: pin: cam.tabs 2 → 3',
  ]);
});

test('a bought part\'s body moved or reshaped', () => {
  const before = layout([], { hardware: [runner([0, 0, 0])] });
  const moved = diffLayouts(before, layout([], { hardware: [runner([0, 5, 0], 'examples/a.py:40')] }));
  assert.deepEqual(moved.changed, [{ path: 'm.runners.left', kind: 'hardware', box: true, moved: [0, 5, 0], resized: false,
    rest: [], values: {} }]);
  assert.equal(changeSummary(moved.changed[0], frame), 'hardware, moved back 5 mm');
  const item = runner([0, 0, 0]);
  item.bodies[0].boxes[1].max[2] = 20;
  const reshaped = diffLayouts(before, layout([], { hardware: [item] })).changed[0];
  assert.equal(reshaped.moved, null);
  assert.equal(changeSummary(reshaped, frame), 'hardware, reshaped');
  const lines = diffLayouts(before, layout([], { hardware: [runner([0, 0, 0], 'examples/a.py:41')] }));
  assert.deepEqual(lines.changed, []);
  assert.equal(lines.provenance, true);
});

test('a part that became a bought part\'s body is gone and added', () => {
  const diff = diffLayouts(layout([board('m.runners.left')]), layout([], { hardware: [runner([0, 0, 0])] }));
  assert.deepEqual([diff.added, diff.gone], [['m.runners.left'], ['m.runners.left']]);
});

test('problems that came and went, their lines left out', () => {
  const before = layout([], { problems: ['examples/a.py:4: m.a overlaps m.b', 'm.c is outside the sheet'] });
  const after = layout([], { problems: ['examples/a.py:6: m.a overlaps m.b', 'm.d has no material'] });
  const diff = diffLayouts(before, after);
  assert.deepEqual(diff.problems, { added: ['m.d has no material'], gone: ['m.c is outside the sheet'] });
  assert.deepEqual(changeRows(diff, frame).map((row) => row.map((p) => p.text).join('')),
    ['no part changed', 'new problem: m.d has no material', '1 problem gone']);
});

test('the panel names the first parts and counts the rest', () => {
  const before = layout(Array.from({ length: 12 }, (_, i) => board(`m.p${i}`, { ops: [hole(10, 10)] })));
  const after = layout(Array.from({ length: 12 }, (_, i) => board(`m.p${i}`, { ops: [hole(10, 10), hole(20, 10)] })));
  const [row] = changeRows(diffLayouts(before, after), frame, [], 3);
  assert.equal(row.map((p) => p.text).join(''), '12 parts changed: m.p0 (1 op), m.p1 (1 op), m.p2 (1 op), and 9 more');
  assert.deepEqual(row.filter((p) => p.path).map((p) => p.path), ['m.p0', 'm.p1', 'm.p2']);
});

test('chamfers glow along what they follow: the outline on their face, an edge, a named operation', () => {
  const part = board('m.shelf', { ops: [hole(50, 60, { name: 'pin' })] });
  const chamfer = (what, face = 'top') => ({ kind: 'chamfer', what, size: 1, face, where: '' });
  const outline = opMarks(frame, part, chamfer('outline'));
  assert.equal(outline.lines.length, 4);
  assert.deepEqual(outline.lines[0], [[0, 300, 18], [0, 0, 18]]);
  assert.deepEqual(opMarks(frame, part, chamfer('outline', 'bottom')).lines[1], [[0, 0, 0], [600, 0, 0]]);
  assert.deepEqual(opMarks(frame, part, chamfer('front.top')), { points: [], lines: [[[0, 0, 18], [600, 0, 18]]] });
  assert.deepEqual(opMarks(frame, part, chamfer('right.back')), { points: [], lines: [[[600, 300, 0], [600, 300, 18]]] });
  assert.deepEqual(opMarks(frame, part, chamfer('pin')), { points: [[50, 60, 18]], lines: [] });
  assert.equal(opMarks(frame, part, chamfer('nothing')), null);
  assert.equal(opMarks(frame, part, chamfer('top.bottom')), null);
  assert.equal(opMarks(frame, part, chamfer('outline', 'front')), null);
});

test('what the page cannot place is listed', () => {
  const before = layout([board('m.shelf', { ops: [{ kind: 'chamfer', what: 'outline', size: 1, face: 'top', where: '' }] })]);
  const after = layout([board('m.shelf', { ops: [{ kind: 'chamfer', what: 'gone_op', size: 1, face: 'top', where: '' }] })]);
  const diff = diffLayouts(before, after);
  const { unplaced } = changeMarks(diff, before, after);
  assert.deepEqual(unplaced, ['m.shelf: chamfer 0']);
  assert.deepEqual(changeRows(diff, frame, unplaced).at(-1), [{ text: 'not placed in the scene: m.shelf: chamfer 0' }]);
});

test('an edge operation moves with its part', () => {
  const edge = (s, t) => ({ kind: 'edge', face: 'front', s, t, where: '',
    op: { kind: 'hole', name: null, face: 'front', u: 0, v: 0, d: 8, depth: 30, depth_spec: '30', through: false, chamfer: 0, where: '' } });
  const before = layout([board('m.shelf', { ops: [edge(100, 9)] })]);
  const after = layout([board('m.shelf', { at: [5, 7, 3], ops: [edge(105, 12)] })]);
  const change = diffLayouts(before, after).changed[0];
  assert.deepEqual(change.moved, [5, 7, 3]);
  assert.deepEqual(change.ops, { changed: [], added: [], removed: [] });
  const shifted = diffLayouts(before, layout([board('m.shelf', { ops: [edge(102, 9)] })]));
  assert.deepEqual(changeMarks(shifted, before, layout([board('m.shelf', { ops: [edge(102, 9)] })])).marks[0],
    { at: [102, 0, 9], kind: 'changed', path: 'm.shelf', op: 'edge hole 0' });
});

test('the diff is linear: thousands of holes, all moved, in a moment', () => {
  const n = 5000;
  const ops = (dv) => Array.from({ length: n }, (_, i) => hole(i * 0.1, 50 + dv));
  const before = layout([board('m.big', { ops: ops(0) })]);
  const after = layout([board('m.big', { ops: ops(0.5) })]);
  const start = performance.now();
  const diff = diffLayouts(before, after);
  const marks = changeMarks(diff, before, after);
  assert.equal(diff.changed[0].ops.changed.length, n);
  assert.equal(marks.marks.length, 2 * n);
  assert.ok(performance.now() - start < 1000, `took ${performance.now() - start} ms`);
});

test('lengths and moves as the panel writes them', () => {
  assert.equal(mm(20), '20');
  assert.equal(mm(0.5), '0.5');
  assert.equal(mm(2.256), '2.26');
  assert.equal(mm(0.004), '0.004');
  assert.equal(moveText([20, 0, -2.5], frame), 'right 20 mm, bottom 2.5 mm');
  assert.equal(moveText([0, -3, 0], {}), '-y 3 mm');
  assert.equal(opLabel({ name: 'toekick', kind: 'cut', index: 3 }), 'toekick');
  assert.equal(opLabel({ name: null, kind: 'edge hole', index: 3 }), 'edge hole 3');
});

test('partChange is null for a part the same but for its lines', () => {
  assert.equal(partChange(board('m.a'), board('m.a', { where: 'examples/b.py:3' }), frame), null);
});
