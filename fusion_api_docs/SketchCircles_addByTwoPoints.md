# SketchCircles.addByTwoPoints Method

Parent Object: [SketchCircles](SketchCircles.md)  

## Description

Creates a sketch circle where the circle passes through the two points and the distance between the two points is the diameter of the circle.

## Syntax

"sketchCircles_var" is a variable referencing a [SketchCircles](SketchCircles.md) object.

```python
returnValue = sketchCircles_var.addByTwoPoints(pointOne, pointTwo)
```

## Return Value

| Type | Description |
|----|----|
| [SketchCircle](SketchCircle.md) | Returns the newly created SketchCircle object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointOne | [Point3D](Point3D.md) | A Point3D object that defines a point is sketch space and lies on the x-y plane of the sketch. |
| pointTwo | [Point3D](Point3D.md) | A Point3D object that defines a point is sketch space and lies on the x-y plane of the sketch. |

## Samples

| Name | Description |
|----|----|
| [SketchCircles.addByTwoPoints](SketchCircles_addByTwoPoints_Sample.md) | Demonstrates the SketchCircles.addByTwoPoints method. |
| [SketchDimensions.addConcentricCicleDimension](SketchDimension_addConcentricCircleDimension_Sample.md) | Demonstrates the SketchDimension.addConcentricCircleDimension method. |
| [SketchDimensions.addDiameterDimension](SketchDimension_addDiameterDimension_Sample.md) | Demonstrates the SketchDimension.addDiameterDimension method. |

## Version

Introduced in version August 2014  

