# SurfaceEvaluator.getParametersAtPoints Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Get the parameter positions that correspond to a set of points on the surface. For reliable results, the points should lie on the surface within model tolerance. If the points do not lie on the surface, the parameter of the nearest point on the surface will generally be returned.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, parameters) = surfaceEvaluator_var.getParametersAtPoints(points)
```

## Return Value

| Type    | Description                                                |
|---------|------------------------------------------------------------|
| boolean | Returns true if the parameters were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| points | Point3D\[\] | An array of points to get the surface parameter values at. |
| parameters | Point2D\[\] | The output array of parameter positions corresponding to the set of points. The length of this array will be equal to the length of the points array specified. |

## Version

Introduced in version August 2014  

