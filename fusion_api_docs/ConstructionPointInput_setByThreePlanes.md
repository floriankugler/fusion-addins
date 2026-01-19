# ConstructionPointInput.setByThreePlanes Method

Parent Object: [ConstructionPointInput](ConstructionPointInput.md)  

## Description

This input method is for creating a construction point at the intersection of the three planes or planar faces. This can result in a parametric or non-parametric construction point depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionPointInput_var" is a variable referencing a [ConstructionPointInput](ConstructionPointInput.md) object.

```python
returnValue = constructionPointInput_var.setByThreePlanes(planeOne, planeTwo, planeThree)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionPointInput is successful. |

## Parameters

| Name       | Type             | Description                                  |
|------------|------------------|----------------------------------------------|
| planeOne   | [Base](Base.md) | The first plane or planar face to intersect  |
| planeTwo   | [Base](Base.md) | The second plane or planar face to intersect |
| planeThree | [Base](Base.md) | The third plane or planar face to intersect  |

## Samples

| Name | Description |
|----|----|
| [Construction Point API Sample](ConstructionPointSample_Sample.md) | Demonstrates creating construction point by different ways |

## Version

Introduced in version August 2014  

