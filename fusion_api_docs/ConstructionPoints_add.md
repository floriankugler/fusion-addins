# ConstructionPoints.add Method

Parent Object: [ConstructionPoints](ConstructionPoints.md)  

## Description

Creates a new construction point.  

If the ConstructionPointInput was defined using the setByPoint method using a Point3D object then the add will only work in the direct modeling mode and will fail in the parametric modeling mode.

## Syntax

"constructionPoints_var" is a variable referencing a [ConstructionPoints](ConstructionPoints.md) object.

```python
returnValue = constructionPoints_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [ConstructionPoint](ConstructionPoint.md) | Returns the newly created construction point or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [ConstructionPointInput](ConstructionPointInput.md) | A ConstructionPointInput object |

## Samples

| Name | Description |
|----|----|
| [Construction Point API Sample](ConstructionPointSample_Sample.md) | Demonstrates creating construction point by different ways |

## Version

Introduced in version August 2014  

