# UnfoldFeatures.item Method

Parent Object: [UnfoldFeatures](UnfoldFeatures.md)  

## Description

Function that returns the specified unfold feature using an index into the collection.

## Syntax

"unfoldFeatures_var" is a variable referencing a [UnfoldFeatures](UnfoldFeatures.md) object.

```python
returnValue = unfoldFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [UnfoldFeature](UnfoldFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2020  

