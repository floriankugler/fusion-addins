# Occurrence.isLightBulbOn Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Gets and sets if the light bulb of this occurrence as displayed in the browser is on or off. An occurrence will only be visible if the light bulb is switched on. However, the light bulb can be on and the occurrence still invisible if a higher level occurrence in the assembly context is not visible because its light bulb is off.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.isLightBulbOn

# Set the value of the property.
occurrence_var.isLightBulbOn = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

