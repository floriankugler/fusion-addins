# TextCommandPalette.writeText Method

Parent Object: [TextCommandPalette](TextCommandPalette.md)  

## Description

Write the specified text to the TEXT COMMAND window.

## Remarks

Below is some sample code that illustrates making sure the palette is visible and writing some text to it.

```python
# Get the palette that represents the TEXT COMMANDS window.
textPalette = ui.palettes.itemById('TextCommands')

# Make sure the palette is visible.
if not textPalette.isVisible:
  textPalette.isVisible = True

# Write some text.
textPalette.writeText('This is a text message.') 
```

## Syntax

"textCommandPalette_var" is a variable referencing a [TextCommandPalette](TextCommandPalette.md) object.

```python
returnValue = textCommandPalette_var.writeText(text)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type   | Description                                   |
|------|--------|-----------------------------------------------|
| text | string | The text to write to the Text Command window. |

## Version

Introduced in version August 2017  

