# SweepFeature.solidTwistAxis Property

Parent Object: [SweepFeature](SweepFeature.md)  

## Description

Gets and sets the twist axis of the solid being swept. The axis is used when sweeping a solid, and the twist angle is set. It can be a sketch line, linear edge, construction axis, or a face that defines an axis (cylinder, cone, torus, etc.).

## Syntax

"sweepFeature_var" is a variable referencing a SweepFeature object.  

```python
# Get the value of the property.
propertyValue = sweepFeature_var.solidTwistAxis

# Set the value of the property.
sweepFeature_var.solidTwistAxis = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version May 2024  

