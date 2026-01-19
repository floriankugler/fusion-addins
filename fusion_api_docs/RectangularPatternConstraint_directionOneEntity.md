# RectangularPatternConstraint.directionOneEntity Property

Parent Object: [RectangularPatternConstraint](RectangularPatternConstraint.md)  

## Description

Gets and sets the entity that defined the first direction of the pattern. This can be null which indicates to use the default which is the X-axis of the sketch. Setting this property to null will automatically clear directionTwoEntity, if it has been set.

## Syntax

"rectangularPatternConstraint_var" is a variable referencing a RectangularPatternConstraint object.  

```python
# Get the value of the property.
propertyValue = rectangularPatternConstraint_var.directionOneEntity

# Set the value of the property.
rectangularPatternConstraint_var.directionOneEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [SketchLine](SketchLine.md).

## Version

Introduced in version September 2022  

