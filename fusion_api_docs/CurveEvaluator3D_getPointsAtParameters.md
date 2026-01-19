# CurveEvaluator3D.getPointsAtParameters Method

Parent Object: [CurveEvaluator3D](CurveEvaluator3D.md)  

## Description

Get the points on the curve that correspond to evaluating a set of parameter positions on the curve.

## Syntax

"curveEvaluator3D_var" is a variable referencing a [CurveEvaluator3D](CurveEvaluator3D.md) object.  

```python
(returnValue, points) = curveEvaluator3D_var.getPointsAtParameters(parameters)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if the points were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameters | double\[\] | The array of parameter positions to evaluate the curve position at. Each parameter value must be within the range of the parameter extents as provided by getParameterExtents. |
| points | Point3D\[\] | The output array of curve positions corresponding to evaluating the curve at that parameter position. The length of this array will be equal to the length of the parameters array specified. |

## Version

Introduced in version August 2014  

