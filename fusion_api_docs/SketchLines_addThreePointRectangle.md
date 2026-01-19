# SketchLines.addThreePointRectangle Method

Parent Object: [SketchLines](SketchLines.md)  

## Description

Creates four sketch lines representing a rectangle where the first two points are the base corners of the rectangle and the third point defines the height.

## Syntax

"sketchLines_var" is a variable referencing a [SketchLines](SketchLines.md) object.

```python
returnValue = sketchLines_var.addThreePointRectangle(pointOne, pointTwo, pointThree)
```

## Return Value

| Type | Description |
|----|----|
| [SketchLineList](SketchLineList.md) | Returns the four new sketch lines or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointOne | [Base](Base.md) | The first corner of the rectangle. It can be a SketchPoint or Point3D object. |
| pointTwo | [Base](Base.md) | The first corner of the rectangle. It can be a SketchPoint or Point3D object. |
| pointThree | [Point3D](Point3D.md) | The first corner of the rectangle. a Point3D object defining the height of the rectangle. |

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [SketchLines.addThreePointRectangle](SketchLines_addThreePointRectangle_Sample.md) | Demonstrates the SketchLines.addThreePointRectangle method. |

## Version

Introduced in version August 2014  

