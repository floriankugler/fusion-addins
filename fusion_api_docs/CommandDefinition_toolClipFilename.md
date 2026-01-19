# CommandDefinition.toolClipFilename Property

Parent Object: [CommandDefinition](CommandDefinition.md)  

## Description

Gets or sets the full filename of the image file (PNG) used for the tool clip. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip along with the tooltip text.

## Syntax

"commandDefinition_var" is a variable referencing a CommandDefinition object.  

```python
# Get the value of the property.
propertyValue = commandDefinition_var.toolClipFilename

# Set the value of the property.
commandDefinition_var.toolClipFilename = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2014  

