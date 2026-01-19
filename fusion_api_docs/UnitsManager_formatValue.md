# UnitsManager.formatValue Method

Parent Object: [UnitsManager](UnitsManager.md)  

## Description

Given a floating point number this method evaluates it as a value of a specific unit type and returns an appropriate string. By default, the current unit settings defined in the user preferences is used, but you can set the method arguments to override the defaults to specify the formatting you want. The input value always uses internal units, which are centimeters for length, radians for angles, and mass is in kilograms.  

This method is useful whenever you have a value you've gotten from Fusion or computed on your own and need to display it to the user as a string. This method does the conversion and also takes into account the units and the formatting the user has specified in their preferences.  

Below are some examples of various formatting where the user preferences for general precision is four decimal places, and the angular precision is one decimal place. Also, trailing zeros are set to be hidden and the minimum precision is two decimal places when trailing zeros are turned off. The design units are specified to be "inch".  

Here, only the value is supplied and the default is to assume the units are the current design length unit and use the preference settings to format it so there are four decimal places shown and the unit name is included. formatValue(1.5) -> "0.5906 in"  

In this example, an angle is specified by using "deg" as the unit, and the result showing one decimal place, which is what's defined in the user preference, and it shows the unit name. formatValue(0.7853981633974483096, "deg") -> "45.0 deg"  

This example converts the input value of 1.5 cm to mm where eight decimal places are shown, trailing zeros are shown, and the unit name is shown. The fourth argument of minimum precision is ignored, since it is only used when showTrailing zeros is False. formatValue(1.5, "mm", 8, BooleanOptions.TrueBooleanOption, 0, True) - > "15.00000000 mm"

## Syntax

"unitsManager_var" is a variable referencing a [UnitsManager](UnitsManager.md) object.

```python
# Uses no optional arguments.
returnValue = unitsManager_var.formatValue(value)

# Uses optional arguments.
returnValue = unitsManager_var.formatValue(value, units, precision, showTrailingZeros, minimumPrecision, showUnits)
```

## Return Value

| Type | Description |
|----|----|
| string | Returns the formatted string or an empty string in case of an error. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| value | double | A floating point value that is assumed to use the internal unit type, which are centimeters for length, radians for angles, and mass is in kilograms. |
| units | string | The units the value represents. The default value for this argument is "DefaultDistance" which means it will use the default distance units defined for the active design. This is an optional argument whose default value is "DefaultDistance". |
| precision | integer | This specifies the number of decimal places to display. The default value is -1 which indicates the precision specified in preferences should be used. A maximum of 9 can be used and any larger numbers will be forced to 9. This is an optional argument whose default value is -1. |
| showTrailingZeros | [BooleanOptions](BooleanOptions.md) | Specifies if trailing zeros should be shown or not. The default value is to use the preference setting. This is an optional argument whose default value is BooleanOptions.DefaultBooleanOption. |
| minimumPrecision | integer | When trailing zeros are not displayed, this specifies a minimum precision where some trailing zeros are still shown. The default value is -1 which indicates the minimum precision specified in preferences should be used. A maximum of 8 can be used, and any larger numbers will be forced to 8. This is an optional argument whose default value is -1. |
| showUnits | boolean | This specifies whether the unit name or symbol should be included in the result. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
|----|----|
| [Get Volume of Active Design API Sample](GetsVolumeOfActiveDesign_Sample.md) | Traverses through the active design and totals the volume of every body within the design. |

## Version

Introduced in version March 2024  

