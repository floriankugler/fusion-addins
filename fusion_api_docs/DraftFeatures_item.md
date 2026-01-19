# DraftFeatures.item Method

Parent Object: [DraftFeatures](DraftFeatures.md)  

## Description

Function that returns the specified draft feature using an index into the collection.

## Syntax

"draftFeatures_var" is a variable referencing a [DraftFeatures](DraftFeatures.md) object.

```python
returnValue = draftFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [DraftFeature](DraftFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version January 2015  

