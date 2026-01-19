# SketchEllipticalArc.majorAxis Property

Parent Object: [SketchEllipticalArc](SketchEllipticalArc.md)  

## Description

Gets and sets the major axis direction of the elliptical arc. Changing the axis is limited by any constraints that might exist on the elliptical arc. Setting the axis can fail in cases where the direction is fully defined through constraints.

## Syntax

"sketchEllipticalArc_var" is a variable referencing a SketchEllipticalArc object.  

```python
# Get the value of the property.
propertyValue = sketchEllipticalArc_var.majorAxis

# Set the value of the property.
sketchEllipticalArc_var.majorAxis = propertyValue
```

## Property Value

This is a read/write property whose value is a [Vector3D](Vector3D.md).

## Version

Introduced in version August 2014  

