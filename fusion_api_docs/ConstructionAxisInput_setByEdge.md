# ConstructionAxisInput.setByEdge Method

Parent Object: [ConstructionAxisInput](ConstructionAxisInput.md)  

## Description

This input method is for creating a construction axis from a specified linear/circular edge or sketch curve. This can result in a parametric or non-parametric construction axis depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionAxisInput_var" is a variable referencing a [ConstructionAxisInput](ConstructionAxisInput.md) object.

```python
returnValue = constructionAxisInput_var.setByEdge(edgeEntity)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionAxisInput is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| edgeEntity | [Base](Base.md) | A linear/circular edge, construction line, or sketch line |

## Samples

| Name | Description |
|----|----|
| [Construction Axis API Sample](ConstructionAxisSample_Sample.md) | Demonstrates creating construction axis in various ways. |

## Version

Introduced in version August 2014  

