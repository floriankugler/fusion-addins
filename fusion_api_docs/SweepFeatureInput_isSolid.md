# SweepFeatureInput.isSolid Property

Parent Object: [SweepFeatureInput](SweepFeatureInput.md)  

## Description

Specifies if the sweep should be created as a solid or surface. If it's a surface then there aren't any end caps and it's open. This is initialized to true so a solid will be created if it's not changed.

## Syntax

"sweepFeatureInput_var" is a variable referencing a SweepFeatureInput object.  

```python
# Get the value of the property.
propertyValue = sweepFeatureInput_var.isSolid

# Set the value of the property.
sweepFeatureInput_var.isSolid = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version March 2015  

