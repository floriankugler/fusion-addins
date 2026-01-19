# CurveEvaluator2D.getCurvature Method

Parent Object: [CurveEvaluator2D](CurveEvaluator2D.md)  

## Description

Get the curvature value at a parameter position on the curve.

## Syntax

"curveEvaluator2D_var" is a variable referencing a [CurveEvaluator2D](CurveEvaluator2D.md) object.  

```python
(returnValue, direction, curvature) = curveEvaluator2D_var.getCurvature(parameter)
```

## Return Value

| Type    | Description                                              |
|---------|----------------------------------------------------------|
| boolean | Returns true if the curvature was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | double | The parameter position to return the curvature information at. This value must be within the range of the parameter extents as provided by getParameterExtents. |
| direction | [Vector2D](Vector2D.md) | The output direction of the curvature at the position on the curve. |
| curvature | double | The output magnitude of the curvature at the position on the curve. |

## Version

Introduced in version August 2014  

