# SketchLinearDimension.isDriving Property

Parent Object: [SketchLinearDimension](SketchLinearDimension.md)  

## Description

Gets and sets if the dimension is Driving or is Driven. Setting this property to true for a given dimension may fail if the result would over constrain the sketch. Fusion does not allow over-constrained sketches.

## Syntax

"sketchLinearDimension_var" is a variable referencing a SketchLinearDimension object.  

```python
# Get the value of the property.
propertyValue = sketchLinearDimension_var.isDriving

# Set the value of the property.
sketchLinearDimension_var.isDriving = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2015  

