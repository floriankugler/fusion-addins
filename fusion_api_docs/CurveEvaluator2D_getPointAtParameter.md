# CurveEvaluator2D.getPointAtParameter Method

Parent Object: [CurveEvaluator2D](CurveEvaluator2D.md)  

## Description

Get the point on the curve that corresponds to evaluating a parameter position on the curve.

## Syntax

"curveEvaluator2D_var" is a variable referencing a [CurveEvaluator2D](CurveEvaluator2D.md) object.  

```python
(returnValue, point) = curveEvaluator2D_var.getPointAtParameter(parameter)
```

## Return Value

| Type    | Description                                          |
|---------|------------------------------------------------------|
| boolean | Returns true if the point was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | double | The parameter position to evaluate the curve position at. The parameter value must be within the range of the parameter extents as provided by getParameterExtents. |
| point | [Point2D](Point2D.md) | The output curve position corresponding to evaluating the curve at that parameter position. |

## Version

Introduced in version August 2014  

