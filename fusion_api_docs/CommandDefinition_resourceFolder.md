# CommandDefinition.resourceFolder Property

Parent Object: [CommandDefinition](CommandDefinition.md)  

## Description

This argument defines the resource folder that contains the images used for the command icon. Icons can be defined using either PNG or SVG files. More information about icons can be found in the user manual topic [User Interface Customization](UserInterface_UM.htm#IconsForCommands).

## Syntax

"commandDefinition_var" is a variable referencing a CommandDefinition object.  

```python
# Get the value of the property.
propertyValue = commandDefinition_var.resourceFolder

# Set the value of the property.
commandDefinition_var.resourceFolder = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2014  

