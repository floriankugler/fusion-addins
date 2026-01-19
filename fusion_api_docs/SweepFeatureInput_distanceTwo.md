# SweepFeatureInput.distanceTwo Property

Parent Object: [SweepFeatureInput](SweepFeatureInput.md)  

## Description

Gets and sets the distance for the second side. The distance is a value from 0 to 1 indicating the position along the path where 0 is at the start and 1 is at the end. The value defaults to 0 in the case where the path is closed, otherwise it defaults to 1.0. It is ignored if the path is only on one side of the profile or if the sweep definition includes a guide rail. It's always the distance against the normal of the profile if available.

## Syntax

"sweepFeatureInput_var" is a variable referencing a SweepFeatureInput object.  

```python
# Get the value of the property.
propertyValue = sweepFeatureInput_var.distanceTwo

# Set the value of the property.
sweepFeatureInput_var.distanceTwo = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version January 2015  

