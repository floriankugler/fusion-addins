// The page's bookkeeping (state.js): the layout version, hidden parts, the
// levels asked for, and the promises of preview.loaded(), preview.open()
// and preview.level().
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { LAYOUT_VERSION, layoutVersionProblem, setHidden, toggleHides, isolate, LoadTracker, nestStatusText, chosenNest, settingsText, sheetNames, sheetMade, fixable, LEVELS, LevelChoice, untilLevel } from '../state.js';

// Whether a promise settled, without waiting for it: 'pending', or
// ['resolved', value] / ['rejected', message].
async function stateOf(promise) {
  const pending = Symbol('pending');
  const result = await Promise.race([
    promise.then((value) => ['resolved', value], (error) => ['rejected', error.message]),
    new Promise((resolve) => setImmediate(() => resolve(pending))),
  ]);
  return result === pending ? 'pending' : result;
}

const ok = (builds, version) => ({ builds, state: 'ok', version, log: 'ok' });
const failed = (builds, version, log = 'Traceback: boom') => ({ builds, state: 'failed', version, log });
const building = (builds, version) => ({ builds, state: 'building', version, log: '' });

test('a part\'s settings, one line each with where it came from', () => {
  assert.equal(settingsText({
    chamfer_size: { value: 0.5, source: 'kitchen' },
    material: { value: 'birch 15', source: 'kitchen.left' },
    nest: { value: false, source: 'root' },
    tabs: { value: [1, 2], source: 'master: Tabs' },
  }), 'chamfer_size 0.5: kitchen\nmaterial birch 15: kitchen.left\nnest false: root\ntabs [1,2]: master: Tabs');
  assert.equal(settingsText({}), '');
  assert.equal(settingsText(undefined), '');
});

test('the layout version the page reads', () => {
  assert.equal(LAYOUT_VERSION, 8);
  assert.equal(layoutVersionProblem({ version: LAYOUT_VERSION }), null);
  assert.equal(layoutVersionProblem({ version: 2 }), 'layout version 2, this viewer reads 8');
  assert.equal(layoutVersionProblem({ version: 9 }), 'layout version 9, this viewer reads 8');
  assert.equal(layoutVersionProblem({}), 'layout version missing, this viewer reads 8');
  assert.equal(layoutVersionProblem(null), 'layout version missing, this viewer reads 8');
});

test('the nest state as the side panel says it', () => {
  assert.equal(nestStatusText({ state: 'ok' }), 'its parts are as nested');
  assert.equal(nestStatusText({ state: 'changed', changed: ['m.left'], new: ['m.shelf'], gone: [] }),
    'parts changed since it was nested: nest again\nchanged: m.left\nnew: m.shelf');
  assert.match(nestStatusText({ state: 'running' }), /nesting/);
  assert.equal(nestStatusText({ state: 'failed', log: 'error: no bed\n' }), 'the nest failed:\nerror: no bed');
  assert.match(nestStatusText({ state: 'none' }), /not nested yet/);
  assert.match(nestStatusText(undefined), /lists no nest/);
});

test('a nest marked as made says what is made and what is not', () => {
  const sheets = [['birch 15', '1'], ['birch 15', '2'], ['birch 15', '3']];
  assert.equal(nestStatusText({ state: 'made', sheets, made: sheets, changed: [], not_made: [], new: [], gone: [] }),
    'made, every sheet: frozen');
  assert.equal(nestStatusText({ state: 'sheets', sheets, made: [['birch 15', '1'], ['birch 15', '3']],
    changed: ['m.left'], not_made: ['m.top'], new: [], gone: ['m.old'] }),
  'made by sheets (1, 3 of 3): frozen\nchanged since made: m.left\nnot made: m.top\nmade, gone: m.old\n'
    + 'nest again: they go into the next nest beside it');
  assert.equal(nestStatusText({ state: 'sheets', sheets, made: [['birch 15', '1']], next: 'm.carcass-2', changed: [],
    not_made: [], new: [], gone: [], made_parts: { 'm.left': 'fixed' } }),
  'made by sheets (1 of 3): frozen\nwhat it left was nested anew in m.carcass-2, made too\nevery part of it is made');
  assert.equal(nestStatusText({ state: 'ok', follows: 'm.carcass' }),
    'second nest of m.carcass: what is not made of it\nits parts are as nested');
});

test('sheets are named with their material where a nest has several', () => {
  assert.equal(sheetNames([['birch 15', '1'], ['birch 15', '2']]), '1, 2');
  assert.equal(sheetNames([['birch 9', '1']], [['birch 15', '1'], ['birch 9', '1']]), 'birch 9:1');
  const nest = { state: 'sheets', made: [['birch 15', '2']], changed: ['m.left'] };
  assert.ok(sheetMade(nest, ['birch 15', '2']) && !sheetMade(nest, ['birch 15', '1']));
  assert.ok(fixable(nest, 'm.left') && !fixable(nest, 'm.top'));
  assert.ok(!fixable({ state: 'changed', changed: ['m.left'] }, 'm.left'));
  assert.ok(!fixable({ state: 'made', follows: 'm.carcass', changed: ['m.left'] }, 'm.left'));
});

test('the nest shown is the one wanted, else the first', () => {
  const nests = [{ path: 'kitchen.carcass' }, { path: 'kitchen.birch_9' }];
  assert.equal(chosenNest(nests, 'kitchen.birch_9').path, 'kitchen.birch_9');
  assert.equal(chosenNest(nests, 'gone.birch_15').path, 'kitchen.carcass');
  assert.equal(chosenNest(nests, undefined).path, 'kitchen.carcass');
  assert.equal(chosenNest([], 'kitchen.carcass'), null);
  assert.equal(chosenNest(undefined, null), null);
});

test('setHidden hides and shows paths', () => {
  const hidden = new Set(['a']);
  setHidden(hidden, ['b', 'c'], true);
  assert.deepEqual([...hidden].sort(), ['a', 'b', 'c']);
  setHidden(hidden, ['a', 'c', 'gone'], false);
  assert.deepEqual([...hidden], ['b']);
});

test('toggling shows the paths only when all of them are hidden', () => {
  const hidden = new Set(['a', 'b']);
  assert.equal(toggleHides(hidden, ['a', 'b']), false);
  assert.equal(toggleHides(hidden, ['a', 'c']), true);
  assert.equal(toggleHides(hidden, ['c']), true);
});

test('isolate shows only the paths kept', () => {
  const all = ['m.a', 'm.b', 'n.c'];
  const hidden = new Set(['m.a']);
  assert.equal(isolate(hidden, all, ['m.a', 'm.b']), true);
  assert.deepEqual([...hidden], ['n.c']);
  // Without toggle, isolating again keeps them isolated (the API).
  assert.equal(isolate(hidden, all, ['m.a', 'm.b']), true);
  assert.deepEqual([...hidden], ['n.c']);
});

test('isolate with toggle shows everything when the paths already are isolated', () => {
  const all = ['a', 'b', 'c'];
  const hidden = new Set();
  assert.equal(isolate(hidden, all, ['b'], { toggle: true }), true);
  assert.deepEqual([...hidden].sort(), ['a', 'c']);
  assert.equal(isolate(hidden, all, ['b'], { toggle: true }), false);
  assert.deepEqual([...hidden], []);
  // A kept path that is hidden is not isolated yet: it isolates.
  hidden.add('a').add('b').add('c');
  assert.equal(isolate(hidden, all, ['b'], { toggle: true }), true);
  assert.deepEqual([...hidden].sort(), ['a', 'c']);
});

test('loaded() resolves at once when a scene is on screen, else once one is', async () => {
  const t = new LoadTracker();
  const first = t.loaded();
  assert.equal(await stateOf(first), 'pending');
  t.reported(building(0, null));
  t.shown('v1');
  t.reported(ok(1, 'v1'));
  assert.deepEqual(await stateOf(first), ['resolved', 'v1']);
  assert.deepEqual(await stateOf(t.loaded()), ['resolved', 'v1']);
});

test('loaded(after) waits for a version other than after', async () => {
  const t = new LoadTracker();
  t.shown('v1');
  t.reported(ok(1, 'v1'));
  const next = t.loaded('v1');
  t.reported(building(1, 'v1'));
  assert.equal(await stateOf(next), 'pending');
  t.shown('v2');
  assert.deepEqual(await stateOf(next), ['resolved', 'v2']);
});

test('loaded() rejects with the log when the first build failed', async () => {
  const t = new LoadTracker();
  const waiting = t.loaded();
  t.reported(building(0, null));
  assert.equal(await stateOf(waiting), 'pending');
  t.reported(failed(1, null));
  assert.deepEqual(await stateOf(waiting), ['rejected', 'Traceback: boom']);
  // A call after the failure, with nothing on screen, rejects at once.
  assert.deepEqual(await stateOf(t.loaded()), ['rejected', 'Traceback: boom']);
  // A new build clears it: the next call waits again.
  t.reported(building(1, null));
  assert.equal(await stateOf(t.loaded()), 'pending');
});

test('loaded(after) rejects when a build after the call failed, the old scene staying', async () => {
  const t = new LoadTracker();
  t.shown('v1');
  t.reported(failed(2, 'v1'));      // an earlier failed build, before the call
  const next = t.loaded('v1');
  t.reported(failed(2, 'v1'));      // the same report again: not a build after the call
  assert.equal(await stateOf(next), 'pending');
  t.reported(building(2, 'v1'));
  t.reported(failed(3, 'v1', 'second failure'));
  assert.deepEqual(await stateOf(next), ['rejected', 'second failure']);
  // The old scene is on screen, so loaded() without after resolves.
  assert.deepEqual(await stateOf(t.loaded()), ['resolved', 'v1']);
});

test('loaded() and open() reject when the scene could not be drawn', async () => {
  const t = new LoadTracker();
  const waiting = t.loaded();
  const opening = t.opened();
  t.failed('layout version 2, this viewer reads 3');
  assert.deepEqual(await stateOf(waiting), ['rejected', 'layout version 2, this viewer reads 3']);
  assert.deepEqual(await stateOf(opening), ['rejected', 'layout version 2, this viewer reads 3']);
  assert.deepEqual(await stateOf(t.loaded()), ['rejected', 'layout version 2, this viewer reads 3']);
  // open() again on the same build: the server reports it, the page does not load it again.
  const again = t.opened();
  t.reported(ok(1, 'v1'));
  assert.deepEqual(await stateOf(again), ['rejected', 'layout version 2, this viewer reads 3']);
});

test('a switch to another design rejects loaded() and open()', async () => {
  const t = new LoadTracker();
  t.switched(null, 'van');            // the first design shown: no switch for loaded()
  const early = t.loaded();
  t.shown('v1');
  assert.deepEqual(await stateOf(early), ['resolved', 'v1']);
  const next = t.loaded('v1');
  const opening = t.opened();
  t.switched('van', 'shelf');
  assert.deepEqual(await stateOf(next), ['rejected', 'switched to shelf']);
  assert.deepEqual(await stateOf(opening), ['rejected', 'switched to shelf']);
  assert.equal(t.version, null);
  assert.equal(await stateOf(t.loaded()), 'pending');
});

test('loaded() called before the first design is chosen waits for its scene', async () => {
  const t = new LoadTracker();
  const waiting = t.loaded();
  t.switched(null, 'van');
  assert.equal(await stateOf(waiting), 'pending');
  t.shown('v1');
  assert.deepEqual(await stateOf(waiting), ['resolved', 'v1']);
});

test('open() settles once the latest build is on screen', async () => {
  const t = new LoadTracker();
  const opening = t.opened();
  t.reported(building(0, null));
  t.reported(ok(1, 'v2'));            // not on screen yet
  assert.equal(await stateOf(opening), 'pending');
  t.shown('v2');
  t.reported(ok(1, 'v2'));
  assert.deepEqual(await stateOf(opening), ['resolved', 'v2']);
});

test('open() rejects with the log when the latest build failed, also with no scene at all', async () => {
  const t = new LoadTracker();
  const first = t.opened();
  t.reported(failed(1, null));
  assert.deepEqual(await stateOf(first), ['rejected', 'Traceback: boom']);
  t.shown('v1');
  const second = t.opened();
  t.reported(failed(2, 'v1', 'later failure'));
  assert.deepEqual(await stateOf(second), ['rejected', 'later failure']);
});

test('a level picked goes with the status requests until the server reports it', () => {
  assert.deepEqual(LEVELS, ['fine', 'normal']);
  const levels = new LevelChoice();
  assert.equal(levels.query('van'), '');
  assert.equal(levels.reported('van', 'normal'), 'normal');         // the server's, nothing picked
  levels.pick('van', 'fine');
  assert.equal(levels.query('van'), '&level=fine');
  assert.equal(levels.query('shelf'), '', 'per design');
  assert.equal(levels.reported('van', 'normal'), 'fine', 'shown while on its way');
  assert.equal(levels.query('van'), '&level=fine');
  assert.equal(levels.reported('van', 'fine'), 'fine');
  assert.equal(levels.query('van'), '', 'the server keeps it from then on');
  assert.equal(levels.reported('van', 'normal'), 'normal', 'another page may pick another one');
  assert.throws(() => levels.pick('van', 'rough'), /no level "rough"; there are fine, normal/);
});

test('untilLevel waits for a scene of the level asked', async () => {
  const t = new LoadTracker();
  let level = null;
  const shown = (version, built) => { level = built; t.shown(version); };
  shown('v1', 'normal');
  t.reported(ok(1, 'v1'));
  assert.deepEqual(await stateOf(untilLevel(t, () => level, 'normal')), ['resolved', 'v1']);
  const fine = untilLevel(t, () => level, 'fine');
  assert.equal(await stateOf(fine), 'pending');
  shown('v2', 'normal');           // a build started before the level changed
  assert.equal(await stateOf(fine), 'pending');
  shown('v3', 'fine');
  assert.deepEqual(await stateOf(fine), ['resolved', 'v3']);
  const back = untilLevel(t, () => level, 'normal');
  assert.equal(await stateOf(back), 'pending');
  t.reported(failed(4, 'v3'));
  assert.deepEqual(await stateOf(back), ['rejected', 'Traceback: boom']);
});
