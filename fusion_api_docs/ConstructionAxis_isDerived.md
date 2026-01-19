# ConstructionAxis.isDerived Property

Parent Object: [ConstructionAxis](ConstructionAxis.md)  

## Description

Returns if this construction axis is derived from another design. If true, the construction axis cannot be deleted. You should not attempt to make any edits to the derived construction axis. Any edits made to this derived construction axis will be lost when the derive updates.

## Syntax

"constructionAxis_var" is a variable referencing a ConstructionAxis object.  

```python
# Get the value of the property.
propertyValue = constructionAxis_var.isDerived
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2026  

