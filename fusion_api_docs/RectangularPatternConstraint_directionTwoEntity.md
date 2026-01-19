# RectangularPatternConstraint.directionTwoEntity Property

Parent Object: [RectangularPatternConstraint](RectangularPatternConstraint.md)  

## Description

Gets and sets the entity that defines the second direction of the pattern. This can be null which indicates to use the default direction, which is perpendicular to direction one. The directionOneEntity property must be set before setting this property.

## Syntax

"rectangularPatternConstraint_var" is a variable referencing a RectangularPatternConstraint object.  

```python
# Get the value of the property.
propertyValue = rectangularPatternConstraint_var.directionTwoEntity

# Set the value of the property.
rectangularPatternConstraint_var.directionTwoEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [SketchLine](SketchLine.md).

## Version

Introduced in version September 2022  

