# GeometricConstraints.addSymmetry Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new symmetry constraint.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addSymmetry(entityOne, entityTwo, symmetryLine)
```

## Return Value

| Type | Description |
|----|----|
| [SymmetryConstraint](SymmetryConstraint.md) | Returns the newly created SymmetryConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entityOne | [SketchEntity](SketchEntity.md) | The first sketch entity to be symmetric. |
| entityTwo | [SketchEntity](SketchEntity.md) | The second sketch entity to be symmetric. It must be the same type as the first entity. |
| symmetryLine | [SketchLine](SketchLine.md) | The SketchLine that defines the axis of symmetry. |

## Samples

| Name | Description |
|----|----|
| [GeometricConstraints.addSymmetry](GeometricConstraints_addSymmetry_Sample.md) | Demonstrates the GeometricConstraints.addSymmetry method. |

## Version

Introduced in version August 2014  

