# ExtrudeFeature.taperAngleTwo Property

Parent Object: [ExtrudeFeature](ExtrudeFeature.md)  

## Description

Gets the parameter controlling the taper angle for side two of a two-sided extrusion. if the extrusion is single-sided, this property will return null. The hasTwoExtents property can be used to determine if there are two sides or not. To edit the angle, use properties on the parameter to change the value of the parameter.

## Syntax

"extrudeFeature_var" is a variable referencing an ExtrudeFeature object.  

```python
# Get the value of the property.
propertyValue = extrudeFeature_var.taperAngleTwo
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version November 2016  

