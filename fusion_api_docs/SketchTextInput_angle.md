# SketchTextInput.angle Property

Parent Object: [SketchTextInput](SketchTextInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets the angle of the text relative to the x-axis of the x-y plane of the sketch.

## Remarks

This property was retired when Fusion added support for sketch along a curve, where defining a rotation angle doesn't make sense. When creating multi-line text you can use the Sketch.move command to rotate and/or move the four lines defining the bounding rectangle of the text.

## Syntax

"sketchTextInput_var" is a variable referencing a SketchTextInput object.  

```python
# Get the value of the property.
propertyValue = sketchTextInput_var.angle

# Set the value of the property.
sketchTextInput_var.angle = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version March 2015  
Retired in version January 2021  

