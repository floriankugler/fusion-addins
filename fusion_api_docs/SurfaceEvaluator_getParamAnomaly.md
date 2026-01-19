# SurfaceEvaluator.getParamAnomaly Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Gets details about anomalies in parameter space of the surface. This includes information about periodic intervals, singularities, or unbounded parameter ranges.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, periodicityU, periodicityV, singularitiesU, singularitiesV, unboundedParameters) = surfaceEvaluator_var.getParamAnomaly()
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the parameter anomalies were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| periodicityU | double\[\] | The output array with information about the period of the surface in U. periodicityU\[0\] will contain the period of the surface in U. If periodicityU\[0\] is 0, the surface is not periodic in U. If the surface is periodic in U, peridocityU\[1\] will contain the parameter value at the start of the principle period. |
| periodicityV | double\[\] | The output array with information about the period of the surface in V. periodicityV\[0\] will contain the period of the surface in V. If periodicityV\[0\] is 0, the surface is not periodic in V. If the surface is periodic in V, peridocityV\[1\] will contain the parameter value at the start of the principle period. |
| singularitiesU | double\[\] | The output array parameter values of singularities in U. If this array is empty, there are no singularities in U. |
| singularitiesV | double\[\] | The output array parameter values of singularities in V. If this array is empty, there are no singularities in V. |
| unboundedParameters | boolean\[\] | The output array that indicates if the parameter range is unbounded in U or V. unboundedParameters\[0\] will be true if U is unbounded. unboundedParameters\[1\] will be true if V is unbounded. |

## Version

Introduced in version August 2014  

