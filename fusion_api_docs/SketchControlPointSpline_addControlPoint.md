# SketchControlPointSpline.addControlPoint Method

Parent Object: [SketchControlPointSpline](SketchControlPointSpline.md)  

## Description

Adds an additional control point to the control point spline. Inserting a new control point does not change the shape of the curve, but the control frame will be re-computed and the control points will be adjusted to maintain the current shape.  

This method will fail in the case where the control frame is not displayed. You can check for this by using the is isControlFrameDisplayed.

## Syntax

"sketchControlPointSpline_var" is a variable referencing a [SketchControlPointSpline](SketchControlPointSpline.md) object.

```python
returnValue = sketchControlPointSpline_var.addControlPoint(parameter)
```

## Return Value

| Type    | Description                                              |
|---------|----------------------------------------------------------|
| boolean | Returns true if adding the control point was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | double | The parameter position that defines where to insert the new control point. The parameter value must be within the parametric range of the curve. This can be determined by using the getParameterExtents method of the CurveEvaluator3D returned by the evaluator property. |

## Version

Introduced in version July 2022  

