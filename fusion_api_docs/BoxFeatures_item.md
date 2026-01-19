# BoxFeatures.item Method

Parent Object: [BoxFeatures](BoxFeatures.md)  

## Description

Function that returns the specified box feature using an index into the collection.

## Syntax

"boxFeatures_var" is a variable referencing a [BoxFeatures](BoxFeatures.md) object.

```python
returnValue = boxFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BoxFeature](BoxFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2015  

