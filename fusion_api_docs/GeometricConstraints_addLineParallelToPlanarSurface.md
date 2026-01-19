# GeometricConstraints.addLineParallelToPlanarSurface Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new parallel constraint between a sketch line and a planar surface that will constrain the line to lie on a plane parallel to the specified surface.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addLineParallelToPlanarSurface(line, planarSurface)
```

## Return Value

| Type | Description |
|----|----|
| [LineParallelToPlanarSurfaceConstraint](LineParallelToPlanarSurfaceConstraint.md) | Returns the newly created LineParallelToPlanarSurfaceConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| line | [SketchLine](SketchLine.md) | The SketchLine to constrain to the surface. |
| planarSurface | [Base](Base.md) | The planar BRepFace or CosntructionPlane the sketch line will be parallel to. |

## Version

Introduced in version September 2023  

