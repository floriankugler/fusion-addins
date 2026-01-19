# OffsetFeatures.itemByName Method

Parent Object: [OffsetFeatures](OffsetFeatures.md)  

## Description

Function that returns the specified offset feature using the name of the feature.

## Syntax

"offsetFeatures_var" is a variable referencing an [OffsetFeatures](OffsetFeatures.md) object.

```python
returnValue = offsetFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetFeature](OffsetFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

