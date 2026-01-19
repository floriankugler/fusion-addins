# MultiAxisMachineElement.feedrateSettings Property

Parent Object: [MultiAxisMachineElement](MultiAxisMachineElement.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The multi-axis feedrate settings for this machine. For changes to to this object to take effect, re-assign them to this property. Cannot be set to null.

## Syntax

"multiAxisMachineElement_var" is a variable referencing a MultiAxisMachineElement object.  

```python
# Get the value of the property.
propertyValue = multiAxisMachineElement_var.feedrateSettings

# Set the value of the property.
multiAxisMachineElement_var.feedrateSettings = propertyValue
```

## Property Value

This is a read/write property whose value is a [MultiAxisFeedrateSettings](MultiAxisFeedrateSettings.md).

## Version

Introduced in version September 2025  

