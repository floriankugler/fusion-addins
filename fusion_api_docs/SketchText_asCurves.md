# SketchText.asCurves Method

Parent Object: [SketchText](SketchText.md)  

## Description

Returns the underlying curves that define the outline of the text. Calling this does not affect the SketchText and does not create any new sketch geometry but returns the geometrical definition of the sketch outline.

## Syntax

"sketchText_var" is a variable referencing a [SketchText](SketchText.md) object.

```python
returnValue = sketchText_var.asCurves()
```

## Return Value

| Type | Description |
|----|----|
| [Curve3D](Curve3D.md)\[\] | Returns an array of transient curves that represent the outline of the text. |

## Version

Introduced in version August 2016  

