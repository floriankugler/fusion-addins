# SweepFeatures.item Method

Parent Object: [SweepFeatures](SweepFeatures.md)  

## Description

Function that returns the specified sweep feature using an index into the collection.

## Syntax

"sweepFeatures_var" is a variable referencing a [SweepFeatures](SweepFeatures.md) object.

```python
returnValue = sweepFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SweepFeature](SweepFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version November 2014  

