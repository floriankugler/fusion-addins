# SweepFeatureInput.solidAlignedAxis Property

Parent Object: [SweepFeatureInput](SweepFeatureInput.md)  

## Description

Gets and sets the axis to align the solid being swept with. The axis is used when sweeping a solid, and the solid orientation is set to AlignedSolidOrientationType. It can be a sketch line, linear edge, or construction axis.

## Syntax

"sweepFeatureInput_var" is a variable referencing a SweepFeatureInput object.  

```python
# Get the value of the property.
propertyValue = sweepFeatureInput_var.solidAlignedAxis

# Set the value of the property.
sweepFeatureInput_var.solidAlignedAxis = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version May 2024  

