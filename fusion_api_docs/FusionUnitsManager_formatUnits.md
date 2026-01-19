# FusionUnitsManager.formatUnits Method

Parent Object: [FusionUnitsManager](FusionUnitsManager.md)  

## Description

Formats the unit according to the user preferences "centimeter" -> "cm" "inch" -> "in" "cm\* cm \*cm / s" -> , "cm^3 / s"

## Syntax

"fusionUnitsManager_var" is a variable referencing a [FusionUnitsManager](FusionUnitsManager.md) object.

```python
returnValue = fusionUnitsManager_var.formatUnits(units)
```

## Return Value

| Type | Description |
|----|----|
| string | Returns an empty string and GetLastError returns ExpressionError in the event of an error. |

## Parameters

| Name  | Type   | Description                                              |
|-------|--------|----------------------------------------------------------|
| units | string | The unit to use when converting the value into a string. |

## Version

Introduced in version August 2014  

