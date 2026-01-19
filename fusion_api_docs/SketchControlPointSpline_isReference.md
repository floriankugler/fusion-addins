# SketchControlPointSpline.isReference Property

Parent Object: [SketchControlPointSpline](SketchControlPointSpline.md)  

## Description

Indicates if this geometry is a reference. Changing this property from true to false removes the reference. This property can not be set to true if it is already false.

## Syntax

"sketchControlPointSpline_var" is a variable referencing a SketchControlPointSpline object.  

```python
# Get the value of the property.
propertyValue = sketchControlPointSpline_var.isReference

# Set the value of the property.
sketchControlPointSpline_var.isReference = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2022  

