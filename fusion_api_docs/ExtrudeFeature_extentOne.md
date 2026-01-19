# ExtrudeFeature.extentOne Property

Parent Object: [ExtrudeFeature](ExtrudeFeature.md)  

## Description

Gets and sets the extent used for a single sided extrude or side one of a two-sided extrusion. Valid inputs are DistanceExtentDefinition, ToEntityExtentDefinition, and ThroughAllExtentDefinition object, which can be created statically using the create method on the classes.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"extrudeFeature_var" is a variable referencing an ExtrudeFeature object.  

```python
# Get the value of the property.
propertyValue = extrudeFeature_var.extentOne

# Set the value of the property.
extrudeFeature_var.extentOne = propertyValue
```

## Property Value

This is a read/write property whose value is an [ExtentDefinition](ExtentDefinition.md).

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |

## Version

Introduced in version November 2016  

