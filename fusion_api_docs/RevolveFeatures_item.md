# RevolveFeatures.item Method

Parent Object: [RevolveFeatures](RevolveFeatures.md)  

## Description

Function that returns the specified revolve feature using an index into the collection.

## Syntax

"revolveFeatures_var" is a variable referencing a [RevolveFeatures](RevolveFeatures.md) object.

```python
returnValue = revolveFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [RevolveFeature](RevolveFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

