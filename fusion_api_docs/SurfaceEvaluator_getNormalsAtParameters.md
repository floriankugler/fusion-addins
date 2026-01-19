# SurfaceEvaluator.getNormalsAtParameters Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Gets the surface normal at a number of parameter positions on the surface.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, normals) = surfaceEvaluator_var.getNormalsAtParameters(parameters)
```

## Return Value

| Type    | Description                                             |
|---------|---------------------------------------------------------|
| boolean | Returns true if the normals were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameters | Point2D\[\] | The array of parameter positions to return the normal at. Each parameter position must be with the range of the parameter extents as verified by isParameterOnFace. |
| normals | Vector3D\[\] | The output array of normals for each parameter position on the surface. The length of this array will be the same as the length of the parameters array provided. |

## Version

Introduced in version August 2014  

