# NurbsCurve3D.merge Method

Parent Object: [NurbsCurve3D](NurbsCurve3D.md)  

## Description

Define a new NURBS curve that is the result of combining this NURBS curve with another NURBS curve.

## Syntax

"nurbsCurve3D_var" is a variable referencing a [NurbsCurve3D](NurbsCurve3D.md) object.

```python
returnValue = nurbsCurve3D_var.merge(nurbsCurve)
```

## Return Value

| Type                             | Description                        |
|----------------------------------|------------------------------------|
| [NurbsCurve3D](NurbsCurve3D.md) | Returns a new NurbsCurve3D object. |

## Parameters

| Name | Type | Description |
|----|----|----|
| nurbsCurve | [NurbsCurve3D](NurbsCurve3D.md) | The NURBS curve to combine with. |

## Version

Introduced in version August 2014  

