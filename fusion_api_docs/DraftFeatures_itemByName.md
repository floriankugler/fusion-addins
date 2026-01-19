# DraftFeatures.itemByName Method

Parent Object: [DraftFeatures](DraftFeatures.md)  

## Description

Function that returns the specified draft feature using the name of the feature.

## Syntax

"draftFeatures_var" is a variable referencing a [DraftFeatures](DraftFeatures.md) object.

```python
returnValue = draftFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [DraftFeature](DraftFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

