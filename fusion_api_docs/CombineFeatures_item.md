# CombineFeatures.item Method

Parent Object: [CombineFeatures](CombineFeatures.md)  

## Description

Function that returns the specified combine feature using an index into the collection.

## Syntax

"combineFeatures_var" is a variable referencing a [CombineFeatures](CombineFeatures.md) object.

```python
returnValue = combineFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CombineFeature](CombineFeature.md) | Returns the specified item or null if an invalid index was specified. This property returns nothing in the case where the feature is non-parametric. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version November 2014  

