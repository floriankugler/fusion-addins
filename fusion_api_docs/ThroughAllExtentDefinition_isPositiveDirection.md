# ThroughAllExtentDefinition.isPositiveDirection Property

Parent Object: [ThroughAllExtentDefinition](ThroughAllExtentDefinition.md)  

## Description

Gets and sets if the direction is positive or negative. A value of true indicates it is in the same direction as the z direction of the profile's sketch plane.  

This is only used when the extrusion is only defined in a single direction from the profile plane. If it's a two sided extrusion, this value is ignored.

## Syntax

"throughAllExtentDefinition_var" is a variable referencing a ThroughAllExtentDefinition object.  

```python
# Get the value of the property.
propertyValue = throughAllExtentDefinition_var.isPositiveDirection

# Set the value of the property.
throughAllExtentDefinition_var.isPositiveDirection = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |

## Version

Introduced in version November 2016  

