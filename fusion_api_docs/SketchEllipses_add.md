# SketchEllipses.add Method

Parent Object: [SketchEllipses](SketchEllipses.md)  

## Description

Creates a sketch ellipse using the center point, a point defining the major axis and a third point anywhere along the ellipse. The created ellipse is parallel to the x-y plane of the sketch.

## Syntax

"sketchEllipses_var" is a variable referencing a [SketchEllipses](SketchEllipses.md) object.

```python
returnValue = sketchEllipses_var.add(centerPoint, majorAxisPoint, point)
```

## Return Value

| Type | Description |
|----|----|
| [SketchEllipse](SketchEllipse.md) | Returns the newly created SketchEllipse object if the creation was successful or null if it failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| centerPoint | [Base](Base.md) | The center point of the ellipse. This can be either an existing SketchPoint or a Point3D object. |
| majorAxisPoint | [Point3D](Point3D.md) | A point3D object that defines both the major axis direction and major axis radius. |
| point | [Point3D](Point3D.md) | A point3D object that the ellipse will pass through. |

## Samples

| Name | Description |
|----|----|
| [SketchDimensions.AddEllipseMajorRadiusDimension](SketchDimension_addEllipseMajorRadiusDimension_Sample.md) | Demonstrates the SketchDimension.addEllipseMajorRadiusDimension method. |
| [SketchDimensions.AddEllipseMinorRadiusDimension](SketchDimension_addEllipseMinorRadiusDimension_Sample.md) | Demonstrates the SketchDimension.addEllipseMinorRadiusDimension method. |
| [SketchEllipses.add](SketchEllipses_add_Sample.md) | Demonstrates the SketchEllipses.add method. |

## Version

Introduced in version August 2014  

