# SketchArc.radius Property

Parent Object: [SketchArc](SketchArc.md)  

## Description

Gets and sets the radius of the arc. Changing the radius is limited by any constraints that might exist on the circle. Setting the radius can fail in cases where the radius is fully defined through constraints.

## Syntax

"sketchArc_var" is a variable referencing a SketchArc object.  

```python
# Get the value of the property.
propertyValue = sketchArc_var.radius

# Set the value of the property.
sketchArc_var.radius = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version August 2014  

