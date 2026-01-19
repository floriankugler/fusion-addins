# ConstructionAxisInput.setByTwoPlanes Method

Parent Object: [ConstructionAxisInput](ConstructionAxisInput.md)  

## Description

This input method is for creating a construction axis coincident with the intersection of two planes or planar faces. This will fail if the two planes are parallel. This can result in a parametric or non-parametric construction axis depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionAxisInput_var" is a variable referencing a [ConstructionAxisInput](ConstructionAxisInput.md) object.

```python
returnValue = constructionAxisInput_var.setByTwoPlanes(planarEntityOne, planarEntityTwo)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionAxisInput is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| planarEntityOne | [Base](Base.md) | The first planar face or construction plane to intersect |
| planarEntityTwo | [Base](Base.md) | The second planar face or construction plane to intersect |

## Samples

| Name | Description |
|----|----|
| [Construction Axis API Sample](ConstructionAxisSample_Sample.md) | Demonstrates creating construction axis in various ways. |

## Version

Introduced in version August 2014  

