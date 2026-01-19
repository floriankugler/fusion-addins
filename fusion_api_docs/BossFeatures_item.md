# BossFeatures.item Method

Parent Object: [BossFeatures](BossFeatures.md)  

## Description

Function that returns the specified boss feature using an index into the collection.

## Syntax

"bossFeatures_var" is a variable referencing a [BossFeatures](BossFeatures.md) object.

```python
returnValue = bossFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BossFeature](BossFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version October 2022  

