# SketchPoint.move Method

Parent Object: [SketchPoint](SketchPoint.md)  

## Description

Moves the sketch geometry using the specified transform. Move respects any constraints that would normally prohibit the move. This will fail in the case where the IsReference property is true.

## Syntax

"sketchPoint_var" is a variable referencing a [SketchPoint](SketchPoint.md) object.

```python
returnValue = sketchPoint_var.move(translation)
```

## Return Value

| Type    | Description                                             |
|---------|---------------------------------------------------------|
| boolean | Returns true if moving the sketch point was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| translation | [Vector3D](Vector3D.md) | The vector that defines the distance and direction to move. |

## Samples

| Name | Description |
|----|----|
| [Sketch Point API Sample](SketchPointSample_Sample.md) | Demonstrates creating a new sketch point. |

## Version

Introduced in version August 2014  

