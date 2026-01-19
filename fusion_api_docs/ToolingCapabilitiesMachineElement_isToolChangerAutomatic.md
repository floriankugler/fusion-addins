# ToolingCapabilitiesMachineElement.isToolChangerAutomatic Property

Parent Object: [ToolingCapabilitiesMachineElement](ToolingCapabilitiesMachineElement.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

If your machine has an automatic tool changer, set this to true. For machines with manual tool change capabilities, set this to false.

## Syntax

"toolingCapabilitiesMachineElement_var" is a variable referencing a ToolingCapabilitiesMachineElement object.  

```python
# Get the value of the property.
propertyValue = toolingCapabilitiesMachineElement_var.isToolChangerAutomatic

# Set the value of the property.
toolingCapabilitiesMachineElement_var.isToolChangerAutomatic = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2025  

