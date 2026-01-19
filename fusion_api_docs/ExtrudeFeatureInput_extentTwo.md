# ExtrudeFeatureInput.extentTwo Property

Parent Object: [ExtrudeFeatureInput](ExtrudeFeatureInput.md)  

## Description

Gets the extent assigned for side two of the extrusion. If the extrude is single sided extrude this property will return null. The hasTwoExtents property can be used to determine if there are two sides or not. To set the extent, use one of the set methods on the ExtrudeFeatureInput object.

## Syntax

"extrudeFeatureInput_var" is a variable referencing an ExtrudeFeatureInput object.  

```python
# Get the value of the property.
propertyValue = extrudeFeatureInput_var.extentTwo
```

## Property Value

This is a read only property whose value is an [ExtentDefinition](ExtentDefinition.md).

## Version

Introduced in version November 2016  

