# GeometricConstraints.addEqual Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new equal constraint between two lines, or between arcs and circles.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addEqual(curveOne, curveTwo)
```

## Return Value

| Type | Description |
|----|----|
| [EqualConstraint](EqualConstraint.md) | Returns the newly created EqualConstraint object or null if the creation failed. |

## Parameters

| Name     | Type                           | Description                      |
|----------|--------------------------------|----------------------------------|
| curveOne | [SketchCurve](SketchCurve.md) | The first line, arc, or circle.  |
| curveTwo | [SketchCurve](SketchCurve.md) | The second line, arc, or circle. |

## Samples

| Name | Description |
|----|----|
| [GeometricConstraints.addEqual](GeometricConstraints_addEqual_Sample.md) | Demonstrates the GeometricConstraints.addEqual method. |

## Version

Introduced in version August 2014  

