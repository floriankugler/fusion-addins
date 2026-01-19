# CurveEvaluator3D.getSecondDerivative Method

Parent Object: [CurveEvaluator3D](CurveEvaluator3D.md)  

## Description

Get the second derivative of the curve at the specified parameter position.

## Syntax

"curveEvaluator3D_var" is a variable referencing a [CurveEvaluator3D](CurveEvaluator3D.md) object.  

```python
(returnValue, secondDerivative) = curveEvaluator3D_var.getSecondDerivative(parameter)
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns true if the second derivative was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | double | The parameter position to get the curve second derivative at. The parameter value must be within the range of the parameter extents as provided by getParameterExtents. |
| secondDerivative | [Vector3D](Vector3D.md) | The output second derivative vector at the parameter position specified. |

## Version

Introduced in version August 2014  

