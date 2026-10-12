// The preview page's bookkeeping that needs no three.js and no DOM, so that
// `node --test lang/preview/viewer/tests/` can check it: the layout version
// the page reads, the hidden parts, and the promises of `preview.loaded()`
// and `preview.open()`.

// The layout file version this page draws (lang/core/layout_types.py
// LAYOUT_VERSION). A layout of another version is not drawn; the status
// line says so.
export const LAYOUT_VERSION = 3;

/** Why the page cannot draw `layout`, or null when it can. */
export function layoutVersionProblem(layout) {
  const version = layout?.version;
  if (version === LAYOUT_VERSION) return null;
  return `layout version ${version ?? 'missing'}, this viewer reads ${LAYOUT_VERSION}`;
}

// -- hidden parts ----------------------------------------------------------
//
// `hidden` is the Set of the hidden parts' paths. The page changes it only
// through these, then refreshes the scene, the parts list and the selection.

/** Hides the paths (`on`) or shows them. */
export function setHidden(hidden, paths, on) {
  for (const path of paths) {
    if (on) hidden.add(path); else hidden.delete(path);
  }
}

/** Whether toggling the paths hides them: it shows them only when all are hidden. */
export function toggleHides(hidden, paths) {
  return !paths.every((path) => hidden.has(path));
}

/**
 * Hides every path of `all` except those in `keep`. With `toggle`, when
 * they already are the only ones shown, shows everything again instead.
 * Returns whether the paths are isolated afterwards.
 */
export function isolate(hidden, all, keep, { toggle = false } = {}) {
  const kept = new Set(keep);
  const others = all.filter((path) => !kept.has(path));
  if (toggle && others.every((path) => hidden.has(path)) && [...kept].every((path) => !hidden.has(path))) {
    hidden.clear();
    return false;
  }
  hidden.clear();
  for (const path of others) hidden.add(path);
  return true;
}

// -- loading -----------------------------------------------------------------

/**
 * The shown design's scene and builds, and the promises waiting for them.
 *
 * `loaded(after)` resolves with the version on screen once there is one
 * (other than `after`). It rejects with the build's log when the latest
 * build failed and nothing is on screen, or a build finished after the call
 * and failed; with the reason when the latest version could not be drawn;
 * and when the page switches from one design to another.
 *
 * `opened()` (for `preview.open()`) settles once the design's latest build
 * is on screen: it resolves when that build went through, rejects with its
 * log when it failed (the last good scene stays), or with the reason when
 * its scene could not be drawn, or when the page switches designs.
 *
 * The page reports: `shown(version)` when a scene is on screen,
 * `failed(reason)` when one could not be drawn, `reported(build)` with each
 * state of the design's build from the server, after it drew a newer
 * version, and `switched(from, to)` when it shows another design.
 */
export class LoadTracker {
  constructor() {
    this.version = null;    // the version on screen, null when nothing is
    this.build = null;      // the latest {builds, state, version, log} from the server
    this.error = null;      // why nothing (newer) is on screen: a failed build's log or a scene not drawn
    this.loads = [];        // loaded() calls: {after, builds, resolve, reject}
    this.opens = [];        // opened() calls: {resolve, reject}
  }

  loaded(after) {
    if (this.version !== null && this.version !== after) return Promise.resolve(this.version);
    if (this.version === null && this.error !== null) return Promise.reject(new Error(this.error));
    return new Promise((resolve, reject) => {
      this.loads.push({ after, builds: this.build?.builds ?? -1, resolve, reject });
    });
  }

  opened() {
    return new Promise((resolve, reject) => this.opens.push({ resolve, reject }));
  }

  shown(version) {
    this.version = version;
    this.error = null;
    this.loads = this.loads.filter((call) => {
      if (call.after === version) return true;
      call.resolve(version);
      return false;
    });
  }

  failed(reason) {
    this.error = reason;
    for (const call of this.loads.splice(0)) call.reject(new Error(reason));
    for (const call of this.opens.splice(0)) call.reject(new Error(reason));
  }

  reported({ builds, state, version, log }) {
    this.build = { builds, state, version, log };
    if (state === 'building') {
      this.error = null;
      return;
    }
    if (state === 'failed') {
      if (this.version === null) this.error = log;
      this.loads = this.loads.filter((call) => {
        if (this.version !== null && call.builds >= builds) return true;   // waits for a build after the call
        call.reject(new Error(log));
        return false;
      });
    }
    if (version === this.version) {     // the latest build is on screen, or none and nothing is
      for (const call of this.opens.splice(0)) {
        if (state === 'ok') call.resolve(version); else call.reject(new Error(log));
      }
    } else if (this.error !== null) {   // its scene could not be drawn
      for (const call of this.opens.splice(0)) call.reject(new Error(this.error));
    }
  }

  switched(from, to) {
    const error = new Error(`switched to ${to}`);
    for (const call of this.opens.splice(0)) call.reject(error);
    // The first design the page shows is no switch: loaded() calls made
    // before it wait for its scene.
    if (from !== null) for (const call of this.loads.splice(0)) call.reject(error);
    this.version = this.build = this.error = null;
  }
}
