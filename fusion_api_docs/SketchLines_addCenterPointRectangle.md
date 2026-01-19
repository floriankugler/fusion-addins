# SketchLines.addCenterPointRectangle Method

Parent Object: [SketchLines](SketchLines.md)  

## Description

Creates four sketch lines representing a rectangle where the first point represents the center of the rectangle. The second point is the corner of the rectangle and can be either an existing SketchPoint or Point3D object. The four sketch lines are returned.

## Syntax

"sketchLines_var" is a variable referencing a [SketchLines](SketchLines.md) object.

```python
returnValue = sketchLines_var.addCenterPointRectangle(centerPoint, cornerPoint)
```

## Return Value

| Type | Description |
|----|----|
| [SketchLineList](SketchLineList.md) | Returns the four new sketch lines or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| centerPoint | [Point3D](Point3D.md) | The center point of the rectangle |
| cornerPoint | [Base](Base.md) | The corner of the rectangle. It can be a SketchPoint or Point3D object. |

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [SketchLines.addCenterPointRectangle](SketchLines_addCenterPointRectangle_Sample.md) | Demonstrates the SketchLines.addCenterPointRectangle method. |

## Version

Introduced in version August 2014  

