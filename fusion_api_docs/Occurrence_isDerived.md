# Occurrence.isDerived Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Returns if this occurrence is derived from another design. If true, the occurrence cannot be deleted. You should not attempt to make any edits to the component referenced by the derived occurrence. Any edits made to this derived occurrence will be lost when the derive updates.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.isDerived
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2026  

