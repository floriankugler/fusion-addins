# LoftFeatures.item Method

Parent Object: [LoftFeatures](LoftFeatures.md)  

## Description

Function that returns the specified loft feature using an index into the collection.

## Syntax

"loftFeatures_var" is a variable referencing a [LoftFeatures](LoftFeatures.md) object.

```python
returnValue = loftFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [LoftFeature](LoftFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2015  

