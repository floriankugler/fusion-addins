# SketchCircles.addByThreeTangents Method

Parent Object: [SketchCircles](SketchCircles.md)  

## Description

Creates a sketch circle that is tangent to the three input lines. The three lines must lie on the x-y plane of the sketch.

## Syntax

"sketchCircles_var" is a variable referencing a [SketchCircles](SketchCircles.md) object.

```python
returnValue = sketchCircles_var.addByThreeTangents(tangentOne, tangentTwo, tangentThree, hintPoint)
```

## Return Value

| Type | Description |
|----|----|
| [SketchCircle](SketchCircle.md) | Returns the newly created SketchCircle object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| tangentOne | [SketchLine](SketchLine.md) | The first line that the circle will be tangent to. The line must lie on the x-y plane of the sketch and cannot be parallel to the second or third line. |
| tangentTwo | [SketchLine](SketchLine.md) | The second line that the circle will be tangent to. The line must lie on the x-y plane of the sketch and cannot be parallel to the first or third line. |
| tangentThree | [SketchLine](SketchLine.md) | The third line that the circle will be tangent to. The line must lie on the x-y plane of the sketch and cannot be parallel to the first or second line. |
| hintPoint | [Point3D](Point3D.md) | A point that specifies which of the possible multiple solutions to use when creating the circle. If you consider the three input lines to be infinite there are many possible solutions when creating a circle that is tangent to all three lines. The hint point is a point anywhere within the area defined by the three lines where the circle is to be created. |

## Samples

| Name | Description |
|----|----|
| [Create Circle By 3 Tangents API Sample](CreateCcircleBy3Tangents_Sample.md) | Creates three lines and then draws a circle that is tangent to the lines. It then creates tangent constraints to maintain that relationship. |
| [SketchCircles.addByThreeTangents](SketchCircles_addByThreeTangents_Sample.md) | Demonstrates the SketchCircles.addByThreeTangets method. |

## Version

Introduced in version August 2014  

