# MultiAxisDPMFeedrateSettings.outputTolerance Property

Parent Object: [MultiAxisDPMFeedrateSettings](MultiAxisDPMFeedrateSettings.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The tolerance for deciding whether to output a feedrate value or not. It helps to minimize the output of multi-axis feedrate numbers. If the feedrate value is within this tolerance of the previous feedrate value, then it is set to the previous value. Value is in deg/min.

## Syntax

"multiAxisDPMFeedrateSettings_var" is a variable referencing a MultiAxisDPMFeedrateSettings object.  

```python
# Get the value of the property.
propertyValue = multiAxisDPMFeedrateSettings_var.outputTolerance

# Set the value of the property.
multiAxisDPMFeedrateSettings_var.outputTolerance = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version September 2025  

