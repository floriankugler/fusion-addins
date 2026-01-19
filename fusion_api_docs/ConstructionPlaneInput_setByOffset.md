# ConstructionPlaneInput.setByOffset Method

Parent Object: [ConstructionPlaneInput](ConstructionPlaneInput.md)  

## Description

This input method is for creating a construction plane that is offset from a planar face or construction plane at a specified distance. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionPlaneInput_var" is a variable referencing a [ConstructionPlaneInput](ConstructionPlaneInput.md) object.

```python
returnValue = constructionPlaneInput_var.setByOffset(planarEntity, offset)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionPlaneInput is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| planarEntity | [Base](Base.md) | A plane, planar face or construction plane from which to create the offset plane |
| offset | [ValueInput](ValueInput.md) | ValueInput object that specifies the offset distance for the plane |

## Samples

| Name | Description |
|----|----|
| [Construction Plane API Sample](ConstructionPlaneSample_Sample.md) | Demonstrates creating construction plane by different ways. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version August 2014  

