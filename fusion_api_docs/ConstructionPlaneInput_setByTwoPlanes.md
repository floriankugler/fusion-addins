# ConstructionPlaneInput.setByTwoPlanes Method

Parent Object: [ConstructionPlaneInput](ConstructionPlaneInput.md)  

## Description

This input method is for creating a construction plane at the midpoint between two planar faces or construction planes. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionPlaneInput_var" is a variable referencing a [ConstructionPlaneInput](ConstructionPlaneInput.md) object.

```python
returnValue = constructionPlaneInput_var.setByTwoPlanes(planarEntityOne, planarEntityTwo)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionPlaneInput is successful. This will fail if the two planes are co-planar. |

## Parameters

| Name | Type | Description |
|----|----|----|
| planarEntityOne | [Base](Base.md) | The first planar face or construction plane to create a bisecting plane between |
| planarEntityTwo | [Base](Base.md) | The second planar face or construction plane to create a bisecting plane between |

## Samples

| Name | Description |
|----|----|
| [Construction Plane API Sample](ConstructionPlaneSample_Sample.md) | Demonstrates creating construction plane by different ways. |

## Version

Introduced in version August 2014  

