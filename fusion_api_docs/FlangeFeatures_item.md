# FlangeFeatures.item Method

Parent Object: [FlangeFeatures](FlangeFeatures.md)  

## Description

Function that returns the specified flange feature using an index into the collection.

## Syntax

"flangeFeatures_var" is a variable referencing a [FlangeFeatures](FlangeFeatures.md) object.

```python
returnValue = flangeFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [FlangeFeature](FlangeFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2020  

