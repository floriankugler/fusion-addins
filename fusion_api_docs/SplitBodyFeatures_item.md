# SplitBodyFeatures.item Method

Parent Object: [SplitBodyFeatures](SplitBodyFeatures.md)  

## Description

Function that returns the specified split body feature using an index into the collection.

## Syntax

"splitBodyFeatures_var" is a variable referencing a [SplitBodyFeatures](SplitBodyFeatures.md) object.

```python
returnValue = splitBodyFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SplitBodyFeature](SplitBodyFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version June 2015  

