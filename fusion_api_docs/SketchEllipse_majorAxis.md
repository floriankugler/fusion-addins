# SketchEllipse.majorAxis Property

Parent Object: [SketchEllipse](SketchEllipse.md)  

## Description

Gets and sets the major axis direction of the ellipse. Changing the axis is limited by any constraints that might exist on the ellipse. Setting the axis can fail in cases where the direction is fully defined through constraints.

## Syntax

"sketchEllipse_var" is a variable referencing a SketchEllipse object.  

```python
# Get the value of the property.
propertyValue = sketchEllipse_var.majorAxis

# Set the value of the property.
sketchEllipse_var.majorAxis = propertyValue
```

## Property Value

This is a read/write property whose value is a [Vector3D](Vector3D.md).

## Version

Introduced in version August 2014  

