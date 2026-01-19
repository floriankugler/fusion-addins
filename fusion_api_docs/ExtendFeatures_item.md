# ExtendFeatures.item Method

Parent Object: [ExtendFeatures](ExtendFeatures.md)  

## Description

Function that returns the specified extend feature using an index into the collection.

## Syntax

"extendFeatures_var" is a variable referencing an [ExtendFeatures](ExtendFeatures.md) object.

```python
returnValue = extendFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ExtendFeature](ExtendFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version June 2015  

