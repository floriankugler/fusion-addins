# SketchCircles.addByCenterRadius Method

Parent Object: [SketchCircles](SketchCircles.md)  

## Description

Creates a sketch circle that is always parallel to the x-y plane of the sketch and is centered at the specified point.

## Syntax

"sketchCircles_var" is a variable referencing a [SketchCircles](SketchCircles.md) object.

```python
returnValue = sketchCircles_var.addByCenterRadius(centerPoint, radius)
```

## Return Value

| Type | Description |
|----|----|
| [SketchCircle](SketchCircle.md) | Returns the newly created SketchCircle object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| centerPoint | [Base](Base.md) | The center point of the circle. It can be an existing SketchPoint or a Point3D object. |
| radius | double | The radius of the circle in centimeters. |

## Samples

| Name | Description |
|----|----|
| [Create circle by center and radius API Sample](CircleByCenterRadius_Sample.md) | Demonstrates creating a sketch circle by the center and radius. |
| [GeometricConstraint.addMidPont](GeometricConstraint_addMidPont_Sample.md) | Demonstrate the GeometricConstraint.addMidPont method. |
| [GeometricConstraints.addConcentric](GeometricConstraints_addConcentric_Sample.md) | Demonstrates the GeometricConstraints.addConcentric method. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |
| [SketchCircles.addByCenterRadius](SketchCircles_addByCenterRadius_Sample.md) | Demonstrates the SketchCircles.addByCenterRadius method. |

## Version

Introduced in version August 2014  

