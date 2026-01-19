# ExtrudeFeature.extentTwo Property

Parent Object: [ExtrudeFeature](ExtrudeFeature.md)  

## Description

Gets and sets the extent used for side two of the extrusion. If the extrude is a single sided extrude this property will return null and will fail if set. The hasTwoExtents property can be used to determine if there are two sides or not. When setting this property, valid inputs are DistanceExtentDefinition, ToEntityExtentDefinition, and ThroughAllExtentDefinition object, which can be created statically using the create method on the classes.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"extrudeFeature_var" is a variable referencing an ExtrudeFeature object.  

```python
# Get the value of the property.
propertyValue = extrudeFeature_var.extentTwo

# Set the value of the property.
extrudeFeature_var.extentTwo = propertyValue
```

## Property Value

This is a read/write property whose value is an [ExtentDefinition](ExtentDefinition.md).

## Version

Introduced in version November 2016  

