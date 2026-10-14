// Run SVGnest's own code (vendor/SVGnest, unmodified) headless in node.
//
//     node experiments/nesting/svgnest/nest.mjs job.json result.json
//
// SVGnest is browser code: its genetic algorithm and the calls to its
// workers live in svgnest.js, the no-fit polygons in util/geometryutil.js
// (orbiting) and in svgnest.js (Clipper's Minkowski sum), the placement in
// util/placementworker.js. They are loaded as they are into one vm context,
// with stand-ins for what the browser gave them:
//
// - Parallel (web workers): runs the mapped function in this thread, on a
//   clone of the data as a worker would get it, and calls back
//   asynchronously as a worker would.
// - SvgParser (the DOM): the job's polygons are the SVG elements, and
//   `polygonify` returns their points. SVGnest still cleans them
//   (`cleanPolygon`), builds its part tree (a polygon whose first point lies
//   inside another becomes its hole) and offsets them for the spacing.
// - setInterval: the loop that starts one evaluation after the other is
//   driven here, as fast as the evaluations finish.
// - Math.random: seeded (mulberry32), so a run can be repeated.
//
// The job (written by jobs.py):
//   {parts: [{id, rings: [exterior, ...holes]}], bin: {rings: [exterior]},
//    config: {spacing, rotations, populationSize, mutationRate, useHoles,
//             exploreConcave, curveTolerance},
//    seed, evaluations, seconds}
// The result: for each bin SVGnest opened, the parts on it with their
// rotation (degrees, counter-clockwise) and translation, mapped back to the
// job's own coordinates (placed = R(rotation) p + [tx, ty] for a point p of
// the part's rings); the parts it did not place; and the history of each
// improvement.

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const vendor = path.resolve(here, '../vendor/SVGnest');

function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Fixes applied to SVGnest's source as it is loaded, when a job asks for
// them (`job.patches`); the vendored files stay as they are.
const PATCHES = {
  // svgnest.js builds its part tree with `children` but reads a part's holes
  // as `childNodes`, in the no-fit polygons for `useHoles` and in the spacing
  // offset of holes: parts never go into holes, and holes are not shrunk by
  // the spacing.
  holes: [
    ['useHoles && A.childNodes && A.childNodes.length > 0', 'useHoles && A.children && A.children.length > 0'],
    ['for(var i=0; i<A.childNodes.length; i++){', 'for(var i=0; i<A.children.length; i++){'],
    ['GeometryUtil.getPolygonBounds(A.childNodes[i])', 'GeometryUtil.getPolygonBounds(A.children[i])'],
    ['GeometryUtil.noFitPolygon(A.childNodes[i],B,true,searchEdges)', 'GeometryUtil.noFitPolygon(A.children[i],B,true,searchEdges)'],
    ['if(t[i].childNodes && t[i].childNodes.length > 0){', 'if(t[i].children && t[i].children.length > 0){'],
    ['offsetTree(t[i].childNodes, -offset, offsetFunction);', 'offsetTree(t[i].children, -offset, offsetFunction);'],
  ],
  // launchWorkers keeps only the no-fit polygons the last evaluation used
  // ("only keep cache for one cycle"), so the next one computes again most
  // of what an earlier one had. Keep them all: a pair's no-fit polygon
  // depends only on the two parts and their turns.
  cache: [
    ['nfpCache = newCache;', 'for(var k in newCache){ nfpCache[k] = newCache[k]; }'],
  ],
};

function source(file, patches) {
  let src = fs.readFileSync(path.join(vendor, file), 'utf8');
  for (const name of patches) {
    for (const [from, to] of PATCHES[name] || []) {
      if (file !== 'svgnest.js') continue;
      if (!src.includes(from)) throw new Error(`patch ${name}: not found in ${file}: ${from}`);
      src = src.split(from).join(to);
    }
  }
  return src;
}

export function loadSvgNest(seed, patches = []) {
  for (const name of patches) if (!PATCHES[name]) throw new Error(`unknown patch ${name}`);
  const ctx = { console, navigator: { userAgent: 'node', appName: 'node' } };
  ctx.window = ctx;
  ctx.self = ctx;
  vm.createContext(ctx);
  vm.runInContext('Math', ctx).random = mulberry32(seed);
  // A worker's copy of its data, made in the context's own realm: arrays
  // keep their other properties (a polygon's id, rotation, children) and
  // cycles (a hole's parent), as structured cloning keeps them.
  const clone = vm.runInContext(`(function clone(v, seen = new Map()) {
    if (v === null || typeof v !== 'object') return v;
    if (seen.has(v)) return seen.get(v);
    const out = Array.isArray(v) ? [] : {};
    seen.set(v, out);
    for (const k of Object.keys(v)) out[k] = clone(v[k], seen);
    return out;
  })`, ctx);

  // The interval SVGnest starts in start(); driven by run() below.
  ctx.__interval = null;
  ctx.setInterval = (fn) => { ctx.__interval = fn; return 1; };
  ctx.clearInterval = () => { ctx.__interval = null; };

  ctx.__timing = { nfp: 0, placement: 0, pairs: 0 };
  ctx.Parallel = class {
    constructor(data, options) { this.data = data; this.env = (options && options.env) || {}; }
    require() { return this; }
    map(fn) {
      const data = clone(this.data);
      const env = this.env;
      return {
        then(ok, fail) {
          setImmediate(() => {
            let out;
            try {
              ctx.global = { env };
              const t = performance.now();
              out = data.map((item) => fn(item));
              // The no-fit polygons are mapped over pairs, the placement over
              // one list of parts.
              const kind = env.self ? 'placement' : 'nfp';
              ctx.__timing[kind] += performance.now() - t;
              if (kind === 'nfp') ctx.__timing.pairs += data.length;
            } catch (e) {
              if (fail) { fail(e); return; }
              throw e;
            }
            ok(out);
          });
        },
      };
    }
  };

  ctx.SvgParser = {
    _svg: null,
    config() {},
    load(svg) { this._svg = svg; return svg; },
    getStyle() { return null; },
    clean() { return this._svg; },
    polygonify(el) { return el.points.map(([x, y]) => ({ x, y })); },
  };

  for (const f of ['util/clipper.js', 'util/geometryutil.js', 'util/placementworker.js', 'svgnest.js']) {
    vm.runInContext(source(f, patches), ctx, { filename: f });
  }
  return ctx;
}

// The job's polygons as SVGnest's elements: each part's exterior and holes
// moved by an offset of its own, so that no part lies inside another (which
// SVGnest would take for a hole); the bin last.
function elements(job) {
  const els = [];
  const owner = [];
  const offsets = [];
  let x = 0;
  job.parts.forEach((part, i) => {
    const xs = part.rings[0].map((p) => p[0]);
    const off = [x - Math.min(...xs), 0];
    offsets.push(off);
    x += Math.max(...xs) - Math.min(...xs) + 1000;
    for (const ring of part.rings) {
      els.push({ points: ring.map(([px, py]) => [px + off[0], py + off[1]]) });
      owner.push(i);
    }
  });
  const bin = { points: job.bin.rings[0] };
  els.push(bin);
  return { els, owner, offsets, bin };
}

export async function run(job, log = () => {}) {
  const ctx = loadSvgNest(job.seed ?? 1, job.patches || []);
  const nest = ctx.SvgNest;
  const { els, owner, offsets, bin } = elements(job);

  // Keep the tree SVGnest builds in start(), to map its ids back.
  let tree = null;
  const getParts = nest.getParts;
  nest.getParts = function (paths) { tree = getParts.call(this, paths); return tree; };
  // Return the raw placements instead of SVG elements.
  nest.applyPlacement = (placement) => placement;

  nest.config(job.config || {});
  nest.parsesvg({ childNodes: els });
  nest.setbin(bin);

  // Where start() puts the bin: cleaned, offset inwards by half the spacing
  // (only when that gives one polygon), then moved to the origin. Done here
  // the same way, to map placements back.
  const config = nest.config();
  let binPoly = nest.cleanPolygon(ctx.SvgParser.polygonify(bin));
  let binOffsetApplied = false;
  if (config.spacing > 0) {
    const off = nest.polygonOffset(binPoly, -0.5 * config.spacing);
    if (off.length === 1) { binPoly = off[0]; binOffsetApplied = true; }
  }
  const binMin = [Math.min(...binPoly.map((p) => p.x)), Math.min(...binPoly.map((p) => p.y))];

  const history = [];
  let best = null;
  let evaluations = 0;
  const t0 = performance.now();
  const started = nest.start(() => {}, (placement, utilisation, placed, total) => {
    evaluations += 1;
    if (placement) {
      best = { placement, utilisation, placed, total, evaluation: evaluations, seconds: (performance.now() - t0) / 1000 };
      history.push({ evaluation: evaluations, seconds: best.seconds, bins: placement.length, placed, utilisation });
      log(`#${evaluations} ${best.seconds.toFixed(1)}s: ${placement.length} bins, ${placed}/${total} placed, utilisation ${(utilisation * 100).toFixed(1)}%`);
    }
  });
  if (started === false) throw new Error('SVGnest did not start (bin not a polygon?)');

  const maxEval = job.evaluations ?? 100;
  const maxSec = job.seconds ?? 60;
  while (evaluations < maxEval && (performance.now() - t0) / 1000 < maxSec) {
    if (ctx.__interval) ctx.__interval();
    await new Promise((r) => setImmediate(r));
  }
  nest.stop();
  const seconds = (performance.now() - t0) / 1000;

  // Map the best placement back to the job's parts.
  const bins = [];
  const placedIds = new Set();
  for (const binPlacements of best ? best.placement : []) {
    const out = [];
    for (const p of binPlacements) {
      const index = owner[tree[p.id].source];
      const a = (p.rotation * Math.PI) / 180;
      const [c, s] = [Math.cos(a), Math.sin(a)];
      const [ox, oy] = offsets[index];
      out.push({
        id: job.parts[index].id,
        index,
        rotation: p.rotation,
        translation: [c * ox - s * oy + p.x + binMin[0], s * ox + c * oy + p.y + binMin[1]],
      });
      placedIds.add(index);
    }
    bins.push(out);
  }
  const unplaced = job.parts.map((p, i) => i).filter((i) => !placedIds.has(i)).map((i) => job.parts[i].id);
  return {
    solver: 'svgnest', seed: job.seed ?? 1, patches: job.patches || [], config, binOffsetApplied,
    evaluations, seconds, bestAt: best && { evaluation: best.evaluation, seconds: best.seconds },
    timing: { nfpSeconds: ctx.__timing.nfp / 1000, placementSeconds: ctx.__timing.placement / 1000, nfpPairs: ctx.__timing.pairs },
    bins, unplaced, history,
  };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const [jobFile, outFile] = process.argv.slice(2);
  if (!jobFile || !outFile) {
    console.error('usage: node nest.mjs job.json result.json');
    process.exit(2);
  }
  const job = JSON.parse(fs.readFileSync(jobFile, 'utf8'));
  const result = await run(job, (m) => console.error(m));
  fs.writeFileSync(outFile, JSON.stringify(result, null, 1));
  const tm = result.timing;
  console.error(`${result.evaluations} evaluations in ${result.seconds.toFixed(1)} s (no-fit polygons ${tm.nfpSeconds.toFixed(1)} s for ${tm.nfpPairs} pairs, placement ${tm.placementSeconds.toFixed(1)} s); best: ${result.bins.length} bins, ${result.unplaced.length} unplaced`);
}
