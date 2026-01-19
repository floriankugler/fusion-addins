# ReplaceFaceFeatures.item Method

Parent Object: [ReplaceFaceFeatures](ReplaceFaceFeatures.md)  

## Description

Function that returns the specified replace face feature using an index into the collection.

## Syntax

"replaceFaceFeatures_var" is a variable referencing a [ReplaceFaceFeatures](ReplaceFaceFeatures.md) object.

```python
returnValue = replaceFaceFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ReplaceFaceFeature](ReplaceFaceFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version March 2015  

