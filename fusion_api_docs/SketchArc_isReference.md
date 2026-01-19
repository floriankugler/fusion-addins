# SketchArc.isReference Property

Parent Object: [SketchArc](SketchArc.md)  

## Description

Indicates if this geometry is a reference. Changing this property from true to false removes the reference. This property can not be set to true if it is already false.

## Syntax

"sketchArc_var" is a variable referencing a SketchArc object.  

```python
# Get the value of the property.
propertyValue = sketchArc_var.isReference

# Set the value of the property.
sketchArc_var.isReference = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

