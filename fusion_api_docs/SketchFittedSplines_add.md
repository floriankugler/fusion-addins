# SketchFittedSplines.add Method

Parent Object: [SketchFittedSplines](SketchFittedSplines.md)  

## Description

Creates a new fitted spline through the specified points.

## Syntax

"sketchFittedSplines_var" is a variable referencing a [SketchFittedSplines](SketchFittedSplines.md) object.

```python
returnValue = sketchFittedSplines_var.add(fitPoints)
```

## Return Value

| Type | Description |
|----|----|
| [SketchFittedSpline](SketchFittedSpline.md) | Returns the newly created SketchFittedSpline object if the creation was successful or null if it failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| fitPoints | [ObjectCollection](ObjectCollection.md) | A collection of points that the curve will fit through. They can be any combination of existing SketchPoint or Point3D objects. |

## Samples

| Name | Description |
|----|----|
| [GeometricConstraints.addSmooth](GeometricConstraints_addSmooth_Sample.md) | Demonstrate the GeometricConstraints.addSmooth method. |
| [SketchFittedSplines.add](SketchFittedSplines_add_Sample.md) | Demonstrates the SketchFittedSplines.add method. |
| [Sketch spline through points creation and relative functions API Sample](SketchSplineThroughPoints_Sample.md) | Create a sketch spline with points and use some operations for spline tangent handle & curvature handle. |

## Version

Introduced in version August 2014  

