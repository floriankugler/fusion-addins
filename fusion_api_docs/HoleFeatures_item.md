# HoleFeatures.item Method

Parent Object: [HoleFeatures](HoleFeatures.md)  

## Description

Function that returns the specified hole feature using an index into the collection.

## Syntax

"holeFeatures_var" is a variable referencing a [HoleFeatures](HoleFeatures.md) object.

```python
returnValue = holeFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [HoleFeature](HoleFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

