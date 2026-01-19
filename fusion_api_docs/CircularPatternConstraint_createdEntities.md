# CircularPatternConstraint.createdEntities Property

Parent Object: [CircularPatternConstraint](CircularPatternConstraint.md)  

## Description

Returns an array that contains all of the sketch entities that were created as a result of the pattern. This does not contain the original entities that were used as input to the pattern. The input entities can be obtained by using the entities property.

## Syntax

"circularPatternConstraint_var" is a variable referencing a CircularPatternConstraint object.  

```python
# Get the value of the property.
propertyValue = circularPatternConstraint_var.createdEntities
```

## Property Value

This is a read only property whose value is an array of type [SketchEntity](SketchEntity.md).

## Version

Introduced in version September 2022  

