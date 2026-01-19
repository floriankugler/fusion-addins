# CurveEvaluator2D.getTangents Method

Parent Object: [CurveEvaluator2D](CurveEvaluator2D.md)  

## Description

Get the tangent to the curve at a number of parameter positions on the curve.

## Syntax

"curveEvaluator2D_var" is a variable referencing a [CurveEvaluator2D](CurveEvaluator2D.md) object.  

```python
(returnValue, tangents) = curveEvaluator2D_var.getTangents(parameters)
```

## Return Value

| Type    | Description                                              |
|---------|----------------------------------------------------------|
| boolean | Returns true if the tangents were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameters | double\[\] | The array of parameter positions to return the tangent at. Each parameter value must be within the range of the parameter extents as provided by getParameterExtents. |
| tangents | Vector2D\[\] | The output array of tangent vectors for each position on the curve. The length of this array will be the same as the length of the parameters array provided. |

## Version

Introduced in version August 2014  

