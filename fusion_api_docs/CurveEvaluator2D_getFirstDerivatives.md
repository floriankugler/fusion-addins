# CurveEvaluator2D.getFirstDerivatives Method

Parent Object: [CurveEvaluator2D](CurveEvaluator2D.md)  

## Description

Get the first derivatives of the curve at the specified parameter positions.

## Syntax

"curveEvaluator2D_var" is a variable referencing a [CurveEvaluator2D](CurveEvaluator2D.md) object.  

```python
(returnValue, firstDerivatives) = curveEvaluator2D_var.getFirstDerivatives(parameters)
```

## Return Value

| Type    | Description                                                       |
|---------|-------------------------------------------------------------------|
| boolean | Returns true if the first derivatives were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameters | double\[\] | The array of parameter positions to get the curve first derivative at. Each parameter value must be within the range of the parameter extents as provided by getParameterExtents. |
| firstDerivatives | Vector2D\[\] | The output array of first derivative vectors at each parameter position specified. The length of this array is equal to the length of the parameters array specified. |

## Version

Introduced in version August 2014  

