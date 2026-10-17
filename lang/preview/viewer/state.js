// The preview page's bookkeeping that needs no three.js and no DOM, so that
// `node --test lang/preview/viewer/tests/` can check it: the layout version
// the page reads, the build file's lines it links to the editor, the hidden
// parts, the level each design is meshed at, and the promises of
// `preview.loaded()`, `preview.open()` and `preview.level()`.

// The layout file version this page draws (lang/core/layout_types.py
// LAYOUT_VERSION). A layout of another version is not drawn; the status
// line says so.
export const LAYOUT_VERSION = 10;

/**
 * A part's settings (the layout's `settings`, lang/core/settings.py) as the
 * selection's info shows them, one line each with where it came from:
 * `chamfer_size 0.5: kitchen`, `material birch 15: kitchen.left`.
 */
export function settingsText(settings) {
  return Object.entries(settings ?? {}).map(([name, { value, source }]) =>
    `${name} ${typeof value === 'string' ? value : JSON.stringify(value)}: ${source}`).join('\n');
}

/** Why the page cannot draw `layout`, or null when it can. */
export function layoutVersionProblem(layout) {
  const version = layout?.version;
  if (version === LAYOUT_VERSION) return null;
  return `layout version ${version ?? 'missing'}, this viewer reads ${LAYOUT_VERSION}`;
}

// -- lines of the build file ------------------------------------------------

/** A line as the layout names it (`where`, `examples/van.py:45`) as its
 * file and line number; null for none ("", or no number). */
export function splitWhere(where) {
  const found = /^(.+):(\d+)$/.exec(where ?? '');
  return found ? { file: found[1], line: Number(found[2]) } : null;
}

// A Python file's line in a log: `examples/van.py:45`, a whole path too; no
// spaces, colons or quotes in the path.
const FILE_LINE = /([^\s:'"()]+\.py):(\d+)/g;

/** The build log as the status box shows it: per line of the text, its
 * pieces, each `{text}` or, for a file's line in it, `{text, file, line}`,
 * which the page makes a link that opens the editor there. */
export function logPieces(text) {
  return (text ?? '').split('\n').map((row) => {
    const pieces = [];
    let at = 0;
    for (const found of row.matchAll(FILE_LINE)) {
      if (found.index > at) pieces.push({ text: row.slice(at, found.index) });
      pieces.push({ text: found[0], file: found[1], line: Number(found[2]) });
      at = found.index + found[0].length;
    }
    if (at < row.length || !pieces.length) pieces.push({ text: row.slice(at) });
    return pieces;
  });
}

// -- the nest ---------------------------------------------------------------

/** A nest's state as the side panel says it (an entry of `nests` in
 * status.json): what it is, then what changed since it was nested or made. */
export function nestStatusText(nest) {
  const lines = [];
  if (nest?.follows) lines.push(`second nest of ${nest.follows}: what is not made of it`);
  const marked = nest?.state === 'made' || nest?.state === 'sheets';
  switch (nest?.state) {
    case 'ok': lines.push('its parts are as nested'); break;
    case 'changed': lines.push('parts changed since it was nested: nest again'); break;
    case 'made': lines.push('made, every sheet: frozen'); break;
    case 'sheets':
      lines.push(`made by sheets (${sheetNames(nest.made, nest.sheets)} of ${nest.sheets.length}): frozen`);
      break;
    case 'running': lines.push('nesting… (seconds to minutes)'); break;
    case 'failed': lines.push('the nest failed:\n' + (nest.log ?? '').trim()); break;
    default: lines.push(nest ? 'not nested yet: nest again, or python -m lang.nesting' : 'the layout lists no nest');
  }
  const listed = marked
    ? [['changed since made', nest.changed], ['not made', nest.not_made], ['new', nest.new], ['made, gone', nest.gone]]
    : [['changed', nest?.changed], ['new', nest?.new], ['gone', nest?.gone]];
  if (nest?.next) lines.push(`what it left was nested anew in ${nest.next}, made too`);
  for (const [label, paths] of listed) if (paths?.length) lines.push(`${label}: ${paths.join(', ')}`);
  if (marked && (nest.changed?.length || nest.not_made?.length || nest.new?.length)) {
    lines.push('nest again: they go into the next nest beside it');
  } else if (marked && nest.made_parts) {
    lines.push('every part of it is made');
  }
  return lines.join('\n');
}

/** Sheets ([material, name]) as the panel names them: by name, with the
 * material where the nest has several. */
export function sheetNames(sheets, all = sheets) {
  const several = new Set((all ?? []).map(([m]) => m)).size > 1;
  return (sheets ?? []).map(([m, s]) => (several ? `${m}:${s}` : s)).join(', ');
}

/** Whether a sheet ([material, name]) is among those marked made. */
export function sheetMade(nest, sheet) {
  return (nest?.made ?? []).some(([m, s]) => m === sheet[0] && s === sheet[1]);
}

/** Whether a part may be marked as fixed in a nest: made in it (it is
 * marked) and changed since. */
export function fixable(nest, path) {
  return (nest?.state === 'made' || nest?.state === 'sheets') && !nest.follows && (nest.changed ?? []).includes(path);
}

/** The nest the panel shows of a design's `nests` (status.json): the one
 * wanted (by path) if it is listed, else the first; null for none. */
export function chosenNest(nests, wanted) {
  if (!nests?.length) return null;
  return nests.find((n) => n.path === wanted) ?? nests[0];
}

// -- the level ---------------------------------------------------------------

/** The levels the preview meshes at (lang/preview/levels.py), finest first. */
export const LEVELS = ['fine', 'normal'];

/**
 * The levels the page asks the server to mesh the designs at. A level
 * picked for a design goes with its status requests (`query`) until the
 * server reports it as the design's (`reported`); the server keeps it
 * from then on, for every page.
 */
export class LevelChoice {
  constructor() {
    this.picked = new Map();    // design -> the level picked, not reported yet
  }

  pick(design, level) {
    if (!LEVELS.includes(level)) throw new Error(`no level ${JSON.stringify(level)}; there are ${LEVELS.join(', ')}`);
    this.picked.set(design, level);
  }

  /** What a status request for the design adds to its query: `&level=fine`, or nothing. */
  query(design) {
    const level = this.picked.get(design);
    return level ? `&level=${encodeURIComponent(level)}` : '';
  }

  /** The level the server reports for the design; returns the one the page shows: a level picked
   *  and not reported yet, else the server's. */
  reported(design, level) {
    if (this.picked.get(design) === level) this.picked.delete(design);
    return this.picked.get(design) ?? level;
  }
}

/**
 * Resolves with the version on screen once its scene is of the level
 * named: waits for scenes (`tracker.loaded`) until `levelOf()`, the level
 * of the scene on screen, is that one. Rejects as `loaded()` does.
 */
export async function untilLevel(tracker, levelOf, name) {
  let version = await tracker.loaded();
  while (levelOf() !== name) version = await tracker.loaded(version);
  return version;
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
