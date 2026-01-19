# SurfaceEvaluator.getFirstDerivatives Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Get the first derivatives of the surface at the specified parameter positions.

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.  

```python
(returnValue, partialsU, partialsV) = surfaceEvaluator_var.getFirstDerivatives(parameters)
```

## Return Value

| Type    | Description                                                       |
|---------|-------------------------------------------------------------------|
| boolean | Returns true if the first derivatives were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameters | Point2D\[\] | The array of parameter positions to get the surface first derivative at. Each parameter position must be within the range of the parameter extents as verified by isParameterOnFace. |
| partialsU | Vector3D\[\] | The output array of first derivative U partial vectors at each parameter position specified. The length of this array is equal to the length of the parameters array specified. |
| partialsV | Vector3D\[\] | The output array of first derivative V partial vectors at each parameter position specified. The length of this array is equal to the length of the parameters array specified. |

## Version

Introduced in version August 2014  

