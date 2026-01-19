# GeometricConstraints.createCircularPatternInput Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a CircularPatternConstraintInput object. Use properties and methods on this object to define the circular pattern you want to create and then use the Add method, passing in the CircularPatternConstraintInput object.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.createCircularPatternInput(inputEntities, centerPoint)
```

## Return Value

| Type | Description |
|----|----|
| [CircularPatternConstraintInput](CircularPatternConstraintInput.md) | Returns the newly created CircularPatternConstraintInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| inputEntities | SketchEntity\[\] | An array of sketch entities to be patterned. All of the entities must be from the current sketch. |
| centerPoint | [SketchPoint](SketchPoint.md) | A SketchPoint from the same sketch that defines the center of the pattern. |

## Version

Introduced in version September 2022  

