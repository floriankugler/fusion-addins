# SketchConicCurve.isReference Property

Parent Object: [SketchConicCurve](SketchConicCurve.md)  

## Description

Indicates if this geometry is a reference. Changing this property from true to false removes the reference. This property can not be set to true if it is already false.

## Syntax

"sketchConicCurve_var" is a variable referencing a SketchConicCurve object.  

```python
# Get the value of the property.
propertyValue = sketchConicCurve_var.isReference

# Set the value of the property.
sketchConicCurve_var.isReference = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2015  

