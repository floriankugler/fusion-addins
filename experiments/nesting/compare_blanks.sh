#!/bin/bash
# The blank strategies on the 62 parts and on twice as many.
cd "$(dirname "$0")"
P=.venv/bin/python
ALIGNED="--blank-lengths 2000 1600 1233 866 822 466 --blank-widths 1240 1000 800 618 436 413 236"
for w in b15 b15x2; do
  nest=20; [ $w = b15x2 ] && nest=40
  $P blanks.py out/jobs/${w}_bed.json --strategy baseline patterns --out out/cmp/$w/patterns --nest-seconds $nest
  $P blanks.py out/jobs/${w}_bed.json --strategy twostep --out out/cmp/$w/ts_default --min-strip 0 --refill 10 --nest-seconds $nest
  $P blanks.py out/jobs/${w}_bed.json --strategy twostep --out out/cmp/$w/ts_area --min-strip 0 --refill 10 --blank-cost 0 --nest-seconds $nest
  $P blanks.py out/jobs/${w}_bed.json --strategy twostep --out out/cmp/$w/ts_aligned --min-strip 0 --refill 10 $ALIGNED --nest-seconds $nest
  $P blanks.py out/jobs/${w}_bed.json --strategy twostep --out out/cmp/$w/ts_aligned_dear --min-strip 0 --refill 10 $ALIGNED --blank-cost 200000 --nest-seconds $nest
done
