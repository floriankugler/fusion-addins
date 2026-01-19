# Joint.isLightBulbOn Property

Parent Object: [Joint](Joint.md)  

## Description

Gets and sets if the light bulb of this joint as displayed in the browser is on or off. A joint will only be visible if the light bulb is switched on. However, the light bulb can be on and the joint still invisible if a higher level occurrence in the assembly context is not visible because its light bulb is off or the joints folder is light bulb is off.

## Syntax

"joint_var" is a variable referencing a Joint object.  

```python
# Get the value of the property.
propertyValue = joint_var.isLightBulbOn

# Set the value of the property.
joint_var.isLightBulbOn = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2016  

