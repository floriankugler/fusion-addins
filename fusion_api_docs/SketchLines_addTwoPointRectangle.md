# SketchLines.addTwoPointRectangle Method

Parent Object: [SketchLines](SketchLines.md)  

## Description

Creates four sketch lines representing a rectangle where the two points are the opposing corners of the rectangle. The input points can be either existing SketchPoints or Point3D objects. If a SketchPoint is used the new lines will be based on that sketch point and update if the sketch point is modified.

## Syntax

"sketchLines_var" is a variable referencing a [SketchLines](SketchLines.md) object.

```python
returnValue = sketchLines_var.addTwoPointRectangle(pointOne, pointTwo)
```

## Return Value

| Type | Description |
|----|----|
| [SketchLineList](SketchLineList.md) | Returns the four new sketch lines or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointOne | [Base](Base.md) | The first corner of the rectangle. It can be a SketchPoint or Point3D object. |
| pointTwo | [Base](Base.md) | The second corner of the rectangle. It can be a SketchPoint or Point3D object. |

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [Sketch Chamfer API Sample](SketchChamferSample_Sample.md) | Demonstrates creating a new sketch point. |
| [SketchLines.addTwoPointRectangle](SketchLines_addTwoPointRectangle_Sample.md) | Demonstrates the SketchLines.addTwoPointRectangle method. |

## Version

Introduced in version August 2014  

