# SketchRadialDimension.isDriving Property

Parent Object: [SketchRadialDimension](SketchRadialDimension.md)  

## Description

Gets and sets if the dimension is Driving or is Driven. Setting this property to true for a given dimension may fail if the result would over constrain the sketch. Fusion does not allow over-constrained sketches.

## Syntax

"sketchRadialDimension_var" is a variable referencing a SketchRadialDimension object.  

```python
# Get the value of the property.
propertyValue = sketchRadialDimension_var.isDriving

# Set the value of the property.
sketchRadialDimension_var.isDriving = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2015  

