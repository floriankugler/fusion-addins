# CoilFeatureInput.isSolid Property

Parent Object: [CoilFeatureInput](CoilFeatureInput.md)  

## Description

Specifies if the coil should be created as a solid or surface. This is initialized to true so a solid will be created if it's not changed. It only can be set to false in non-parametric modeling.

## Syntax

"coilFeatureInput_var" is a variable referencing a CoilFeatureInput object.  

```python
# Get the value of the property.
propertyValue = coilFeatureInput_var.isSolid

# Set the value of the property.
coilFeatureInput_var.isSolid = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version March 2016  

