# ConstructionPoints.createInput Method

Parent Object: [ConstructionPoints](ConstructionPoints.md)  

## Description

Create a ConstructionPointInput object that is in turn used to create a ConstructionPoint.

## Syntax

"constructionPoints_var" is a variable referencing a [ConstructionPoints](ConstructionPoints.md) object.

```python
# Uses no optional arguments.
returnValue = constructionPoints_var.createInput()

# Uses optional arguments.
returnValue = constructionPoints_var.createInput(occurrenceForCreation)
```

## Return Value

| Type | Description |
|----|----|
| [ConstructionPointInput](ConstructionPointInput.md) | Returns a ConstructionPointInput object |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| occurrenceForCreation | [Occurrence](Occurrence.md) | A creation occurrence is needed if the input is in another component AND the construction point is not in the root component. The occurrenceForCreation is analogous to the active occurrence in the UI. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [Construction Point API Sample](ConstructionPointSample_Sample.md) | Demonstrates creating construction point by different ways |

## Version

Introduced in version August 2014  

