# SketchFixedSplines.addByNurbsCurve Method

Parent Object: [SketchFixedSplines](SketchFixedSplines.md)  

## Description

Creates a new fixed spline using the input NurbsCurve3D to define the shape. The resulting curve is not editable by the user but can be updated via the API using the replaceGeometry method on the SketchFixedSpline object.

## Syntax

"sketchFixedSplines_var" is a variable referencing a [SketchFixedSplines](SketchFixedSplines.md) object.

```python
returnValue = sketchFixedSplines_var.addByNurbsCurve(nurbsCurve)
```

## Return Value

| Type | Description |
|----|----|
| [SketchFixedSpline](SketchFixedSpline.md) | Returns the newly created SketchFixedSpline object if the creation was successful or null if it failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| nurbsCurve | [NurbsCurve3D](NurbsCurve3D.md) | A NurbsCurve3D object that defines a valid NURBS curve. |

## Samples

| Name | Description |
|----|----|
| [SketchFixedSplines.addByNurbsCurve](SketchFixedSplines_addByNurbsCurve_Sample.md) | Demonstrates the SketchFixedSplines.addByNurbsCurve method. |

## Version

Introduced in version December 2020  

