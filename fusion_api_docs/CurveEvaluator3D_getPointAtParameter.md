# CurveEvaluator3D.getPointAtParameter Method

Parent Object: [CurveEvaluator3D](CurveEvaluator3D.md)  

## Description

Get the point on the curve that corresponds to evaluating a parameter position on the curve.

## Syntax

"curveEvaluator3D_var" is a variable referencing a [CurveEvaluator3D](CurveEvaluator3D.md) object.  

```python
(returnValue, point) = curveEvaluator3D_var.getPointAtParameter(parameter)
```

## Return Value

| Type    | Description                                          |
|---------|------------------------------------------------------|
| boolean | Returns true if the point was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | double | The parameter position to evaluate the curve position at. The parameter value must be within the range of the parameter extents as provided by getParameterExtents. |
| point | [Point3D](Point3D.md) | The output curve position corresponding to evaluating the curve at that parameter position. |

## Samples

| Name | Description |
|----|----|
| [SketchArcs.split](SketchArcs_split_Sample.md) | Demonstrates the SketchArc.split method. |

## Version

Introduced in version August 2014  

