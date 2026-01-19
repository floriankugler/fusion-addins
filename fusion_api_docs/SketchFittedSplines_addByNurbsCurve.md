# SketchFittedSplines.addByNurbsCurve Method

Parent Object: [SketchFittedSplines](SketchFittedSplines.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Creates a new fitted spline using the input NurbsCurve3D to define the shape. Fit points are created to create a curve that exactly matches the input curve.

## Remarks

This method has been retired and replaced by the addByNurbsCurve method on the SketchFixedSplines collection. Using this method creates a curve that can have unreliable behavior if it is edited in any way. The new method will create a stable curve and also supports the ability to modify it by providing a new NURBS curve definition.

## Syntax

"sketchFittedSplines_var" is a variable referencing a [SketchFittedSplines](SketchFittedSplines.md) object.

```python
returnValue = sketchFittedSplines_var.addByNurbsCurve(nurbsCurve)
```

## Return Value

| Type | Description |
|----|----|
| [SketchFittedSpline](SketchFittedSpline.md) | Returns the newly created SketchFittedSpline object if the creation was successful or null if it failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| nurbsCurve | [NurbsCurve3D](NurbsCurve3D.md) | A NurbsCurve3D object that defines a valid NURBS curve. |

## Version

Introduced in version May 2016  
Retired in version September 2022  

