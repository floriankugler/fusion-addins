# SurfaceEvaluator.getFirstDerivative Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Get the first derivative of the surface at the specified parameter position.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, partialU, partialV) = surfaceEvaluator_var.getFirstDerivative(parameter)
```

## Return Value

| Type    | Description                                                     |
|---------|-----------------------------------------------------------------|
| boolean | Returns true if the first derivative was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | [Point2D](Point2D.md) | The parameter positions to get the surface first derivative at. The parameter position must be within the range of the parameter extents as verified by isParameterOnFace. |
| partialU | [Vector3D](Vector3D.md) | The output first derivative U partial vector at the parameter position specified. |
| partialV | [Vector3D](Vector3D.md) | The output first derivative V partial vector at the parameter position specified. |

## Version

Introduced in version August 2014  

