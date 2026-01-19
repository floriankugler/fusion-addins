# ScaleFeatures.item Method

Parent Object: [ScaleFeatures](ScaleFeatures.md)  

## Description

Function that returns the specified scale feature using an index into the collection.

## Syntax

"scaleFeatures_var" is a variable referencing a [ScaleFeatures](ScaleFeatures.md) object.

```python
returnValue = scaleFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ScaleFeature](ScaleFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version January 2015  

