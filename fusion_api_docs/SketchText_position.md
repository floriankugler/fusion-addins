# SketchText.position Property

Parent Object: [SketchText](SketchText.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets the position of the text on the x-y plane of the sketch. The text must lie on the x-y plane so the Z component of the point is ignored and always treated as zero.

## Remarks

This property has been retired as a result of Fusion adding support for text along a curve. To move text, you can use the Sketch.move method.

## Syntax

"sketchText_var" is a variable referencing a SketchText object.  

```python
# Get the value of the property.
propertyValue = sketchText_var.position

# Set the value of the property.
sketchText_var.position = propertyValue
```

## Property Value

This is a read/write property whose value is a [Point3D](Point3D.md).

## Version

Introduced in version March 2015  
Retired in version January 2021  

