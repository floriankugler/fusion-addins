# ThreadFeatures.item Method

Parent Object: [ThreadFeatures](ThreadFeatures.md)  

## Description

Function that returns the specified thread feature using an index into the collection.

## Syntax

"threadFeatures_var" is a variable referencing a [ThreadFeatures](ThreadFeatures.md) object.

```python
returnValue = threadFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ThreadFeature](ThreadFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version January 2015  

