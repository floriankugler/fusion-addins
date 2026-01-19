# SilhouetteSplitFeatures.item Method

Parent Object: [SilhouetteSplitFeatures](SilhouetteSplitFeatures.md)  

## Description

Function that returns the specified silhouette split feature using an index into the collection.

## Syntax

"silhouetteSplitFeatures_var" is a variable referencing a [SilhouetteSplitFeatures](SilhouetteSplitFeatures.md) object.

```python
returnValue = silhouetteSplitFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SilhouetteSplitFeature](SilhouetteSplitFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version June 2015  

