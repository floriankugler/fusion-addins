# MoveFeatures.item Method

Parent Object: [MoveFeatures](MoveFeatures.md)  

## Description

Function that returns the specified move feature using an index into the collection.

## Syntax

"moveFeatures_var" is a variable referencing a [MoveFeatures](MoveFeatures.md) object.

```python
returnValue = moveFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [MoveFeature](MoveFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version March 2015  

