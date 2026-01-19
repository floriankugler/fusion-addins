# MirrorFeatures.item Method

Parent Object: [MirrorFeatures](MirrorFeatures.md)  

## Description

Function that returns the specified mirror feature using an index into the collection.

## Syntax

"mirrorFeatures_var" is a variable referencing a [MirrorFeatures](MirrorFeatures.md) object.

```python
returnValue = mirrorFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [MirrorFeature](MirrorFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version November 2014  

