# ExtrudeFeature.startExtent Property

Parent Object: [ExtrudeFeature](ExtrudeFeature.md)  

## Description

Gets and sets the extent used to define the start of the extrusion. You can set this property with either a ProfilePlaneStartDefinition, OffsetStartDefinition or a EntityStartDefinition object. You can get any of those objects by using the static create method on the class.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"extrudeFeature_var" is a variable referencing an ExtrudeFeature object.  

```python
# Get the value of the property.
propertyValue = extrudeFeature_var.startExtent

# Set the value of the property.
extrudeFeature_var.startExtent = propertyValue
```

## Property Value

This is a read/write property whose value is an [ExtentDefinition](ExtentDefinition.md).

## Version

Introduced in version November 2016  

