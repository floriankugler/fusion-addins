# SketchCircles.addByTwoTangents Method

Parent Object: [SketchCircles](SketchCircles.md)  

## Description

Creates a sketch circle that is tangent to the two input lines. The two lines must lie on the x-y plane of the sketch.

## Syntax

"sketchCircles_var" is a variable referencing a [SketchCircles](SketchCircles.md) object.

```python
returnValue = sketchCircles_var.addByTwoTangents(tangentOne, tangentTwo, radius, hintPoint)
```

## Return Value

| Type | Description |
|----|----|
| [SketchCircle](SketchCircle.md) | Returns the newly created SketchCircle object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| tangentOne | [SketchLine](SketchLine.md) | The first line that the circle will be tangent to. The line must lie on the x-y plane of the sketch. |
| tangentTwo | [SketchLine](SketchLine.md) | The second line that the circle will be tangent to. The line must lie on the x-y plane of the sketch and cannot be parallel to the first line. |
| radius | double | The radius of the circle in centimeters. |
| hintPoint | [Point3D](Point3D.md) | A point that specifies which of the possible four solutions to use when creating the circle. If you consider the two input lines to be infinite they create four quadrants which results in four possible solutions for the creation of the circle. The hint point is a point anywhere within the quadrant where you want the circle created. |

## Samples

| Name | Description |
|----|----|
| [SketchCircles.addByTwoTangents](SketchCircles_addByTwoTangents_Sample.md) | Demonstrates the SketchCircles.addByTwoTangets method. |

## Version

Introduced in version August 2014  

