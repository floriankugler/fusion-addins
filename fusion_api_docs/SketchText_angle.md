# SketchText.angle Property

Parent Object: [SketchText](SketchText.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets the angle of the text relative to the x-axis of the x-y plane of the sketch.

## Remarks

This was retired when Fusion added support for sketch along a curve and multi-line text, which neither supports getting and setting an angle. For multi-line text you can get the rectangle sketch lines that define the boundary of the text and manipulate those to move and rotate the text.

## Syntax

"sketchText_var" is a variable referencing a SketchText object.  

```python
# Get the value of the property.
propertyValue = sketchText_var.angle

# Set the value of the property.
sketchText_var.angle = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version March 2015  
Retired in version January 2021  

