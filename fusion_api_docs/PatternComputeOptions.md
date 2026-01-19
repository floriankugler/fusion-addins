# PatternComputeOptions Enumerator

## Description

List of the compute options for mirroring and patterning features in the parametric modeling environment.  

## Methods

| Name | Value | Description |
|----|----|----|
| AdjustPatternCompute | 2 | Adjust pattern compute. This is the slowest of all compute options. It can almost never produce a wrong result (e.g. works well even on Split features) |
| IdenticalPatternCompute | 1 | Identical pattern compute. Used when you want force the resulting mirror or pattern to create identical results regardless of the dependencies that define the feature being copied. |
| OptimizedPatternCompute | 0 | Optimized pattern compute. This is the fastest of all compute options. This option may fail or give wrong results in some very rare cases (e.g. when patterning a Split feature) |

## Version

Introduced in version November 2015  

