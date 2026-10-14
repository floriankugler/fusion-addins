#!/bin/bash
cd "$(dirname "$0")"
P=.venv/bin/python
$P blanks.py out/jobs/b15x2_bed.json --strategy patterns --out out/cmp2/b15x2/patterns --refill 10
$P blanks.py out/jobs/b15x2_bed.json --strategy twostep --out out/cmp2/b15x2/ts_default --min-strip 0 --refill 10 --nest-seconds 40
$P blanks.py out/jobs/b15x2_bed.json --strategy twostep --out out/cmp2/b15x2/ts_area --min-strip 0 --refill 10 --blank-cost 0 --nest-seconds 40
$P blanks.py out/jobs/b15_bed.json --strategy twostep --out out/cmp2/b15/ts_default --min-strip 0 --refill 10
$P blanks.py out/jobs/b15_bed.json --strategy patterns twostep --out out/cmp2/b15/offcuts --min-strip 0 --refill 10 --offcut 1250x600 --offcut 900x450 --offcut 1600x300
