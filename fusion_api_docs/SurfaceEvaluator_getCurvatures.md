# SurfaceEvaluator.getCurvatures Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Get the curvature values at a number of parameter positions on the surface.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, maxTangents, maxCurvatures, minCurvatures) = surfaceEvaluator_var.getCurvatures(parameters)
```

## Return Value

| Type    | Description                                                |
|---------|------------------------------------------------------------|
| boolean | Returns true if the curvatures were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameters | Point2D\[\] | The array of parameter positions to return curvature information at. Each parameter position must be with the range of the parameter extents as verified by isParameterOnFace. |
| maxTangents | Vector3D\[\] | The output array of directions of maximum curvature at each position on the surface. The length of this array will be the same as the length of the parameters array provided. |
| maxCurvatures | double\[\] | The output array of the magnitude of the maximum curvature at each position on the surface. The length of this array will be the same as the length of the parameters array provided. |
| minCurvatures | double\[\] | The output array of the magnitude of the minimum curvature at each position on the surface. The minimum curvature direction is perpendicular to the maximum curvature tangent directions. The length of this array will be the same as the length of the parameters array provided. |

## Version

Introduced in version August 2014  

