# ConstructionPlanes.createInput Method

Parent Object: [ConstructionPlanes](ConstructionPlanes.md)  

## Description

Create a ConstructionPlaneInput object that is in turn used to create a ConstructionPlane.

## Syntax

"constructionPlanes_var" is a variable referencing a [ConstructionPlanes](ConstructionPlanes.md) object.

```python
# Uses no optional arguments.
returnValue = constructionPlanes_var.createInput()

# Uses optional arguments.
returnValue = constructionPlanes_var.createInput(occurrenceForCreation)
```

## Return Value

| Type | Description |
|----|----|
| [ConstructionPlaneInput](ConstructionPlaneInput.md) | Returns a ConstructionPlaneInput object |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| occurrenceForCreation | [Occurrence](Occurrence.md) | A creation occurrence is needed if the input is in another component AND the construction plane is not in the root component. The occurrenceForCreation is analogous to the active occurrence in the UI. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [Construction Plane API Sample](ConstructionPlaneSample_Sample.md) | Demonstrates creating construction plane by different ways. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version August 2014  

