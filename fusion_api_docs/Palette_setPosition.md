# Palette.setPosition Method

Parent Object: [Palette](Palette.md)  

## Description

Sets the position of the palette. If the palette is docked or snapped, this will result in changing it to be floating.

## Syntax

"palette_var" is a variable referencing a [Palette](Palette.md) object.

```python
returnValue = palette_var.setPosition(left, top)
```

## Return Value

| Type    | Description                                          |
|---------|------------------------------------------------------|
| boolean | Returns true if setting the position was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| left | integer | The position of the left side of the palette relative to screen space and in pixels. Because palettes can be positioned outside of the Fusion window, a value of zero indicates the left side of the screen and not the Fusion window. |
| top | integer | The position of the top of the palette relative to screen space and in pixels. Because palettes can be positioned outside of the Fusion window, a value of zero indicates the top of the screen and not the Fusion window. |

## Version

Introduced in version March 2017  

