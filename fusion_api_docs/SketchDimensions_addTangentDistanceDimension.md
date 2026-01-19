# SketchDimensions.addTangentDistanceDimension Method

Parent Object: [SketchDimensions](SketchDimensions.md)  

## Description

Creates a new linear dimension from between a line and circle or arc and a second circle or arc where the dimension is to the tangent on the edge of the circle or arc.

## Syntax

"sketchDimensions_var" is a variable referencing a [SketchDimensions](SketchDimensions.md) object.

```python
# Uses no optional arguments.
returnValue = sketchDimensions_var.addTangentDistanceDimension(entityOne, isCloseToEnityTwo, entityTwo, isCloseToEnityOne, textPoint)

# Uses optional arguments.
returnValue = sketchDimensions_var.addTangentDistanceDimension(entityOne, isCloseToEnityTwo, entityTwo, isCloseToEnityOne, textPoint, isDriving)
```

## Return Value

| Type | Description |
|----|----|
| [SketchTangentDistanceDimension](SketchTangentDistanceDimension.md) | Returns the newly created dimension or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| entityOne | [SketchEntity](SketchEntity.md) | The first entity to dimension to. This can be a SketchPoint, SketchLine, SketchCircle or SketchArc. If a circle or arc is provided then the tangentSideOne argument must be specified. |
| isCloseToEnityTwo | boolean | If entityOne is a circle or arc this specifies which side of the circle or arc the dimension will be tangent to. If true, it will be on the side that is closer to entityTwo. If a SketchLine or SketchPoint was input for the entityOne argument this argument is ignored and any value can be used. |
| entityTwo | [SketchCurve](SketchCurve.md) | A SketchCircle or SketchArc entity that you will dimension to. |
| isCloseToEnityOne | boolean | Specifies which side of the circle or arc input as the entityTwo argument the dimension will be tangent to. If true, it will be on the side that is closer to entityOne. |
| textPoint | [Point3D](Point3D.md) | A Point3D object that defines the position of the dimension text. |
| isDriving | boolean | Optional argument that specifies if a driving (the dimension controls the geometry) or a driven (the geometry controls the dimension) dimension is created. If not provided a driving dimension will be created. This is an optional argument whose default value is True. |

## Version

Introduced in version July 2022  

