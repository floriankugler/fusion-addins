# GeometricConstraints.addLineOnPlanarSurface Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new constraint that forces the sketch line to lie on a planar surface.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addLineOnPlanarSurface(line, planarSurface)
```

## Return Value

| Type | Description |
|----|----|
| [LineOnPlanarSurfaceConstraint](LineOnPlanarSurfaceConstraint.md) | Returns the newly created LineOnPlanarSurfaceConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| line | [SketchLine](SketchLine.md) | The SketchLine to constrain to the surface. |
| planarSurface | [Base](Base.md) | The planar BRepFace or CosntructionPlane the sketch line will lie on. |

## Version

Introduced in version September 2023  

