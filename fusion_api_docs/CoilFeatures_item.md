# CoilFeatures.item Method

Parent Object: [CoilFeatures](CoilFeatures.md)  

## Description

Function that returns the specified coil feature using an index into the collection.

## Syntax

"coilFeatures_var" is a variable referencing a [CoilFeatures](CoilFeatures.md) object.

```python
returnValue = coilFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CoilFeature](CoilFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version March 2015  

