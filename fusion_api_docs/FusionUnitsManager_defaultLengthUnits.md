# FusionUnitsManager.defaultLengthUnits Property

Parent Object: [FusionUnitsManager](FusionUnitsManager.md)  

## Description

Returns the unit strings for the current default length unit as specified in preferences. - e.g. "cm" or "in" This is the string that is being used by Fusion to represent the current length unit and is affected by the preference settings that let the user choose whether abbreviations and symbols can be used. This means that inch length units can be returned as inch, in, or ". If you need a consistent way of determining the current length unit, the distanceDisplayUnits of the FusionUnitsManager object returns an enum value.

## Syntax

"fusionUnitsManager_var" is a variable referencing a FusionUnitsManager object.  

```python
# Get the value of the property.
propertyValue = fusionUnitsManager_var.defaultLengthUnits
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version August 2014  

