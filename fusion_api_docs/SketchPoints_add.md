# SketchPoints.add Method

Parent Object: [SketchPoints](SketchPoints.md)  

## Description

Creates a point at the specified location. This is the equivalent of creating a sketch point using the Point command in the user interface and will create a visible point in the graphics window.

## Syntax

"sketchPoints_var" is a variable referencing a [SketchPoints](SketchPoints.md) object.

```python
returnValue = sketchPoints_var.add(point)
```

## Return Value

| Type | Description |
|----|----|
| [SketchPoint](SketchPoint.md) | Returns the new sketch point or null if the creation fails. |

## Parameters

| Name | Type | Description |
|----|----|----|
| point | [Point3D](Point3D.md) | The coordinate location to create the sketch point. |

## Samples

| Name | Description |
|----|----|
| [GeometricConstraint.addMidPont](GeometricConstraint_addMidPont_Sample.md) | Demonstrate the GeometricConstraint.addMidPont method. |
| [GeometricConstraints.addCoincident](GeometricConstraints_addCoincident_Sample.md) | Demonstrates the GeometricConstraints.addCoincident method. |
| [SketchPoint.add](SketchPoint_add_Sample.md) | Demonstrates the SketchPoint.add method. |
| [Sketch Point API Sample](SketchPointSample_Sample.md) | Demonstrates creating a new sketch point. |

## Version

Introduced in version August 2014  

