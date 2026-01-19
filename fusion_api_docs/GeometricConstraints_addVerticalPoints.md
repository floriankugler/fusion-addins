# GeometricConstraints.addVerticalPoints Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new vertical constraint between two points.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addVerticalPoints(pointOne, pointTwo)
```

## Return Value

| Type | Description |
|----|----|
| [VerticalPointsConstraint](VerticalPointsConstraint.md) | Returns the newly created VerticalPointsConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointOne | [SketchPoint](SketchPoint.md) | The first SketchPoint to constrain vertically. |
| pointTwo | [SketchPoint](SketchPoint.md) | The second SketchPoint to constrain vertically. |

## Version

Introduced in version August 2014  

