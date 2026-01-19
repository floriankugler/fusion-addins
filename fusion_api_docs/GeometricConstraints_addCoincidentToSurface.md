# GeometricConstraints.addCoincidentToSurface Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new coincident constraint between the sketch point and surface. This forces the point to lie on the surface.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addCoincidentToSurface(point, surface)
```

## Return Value

| Type | Description |
|----|----|
| [CoincidentToSurfaceConstraint](CoincidentToSurfaceConstraint.md) | Returns the newly created CoincidentToSurfaceConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| point | [SketchPoint](SketchPoint.md) | The SketchPoint to constrain to the surface. |
| surface | [Base](Base.md) | The BRepFace or ConstructionPlane the point will be coincident to. |

## Version

Introduced in version September 2023  

