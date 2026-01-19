# SketchEllipticalArc.majorAxisRadius Property

Parent Object: [SketchEllipticalArc](SketchEllipticalArc.md)  

## Description

Gets and sets the major axis radius of the elliptical arc. Changing the radius is limited by any constraints that might exist on the elliptical arc. Setting the radius can fail in cases where the radius is fully defined through constraints.

## Syntax

"sketchEllipticalArc_var" is a variable referencing a SketchEllipticalArc object.  

```python
# Get the value of the property.
propertyValue = sketchEllipticalArc_var.majorAxisRadius

# Set the value of the property.
sketchEllipticalArc_var.majorAxisRadius = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version August 2014  

