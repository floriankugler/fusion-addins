# MultiAxisMachineElement.createFeedrateSettings Method

Parent Object: [MultiAxisMachineElement](MultiAxisMachineElement.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a MultiAxisFeedrateSettings specialized object from the given input.

## Syntax

"multiAxisMachineElement_var" is a variable referencing a [MultiAxisMachineElement](MultiAxisMachineElement.md) object.

```python
returnValue = multiAxisMachineElement_var.createFeedrateSettings(input)
```

## Return Value

| Type | Description |
|----|----|
| [MultiAxisFeedrateSettings](MultiAxisFeedrateSettings.md) | The specialized MultiAxisFeedrateSettings object created from the input. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [MultiAxisFeedrateSettingsInput](MultiAxisFeedrateSettingsInput.md) | The input object containing the settings to create the MultiAxisFeedrateSettings object. Set this object on the feedrateSettings property to apply the changes. |

## Version

Introduced in version September 2025  

