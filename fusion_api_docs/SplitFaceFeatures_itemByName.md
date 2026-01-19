# SplitFaceFeatures.itemByName Method

Parent Object: [SplitFaceFeatures](SplitFaceFeatures.md)  

## Description

Function that returns the specified split face feature using the name of the feature.

## Syntax

"splitFaceFeatures_var" is a variable referencing a [SplitFaceFeatures](SplitFaceFeatures.md) object.

```python
returnValue = splitFaceFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [SplitFaceFeature](SplitFaceFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

