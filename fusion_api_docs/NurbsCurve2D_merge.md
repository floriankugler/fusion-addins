# NurbsCurve2D.merge Method

Parent Object: [NurbsCurve2D](NurbsCurve2D.md)  

## Description

Define a new NURBS curve that is the result of combining this NURBS curve with another NURBS curve. The curves are merged with the end point of the current curve merging with the start point of the other curve. The curves are forced to join even if they are not physically touching so you will typically want to make sure the end and start points of the curves are where you expect them to be.

## Syntax

"nurbsCurve2D_var" is a variable referencing a [NurbsCurve2D](NurbsCurve2D.md) object.

```python
returnValue = nurbsCurve2D_var.merge(nurbsCurve)
```

## Return Value

| Type                             | Description                        |
|----------------------------------|------------------------------------|
| [NurbsCurve2D](NurbsCurve2D.md) | Returns a new NurbsCurve2D object. |

## Parameters

| Name | Type | Description |
|----|----|----|
| nurbsCurve | [NurbsCurve2D](NurbsCurve2D.md) | The NURBS curve to combine with |

## Version

Introduced in version August 2014  

