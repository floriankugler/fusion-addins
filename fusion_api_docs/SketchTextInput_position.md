# SketchTextInput.position Property

Parent Object: [SketchTextInput](SketchTextInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets the position of the text on the x-y plane of the sketch. The text must lie on the x-y plane so the Z component of the point is ignored and always treated as zero.

## Remarks

This method has been retired. The closest equivalent is when creating multi-line text. The setAsMultiLine has a cornerPoint argument that lets you define the position of the text. For text along a curve, the curve defines its positions.

## Syntax

"sketchTextInput_var" is a variable referencing a SketchTextInput object.  

```python
# Get the value of the property.
propertyValue = sketchTextInput_var.position

# Set the value of the property.
sketchTextInput_var.position = propertyValue
```

## Property Value

This is a read/write property whose value is a [Point3D](Point3D.md).

## Version

Introduced in version March 2015  
Retired in version January 2023  

