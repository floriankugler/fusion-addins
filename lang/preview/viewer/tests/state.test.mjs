// The page's bookkeeping (state.js): the layout version, hidden parts, and
// the promises of preview.loaded() and preview.open().
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { LAYOUT_VERSION, layoutVersionProblem, setHidden, toggleHides, isolate, LoadTracker, nestStatusText } from '../state.js';

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

test('the layout version the page reads', () => {
  assert.equal(LAYOUT_VERSION, 6);
  assert.equal(layoutVersionProblem({ version: LAYOUT_VERSION }), null);
  assert.equal(layoutVersionProblem({ version: 2 }), 'layout version 2, this viewer reads 6');
  assert.equal(layoutVersionProblem({ version: 7 }), 'layout version 7, this viewer reads 6');
  assert.equal(layoutVersionProblem({}), 'layout version missing, this viewer reads 6');
  assert.equal(layoutVersionProblem(null), 'layout version missing, this viewer reads 6');
});

test('the nest state as the side panel says it', () => {
  assert.equal(nestStatusText({ state: 'ok' }), 'nest of this layout');
  assert.match(nestStatusText({ state: 'stale' }), /older layout/);
  assert.match(nestStatusText({ state: 'running' }), /nesting/);
  assert.equal(nestStatusText({ state: 'failed', log: 'error: no bed\n' }), 'the nest failed:\nerror: no bed');
  assert.match(nestStatusText({ state: 'none' }), /no nest/);
  assert.match(nestStatusText(undefined), /no nest/);
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
