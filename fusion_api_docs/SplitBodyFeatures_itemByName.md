# SplitBodyFeatures.itemByName Method

Parent Object: [SplitBodyFeatures](SplitBodyFeatures.md)  

## Description

Function that returns the specified split body feature using the name of the feature.

## Syntax

"splitBodyFeatures_var" is a variable referencing a [SplitBodyFeatures](SplitBodyFeatures.md) object.

```python
returnValue = splitBodyFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [SplitBodyFeature](SplitBodyFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

