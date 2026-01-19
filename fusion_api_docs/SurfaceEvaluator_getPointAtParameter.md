# SurfaceEvaluator.getPointAtParameter Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Get the point on the surface that correspond to evaluating a parameter position on the surface.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, point) = surfaceEvaluator_var.getPointAtParameter(parameter)
```

## Return Value

| Type    | Description                                          |
|---------|------------------------------------------------------|
| boolean | Returns true if the point was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | [Point2D](Point2D.md) | The parameter positions to evaluate the surface position at. The parameter position must be within the range of the parameter extents as verified by isParameterOnFace. |
| point | [Point3D](Point3D.md) | The output point corresponding to evaluating the curve at that parameter position. |

## Version

Introduced in version August 2014  

