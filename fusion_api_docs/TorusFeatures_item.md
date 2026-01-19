# TorusFeatures.item Method

Parent Object: [TorusFeatures](TorusFeatures.md)  

## Description

Function that returns the specified torus feature using an index into the collection.

## Syntax

"torusFeatures_var" is a variable referencing a [TorusFeatures](TorusFeatures.md) object.

```python
returnValue = torusFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [TorusFeature](TorusFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2015  

