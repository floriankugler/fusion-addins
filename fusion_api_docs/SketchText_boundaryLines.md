# SketchText.boundaryLines Property

Parent Object: [SketchText](SketchText.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Returns the four sketch lines that define the boundary of the sketch text. By adding constraints to these lines you can associatively control the size, position and angle of the sketch text.

## Remarks

This was retired when Fusion added support for sketch along a curve, which doesn't have the boundary lines. This functionality is replaced by the MultiLineTextDefinition.rectangleLines property.

## Syntax

"sketchText_var" is a variable referencing a SketchText object.  

```python
# Get the value of the property.
propertyValue = sketchText_var.boundaryLines
```

## Property Value

This is a read only property whose value is a [SketchLineList](SketchLineList.md).

## Version

Introduced in version March 2015  
Retired in version January 2021  

