# GeometricConstraints.createRectangularPatternInput Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new RectangularPatternConstraintInput object. Use this object to define the various settings associated with a rectangular pattern in a sketch. Once the pattern is defined you can call the addRectangularPattern method and pass in the input object to create the sketch rectangular pattern.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.createRectangularPatternInput(entities, distanceType)
```

## Return Value

| Type | Description |
|----|----|
| [RectangularPatternConstraintInput](RectangularPatternConstraintInput.md) | Returns the created RectangularPatternsConstraintInput object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entities | SketchEntity\[\] | An array of sketch entities to pattern. These can be sketch points and curves. |
| distanceType | [PatternDistanceType](PatternDistanceType.md) | Specifies if the distances defined for the pattern define the overall size of the pattern or the distance between the rows and columns. |

## Version

Introduced in version September 2022  

