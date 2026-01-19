# CurveEvaluator2D.getParameterExtents Method

Parent Object: [CurveEvaluator2D](CurveEvaluator2D.md)  

## Description

Get the parametric range of the curve.

## Syntax

"curveEvaluator2D_var" is a variable referencing a [CurveEvaluator2D](CurveEvaluator2D.md) object.  

```python
(returnValue, startParameter, endParameter) = curveEvaluator2D_var.getParameterExtents()
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the curve is bounded and the parameter extents were successfully returned. |

## Parameters

| Name           | Type   | Description                                    |
|----------------|--------|------------------------------------------------|
| startParameter | double | The output lower bound of the parameter range. |
| endParameter   | double | The output upper bound of the parameter range. |

## Version

Introduced in version August 2014  

