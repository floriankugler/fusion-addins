# GeometricConstraints.addVertical Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new vertical constraint on a line.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addVertical(line)
```

## Return Value

| Type | Description |
|----|----|
| [VerticalConstraint](VerticalConstraint.md) | Returns the newly created VerticalConstraint object or null if the creation failed. |

## Parameters

| Name | Type                         | Description                       |
|------|------------------------------|-----------------------------------|
| line | [SketchLine](SketchLine.md) | The line to constrain vertically. |

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [GeometricConstraints.addVertical](GeometricConstraints_addVertical_Sample.md) | Demonstrates the GeometricConstraints.addVertical method. |

## Version

Introduced in version August 2014  

