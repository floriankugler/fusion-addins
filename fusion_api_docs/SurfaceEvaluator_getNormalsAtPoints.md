# SurfaceEvaluator.getNormalsAtPoints Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Gets the surface normal at a number of positions on the surface.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, normals) = surfaceEvaluator_var.getNormalsAtPoints(points)
```

## Return Value

| Type    | Description                                             |
|---------|---------------------------------------------------------|
| boolean | Returns true if the normals were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| points | Point3D\[\] | The array of points to return the normal at. For reliable results each point should lie on the surface. |
| normals | Vector3D\[\] | The output array of normals for each point on the surface. The length of this array will be the same as the length of the points array provided. |

## Version

Introduced in version August 2014  

