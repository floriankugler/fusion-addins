# ExtrudeFeatureInput.isSolid Property

Parent Object: [ExtrudeFeatureInput](ExtrudeFeatureInput.md)  

## Description

Specifies if the extrusion should be created as a solid or surface. If it's a surface then there aren't any end caps and it's open. When an ExtrudeFeature input is created, this is initialized to true so a solid will be created if it's not changed.

## Syntax

"extrudeFeatureInput_var" is a variable referencing an ExtrudeFeatureInput object.  

```python
# Get the value of the property.
propertyValue = extrudeFeatureInput_var.isSolid

# Set the value of the property.
extrudeFeatureInput_var.isSolid = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |
| [Manage Participant Bodies API Sample](ParticipantBodiesSample_Sample.md) | Demonstrates how to manage participant During Cut operation. Same API can be used to manage participants During intersection also. |

## Version

Introduced in version March 2015  

