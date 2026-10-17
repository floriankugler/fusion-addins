// Scene helpers of the preview page that need no three.js import, so that
// `node --test lang/preview/viewer/tests/` can check them against stubs.

/** The index of a layout axis name in a vector: AXIS.y === 1. */
export const AXIS = Object.freeze({ x: 0, y: 1, z: 2 });

/** The default oblique view: the direction from the target toward the eye, not normalised. */
export const ISO = Object.freeze([-1, -1.2, 0.8]);

/** World up: z is up in the layout. */
export const UP = Object.freeze([0, 0, 1]);

// Geometries, materials and textures that outlive the content they are
// used in (one edge material for all parts, the cap materials per colour),
// which disposeTree() leaves alone.
const shared = new WeakSet();

/** Marks a resource as shared, so that disposeTree() keeps it; returns it. */
export function share(resource) {
  shared.add(resource);
  return resource;
}

/**
 * Frees the GPU resources of an object and everything below it that is
 * not shared: geometries, materials (also a list of them) and their
 * textures, also those in a shader's uniforms. Removes CSS labels' elements
 * from the page. Call it on content that is taken off the scene for good.
 */
export function disposeTree(root) {
  const seen = new Set();
  const dispose = (resource) => {
    if (!resource || seen.has(resource) || shared.has(resource)) return;
    seen.add(resource);
    resource.dispose();
  };
  root.traverse((object) => {
    dispose(object.geometry);
    for (const material of [object.material].flat()) {
      if (!material || seen.has(material) || shared.has(material)) continue;
      for (const value of Object.values(material)) if (value?.isTexture) dispose(value);
      for (const uniform of Object.values(material.uniforms ?? {})) if (uniform?.value?.isTexture) dispose(uniform.value);
      dispose(material);
    }
    if (object.isCSS2DObject) object.element.remove();
  });
}

/** Empties a group of rebuilt content, freeing what its children hold. */
export function clearGroup(group) {
  for (const child of group.children) disposeTree(child);
  group.clear();
}

/** The bounds of rings of [u, v] points: [u0, v0, u1, v1]. */
export function ringBounds(rings) {
  let u0 = Infinity, v0 = Infinity, u1 = -Infinity, v1 = -Infinity;
  for (const ring of rings) {
    for (const [u, v] of ring) {
      if (u < u0) u0 = u;
      if (u > u1) u1 = u;
      if (v < v0) v0 = v;
      if (v > v1) v1 = v;
    }
  }
  return [u0, v0, u1, v1];
}

/**
 * A point of a part's operation, in world mm: the centre of a hole, pocket,
 * cut or V-groove on the face it is made from (`frame` the layout's, which
 * names the faces' directions). Throws for one without a point (a chamfer).
 */
export function opPoint(frame, part, op) {
  const axes = part.axes, b = part.box;
  const inner = op.kind === 'edge' ? op.op : op;
  const code = frame[op.face ?? inner.face] ?? null;
  const p = [0, 0, 0];
  let a, c;
  if (op.kind === 'edge') {
    const faceAxis = code[1];
    const s = faceAxis === axes.u ? axes.v : axes.u;
    [a, c] = [op.s, op.t];
    const [u0, v0, u1, v1] = inner.kind === 'pocket' ? ringBounds(inner.shape) : [0, 0, 0, 0];
    p[AXIS[s]] = a + (u0 + u1) / 2; p[AXIS[axes.t]] = c + (v0 + v1) / 2;
  } else if (op.kind === 'hole') {
    p[AXIS[axes.u]] = op.u; p[AXIS[axes.v]] = op.v;
  } else if (op.kind === 'vgroove') {
    p[AXIS[axes.u]] = (op.start[0] + op.end[0]) / 2; p[AXIS[axes.v]] = (op.start[1] + op.end[1]) / 2;
  } else if (op.shape) {
    const [u0, v0, u1, v1] = ringBounds(op.shape);
    p[AXIS[axes.u]] = (u0 + u1) / 2; p[AXIS[axes.v]] = (v0 + v1) / 2;
  } else {
    throw new Error(`a ${op.kind} has no point to look at`);
  }
  if (code) {
    const i = AXIS[code[1]];
    p[i] = code[0] === '+' ? b.max[i] : b.min[i];
  } else {
    const i = AXIS[axes.t];
    p[i] = (b.min[i] + b.max[i]) / 2;
  }
  return p;
}
