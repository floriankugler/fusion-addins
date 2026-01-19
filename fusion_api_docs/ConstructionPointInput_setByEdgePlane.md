# ConstructionPointInput.setByEdgePlane Method

Parent Object: [ConstructionPointInput](ConstructionPointInput.md)  

## Description

This input method is for creating a construction point at the intersection of a construction plane, planar face or sketch profile and a linear edge, construction axis or sketch line. This can result in a parametric or non-parametric construction point depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionPointInput_var" is a variable referencing a [ConstructionPointInput](ConstructionPointInput.md) object.

```python
returnValue = constructionPointInput_var.setByEdgePlane(edge, plane)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionPointInput is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| edge | [Base](Base.md) | A linear B-Rep edge, construction axis or sketch line. |
| plane | [Base](Base.md) | A plane, planar B-Rep face or construction plane. |

## Samples

| Name | Description |
|----|----|
| [Construction Point API Sample](ConstructionPointSample_Sample.md) | Demonstrates creating construction point by different ways |

## Version

Introduced in version August 2014  

