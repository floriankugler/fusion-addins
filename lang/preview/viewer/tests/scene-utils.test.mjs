// Freeing rebuilt content (scene-utils.js), against stand-ins for three.js
// objects that count their dispose() calls.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { AXIS, ISO, UP, share, disposeTree, clearGroup } from '../scene-utils.js';

class Resource {
  constructor(name) { this.name = name; this.disposed = 0; }
  dispose() { this.disposed += 1; }
}
class Texture extends Resource { get isTexture() { return true; } }

class Node {
  constructor({ geometry, material, element } = {}) {
    this.geometry = geometry;
    this.material = material;
    this.children = [];
    if (element) { this.element = element; this.isCSS2DObject = true; }
  }
  add(...children) { this.children.push(...children); return this; }
  clear() { this.children = []; return this; }
  traverse(fn) { fn(this); for (const child of this.children) child.traverse(fn); }
}

test('the shared constants', () => {
  assert.deepEqual(AXIS, { x: 0, y: 1, z: 2 });
  assert.deepEqual(ISO, [-1, -1.2, 0.8]);
  assert.deepEqual(UP, [0, 0, 1]);
  assert.ok(Object.isFrozen(AXIS) && Object.isFrozen(ISO) && Object.isFrozen(UP));
});

test('disposeTree frees each geometry, material and texture once', () => {
  // A part as the page builds it: its mesh, edges shared by two line sets,
  // two stencil meshes on the part's geometry.
  const geometry = new Resource('part');
  const map = new Texture('map');
  const material = new Resource('material');
  material.map = map;
  const edges = new Resource('edges');
  const edgeMaterial = share(new Resource('edge material'));
  const stencilMaterial = share(new Resource('stencil'));
  const part = new Node({ geometry, material }).add(
    new Node({ geometry: edges, material: edgeMaterial }),
    new Node({ geometry: edges, material: edgeMaterial }),
    new Node().add(new Node({ geometry, material: stencilMaterial }), new Node({ geometry, material: stencilMaterial })),
  );
  const root = new Node().add(part);
  disposeTree(root);
  assert.equal(geometry.disposed, 1);
  assert.equal(material.disposed, 1);
  assert.equal(map.disposed, 1);
  assert.equal(edges.disposed, 1);
  assert.equal(edgeMaterial.disposed, 0, 'a shared material stays');
  assert.equal(stencilMaterial.disposed, 0);
});

test('disposeTree frees material lists and shader uniform textures', () => {
  const a = new Resource('a'), b = new Resource('b');
  const texture = new Texture('uniform');
  b.uniforms = { color: { value: 0xff0000 }, map: { value: texture }, empty: null };
  const mesh = new Node({ geometry: new Resource('g'), material: [a, b] });
  disposeTree(mesh);
  assert.equal(a.disposed, 1);
  assert.equal(b.disposed, 1);
  assert.equal(texture.disposed, 1);
});

test('disposeTree keeps shared geometries and removes labels from the page', () => {
  const plane = share(new Resource('cap plane'));
  let removed = 0;
  const label = new Node({ element: { remove() { removed += 1; } } });
  const cap = new Node({ geometry: plane, material: share(new Resource('cap')) }).add(label);
  disposeTree(cap);
  assert.equal(plane.disposed, 0);
  assert.equal(removed, 1);
});

test('clearGroup frees the children and empties the group', () => {
  const g1 = new Resource('g1'), g2 = new Resource('g2');
  const group = new Node().add(new Node({ geometry: g1 }), new Node({ geometry: g2 }));
  clearGroup(group);
  assert.equal(group.children.length, 0);
  assert.equal(g1.disposed, 1);
  assert.equal(g2.disposed, 1);
});
