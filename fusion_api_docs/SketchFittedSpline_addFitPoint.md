# SketchFittedSpline.addFitPoint Method

Parent Object: [SketchFittedSpline](SketchFittedSpline.md)  

## Description

Creates a new fit point at the specified parameter value.

## Syntax

"sketchFittedSpline_var" is a variable referencing a [SketchFittedSpline](SketchFittedSpline.md) object.

```python
returnValue = sketchFittedSpline_var.addFitPoint(parameter)
```

## Return Value

| Type | Description |
|----|----|
| [SketchPoint](SketchPoint.md) | Returns the newly created SketchPoint that acts as the fit point. Fails in the case where an invalid parameter is specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | double | The parameter value at the position along the curve where you want to add the new fit point. The CurveEvaluator3D object provides utilities that support going from a 3D coordinate to a parameter value on the curve. |

## Version

Introduced in version September 2022  

