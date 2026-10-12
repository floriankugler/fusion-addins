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
