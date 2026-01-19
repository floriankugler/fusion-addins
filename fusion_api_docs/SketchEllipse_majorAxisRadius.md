# SketchEllipse.majorAxisRadius Property

Parent Object: [SketchEllipse](SketchEllipse.md)  

## Description

Gets and sets the major axis radius of the ellipse. Changing the radius is limited by any constraints that might exist on the ellipse. Setting the radius can fail in cases where the radius is fully defined through constraints.

## Syntax

"sketchEllipse_var" is a variable referencing a SketchEllipse object.  

```python
# Get the value of the property.
propertyValue = sketchEllipse_var.majorAxisRadius

# Set the value of the property.
sketchEllipse_var.majorAxisRadius = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version August 2014  

