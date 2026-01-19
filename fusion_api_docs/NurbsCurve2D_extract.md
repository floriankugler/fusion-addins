# NurbsCurve2D.extract Method

Parent Object: [NurbsCurve2D](NurbsCurve2D.md)  

## Description

Defines a new NURBS curve that is the subset of this NURBS curve in the parameter range of \[startParam, endParam\]

## Syntax

"nurbsCurve2D_var" is a variable referencing a [NurbsCurve2D](NurbsCurve2D.md) object.

```python
returnValue = nurbsCurve2D_var.extract(startParam, endParam)
```

## Return Value

| Type                             | Description                        |
|----------------------------------|------------------------------------|
| [NurbsCurve2D](NurbsCurve2D.md) | Returns a new NurbsCurve2D object. |

## Parameters

| Name       | Type   | Description                                        |
|------------|--------|----------------------------------------------------|
| startParam | double | The parameter position of the start of the subset. |
| endParam   | double | The parameter position of the end of the subset.   |

## Version

Introduced in version August 2014  

