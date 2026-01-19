# DeriveFeatures.item Method

Parent Object: [DeriveFeatures](DeriveFeatures.md)  

## Description

Function that returns the specified derive feature using an index into the collection.

## Syntax

"deriveFeatures_var" is a variable referencing a [DeriveFeatures](DeriveFeatures.md) object.

```python
returnValue = deriveFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [DeriveFeature](DeriveFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version January 2026  

