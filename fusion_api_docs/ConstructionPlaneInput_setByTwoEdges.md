# ConstructionPlaneInput.setByTwoEdges Method

Parent Object: [ConstructionPlaneInput](ConstructionPlaneInput.md)  

## Description

This input method is for creating a construction plane that passes through two coplanar linear entities or axes. Defines a plane by specifying two coplanar linear entities. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionPlaneInput_var" is a variable referencing a [ConstructionPlaneInput](ConstructionPlaneInput.md) object.

```python
returnValue = constructionPlaneInput_var.setByTwoEdges(linearEntityOne, linearEntityTwo)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionPlaneInput is successful. This will fail if the two linear entities are not coplanar. |

## Parameters

| Name | Type | Description |
|----|----|----|
| linearEntityOne | [Base](Base.md) | The first of two coplanar linear entities to define the plane |
| linearEntityTwo | [Base](Base.md) | The second of two coplanar linear entities to define the plane |

## Samples

| Name | Description |
|----|----|
| [Construction Plane API Sample](ConstructionPlaneSample_Sample.md) | Demonstrates creating construction plane by different ways. |

## Version

Introduced in version August 2014  

