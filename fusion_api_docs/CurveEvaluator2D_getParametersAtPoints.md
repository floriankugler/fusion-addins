# CurveEvaluator2D.getParametersAtPoints Method

Parent Object: [CurveEvaluator2D](CurveEvaluator2D.md)  

## Description

Get the parameter positions that correspond to a set of points on the curve. For reliable results, the points should lie on the curve within model tolerance. If the points do not lie on the curve, the parameter of the nearest point on the curve will generally be returned.

## Syntax

"curveEvaluator2D_var" is a variable referencing a [CurveEvaluator2D](CurveEvaluator2D.md) object.  

```python
(returnValue, parameters) = curveEvaluator2D_var.getParametersAtPoints(points)
```

## Return Value

| Type    | Description                                                |
|---------|------------------------------------------------------------|
| boolean | Returns true if the parameters were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| points | Point2D\[\] | An array of points to get the curve parameter values at. |
| parameters | double\[\] | The output array of parameter positions corresponding to the set of points. The length of this array will be equal to the length of the points array specified. |

## Version

Introduced in version August 2014  

