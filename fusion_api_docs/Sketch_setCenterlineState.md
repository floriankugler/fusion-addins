# Sketch.setCenterlineState Method

Parent Object: [Sketch](Sketch.md)  

## Description

Method that sets the Centerline state for an array of sketch lines.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.setCenterlineState(sketchLines, centerlineState)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sketchLines | SketchLine\[\] | An array of sketch lines to set the centerline status |
| centerlineState | [SketchLineCenterlineStates](SketchLineCenterlineStates.md) | Input enum value that specifies if the centerline state of the input lines should be toggled, set to centerline, or set to normal |

## Version

Introduced in version March 2024  

