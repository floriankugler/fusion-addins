# SweepFeatureInput.taperAngle Property

Parent Object: [SweepFeatureInput](SweepFeatureInput.md)  

## Description

Gets and sets the taper angle of the sweep. This property is initialized with a taper angle of zero. A negative angle will taper the sweep inward while a positive value will taper the sweep outward.  

This property is ignored if sweeping a solid or a guide rail or surface has been specified. This property is valid for both parametric and non-parametric extrusions.

## Syntax

"sweepFeatureInput_var" is a variable referencing a SweepFeatureInput object.  

```python
# Get the value of the property.
propertyValue = sweepFeatureInput_var.taperAngle

# Set the value of the property.
sweepFeatureInput_var.taperAngle = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version December 2017  

