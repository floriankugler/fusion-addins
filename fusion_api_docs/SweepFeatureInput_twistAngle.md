# SweepFeatureInput.twistAngle Property

Parent Object: [SweepFeatureInput](SweepFeatureInput.md)  

## Description

Gets and sets the twist angle of the sweep. This property is initialized with a twist angle of zero. When sweeping a solid setting the twist angle requires the solid twist axis to be set.  

This property is ignored if a guide rail or surface has been specified. This property is valid for both parametric and non-parametric extrusions.

## Syntax

"sweepFeatureInput_var" is a variable referencing a SweepFeatureInput object.  

```python
# Get the value of the property.
propertyValue = sweepFeatureInput_var.twistAngle

# Set the value of the property.
sweepFeatureInput_var.twistAngle = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version December 2017  

