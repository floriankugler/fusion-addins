# SketchTextInput.setAsAlongPath Method

Parent Object: [SketchTextInput](SketchTextInput.md)  

## Description

Sets this SketchTextInput to define text that follows along a specified path.

## Syntax

"sketchTextInput_var" is a variable referencing a [SketchTextInput](SketchTextInput.md) object.

```python
returnValue = sketchTextInput_var.setAsAlongPath(path, isAbovePath, horizontalAlignment, characterSpacing)
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
| characterSpacing | double | The percentage change in default spacing between characters. |

## Samples

| Name | Description |
|----|----|
| [SketchTextInput.setAsAlongPath](SketchTextinput_setAsAlongPath_Sample.md) | Demonstrates the SketchTextInput.setAsAlongPath method. |
| [Sketch Text API Sample](SketchTextSample_Sample.md) | Demonstrates creating sketch text by creating both mult-line text and text along a curve. |

## Version

Introduced in version December 2020  

