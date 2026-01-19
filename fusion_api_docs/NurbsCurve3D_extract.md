# NurbsCurve3D.extract Method

Parent Object: [NurbsCurve3D](NurbsCurve3D.md)  

## Description

Defines a new NURBS curve that is the subset of this NURBS curve in the parameter range of \[startParam, endParam\]

## Syntax

"nurbsCurve3D_var" is a variable referencing a [NurbsCurve3D](NurbsCurve3D.md) object.

```python
returnValue = nurbsCurve3D_var.extract(startParam, endParam)
```

## Return Value

| Type                             | Description                        |
|----------------------------------|------------------------------------|
| [NurbsCurve3D](NurbsCurve3D.md) | Returns a new NurbsCurve3D object. |

## Parameters

| Name | Type | Description |
|----|----|----|
| startParam | double | The parameter position that defines the start of the subset. |
| endParam | double | The parameter position that defines the end of the subset. |

## Version

Introduced in version August 2014  

