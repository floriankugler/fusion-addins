# FusionUnitsManager.unitSystem Property

Parent Object: [FusionUnitsManager](FusionUnitsManager.md)  

## Description

Gets and sets the pre-defined combination of length and mass units to use for the units in the design. The distanceDisplayUnits and massDisplayUnits properties provide a way to get the current setting for distance and mass and to modify them to other values besides the predefined combinations. When a custom unit system is specified, any combination of distance and mass can be specified.

## Syntax

"fusionUnitsManager_var" is a variable referencing a FusionUnitsManager object.  

```python
# Get the value of the property.
propertyValue = fusionUnitsManager_var.unitSystem

# Set the value of the property.
fusionUnitsManager_var.unitSystem = propertyValue
```

## Property Value

This is a read/write property whose value is a [UnitSystems](UnitSystems.md).

## Version

Introduced in version May 2025  

