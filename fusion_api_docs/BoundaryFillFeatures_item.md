# BoundaryFillFeatures.item Method

Parent Object: [BoundaryFillFeatures](BoundaryFillFeatures.md)  

## Description

Function that returns the specified boundary fill feature using an index into the collection.

## Syntax

"boundaryFillFeatures_var" is a variable referencing a [BoundaryFillFeatures](BoundaryFillFeatures.md) object.

```python
returnValue = boundaryFillFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BoundaryFillFeature](BoundaryFillFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version June 2015  

