# SweepFeature.extent Property

Parent Object: [SweepFeature](SweepFeature.md)  

## Description

Gets and sets the sweep extent type. It defaults to PerpendicularToPathExtentType. When sweeping a solid setting the twist angle requires the solid twist axis to be set. This property is ignored when a guide rail has not been specified.

## Syntax

"sweepFeature_var" is a variable referencing a SweepFeature object.  

```python
# Get the value of the property.
propertyValue = sweepFeature_var.extent

# Set the value of the property.
sweepFeature_var.extent = propertyValue
```

## Property Value

This is a read/write property whose value is a [SweepExtentTypes](SweepExtentTypes.md).

## Version

Introduced in version December 2020  

