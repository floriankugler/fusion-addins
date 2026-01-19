# Decal.isDerived Property

Parent Object: [Decal](Decal.md)  

## Description

Returns if this decal is derived from another design. If true, the canvas cannot be deleted. You should not attempt to make any edits to the derived decal. Any edits made to this derived decal will be lost when the derive updates.

## Syntax

"decal_var" is a variable referencing a Decal object.  

```python
# Get the value of the property.
propertyValue = decal_var.isDerived
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2026  

