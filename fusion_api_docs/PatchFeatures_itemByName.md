# PatchFeatures.itemByName Method

Parent Object: [PatchFeatures](PatchFeatures.md)  

## Description

Function that returns the specified patch feature using the name of the feature.

## Syntax

"patchFeatures_var" is a variable referencing a [PatchFeatures](PatchFeatures.md) object.

```python
returnValue = patchFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [PatchFeature](PatchFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

