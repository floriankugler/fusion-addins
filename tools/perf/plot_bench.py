"""Summarise compile_bench results: a Markdown table and an SVG growth plot.

    python3 tools/perf/plot_bench.py <results_dir> [<out.svg>]

Runs outside Fusion with the standard library only. The plot shows the
time per pair (one tenon board plus one mortise board) against the pair
index, one line per cell, so the growth of the write cost with document
size is visible directly.
"""
import json
import os
import sys


def load(results_dir):
    cells = []
    for name in sorted(os.listdir(results_dir)):
        if not name.endswith('.json') or name.startswith('smoke'):
            continue
        with open(os.path.join(results_dir, name)) as fh:
            cells.append(json.load(fh))
    return cells


def per_pair(cell):
    totals = {}
    for r in cell['records']:
        if r['pair'] >= 0:
            totals[r['pair']] = totals.get(r['pair'], 0.0) + r['dt']
    return [totals[k] for k in sorted(totals)]


def table(cells):
    rows = ['| Cell | Design | Pairs | Features | Sketch entities | Total s | First pair s | Last pair s | Growth |',
            '|---|---|---|---|---|---|---|---|---|']
    for c in cells:
        s, cfg = c['summary'], c['config']
        variant = []
        if not cfg['batched']:
            variant.append('unbatched')
        if cfg['outline'] == 'plain':
            variant.append('plain')
        if cfg['extent'] == 'to_object':
            variant.append('to-object')
        if cfg['sketch_deferred']:
            variant.append('deferred')
        if cfg['profile_source'] == 'brep':
            variant.append('brep')
        growth = s['last_pair_s'] / s['first_pair_s'] if s['first_pair_s'] else 0
        rows.append('| %s | %s%s | %d | %d | %d | %.1f | %.2f | %.2f | %.1fx |' % (
            s['label'], cfg['design'], ' ' + '+'.join(variant) if variant else '',
            cfg['pairs'], s['features'], s['sketch_entities'], s['total_s'],
            s['first_pair_s'], s['last_pair_s'], growth))
    return '\n'.join(rows)


def by_kind(cells, labels):
    """Time share per feature kind for the named cells."""
    out = []
    for c in cells:
        if c['summary']['label'] not in labels:
            continue
        kinds = sorted(c['summary']['by_kind'].items(), key=lambda kv: -kv[1]['total'])
        out.append('%s (%.1f s total):' % (c['summary']['label'], c['summary']['total_s']))
        for kind, v in kinds[:8]:
            out.append('  %-22s %6.2f s  %5d calls  avg %6.1f ms  max %6.1f ms' % (
                kind, v['total'], v['count'], 1000 * v['total'] / v['count'], 1000 * v['max']))
    return '\n'.join(out)


PALETTE = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
           '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#393b79', '#637939',
           '#8c6d31', '#843c39', '#7b4173', '#3182bd']


def svg(cells, path, labels=None, max_pairs=None, max_seconds=None):
    width, height, ml, mr, mt, mb = 900, 520, 60, 20, 30, 50
    series = [(c['summary']['label'], per_pair(c)) for c in cells
              if labels is None or c['summary']['label'] in labels]
    xmax = max_pairs or max(len(s) for _, s in series)
    ymax = max_seconds or max(max(s) for _, s in series)
    pw, ph = width - ml - mr, height - mt - mb

    def X(i):
        return ml + pw * i / max(1, xmax - 1)

    def Y(v):
        return mt + ph * (1 - v / ymax)

    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="sans-serif" font-size="12">' % (width, height),
             '<rect width="100%" height="100%" fill="white"/>']
    for k in range(6):
        v = ymax * k / 5
        parts.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#ddd"/>' % (ml, Y(v), ml + pw, Y(v)))
        parts.append('<text x="%d" y="%.1f" text-anchor="end" dy="4">%.1f s</text>' % (ml - 6, Y(v), v))
    for i in range(0, xmax, max(1, xmax // 10)):
        parts.append('<text x="%.1f" y="%d" text-anchor="middle">%d</text>' % (X(i), height - mb + 18, i + 1))
    parts.append('<text x="%d" y="%d" text-anchor="middle">pair index (one tenon board + one mortise board each)</text>' % (ml + pw / 2, height - 8))
    parts.append('<text x="%d" y="%d" transform="rotate(-90 14 %d)" text-anchor="middle">seconds per pair</text>' % (14, mt + ph / 2, mt + ph / 2))
    for n, (label, values) in enumerate(series):
        color = PALETTE[n % len(PALETTE)]
        pts = ' '.join('%.1f,%.1f' % (X(i), Y(min(v, ymax))) for i, v in enumerate(values))
        parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.6"/>' % (pts, color))
        # Legend inside the plot, top left, where the curves leave room.
        ly = mt + 14 + 16 * n
        parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (ml + 16, ly, ml + 38, ly, color))
        parts.append('<text x="%d" y="%d" dy="4">%s</text>' % (ml + 44, ly, label))
    parts.append('</svg>')
    with open(path, 'w') as fh:
        fh.write('\n'.join(parts))


if __name__ == '__main__':
    results_dir = sys.argv[1]
    cells = load(results_dir)
    print(table(cells))
    print()
    print(by_kind(cells, {'param_p30', 'direct_p30', 'param_deferred_p30', 'param_brep_p30'}))
    if len(sys.argv) > 2:
        # Only the cells that tell the story; the table has the rest.
        svg(cells, sys.argv[2], labels={
            'param_p60', 'param_p30', 'param_best_p30', 'param_unbatched_p15',
            'direct_p60', 'direct_p30', 'direct_best_p60'})
        print('\nwrote', sys.argv[2])
