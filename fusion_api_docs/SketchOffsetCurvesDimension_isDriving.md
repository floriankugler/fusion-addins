# SketchOffsetCurvesDimension.isDriving Property

Parent Object: [SketchOffsetCurvesDimension](SketchOffsetCurvesDimension.md)  

## Description

Gets and sets if the dimension is Driving or is Driven. Setting this property to true for a given dimension may fail if the result would over constrain the sketch. Fusion does not allow over-constrained sketches.

## Syntax

"sketchOffsetCurvesDimension_var" is a variable referencing a SketchOffsetCurvesDimension object.  

```python
# Get the value of the property.
propertyValue = sketchOffsetCurvesDimension_var.isDriving

# Set the value of the property.
sketchOffsetCurvesDimension_var.isDriving = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version March 2016  

