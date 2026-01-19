# TextCommandPalette.setMaximumSize Method

Parent Object: [TextCommandPalette](TextCommandPalette.md)  

## Description

Sets the maximum size of the palette. The user cannot resize it to be larger than this size. This does not change the current size of the palette unless the palette is already larger than this size.  

Calling this method and setting the width and height to zero, removes the maximum size restriction.

## Syntax

"textCommandPalette_var" is a variable referencing a [TextCommandPalette](TextCommandPalette.md) object.

```python
returnValue = textCommandPalette_var.setMaximumSize(width, height)
```

## Return Value

| Type    | Description                                             |
|---------|---------------------------------------------------------|
| boolean | Returns true if setting the maximum size was succesful. |

## Parameters

| Name   | Type    | Description                                  |
|--------|---------|----------------------------------------------|
| width  | integer | Specifies the maximum width of the palette.  |
| height | integer | Specifies the maximum height of the palette. |

## Version

Introduced in version August 2017  

