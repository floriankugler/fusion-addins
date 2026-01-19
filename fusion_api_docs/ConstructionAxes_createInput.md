# ConstructionAxes.createInput Method

Parent Object: [ConstructionAxes](ConstructionAxes.md)  

## Description

Create a ConstructionAxisInput object that is in turn used to create a ConstructionAxis.

## Syntax

"constructionAxes_var" is a variable referencing a [ConstructionAxes](ConstructionAxes.md) object.

```python
# Uses no optional arguments.
returnValue = constructionAxes_var.createInput()

# Uses optional arguments.
returnValue = constructionAxes_var.createInput(occurrenceForCreation)
```

## Return Value

| Type | Description |
|----|----|
| [ConstructionAxisInput](ConstructionAxisInput.md) | Returns a ConstructionAxisInput object |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| occurrenceForCreation | [Occurrence](Occurrence.md) | A creation occurrence is needed if the input is in another component AND the construction axis is not in the root component. The occurrenceForCreation is analogous to the active occurrence in the UI. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [Construction Axis API Sample](ConstructionAxisSample_Sample.md) | Demonstrates creating construction axis in various ways. |

## Version

Introduced in version August 2014  

