# TextCommandPalette.setMinimumSize Method

Parent Object: [TextCommandPalette](TextCommandPalette.md)  

## Description

Sets the minimum size of the palette. The user cannot resize it to be smaller than this size. This does not change the current size of the palette unless the palette is already smaller than this size.  

Calling this method and setting the width and height to zero, removes the minimum size restriction.

## Syntax

"textCommandPalette_var" is a variable referencing a [TextCommandPalette](TextCommandPalette.md) object.

```python
returnValue = textCommandPalette_var.setMinimumSize(width, height)
```

## Return Value

| Type    | Description                                             |
|---------|---------------------------------------------------------|
| boolean | Returns true if setting the minimum size was succesful. |

## Parameters

| Name   | Type    | Description                                  |
|--------|---------|----------------------------------------------|
| width  | integer | Specifies the minimum width of the palette.  |
| height | integer | Specifies the minimum height of the palette. |

## Version

Introduced in version August 2017  

