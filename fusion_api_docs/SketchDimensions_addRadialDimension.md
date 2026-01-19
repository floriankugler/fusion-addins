# SketchDimensions.addRadialDimension Method

Parent Object: [SketchDimensions](SketchDimensions.md)  

## Description

Creates a new radial dimension constraint on the arc or circle.

## Syntax

"sketchDimensions_var" is a variable referencing a [SketchDimensions](SketchDimensions.md) object.

```python
# Uses no optional arguments.
returnValue = sketchDimensions_var.addRadialDimension(entity, textPoint)

# Uses optional arguments.
returnValue = sketchDimensions_var.addRadialDimension(entity, textPoint, isDriving)
```

## Return Value

| Type | Description |
|----|----|
| [SketchRadialDimension](SketchRadialDimension.md) | Returns the newly created dimension or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| entity | [SketchCurve](SketchCurve.md) | The SketchCircle or SketchArc to dimension. |
| textPoint | [Point3D](Point3D.md) | A Point3D object that defines the position of the dimension text. |
| isDriving | boolean | Optional argument that specifies if a driving (the dimension controls the geometry) or a driven (the geometry controls the dimension) dimension is created. If not provided a driving dimension will be created. This is an optional argument whose default value is True. |

## Version

Introduced in version August 2014  

