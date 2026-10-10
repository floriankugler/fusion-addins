# Compile-speed benchmark, 2026-10-10

Fusion 2705.1.30, macOS, no other documents open.
Workload and cell names: see `tools/perf/compile_bench.py`. One pair = one
tenon board (28-line outline, chamfer on all top edges) + one mortise board
(six slot mortises, eight holes + pocket on the top face, two holes into a
narrow face). Default cells are batched, tenon outline, distance extents.

Cells named `*_repeat` and `*_late` ran after the Fusion session had
degraded (see notes) and are not valid. `*_repeat2` and `*_fresh` ran after
a Fusion restart and confirm the first runs within 3%.

| Cell | Design | Pairs | Features | Sketch entities | Total s | First pair s | Last pair s | Growth |
|---|---|---|---|---|---|---|---|---|
| direct_best_p60 | direct deferred+brep | 60 | 660 | 900 | 12.8 | 0.06 | 0.34 | 5.4x |
| direct_brep2_p30 | direct brep | 30 | 330 | 450 | 4.1 | 0.07 | 0.19 | 2.9x |
| direct_brep_p30 | direct brep | 30 | 360 | 1170 | 5.6 | 0.11 | 0.26 | 2.4x |
| direct_deferred_p30 | direct deferred | 30 | 420 | 2010 | 5.6 | 0.07 | 0.27 | 3.7x |
| direct_p15 | direct | 15 | 210 | 1005 | 2.4 | 0.11 | 0.19 | 1.7x |
| direct_p30 | direct | 30 | 420 | 2010 | 6.5 | 0.11 | 0.31 | 2.7x |
| direct_p30_repeat | direct | 30 | 420 | 2010 | 49.6 | 0.75 | 2.46 | 3.3x |
| direct_p30_repeat2 | direct | 30 | 420 | 2010 | 6.3 | 0.11 | 0.30 | 2.7x |
| direct_p5 | direct | 5 | 70 | 335 | 0.8 | 0.12 | 0.14 | 1.1x |
| direct_p5_fresh | direct | 5 | 70 | 335 | 0.7 | 0.11 | 0.13 | 1.2x |
| direct_p5_late | direct | 5 | 70 | 335 | 5.0 | 0.79 | 0.96 | 1.2x |
| direct_p60 | direct | 60 | 840 | 4020 | 21.4 | 0.12 | 0.62 | 5.4x |
| direct_plain_p30 | direct plain | 30 | 420 | 1290 | 4.5 | 0.09 | 0.20 | 2.3x |
| direct_toobj_p30 | direct to-object | 30 | 420 | 2010 | 6.9 | 0.12 | 0.32 | 2.6x |
| direct_unbatched_p15 | direct unbatched | 15 | 405 | 1005 | 3.1 | 0.13 | 0.28 | 2.2x |
| param_best_p30 | parametric deferred+brep | 30 | 420 | 1170 | 15.7 | 0.12 | 0.94 | 7.6x |
| param_brep2_p30 | parametric brep | 30 | 600 | 450 | 23.8 | 0.17 | 1.55 | 9.0x |
| param_brep_p30 | parametric brep | 30 | 420 | 1170 | 22.1 | 0.20 | 1.36 | 6.9x |
| param_deferred_p30 | parametric deferred | 30 | 420 | 2010 | 19.6 | 0.12 | 1.24 | 10.5x |
| param_p15 | parametric | 15 | 210 | 1005 | 8.9 | 0.22 | 1.00 | 4.6x |
| param_p30 | parametric | 30 | 420 | 2010 | 31.6 | 0.21 | 2.06 | 9.8x |
| param_p30_repeat | parametric | 30 | 420 | 2010 | 208.0 | 1.41 | 12.93 | 9.2x |
| param_p30_repeat2 | parametric | 30 | 420 | 2010 | 31.5 | 0.21 | 2.04 | 9.5x |
| param_p5 | parametric | 5 | 70 | 335 | 1.6 | 0.22 | 0.40 | 1.8x |
| param_p60 | parametric | 60 | 840 | 4020 | 135.5 | 0.22 | 4.68 | 21.5x |
| param_plain_p30 | parametric plain | 30 | 420 | 1290 | 23.5 | 0.17 | 1.51 | 8.8x |
| param_toobj_p30 | parametric to-object | 30 | 420 | 2010 | 32.6 | 0.22 | 2.11 | 9.4x |
| param_unbatched_p15 | parametric unbatched | 15 | 405 | 1005 | 15.9 | 0.26 | 1.97 | 7.5x |

direct_p30 (6.5 s total):
  sketch_line              1.51 s   1320 calls  avg    1.1 ms  max    3.4 ms
  hole_face                0.88 s     30 calls  avg   29.3 ms  max   50.1 ms
  sketch_arc               0.74 s    360 calls  avg    2.0 ms  max    3.7 ms
  chamfer                  0.55 s     30 calls  avg   18.3 ms  max   24.2 ms
  extrude_new              0.49 s     60 calls  avg    8.1 ms  max   15.4 ms
  extrude_cut_mortise      0.44 s     30 calls  avg   14.5 ms  max   20.4 ms
  hole_edge                0.32 s     30 calls  avg   10.5 ms  max   18.6 ms
  extrude_cut_pocket       0.25 s     30 calls  avg    8.5 ms  max   14.9 ms
param_brep_p30 (22.1 s total):
  sketch_line              3.20 s    480 calls  avg    6.7 ms  max   14.5 ms
  sketch_arc               2.60 s    360 calls  avg    7.2 ms  max   14.7 ms
  sketch_point             2.36 s    300 calls  avg    7.9 ms  max   15.6 ms
  extrude_cut_mortise      1.58 s     30 calls  avg   52.7 ms  max   91.4 ms
  base_feature             1.33 s     30 calls  avg   44.3 ms  max   79.9 ms
  sketch_holes             1.23 s     30 calls  avg   40.9 ms  max   72.0 ms
  chamfer                  1.09 s     30 calls  avg   36.3 ms  max   58.5 ms
  sketch_edge              0.97 s     30 calls  avg   32.2 ms  max   62.0 ms
param_deferred_p30 (19.6 s total):
  extrude_new              2.06 s     60 calls  avg   34.4 ms  max   70.4 ms
  extrude_cut_mortise      1.93 s     30 calls  avg   64.2 ms  max  118.3 ms
  sketch_outline           1.92 s     60 calls  avg   32.0 ms  max   68.0 ms
  sketch_line              1.72 s   1320 calls  avg    1.3 ms  max    5.3 ms
  plane                    1.49 s     60 calls  avg   24.9 ms  max   52.8 ms
  sketch_holes             1.46 s     30 calls  avg   48.5 ms  max   89.2 ms
  chamfer                  1.21 s     30 calls  avg   40.2 ms  max   68.4 ms
  sketch_edge              1.20 s     30 calls  avg   39.9 ms  max   81.3 ms
param_p30 (31.6 s total):
  sketch_line              9.67 s   1320 calls  avg    7.3 ms  max   18.0 ms
  sketch_arc               3.15 s    360 calls  avg    8.8 ms  max   18.0 ms
  sketch_point             2.82 s    300 calls  avg    9.4 ms  max   18.5 ms
  extrude_new              2.05 s     60 calls  avg   34.2 ms  max   70.0 ms
  extrude_cut_mortise      1.91 s     30 calls  avg   63.8 ms  max  116.0 ms
  sketch_outline           1.90 s     60 calls  avg   31.6 ms  max   67.4 ms
  plane                    1.48 s     60 calls  avg   24.7 ms  max   53.0 ms
  sketch_holes             1.43 s     30 calls  avg   47.8 ms  max   90.0 ms

wrote tools/perf/results/2026-10-10/growth.svg

## Notes

- After about 25 document create/close cycles and two days of Fusion
  uptime, every modifying API call got uniformly 6-7x slower (compare
  `direct_p5` with `direct_p5_late`), in new documents too, while Python
  loops and read-only API calls inside Fusion stayed at full speed and
  Fusion idled at 0.2% CPU with 20 GB resident. A Fusion restart cleared it
  (`direct_p5_fresh`). Cause unknown; the compiler will create many
  documents per session, so watch for it.
