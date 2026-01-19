# MultiAxisCombinationDPMFeedrateSettings.pulseWeight Property

Parent Object: [MultiAxisCombinationDPMFeedrateSettings](MultiAxisCombinationDPMFeedrateSettings.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The pulse weight ratio for the rotary axes when DPM feedrates are output as a combination of linear and rotary movements. The pulse weight is a scale factor based on the rotary axes accuracy compared to the linear axes accuracy. For example, it should be set to .1 when the linear axes are output on .0001 increments and the rotary axes on .001 increments.

## Syntax

"multiAxisCombinationDPMFeedrateSettings_var" is a variable referencing a MultiAxisCombinationDPMFeedrateSettings object.  

```python
# Get the value of the property.
propertyValue = multiAxisCombinationDPMFeedrateSettings_var.pulseWeight

# Set the value of the property.
multiAxisCombinationDPMFeedrateSettings_var.pulseWeight = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version September 2025  

