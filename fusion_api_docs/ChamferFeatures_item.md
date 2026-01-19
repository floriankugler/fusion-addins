# ChamferFeatures.item Method

Parent Object: [ChamferFeatures](ChamferFeatures.md)  

## Description

Function that returns the specified chamfer feature using an index into the collection.

## Syntax

"chamferFeatures_var" is a variable referencing a [ChamferFeatures](ChamferFeatures.md) object.

```python
returnValue = chamferFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ChamferFeature](ChamferFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version November 2014  

