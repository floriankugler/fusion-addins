# RevolveFeatureInput.isSolid Property

Parent Object: [RevolveFeatureInput](RevolveFeatureInput.md)  

## Description

Specifies if the revolution should be created as a solid or surface. If it's a surface then there aren't any end caps and it's open. This is initialized to true so a solid will be created if it's not changed.

## Syntax

"revolveFeatureInput_var" is a variable referencing a RevolveFeatureInput object.  

```python
# Get the value of the property.
propertyValue = revolveFeatureInput_var.isSolid

# Set the value of the property.
revolveFeatureInput_var.isSolid = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version March 2015  

