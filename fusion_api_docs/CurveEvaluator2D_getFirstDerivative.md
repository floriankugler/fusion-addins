# CurveEvaluator2D.getFirstDerivative Method

Parent Object: [CurveEvaluator2D](CurveEvaluator2D.md)  

## Description

Get the first derivative of the curve at the specified parameter position.

## Syntax

"curveEvaluator2D_var" is a variable referencing a [CurveEvaluator2D](CurveEvaluator2D.md) object.  

```python
(returnValue, firstDerivative) = curveEvaluator2D_var.getFirstDerivative(parameter)
```

## Return Value

| Type    | Description                                                     |
|---------|-----------------------------------------------------------------|
| boolean | Returns true if the first derivative was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | double | The parameter position to get the curve first derivative at. The parameter value must be within the range of the parameter extents as provided by getParameterExtents. |
| firstDerivative | [Vector2D](Vector2D.md) | The output first derivative vector at the parameter position specified. |

## Version

Introduced in version August 2014  

