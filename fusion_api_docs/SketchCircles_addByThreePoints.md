# SketchCircles.addByThreePoints Method

Parent Object: [SketchCircles](SketchCircles.md)  

## Description

Creates a sketch circle that passes through the three points. The three points must lie on the x-y plane of the sketch.

## Syntax

"sketchCircles_var" is a variable referencing a [SketchCircles](SketchCircles.md) object.

```python
returnValue = sketchCircles_var.addByThreePoints(pointOne, pointTwo, pointThree)
```

## Return Value

| Type | Description |
|----|----|
| [SketchCircle](SketchCircle.md) | Returns the newly created SketchCircle object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointOne | [Point3D](Point3D.md) | The first point that the circle will pass through. The z component must be zero. |
| pointTwo | [Point3D](Point3D.md) | The second point that the circle will pass through. The z component must be zero. |
| pointThree | [Point3D](Point3D.md) | The third point that the circle will pass through. The z component must be zero. |

## Samples

| Name | Description |
|----|----|
| [SketchCircles.addByThreePoints](SketchCircles_addByThreePoints_Sample.md) | Demonstrates the SketchCircles.addByThreePoints method. |

## Version

Introduced in version August 2014  

