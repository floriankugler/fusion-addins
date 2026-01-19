# OffsetFeatures.item Method

Parent Object: [OffsetFeatures](OffsetFeatures.md)  

## Description

Function that returns the specified offset feature using an index into the collection.

## Syntax

"offsetFeatures_var" is a variable referencing an [OffsetFeatures](OffsetFeatures.md) object.

```python
returnValue = offsetFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetFeature](OffsetFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version June 2015  

