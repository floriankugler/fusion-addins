# SketchDimensions.addLinearDiameterDimension Method

Parent Object: [SketchDimensions](SketchDimensions.md)  

## Description

Creates a new linear dimension showing the diameter where the first line acts as the center line and the second entity defines the size. The first input entity must be a sketch line. The second entity can be a point or a line that is parallel to the first. The dimension controls the distance as measured perpendicular to the first input line.

## Syntax

"sketchDimensions_var" is a variable referencing a [SketchDimensions](SketchDimensions.md) object.

```python
# Uses no optional arguments.
returnValue = sketchDimensions_var.addLinearDiameterDimension(centerLine, entityTwo, textPoint)

# Uses optional arguments.
returnValue = sketchDimensions_var.addLinearDiameterDimension(centerLine, entityTwo, textPoint, isDriving)
```

## Return Value

| Type | Description |
|----|----|
| [SketchLinearDiameterDimension](SketchLinearDiameterDimension.md) | Returns the newly created dimension or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| centerLine | [SketchLine](SketchLine.md) | The SketchLine to dimension to which acts as the center line. |
| entityTwo | [SketchEntity](SketchEntity.md) | The parallel SketchLine or SketchPoint to dimension to. If a SketchLine is used it must be parallel to the first line. |
| textPoint | [Point3D](Point3D.md) | A Point3D object that defines the position of the dimension text. |
| isDriving | boolean | Optional argument that specifies if a driving (the dimension controls the geometry) or a driven (the geometry controls the dimension) dimension is created. If not provided a driving dimension will be created. This is an optional argument whose default value is True. |

## Version

Introduced in version September 2022  

