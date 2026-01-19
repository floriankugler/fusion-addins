# SketchText.redefineAsAlongPath Method

Parent Object: [SketchText](SketchText.md)  

## Description

Sets this SketchTextInput to define text that follows along a specified path.

## Syntax

"sketchText_var" is a variable referencing a [SketchText](SketchText.md) object.

```python
returnValue = sketchText_var.redefineAsAlongPath(path, isAbovePath, horizontalAlignment, characterSpacing)
```

## Return Value

| Type    | Description                                                |
|---------|------------------------------------------------------------|
| boolean | Returns true if the setting the definition was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| path | [Base](Base.md) | The entity that defines the path for the text. This can be a SketchCurve or BRepEdge object. |
| isAbovePath | boolean | Indicates if the text should be positioned above or below the path entity. |
| horizontalAlignment | [HorizontalAlignments](HorizontalAlignments.md) | Specifies the horizontal alignment of the text with respect to the path curve. |
| characterSpacing | double | The spacing between the characters. This is an additional spacing to apply that is defined as a percentage of the default spacing. A spacing of 0 indicates no additional spacing. A spacing of 50 indicates to use the default plus 50% of the default. |

## Version

Introduced in version December 2020  

