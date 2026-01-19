# SurfaceEvaluator.getCurvature Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Get the curvature values at a parameter positions on the surface.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, maxTangent, maxCurvature, minCurvature) = surfaceEvaluator_var.getCurvature(parameter)
```

## Return Value

| Type    | Description                                              |
|---------|----------------------------------------------------------|
| boolean | Returns true if the curvature was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | [Point2D](Point2D.md) | The parameter positions to return curvature information at. |
| maxTangent | [Vector3D](Vector3D.md) | The output directions of maximum curvature at the position on the surface. |
| maxCurvature | double | The output magnitude of the maximum curvature at the position on the surface. |
| minCurvature | double | The output magnitude of the minimum curvature at the position on the surface. The minimum curvature direction is perpendicular to the maximum curvature tangent directions. |

## Version

Introduced in version August 2014  

