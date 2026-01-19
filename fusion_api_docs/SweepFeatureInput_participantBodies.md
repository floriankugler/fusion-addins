# SweepFeatureInput.participantBodies Property

Parent Object: [SweepFeatureInput](SweepFeatureInput.md)  

## Description

Gets and sets the list of bodies that will participate in the feature when the operation is a cut or intersection.  

If this property has not been set, the default behavior is that all bodies that are intersected by the feature will participate.  

This property can return null in the case where the feature has not been fully defined so that possible intersecting bodies can be computed.

## Syntax

"sweepFeatureInput_var" is a variable referencing a SweepFeatureInput object.  

```python
# Get the value of the property.
propertyValue = sweepFeatureInput_var.participantBodies

# Set the value of the property.
sweepFeatureInput_var.participantBodies = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepBody](BRepBody.md).

## Version

Introduced in version January 2017  

