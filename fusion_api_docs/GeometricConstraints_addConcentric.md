# GeometricConstraints.addConcentric Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new concentric constraint between two circles, arcs, ellipses, or elliptical arcs.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addConcentric(entityOne, entityTwo)
```

## Return Value

| Type | Description |
|----|----|
| [ConcentricConstraint](ConcentricConstraint.md) | Returns the newly created ConcentricConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entityOne | [SketchCurve](SketchCurve.md) | The first circle, arc, ellipse or elliptical arc. |
| entityTwo | [SketchCurve](SketchCurve.md) | The second circle, arc, ellipse or elliptical arc. |

## Samples

| Name | Description |
|----|----|
| [GeometricConstraints.addConcentric](GeometricConstraints_addConcentric_Sample.md) | Demonstrates the GeometricConstraints.addConcentric method. |

## Version

Introduced in version August 2014  

