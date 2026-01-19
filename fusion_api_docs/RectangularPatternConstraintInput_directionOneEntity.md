# RectangularPatternConstraintInput.directionOneEntity Property

Parent Object: [RectangularPatternConstraintInput](RectangularPatternConstraintInput.md)  

## Description

Defines the first direction of the pattern. This can be null which indicates to use the default which is the X-axis of the sketch. Setting this property to null will automatically clear directionTwoEntity, if it has been set.

## Syntax

"rectangularPatternConstraintInput_var" is a variable referencing a RectangularPatternConstraintInput object.  

```python
# Get the value of the property.
propertyValue = rectangularPatternConstraintInput_var.directionOneEntity

# Set the value of the property.
rectangularPatternConstraintInput_var.directionOneEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [SketchLine](SketchLine.md).

## Version

Introduced in version September 2022  

