# ConstructionAxisInput.setByTwoPoints Method

Parent Object: [ConstructionAxisInput](ConstructionAxisInput.md)  

## Description

This input method is for creating a construction axis that passes through the two points (work points, sketch points or vertices). This will fail if the two points are coincident. This can result in a parametric or non-parametric construction axis depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionAxisInput_var" is a variable referencing a [ConstructionAxisInput](ConstructionAxisInput.md) object.

```python
returnValue = constructionAxisInput_var.setByTwoPoints(pointEntityOne, pointEntityTwo)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionAxisInput is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointEntityOne | [Base](Base.md) | The first construction point, sketch point or vertex the axis passes through |
| pointEntityTwo | [Base](Base.md) | The second construction point, sketch point or vertex the axis passes through |

## Samples

| Name | Description |
|----|----|
| [Construction Axis API Sample](ConstructionAxisSample_Sample.md) | Demonstrates creating construction axis in various ways. |

## Version

Introduced in version August 2014  

