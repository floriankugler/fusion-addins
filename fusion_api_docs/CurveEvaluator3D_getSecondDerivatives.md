# CurveEvaluator3D.getSecondDerivatives Method

Parent Object: [CurveEvaluator3D](CurveEvaluator3D.md)  

## Description

Get the second derivatives of the curve at the specified parameter positions.

## Syntax

"curveEvaluator3D_var" is a variable referencing a [CurveEvaluator3D](CurveEvaluator3D.md) object.  

```python
(returnValue, secondDerivatives) = curveEvaluator3D_var.getSecondDerivatives(parameters)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the second derivatives were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameters | double\[\] | The array of parameter positions to get the curve second derivative at. Each parameter value must be within the range of the parameter extents as provided by getParameterExtents. |
| secondDerivatives | Vector3D\[\] | The output array of second derivative vectors at each parameter position specified. The length of this array is equal to the length of the parameters array specified. |

## Version

Introduced in version August 2014  

