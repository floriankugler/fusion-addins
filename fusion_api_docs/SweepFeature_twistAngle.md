# SweepFeature.twistAngle Property

Parent Object: [SweepFeature](SweepFeature.md)  

## Description

Gets the ModelParameter that defines the twist angle of the sweep feature. The value of the angle can be edited by using the properties on the ModelParameter object to edit the parameter. When sweeping a solid setting the twist angle requires the solid twist axis to be set. This property is ignored if a guide rail or surface has been specified.

## Syntax

"sweepFeature_var" is a variable referencing a SweepFeature object.  

```python
# Get the value of the property.
propertyValue = sweepFeature_var.twistAngle
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version December 2017  

