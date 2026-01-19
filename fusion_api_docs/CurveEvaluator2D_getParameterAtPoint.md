# CurveEvaluator2D.getParameterAtPoint Method

Parent Object: [CurveEvaluator2D](CurveEvaluator2D.md)  

## Description

Get the parameter position that correspond to a point on the curve. For reliable results, the point should lie on the curve within model tolerance. If the point does not lie on the curve, the parameter of the nearest point on the curve will generally be returned.

## Syntax

"curveEvaluator2D_var" is a variable referencing a [CurveEvaluator2D](CurveEvaluator2D.md) object.  

```python
(returnValue, parameter) = curveEvaluator2D_var.getParameterAtPoint(point)
```

## Return Value

| Type    | Description                                              |
|---------|----------------------------------------------------------|
| boolean | Returns true of the parameter was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| point | [Point2D](Point2D.md) | The point to get the curve parameter value at. |
| parameter | double | The output parameter position corresponding to the point. |

## Version

Introduced in version August 2014  

