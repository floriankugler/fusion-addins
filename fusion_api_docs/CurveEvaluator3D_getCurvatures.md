# CurveEvaluator3D.getCurvatures Method

Parent Object: [CurveEvaluator3D](CurveEvaluator3D.md)  

## Description

Get the curvature values at a number of parameter positions on the curve.

## Syntax

"curveEvaluator3D_var" is a variable referencing a [CurveEvaluator3D](CurveEvaluator3D.md) object.  

```python
(returnValue, directions, curvatures) = curveEvaluator3D_var.getCurvatures(parameters)
```

## Return Value

| Type    | Description                                                |
|---------|------------------------------------------------------------|
| boolean | Returns true if the curvatures were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameters | double\[\] | The array of parameter positions to return curvature information at. Each parameter value must be within the range of the parameter extents as provided by getParameterExtents. |
| directions | Vector3D\[\] | The output array of the direction of the curvature at each position on the curve. The length of this array will be the same as the length of the parameters array provided. |
| curvatures | double\[\] | The output array of the magnitude of the curvature at the position on the curve. The length of this array will be the same as the length of the parameters array provided. |

## Version

Introduced in version August 2014  

