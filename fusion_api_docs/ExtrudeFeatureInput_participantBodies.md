# ExtrudeFeatureInput.participantBodies Property

Parent Object: [ExtrudeFeatureInput](ExtrudeFeatureInput.md)  

## Description

Gets and sets the list of bodies that will participate in the feature when the operation is a cut or intersection.  

If this property has not been set, the default behavior is that all bodies that are intersected by the feature will participate.  

This property can return null in the case where the feature has not been fully defined so that possible intersecting bodies can be computed.

## Syntax

"extrudeFeatureInput_var" is a variable referencing an ExtrudeFeatureInput object.  

```python
# Get the value of the property.
propertyValue = extrudeFeatureInput_var.participantBodies

# Set the value of the property.
extrudeFeatureInput_var.participantBodies = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepBody](BRepBody.md).

## Samples

| Name | Description |
|----|----|
| [Manage Participant Bodies API Sample](ParticipantBodiesSample_Sample.md) | Demonstrates how to manage participant During Cut operation. Same API can be used to manage participants During intersection also. |

## Version

Introduced in version January 2017  

