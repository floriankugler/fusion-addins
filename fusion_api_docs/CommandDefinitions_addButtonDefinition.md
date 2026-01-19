# CommandDefinitions.addButtonDefinition Method

Parent Object: [CommandDefinitions](CommandDefinitions.md)  

## Description

Creates a new command definition that can be used to create a button control and handle the response when the button is clicked.

## Syntax

"commandDefinitions_var" is a variable referencing a [CommandDefinitions](CommandDefinitions.md) object.

```python
# Uses no optional arguments.
returnValue = commandDefinitions_var.addButtonDefinition(id, name, tooltip)

# Uses optional arguments.
returnValue = commandDefinitions_var.addButtonDefinition(id, name, tooltip, resourceFolder)
```

## Return Value

| Type | Description |
|----|----|
| [CommandDefinition](CommandDefinition.md) | Returns the created CommandDefinition object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique identifier for this command definition. It must be unique with respect to all other command definitions and is limited to the following set of characters, [A-Z][a-z][0-9] and _. |
| name | string | The name displayed in the UI for the associated button control. |
| tooltip | string | The full description of the command as seen in the extended tooltip in the user interface. Using the returned CommandDefinition you can also optionally set the toolClipFilename property to show an image the extended tooltip. The width of all tooltips is limited to 300 pixels. Word wrapping is enabled, so Fusion will automatically break the line and flow your text to the next line. However, if you include a long word that exceeds 300 pixels, it doesn't wrap and the right portion will be clipped. This is common when displaying paths or URL's. If a single word is longer than 300 pixels there are a couple of options to avoid the clipping. The first option is to insert one or more zero width space characters within the word to define where the word should be broken. The UNICODE character '\u200b' defines a zero width space. This is not displayed is only used to designate a possible break point. The second option is to shorten the word by removing a section. For example, if the word is a full path to a file and a portion of the path is common you can remove that portion and replace it with the ellipsis character to indicate there is some missing text. There is a single UNICODE character you can use the ellipsis. It is '\u2026'. |
| resourceFolder | string | This argument defines the resource folder that contains the images used for the icon. Icons can be defined using either PNG or SVG files. More information about icons can be found in the user manual topic [User Interface Customization](UserInterface_UM.htm#IconsForCommands). This is an optional argument and if not provided a default icon will be used. This is an optional argument whose default value is "". |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2014  

