# SurfaceEvaluator.getNormalAtParameter Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Gets the surface normal at a parameter position on the surface.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, normal) = surfaceEvaluator_var.getNormalAtParameter(parameter)
```

## Return Value

| Type    | Description                                           |
|---------|-------------------------------------------------------|
| boolean | Returns true if the normal was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | [Point2D](Point2D.md) | The parameter position to return the normal at. The parameter position must be with the range of the parameter extents as verified by isParameterOnFace. |
| normal | [Vector3D](Vector3D.md) | The output normal for the parameter position on the surface. |

## Version

Introduced in version August 2014  

