# SurfaceEvaluator.getPointsAtParameters Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Get the points on the surface that correspond to evaluating a set of parameter positions on the surface.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, points) = surfaceEvaluator_var.getPointsAtParameters(parameters)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if the points were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameters | Point2D\[\] | The array of parameter positions to evaluate the surface position at. Each parameter position must be within the range of the parameter extents as verified by isParameterOnFace. |
| points | Point3D\[\] | The output array of points corresponding to evaluating the curve at that parameter position. The length of this array will be equal to the length of the parameters array specified. |

## Version

Introduced in version August 2014  

