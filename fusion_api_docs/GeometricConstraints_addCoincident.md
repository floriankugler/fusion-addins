# GeometricConstraints.addCoincident Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a new coincident constraint between two entities. The first argument is a sketch point. The second argument is a sketch curve or point.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addCoincident(point, entity)
```

## Return Value

| Type | Description |
|----|----|
| [CoincidentConstraint](CoincidentConstraint.md) | Returns the newly created CoincidentConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| point | [SketchPoint](SketchPoint.md) | The SketchPoint that will be made coincident. |
| entity | [SketchEntity](SketchEntity.md) | The SketchPoint or sketch curve that the point will be made coincident to. |

## Samples

| Name | Description |
|----|----|
| [GeometricConstraints.addCoincident](GeometricConstraints_addCoincident_Sample.md) | Demonstrates the GeometricConstraints.addCoincident method. |

## Version

Introduced in version August 2014  

