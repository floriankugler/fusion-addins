# Palette.snapTo Method

Parent Object: [Palette](Palette.md)  

## Description

Snaps this palette to another palette.

## Syntax

"palette_var" is a variable referencing a [Palette](Palette.md) object.

```python
returnValue = palette_var.snapTo(palette, snapOption)
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

Introduced in version March 2017  

