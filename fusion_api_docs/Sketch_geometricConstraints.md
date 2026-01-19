# Sketch.geometricConstraints Property

Parent Object: [Sketch](Sketch.md)  

## Description

Returns the sketch constraints collection associated with this sketch. This provides access to the existing sketch constraints and supports the creation of new sketch constraints.

## Syntax

"sketch_var" is a variable referencing a Sketch object.  

```python
# Get the value of the property.
propertyValue = sketch_var.geometricConstraints
```

## Property Value

This is a read only property whose value is a [GeometricConstraints](GeometricConstraints.md).

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [GeometricConstraint.addHorizontal](GeometricConstraint_addHorizontal_Sample.md) | Demonstrates the GeometricConstraint.addHorizontal method. |
| [GeometricConstraint.addHorizontalPoints](GeometricConstraint_addHorizontalPoints_Sample.md) | Demonstrates the GeometricConstraint.addHorizontalPoints method. |
| [GeometricConstraint.addMidPont](GeometricConstraint_addMidPont_Sample.md) | Demonstrate the GeometricConstraint.addMidPont method. |
| [GeometricConstraints.addCoincident](GeometricConstraints_addCoincident_Sample.md) | Demonstrates the GeometricConstraints.addCoincident method. |
| [GeometricConstraints.addCollinear](GeometricConstraints_addCollinear_Sample.md) | Demonstrates the GeometricConstraints.addCollinear method. |
| [GeometricConstraints.addConcentric](GeometricConstraints_addConcentric_Sample.md) | Demonstrates the GeometricConstraints.addConcentric method. |
| [GeometricConstraints.addEqual](GeometricConstraints_addEqual_Sample.md) | Demonstrates the GeometricConstraints.addEqual method. |
| [GeometricConstraints.addParallel](GeometricConstraints_addParallel_Sample.md) | Demonstrate the GeometricConstraints.addParallel method. |
| [GeometricConstraints.addPerpendicular](GeometricConstraints_addPerpendicular_Sample.md) | Demonstrates the GeometricConstraints.addPerpendicular method. |
| [GeometricConstraints.addSmooth](GeometricConstraints_addSmooth_Sample.md) | Demonstrate the GeometricConstraints.addSmooth method. |
| [GeometricConstraints.addSymmetry](GeometricConstraints_addSymmetry_Sample.md) | Demonstrates the GeometricConstraints.addSymmetry method. |
| [GeometricConstraints.addTangent](GeometricConstraints_addTangent_Sample.md) | Demonstrates the GeometricConstraints.addTangent method. |
| [GeometricConstraints.addVertical](GeometricConstraints_addVertical_Sample.md) | Demonstrates the GeometricConstraints.addVertical method. |
| [SketchCircles.addByTwoTangents](SketchCircles_addByTwoTangents_Sample.md) | Demonstrates the SketchCircles.addByTwoTangets method. |

## Version

Introduced in version August 2014  

