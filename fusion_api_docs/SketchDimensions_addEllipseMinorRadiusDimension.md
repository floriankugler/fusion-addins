# SketchDimensions.addEllipseMinorRadiusDimension Method

Parent Object: [SketchDimensions](SketchDimensions.md)  

## Description

Creates a new dimension constraint on the minor radius of an ellipse.

## Syntax

"sketchDimensions_var" is a variable referencing a [SketchDimensions](SketchDimensions.md) object.

```python
# Uses no optional arguments.
returnValue = sketchDimensions_var.addEllipseMinorRadiusDimension(ellipse, textPoint)

# Uses optional arguments.
returnValue = sketchDimensions_var.addEllipseMinorRadiusDimension(ellipse, textPoint, isDriving)
```

## Return Value

| Type | Description |
|----|----|
| [SketchEllipseMinorRadiusDimension](SketchEllipseMinorRadiusDimension.md) | Returns the newly created dimension or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| ellipse | [SketchCurve](SketchCurve.md) | The SketchEllipse to dimension. |
| textPoint | [Point3D](Point3D.md) | A Point3D object that defines the position of the dimension text. |
| isDriving | boolean | Optional argument that specifies if a driving (the dimension controls the geometry) or a driven (the geometry controls the dimension) dimension is created. If not provided a driving dimension will be created. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
|----|----|
| [SketchDimensions.AddEllipseMinorRadiusDimension](SketchDimension_addEllipseMinorRadiusDimension_Sample.md) | Demonstrates the SketchDimension.addEllipseMinorRadiusDimension method. |

## Version

Introduced in version August 2014  

