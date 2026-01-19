# Sketch.isDerived Property

Parent Object: [Sketch](Sketch.md)  

## Description

Returns if this sketch is derived from another design. If true, the sketch cannot be deleted. You should not attempt to make any edits to the derived sketch. Any edits made to this derived sketch will be lost when the derive updates.

## Syntax

"sketch_var" is a variable referencing a Sketch object.  

```python
# Get the value of the property.
propertyValue = sketch_var.isDerived
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2026  

