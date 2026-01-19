# GeometricConstraints.addPerpendicular Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new perpendicular constraint between two lines.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addPerpendicular(lineOne, lineTwo)
```

## Return Value

| Type | Description |
|----|----|
| [PerpendicularConstraint](PerpendicularConstraint.md) | Returns the newly created PerpendicularConstraint object or null if the creation failed. |

## Parameters

| Name    | Type                         | Description            |
|---------|------------------------------|------------------------|
| lineOne | [SketchLine](SketchLine.md) | The first SketchLine.  |
| lineTwo | [SketchLine](SketchLine.md) | The second SketchLine. |

## Samples

| Name | Description |
|----|----|
| [GeometricConstraints.addPerpendicular](GeometricConstraints_addPerpendicular_Sample.md) | Demonstrates the GeometricConstraints.addPerpendicular method. |

## Version

Introduced in version August 2014  

