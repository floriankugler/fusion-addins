# SweepFeatureInput.solidOrientation Property

Parent Object: [SweepFeatureInput](SweepFeatureInput.md)  

## Description

Gets and sets the solid sweep orientation. It defaults to PerpendicularSolidOrientationType. Setting the solid orientation to AlignedSolidOrientationType requires the solid aligned axis to be set. This property is ignored if sweeping a profile.

## Syntax

"sweepFeatureInput_var" is a variable referencing a SweepFeatureInput object.  

```python
# Get the value of the property.
propertyValue = sweepFeatureInput_var.solidOrientation

# Set the value of the property.
sweepFeatureInput_var.solidOrientation = propertyValue
```

## Property Value

This is a read/write property whose value is a [SweepSolidOrientationTypes](SweepSolidOrientationTypes.md).

## Version

Introduced in version May 2024  

