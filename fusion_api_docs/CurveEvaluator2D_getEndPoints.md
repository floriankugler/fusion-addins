# CurveEvaluator2D.getEndPoints Method

Parent Object: [CurveEvaluator2D](CurveEvaluator2D.md)  

## Description

Get the end points of the curve.

## Syntax

"curveEvaluator2D_var" is a variable referencing a [CurveEvaluator2D](CurveEvaluator2D.md) object.  

```python
(returnValue, startPoint, endPoint) = curveEvaluator2D_var.getEndPoints()
```

## Return Value

| Type    | Description                                                |
|---------|------------------------------------------------------------|
| boolean | Returns true if the end points were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| startPoint | [Point2D](Point2D.md) | The output start point of the curve. If the curve is unbounded at the start, this value will be null. |
| endPoint | [Point2D](Point2D.md) | The output end point of the curve. If the curve is unbounded at the end, this value will be null. |

## Version

Introduced in version August 2014  

