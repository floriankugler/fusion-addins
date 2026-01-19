# CommandControl.isPromoted Property

Parent Object: [CommandControl](CommandControl.md)  

## Description

Gets or sets if this command has been promoted to the parent panel. This property is ignored in the case where this control isn't in a panel.  

The promote method provides more options over how the control is promoted.

## Syntax

"commandControl_var" is a variable referencing a CommandControl object.  

```python
# Get the value of the property.
propertyValue = commandControl_var.isPromoted

# Set the value of the property.
commandControl_var.isPromoted = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2014  

