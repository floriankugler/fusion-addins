# SketchDimensions.addDistanceDimension Method

Parent Object: [SketchDimensions](SketchDimensions.md)  

## Description

Creates a new linear dimension constraint between the two input entities.

## Syntax

"sketchDimensions_var" is a variable referencing a [SketchDimensions](SketchDimensions.md) object.

```python
# Uses no optional arguments.
returnValue = sketchDimensions_var.addDistanceDimension(pointOne, pointTwo, orientation, textPoint)

# Uses optional arguments.
returnValue = sketchDimensions_var.addDistanceDimension(pointOne, pointTwo, orientation, textPoint, isDriving)
```

## Return Value

| Type | Description |
|----|----|
| [SketchLinearDimension](SketchLinearDimension.md) | Returns the newly created dimension or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| pointOne | [SketchPoint](SketchPoint.md) | The first SketchPoint to dimension to. |
| pointTwo | [SketchPoint](SketchPoint.md) | The second SketchPoint to dimension to.. |
| orientation | [DimensionOrientations](DimensionOrientations.md) | The orientation of the dimension. |
| textPoint | [Point3D](Point3D.md) | A Point3D object that defines the position of the dimension text. |
| isDriving | boolean | Optional argument that specifies if a driving (the dimension controls the geometry) or a driven (the geometry controls the dimension) dimension is created. If not provided a driving dimension will be created. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [SketchDimensions.addDistanceDimension](SketchDimension_addDistanceDimension_Sample.md) | Demonstrates the SketchDimension.addDistanceDimension method. |

## Version

Introduced in version August 2014  

