# JointOriginInput.globalOrientParamOne Property

Parent Object: [JointOriginInput](JointOriginInput.md)  

## Description

Gets and sets the value that defines the first global orient parameter for the joint origin. This defaults to zero if it's not specified. For Cylineder or cone, it represents the angle around the center axis. For Sphere and Torus, it represents the angle around the center axis. For Spline, it represents the U parameter.

## Syntax

"jointOriginInput_var" is a variable referencing a JointOriginInput object.  

```python
# Get the value of the property.
propertyValue = jointOriginInput_var.globalOrientParamOne

# Set the value of the property.
jointOriginInput_var.globalOrientParamOne = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version May 2025  

