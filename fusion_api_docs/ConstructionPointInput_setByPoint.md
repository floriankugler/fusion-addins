# ConstructionPointInput.setByPoint Method

Parent Object: [ConstructionPointInput](ConstructionPointInput.md)  

## Description

This input method is for creating a construction point on the specified point or vertex. The point can be either a B-Rep vertex, SketchPoint, or a Point3D object.  

Providing a Point3D object is only valid when working in the direct edit modeling mode. This is not valid when working in the parametric modeling mode and will fail.  

Even when providing a B-Rep vertex, or SketchPoint the result will be non-parametric if the parent component is a direct edit component.

## Syntax

"constructionPointInput_var" is a variable referencing a [ConstructionPointInput](ConstructionPointInput.md) object.

```python
returnValue = constructionPointInput_var.setByPoint(point)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionPointInput is successful. |

## Parameters

| Name  | Type             | Description                                  |
|-------|------------------|----------------------------------------------|
| point | [Base](Base.md) | A B-Rep vertex, SketchPoint, or Point object |

## Samples

| Name | Description |
|----|----|
| [Construction Point API Sample](ConstructionPointSample_Sample.md) | Demonstrates creating construction point by different ways |

## Version

Introduced in version August 2014  

