# CircularPatternFeatures.item Method

Parent Object: [CircularPatternFeatures](CircularPatternFeatures.md)  

## Description

Function that returns the specified circular pattern feature using an index into the collection.

## Syntax

"circularPatternFeatures_var" is a variable referencing a [CircularPatternFeatures](CircularPatternFeatures.md) object.

```python
returnValue = circularPatternFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CircularPatternFeature](CircularPatternFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version November 2014  

