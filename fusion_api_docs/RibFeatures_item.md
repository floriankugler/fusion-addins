# RibFeatures.item Method

Parent Object: [RibFeatures](RibFeatures.md)  

## Description

Function that returns the specified Rib feature using an index into the collection.

## Syntax

"ribFeatures_var" is a variable referencing a [RibFeatures](RibFeatures.md) object.

```python
returnValue = ribFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [RibFeature](RibFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2015  

