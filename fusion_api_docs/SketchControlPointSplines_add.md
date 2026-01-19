# SketchControlPointSplines.add Method

Parent Object: [SketchControlPointSplines](SketchControlPointSplines.md)  

## Description

Creates a new control point spline.

## Syntax

"sketchControlPointSplines_var" is a variable referencing a [SketchControlPointSplines](SketchControlPointSplines.md) object.

```python
returnValue = sketchControlPointSplines_var.add(controlPoints, degree)
```

## Return Value

| Type | Description |
|----|----|
| [SketchControlPointSpline](SketchControlPointSpline.md) | Returns the newly created SketchControlPointSpline object if the creation was successful or null if it failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| controlPoints | Base\[\] | An array of points that define the control points of the curve's polygon. They can be any combination of existing SketchPoint or Point3D objects. |
| degree | [SplineDegrees](SplineDegrees.md) | Specifies the degree of the spline. Only degree 3 and degree 5 can be specified while creating the spline. |

## Version

Introduced in version July 2022  

