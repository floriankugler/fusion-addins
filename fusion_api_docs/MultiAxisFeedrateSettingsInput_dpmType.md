# MultiAxisFeedrateSettingsInput.dpmType Property

Parent Object: [MultiAxisFeedrateSettingsInput](MultiAxisFeedrateSettingsInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

If the feedMode is MultiAxisFeedMode.MultiAxisFeedMode_DegreesPerMinute, determines what type of MultiAxisCombinationDPMFeedrateSettings will create.

## Syntax

"multiAxisFeedrateSettingsInput_var" is a variable referencing a MultiAxisFeedrateSettingsInput object.  

```python
# Get the value of the property.
propertyValue = multiAxisFeedrateSettingsInput_var.dpmType

# Set the value of the property.
multiAxisFeedrateSettingsInput_var.dpmType = propertyValue
```

## Property Value

This is a read/write property whose value is a [MultiAxisDegreesPerMinuteType](MultiAxisDegreesPerMinuteType.md).

## Version

Introduced in version September 2025  

