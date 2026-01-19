# UnitsManager.defaultLengthUnits Property

Parent Object: [UnitsManager](UnitsManager.md)  

## Description

Returns the unit strings for the current default length unit as specified in preferences. - e.g. "cm" or "in" This is the string that is being used by Fusion to represent the current length unit and is affected by the preference settings that let the user choose whether abbreviations and symbols can be used. This means that inch length units can be returned as inch, in, or ". If you need a consistent way of determining the current length unit, the distanceDisplayUnits of the FusionUnitsManager object returns an enum value.

## Syntax

"unitsManager_var" is a variable referencing a UnitsManager object.  

```python
# Get the value of the property.
propertyValue = unitsManager_var.defaultLengthUnits
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Get Volume of Active Design API Sample](GetsVolumeOfActiveDesign_Sample.md) | Traverses through the active design and totals the volume of every body within the design. |

## Version

Introduced in version August 2014  

