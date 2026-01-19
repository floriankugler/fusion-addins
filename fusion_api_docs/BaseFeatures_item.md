# BaseFeatures.item Method

Parent Object: [BaseFeatures](BaseFeatures.md)  

## Description

Function that returns the specified base feature using an index into the collection.

## Syntax

"baseFeatures_var" is a variable referencing a [BaseFeatures](BaseFeatures.md) object.

```python
returnValue = baseFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [BaseFeature](BaseFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2015  

