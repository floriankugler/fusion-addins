# Canvas.isDerived Property

Parent Object: [Canvas](Canvas.md)  

## Description

Returns if this canvas is derived from another design. If true, the canvas cannot be deleted. You should not attempt to make any edits to the derived canvas. Any edits made to this derived canvas will be lost when the derive updates.

## Syntax

"canvas_var" is a variable referencing a Canvas object.  

```python
# Get the value of the property.
propertyValue = canvas_var.isDerived
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2026  

