# CommandDefinition.tooltip Property

Parent Object: [CommandDefinition](CommandDefinition.md)  

## Description

Gets or sets the tooltip string. This is always shown for commands. If the tooltip description and/or tool clip are also specified then the tooltip will progressively display more information as the user hovers the mouse over the control.  

The width of all tooltips is limited to 300 pixels. Word wrapping is enabled, so Fusion will automatically break the line and flow your text to the next line. However, if you include a long word that exceeds 300 pixels, it doesn't wrap and the right portion will be clipped. This is common when displaying paths or URL's. If a single word is longer than 300 pixels there are a couple of options to avoid the clipping.  

The first option is to insert one or more zero width space characters within the word to define where the word should be broken. The UNICODE character '\u200b' defines a zero width space. This is not displayed is only used to designate a possible break point.  

The second option is to shorten the word by removing a section. For example, if the word is a full path to a file and a portion of the path is common you can remove that portion and replace it with the ellipsis character to indicate there is some missing text. There is a single UNICODE character you can use the ellipsis. It is '\u2026'.

## Syntax

"commandDefinition_var" is a variable referencing a CommandDefinition object.  

```python
# Get the value of the property.
propertyValue = commandDefinition_var.tooltip

# Set the value of the property.
commandDefinition_var.tooltip = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2014  

