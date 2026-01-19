# CurveEvaluator3D.getParameterExtents Method

Parent Object: [CurveEvaluator3D](CurveEvaluator3D.md)  

## Description

Get the parametric range of the curve.

## Syntax

"curveEvaluator3D_var" is a variable referencing a [CurveEvaluator3D](CurveEvaluator3D.md) object.  

```python
(returnValue, startParameter, endParameter) = curveEvaluator3D_var.getParameterExtents()
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the curve is bounded and the parameter extents were successfully returned. |

## Parameters

| Name           | Type   | Description                                    |
|----------------|--------|------------------------------------------------|
| startParameter | double | The output lower bound of the parameter range. |
| endParameter   | double | The output upper bound of the parameter range. |

## Samples

| Name | Description |
|----|----|
| [SketchArcs.split](SketchArcs_split_Sample.md) | Demonstrates the SketchArc.split method. |

## Version

Introduced in version August 2014  

