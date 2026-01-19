# SketchControlPointSpline.controlFrameLines Property

Parent Object: [SketchControlPointSpline](SketchControlPointSpline.md)  

## Description

Returns the sketch lines that represent the control frame of the spline. The lines are in sequential order starting with the line that connects to the starting control point to the end.

## Remarks

There are cases, like when a curve is offset, where a control point spline is created but the control frame is not displayed and the curve is not editable. You can check for this case by checking the value of the isControlFrameDisplayed property. If it is true, this property will return an empty array of sketch lines since they do not currently exist.

## Syntax

"sketchControlPointSpline_var" is a variable referencing a SketchControlPointSpline object.  

```python
# Get the value of the property.
propertyValue = sketchControlPointSpline_var.controlFrameLines
```

## Property Value

This is a read only property whose value is an array of type [SketchLine](SketchLine.md).

## Version

Introduced in version October 2022  

