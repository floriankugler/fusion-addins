# SketchConicCurves.add Method

Parent Object: [SketchConicCurves](SketchConicCurves.md)  

## Description

Creates a new conic curve.

## Syntax

"sketchConicCurves_var" is a variable referencing a [SketchConicCurves](SketchConicCurves.md) object.

```python
returnValue = sketchConicCurves_var.add(startPoint, endPoint, apexPoint, rhoValue)
```

## Return Value

| Type | Description |
|----|----|
| [SketchConicCurve](SketchConicCurve.md) | Returns the new conic curve or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| startPoint | [Base](Base.md) | The start point of the conic curve. This can be either an existing SketchPoint or a Point3D object. |
| endPoint | [Base](Base.md) | The end point of the conic curve. This can be either an existing SketchPoint or a Point3D object. |
| apexPoint | [Base](Base.md) | The apex point of the conic curve. This can be either an existing SketchPoint or a Point3D object. |
| rhoValue | double | Double that specifies the rho value for the conic. This value must be greater than zero and less than one. |

## Version

Introduced in version May 2022  

