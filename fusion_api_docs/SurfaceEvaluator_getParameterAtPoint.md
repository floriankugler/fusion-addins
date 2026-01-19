# SurfaceEvaluator.getParameterAtPoint Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Get the parameter position that correspond to a point on the surface. For reliable results, the point should lie on the surface within model tolerance. If the point does not lie on the surface, the parameter of the nearest point on the surface will generally be returned.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, parameter) = surfaceEvaluator_var.getParameterAtPoint(point)
```

## Return Value

| Type    | Description                                              |
|---------|----------------------------------------------------------|
| boolean | Returns true of the parameter was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| point | [Point3D](Point3D.md) | The point to get the curve parameter value at. |
| parameter | [Point2D](Point2D.md) | The output parameter position corresponding to the point. |

## Version

Introduced in version August 2014  

