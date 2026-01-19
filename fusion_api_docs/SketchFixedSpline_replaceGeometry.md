# SketchFixedSpline.replaceGeometry Method

Parent Object: [SketchFixedSpline](SketchFixedSpline.md)  

## Description

Replaces the underlying NURBS curve that defines the shape of the fixed curve. This can only be used if the isNative property of the SketchFixedSpline returns false.

## Syntax

"sketchFixedSpline_var" is a variable referencing a [SketchFixedSpline](SketchFixedSpline.md) object.

```python
returnValue = sketchFixedSpline_var.replaceGeometry(nurbsCurve)
```

## Return Value

| Type    | Description                                     |
|---------|-------------------------------------------------|
| boolean | Returns true if the replacement was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| nurbsCurve | [NurbsCurve3D](NurbsCurve3D.md) | A NurbsCurve3D object that defines a valid NURBS curve and will be used to replace the existing geometry definition. |

## Version

Introduced in version December 2020  

