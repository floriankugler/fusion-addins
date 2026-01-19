# ConstructionPlane.isDerived Property

Parent Object: [ConstructionPlane](ConstructionPlane.md)  

## Description

Returns if this construction plane is derived from another design. If true, the construction plane cannot be deleted. You should not attempt to make any edits to the derived construction plane. Any edits made to this derived construction plane will be lost when the derive updates.

## Syntax

"constructionPlane_var" is a variable referencing a ConstructionPlane object.  

```python
# Get the value of the property.
propertyValue = constructionPlane_var.isDerived
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2026  

