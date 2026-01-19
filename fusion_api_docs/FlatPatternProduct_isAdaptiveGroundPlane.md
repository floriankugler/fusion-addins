# FlatPatternProduct.isAdaptiveGroundPlane Property

Parent Object: [FlatPatternProduct](FlatPatternProduct.md)  

## Description

Gets and sets if the position of the ground plane for this design is adaptive. If true, the ground plane will automatically move to be just below the model. The orientation of the ground plane is always normal to the "up" direction as defined by the view cube.

## Syntax

"flatPatternProduct_var" is a variable referencing a FlatPatternProduct object.  

```python
# Get the value of the property.
propertyValue = flatPatternProduct_var.isAdaptiveGroundPlane

# Set the value of the property.
flatPatternProduct_var.isAdaptiveGroundPlane = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2025  

