# SketchLines.addByTwoPoints Method

Parent Object: [SketchLines](SketchLines.md)  

## Description

Creates a sketch line between the two input points. The input points can be either existing SketchPoints or Point3D objects. If a SketchPoint is used the new line will be based on that sketch point and update if the sketch point is modified.

## Syntax

"sketchLines_var" is a variable referencing a [SketchLines](SketchLines.md) object.

```python
returnValue = sketchLines_var.addByTwoPoints(startPoint, endPoint)
```

## Return Value

| Type | Description |
|----|----|
| [SketchLine](SketchLine.md) | Returns the newly created SketchLine object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| startPoint | [Base](Base.md) | The start point of the line. It can be a SketchPoint or Point3D object. |
| endPoint | [Base](Base.md) | The end point of the line. It can be a SketchPoint or Point3D object. |

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |
| [SketchArcs.addFillet](SketchArcs_addFillet_Sample.md) | Demonstrates the SketchArcs.addFillet method. |
| [SketchCircles.addByThreeTangents](SketchCircles_addByThreeTangents_Sample.md) | Demonstrates the SketchCircles.addByThreeTangets method. |
| [SketchCircles.addByTwoTangents](SketchCircles_addByTwoTangents_Sample.md) | Demonstrates the SketchCircles.addByTwoTangets method. |
| [SketchLines.addAngleChamfer](SketchLines_addAngleChamfer_Sample.md) | Demonstrates the SketchLines.addAngleChamfer method. |
| [SketchLines.addByTwoPoints](SketchLines_addByTwoPoints_Sample.md) | Demonstrates the SketchLines.addByTwoPoints method. |
| [SketchLines.addDistanceChamfer](SketchLines_addDistanceChamfer_Sample.md) | Demonstrates the SketchLines.addDistanceChamfer method. |

## Version

Introduced in version August 2014  

