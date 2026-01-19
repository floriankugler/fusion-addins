# GeometricConstraints.addCircularPattern Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new circular pattern in the sketch.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addCircularPattern(input)
```

## Return Value

| Type | Description |
|----|----|
| [CircularPatternConstraint](CircularPatternConstraint.md) | Returns the newly created CircularPatternConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [CircularPatternConstraintInput](CircularPatternConstraintInput.md) | A CircularPatternConstraintInput object that defines the desired circular pattern. Use the createCircularPatternInput method to create a new CircularPatternConstraintInput object and then use methods on it to define the circular pattern. |

## Version

Introduced in version September 2022  

