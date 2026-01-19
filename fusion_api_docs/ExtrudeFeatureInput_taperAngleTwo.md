# ExtrudeFeatureInput.taperAngleTwo Property

Parent Object: [ExtrudeFeatureInput](ExtrudeFeatureInput.md)  

## Description

Gets the value that will be used as the taper angle for side two of a two-sided extrusion. If the extrusion is single-sided, this property will return null. The hasTwoExtents property can be used to determine if there are two sides or not. To set the taper angle, use one of the set methods on the ExtrudeFeatureInput object.

## Syntax

"extrudeFeatureInput_var" is a variable referencing an ExtrudeFeatureInput object.  

```python
# Get the value of the property.
propertyValue = extrudeFeatureInput_var.taperAngleTwo
```

## Property Value

This is a read only property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version November 2016  

