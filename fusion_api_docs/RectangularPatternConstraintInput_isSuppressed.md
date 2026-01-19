# RectangularPatternConstraintInput.isSuppressed Property

Parent Object: [RectangularPatternConstraintInput](RectangularPatternConstraintInput.md)  

## Description

Specifies which, if any, instances of the pattern are suppressed. This defaults to all instances being visible. This returns an array of Booleans that indicates if a particular instance in the pattern is suppressed or not. A value of true will result in the associated instance being suppressed.  

Both the quantityOne and quantityTwo properties must be set with valid values before using the isSuppressed property is valid. A quantity of one is a valid value.  

The indices represent the pattern instances in a row-column order, with the initial geometry not counting. For example, if you have a 4x4 pattern, the array will have 15 elements rather than 16 because the original geometry cannot be suppressed as part of the pattern. The first element in the array is the one next to the original in the first direction. The second element is the next one on the first row, and the third is the next one. The fourth element will be the first element in the row next to the first row that contains the original geometry.

## Syntax

"rectangularPatternConstraintInput_var" is a variable referencing a RectangularPatternConstraintInput object.  

```python
# Get the value of the property.
propertyValue = rectangularPatternConstraintInput_var.isSuppressed

# Set the value of the property.
rectangularPatternConstraintInput_var.isSuppressed = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type boolean.

## Version

Introduced in version September 2022  

