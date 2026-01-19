# GeometricConstraints.addPerpendicularToSurface Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new perpendicular constraint that forces the sketch curve to be perpendicular to the specified surface. Line and spline curves are supported.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addPerpendicularToSurface(curve, surface)
```

## Return Value

| Type | Description |
|----|----|
| [PerpendicularToSurfaceConstraint](PerpendicularToSurfaceConstraint.md) | Returns the newly created PerpendicularToSurfaceConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| curve | [SketchCurve](SketchCurve.md) | The SketchCurve to constrain to the surface. |
| surface | [Base](Base.md) | The BRepFace or ConstructionPlane the line will be perpendicular to. |

## Version

Introduced in version September 2023  

