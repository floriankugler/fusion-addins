# Decal.isLightBulbOn Property

Parent Object: [Decal](Decal.md)  

## Description

Gets and sets if the light bulb of this decal as displayed in the browser is on or off.  

A decal will only be visible if the light bulb is switched on. However, the light bulb can be on and the decal still invisible if the visibility of a higher level occurrence has its light bulb off or if the light bulb for the Decals folder is off to turn off all decals in a component.

## Syntax

"decal_var" is a variable referencing a Decal object.  

```python
# Get the value of the property.
propertyValue = decal_var.isLightBulbOn

# Set the value of the property.
decal_var.isLightBulbOn = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2024  

