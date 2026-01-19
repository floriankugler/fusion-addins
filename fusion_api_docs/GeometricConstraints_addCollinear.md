# GeometricConstraints.addCollinear Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new collinear constraint between two lines.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addCollinear(lineOne, lineTwo)
```

## Return Value

| Type | Description |
|----|----|
| [CollinearConstraint](CollinearConstraint.md) | Returns the newly created CollinearConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| lineOne | [SketchLine](SketchLine.md) | The first line to create the constraint on. |
| lineTwo | [SketchLine](SketchLine.md) | The second line to create the constraint on. |

## Samples

| Name | Description |
|----|----|
| [GeometricConstraints.addCollinear](GeometricConstraints_addCollinear_Sample.md) | Demonstrates the GeometricConstraints.addCollinear method. |

## Version

Introduced in version August 2014  

