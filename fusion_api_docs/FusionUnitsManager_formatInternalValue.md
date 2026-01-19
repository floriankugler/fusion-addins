# FusionUnitsManager.formatInternalValue Method

Parent Object: [FusionUnitsManager](FusionUnitsManager.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Formats the internal value as a string. The output string is formatted using the current unit settings in preferences. The preferences control the number of decimal places, whether units are abbreviated and several other things. FormatInternalValue(1.5, "in") -> "0.591 in" FormatInternalValue(1.5, "in", false) -> "0.591" FormatInternalValue(1.5, "mm", true) -> "15.00 mm" FormatInternalValue(1.5) -> depends on DistanceUnits, might be "15.0 mm"

## Remarks

This property has been replaced by the formatValue method. This method does not honor the preferences for the precision, as it's supposed to. The formatValue method provides this capability and the ability to override the preference settings and specify how the value should be formatted.

## Syntax

"fusionUnitsManager_var" is a variable referencing a [FusionUnitsManager](FusionUnitsManager.md) object.

```python
# Uses no optional arguments.
returnValue = fusionUnitsManager_var.formatInternalValue(internalValue)

# Uses optional arguments.
returnValue = fusionUnitsManager_var.formatInternalValue(internalValue, displayUnits, showUnits)
```

## Return Value

| Type   | Description                                                     |
|--------|-----------------------------------------------------------------|
| string | Returns an empty string if the units are incorrectly specified. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| internalValue | double | The internal value to format. |
| displayUnits | string | The units to display the value in. If not supplied the units will default to the default length specified in the preferences. This is an optional argument whose default value is "DefaultDistance". |
| showUnits | boolean | Specify false to exclude units from the format. The default is true. This is an optional argument whose default value is True. |

## Version

Introduced in version August 2014  
Retired in version January 2025  

