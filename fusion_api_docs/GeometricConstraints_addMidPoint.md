# GeometricConstraints.addMidPoint Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new midpoint constraint between a point and a curve.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addMidPoint(point, midPointCurve)
```

## Return Value

| Type | Description |
|----|----|
| [MidPointConstraint](MidPointConstraint.md) | Returns the newly created MidPointConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| point | [SketchPoint](SketchPoint.md) | The point to constrain to the midpoint of a curve. |
| midPointCurve | [SketchCurve](SketchCurve.md) | The curve that defines the midpoint to constraint to. |

## Samples

| Name | Description |
|----|----|
| [GeometricConstraint.addMidPont](GeometricConstraint_addMidPont_Sample.md) | Demonstrate the GeometricConstraint.addMidPont method. |

## Version

Introduced in version August 2014  

