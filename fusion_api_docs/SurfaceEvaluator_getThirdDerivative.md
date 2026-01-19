# SurfaceEvaluator.getThirdDerivative Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Get the third derivative of the surface at the specified parameter position.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, partialUUU, partialVVV) = surfaceEvaluator_var.getThirdDerivative(parameter)
```

## Return Value

| Type    | Description                                                     |
|---------|-----------------------------------------------------------------|
| boolean | Returns true if the third derivative was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | [Point2D](Point2D.md) | The parameter position to get the surface third derivative at. The parameter position must be within the range of the parameter extents as verified by isParameterOnFace. |
| partialUUU | [Vector3D](Vector3D.md) | The output third derivative UUU partial vector at each parameter position specified. |
| partialVVV | [Vector3D](Vector3D.md) | The output third derivative VVV partial vector at each parameter position specified. |

## Version

Introduced in version August 2014  

