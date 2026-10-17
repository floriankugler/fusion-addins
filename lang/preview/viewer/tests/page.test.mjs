// The page's wiring (index.html), read as text: every name it imports from
// the modules next to it exists, so a renamed export does not leave a blank
// page; and the constants the modules hold are not written out again.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const viewer = new URL('../', import.meta.url);
const page = await readFile(new URL('index.html', viewer), 'utf8');

test('every name the page imports from its own modules is exported', async () => {
  const imports = [...page.matchAll(/import\s*\{([^}]*)\}\s*from\s*'\.\/([\w.-]+)'/g)];
  assert.deepEqual(imports.map((m) => m[2]).sort(), ['scene-utils.js', 'spacemouse.js', 'state.js']);
  for (const [, names, file] of imports) {
    const module = await import(new URL(file, viewer));
    for (const name of names.split(',').map((n) => n.trim().split(/\s+as\s+/)[0]).filter(Boolean)) {
      assert.ok(name in module, `${file} exports no ${name}`);
    }
  }
});

test('the constants live in one place', () => {
  assert.equal(page.match(/-1, -1\.2, 0\.8/g), null, 'the iso direction is ISO');
  assert.equal(page.match(/\{ x: 0, y: 1, z: 2 \}/g), null, 'the axis indices are AXIS');
  assert.equal(page.match(/up\.set\(0, 0, 1\)/g), null, 'world up is UP');
  assert.equal(page.match(/300px/g)?.length, 1, 'the side pane width is --side');
  assert.match(page, /store\('master', masterShow\)/, 'the master toggles are kept like the other display settings');
});

test('paths come from the meshes, not from their sanitised names', () => {
  assert.doesNotMatch(page, /sanitized/);
});

test('the level row offers the levels state.js knows, normal chosen', async () => {
  const { LEVELS } = await import(new URL('state.js', viewer));
  const row = page.match(/<select id="level"[^>]*>([\s\S]*?)<\/select>/)[1];
  assert.deepEqual([...row.matchAll(/value="(\w+)"/g)].map((m) => m[1]), LEVELS);
  assert.match(row, /value="normal" selected/);
});
