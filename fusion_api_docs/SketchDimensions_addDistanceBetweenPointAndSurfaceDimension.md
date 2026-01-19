# SketchDimensions.addDistanceBetweenPointAndSurfaceDimension Method

Parent Object: [SketchDimensions](SketchDimensions.md)  

## Description

Creates a new linear dimension controlling the distance between a sketch point and the specified surface or point. The text position is automatically chosen and is positioned so it is midway between the point and surface and the extension lines are a minimum length. You can modify the position by using functionality on the returned SketchDistanceBetweenPointAndSurfaceDimension object.

## Syntax

"sketchDimensions_var" is a variable referencing a [SketchDimensions](SketchDimensions.md) object.

```python
# Uses no optional arguments.
returnValue = sketchDimensions_var.addDistanceBetweenPointAndSurfaceDimension(point, surface)

# Uses optional arguments.
returnValue = sketchDimensions_var.addDistanceBetweenPointAndSurfaceDimension(point, surface, isDriving)
```

## Return Value

| Type | Description |
|----|----|
| [SketchDistanceBetweenPointAndSurfaceDimension](SketchDistanceBetweenPointAndSurfaceDimension.md) | Returns the newly created dimension or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| point | [SketchPoint](SketchPoint.md) | The SketchPoint being constrained by the dimension. |
| surface | [Base](Base.md) | The BRepFace or ConstructionPlane to which the dimension will anchor. Planar, cylindrical, spherical and conical faces are supported. If a cylindrical, spherical or conical face is used, the dimension is from the point to the nearest point on the surface. |
| isDriving | boolean | Optional argument that specifies if a driving (the dimension controls the geometry) or a driven (the geometry controls the dimension) dimension is created. If not provided a driving dimension will be created. This is an optional argument whose default value is True. |

## Version

Introduced in version September 2023  

