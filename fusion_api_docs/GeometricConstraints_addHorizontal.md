# GeometricConstraints.addHorizontal Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new horizontal constraint on a line.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addHorizontal(line)
```

## Return Value

| Type | Description |
|----|----|
| [HorizontalConstraint](HorizontalConstraint.md) | Returns the newly created HorizontalConstraint object or null if the creation failed. |

## Parameters

| Name | Type                         | Description                         |
|------|------------------------------|-------------------------------------|
| line | [SketchLine](SketchLine.md) | The line to constrain horizontally. |

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [GeometricConstraint.addHorizontal](GeometricConstraint_addHorizontal_Sample.md) | Demonstrates the GeometricConstraint.addHorizontal method. |

## Version

Introduced in version August 2014  

