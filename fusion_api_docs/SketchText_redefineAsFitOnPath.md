# SketchText.redefineAsFitOnPath Method

Parent Object: [SketchText](SketchText.md)  

## Description

Sets this SketchTextInput to define text that fits along a specified path. Fitting on a path will space the characters so the text fits along the entire length of the path entity.

## Syntax

"sketchText_var" is a variable referencing a [SketchText](SketchText.md) object.

```python
returnValue = sketchText_var.redefineAsFitOnPath(path, isAbovePath)
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

## Version

Introduced in version December 2020  

