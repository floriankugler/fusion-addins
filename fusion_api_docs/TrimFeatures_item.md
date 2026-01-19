# TrimFeatures.item Method

Parent Object: [TrimFeatures](TrimFeatures.md)  

## Description

Function that returns the specified trim feature using an index into the collection.

## Syntax

"trimFeatures_var" is a variable referencing a [TrimFeatures](TrimFeatures.md) object.

```python
returnValue = trimFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [TrimFeature](TrimFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version July 2015  

