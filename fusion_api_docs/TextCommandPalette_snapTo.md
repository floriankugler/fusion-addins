# TextCommandPalette.snapTo Method

Parent Object: [TextCommandPalette](TextCommandPalette.md)  

## Description

Snaps this palette to another palette.

## Syntax

"textCommandPalette_var" is a variable referencing a [TextCommandPalette](TextCommandPalette.md) object.

```python
returnValue = textCommandPalette_var.snapTo(palette, snapOption)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the palette was successfully snapped to the other palette. |

## Parameters

| Name | Type | Description |
|----|----|----|
| palette | [Palette](Palette.md) | Specifies the palette to snap to. |
| snapOption | [PaletteSnapOptions](PaletteSnapOptions.md) | Specifies how this palette should be snapped to the other palette. |

## Version

Introduced in version August 2017  

