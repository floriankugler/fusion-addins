# GeometricConstraints.addHorizontalPoints Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new horizontal constraint between two points.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addHorizontalPoints(pointOne, pointTwo)
```

## Return Value

| Type | Description |
|----|----|
| [HorizontalPointsConstraint](HorizontalPointsConstraint.md) | Returns the newly created HorizontalPointsConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointOne | [SketchPoint](SketchPoint.md) | The first SketchPoint to constrain horizontally. |
| pointTwo | [SketchPoint](SketchPoint.md) | The second SketchPoint to constrain horizontally. |

## Samples

| Name | Description |
|----|----|
| [GeometricConstraint.addHorizontalPoints](GeometricConstraint_addHorizontalPoints_Sample.md) | Demonstrates the GeometricConstraint.addHorizontalPoints method. |

## Version

Introduced in version August 2014  

