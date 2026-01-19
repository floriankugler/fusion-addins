# BossFeatureInput.participantBodies Property

Parent Object: [BossFeatureInput](BossFeatureInput.md)  

## Description

Gets and sets the list of bodies that will participate in the boss feature. If body provided does not intersect with direction vector at proposed position points it will be ignored. If more bodies intersect at given position point only the closest body will be accepted. Boss feature works with solid bodies only. If this property has not been set (or is empty) closest visible bodies will be detected automatically based on proposed positions and orientation.

## Syntax

"bossFeatureInput_var" is a variable referencing a BossFeatureInput object.  

```python
# Get the value of the property.
propertyValue = bossFeatureInput_var.participantBodies

# Set the value of the property.
bossFeatureInput_var.participantBodies = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepBody](BRepBody.md).

## Version

Introduced in version October 2022  

