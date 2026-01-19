# SilhouetteSplitFeatures.itemByName Method

Parent Object: [SilhouetteSplitFeatures](SilhouetteSplitFeatures.md)  

## Description

Function that returns the specified silhouette split feature using the name of the feature.

## Syntax

"silhouetteSplitFeatures_var" is a variable referencing a [SilhouetteSplitFeatures](SilhouetteSplitFeatures.md) object.

```python
returnValue = silhouetteSplitFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [SilhouetteSplitFeature](SilhouetteSplitFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

