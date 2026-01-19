# ConstructionAxisInput.setByLine Method

Parent Object: [ConstructionAxisInput](ConstructionAxisInput.md)  

## Description

This input method is for creating a non-parametric construction axis whose position in space is defined by an InfiniteLine3D object.  

This method of defining a construction axis is only valid when working in the direct modeling mode. This is not valid when working in the parametric modeling mode and will fail.

## Syntax

"constructionAxisInput_var" is a variable referencing a [ConstructionAxisInput](ConstructionAxisInput.md) object.

```python
returnValue = constructionAxisInput_var.setByLine(line)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionAxisInput is successful. |

## Parameters

| Name | Type                                 | Description              |
|------|--------------------------------------|--------------------------|
| line | [InfiniteLine3D](InfiniteLine3D.md) | An InFiniteLine3D object |

## Samples

| Name | Description |
|----|----|
| [Construction Axis API Sample](ConstructionAxisSample_Sample.md) | Demonstrates creating construction axis in various ways. |

## Version

Introduced in version August 2014  

