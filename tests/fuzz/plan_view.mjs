// The nest view's CAM layer (lang/preview/viewer/cam.js) on one plan, for
// plan_views.py: reads {plan, sheets, labels} as JSON on stdin (`sheets`:
// per "<material>\n<sheet>" the sheet's rect in the drawing, {x, y,
// height}; `labels`: per part path its name's place, {x, y, size}) and
// writes what the page would list and draw as JSON on stdout.
import { readFileSync } from 'node:fs';
import { legend, chosenOperation, releaseRanks, tabPositions, toolColors, setupOverlay, planNotes } from '../../lang/preview/viewer/cam.js';

const { plan, sheets, labels } = JSON.parse(readFileSync(0, 'utf8'));
const colors = toolColors(plan);
const features = (elements) => elements.filter((e) => e.attrs.class.startsWith('cam-feature'));

const setups = plan.setups.map((setup) => {
  const sheet = sheets[`${setup.stock.material}\n${setup.stock.sheet}`] ?? null;
  const n = setup.operations.length;
  return {
    sheet: sheet !== null,
    ranks: [...releaseRanks(setup)],
    tabs: tabPositions(setup),
    choices: [-1, ...setup.operations.keys(), n, 'all'].map((index) => chosenOperation(plan, { setup: setup.name, index })),
    ...(sheet === null ? {} : {
      plain: setupOverlay(setup, { sheet, colors, labels }),
      ops: setup.operations.map((_op, index) => features(setupOverlay(setup, { sheet, chosen: { setup: setup.name, index }, colors }))),
      all: features(setupOverlay(setup, { sheet, chosen: { setup: setup.name, index: 'all' }, colors })).length,
    }),
  };
});

process.stdout.write(JSON.stringify({ legend: legend(plan), colors: [...colors], setups, notes: planNotes(plan) }));
