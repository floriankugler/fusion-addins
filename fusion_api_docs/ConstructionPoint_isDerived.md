# ConstructionPoint.isDerived Property

Parent Object: [ConstructionPoint](ConstructionPoint.md)  

## Description

Returns if this construction point is derived from another design. If true, the construction point cannot be deleted. You should not attempt to make any edits to the derived construction point. Any edits made to this derived construction point will be lost when the derive updates.

## Syntax

"constructionPoint_var" is a variable referencing a ConstructionPoint object.  

```python
# Get the value of the property.
propertyValue = constructionPoint_var.isDerived
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2026  

