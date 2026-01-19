# RefoldFeatures.item Method

Parent Object: [RefoldFeatures](RefoldFeatures.md)  

## Description

Function that returns the specified refold feature using an index into the collection.

## Syntax

"refoldFeatures_var" is a variable referencing a [RefoldFeatures](RefoldFeatures.md) object.

```python
returnValue = refoldFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [RefoldFeature](RefoldFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2020  

