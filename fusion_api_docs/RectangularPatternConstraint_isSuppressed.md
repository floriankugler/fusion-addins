# RectangularPatternConstraint.isSuppressed Property

Parent Object: [RectangularPatternConstraint](RectangularPatternConstraint.md)  

## Description

Specifies which, if any, instances of the pattern are suppressed. This returns an array of Boolean values that indicates if a particular instance in the pattern is suppressed or not. A value of true will result in the associated instance being suppressed.  

The indices represent the pattern instances in a row-column order, with the initial geometry not counting. For example, if you have a 4x4 pattern, the array will have 15 elements rather than 16 because the original geometry cannot be suppressed as part of the pattern. The first element in the array is the one next to the original in the first direction. The second element is the next one on the first row, and the third is the next one. The fourth element will be the first element in the row next to the first row that contains the original geometry.

## Syntax

"rectangularPatternConstraint_var" is a variable referencing a RectangularPatternConstraint object.  

```python
# Get the value of the property.
propertyValue = rectangularPatternConstraint_var.isSuppressed

# Set the value of the property.
rectangularPatternConstraint_var.isSuppressed = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type boolean.

## Version

Introduced in version September 2022  

