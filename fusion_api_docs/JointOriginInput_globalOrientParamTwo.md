# JointOriginInput.globalOrientParamTwo Property

Parent Object: [JointOriginInput](JointOriginInput.md)  

## Description

Gets and sets the value that defines the second global orient parameter for the joint origin. This defaults to zero if it's not specified. For Cylinder or cone, it is not used. For Sphere, it represents the polar angle, which is the angle between the radius line and the equator plane. For Torus, it represents the angle around the center of the section circle. For Spline, it represents the V parameter.

## Syntax

"jointOriginInput_var" is a variable referencing a JointOriginInput object.  

```python
# Get the value of the property.
propertyValue = jointOriginInput_var.globalOrientParamTwo

# Set the value of the property.
jointOriginInput_var.globalOrientParamTwo = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version May 2025  

