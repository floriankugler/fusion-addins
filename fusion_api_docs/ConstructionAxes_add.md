# ConstructionAxes.add Method

Parent Object: [ConstructionAxes](ConstructionAxes.md)  

## Description

Creates and adds a new ConstructionAxis using the creation parameters in the ConstructionAxisInput.  

If the ConstructionAxisInput was defined using the setByLine method then the add will only work in the direct modeling mode and will fail in the parametric modeling mode.

## Syntax

"constructionAxes_var" is a variable referencing a [ConstructionAxes](ConstructionAxes.md) object.

```python
returnValue = constructionAxes_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [ConstructionAxis](ConstructionAxis.md) | Returns the newly created construction axis or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [ConstructionAxisInput](ConstructionAxisInput.md) | A ConstructionAxisInput object |

## Samples

| Name | Description |
|----|----|
| [Construction Axis API Sample](ConstructionAxisSample_Sample.md) | Demonstrates creating construction axis in various ways. |

## Version

Introduced in version August 2014  

