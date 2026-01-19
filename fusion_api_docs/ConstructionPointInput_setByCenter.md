# ConstructionPointInput.setByCenter Method

Parent Object: [ConstructionPointInput](ConstructionPointInput.md)  

## Description

This input method is for creating a construction point at the center of a spherical face (sphere or torus), circular edge or sketch arc/circle This can result in a parametric or non-parametric construction point depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionPointInput_var" is a variable referencing a [ConstructionPointInput](ConstructionPointInput.md) object.

```python
returnValue = constructionPointInput_var.setByCenter(circularEntity)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionPointInput is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| circularEntity | [Base](Base.md) | A spherical face (sphere or torus), circular edge or sketch arc/circle |

## Samples

| Name | Description |
|----|----|
| [Construction Point API Sample](ConstructionPointSample_Sample.md) | Demonstrates creating construction point by different ways |

## Version

Introduced in version August 2014  

