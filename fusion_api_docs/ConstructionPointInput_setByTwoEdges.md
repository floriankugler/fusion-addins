# ConstructionPointInput.setByTwoEdges Method

Parent Object: [ConstructionPointInput](ConstructionPointInput.md)  

## Description

This input method is for creating a construction point at the intersection of the two linear edges or sketch lines. The edges can be B-Rep edges or sketch lines. This can result in a parametric or non-parametric construction point depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionPointInput_var" is a variable referencing a [ConstructionPointInput](ConstructionPointInput.md) object.

```python
returnValue = constructionPointInput_var.setByTwoEdges(edgeOne, edgeTwo)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionPointInput is successful. |

## Parameters

| Name    | Type             | Description                          |
|---------|------------------|--------------------------------------|
| edgeOne | [Base](Base.md) | The first B-Rep edge or sketch line  |
| edgeTwo | [Base](Base.md) | The second B-Rep edge or sketch line |

## Samples

| Name | Description |
|----|----|
| [Construction Point API Sample](ConstructionPointSample_Sample.md) | Demonstrates creating construction point by different ways |

## Version

Introduced in version August 2014  

