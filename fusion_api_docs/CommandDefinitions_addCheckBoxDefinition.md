# CommandDefinitions.addCheckBoxDefinition Method

Parent Object: [CommandDefinitions](CommandDefinitions.md)  

## Description

Creates a new command definition that can be used to create a single check box control and handle the response when the check box is clicked.

## Syntax

"commandDefinitions_var" is a variable referencing a [CommandDefinitions](CommandDefinitions.md) object.

```python
returnValue = commandDefinitions_var.addCheckBoxDefinition(id, name, tooltip, isChecked)
```

## Return Value

| Type | Description |
|----|----|
| [CommandDefinition](CommandDefinition.md) | Returns the created CommandDefinition object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique identifier for this command definition. It must be unique with respect to all other command definitions and is limited to the following set of characters, [A-Z][a-z][0-9] and _. |
| name | string | The name displayed in the UI for the associated check box control. |
| tooltip | string | The full description of the command as seen in the extended tooltip in the user interface. Using the returned CommandDefinition you can also optionally set the toolClipFilename property to show an image the extended tooltip. The width of all tooltips is limited to 300 pixels. Word wrapping is enabled, so Fusion will automatically break the line and flow your text to the next line. However, if you include a long word that exceeds 300 pixels, it doesn't wrap and the right portion will be clipped. This is common when displaying paths or URL's. If a single word is longer than 300 pixels there are a couple of options to avoid the clipping. The first option is to insert one or more zero width space characters within the word to define where the word should be broken. The UNICODE character '\u200b' defines a zero width space. This is not displayed is only used to designate a possible break point. The second option is to shorten the word by removing a section. For example, if the word is a full path to a file and a portion of the path is common you can remove that portion and replace it with the ellipsis character to indicate there is some missing text. There is a single UNICODE character you can use the ellipsis. It is '\u2026'. |
| isChecked | boolean | Indicates if the initial state of the check box. |

## Version

Introduced in version August 2014  

