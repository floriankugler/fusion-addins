# SurfaceEvaluator.getNormalAtPoint Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Gets the surface normal at a point on the surface.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, normal) = surfaceEvaluator_var.getNormalAtPoint(point)
```

## Return Value

| Type    | Description                                           |
|---------|-------------------------------------------------------|
| boolean | Returns true if the normal was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| point | [Point3D](Point3D.md) | The point to return the normal at. For reliable results the point should lie on the surface. |
| normal | [Vector3D](Vector3D.md) | The output normal for the point on the surface. |

## Version

Introduced in version August 2014  

