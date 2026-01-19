# RemoveFeatures.item Method

Parent Object: [RemoveFeatures](RemoveFeatures.md)  

## Description

Function that returns the specified Remove feature using an index into the collection.

## Syntax

"removeFeatures_var" is a variable referencing a [RemoveFeatures](RemoveFeatures.md) object.

```python
returnValue = removeFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [RemoveFeature](RemoveFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2015  

