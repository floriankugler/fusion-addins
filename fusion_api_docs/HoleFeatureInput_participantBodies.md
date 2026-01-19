# HoleFeatureInput.participantBodies Property

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

Gets and sets the list of bodies that will participate in the hole.  

If this property has not been set, the default behavior is that all bodies that are intersected by the hole will participate.  

This property can return null in the case where the feature has not been fully defined so that possible intersecting bodies can be computed.

## Syntax

"holeFeatureInput_var" is a variable referencing a HoleFeatureInput object.  

```python
# Get the value of the property.
propertyValue = holeFeatureInput_var.participantBodies

# Set the value of the property.
holeFeatureInput_var.participantBodies = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepBody](BRepBody.md).

## Version

Introduced in version January 2017  

