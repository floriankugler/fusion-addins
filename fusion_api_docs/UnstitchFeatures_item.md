# UnstitchFeatures.item Method

Parent Object: [UnstitchFeatures](UnstitchFeatures.md)  

## Description

Function that returns the specified Unstitch feature using an index into the collection.

## Syntax

"unstitchFeatures_var" is a variable referencing a [UnstitchFeatures](UnstitchFeatures.md) object.

```python
returnValue = unstitchFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [UnstitchFeature](UnstitchFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version July 2015  

