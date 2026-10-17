// Freeing rebuilt content (scene-utils.js), against stand-ins for three.js
// objects that count their dispose() calls.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { AXIS, ISO, UP, share, disposeTree, clearGroup, ringBounds, opPoint } from '../scene-utils.js';

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

test('the bounds of rings', () => {
  assert.deepEqual(ringBounds([[[0, 5], [10, -2], [3, 8]], [[-1, 0], [2, 2]]]), [-1, -2, 10, 8]);
});

test('where an operation is: on the face it is made from, at its centre', () => {
  const frame = { front: '-y', back: '+y', left: '-x', right: '+x', top: '+z', bottom: '-z' };
  // a side standing at x 0..18, its u along y and v along z
  const part = { axes: { t: 'x', u: 'y', v: 'z' }, box: { min: [0, 0, 0], max: [18, 500, 700] } };
  assert.deepEqual(opPoint(frame, part, { kind: 'hole', face: 'right', u: 30, v: 40 }), [18, 30, 40]);
  assert.deepEqual(opPoint(frame, part, { kind: 'hole', face: 'left', u: 30, v: 40 }), [0, 30, 40]);
  assert.deepEqual(opPoint(frame, part, { kind: 'pocket', face: 'right', shape: [[[10, 10], [30, 10], [30, 50], [10, 50]]] }),
    [18, 20, 30]);
  assert.deepEqual(opPoint(frame, part, { kind: 'cut', shape: [[[0, 0], [100, 0], [100, 80], [0, 80]]] }), [9, 50, 40]);
  assert.deepEqual(opPoint(frame, part, { kind: 'vgroove', face: 'right', start: [0, 100], end: [500, 100] }), [18, 250, 100]);
  // an edge operation on the top face: along y at s, across the thickness at t
  assert.deepEqual(opPoint(frame, part, { kind: 'edge', face: 'top', s: 250, t: 9, op: { kind: 'hole', face: 'top', u: 0, v: 0 } }),
    [9, 250, 700]);
  assert.throws(() => opPoint(frame, part, { kind: 'chamfer', what: 'outline', face: 'right' }), /a chamfer has no point/);
});
