# ConstructionPlanes.add Method

Parent Object: [ConstructionPlanes](ConstructionPlanes.md)  

## Description

Creates and adds a new ConstructionPlane using the creation parameters in the ConstructionPlaneInput.  

If the ConstructionPlaneInput was defined using the setByPlane method then the add will only work in the direct modeling model and will fail in the parametric modeling mode.

## Syntax

"constructionPlanes_var" is a variable referencing a [ConstructionPlanes](ConstructionPlanes.md) object.

```python
returnValue = constructionPlanes_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [ConstructionPlane](ConstructionPlane.md) | Returns the newly created construction plane or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [ConstructionPlaneInput](ConstructionPlaneInput.md) | A ConstructionPlaneInput object |

## Samples

| Name | Description |
|----|----|
| [Construction Plane API Sample](ConstructionPlaneSample_Sample.md) | Demonstrates creating construction plane by different ways. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version August 2014  

