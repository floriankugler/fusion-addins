# CurveEvaluator3D.getTangent Method

Parent Object: [CurveEvaluator3D](CurveEvaluator3D.md)  

## Description

Get the tangent to the curve at a parameter position on the curve.

## Syntax

"curveEvaluator3D_var" is a variable referencing a [CurveEvaluator3D](CurveEvaluator3D.md) object.  

```python
(returnValue, tangent) = curveEvaluator3D_var.getTangent(parameter)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if the tangent was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | double | The parameter position to return the tangent at. This value must be within the range of the parameter extents as provided by getParameterExtents. |
| tangent | [Vector3D](Vector3D.md) | The output tangent vector at the curve position. |

## Version

Introduced in version August 2014  

