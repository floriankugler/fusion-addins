# PathPatternFeatures.item Method

Parent Object: [PathPatternFeatures](PathPatternFeatures.md)  

## Description

Function that returns the specified path pattern feature using an index into the collection.

## Syntax

"pathPatternFeatures_var" is a variable referencing a [PathPatternFeatures](PathPatternFeatures.md) object.

```python
returnValue = pathPatternFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [PathPatternFeature](PathPatternFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version November 2014  

