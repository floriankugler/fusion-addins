# Design.activeOccurrence Property

Parent Object: [Design](Design.md)  

## Description

Returns the occurrence that is currently activated, if any. This can return null in the case where no occurrence is activated and the root component is active.

## Syntax

"design_var" is a variable referencing a Design object.  

```python
# Get the value of the property.
propertyValue = design_var.activeOccurrence
```

## Property Value

This is a read only property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version January 2016  

