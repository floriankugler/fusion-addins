# JointOrigin.isLightBulbOn Property

Parent Object: [JointOrigin](JointOrigin.md)  

## Description

Gets and sets if the light bulb of this jointOrigin as displayed in the browser is on or off. A joint origin will only be visible if the light bulb is switched on. However, the light bulb can be on and the joint origin still invisible if a higher level occurrence in the assembly context is not visible because its light bulb is off or the joint origins folder light bulb is off.

## Syntax

"jointOrigin_var" is a variable referencing a JointOrigin object.  

```python
# Get the value of the property.
propertyValue = jointOrigin_var.isLightBulbOn

# Set the value of the property.
jointOrigin_var.isLightBulbOn = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2022  

